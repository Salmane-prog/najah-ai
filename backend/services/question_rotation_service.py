#!/usr/bin/env python3
"""
Service intelligent pour la rotation des questions adaptatives
"""

import random
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from models.question_history import QuestionHistory
from models.french_learning import FrenchAdaptiveTest
from datetime import datetime

class QuestionRotationService:
    """Service pour gérer la rotation intelligente des questions"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_available_questions(
        self, 
        difficulty: str, 
        test_id: int, 
        question_pool: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Récupère les questions disponibles en évitant les répétitions
        
        Args:
            difficulty: Niveau de difficulté
            test_id: ID du test en cours
            question_pool: Pool de questions disponibles
            
        Returns:
            Liste des questions non utilisées
        """
        try:
            # Récupérer les questions déjà posées dans ce test
            asked_questions = self.db.query(QuestionHistory.question_id).filter(
                QuestionHistory.test_id == test_id
            ).all()
            
            asked_ids = [q[0] for q in asked_questions]
            
            # Filtrer les questions non utilisées
            available_questions = [
                q for q in question_pool 
                if q["difficulty"] == difficulty and q["id"] not in asked_ids
            ]
            
            # Si toutes les questions ont été utilisées, réinitialiser
            if not available_questions:
                print(f"🔄 Toutes les questions de difficulté '{difficulty}' ont été utilisées, réinitialisation...")
                available_questions = [
                    q for q in question_pool 
                    if q["difficulty"] == difficulty
                ]
                
                # Nettoyer l'historique pour ce test et cette difficulté
                self._clean_question_history(test_id, difficulty)
            
            return available_questions
            
        except Exception as e:
            print(f"❌ Erreur lors de la récupération des questions disponibles: {e}")
            # Fallback : retourner toutes les questions de la difficulté
            return [q for q in question_pool if q["difficulty"] == difficulty]
    
    def select_optimal_question(
        self, 
        difficulty: str, 
        test_id: int, 
        question_pool: List[Dict[str, Any]],
        student_performance: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Sélectionne la question optimale en évitant les répétitions
        
        Args:
            difficulty: Niveau de difficulté
            test_id: ID du test en cours
            question_pool: Pool de questions disponibles
            student_performance: Performance de l'étudiant (optionnel)
            
        Returns:
            Question sélectionnée
        """
        try:
            # Récupérer les questions disponibles
            available_questions = self.get_available_questions(difficulty, test_id, question_pool)
            
            if not available_questions:
                print(f"⚠️ Aucune question disponible pour la difficulté '{difficulty}'")
                return self._get_fallback_question(difficulty, question_pool)
            
            # Si on a des informations sur la performance, sélectionner intelligemment
            if student_performance and len(available_questions) > 1:
                selected_question = self._select_based_on_performance(
                    available_questions, student_performance
                )
            else:
                # Sélection aléatoire simple
                selected_question = random.choice(available_questions)
            
            # Enregistrer la question dans l'historique
            self._record_question_asked(test_id, selected_question)
            
            return selected_question
            
        except Exception as e:
            print(f"❌ Erreur lors de la sélection de question: {e}")
            return self._get_fallback_question(difficulty, question_pool)
    
    def _select_based_on_performance(
        self, 
        questions: List[Dict[str, Any]], 
        performance: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Sélectionne une question basée sur la performance de l'étudiant"""
        
        # Prioriser les questions par topic si l'étudiant a des faiblesses
        weak_topics = performance.get("weak_topics", [])
        
        if weak_topics:
            # Chercher des questions sur les sujets faibles
            weak_topic_questions = [
                q for q in questions 
                if any(topic.lower() in q.get("topic", "").lower() for topic in weak_topics)
            ]
            
            if weak_topic_questions:
                return random.choice(weak_topic_questions)
        
        # Sinon, sélection aléatoire
        return random.choice(questions)
    
    def _record_question_asked(self, test_id: int, question: Dict[str, Any]):
        """Enregistre une question posée dans l'historique"""
        try:
            question_history = QuestionHistory(
                test_id=test_id,
                question_id=question["id"],
                question_text=question["question"],
                difficulty=question["difficulty"],
                topic=question.get("topic", ""),
                asked_at=datetime.utcnow()
            )
            
            self.db.add(question_history)
            self.db.commit()
            
        except Exception as e:
            print(f"❌ Erreur lors de l'enregistrement de l'historique: {e}")
            self.db.rollback()
    
    def _clean_question_history(self, test_id: int, difficulty: str):
        """Nettoie l'historique des questions pour une difficulté donnée"""
        try:
            self.db.query(QuestionHistory).filter(
                QuestionHistory.test_id == test_id,
                QuestionHistory.difficulty == difficulty
            ).delete()
            
            self.db.commit()
            print(f"🧹 Historique nettoyé pour le test {test_id}, difficulté {difficulty}")
            
        except Exception as e:
            print(f"❌ Erreur lors du nettoyage de l'historique: {e}")
            self.db.rollback()
    
    def _get_fallback_question(self, difficulty: str, question_pool: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Récupère une question de fallback"""
        fallback_questions = [q for q in question_pool if q["difficulty"] == difficulty]
        
        if fallback_questions:
            return random.choice(fallback_questions)
        else:
            # Dernier recours : première question disponible
            return question_pool[0] if question_pool else {}
    
    def get_question_statistics(self, test_id: int) -> Dict[str, Any]:
        """Récupère les statistiques des questions posées dans un test"""
        try:
            questions = self.db.query(QuestionHistory).filter(
                QuestionHistory.test_id == test_id
            ).all()
            
            stats = {
                "total_questions": len(questions),
                "by_difficulty": {},
                "by_topic": {},
                "repetition_rate": 0.0
            }
            
            # Compter par difficulté
            for q in questions:
                diff = q.difficulty
                stats["by_difficulty"][diff] = stats["by_difficulty"].get(diff, 0) + 1
            
            # Compter par topic
            for q in questions:
                topic = q.topic or "Sans topic"
                stats["by_topic"][topic] = stats["by_topic"].get(topic, 0) + 1
            
            # Calculer le taux de répétition
            unique_questions = len(set(q.question_id for q in questions))
            if questions:
                stats["repetition_rate"] = (len(questions) - unique_questions) / len(questions)
            
            return stats
            
        except Exception as e:
            print(f"❌ Erreur lors du calcul des statistiques: {e}")
            return {}











