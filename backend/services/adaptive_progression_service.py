#!/usr/bin/env python3
"""
Service de progression adaptative intelligente
"""

import json
import random
from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from models.french_learning import FrenchAdaptiveTest, FrenchLearningProfile
from models.question_history import QuestionHistory

class AdaptiveProgressionService:
    """Service pour la progression adaptative intelligente"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def analyze_student_performance(self, student_id: int, test_id: int) -> Dict[str, Any]:
        """Analyse complète de la performance de l'étudiant"""
        
        try:
            # Récupérer l'historique des questions du test
            question_history = self.db.query(QuestionHistory).filter(
                QuestionHistory.test_id == test_id
            ).all()
            
            if not question_history:
                return self._generate_default_profile()
            
            # Analyser les réponses
            total_questions = len(question_history)
            correct_answers = sum(1 for q in question_history if q.is_correct == 1)
            accuracy_rate = (correct_answers / total_questions) * 100 if total_questions > 0 else 0
            
            # Analyser la progression de difficulté
            difficulty_progression = self._analyze_difficulty_progression(question_history)
            
            # Analyser les sujets de faiblesse
            weak_topics = self._identify_weak_topics(question_history)
            
            # Analyser les patterns de réponse
            response_patterns = self._analyze_response_patterns(question_history)
            
            # Déterminer le niveau réel
            real_level = self._determine_real_level(accuracy_rate, difficulty_progression)
            
            # Générer un profil vraiment personnalisé
            personalized_profile = self._generate_personalized_profile(
                student_id, accuracy_rate, weak_topics, response_patterns, real_level
            )
            
            return {
                "performance_analysis": {
                    "total_questions": total_questions,
                    "correct_answers": correct_answers,
                    "accuracy_rate": accuracy_rate,
                    "difficulty_progression": difficulty_progression,
                    "weak_topics": weak_topics,
                    "response_patterns": response_patterns
                },
                "real_level": real_level,
                "personalized_profile": personalized_profile,
                "recommendations": self._generate_smart_recommendations(
                    real_level, weak_topics, accuracy_rate
                )
            }
            
        except Exception as e:
            print(f"❌ Erreur analyse performance: {e}")
            return self._generate_default_profile()
    
    def _analyze_difficulty_progression(self, questions: List[QuestionHistory]) -> Dict[str, Any]:
        """Analyse la progression de difficulté"""
        
        difficulty_counts = {}
        difficulty_accuracy = {}
        
        for q in questions:
            diff = q.difficulty
            difficulty_counts[diff] = difficulty_counts.get(diff, 0) + 1
            if diff not in difficulty_accuracy:
                difficulty_accuracy[diff] = {"correct": 0, "total": 0}
            
            difficulty_accuracy[diff]["total"] += 1
            if q.is_correct == 1:
                difficulty_accuracy[diff]["correct"] += 1
        
        # Calculer les taux de réussite par difficulté
        for diff in difficulty_accuracy:
            total = difficulty_accuracy[diff]["total"]
            correct = difficulty_accuracy[diff]["correct"]
            difficulty_accuracy[diff]["rate"] = (correct / total) * 100 if total > 0 else 0
        
        return {
            "distribution": difficulty_counts,
            "accuracy_by_difficulty": difficulty_accuracy,
            "progression_pattern": self._identify_progression_pattern(difficulty_accuracy)
        }
    
    def _identify_progression_pattern(self, difficulty_accuracy: Dict) -> str:
        """Identifie le pattern de progression"""
        
        if "easy" in difficulty_accuracy and "medium" in difficulty_accuracy:
            easy_rate = difficulty_accuracy["easy"]["rate"]
            medium_rate = difficulty_accuracy["medium"]["rate"]
            
            if easy_rate >= 80 and medium_rate >= 60:
                return "progressive_learner"
            elif easy_rate >= 90 and medium_rate >= 70:
                return "fast_learner"
            elif easy_rate < 70:
                return "needs_foundation"
        
        return "standard_learner"
    
    def _identify_weak_topics(self, questions: List[QuestionHistory]) -> List[str]:
        """Identifie les sujets de faiblesse"""
        
        topic_performance = {}
        
        for q in questions:
            topic = q.topic or "Sans topic"
            if topic not in topic_performance:
                topic_performance[topic] = {"correct": 0, "total": 0}
            
            topic_performance[topic]["total"] += 1
            if q.is_correct == 1:
                topic_performance[topic]["correct"] += 1
        
        # Identifier les sujets avec moins de 70% de réussite
        weak_topics = []
        for topic, perf in topic_performance.items():
            if perf["total"] >= 2:  # Au moins 2 questions pour être significatif
                rate = (perf["correct"] / perf["total"]) * 100
                if rate < 70:
                    weak_topics.append(topic)
        
        return weak_topics
    
    def _analyze_response_patterns(self, questions: List[QuestionHistory]) -> Dict[str, Any]:
        """Analyse les patterns de réponse"""
        
        patterns = {
            "confidence_level": "medium",
            "consistency": "medium",
            "learning_style_hint": "balanced"
        }
        
        # Analyser la consistance
        if len(questions) >= 3:
            recent_questions = questions[-3:]
            recent_correct = sum(1 for q in recent_questions if q.is_correct == 1)
            
            if recent_correct == 3:
                patterns["confidence_level"] = "high"
                patterns["consistency"] = "high"
            elif recent_correct == 0:
                patterns["confidence_level"] = "low"
                patterns["consistency"] = "low"
            elif recent_correct == 2:
                patterns["confidence_level"] = "medium"
                patterns["consistency"] = "medium"
        
        # Analyser le style d'apprentissage basé sur les topics
        topics = [q.topic for q in questions if q.topic]
        if "Articles" in topics and "Conjugaison" in topics:
            patterns["learning_style_hint"] = "grammar_focused"
        elif "Vocabulaire" in topics:
            patterns["learning_style_hint"] = "vocabulary_focused"
        
        return patterns
    
    def _determine_real_level(self, accuracy_rate: float, difficulty_progression: Dict) -> str:
        """Détermine le niveau réel basé sur la performance"""
        
        # Logique de progression intelligente
        if accuracy_rate >= 90:
            # Excellente performance, progression rapide
            if "hard" in difficulty_progression["distribution"]:
                return "B2"  # Niveau avancé
            elif "medium" in difficulty_progression["distribution"]:
                return "B1"  # Niveau intermédiaire avancé
            else:
                return "A2"  # Niveau intermédiaire
        elif accuracy_rate >= 80:
            # Bonne performance
            if "medium" in difficulty_progression["distribution"]:
                return "A2"  # Niveau intermédiaire
            else:
                return "A1+"  # Niveau débutant avancé
        elif accuracy_rate >= 60:
            # Performance moyenne
            return "A1"  # Niveau débutant
        else:
            # Performance faible
            return "A0"  # Niveau très débutant
    
    def _generate_personalized_profile(self, student_id: int, accuracy_rate: float, 
                                     weak_topics: List[str], response_patterns: Dict, 
                                     real_level: str) -> Dict[str, Any]:
        """Génère un profil vraiment personnalisé"""
        
        # Forces basées sur la performance réelle
        strengths = []
        if accuracy_rate >= 80:
            strengths.append("excellente compréhension")
        if accuracy_rate >= 70:
            strengths.append("bonne mémoire")
        if response_patterns["consistency"] == "high":
            strengths.append("apprentissage régulier")
        if "grammar_focused" in response_patterns["learning_style_hint"]:
            strengths.append("logique grammaticale")
        
        # Si pas de forces identifiées, utiliser des forces génériques mais adaptées
        if not strengths:
            if accuracy_rate >= 60:
                strengths = ["motivation", "persévérance"]
            else:
                strengths = ["détermination", "envie d'apprendre"]
        
        # Faiblesses basées sur l'analyse réelle
        if not weak_topics:
            # Analyser les sujets avec performance moyenne
            weak_topics = ["grammaire", "vocabulaire"] if accuracy_rate < 70 else ["perfectionnement"]
        
        # Style d'apprentissage basé sur les patterns réels
        learning_style = self._determine_learning_style(response_patterns, weak_topics)
        
        # Profil cognitif personnalisé
        cognitive_profile = {
            "memory_type": "visual" if "vocabulaire" not in weak_topics else "auditory",
            "attention_span": "long" if accuracy_rate >= 80 else "moyen",
            "problem_solving": "analytical" if "grammaire" not in weak_topics else "intuitive",
            "learning_speed": "rapide" if accuracy_rate >= 85 else "moyen",
            "confidence_level": response_patterns["confidence_level"]
        }
        
        return {
            "learning_style": learning_style,
            "french_level": real_level,
            "preferred_pace": "rapide" if accuracy_rate >= 80 else "moyen",
            "strengths": json.dumps(strengths),
            "weaknesses": json.dumps(weak_topics),
            "cognitive_profile": json.dumps(cognitive_profile),
            "ai_generated": True,
            "confidence_score": min(accuracy_rate / 100, 0.95),
            "personalization_score": self._calculate_personalization_score(accuracy_rate, weak_topics)
        }
    
    def _determine_learning_style(self, response_patterns: Dict, weak_topics: List[str]) -> str:
        """Détermine le style d'apprentissage basé sur les patterns"""
        
        if "grammar_focused" in response_patterns["learning_style_hint"]:
            return "analytical"
        elif "vocabulary_focused" in response_patterns["learning_style_hint"]:
            return "visual"
        elif response_patterns["consistency"] == "high":
            return "systematic"
        else:
            return "adaptive"
    
    def _calculate_personalization_score(self, accuracy_rate: float, weak_topics: List[str]) -> float:
        """Calcule un score de personnalisation"""
        
        base_score = accuracy_rate / 100
        
        # Bonus pour analyse détaillée
        if len(weak_topics) > 0:
            base_score += 0.1
        
        # Bonus pour performance élevée
        if accuracy_rate >= 85:
            base_score += 0.05
        
        return min(base_score, 1.0)
    
    def _generate_smart_recommendations(self, real_level: str, weak_topics: List[str], 
                                      accuracy_rate: float) -> List[str]:
        """Génère des recommandations intelligentes"""
        
        recommendations = []
        
        # Recommandations basées sur le niveau
        if real_level == "A0":
            recommendations.append("Renforcer les bases fondamentales")
        elif real_level == "A1":
            recommendations.append("Pratiquer la grammaire de base")
        elif real_level == "A2":
            recommendations.append("Développer le vocabulaire intermédiaire")
        elif real_level == "B1":
            recommendations.append("Travailler la compréhension orale")
        elif real_level == "B2":
            recommendations.append("Perfectionner l'expression écrite")
        
        # Recommandations basées sur les faiblesses
        for topic in weak_topics:
            if "grammaire" in topic.lower():
                recommendations.append("Exercices ciblés en grammaire")
            elif "vocabulaire" in topic.lower():
                recommendations.append("Enrichissement du vocabulaire")
            elif "conjugaison" in topic.lower():
                recommendations.append("Pratique des conjugaisons")
        
        # Recommandations basées sur la performance
        if accuracy_rate >= 90:
            recommendations.append("Progression vers des exercices plus avancés")
        elif accuracy_rate < 60:
            recommendations.append("Révision des concepts fondamentaux")
        
        return recommendations[:5]  # Limiter à 5 recommandations
    
    def _generate_default_profile(self) -> Dict[str, Any]:
        """Profil par défaut en cas d'erreur"""
        
        return {
            "performance_analysis": {
                "total_questions": 0,
                "correct_answers": 0,
                "accuracy_rate": 0,
                "difficulty_progression": {},
                "weak_topics": [],
                "response_patterns": {}
            },
            "real_level": "A1",
            "personalized_profile": {
                "learning_style": "visual",
                "french_level": "A1",
                "preferred_pace": "moyen",
                "strengths": json.dumps(["motivation"]),
                "weaknesses": json.dumps(["grammaire", "vocabulaire"]),
                "cognitive_profile": json.dumps({
                    "memory_type": "visual",
                    "attention_span": "moyen",
                    "problem_solving": "analytical"
                }),
                "ai_generated": False,
                "confidence_score": 0.5,
                "personalization_score": 0.3
            },
            "recommendations": [
                "Commencer par les bases",
                "Pratiquer régulièrement",
                "Demander de l'aide si nécessaire"
            ]
        }











