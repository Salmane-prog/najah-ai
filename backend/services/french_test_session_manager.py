#!/usr/bin/env python3
"""
Service de gestion des sessions de test français
Gère le cycle complet de l'évaluation : démarrage, progression, finalisation
"""

from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from sqlalchemy import text
import json
from datetime import datetime
import random

from .french_question_selector import FrenchQuestionSelector

class FrenchTestSessionManager:
    """Gestionnaire de sessions de test français"""
    
    def __init__(self, db: Session):
        self.db = db
        self.question_selector = FrenchQuestionSelector(db)
    
    def start_test_session(self, student_id: int) -> Dict[str, Any]:
        """
        Démarrer une nouvelle session de test français
        Retourne la première question et les informations de progression
        """
        print(f"🚀 Démarrage d'une nouvelle session de test français pour l'étudiant {student_id}")
        
        try:
            # Vérifier si l'étudiant a déjà un test en cours
            existing_test = self._get_existing_test(student_id)
            if existing_test:
                print(f"ℹ️ Test existant trouvé pour l'étudiant {student_id}")
                return self._resume_existing_test(existing_test)
            
            # Créer une nouvelle session de test
            test_id = self._create_test_session(student_id)
            
            # Sélectionner les 20 questions
            questions = self.question_selector.select_questions_for_assessment(student_id)
            
            # Sauvegarder la séquence de questions
            self._save_questions_sequence(test_id, questions)
            
            # Retourner la première question
            first_question = self.question_selector.get_question_by_order(questions, 1)
            
            if not first_question:
                raise Exception("Impossible de récupérer la première question")
            
            # Formater la réponse pour l'API
            response = {
                "success": True,
                "test_id": test_id,
                "status": "in_progress",
                "current_question": first_question,
                "progress": {
                    "current": 1,
                    "total": 20,
                    "difficulty": first_question["difficulty"],
                    "level_progression": "A1",
                    "current_level": "A1"
                },
                "questions_sequence": [q["id"] for q in questions],
                "current_question_id": first_question["id"]
            }
            
            print(f"✅ Nouvelle session de test créée avec succès (ID: {test_id})")
            return response
            
        except Exception as e:
            print(f"❌ Erreur lors du démarrage de la session: {e}")
            raise
    
    def submit_answer(self, test_id: int, student_id: int, answer: str) -> Dict[str, Any]:
        """
        Soumettre une réponse et passer à la question suivante
        Arrêt automatique après 20 questions
        """
        print(f"📝 Soumission de réponse pour le test {test_id}, étudiant {student_id}")
        
        try:
            # Récupérer les informations du test
            test_info = self._get_test_info(test_id, student_id)
            if not test_info:
                raise Exception("Test non trouvé")
            
            # Vérifier que le test est en cours
            if test_info["status"] != "in_progress":
                raise Exception("Le test n'est pas en cours")
            
            # Récupérer la question actuelle
            current_question_index = test_info["current_question_index"]
            questions_sequence = json.loads(test_info["questions_sequence"])
            
            # Récupérer la question actuelle
            current_question = self._get_question_by_id(questions_sequence[current_question_index - 1])
            if not current_question:
                raise Exception("Question actuelle non trouvée")
            
            # Vérifier la réponse
            is_correct = answer == current_question["correct"]
            score = 10 if is_correct else 0
            
            # Sauvegarder la réponse
            self._save_answer(test_id, student_id, current_question["id"], answer, is_correct, score)
            
            # Passer à la question suivante
            next_question_index = current_question_index + 1
            
            # Vérifier si c'est la dernière question (20ème)
            if current_question_index >= 20:
                # Test terminé - c'est la 20ème question
                print(f"🎯 Question 20 terminée, finalisation du test {test_id}")
                return self._complete_test(test_id, student_id)
            else:
                # Question suivante
                return self._get_next_question(test_id, student_id, next_question_index, questions_sequence)
                
        except Exception as e:
            print(f"❌ Erreur lors de la soumission de la réponse: {e}")
            raise
    
    def _get_existing_test(self, student_id: int) -> Optional[Dict[str, Any]]:
        """Récupérer un test existant pour l'étudiant"""
        try:
            result = self.db.execute(text("""
                SELECT id, status, current_question_index, questions_sequence, started_at
                FROM french_adaptive_tests
                WHERE student_id = :student_id AND status IN ('in_progress', 'paused')
                ORDER BY started_at DESC
                LIMIT 1
            """), {"student_id": student_id})
            
            row = result.fetchone()
            if row:
                return {
                    "id": row[0],
                    "status": row[1],
                    "current_question_index": row[2],
                    "questions_sequence": row[3],
                    "started_at": row[4]
                }
            return None
            
        except Exception as e:
            print(f"⚠️ Erreur lors de la récupération du test existant: {e}")
            return None
    
    def _resume_existing_test(self, test_info: Dict[str, Any]) -> Dict[str, Any]:
        """Reprendre un test existant"""
        print(f"🔄 Reprise du test existant {test_info['id']}")
        
        try:
            questions_sequence = json.loads(test_info["questions_sequence"])
            current_question_index = test_info["current_question_index"]
            
            # Récupérer la question actuelle
            current_question_id = questions_sequence[current_question_index - 1]
            current_question = self._get_question_by_id(current_question_id)
            
            if not current_question:
                raise Exception("Question actuelle non trouvée")
            
            return {
                "success": True,
                "test_id": test_info["id"],
                "status": "in_progress",
                "current_question": current_question,
                "progress": {
                    "current": current_question_index,
                    "total": 20,
                    "difficulty": current_question["difficulty"],
                    "level_progression": "A1",
                    "current_level": "A1"
                },
                "questions_sequence": questions_sequence,
                "current_question_id": current_question["id"]
            }
            
        except Exception as e:
            print(f"❌ Erreur lors de la reprise du test: {e}")
            raise
    
    def _create_test_session(self, student_id: int) -> int:
        """Créer une nouvelle session de test"""
        try:
            # Créer la table si elle n'existe pas
            self._ensure_tables_exist()
            
            # Insérer la nouvelle session
            result = self.db.execute(text("""
                INSERT INTO french_adaptive_tests 
                (student_id, test_type, current_question_index, total_questions, 
                 current_difficulty, status, started_at, level_progression, current_level)
                VALUES (:student_id, 'initial', 1, 20, 'easy', 'in_progress', 
                        :started_at, 'A1', 'A1')
            """), {
                "student_id": student_id,
                "started_at": datetime.utcnow().isoformat()
            })
            
            test_id = result.lastrowid
            self.db.commit()
            
            print(f"✅ Session de test créée avec l'ID {test_id}")
            return test_id
            
        except Exception as e:
            print(f"❌ Erreur lors de la création de la session: {e}")
            self.db.rollback()
            raise
    
    def _save_questions_sequence(self, test_id: int, questions: List[Dict[str, Any]]):
        """Sauvegarder la séquence de questions pour le test"""
        try:
            questions_sequence = [q["id"] for q in questions]
            
            result = self.db.execute(text("""
                UPDATE french_adaptive_tests 
                SET questions_sequence = :questions_sequence
                WHERE id = :test_id
            """), {
                "questions_sequence": json.dumps(questions_sequence),
                "test_id": test_id
            })
            
            self.db.commit()
            print(f"✅ Séquence de {len(questions_sequence)} questions sauvegardée")
            
        except Exception as e:
            print(f"❌ Erreur lors de la sauvegarde de la séquence: {e}")
            self.db.rollback()
            raise
    
    def _get_test_info(self, test_id: int, student_id: int) -> Optional[Dict[str, Any]]:
        """Récupérer les informations d'un test"""
        try:
            result = self.db.execute(text("""
                SELECT id, status, current_question_index, questions_sequence
                FROM french_adaptive_tests
                WHERE id = :test_id AND student_id = :student_id
            """), {
                "test_id": test_id,
                "student_id": student_id
            })
            
            row = result.fetchone()
            if row:
                            return {
                "id": row[0],
                "status": row[1],
                "current_question_index": row[2],
                "questions_sequence": row[3]
            }
            return None
            
        except Exception as e:
            print(f"⚠️ Erreur lors de la récupération des infos du test: {e}")
            return None
    
    def _get_question_by_id(self, question_id: int) -> Optional[Dict[str, Any]]:
        """Récupérer une question par son ID depuis la banque de questions"""
        all_questions = []
        for difficulty in self.question_selector.question_pool:
            all_questions.extend(self.question_selector.question_pool[difficulty])
        
        for question in all_questions:
            if question["id"] == question_id:
                return question
        
        return None
    
    def _save_answer(self, test_id: int, student_id: int, question_id: int, 
                    answer: str, is_correct: bool, score: int):
        """Sauvegarder la réponse de l'étudiant"""
        try:
            # Créer la table si elle n'existe pas
            self._ensure_answer_table_exists()
            
            # Insérer la réponse
            result = self.db.execute(text("""
                INSERT INTO french_test_answers
                (test_id, student_id, question_id, answer, is_correct, score, answered_at)
                VALUES (:test_id, :student_id, :question_id, :answer, :is_correct, :score, :answered_at)
            """), {
                "test_id": test_id,
                "student_id": student_id,
                "question_id": question_id,
                "answer": answer,
                "is_correct": is_correct,
                "score": score,
                "answered_at": datetime.utcnow().isoformat()
            })
            
            self.db.commit()
            print(f"✅ Réponse sauvegardée pour la question {question_id}")
            
        except Exception as e:
            print(f"❌ Erreur lors de la sauvegarde de la réponse: {e}")
            self.db.rollback()
            raise
    
    def _get_next_question(self, test_id: int, student_id: int, 
                          next_question_index: int, questions_sequence: List[int]) -> Dict[str, Any]:
        """Récupérer la question suivante"""
        try:
            # Mettre à jour l'index de la question actuelle
            result = self.db.execute(text("""
                UPDATE french_adaptive_tests 
                SET current_question_index = :question_index
                WHERE id = :test_id
            """), {
                "question_index": next_question_index,
                "test_id": test_id
            })
            
            self.db.commit()
            
            # Récupérer la question suivante
            next_question_id = questions_sequence[next_question_index - 1]
            next_question = self._get_question_by_id(next_question_id)
            
            if not next_question:
                raise Exception("Question suivante non trouvée")
            
            return {
                "success": True,
                "test_id": test_id,
                "status": "in_progress",
                "next_question": next_question,
                "progress": {
                    "current": next_question_index,
                    "total": 20,
                    "difficulty": next_question["difficulty"],
                    "level_progression": "A1",
                    "current_level": "A1"
                },
                "questions_sequence": questions_sequence,
                "current_question_id": next_question["id"]
            }
            
        except Exception as e:
            print(f"❌ Erreur lors de la récupération de la question suivante: {e}")
            raise
    
    def _complete_test(self, test_id: int, student_id: int) -> Dict[str, Any]:
        """Finaliser le test et générer le profil"""
        print(f"🎉 Finalisation du test {test_id} pour l'étudiant {student_id}")
        
        try:
            # Calculer le score final
            final_score = self._calculate_final_score(test_id)
            
            # Mettre à jour le statut du test
            result = self.db.execute(text("""
                UPDATE french_adaptive_tests 
                SET status = 'completed', completed_at = :completed_at, final_score = :final_score
                WHERE id = :test_id
            """), {
                "completed_at": datetime.utcnow().isoformat(),
                "final_score": final_score,
                "test_id": test_id
            })
            
            self.db.commit()
            
            # Générer le profil d'apprentissage
            profile = self._generate_learning_profile(student_id, final_score)
            
            return {
                "success": True,
                "test_id": test_id,
                "status": "completed",
                "final_score": final_score,
                "profile": profile,
                "message": "Test terminé avec succès ! Votre profil d'apprentissage a été généré."
            }
            
        except Exception as e:
            print(f"❌ Erreur lors de la finalisation du test: {e}")
            raise
    
    def _calculate_final_score(self, test_id: int) -> float:
        """Calculer le score final du test"""
        try:
            result = self.db.execute(text("""
                SELECT SUM(score) as total_score, COUNT(*) as total_questions
                FROM french_test_answers
                WHERE test_id = :test_id
            """), {"test_id": test_id})
            
            row = result.fetchone()
            if row and row[0] is not None:
                total_score = row[0]
                total_questions = row[1]
                return round((total_score / (total_questions * 10)) * 100, 2)
            
            return 0.0
            
        except Exception as e:
            print(f"⚠️ Erreur lors du calcul du score final: {e}")
            return 0.0
    
    def _generate_learning_profile(self, student_id: int, final_score: float) -> Dict[str, Any]:
        """Générer le profil d'apprentissage de l'étudiant"""
        try:
            # Déterminer le niveau français
            if final_score >= 80:
                french_level = "Avancé (B2-C1)"
                learning_style = "Autonome"
                preferred_pace = "Rapide"
            elif final_score >= 60:
                french_level = "Intermédiaire (B1)"
                learning_style = "Structured"
                preferred_pace = "Modéré"
            else:
                french_level = "Débutant (A1-A2)"
                learning_style = "Guidé"
                preferred_pace = "Lent"
            
            # Créer ou mettre à jour le profil
            self._ensure_profile_table_exists()
            
            result = self.db.execute(text("""
                INSERT OR REPLACE INTO french_learning_profiles
                (student_id, french_level, learning_style, preferred_pace, 
                 strengths, weaknesses, cognitive_profile, created_at, updated_at)
                VALUES (:student_id, :french_level, :learning_style, :preferred_pace,
                        :strengths, :weaknesses, :cognitive_profile, :created_at, :updated_at)
            """), {
                "student_id": student_id,
                "french_level": french_level,
                "learning_style": learning_style,
                "preferred_pace": preferred_pace,
                "strengths": json.dumps(["Grammaire de base", "Vocabulaire essentiel"]),
                "weaknesses": json.dumps(["Conjugaisons complexes", "Expressions idiomatiques"]),
                "cognitive_profile": json.dumps({"score": final_score, "level": french_level}),
                "created_at": datetime.utcnow().isoformat(),
                "updated_at": datetime.utcnow().isoformat()
            })
            
            self.db.commit()
            
            return {
                "french_level": french_level,
                "learning_style": learning_style,
                "preferred_pace": preferred_pace,
                "final_score": final_score,
                "strengths": ["Grammaire de base", "Vocabulaire essentiel"],
                "weaknesses": ["Conjugaisons complexes", "Expressions idiomatiques"]
            }
            
        except Exception as e:
            print(f"⚠️ Erreur lors de la génération du profil: {e}")
            return {
                "french_level": "Non déterminé",
                "learning_style": "Standard",
                "preferred_pace": "Modéré",
                "final_score": final_score,
                "strengths": [],
                "weaknesses": []
            }
    
    def _ensure_tables_exist(self):
        """S'assurer que les tables nécessaires existent"""
        try:
            # Table des tests français
            self.db.execute(text("""
                CREATE TABLE IF NOT EXISTS french_adaptive_tests (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    student_id INTEGER NOT NULL,
                    test_type VARCHAR NOT NULL,
                    current_question_index INTEGER DEFAULT 1,
                    total_questions INTEGER,
                    current_difficulty VARCHAR NOT NULL,
                    status VARCHAR DEFAULT 'in_progress',
                    started_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    completed_at DATETIME,
                    final_score FLOAT,
                    difficulty_progression TEXT,
                    level_progression VARCHAR DEFAULT 'A1',
                    current_level VARCHAR DEFAULT 'A1',
                    questions_sequence TEXT
                )
            """))
            
            self.db.commit()
            print("✅ Tables des tests français créées/vérifiées")
            
        except Exception as e:
            print(f"⚠️ Erreur lors de la création des tables: {e}")
    
    def _ensure_answer_table_exists(self):
        """S'assurer que la table des réponses existe"""
        try:
            self.db.execute(text("""
                CREATE TABLE IF NOT EXISTS french_test_answers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    test_id INTEGER NOT NULL,
                    student_id INTEGER NOT NULL,
                    question_id INTEGER NOT NULL,
                    answer TEXT NOT NULL,
                    is_correct BOOLEAN NOT NULL,
                    score INTEGER NOT NULL,
                    answered_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """))
            
            self.db.commit()
            
        except Exception as e:
            print(f"⚠️ Erreur lors de la création de la table des réponses: {e}")
    
    def _ensure_profile_table_exists(self):
        """S'assurer que la table des profils existe"""
        try:
            self.db.execute(text("""
                CREATE TABLE IF NOT EXISTS french_learning_profiles (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    student_id INTEGER NOT NULL UNIQUE,
                    french_level VARCHAR,
                    learning_style VARCHAR,
                    preferred_pace VARCHAR,
                    strengths TEXT,
                    weaknesses TEXT,
                    cognitive_profile TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """))
            
            self.db.commit()
            
        except Exception as e:
            print(f"⚠️ Erreur lors de la création de la table des profils: {e}")
