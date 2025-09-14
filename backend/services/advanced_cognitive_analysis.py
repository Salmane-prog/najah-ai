#!/usr/bin/env python3
"""
Service d'Analyse Cognitive Avancée pour Najah AI
Analyse des temps de réponse, patterns et préférences d'apprentissage
"""

import numpy as np
import json
from typing import Dict, List, Any, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum
import sqlite3
from collections import defaultdict, Counter

class ResponsePattern(Enum):
    """Types de patterns de réponses identifiés"""
    CONFIDENT = "confident"           # Réponse rapide et correcte
    HESITANT = "hesitant"            # Réponse lente avec hésitation
    CORRECTIVE = "corrective"        # Changement de réponse
    ANALYTICAL = "analytical"        # Temps de réflexion long
    IMPULSIVE = "impulsive"          # Réponse très rapide
    THOROUGH = "thorough"            # Vérification complète
    STRUGGLING = "struggling"        # Difficulté évidente

class LearningPreference(Enum):
    """Préférences d'apprentissage détectées"""
    VISUAL = "visual"                # Apprentissage visuel
    AUDITORY = "auditory"            # Apprentissage auditif
    KINESTHETIC = "kinesthetic"      # Apprentissage kinesthésique
    READING_WRITING = "reading_writing"  # Apprentissage par lecture/écriture
    MIXED = "mixed"                  # Style mixte

@dataclass
class ResponseAnalysis:
    """Analyse détaillée d'une réponse"""
    question_id: int
    response_time: float
    pattern: ResponsePattern
    confidence_score: float
    cognitive_load: float
    error_type: str = None
    correction_count: int = 0
    hesitation_markers: List[str] = None

@dataclass
class CognitiveProfile:
    """Profil cognitif complet de l'étudiant"""
    student_id: int
    learning_preference: LearningPreference
    attention_span: float
    memory_strength: float
    problem_solving_style: str
    cognitive_load_capacity: float
    response_patterns: Dict[str, float]
    error_patterns: Dict[str, int]
    confidence_trends: List[float]
    improvement_areas: List[str]

class AdvancedCognitiveAnalyzer:
    """Analyseur cognitif avancé avec algorithmes sophistiqués"""
    
    def __init__(self, db_path: str = "../data/app.db"):
        self.db_path = db_path
        self.response_thresholds = {
            "very_fast": 5.0,      # < 5 secondes
            "fast": 15.0,          # 5-15 secondes
            "normal": 45.0,        # 15-45 secondes
            "slow": 90.0,          # 45-90 secondes
            "very_slow": 90.0      # > 90 secondes
        }
        
        self.pattern_indicators = {
            "hesitation": ["effacer", "modifier", "changer", "hésiter"],
            "correction": ["corriger", "rectifier", "annuler"],
            "verification": ["vérifier", "relire", "revoir"],
            "struggle": ["longue_pause", "aide_demandée", "abandon"]
        }
    
    def analyze_response_time(self, response_time: float, question_difficulty: str) -> Dict[str, Any]:
        """Analyse le temps de réponse selon la difficulté de la question"""
        
        # Temps de référence selon la difficulté
        difficulty_thresholds = {
            "easy": {"optimal": 20, "acceptable": 45, "concerning": 90},
            "medium": {"optimal": 35, "acceptable": 75, "concerning": 120},
            "hard": {"optimal": 60, "acceptable": 120, "concerning": 180}
        }
        
        thresholds = difficulty_thresholds.get(question_difficulty, difficulty_thresholds["medium"])
        
        # Classification du temps de réponse
        if response_time <= thresholds["optimal"]:
            time_category = "optimal"
            efficiency_score = 1.0
        elif response_time <= thresholds["acceptable"]:
            time_category = "acceptable"
            efficiency_score = 0.7
        elif response_time <= thresholds["concerning"]:
            time_category = "concerning"
            efficiency_score = 0.4
        else:
            time_category = "problematic"
            efficiency_score = 0.2
        
        # Calcul de la charge cognitive estimée
        cognitive_load = self._calculate_cognitive_load(response_time, question_difficulty)
        
        return {
            "time_category": time_category,
            "efficiency_score": efficiency_score,
            "cognitive_load": cognitive_load,
            "optimal_time": thresholds["optimal"],
            "deviation_from_optimal": response_time - thresholds["optimal"]
        }
    
    def _calculate_cognitive_load(self, response_time: float, difficulty: str) -> float:
        """Calcule la charge cognitive estimée"""
        
        # Facteurs de difficulté
        difficulty_factors = {"easy": 1.0, "medium": 1.5, "hard": 2.0}
        
        # Temps optimal selon la difficulté
        optimal_times = {"easy": 20, "medium": 35, "hard": 60}
        
        difficulty_factor = difficulty_factors.get(difficulty, 1.0)
        optimal_time = optimal_times.get(difficulty, 35)
        
        # Calcul de la charge cognitive
        if response_time <= optimal_time:
            # Réponse rapide = charge cognitive faible
            cognitive_load = difficulty_factor * (response_time / optimal_time)
        else:
            # Réponse lente = charge cognitive élevée
            cognitive_load = difficulty_factor * (1 + (response_time - optimal_time) / optimal_time)
        
        return min(cognitive_load, 5.0)  # Limite à 5.0
    
    def detect_response_pattern(self, response_data: Dict[str, Any]) -> ResponsePattern:
        """Détecte le pattern de réponse de l'étudiant"""
        
        response_time = response_data.get("response_time", 0)
        correction_count = response_data.get("correction_count", 0)
        hesitation_markers = response_data.get("hesitation_markers", [])
        question_difficulty = response_data.get("question_difficulty", "medium")
        
        # Classification selon les indicateurs
        if correction_count > 2:
            return ResponsePattern.CORRECTIVE
        elif len(hesitation_markers) > 1:
            return ResponsePattern.HESITANT
        elif response_time < 10 and response_data.get("is_correct", False):
            return ResponsePattern.CONFIDENT
        elif response_time > 120:
            return ResponsePattern.STRUGGLING
        elif response_time > 60 and response_data.get("is_correct", True):
            return ResponsePattern.THOROUGH
        elif response_time < 15 and not response_data.get("is_correct", False):
            return ResponsePattern.IMPULSIVE
        else:
            return ResponsePattern.ANALYTICAL
    
    def analyze_error_patterns(self, student_id: int, subject: str = None) -> Dict[str, Any]:
        """Analyse les patterns d'erreurs récurrentes"""
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # Récupérer l'historique des erreurs
            query = """
                SELECT 
                    qr.quiz_id,
                    qr.score,
                    qr.percentage,
                    qr.created_at,
                    q.question_text,
                    q.difficulty,
                    q.subject
                FROM quiz_results qr
                JOIN quizzes q ON qr.quiz_id = q.id
                WHERE qr.user_id = ? AND qr.percentage < 70
            """
            
            if subject:
                query += " AND q.subject = ?"
                cursor.execute(query, (student_id, subject))
            else:
                cursor.execute(query, (student_id,))
            
            error_data = cursor.fetchall()
            
            if not error_data:
                return {"error_count": 0, "patterns": {}, "recommendations": []}
            
            # Analyser les patterns d'erreurs
            error_patterns = defaultdict(int)
            difficulty_errors = defaultdict(int)
            subject_errors = defaultdict(int)
            
            for row in error_data:
                quiz_id, score, percentage, created_at, question, difficulty, subject = row
                
                # Pattern par difficulté
                difficulty_errors[difficulty] += 1
                
                # Pattern par sujet
                subject_errors[subject] += 1
                
                # Pattern par score
                if percentage < 50:
                    error_patterns["very_low"] += 1
                elif percentage < 60:
                    error_patterns["low"] += 1
                else:
                    error_patterns["moderate"] += 1
            
            # Générer des recommandations
            recommendations = self._generate_error_recommendations(error_patterns, difficulty_errors, subject_errors)
            
            return {
                "error_count": len(error_data),
                "patterns": dict(error_patterns),
                "difficulty_breakdown": dict(difficulty_errors),
                "subject_breakdown": dict(subject_errors),
                "recommendations": recommendations,
                "last_errors": [row[3] for row in error_data[:5]]  # 5 dernières erreurs
            }
            
        finally:
            conn.close()
    
    def _generate_error_recommendations(self, error_patterns: Dict, difficulty_errors: Dict, subject_errors: Dict) -> List[str]:
        """Génère des recommandations basées sur l'analyse des erreurs"""
        
        recommendations = []
        
        # Recommandations par type d'erreur
        if error_patterns.get("very_low", 0) > 3:
            recommendations.append("Revoir les concepts de base - nombreuses erreurs fondamentales détectées")
        
        if error_patterns.get("low", 0) > 5:
            recommendations.append("Renforcer la compréhension intermédiaire - exercices de consolidation recommandés")
        
        # Recommandations par difficulté
        if difficulty_errors.get("hard", 0) > difficulty_errors.get("easy", 0):
            recommendations.append("Se concentrer sur les exercices de niveau intermédiaire avant d'aborder les sujets difficiles")
        
        # Recommandations par sujet
        worst_subject = max(subject_errors.items(), key=lambda x: x[1])[0] if subject_errors else None
        if worst_subject:
            recommendations.append(f"Priorité : renforcer les compétences en {worst_subject}")
        
        # Recommandations générales
        if len(recommendations) < 3:
            recommendations.append("Pratiquer régulièrement avec des exercices variés")
            recommendations.append("Utiliser les ressources de remédiation disponibles")
        
        return recommendations
    
    def detect_learning_preferences(self, student_id: int) -> LearningPreference:
        """Détecte les préférences d'apprentissage de l'étudiant"""
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # Analyser les patterns d'activité
            query = """
                SELECT 
                    qr.response_time,
                    qr.percentage,
                    q.question_type,
                    q.difficulty,
                    qr.created_at
                FROM quiz_results qr
                JOIN quizzes q ON qr.quiz_id = q.id
                WHERE qr.user_id = ?
                ORDER BY qr.created_at DESC
                LIMIT 50
            """
            
            cursor.execute(query, (student_id,))
            activity_data = cursor.fetchall()
            
            if not activity_data:
                return LearningPreference.MIXED
            
            # Analyser les préférences
            preferences = {
                "visual": 0,
                "auditory": 0,
                "kinesthetic": 0,
                "reading_writing": 0
            }
            
            for row in activity_data:
                response_time, percentage, question_type, difficulty, created_at = row
                
                # Analyse basée sur le type de question et la performance
                if question_type == "multiple_choice" and percentage > 80:
                    preferences["visual"] += 1
                elif question_type == "text" and percentage > 80:
                    preferences["reading_writing"] += 1
                elif response_time < 30 and percentage > 70:
                    preferences["kinesthetic"] += 1
                elif response_time > 60 and percentage > 75:
                    preferences["auditory"] += 1
            
            # Déterminer la préférence dominante
            dominant_preference = max(preferences.items(), key=lambda x: x[1])
            
            if dominant_preference[1] > len(activity_data) * 0.4:  # Plus de 40% des réponses
                return LearningPreference(dominant_preference[0])
            else:
                return LearningPreference.MIXED
                
        finally:
            conn.close()
    
    def generate_cognitive_profile(self, student_id: int) -> CognitiveProfile:
        """Génère un profil cognitif complet de l'étudiant"""
        
        # Analyser les préférences d'apprentissage
        learning_preference = self.detect_learning_preferences(student_id)
        
        # Analyser les patterns d'erreurs
        error_analysis = self.analyze_error_patterns(student_id)
        
        # Calculer les métriques cognitives
        attention_span = self._calculate_attention_span(student_id)
        memory_strength = self._calculate_memory_strength(student_id)
        problem_solving_style = self._detect_problem_solving_style(student_id)
        cognitive_load_capacity = self._calculate_cognitive_load_capacity(student_id)
        
        # Analyser les tendances de confiance
        confidence_trends = self._analyze_confidence_trends(student_id)
        
        # Identifier les axes d'amélioration
        improvement_areas = self._identify_improvement_areas(error_analysis, confidence_trends)
        
        return CognitiveProfile(
            student_id=student_id,
            learning_preference=learning_preference,
            attention_span=attention_span,
            memory_strength=memory_strength,
            problem_solving_style=problem_solving_style,
            cognitive_load_capacity=cognitive_load_capacity,
            response_patterns={},  # À remplir avec l'analyse en temps réel
            error_patterns=error_analysis.get("patterns", {}),
            confidence_trends=confidence_trends,
            improvement_areas=improvement_areas
        )
    
    def _calculate_attention_span(self, student_id: int) -> float:
        """Calcule la durée d'attention moyenne de l'étudiant"""
        # Implémentation simplifiée - à améliorer avec plus de données
        return 45.0  # 45 minutes en moyenne
    
    def _calculate_memory_strength(self, student_id: int) -> float:
        """Calcule la force de mémoire de l'étudiant"""
        # Implémentation simplifiée - à améliorer avec plus de données
        return 0.75  # 75% de force de mémoire
    
    def _detect_problem_solving_style(self, student_id: int) -> str:
        """Détecte le style de résolution de problèmes"""
        # Implémentation simplifiée - à améliorer avec plus de données
        return "analytical"  # Style analytique par défaut
    
    def _calculate_cognitive_load_capacity(self, student_id: int) -> float:
        """Calcule la capacité de charge cognitive de l'étudiant"""
        # Implémentation simplifiée - à améliorer avec plus de données
        return 3.5  # Capacité de 3.5/5.0
    
    def _analyze_confidence_trends(self, student_id: int) -> List[float]:
        """Analyse les tendances de confiance de l'étudiant"""
        # Implémentation simplifiée - à améliorer avec plus de données
        return [0.7, 0.75, 0.8, 0.85, 0.9]  # Progression de confiance
    
    def _identify_improvement_areas(self, error_analysis: Dict, confidence_trends: List[float]) -> List[str]:
        """Identifie les axes d'amélioration"""
        areas = []
        
        if error_analysis.get("error_count", 0) > 10:
            areas.append("Réduire le nombre d'erreurs - plus de pratique nécessaire")
        
        if len(confidence_trends) > 2 and confidence_trends[-1] < confidence_trends[-2]:
            areas.append("Travailler sur la confiance en soi - révisions et encouragements")
        
        if not areas:
            areas.append("Maintenir le bon niveau - continuer la progression")
        
        return areas

# Test du service
if __name__ == "__main__":
    analyzer = AdvancedCognitiveAnalyzer()
    print("🧠 Service d'Analyse Cognitive Avancée initialisé avec succès !")
    
    # Test d'analyse de temps de réponse
    time_analysis = analyzer.analyze_response_time(25.0, "medium")
    print(f"⏱️ Analyse temps de réponse: {time_analysis}")
    
    # Test de détection de pattern
    response_data = {
        "response_time": 30.0,
        "correction_count": 1,
        "hesitation_markers": ["effacer"],
        "question_difficulty": "medium",
        "is_correct": True
    }
    pattern = analyzer.detect_response_pattern(response_data)
    print(f"🎯 Pattern détecté: {pattern.value}")












