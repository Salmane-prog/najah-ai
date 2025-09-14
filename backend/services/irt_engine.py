#!/usr/bin/env python3
"""
Moteur IRT (Item Response Theory) pour Najah AI
Adaptation intelligente de la difficulté et prédiction de performance
"""

import numpy as np
import json
from typing import Dict, List, Any, Tuple, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta
import sqlite3
from scipy.stats import norm
from scipy.optimize import minimize
import math

@dataclass
class IRTParameters:
    """Paramètres IRT d'une question"""
    question_id: int
    difficulty: float          # Paramètre b (difficulté)
    discrimination: float      # Paramètre a (discrimination)
    guessing: float           # Paramètre c (pseudo-guessing)
    confidence: float         # Niveau de confiance des paramètres

@dataclass
class StudentAbility:
    """Niveau de compétence estimé de l'étudiant"""
    student_id: int
    ability_estimate: float   # Estimation de la compétence (thêta)
    standard_error: float     # Erreur standard de l'estimation
    confidence_interval: Tuple[float, float]  # Intervalle de confiance
    last_updated: datetime

class IRTEngine:
    """Moteur IRT pour l'adaptation intelligente et la prédiction"""
    
    def __init__(self, db_path: str = "../data/app.db"):
        self.db_path = db_path
        self.default_discrimination = 1.0
        self.default_guessing = 0.25  # 25% de chance de deviner pour QCM à 4 choix
        
        # Seuils d'adaptation
        self.adaptation_thresholds = {
            "very_easy": 0.9,    # > 90% = augmenter la difficulté
            "easy": 0.8,         # > 80% = légère augmentation
            "optimal": 0.7,      # 60-80% = niveau optimal
            "difficult": 0.6,    # < 60% = légère diminution
            "very_difficult": 0.4  # < 40% = diminuer significativement
        }
    
    def estimate_student_ability(self, student_id: int, subject: str = None) -> StudentAbility:
        """Estime le niveau de compétence de l'étudiant avec IRT"""
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # Récupérer l'historique des réponses
            query = """
                SELECT 
                    qr.quiz_id,
                    qr.percentage,
                    q.difficulty,
                    qr.created_at,
                    q.subject
                FROM quiz_results qr
                JOIN quizzes q ON qr.quiz_id = q.id
                WHERE qr.user_id = ?
            """
            
            params = [student_id]
            if subject:
                query += " AND q.subject = ?"
                params.append(subject)
            
            query += " ORDER BY qr.created_at DESC LIMIT 50"
            
            cursor.execute(query, params)
            responses = cursor.fetchall()
            
            if not responses:
                return StudentAbility(
                    student_id=student_id,
                    ability_estimate=0.0,
                    standard_error=1.0,
                    confidence_interval=(-2.0, 2.0),
                    last_updated=datetime.utcnow()
                )
            
            # Convertir les difficultés en échelle IRT
            difficulty_mapping = {"easy": -1.0, "medium": 0.0, "hard": 1.0}
            
            # Préparer les données pour l'estimation IRT
            difficulties = []
            responses_binary = []
            weights = []
            
            for response in responses:
                quiz_id, percentage, difficulty, created_at, subject = response
                
                # Convertir le pourcentage en réponse binaire (correct/incorrect)
                is_correct = 1 if percentage >= 70 else 0
                
                # Convertir la difficulté textuelle en valeur numérique
                irt_difficulty = difficulty_mapping.get(difficulty, 0.0)
                
                # Poids temporel (réponses récentes ont plus de poids)
                days_ago = (datetime.utcnow() - datetime.fromisoformat(created_at)).days
                weight = max(0.1, 1.0 - (days_ago * 0.05))  # Décroissance temporelle
                
                difficulties.append(irt_difficulty)
                responses_binary.append(is_correct)
                weights.append(weight)
            
            # Estimation IRT simplifiée (modèle de Rasch)
            ability_estimate = self._estimate_ability_rasch(difficulties, responses_binary, weights)
            
            # Calcul de l'erreur standard
            standard_error = self._calculate_standard_error(difficulties, responses_binary, weights)
            
            # Intervalle de confiance (95%)
            confidence_interval = (
                ability_estimate - 1.96 * standard_error,
                ability_estimate + 1.96 * standard_error
            )
            
            return StudentAbility(
                student_id=student_id,
                ability_estimate=ability_estimate,
                standard_error=standard_error,
                confidence_interval=confidence_interval,
                last_updated=datetime.utcnow()
            )
            
        finally:
            conn.close()
    
    def _estimate_ability_rasch(self, difficulties: List[float], responses: List[int], weights: List[float]) -> float:
        """Estimation de la compétence avec le modèle de Rasch simplifié"""
        
        if not responses:
            return 0.0
        
        # Modèle de Rasch : P(correct) = 1 / (1 + exp(-(theta - b)))
        # où theta est la compétence et b est la difficulté
        
        def rasch_likelihood(theta):
            """Fonction de vraisemblance du modèle de Rasch"""
            log_likelihood = 0.0
            
            for i, (difficulty, response, weight) in enumerate(zip(difficulties, responses, weights)):
                # Probabilité de réponse correcte selon le modèle de Rasch
                p_correct = 1.0 / (1.0 + math.exp(-(theta - difficulty)))
                
                # Log-vraisemblance pondérée
                if response == 1:  # Réponse correcte
                    log_likelihood += weight * math.log(p_correct)
                else:  # Réponse incorrecte
                    log_likelihood += weight * math.log(1.0 - p_correct)
            
            return -log_likelihood  # Minimiser la log-vraisemblance négative
        
        # Estimation par maximum de vraisemblance
        try:
            result = minimize(rasch_likelihood, x0=0.0, method='L-BFGS-B', bounds=[(-3.0, 3.0)])
            if result.success:
                return result.x[0]
            else:
                return 0.0
        except:
            return 0.0
    
    def _calculate_standard_error(self, difficulties: List[float], responses: List[int], weights: List[float]) -> float:
        """Calcule l'erreur standard de l'estimation de compétence"""
        
        if len(responses) < 5:
            return 1.0  # Erreur élevée si peu de données
        
        # Erreur standard basée sur la quantité et la qualité des données
        n_responses = len(responses)
        avg_weight = np.mean(weights)
        
        # Erreur standard = 1 / sqrt(information totale)
        # Information totale = somme des informations des items
        total_information = 0.0
        
        for difficulty, weight in zip(difficulties, weights):
            # Information d'un item = p * (1-p) * weight
            # où p est la probabilité de réponse correcte
            p = 1.0 / (1.0 + math.exp(-(0.0 - difficulty)))  # Probabilité pour theta = 0
            item_information = p * (1.0 - p) * weight
            total_information += item_information
        
        if total_information > 0:
            standard_error = 1.0 / math.sqrt(total_information)
            return min(standard_error, 2.0)  # Limiter l'erreur standard
        else:
            return 1.0
    
    def predict_performance(self, student_ability: float, question_difficulty: float) -> Dict[str, Any]:
        """Prédit la performance d'un étudiant sur une question donnée"""
        
        # Modèle de Rasch : P(correct) = 1 / (1 + exp(-(theta - b)))
        difficulty_irt = self._convert_difficulty_to_irt(question_difficulty)
        
        # Probabilité de réponse correcte
        p_correct = 1.0 / (1.0 + math.exp(-(student_ability - difficulty_irt)))
        
        # Prédiction du score
        predicted_score = p_correct * 100
        
        # Niveau de confiance de la prédiction
        confidence_level = self._calculate_prediction_confidence(student_ability, difficulty_irt)
        
        # Recommandation de difficulté
        recommended_difficulty = self._recommend_difficulty(predicted_score)
        
        return {
            "predicted_score": round(predicted_score, 1),
            "probability_correct": round(p_correct, 3),
            "confidence_level": confidence_level,
            "recommended_difficulty": recommended_difficulty,
            "ability_difficulty_gap": round(student_ability - difficulty_irt, 2)
        }
    
    def _convert_difficulty_to_irt(self, difficulty_text: str) -> float:
        """Convertit la difficulté textuelle en échelle IRT"""
        mapping = {
            "very_easy": -2.0,
            "easy": -1.0,
            "medium": 0.0,
            "hard": 1.0,
            "very_hard": 2.0
        }
        return mapping.get(difficulty_text, 0.0)
    
    def _calculate_prediction_confidence(self, ability: float, difficulty: float) -> str:
        """Calcule le niveau de confiance de la prédiction"""
        
        gap = abs(ability - difficulty)
        
        if gap < 0.5:
            return "high"      # Compétence et difficulté bien alignées
        elif gap < 1.0:
            return "medium"    # Alignement modéré
        else:
            return "low"       # Mauvaise correspondance
    
    def _recommend_difficulty(self, predicted_score: float) -> str:
        """Recommandation de difficulté basée sur la prédiction"""
        
        if predicted_score > 90:
            return "increase"      # Augmenter la difficulté
        elif predicted_score > 80:
            return "slight_increase"  # Légère augmentation
        elif predicted_score > 60:
            return "maintain"      # Maintenir le niveau
        elif predicted_score > 40:
            return "slight_decrease"  # Légère diminution
        else:
            return "decrease"      # Diminuer la difficulté
    
    def adapt_difficulty_irt(self, student_ability: float, current_difficulty: str, 
                            last_performance: float, question_count: int) -> Dict[str, Any]:
        """Adapte la difficulté de manière intelligente avec IRT"""
        
        current_difficulty_irt = self._convert_difficulty_to_irt(current_difficulty)
        
        # Prédiction de performance sur la difficulté actuelle
        performance_prediction = self.predict_performance(student_ability, current_difficulty)
        
        # Analyse de la performance réelle vs prédite
        performance_gap = last_performance - performance_prediction["predicted_score"]
        
        # Calcul de la nouvelle difficulté optimale
        optimal_difficulty_irt = self._calculate_optimal_difficulty(
            student_ability, performance_gap, question_count
        )
        
        # Conversion en difficulté textuelle
        new_difficulty = self._convert_irt_to_difficulty(optimal_difficulty_irt)
        
        # Justification de l'adaptation
        adaptation_reason = self._generate_adaptation_reason(
            current_difficulty_irt, optimal_difficulty_irt, performance_gap
        )
        
        return {
            "current_difficulty": current_difficulty,
            "new_difficulty": new_difficulty,
            "current_difficulty_irt": round(current_difficulty_irt, 2),
            "optimal_difficulty_irt": round(optimal_difficulty_irt, 2),
            "performance_gap": round(performance_gap, 1),
            "adaptation_reason": adaptation_reason,
            "confidence": performance_prediction["confidence_level"]
        }
    
    def _calculate_optimal_difficulty(self, ability: float, performance_gap: float, question_count: int) -> float:
        """Calcule la difficulté optimale selon IRT"""
        
        # Principe : la difficulté optimale est proche de la compétence de l'étudiant
        # avec un ajustement basé sur la performance récente
        
        # Facteur d'ajustement basé sur la performance
        if question_count < 5:
            # Peu de questions = adaptation conservatrice
            adjustment_factor = 0.3
        else:
            # Plus de questions = adaptation plus agressive
            adjustment_factor = 0.5
        
        # Ajustement basé sur la performance
        if performance_gap > 20:
            # Performance meilleure que prédite = augmenter la difficulté
            adjustment = adjustment_factor * min(performance_gap / 100, 0.5)
        elif performance_gap < -20:
            # Performance moins bonne que prédite = diminuer la difficulté
            adjustment = -adjustment_factor * min(abs(performance_gap) / 100, 0.5)
        else:
            # Performance dans la marge = ajustement minimal
            adjustment = 0.0
        
        # Calcul de la difficulté optimale
        optimal_difficulty = ability + adjustment
        
        # Limiter la difficulté dans une plage raisonnable
        return max(-2.0, min(2.0, optimal_difficulty))
    
    def _convert_irt_to_difficulty(self, irt_value: float) -> str:
        """Convertit une valeur IRT en difficulté textuelle"""
        
        if irt_value < -1.5:
            return "very_easy"
        elif irt_value < -0.5:
            return "easy"
        elif irt_value < 0.5:
            return "medium"
        elif irt_value < 1.5:
            return "hard"
        else:
            return "very_hard"
    
    def _generate_adaptation_reason(self, current_irt: float, optimal_irt: float, performance_gap: float) -> str:
        """Génère une explication de l'adaptation de difficulté"""
        
        if abs(current_irt - optimal_irt) < 0.1:
            return "Difficulté actuelle optimale - maintien du niveau"
        
        if optimal_irt > current_irt:
            if performance_gap > 0:
                return f"Performance excellente (+{performance_gap:.1f}%) - augmentation de la difficulté"
            else:
                return "Compétence détectée - progression vers un niveau supérieur"
        else:
            if performance_gap < 0:
                return f"Difficultés détectées ({performance_gap:.1f}%) - diminution de la difficulté"
            else:
                return "Niveau trop élevé - retour à une difficulté appropriée"
    
    def calculate_cognitive_load(self, student_ability: float, question_difficulty: str, 
                               question_type: str, estimated_time: int) -> Dict[str, Any]:
        """Calcule la charge cognitive estimée d'une question"""
        
        difficulty_irt = self._convert_difficulty_to_irt(question_difficulty)
        
        # Facteurs de charge cognitive
        difficulty_factor = 1.0 + abs(difficulty_irt) * 0.5  # Plus difficile = plus de charge
        
        type_factors = {
            "multiple_choice": 1.0,
            "text": 1.2,
            "image": 1.1,
            "interactive": 1.3,
            "essay": 1.5
        }
        type_factor = type_factors.get(question_type, 1.0)
        
        # Facteur temporel (plus de temps = plus de charge cognitive)
        time_factor = 1.0 + (estimated_time - 30) / 60  # Normalisé sur 30 secondes
        
        # Calcul de la charge cognitive totale
        cognitive_load = difficulty_factor * type_factor * time_factor
        
        # Normalisation sur une échelle 0-5
        normalized_load = min(5.0, cognitive_load)
        
        # Classification de la charge
        if normalized_load < 2.0:
            load_category = "faible"
        elif normalized_load < 3.5:
            load_category = "modérée"
        else:
            load_category = "élevée"
        
        # Recommandations selon la charge
        recommendations = self._generate_cognitive_load_recommendations(
            normalized_load, student_ability, difficulty_irt
        )
        
        return {
            "cognitive_load": round(normalized_load, 2),
            "load_category": load_category,
            "difficulty_factor": round(difficulty_factor, 2),
            "type_factor": round(type_factor, 2),
            "time_factor": round(time_factor, 2),
            "recommendations": recommendations
        }
    
    def _generate_cognitive_load_recommendations(self, cognitive_load: float, 
                                               student_ability: float, difficulty_irt: float) -> List[str]:
        """Génère des recommandations basées sur la charge cognitive"""
        
        recommendations = []
        
        if cognitive_load > 4.0:
            recommendations.append("Charge cognitive très élevée - considérer une pause ou une question plus simple")
        elif cognitive_load > 3.0:
            recommendations.append("Charge cognitive élevée - surveiller la fatigue de l'étudiant")
        
        # Recommandations basées sur la correspondance compétence-difficulté
        ability_difficulty_gap = abs(student_ability - difficulty_irt)
        
        if ability_difficulty_gap > 1.5:
            recommendations.append("Écart important entre compétence et difficulté - ajustement recommandé")
        elif ability_difficulty_gap < 0.5:
            recommendations.append("Bonne correspondance compétence-difficulté - progression optimale")
        
        if not recommendations:
            recommendations.append("Charge cognitive appropriée - continuer l'évaluation")
        
        return recommendations

# Test du moteur IRT
if __name__ == "__main__":
    irt_engine = IRTEngine()
    print("🧮 Moteur IRT initialisé avec succès !")
    
    # Test d'estimation de compétence
    student_ability = irt_engine.estimate_student_ability(1)
    print(f"🎯 Compétence estimée: {student_ability.ability_estimate:.2f} ± {student_ability.standard_error:.2f}")
    
    # Test de prédiction de performance
    prediction = irt_engine.predict_performance(student_ability.ability_estimate, "medium")
    print(f"📊 Prédiction: {prediction['predicted_score']}% (confiance: {prediction['confidence_level']})")
    
    # Test d'adaptation de difficulté
    adaptation = irt_engine.adapt_difficulty_irt(
        student_ability.ability_estimate, "medium", 75.0, 10
    )
    print(f"🔄 Adaptation: {adaptation['current_difficulty']} → {adaptation['new_difficulty']}")
    
    # Test de calcul de charge cognitive
    cognitive_load = irt_engine.calculate_cognitive_load(
        student_ability.ability_estimate, "medium", "multiple_choice", 45
    )
    print(f"🧠 Charge cognitive: {cognitive_load['cognitive_load']}/5 ({cognitive_load['load_category']})")












