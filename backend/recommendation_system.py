#!/usr/bin/env python3
"""
Système de Recommandation Intelligent pour Najah AI
Section 2.2.3 : Système de recommandation et Section 3.2 : Technologie IA
"""

import sqlite3
import json
import random
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta
import numpy as np
from collections import defaultdict

@dataclass
class LearningResource:
    """Ressource d'apprentissage recommandée"""
    resource_id: int
    title: str
    description: str
    type: str  # 'video', 'exercice', 'document', 'quiz', 'jeu'
    difficulty: str
    category: str
    estimated_duration: int  # en minutes
    relevance_score: float  # 0.0 à 1.0
    learning_style_match: float  # compatibilité avec le style d'apprentissage

@dataclass
class LearningActivity:
    """Activité d'apprentissage recommandée"""
    activity_id: int
    title: str
    description: str
    type: str  # 'pratique', 'révision', 'défi', 'évaluation'
    difficulty: str
    target_skills: List[str]
    estimated_time: int
    challenge_level: float  # 0.0 à 1.0
    reinforcement_value: float  # valeur de renforcement

class RecommendationEngine:
    """Moteur de recommandation intelligent"""
    
    def __init__(self, db_path: str = "./data/app.db"):
        self.db_path = db_path
        self.conn = None
        self.cursor = None
        self.connect_db()
        
        # Paramètres de personnalisation
        self.difficulty_weights = {
            'débutant': 1.0,
            'intermédiaire': 1.2,
            'avancé': 1.5
        }
        
        self.learning_style_preferences = {
            'visuel': ['video', 'infographie', 'schéma'],
            'auditif': ['audio', 'podcast', 'explication'],
            'kinesthésique': ['exercice', 'jeu', 'manipulation'],
            'lecture-écriture': ['document', 'livre', 'écriture']
        }
    
    def connect_db(self):
        """Connexion à la base de données"""
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()
            print("✅ Connexion à la base de données établie")
        except Exception as e:
            print(f"❌ Erreur de connexion : {e}")
    
    def get_personalized_recommendations(self, student_id: int, 
                                       category: str = None, 
                                       limit: int = 5) -> List[LearningResource]:
        """Obtenir des recommandations personnalisées pour un étudiant"""
        try:
            # Analyser le profil et les performances
            student_analysis = self.analyze_student_performance(student_id)
            
            # Générer des recommandations basées sur l'analyse
            recommendations = []
            
            # 1. Recommandations basées sur les faiblesses
            if student_analysis['weaknesses']:
                weakness_recommendations = self.get_recommendations_for_weaknesses(
                    student_analysis['weaknesses'], 
                    student_analysis['learning_style'],
                    limit // 2
                )
                recommendations.extend(weakness_recommendations)
            
            # 2. Recommandations basées sur les forces (pour renforcer)
            if student_analysis['strengths']:
                strength_recommendations = self.get_recommendations_for_strengths(
                    student_analysis['strengths'],
                    student_analysis['learning_style'],
                    limit // 4
                )
                recommendations.extend(strength_recommendations)
            
            # 3. Recommandations de découverte (nouvelles matières)
            discovery_recommendations = self.get_discovery_recommendations(
                student_id,
                student_analysis['learning_style'],
                limit - len(recommendations)
            )
            recommendations.extend(discovery_recommendations)
            
            # Trier par score de pertinence
            recommendations.sort(key=lambda x: x.relevance_score, reverse=True)
            
            return recommendations[:limit]
            
        except Exception as e:
            print(f"❌ Erreur lors de la génération des recommandations : {e}")
            return []
    
    def analyze_student_performance(self, student_id: int) -> Dict:
        """Analyser les performances de l'étudiant pour personnaliser les recommandations"""
        try:
            # Récupérer l'historique des réponses
            self.cursor.execute("""
                SELECT 
                    q.difficulty_level,
                    c.name as category,
                    sa.is_correct,
                    sa.points_earned,
                    sa.answered_at,
                    q.points as max_points
                FROM student_answers sa
                JOIN assessment_questions q ON sa.question_id = q.id
                JOIN question_categories c ON q.category_id = c.id
                WHERE sa.student_id = ?
                ORDER BY sa.answered_at DESC
                LIMIT 100
            """, (student_id,))
            
            results = self.cursor.fetchall()
            
            if not results:
                return self.get_default_analysis()
            
            # Analyser les patterns
            category_performance = defaultdict(list)
            difficulty_performance = defaultdict(list)
            recent_performance = []
            
            for result in results:
                difficulty, category, is_correct, points_earned, answered_at, max_points = result
                
                # Performance par catégorie
                accuracy = points_earned / max_points if max_points > 0 else 0
                category_performance[category].append(accuracy)
                
                # Performance par difficulté
                difficulty_performance[difficulty].append(accuracy)
                
                # Performance récente (dernières 2 semaines)
                if datetime.now() - datetime.fromisoformat(answered_at) < timedelta(weeks=2):
                    recent_performance.append(accuracy)
            
            # Calculer les moyennes
            avg_category_performance = {
                cat: np.mean(perfs) for cat, perfs in category_performance.items()
            }
            avg_difficulty_performance = {
                diff: np.mean(perfs) for diff, perfs in difficulty_performance.items()
            }
            
            # Déterminer les forces et faiblesses
            strengths = [cat for cat, perf in avg_category_performance.items() if perf > 0.7]
            weaknesses = [cat for cat, perf in avg_category_performance.items() if perf < 0.5]
            
            # Déterminer le style d'apprentissage (basé sur les patterns de performance)
            learning_style = self.detect_learning_style_from_performance(avg_category_performance)
            
            # Calculer le niveau global
            global_level = self.calculate_global_level(avg_difficulty_performance)
            
            # Tendances récentes
            recent_trend = np.mean(recent_performance) if recent_performance else 0.5
            
            return {
                'strengths': strengths,
                'weaknesses': weaknesses,
                'learning_style': learning_style,
                'global_level': global_level,
                'recent_trend': recent_trend,
                'category_performance': avg_category_performance,
                'difficulty_performance': avg_difficulty_performance
            }
            
        except Exception as e:
            print(f"❌ Erreur lors de l'analyse des performances : {e}")
            return self.get_default_analysis()
    
    def get_default_analysis(self) -> Dict:
        """Retourner une analyse par défaut"""
        return {
            'strengths': [],
            'weaknesses': ['Mathématiques', 'Français'],
            'learning_style': 'visuel',
            'global_level': 'débutant',
            'recent_trend': 0.5,
            'category_performance': {},
            'difficulty_performance': {}
        }
    
    def detect_learning_style_from_performance(self, category_performance: Dict[str, float]) -> str:
        """Détecter le style d'apprentissage basé sur les performances par catégorie"""
        if not category_performance:
            return 'visuel'
        
        # Analyser les performances par type de matière
        visual_subjects = ['Mathématiques', 'Géométrie', 'Sciences']
        auditory_subjects = ['Français', 'Langues', 'Histoire']
        kinesthetic_subjects = ['Logique', 'Résolution de problèmes']
        
        visual_score = np.mean([category_performance.get(cat, 0) for cat in visual_subjects])
        auditory_score = np.mean([category_performance.get(cat, 0) for cat in auditory_subjects])
        kinesthetic_score = np.mean([category_performance.get(cat, 0) for cat in kinesthetic_subjects])
        
        scores = [
            ('visuel', visual_score),
            ('auditif', auditory_score),
            ('kinesthésique', kinesthetic_score)
        ]
        
        return max(scores, key=lambda x: x[1])[0]
    
    def calculate_global_level(self, difficulty_performance: Dict[str, float]) -> str:
        """Calculer le niveau global de l'étudiant"""
        if not difficulty_performance:
            return 'débutant'
        
        # Pondérer par difficulté
        weighted_score = 0
        total_weight = 0
        
        for difficulty, performance in difficulty_performance.items():
            weight = self.difficulty_weights.get(difficulty, 1.0)
            weighted_score += performance * weight
            total_weight += weight
        
        if total_weight == 0:
            return 'débutant'
        
        avg_weighted_score = weighted_score / total_weight
        
        if avg_weighted_score > 0.7:
            return 'avancé'
        elif avg_weighted_score > 0.4:
            return 'intermédiaire'
        else:
            return 'débutant'
    
    def get_recommendations_for_weaknesses(self, weaknesses: List[str], 
                                         learning_style: str, 
                                         limit: int) -> List[LearningResource]:
        """Obtenir des recommandations pour améliorer les faiblesses"""
        recommendations = []
        
        for weakness in weaknesses[:limit]:
            # Créer des ressources virtuelles pour les faiblesses
            resource = LearningResource(
                resource_id=len(recommendations) + 1,
                title=f"Révision {weakness} - Niveau Débutant",
                description=f"Ressources pour renforcer vos bases en {weakness}",
                type=self.get_best_resource_type(learning_style),
                difficulty='débutant',
                category=weakness,
                estimated_duration=15,
                relevance_score=0.9,
                learning_style_match=0.8
            )
            recommendations.append(resource)
        
        return recommendations
    
    def get_recommendations_for_strengths(self, strengths: List[str], 
                                        learning_style: str, 
                                        limit: int) -> List[LearningResource]:
        """Obtenir des recommandations pour renforcer les forces"""
        recommendations = []
        
        for strength in strengths[:limit]:
            # Créer des ressources de renforcement
            resource = LearningResource(
                resource_id=len(recommendations) + 1000,
                title=f"Perfectionnement {strength} - Niveau Avancé",
                description=f"Exercices avancés pour exceller en {strength}",
                type=self.get_best_resource_type(learning_style),
                difficulty='avancé',
                category=strength,
                estimated_duration=20,
                relevance_score=0.7,
                learning_style_match=0.9
            )
            recommendations.append(resource)
        
        return recommendations
    
    def get_discovery_recommendations(self, student_id: int, 
                                   learning_style: str, 
                                   limit: int) -> List[LearningResource]:
        """Obtenir des recommandations de découverte"""
        recommendations = []
        
        # Matières à découvrir
        discovery_categories = ['Technologie', 'Arts', 'Philosophie', 'Culture générale']
        
        for category in discovery_categories[:limit]:
            resource = LearningResource(
                resource_id=len(recommendations) + 2000,
                title=f"Découverte {category}",
                description=f"Introduction à {category} pour élargir vos horizons",
                type=self.get_best_resource_type(learning_style),
                difficulty='débutant',
                category=category,
                estimated_duration=25,
                relevance_score=0.6,
                learning_style_match=0.7
            )
            recommendations.append(resource)
        
        return recommendations
    
    def get_best_resource_type(self, learning_style: str) -> str:
        """Obtenir le meilleur type de ressource pour un style d'apprentissage"""
        preferred_types = self.learning_style_preferences.get(learning_style, ['document'])
        return random.choice(preferred_types)
    
    def recommend_learning_activities(self, student_id: int, 
                                    target_skill: str = None,
                                    activity_type: str = None) -> List[LearningActivity]:
        """Recommander des activités d'apprentissage personnalisées"""
        try:
            # Analyser le profil de l'étudiant
            analysis = self.analyze_student_performance(student_id)
            
            # Déterminer le type d'activité optimal
            if not activity_type:
                activity_type = self.get_optimal_activity_type(analysis)
            
            # Déterminer la compétence cible
            if not target_skill:
                target_skill = self.get_optimal_target_skill(analysis)
            
            # Créer des activités personnalisées
            activities = []
            
            # Activité de pratique
            practice_activity = LearningActivity(
                activity_id=1,
                title=f"Pratique {target_skill}",
                description=f"Exercices pratiques pour renforcer {target_skill}",
                type='pratique',
                difficulty=analysis['global_level'],
                target_skills=[target_skill],
                estimated_time=20,
                challenge_level=0.6,
                reinforcement_value=0.8
            )
            activities.append(practice_activity)
            
            # Activité de révision
            review_activity = LearningActivity(
                activity_id=2,
                title=f"Révision {target_skill}",
                description=f"Révision des concepts clés de {target_skill}",
                type='révision',
                difficulty=analysis['global_level'],
                target_skills=[target_skill],
                estimated_time=15,
                challenge_level=0.4,
                reinforcement_value=0.9
            )
            activities.append(review_activity)
            
            # Défi d'apprentissage
            challenge_activity = LearningActivity(
                activity_id=3,
                title=f"Défi {target_skill}",
                description=f"Défi pour tester vos compétences en {target_skill}",
                type='défi',
                difficulty=self.get_next_difficulty(analysis['global_level']),
                target_skills=[target_skill],
                estimated_time=30,
                challenge_level=0.8,
                reinforcement_value=0.7
            )
            activities.append(challenge_activity)
            
            return activities
            
        except Exception as e:
            print(f"❌ Erreur lors de la recommandation d'activités : {e}")
            return []
    
    def get_optimal_activity_type(self, analysis: Dict) -> str:
        """Déterminer le type d'activité optimal basé sur l'analyse"""
        if analysis['recent_trend'] < 0.4:
            return 'révision'  # Besoin de renforcement
        elif analysis['recent_trend'] > 0.7:
            return 'défi'  # Prêt pour des défis
        else:
            return 'pratique'  # Équilibre
    
    def get_optimal_target_skill(self, analysis: Dict) -> str:
        """Déterminer la compétence cible optimale"""
        if analysis['weaknesses']:
            return random.choice(analysis['weaknesses'])
        elif analysis['strengths']:
            return random.choice(analysis['strengths'])
        else:
            return 'Mathématiques'  # Compétence par défaut
    
    def get_next_difficulty(self, current_level: str) -> str:
        """Obtenir le niveau de difficulté suivant"""
        levels = ['débutant', 'intermédiaire', 'avancé']
        current_index = levels.index(current_level)
        
        if current_index < len(levels) - 1:
            return levels[current_index + 1]
        else:
            return current_level
    
    def predict_performance(self, student_id: int, skill: str, 
                          time_horizon: str = '1_week') -> Dict:
        """Prédire les performances futures de l'étudiant"""
        try:
            # Analyser les tendances historiques
            analysis = self.analyze_student_performance(student_id)
            
            # Calculer la tendance de progression
            current_performance = analysis['category_performance'].get(skill, 0.5)
            recent_trend = analysis['recent_trend']
            
            # Prédiction basée sur la tendance
            if time_horizon == '1_week':
                predicted_performance = current_performance + (recent_trend - 0.5) * 0.1
            elif time_horizon == '1_month':
                predicted_performance = current_performance + (recent_trend - 0.5) * 0.3
            else:  # 3_months
                predicted_performance = current_performance + (recent_trend - 0.5) * 0.5
            
            # Limiter les valeurs
            predicted_performance = max(0.0, min(1.0, predicted_performance))
            
            # Calculer la confiance de la prédiction
            confidence = self.calculate_prediction_confidence(analysis, skill)
            
            return {
                'skill': skill,
                'current_performance': current_performance,
                'predicted_performance': predicted_performance,
                'time_horizon': time_horizon,
                'confidence': confidence,
                'factors': {
                    'recent_trend': recent_trend,
                    'learning_style': analysis['learning_style'],
                    'global_level': analysis['global_level']
                }
            }
            
        except Exception as e:
            print(f"❌ Erreur lors de la prédiction : {e}")
            return {'error': str(e)}
    
    def calculate_prediction_confidence(self, analysis: Dict, skill: str) -> float:
        """Calculer la confiance de la prédiction"""
        # Plus de données = plus de confiance
        data_points = len(analysis['category_performance'])
        
        if data_points < 5:
            return 0.3  # Faible confiance
        elif data_points < 20:
            return 0.6  # Confiance moyenne
        else:
            return 0.8  # Haute confiance
    
    def get_adaptive_challenges(self, student_id: int, 
                              skill: str, 
                              challenge_count: int = 3) -> List[Dict]:
        """Générer des défis adaptatifs personnalisés"""
        try:
            analysis = self.analyze_student_performance(student_id)
            current_level = analysis['global_level']
            
            challenges = []
            
            for i in range(challenge_count):
                # Défi progressif
                if i == 0:
                    difficulty = current_level
                elif i == 1:
                    difficulty = self.get_next_difficulty(current_level)
                else:
                    difficulty = self.get_next_difficulty(self.get_next_difficulty(current_level))
                
                challenge = {
                    'id': i + 1,
                    'title': f"Défi {skill} - Niveau {difficulty}",
                    'description': f"Testez vos compétences en {skill} avec ce défi {difficulty}",
                    'difficulty': difficulty,
                    'skill': skill,
                    'estimated_time': 15 + (i * 5),  # Temps croissant
                    'challenge_level': 0.5 + (i * 0.2),  # Niveau croissant
                    'reward_multiplier': 1.0 + (i * 0.3)  # Récompense croissante
                }
                
                challenges.append(challenge)
            
            return challenges
            
        except Exception as e:
            print(f"❌ Erreur lors de la génération des défis : {e}")
            return []
    
    def close(self):
        """Fermer la connexion à la base de données"""
        if self.conn:
            self.conn.close()

# Exemple d'utilisation
if __name__ == "__main__":
    engine = RecommendationEngine()
    
    print("🎯 Test du Système de Recommandation Intelligent")
    print("=" * 60)
    
    student_id = 1
    
    # Analyser les performances
    analysis = engine.analyze_student_performance(student_id)
    print(f"📊 Analyse de l'étudiant {student_id}:")
    print(f"   • Niveau global: {analysis['global_level']}")
    print(f"   • Style d'apprentissage: {analysis['learning_style']}")
    print(f"   • Forces: {', '.join(analysis['strengths']) if analysis['strengths'] else 'Aucune'}")
    print(f"   • Faiblesses: {', '.join(analysis['weaknesses']) if analysis['weaknesses'] else 'Aucune'}")
    print(f"   • Tendance récente: {analysis['recent_trend']:.2f}")
    
    # Obtenir des recommandations
    recommendations = engine.get_personalized_recommendations(student_id, limit=5)
    print(f"\n💡 Recommandations personnalisées ({len(recommendations)}):")
    for i, rec in enumerate(recommendations, 1):
        print(f"   {i}. {rec.title} ({rec.category}) - Score: {rec.relevance_score:.2f}")
    
    # Prédire les performances
    prediction = engine.predict_performance(student_id, "Mathématiques", "1_month")
    print(f"\n🔮 Prédiction de performance - Mathématiques (1 mois):")
    print(f"   • Performance actuelle: {prediction['current_performance']:.2f}")
    print(f"   • Performance prédite: {prediction['predicted_performance']:.2f}")
    print(f"   • Confiance: {prediction['confidence']:.2f}")
    
    # Générer des défis adaptatifs
    challenges = engine.get_adaptive_challenges(student_id, "Mathématiques", 3)
    print(f"\n🏆 Défis adaptatifs - Mathématiques:")
    for challenge in challenges:
        print(f"   • {challenge['title']} - Niveau: {challenge['challenge_level']:.2f}")
    
    engine.close()
