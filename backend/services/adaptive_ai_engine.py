#!/usr/bin/env python3
"""
Moteur d'Intelligence Artificielle pour l'Évaluation Adaptative
Implémente des algorithmes avancés d'adaptation en temps réel
"""

import numpy as np
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass
from enum import Enum
import sqlite3
import os

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AdaptationAlgorithm(Enum):
    """Algorithmes d'adaptation disponibles"""
    IRT = "irt"  # Item Response Theory
    ML_GRADIENT = "ml_gradient"  # Machine Learning avec gradient
    EXPERT_RULES = "expert_rules"  # Système expert
    HYBRID = "hybrid"  # Combinaison des approches

@dataclass
class StudentProfile:
    """Profil d'apprentissage d'un étudiant"""
    student_id: int
    current_ability: float
    confidence_interval: Tuple[float, float]
    learning_speed: float
    preferred_difficulty: float
    strength_subjects: List[str]
    weakness_subjects: List[str]
    learning_patterns: Dict[str, Any]
    last_updated: datetime

@dataclass
class QuestionProfile:
    """Profil d'une question pour l'adaptation"""
    question_id: int
    difficulty_level: float
    discrimination: float  # Capacité à discriminer les niveaux
    guessing: float  # Probabilité de réponse aléatoire
    subject: str
    topic: str
    tags: List[str]
    success_rate: float
    avg_response_time: float

@dataclass
class AdaptationDecision:
    """Décision d'adaptation prise par l'IA"""
    next_question_id: int
    difficulty_adjustment: float
    confidence_level: float
    reasoning: str
    algorithm_used: AdaptationAlgorithm
    metadata: Dict[str, Any]

class AdaptiveAIEngine:
    """
    Moteur d'IA principal pour l'évaluation adaptative
    """
    
    def __init__(self, db_path: str = "./data/app.db"):
        self.db_path = db_path
        self.irt_parameters = {
            'learning_rate': 0.1,
            'confidence_threshold': 0.95,
            'max_questions': 20,
            'min_confidence_interval': 0.5
        }
        self.ml_parameters = {
            'batch_size': 10,
            'epochs': 100,
            'learning_rate': 0.001
        }
        
        logger.info("🚀 Moteur d'IA adaptative initialisé")
    
    def get_db_connection(self) -> sqlite3.Connection:
        """Obtenir une connexion à la base de données"""
        return sqlite3.connect(self.db_path)
    
    def analyze_student_performance(self, student_id: int, test_id: int) -> StudentProfile:
        """
        Analyser les performances d'un étudiant pour créer son profil
        """
        try:
            conn = self.get_db_connection()
            cursor = conn.cursor()
            
            # Récupérer l'historique des performances
            cursor.execute("""
                SELECT 
                    sa.question_id,
                    sa.is_correct,
                    sa.response_time,
                    sa.confidence_level,
                    aq.difficulty_level,
                    aq.subject,
                    aq.topic
                FROM student_answers sa
                JOIN adaptive_questions aq ON sa.question_id = aq.id
                JOIN student_adaptive_tests sat ON sa.student_test_id = sat.id
                WHERE sat.student_id = ? AND sat.test_id = ?
                ORDER BY sa.created_at
            """, (student_id, test_id))
            
            answers = cursor.fetchall()
            
            if not answers:
                # Profil par défaut pour un nouvel étudiant
                return StudentProfile(
                    student_id=student_id,
                    current_ability=5.0,  # Niveau moyen
                    confidence_interval=(4.0, 6.0),
                    learning_speed=1.0,
                    preferred_difficulty=5.0,
                    strength_subjects=[],
                    weakness_subjects=[],
                    learning_patterns={},
                    last_updated=datetime.now()
                )
            
            # Analyser les réponses
            correct_answers = [a for a in answers if a[1]]
            total_answers = len(answers)
            accuracy = len(correct_answers) / total_answers if total_answers > 0 else 0.5
            
            # Calculer la capacité actuelle basée sur IRT
            current_ability = self._calculate_irt_ability(answers)
            
            # Analyser les patterns d'apprentissage
            learning_patterns = self._analyze_learning_patterns(answers)
            
            # Identifier les forces et faiblesses par matière
            subject_performance = self._analyze_subject_performance(answers)
            strength_subjects = [s for s, p in subject_performance.items() if p > 0.7]
            weakness_subjects = [s for s, p in subject_performance.items() if p < 0.4]
            
            # Calculer la vitesse d'apprentissage
            learning_speed = self._calculate_learning_speed(answers)
            
            # Calculer l'intervalle de confiance
            confidence_interval = self._calculate_confidence_interval(answers, current_ability)
            
            profile = StudentProfile(
                student_id=student_id,
                current_ability=current_ability,
                confidence_interval=confidence_interval,
                learning_speed=learning_speed,
                preferred_difficulty=current_ability,
                strength_subjects=strength_subjects,
                weakness_subjects=weakness_subjects,
                learning_patterns=learning_patterns,
                last_updated=datetime.now()
            )
            
            conn.close()
            logger.info(f"📊 Profil étudiant {student_id} analysé: capacité={current_ability:.2f}")
            return profile
            
        except Exception as e:
            logger.error(f"❌ Erreur lors de l'analyse du profil étudiant: {e}")
            conn.close()
            raise
    
    def select_next_question(
        self, 
        student_profile: StudentProfile, 
        test_id: int, 
        answered_questions: List[int],
        algorithm: AdaptationAlgorithm = AdaptationAlgorithm.HYBRID
    ) -> AdaptationDecision:
        """
        Sélectionner la prochaine question optimale basée sur l'algorithme choisi
        """
        try:
            if algorithm == AdaptationAlgorithm.IRT:
                return self._irt_question_selection(student_profile, test_id, answered_questions)
            elif algorithm == AdaptationAlgorithm.ML_GRADIENT:
                return self._ml_gradient_selection(student_profile, test_id, answered_questions)
            elif algorithm == AdaptationAlgorithm.EXPERT_RULES:
                return self._expert_rules_selection(student_profile, test_id, answered_questions)
            elif algorithm == AdaptationAlgorithm.HYBRID:
                return self._hybrid_selection(student_profile, test_id, answered_questions)
            else:
                raise ValueError(f"Algorithme non supporté: {algorithm}")
                
        except Exception as e:
            logger.error(f"❌ Erreur lors de la sélection de question: {e}")
            raise
    
    def _irt_question_selection(
        self, 
        student_profile: StudentProfile, 
        test_id: int, 
        answered_questions: List[int]
    ) -> AdaptationDecision:
        """
        Sélection de question basée sur la théorie de réponse aux items (IRT)
        """
        try:
            conn = self.get_db_connection()
            cursor = conn.cursor()
            
            # Récupérer les questions disponibles
            cursor.execute("""
                SELECT 
                    id, difficulty_level, subject, topic, success_rate, avg_response_time
                FROM adaptive_questions 
                WHERE test_id = ? AND id NOT IN ({})
                ORDER BY ABS(difficulty_level - ?)
            """.format(','.join('?' * len(answered_questions))), 
            [test_id] + answered_questions + [student_profile.current_ability])
            
            available_questions = cursor.fetchall()
            
            if not available_questions:
                raise ValueError("Aucune question disponible")
            
            # Sélectionner la question optimale selon IRT
            best_question = None
            best_information = -1
            
            for question in available_questions:
                question_id, difficulty, subject, topic, success_rate, avg_time = question
                
                # Calculer l'information de Fisher pour cette question
                information = self._calculate_fisher_information(
                    difficulty, 
                    student_profile.current_ability
                )
                
                # Bonus pour les matières de faiblesse
                if subject in student_profile.weakness_subjects:
                    information *= 1.2
                
                # Bonus pour les questions de difficulté appropriée
                difficulty_match = 1.0 - abs(difficulty - student_profile.current_ability) / 10.0
                information *= (1.0 + difficulty_match * 0.3)
                
                if information > best_information:
                    best_information = information
                    best_question = question
            
            if not best_question:
                raise ValueError("Impossible de sélectionner une question")
            
            question_id, difficulty, subject, topic, success_rate, avg_time = best_question
            
            # Calculer l'ajustement de difficulté
            difficulty_adjustment = self._calculate_difficulty_adjustment(
                student_profile, difficulty, subject
            )
            
            decision = AdaptationDecision(
                next_question_id=question_id,
                difficulty_adjustment=difficulty_adjustment,
                confidence_level=min(0.95, best_information / 10.0),
                reasoning=f"Question sélectionnée par IRT: difficulté={difficulty}, sujet={subject}, information={best_information:.3f}",
                algorithm_used=AdaptationAlgorithm.IRT,
                metadata={
                    'fisher_information': best_information,
                    'difficulty_match': 1.0 - abs(difficulty - student_profile.current_ability) / 10.0,
                    'subject_priority': subject in student_profile.weakness_subjects
                }
            )
            
            conn.close()
            logger.info(f"🎯 Question IRT sélectionnée: {question_id} (difficulté: {difficulty})")
            return decision
            
        except Exception as e:
            logger.error(f"❌ Erreur lors de la sélection IRT: {e}")
            conn.close()
            raise
    
    def _ml_gradient_selection(
        self, 
        student_profile: StudentProfile, 
        test_id: int, 
        answered_questions: List[int]
    ) -> AdaptationDecision:
        """
        Sélection de question basée sur l'apprentissage automatique avec gradient
        """
        try:
            # Pour l'instant, utiliser une approche simplifiée
            # Dans une implémentation complète, on utiliserait un modèle ML entraîné
            
            # Simuler un modèle ML qui prédit la difficulté optimale
            predicted_difficulty = self._predict_optimal_difficulty_ml(student_profile)
            
            conn = self.get_db_connection()
            cursor = conn.cursor()
            
            # Trouver la question la plus proche de la difficulté prédite
            cursor.execute("""
                SELECT 
                    id, difficulty_level, subject, topic, success_rate, avg_response_time
                FROM adaptive_questions 
                WHERE test_id = ? AND id NOT IN ({})
                ORDER BY ABS(difficulty_level - ?)
                LIMIT 1
            """.format(','.join('?' * len(answered_questions))), 
            [test_id] + answered_questions + [predicted_difficulty])
            
            question = cursor.fetchone()
            
            if not question:
                raise ValueError("Aucune question disponible")
            
            question_id, difficulty, subject, topic, success_rate, avg_time = question
            
            # Calculer l'ajustement basé sur la prédiction ML
            difficulty_adjustment = predicted_difficulty - difficulty
            
            decision = AdaptationDecision(
                next_question_id=question_id,
                difficulty_adjustment=difficulty_adjustment,
                confidence_level=0.85,  # Confiance ML
                reasoning=f"Question sélectionnée par ML: difficulté prédite={predicted_difficulty:.2f}, actuelle={difficulty}",
                algorithm_used=AdaptationAlgorithm.ML_GRADIENT,
                metadata={
                    'predicted_difficulty': predicted_difficulty,
                    'ml_confidence': 0.85,
                    'model_version': '1.0'
                }
            )
            
            conn.close()
            logger.info(f"🤖 Question ML sélectionnée: {question_id} (prédiction: {predicted_difficulty:.2f})")
            return decision
            
        except Exception as e:
            logger.error(f"❌ Erreur lors de la sélection ML: {e}")
            conn.close()
            raise
    
    def _expert_rules_selection(
        self, 
        student_profile: StudentProfile, 
        test_id: int, 
        answered_questions: List[int]
    ) -> AdaptationDecision:
        """
        Sélection de question basée sur des règles expertes éducatives
        """
        try:
            conn = self.get_db_connection()
            cursor = conn.cursor()
            
            # Règles expertes pour la sélection de questions
            rules = self._get_expert_rules(student_profile)
            
            # Appliquer les règles pour filtrer les questions
            filtered_questions = self._apply_expert_rules(
                cursor, test_id, answered_questions, rules
            )
            
            if not filtered_questions:
                raise ValueError("Aucune question ne respecte les règles expertes")
            
            # Sélectionner la meilleure question selon les règles
            best_question = self._select_best_by_rules(filtered_questions, student_profile)
            
            question_id, difficulty, subject, topic, success_rate, avg_time = best_question
            
            # Calculer l'ajustement selon les règles expertes
            difficulty_adjustment = self._calculate_expert_adjustment(
                student_profile, difficulty, subject, rules
            )
            
            decision = AdaptationDecision(
                next_question_id=question_id,
                difficulty_adjustment=difficulty_adjustment,
                confidence_level=0.90,  # Confiance règles expertes
                reasoning=f"Question sélectionnée par règles expertes: {rules['primary_rule']}",
                algorithm_used=AdaptationAlgorithm.EXPERT_RULES,
                metadata={
                    'applied_rules': rules,
                    'rule_confidence': 0.90,
                    'expert_system_version': '2.0'
                }
            )
            
            conn.close()
            logger.info(f"🧠 Question expert sélectionnée: {question_id} (règle: {rules['primary_rule']})")
            return decision
            
        except Exception as e:
            logger.error(f"❌ Erreur lors de la sélection expert: {e}")
            conn.close()
            raise
    
    def _hybrid_selection(
        self, 
        student_profile: StudentProfile, 
        test_id: int, 
        answered_questions: List[int]
    ) -> AdaptationDecision:
        """
        Sélection hybride combinant plusieurs algorithmes
        """
        try:
            # Obtenir les décisions de chaque algorithme
            irt_decision = self._irt_question_selection(student_profile, test_id, answered_questions)
            ml_decision = self._ml_gradient_selection(student_profile, test_id, answered_questions)
            expert_decision = self._expert_rules_selection(student_profile, test_id, answered_questions)
            
            # Combiner les décisions avec des poids
            decisions = [
                (irt_decision, 0.4),      # IRT: 40%
                (ml_decision, 0.35),     # ML: 35%
                (expert_decision, 0.25)  # Expert: 25%
            ]
            
            # Sélectionner la question finale
            final_question_id = self._combine_decisions(decisions)
            
            # Calculer l'ajustement final
            final_adjustment = self._calculate_hybrid_adjustment(decisions, final_question_id)
            
            # Calculer la confiance combinée
            combined_confidence = sum(d.confidence_level * w for d, w in decisions)
            
            decision = AdaptationDecision(
                next_question_id=final_question_id,
                difficulty_adjustment=final_adjustment,
                confidence_level=combined_confidence,
                reasoning="Sélection hybride combinant IRT, ML et règles expertes",
                algorithm_used=AdaptationAlgorithm.HYBRID,
                metadata={
                    'irt_decision': irt_decision.next_question_id,
                    'ml_decision': ml_decision.next_question_id,
                    'expert_decision': expert_decision.next_question_id,
                    'weights': {'irt': 0.4, 'ml': 0.35, 'expert': 0.25}
                }
            )
            
            logger.info(f"🔄 Question hybride sélectionnée: {final_question_id}")
            return decision
            
        except Exception as e:
            logger.error(f"❌ Erreur lors de la sélection hybride: {e}")
            raise
    
    def update_student_profile(
        self, 
        student_profile: StudentProfile, 
        question_id: int, 
        is_correct: bool, 
        response_time: float,
        confidence_level: int
    ) -> StudentProfile:
        """
        Mettre à jour le profil de l'étudiant après une réponse
        """
        try:
            # Récupérer les informations de la question
            conn = self.get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT difficulty_level, subject, topic
                FROM adaptive_questions 
                WHERE id = ?
            """, (question_id,))
            
            question_info = cursor.fetchone()
            if not question_info:
                raise ValueError(f"Question {question_id} non trouvée")
            
            difficulty, subject, topic = question_info
            conn.close()
            
            # Mettre à jour la capacité selon IRT
            new_ability = self._update_irt_ability(
                student_profile.current_ability,
                difficulty,
                is_correct,
                response_time
            )
            
            # Mettre à jour les patterns d'apprentissage
            updated_patterns = student_profile.learning_patterns.copy()
            if subject not in updated_patterns:
                updated_patterns[subject] = {'correct': 0, 'total': 0, 'avg_time': 0}
            
            updated_patterns[subject]['total'] += 1
            if is_correct:
                updated_patterns[subject]['correct'] += 1
            
            # Mettre à jour le temps moyen
            current_avg = updated_patterns[subject]['avg_time']
            total_questions = updated_patterns[subject]['total']
            updated_patterns[subject]['avg_time'] = (
                (current_avg * (total_questions - 1) + response_time) / total_questions
            )
            
            # Recalculer les forces et faiblesses
            strength_subjects = []
            weakness_subjects = []
            for subj, data in updated_patterns.items():
                if data['total'] >= 3:  # Au moins 3 questions pour évaluer
                    accuracy = data['correct'] / data['total']
                    if accuracy > 0.7:
                        strength_subjects.append(subj)
                    elif accuracy < 0.4:
                        weakness_subjects.append(subj)
            
            # Mettre à jour la vitesse d'apprentissage
            learning_speed = self._update_learning_speed(
                student_profile.learning_speed,
                is_correct,
                response_time,
                difficulty
            )
            
            # Recalculer l'intervalle de confiance
            confidence_interval = self._update_confidence_interval(
                student_profile, new_ability, is_correct
            )
            
            updated_profile = StudentProfile(
                student_id=student_profile.student_id,
                current_ability=new_ability,
                confidence_interval=confidence_interval,
                learning_speed=learning_speed,
                preferred_difficulty=new_ability,
                strength_subjects=strength_subjects,
                weakness_subjects=weakness_subjects,
                learning_patterns=updated_patterns,
                last_updated=datetime.now()
            )
            
            logger.info(f"📈 Profil étudiant {student_profile.student_id} mis à jour: capacité {student_profile.current_ability:.2f} → {new_ability:.2f}")
            return updated_profile
            
        except Exception as e:
            logger.error(f"❌ Erreur lors de la mise à jour du profil: {e}")
            raise
    
    def generate_learning_recommendations(
        self, 
        student_profile: StudentProfile
    ) -> Dict[str, Any]:
        """
        Générer des recommandations d'apprentissage personnalisées
        """
        try:
            recommendations = {
                'immediate_actions': [],
                'short_term_goals': [],
                'long_term_strategy': [],
                'resource_suggestions': [],
                'difficulty_adjustments': {}
            }
            
            # Recommandations immédiates basées sur les faiblesses
            for subject in student_profile.weakness_subjects:
                recommendations['immediate_actions'].append({
                    'action': f'Réviser les concepts de base en {subject}',
                    'priority': 'high',
                    'estimated_time': '30 minutes'
                })
            
            # Objectifs à court terme
            if student_profile.current_ability < 6.0:
                recommendations['short_term_goals'].append({
                    'goal': 'Améliorer la capacité générale à 6.0+',
                    'target_date': (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d'),
                    'milestones': ['Compléter 5 questions de niveau 5-6', 'Réviser les erreurs fréquentes']
                })
            
            # Stratégie à long terme
            recommendations['long_term_strategy'].append({
                'strategy': 'Approche progressive par matière',
                'description': 'Se concentrer sur une matière à la fois, en commençant par les plus faibles',
                'timeline': '2-3 semaines par matière'
            })
            
            # Suggestions de ressources
            for subject in student_profile.weakness_subjects:
                recommendations['resource_suggestions'].append({
                    'subject': subject,
                    'resources': [
                        f'Exercices de niveau {max(1, int(student_profile.current_ability - 1))} en {subject}',
                        f'Vidéos explicatives sur les concepts de base de {subject}',
                        f'Quiz d\'auto-évaluation en {subject}'
                    ]
                })
            
            # Ajustements de difficulté recommandés
            for subject in student_profile.learning_patterns:
                current_difficulty = student_profile.learning_patterns[subject].get('avg_difficulty', 5.0)
                if subject in student_profile.strength_subjects:
                    recommendations['difficulty_adjustments'][subject] = min(10.0, current_difficulty + 0.5)
                elif subject in student_profile.weakness_subjects:
                    recommendations['difficulty_adjustments'][subject] = max(1.0, current_difficulty - 0.5)
                else:
                    recommendations['difficulty_adjustments'][subject] = current_difficulty
            
            logger.info(f"💡 Recommandations générées pour l'étudiant {student_profile.student_id}")
            return recommendations
            
        except Exception as e:
            logger.error(f"❌ Erreur lors de la génération des recommandations: {e}")
            raise
    
    # ============================================================================
    # MÉTHODES UTILITAIRES PRIVÉES
    # ============================================================================
    
    def _calculate_irt_ability(self, answers: List[Tuple]) -> float:
        """Calculer la capacité selon IRT"""
        if not answers:
            return 5.0
        
        # Implémentation simplifiée d'IRT
        total_difficulty = sum(a[4] for a in answers)  # difficulty_level
        total_correct = sum(1 for a in answers if a[1])  # is_correct
        
        if total_correct == 0:
            return max(1.0, total_difficulty / len(answers) - 1.0)
        elif total_correct == len(answers):
            return min(10.0, total_difficulty / len(answers) + 1.0)
        else:
            # Estimation IRT basée sur la proportion de réussite
            success_rate = total_correct / len(answers)
            avg_difficulty = total_difficulty / len(answers)
            
            # Ajuster selon le taux de réussite
            if success_rate > 0.8:
                return min(10.0, avg_difficulty + 1.0)
            elif success_rate < 0.2:
                return max(1.0, avg_difficulty - 1.0)
            else:
                return avg_difficulty
    
    def _calculate_fisher_information(self, difficulty: float, ability: float) -> float:
        """Calculer l'information de Fisher pour une question"""
        # Formule simplifiée de l'information de Fisher
        p = 1.0 / (1.0 + np.exp(-(ability - difficulty)))
        return p * (1.0 - p)
    
    def _calculate_difficulty_adjustment(
        self, 
        student_profile: StudentProfile, 
        question_difficulty: float, 
        subject: str
    ) -> float:
        """Calculer l'ajustement de difficulté recommandé"""
        base_adjustment = 0.0
        
        # Ajuster selon la capacité de l'étudiant
        if question_difficulty > student_profile.current_ability + 1.0:
            base_adjustment = -0.5  # Réduire la difficulté
        elif question_difficulty < student_profile.current_ability - 1.0:
            base_adjustment = 0.5   # Augmenter la difficulté
        
        # Ajuster selon les forces/faiblesses
        if subject in student_profile.strength_subjects:
            base_adjustment += 0.3
        elif subject in student_profile.weakness_subjects:
            base_adjustment -= 0.3
        
        return np.clip(base_adjustment, -1.0, 1.0)
    
    def _predict_optimal_difficulty_ml(self, student_profile: StudentProfile) -> float:
        """Prédire la difficulté optimale avec ML (simulation)"""
        # Simulation d'un modèle ML
        base_difficulty = student_profile.current_ability
        
        # Facteurs d'ajustement simulés
        learning_speed_factor = student_profile.learning_speed
        confidence_factor = (student_profile.confidence_interval[1] - student_profile.confidence_interval[0]) / 2.0
        
        # Prédiction simulée
        predicted = base_difficulty + (learning_speed_factor - 1.0) * 0.5 + confidence_factor * 0.3
        
        return np.clip(predicted, 1.0, 10.0)
    
    def _get_expert_rules(self, student_profile: StudentProfile) -> Dict[str, Any]:
        """Obtenir les règles expertes applicables"""
        rules = {
            'primary_rule': 'difficulty_matching',
            'secondary_rules': [],
            'constraints': {}
        }
        
        # Règle principale: correspondance de difficulté
        if student_profile.current_ability < 4.0:
            rules['primary_rule'] = 'build_confidence'
            rules['constraints']['max_difficulty'] = student_profile.current_ability + 0.5
        elif student_profile.current_ability > 7.0:
            rules['primary_rule'] = 'challenge_student'
            rules['constraints']['min_difficulty'] = student_profile.current_ability - 0.5
        else:
            rules['primary_rule'] = 'optimal_challenge'
            rules['constraints']['target_difficulty'] = student_profile.current_ability
        
        # Règles secondaires
        if student_profile.weakness_subjects:
            rules['secondary_rules'].append('focus_weaknesses')
        if student_profile.strength_subjects:
            rules['secondary_rules'].append('maintain_strengths')
        
        return rules
    
    def _apply_expert_rules(
        self, 
        cursor, 
        test_id: int, 
        answered_questions: List[int], 
        rules: Dict[str, Any]
    ) -> List[Tuple]:
        """Appliquer les règles expertes pour filtrer les questions"""
        # Implémentation simplifiée
        cursor.execute("""
            SELECT 
                id, difficulty_level, subject, topic, success_rate, avg_response_time
            FROM adaptive_questions 
            WHERE test_id = ? AND id NOT IN ({})
        """.format(','.join('?' * len(answered_questions))), 
        [test_id] + answered_questions)
        
        questions = cursor.fetchall()
        
        # Filtrer selon les règles
        if 'max_difficulty' in rules['constraints']:
            questions = [q for q in questions if q[1] <= rules['constraints']['max_difficulty']]
        elif 'min_difficulty' in rules['constraints']:
            questions = [q for q in questions if q[1] >= rules['constraints']['min_difficulty']]
        elif 'target_difficulty' in rules['constraints']:
            target = rules['constraints']['target_difficulty']
            questions = sorted(questions, key=lambda x: abs(x[1] - target))
        
        return questions
    
    def _select_best_by_rules(self, questions: List[Tuple], student_profile: StudentProfile) -> Tuple:
        """Sélectionner la meilleure question selon les règles"""
        if not questions:
            raise ValueError("Aucune question disponible")
        
        # Priorité aux matières de faiblesse
        for question in questions:
            if question[2] in student_profile.weakness_subjects:  # subject
                return question
        
        # Sinon, retourner la première question
        return questions[0]
    
    def _calculate_expert_adjustment(
        self, 
        student_profile: StudentProfile, 
        difficulty: float, 
        subject: str, 
        rules: Dict[str, Any]
    ) -> float:
        """Calculer l'ajustement selon les règles expertes"""
        adjustment = 0.0
        
        if rules['primary_rule'] == 'build_confidence':
            if difficulty > student_profile.current_ability:
                adjustment = -0.5
        elif rules['primary_rule'] == 'challenge_student':
            if difficulty < student_profile.current_ability:
                adjustment = 0.5
        
        return adjustment
    
    def _combine_decisions(self, decisions: List[Tuple[AdaptationDecision, float]]) -> int:
        """Combiner les décisions de plusieurs algorithmes"""
        # Vote pondéré simple
        question_votes = {}
        
        for decision, weight in decisions:
            question_id = decision.next_question_id
            if question_id not in question_votes:
                question_votes[question_id] = 0
            question_votes[question_id] += weight
        
        # Retourner la question avec le plus de votes
        return max(question_votes.items(), key=lambda x: x[1])[0]
    
    def _calculate_hybrid_adjustment(
        self, 
        decisions: List[Tuple[AdaptationDecision, float]], 
        final_question_id: int
    ) -> float:
        """Calculer l'ajustement final hybride"""
        total_adjustment = 0.0
        total_weight = 0.0
        
        for decision, weight in decisions:
            if decision.next_question_id == final_question_id:
                total_adjustment += decision.difficulty_adjustment * weight
                total_weight += weight
        
        return total_adjustment / total_weight if total_weight > 0 else 0.0
    
    def _update_irt_ability(
        self, 
        current_ability: float, 
        question_difficulty: float, 
        is_correct: bool, 
        response_time: float
    ) -> float:
        """Mettre à jour la capacité selon IRT"""
        # Facteur d'apprentissage basé sur la réponse
        if is_correct:
            if question_difficulty > current_ability:
                learning_factor = 0.3  # Apprentissage significatif
            else:
                learning_factor = 0.1  # Consolidation
        else:
            if question_difficulty < current_ability:
                learning_factor = -0.3  # Révision nécessaire
            else:
                learning_factor = -0.1  # Ajustement mineur
        
        # Facteur de temps de réponse
        time_factor = 0.0
        if response_time < 10.0:  # Réponse rapide
            time_factor = 0.1
        elif response_time > 60.0:  # Réponse lente
            time_factor = -0.1
        
        # Mise à jour de la capacité
        new_ability = current_ability + learning_factor + time_factor
        
        return np.clip(new_ability, 1.0, 10.0)
    
    def _update_learning_speed(
        self, 
        current_speed: float, 
        is_correct: bool, 
        response_time: float, 
        difficulty: float
    ) -> float:
        """Mettre à jour la vitesse d'apprentissage"""
        # Facteurs d'ajustement
        correctness_factor = 0.1 if is_correct else -0.05
        time_factor = 0.05 if response_time < 30.0 else -0.02
        difficulty_factor = 0.02 if difficulty > 5.0 else -0.01
        
        new_speed = current_speed + correctness_factor + time_factor + difficulty_factor
        
        return np.clip(new_speed, 0.5, 2.0)
    
    def _update_confidence_interval(
        self, 
        student_profile: StudentProfile, 
        new_ability: float, 
        is_correct: bool
    ) -> Tuple[float, float]:
        """Mettre à jour l'intervalle de confiance"""
        current_interval = student_profile.confidence_interval[1] - student_profile.confidence_interval[0]
        
        # Réduire l'intervalle avec plus de données
        if is_correct:
            reduction = 0.1
        else:
            reduction = 0.05
        
        new_interval = max(0.5, current_interval - reduction)
        
        # Centrer l'intervalle sur la nouvelle capacité
        half_interval = new_interval / 2.0
        lower = max(1.0, new_ability - half_interval)
        upper = min(10.0, new_ability + half_interval)
        
        return (lower, upper)
    
    def _analyze_learning_patterns(self, answers: List[Tuple]) -> Dict[str, Any]:
        """Analyser les patterns d'apprentissage"""
        patterns = {}
        
        for answer in answers:
            subject = answer[5]  # subject
            if subject not in patterns:
                patterns[subject] = {
                    'correct': 0,
                    'total': 0,
                    'avg_time': 0.0,
                    'difficulty_progression': []
                }
            
            patterns[subject]['total'] += 1
            if answer[1]:  # is_correct
                patterns[subject]['correct'] += 1
            
            # Temps moyen
            current_avg = patterns[subject]['avg_time']
            total = patterns[subject]['total']
            patterns[subject]['avg_time'] = (
                (current_avg * (total - 1) + answer[2]) / total  # response_time
            )
            
            # Progression de difficulté
            patterns[subject]['difficulty_progression'].append(answer[4])  # difficulty_level
        
        return patterns
    
    def _analyze_subject_performance(self, answers: List[Tuple]) -> Dict[str, float]:
        """Analyser la performance par matière"""
        subject_performance = {}
        
        for answer in answers:
            subject = answer[5]  # subject
            if subject not in subject_performance:
                subject_performance[subject] = {'correct': 0, 'total': 0}
            
            subject_performance[subject]['total'] += 1
            if answer[1]:  # is_correct
                subject_performance[subject]['correct'] += 1
        
        # Calculer les taux de réussite
        return {
            subject: data['correct'] / data['total'] 
            for subject, data in subject_performance.items()
        }
    
    def _calculate_learning_speed(self, answers: List[Tuple]) -> float:
        """Calculer la vitesse d'apprentissage"""
        if len(answers) < 2:
            return 1.0
        
        # Analyser la progression des performances
        early_answers = answers[:len(answers)//2]
        late_answers = answers[len(answers)//2:]
        
        early_accuracy = sum(1 for a in early_answers if a[1]) / len(early_answers)
        late_accuracy = sum(1 for a in late_answers if a[1]) / len(late_answers)
        
        if late_accuracy > early_accuracy:
            improvement = (late_accuracy - early_accuracy) / early_accuracy
            return 1.0 + min(1.0, improvement)
        else:
            return max(0.5, 1.0 - (early_accuracy - late_accuracy) / early_accuracy)

# Instance globale du moteur d'IA
adaptive_ai_engine = AdaptiveAIEngine()





















