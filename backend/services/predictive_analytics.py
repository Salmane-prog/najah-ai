#!/usr/bin/env python3
"""
Service d'Analyse Prédictive pour l'Évaluation Adaptative
Prédit les performances futures et détecte les blocages d'apprentissage
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional, Any
import sqlite3
import logging

logger = logging.getLogger(__name__)

class PredictiveAnalytics:
    """Service d'analyse prédictive avancée"""
    
    def __init__(self, db_path: str = "./data/app.db"):
        self.db_path = db_path
        self.prediction_models = {}
        
    def predict_student_performance(
        self, 
        student_id: int, 
        test_id: int, 
        horizon_days: int = 30
    ) -> Dict[str, Any]:
        """Prédire les performances futures d'un étudiant"""
        try:
            # Analyser l'historique des performances
            performance_data = self._get_performance_history(student_id, test_id)
            
            if not performance_data:
                return {"error": "Données insuffisantes pour la prédiction"}
            
            # Prédictions
            predictions = {
                'predicted_score': self._predict_final_score(performance_data),
                'completion_time': self._predict_completion_time(performance_data),
                'difficulty_progression': self._predict_difficulty_progression(performance_data),
                'risk_factors': self._identify_risk_factors(performance_data),
                'confidence_level': self._calculate_prediction_confidence(performance_data),
                'recommendations': self._generate_predictive_recommendations(performance_data)
            }
            
            return predictions
            
        except Exception as e:
            logger.error(f"Erreur lors de la prédiction: {e}")
            return {"error": str(e)}
    
    def detect_learning_blockages(self, student_id: int, test_id: int) -> Dict[str, Any]:
        """Détecter les blocages d'apprentissage"""
        try:
            # Analyser les patterns de réponses
            response_patterns = self._analyze_response_patterns(student_id, test_id)
            
            blockages = {
                'detected_blockages': [],
                'confidence_level': 0.0,
                'intervention_suggestions': []
            }
            
            # Détecter les blocages
            if self._detect_plateau_effect(response_patterns):
                blockages['detected_blockages'].append({
                    'type': 'plateau_effect',
                    'description': 'L\'étudiant semble bloqué à un niveau de difficulté',
                    'severity': 'medium'
                })
            
            if self._detect_regression(response_patterns):
                blockages['detected_blockages'].append({
                    'type': 'regression',
                    'description': 'Dégradation des performances',
                    'severity': 'high'
                })
            
            if self._detect_time_increase(response_patterns):
                blockages['detected_blockages'].append({
                    'type': 'time_increase',
                    'description': 'Augmentation du temps de réponse',
                    'severity': 'low'
                })
            
            # Calculer le niveau de confiance
            blockages['confidence_level'] = self._calculate_blockage_confidence(response_patterns)
            
            # Générer des suggestions d'intervention
            blockages['intervention_suggestions'] = self._generate_intervention_suggestions(blockages)
            
            return blockages
            
        except Exception as e:
            logger.error(f"Erreur lors de la détection des blocages: {e}")
            return {"error": str(e)}
    
    def _get_performance_history(self, student_id: int, test_id: int) -> List[Dict]:
        """Récupérer l'historique des performances"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT 
                sa.created_at,
                sa.is_correct,
                sa.response_time,
                aq.difficulty_level,
                aq.subject
            FROM student_answers sa
            JOIN adaptive_questions aq ON sa.question_id = aq.id
            JOIN student_adaptive_tests sat ON sa.student_test_id = sat.id
            WHERE sat.student_id = ? AND sat.test_id = ?
            ORDER BY sa.created_at
        """, (student_id, test_id))
        
        results = cursor.fetchall()
        conn.close()
        
        return [
            {
                'timestamp': row[0],
                'is_correct': row[1],
                'response_time': row[2],
                'difficulty': row[3],
                'subject': row[4]
            }
            for row in results
        ]
    
    def _predict_final_score(self, performance_data: List[Dict]) -> float:
        """Prédire le score final"""
        if len(performance_data) < 3:
            return 0.0
        
        # Calculer le taux de réussite actuel
        correct_answers = sum(1 for p in performance_data if p['is_correct'])
        current_accuracy = correct_answers / len(performance_data)
        
        # Ajuster selon la tendance
        trend = self._calculate_performance_trend(performance_data)
        
        # Prédiction basée sur la tendance
        predicted_accuracy = current_accuracy + (trend * 0.1)
        
        return min(100.0, max(0.0, predicted_accuracy * 100))
    
    def _predict_completion_time(self, performance_data: List[Dict]) -> int:
        """Prédire le temps de completion en minutes"""
        if len(performance_data) < 2:
            return 0
        
        # Temps moyen par question
        avg_time_per_question = np.mean([p['response_time'] for p in performance_data])
        
        # Estimation du nombre total de questions (basé sur la difficulté)
        estimated_total_questions = self._estimate_total_questions(performance_data)
        
        # Temps restant estimé
        remaining_questions = estimated_total_questions - len(performance_data)
        estimated_completion_time = remaining_questions * avg_time_per_question
        
        return int(estimated_completion_time / 60)  # Convertir en minutes
    
    def _predict_difficulty_progression(self, performance_data: List[Dict]) -> List[float]:
        """Prédire la progression de difficulté"""
        if len(performance_data) < 3:
            return []
        
        difficulties = [p['difficulty'] for p in performance_data]
        
        # Régression linéaire simple pour prédire la progression
        x = np.arange(len(difficulties))
        coeffs = np.polyfit(x, difficulties, 1)
        
        # Prédire les 5 prochaines questions
        future_x = np.arange(len(difficulties), len(difficulties) + 5)
        predicted_difficulties = np.polyval(coeffs, future_x)
        
        return np.clip(predicted_difficulties, 1.0, 10.0).tolist()
    
    def _identify_risk_factors(self, performance_data: List[Dict]) -> List[Dict]:
        """Identifier les facteurs de risque"""
        risk_factors = []
        
        # Risque de faible performance
        if len(performance_data) >= 5:
            recent_accuracy = sum(1 for p in performance_data[-5:] if p['is_correct']) / 5
            if recent_accuracy < 0.4:
                risk_factors.append({
                    'factor': 'low_recent_accuracy',
                    'value': recent_accuracy,
                    'threshold': 0.4,
                    'severity': 'high'
                })
        
        # Risque de temps de réponse élevé
        avg_response_time = np.mean([p['response_time'] for p in performance_data])
        if avg_response_time > 60.0:  # Plus d'1 minute en moyenne
            risk_factors.append({
                'factor': 'high_response_time',
                'value': avg_response_time,
                'threshold': 60.0,
                'severity': 'medium'
            })
        
        # Risque de stagnation
        if len(performance_data) >= 10:
            early_accuracy = sum(1 for p in performance_data[:5] if p['is_correct']) / 5
            late_accuracy = sum(1 for p in performance_data[-5:] if p['is_correct']) / 5
            if abs(late_accuracy - early_accuracy) < 0.1:
                risk_factors.append({
                    'factor': 'performance_stagnation',
                    'value': abs(late_accuracy - early_accuracy),
                    'threshold': 0.1,
                    'severity': 'medium'
                })
        
        return risk_factors
    
    def _calculate_prediction_confidence(self, performance_data: List[Dict]) -> float:
        """Calculer le niveau de confiance des prédictions"""
        if len(performance_data) < 5:
            return 0.3
        
        # Facteurs de confiance
        data_quantity_factor = min(1.0, len(performance_data) / 20.0)  # Plus de données = plus de confiance
        
        # Consistance des performances
        accuracies = []
        for i in range(0, len(performance_data) - 4, 5):
            batch = performance_data[i:i+5]
            if len(batch) == 5:
                accuracy = sum(1 for p in batch if p['is_correct']) / 5
                accuracies.append(accuracy)
        
        if len(accuracies) >= 2:
            consistency_factor = 1.0 - np.std(accuracies)  # Moins de variance = plus de confiance
        else:
            consistency_factor = 0.5
        
        # Confiance finale
        confidence = (data_quantity_factor * 0.6 + consistency_factor * 0.4)
        
        return np.clip(confidence, 0.0, 1.0)
    
    def _generate_predictive_recommendations(self, performance_data: List[Dict]) -> List[Dict]:
        """Générer des recommandations basées sur les prédictions"""
        recommendations = []
        
        # Analyser les tendances
        trend = self._calculate_performance_trend(performance_data)
        
        if trend < -0.1:  # Tendance négative
            recommendations.append({
                'type': 'intervention',
                'priority': 'high',
                'action': 'Réviser les concepts de base',
                'reasoning': 'Tendance de performance décroissante détectée'
            })
        
        # Analyser les matières
        subject_performance = {}
        for p in performance_data:
            subject = p['subject']
            if subject not in subject_performance:
                subject_performance[subject] = {'correct': 0, 'total': 0}
            subject_performance[subject]['total'] += 1
            if p['is_correct']:
                subject_performance[subject]['correct'] += 1
        
        for subject, data in subject_performance.items():
            if data['total'] >= 3:
                accuracy = data['correct'] / data['total']
                if accuracy < 0.5:
                    recommendations.append({
                        'type': 'subject_focus',
                        'priority': 'medium',
                        'action': f'Se concentrer sur {subject}',
                        'reasoning': f'Performance faible en {subject} ({accuracy:.1%})'
                    })
        
        return recommendations
    
    def _calculate_performance_trend(self, performance_data: List[Dict]) -> float:
        """Calculer la tendance des performances"""
        if len(performance_data) < 5:
            return 0.0
        
        # Diviser en périodes et calculer la tendance
        mid_point = len(performance_data) // 2
        
        early_performance = performance_data[:mid_point]
        late_performance = performance_data[mid_point:]
        
        early_accuracy = sum(1 for p in early_performance if p['is_correct']) / len(early_performance)
        late_accuracy = sum(1 for p in late_performance if p['is_correct']) / len(late_performance)
        
        return late_accuracy - early_accuracy
    
    def _estimate_total_questions(self, performance_data: List[Dict]) -> int:
        """Estimer le nombre total de questions"""
        # Estimation basée sur la difficulté moyenne et la performance
        avg_difficulty = np.mean([p['difficulty'] for p in performance_data])
        current_accuracy = sum(1 for p in performance_data if p['is_correct']) / len(performance_data)
        
        # Plus la difficulté est élevée et la performance bonne, plus il y aura de questions
        base_questions = 15
        difficulty_factor = avg_difficulty / 5.0
        performance_factor = current_accuracy
        
        estimated = base_questions * difficulty_factor * (1 + performance_factor)
        
        return int(np.clip(estimated, 10, 30))
    
    def _analyze_response_patterns(self, student_id: int, test_id: int) -> Dict[str, Any]:
        """Analyser les patterns de réponses"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT 
                sa.is_correct,
                sa.response_time,
                aq.difficulty_level
            FROM student_answers sa
            JOIN adaptive_questions aq ON sa.question_id = aq.id
            JOIN student_adaptive_tests sat ON sa.student_test_id = sat.id
            WHERE sat.student_id = ? AND sat.test_id = ?
            ORDER BY sa.created_at
        """, (student_id, test_id))
        
        results = cursor.fetchall()
        conn.close()
        
        return {
            'responses': [
                {'is_correct': r[0], 'response_time': r[1], 'difficulty': r[2]}
                for r in results
            ]
        }
    
    def _detect_plateau_effect(self, response_patterns: Dict[str, Any]) -> bool:
        """Détecter l'effet de plateau"""
        responses = response_patterns['responses']
        if len(responses) < 8:
            return False
        
        # Analyser les 8 dernières réponses
        recent_responses = responses[-8:]
        
        # Vérifier si la performance reste stable
        correct_count = sum(1 for r in recent_responses if r['is_correct'])
        accuracy = correct_count / len(recent_responses)
        
        # Si la performance est stable autour de 50%, c'est un plateau
        return 0.4 <= accuracy <= 0.6
    
    def _detect_regression(self, response_patterns: Dict[str, Any]) -> bool:
        """Détecter la régression des performances"""
        responses = response_patterns['responses']
        if len(responses) < 6:
            return False
        
        # Comparer les performances récentes vs anciennes
        early_responses = responses[:3]
        late_responses = responses[-3:]
        
        early_accuracy = sum(1 for r in early_responses if r['is_correct']) / 3
        late_accuracy = sum(1 for r in late_responses if r['is_correct']) / 3
        
        # Régression si la performance récente est significativement plus faible
        return late_accuracy < early_accuracy - 0.3
    
    def _detect_time_increase(self, response_patterns: Dict[str, Any]) -> bool:
        """Détecter l'augmentation du temps de réponse"""
        responses = response_patterns['responses']
        if len(responses) < 6:
            return False
        
        # Comparer les temps de réponse
        early_times = [r['response_time'] for r in responses[:3]]
        late_times = [r['response_time'] for r in responses[-3:]]
        
        early_avg = np.mean(early_times)
        late_avg = np.mean(late_times)
        
        # Augmentation significative du temps
        return late_avg > early_avg * 1.5
    
    def _calculate_blockage_confidence(self, response_patterns: Dict[str, Any]) -> float:
        """Calculer le niveau de confiance de la détection de blocage"""
        responses = response_patterns['responses']
        if len(responses) < 5:
            return 0.0
        
        # Facteurs de confiance
        data_quantity = min(1.0, len(responses) / 10.0)
        
        # Consistance des patterns
        pattern_consistency = 0.0
        if self._detect_plateau_effect(response_patterns):
            pattern_consistency += 0.4
        if self._detect_regression(response_patterns):
            pattern_consistency += 0.4
        if self._detect_time_increase(response_patterns):
            pattern_consistency += 0.2
        
        confidence = (data_quantity * 0.3 + pattern_consistency * 0.7)
        return np.clip(confidence, 0.0, 1.0)
    
    def _generate_intervention_suggestions(self, blockages: Dict[str, Any]) -> List[Dict]:
        """Générer des suggestions d'intervention"""
        suggestions = []
        
        for blockage in blockages['detected_blockages']:
            if blockage['type'] == 'plateau_effect':
                suggestions.append({
                    'intervention': 'Révision ciblée',
                    'description': 'Revoir les concepts de base de la matière',
                    'duration': '30-45 minutes',
                    'priority': 'medium'
                })
            
            elif blockage['type'] == 'regression':
                suggestions.append({
                    'intervention': 'Intervention immédiate',
                    'description': 'Identifier et corriger les difficultés spécifiques',
                    'duration': '1 heure',
                    'priority': 'high'
                })
            
            elif blockage['type'] == 'time_increase':
                suggestions.append({
                    'intervention': 'Support méthodologique',
                    'description': 'Aider à améliorer les stratégies de résolution',
                    'duration': '20-30 minutes',
                    'priority': 'low'
                })
        
        return suggestions

# Instance globale du service d'analyse prédictive
predictive_analytics = PredictiveAnalytics()
























