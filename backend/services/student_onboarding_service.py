#!/usr/bin/env python3
"""
Service d'onboarding automatique des étudiants
Lance automatiquement l'évaluation initiale à la première connexion
"""

from typing import Dict, Any, Optional
from sqlalchemy.orm import Session
from sqlalchemy import text
from datetime import datetime
import json

class StudentOnboardingService:
    """Service d'onboarding automatique des étudiants"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def check_and_initialize_student(self, student_id: int) -> Dict[str, Any]:
        """
        Vérifier si l'étudiant a besoin d'être initialisé
        Retourne les informations d'onboarding
        """
        print(f"🎓 Vérification de l'onboarding pour l'étudiant {student_id}")
        
        try:
            # Vérifier si l'étudiant a déjà un profil d'apprentissage
            has_profile = self._check_learning_profile(student_id)
            
            # Vérifier si l'étudiant a déjà passé une évaluation
            has_assessment = self._check_assessment_status(student_id)
            
            # Déterminer le statut d'onboarding
            if not has_profile and not has_assessment:
                status = "needs_initial_evaluation"
                message = "Évaluation initiale requise pour commencer votre apprentissage"
                action_required = "start_french_assessment"
            elif has_profile and not has_assessment:
                status = "profile_exists_no_assessment"
                message = "Votre profil existe mais l'évaluation initiale n'est pas terminée"
                action_required = "complete_french_assessment"
            elif has_profile and has_assessment:
                status = "fully_onboarded"
                message = "Vous êtes entièrement configuré pour l'apprentissage"
                action_required = "none"
            else:
                status = "partial_onboarding"
                message = "Configuration partielle détectée"
                action_required = "verify_status"
            
            onboarding_info = {
                "student_id": student_id,
                "status": status,
                "message": message,
                "action_required": action_required,
                "has_learning_profile": has_profile,
                "has_completed_assessment": has_assessment,
                "onboarding_date": datetime.utcnow().isoformat()
            }
            
            print(f"✅ Statut d'onboarding: {status}")
            return onboarding_info
            
        except Exception as e:
            print(f"❌ Erreur lors de la vérification de l'onboarding: {e}")
            return {
                "student_id": student_id,
                "status": "error",
                "message": f"Erreur lors de la vérification: {str(e)}",
                "action_required": "contact_support",
                "has_learning_profile": False,
                "has_completed_assessment": False,
                "onboarding_date": datetime.utcnow().isoformat()
            }
    
    def auto_start_initial_assessment(self, student_id: int) -> Dict[str, Any]:
        """
        Démarrer automatiquement l'évaluation initiale pour un étudiant
        """
        print(f"🚀 Démarrage automatique de l'évaluation initiale pour l'étudiant {student_id}")
        
        try:
            # Vérifier que l'étudiant n'a pas déjà une évaluation en cours
            existing_assessment = self._get_existing_assessment(student_id)
            
            if existing_assessment:
                if existing_assessment["status"] == "completed":
                    return {
                        "success": False,
                        "message": "L'évaluation initiale est déjà terminée",
                        "assessment_id": existing_assessment["id"],
                        "status": "already_completed"
                    }
                elif existing_assessment["status"] == "in_progress":
                    return {
                        "success": True,
                        "message": "Évaluation déjà en cours",
                        "assessment_id": existing_assessment["id"],
                        "status": "resume_existing"
                    }
            
            # Créer une nouvelle évaluation initiale
            assessment_id = self._create_initial_assessment(student_id)
            
            # Créer les questions d'évaluation
            questions_created = self._create_assessment_questions(assessment_id)
            
            if questions_created:
                return {
                    "success": True,
                    "message": "Évaluation initiale créée avec succès",
                    "assessment_id": assessment_id,
                    "status": "new_assessment_created",
                    "questions_count": 20
                }
            else:
                return {
                    "success": False,
                    "message": "Erreur lors de la création des questions",
                    "assessment_id": assessment_id,
                    "status": "error"
                }
                
        except Exception as e:
            print(f"❌ Erreur lors du démarrage automatique: {e}")
            return {
                "success": False,
                "message": f"Erreur lors du démarrage: {str(e)}",
                "status": "error"
            }
    
    def _check_learning_profile(self, student_id: int) -> bool:
        """Vérifier si l'étudiant a un profil d'apprentissage"""
        try:
            # Vérifier dans french_learning_profiles
            result = self.db.execute(text("""
                SELECT COUNT(*) FROM french_learning_profiles 
                WHERE student_id = :student_id
            """), {"student_id": student_id})
            
            count = result.fetchone()[0]
            return count > 0
            
        except Exception as e:
            print(f"⚠️ Erreur lors de la vérification du profil: {e}")
            return False
    
    def _check_assessment_status(self, student_id: int) -> bool:
        """Vérifier si l'étudiant a terminé une évaluation"""
        try:
            # Vérifier dans french_adaptive_tests
            result = self.db.execute(text("""
                SELECT COUNT(*) FROM french_adaptive_tests 
                WHERE student_id = :student_id AND status = 'completed'
            """), {"student_id": student_id})
            
            count = result.fetchone()[0]
            return count > 0
            
        except Exception as e:
            print(f"⚠️ Erreur lors de la vérification de l'évaluation: {e}")
            return False
    
    def _get_existing_assessment(self, student_id: int) -> Optional[Dict[str, Any]]:
        """Récupérer une évaluation existante pour l'étudiant"""
        try:
            result = self.db.execute(text("""
                SELECT id, status, started_at, completed_at
                FROM french_adaptive_tests 
                WHERE student_id = :student_id 
                ORDER BY started_at DESC 
                LIMIT 1
            """), {"student_id": student_id})
            
            row = result.fetchone()
            if row:
                return {
                    "id": row[0],
                    "status": row[1],
                    "started_at": row[2],
                    "completed_at": row[3]
                }
            return None
            
        except Exception as e:
            print(f"⚠️ Erreur lors de la récupération de l'évaluation: {e}")
            return None
    
    def _create_initial_assessment(self, student_id: int) -> int:
        """Créer une nouvelle évaluation initiale"""
        try:
            # Créer la table si elle n'existe pas
            self._ensure_assessment_table_exists()
            
            # Insérer la nouvelle évaluation
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
            
            assessment_id = result.lastrowid
            self.db.commit()
            
            print(f"✅ Évaluation initiale créée avec l'ID {assessment_id}")
            return assessment_id
            
        except Exception as e:
            print(f"❌ Erreur lors de la création de l'évaluation: {e}")
            self.db.rollback()
            raise
    
    def _create_assessment_questions(self, assessment_id: int) -> bool:
        """Créer les questions pour l'évaluation"""
        try:
            # Questions d'évaluation initiale (20 questions)
            questions_data = [
                # Questions faciles (7)
                {
                    "question_text": "Quel est l'article correct ? '___ chat'",
                    "question_type": "multiple_choice",
                    "subject": "Français",
                    "difficulty": "easy",
                    "options": json.dumps(["Le", "La", "Les", "L'"]),
                    "correct_answer": "Le",
                    "points": 1.0,
                    "order": 1
                },
                {
                    "question_text": "Conjuguez le verbe 'être' à la 1ère personne du singulier au présent",
                    "question_type": "multiple_choice",
                    "subject": "Français",
                    "difficulty": "easy",
                    "options": json.dumps(["Je suis", "Je es", "Je être", "Je suis être"]),
                    "correct_answer": "Je suis",
                    "points": 1.0,
                    "order": 2
                },
                {
                    "question_text": "Quel est le genre du mot 'maison' ?",
                    "question_type": "multiple_choice",
                    "subject": "Français",
                    "difficulty": "easy",
                    "options": json.dumps(["Masculin", "Féminin", "Neutre", "Variable"]),
                    "correct_answer": "Féminin",
                    "points": 1.0,
                    "order": 3
                },
                {
                    "question_text": "Quel est le pluriel de 'cheval' ?",
                    "question_type": "multiple_choice",
                    "subject": "Français",
                    "difficulty": "easy",
                    "options": json.dumps(["Chevals", "Chevaux", "Chevales", "Cheval"]),
                    "correct_answer": "Chevaux",
                    "points": 1.0,
                    "order": 4
                },
                {
                    "question_text": "Quel est l'antonyme de 'grand' ?",
                    "question_type": "multiple_choice",
                    "subject": "Français",
                    "difficulty": "easy",
                    "options": json.dumps(["Petit", "Gros", "Long", "Large"]),
                    "correct_answer": "Petit",
                    "points": 1.0,
                    "order": 5
                },
                {
                    "question_text": "Complétez : 'Je ___ un étudiant'",
                    "question_type": "multiple_choice",
                    "subject": "Français",
                    "difficulty": "easy",
                    "options": json.dumps(["suis", "es", "est", "sont"]),
                    "correct_answer": "suis",
                    "points": 1.0,
                    "order": 6
                },
                {
                    "question_text": "Quel est le féminin de 'professeur' ?",
                    "question_type": "multiple_choice",
                    "subject": "Français",
                    "difficulty": "easy",
                    "options": json.dumps(["Professeur", "Professeure", "Professeuse", "Professeure"]),
                    "correct_answer": "Professeure",
                    "points": 1.0,
                    "order": 7
                },
                # Questions moyennes (6)
                {
                    "question_text": "Complétez : 'Les enfants ___ dans le jardin.'",
                    "question_type": "multiple_choice",
                    "subject": "Français",
                    "difficulty": "medium",
                    "options": json.dumps(["joue", "jouent", "joues", "jouer"]),
                    "correct_answer": "jouent",
                    "points": 1.0,
                    "order": 8
                },
                {
                    "question_text": "Quel temps verbal dans 'J'ai mangé' ?",
                    "question_type": "multiple_choice",
                    "subject": "Français",
                    "difficulty": "medium",
                    "options": json.dumps(["Présent", "Imparfait", "Passé composé", "Futur"]),
                    "correct_answer": "Passé composé",
                    "points": 1.0,
                    "order": 9
                },
                {
                    "question_text": "Quel est le féminin de 'acteur' ?",
                    "question_type": "multiple_choice",
                    "subject": "Français",
                    "difficulty": "medium",
                    "options": json.dumps(["Acteur", "Actrice", "Acteuse", "Acteure"]),
                    "correct_answer": "Actrice",
                    "points": 1.0,
                    "order": 10
                },
                {
                    "question_text": "Combien de syllabes dans 'ordinateur' ?",
                    "question_type": "multiple_choice",
                    "subject": "Français",
                    "difficulty": "medium",
                    "options": json.dumps(["3", "4", "5", "6"]),
                    "correct_answer": "4",
                    "points": 1.0,
                    "order": 11
                },
                {
                    "question_text": "Quel est le sens de 'rapidement' ?",
                    "question_type": "multiple_choice",
                    "subject": "Français",
                    "difficulty": "medium",
                    "options": json.dumps(["Lentement", "Vite", "Doucement", "Fortement"]),
                    "correct_answer": "Vite",
                    "points": 1.0,
                    "order": 12
                },
                {
                    "question_text": "Identifiez la fonction de 'très' dans 'Il est très intelligent'",
                    "question_type": "multiple_choice",
                    "subject": "Français",
                    "difficulty": "medium",
                    "options": json.dumps(["Adjectif", "Adverbe", "Nom", "Verbe"]),
                    "correct_answer": "Adverbe",
                    "points": 1.0,
                    "order": 13
                },
                # Questions difficiles (7)
                {
                    "question_text": "Quel est le mode du verbe dans 'Veuillez patienter' ?",
                    "question_type": "multiple_choice",
                    "subject": "Français",
                    "difficulty": "hard",
                    "options": json.dumps(["Indicatif", "Subjonctif", "Impératif", "Conditionnel"]),
                    "correct_answer": "Impératif",
                    "points": 1.0,
                    "order": 14
                },
                {
                    "question_text": "Quel est le type de phrase 'Quelle belle journée !' ?",
                    "question_type": "multiple_choice",
                    "subject": "Français",
                    "difficulty": "hard",
                    "options": json.dumps(["Déclarative", "Interrogative", "Exclamative", "Impérative"]),
                    "correct_answer": "Exclamative",
                    "points": 1.0,
                    "order": 15
                },
                {
                    "question_text": "Quel est le registre de langue de 'bagnole' ?",
                    "question_type": "multiple_choice",
                    "subject": "Français",
                    "difficulty": "hard",
                    "options": json.dumps(["Soutenu", "Courant", "Familier", "Argotique"]),
                    "correct_answer": "Familier",
                    "points": 1.0,
                    "order": 16
                },
                {
                    "question_text": "Quel est le sens figuré de 'avoir le cafard' ?",
                    "question_type": "multiple_choice",
                    "subject": "Français",
                    "difficulty": "hard",
                    "options": json.dumps(["Être malade", "Être triste", "Être fatigué", "Être en colère"]),
                    "correct_answer": "Être triste",
                    "points": 1.0,
                    "order": 17
                },
                {
                    "question_text": "Quel est le type de complément dans 'Il mange une pomme' ?",
                    "question_type": "multiple_choice",
                    "subject": "Français",
                    "difficulty": "hard",
                    "options": json.dumps(["Complément d'objet direct", "Complément d'objet indirect", "Complément circonstanciel", "Attribut"]),
                    "correct_answer": "Complément d'objet direct",
                    "points": 1.0,
                    "order": 18
                },
                {
                    "question_text": "Quel est le degré de l'adjectif dans 'C'est le plus beau jour' ?",
                    "question_type": "multiple_choice",
                    "subject": "Français",
                    "difficulty": "hard",
                    "options": json.dumps(["Positif", "Comparatif", "Superlatif", "Absolu"]),
                    "correct_answer": "Superlatif",
                    "points": 1.0,
                    "order": 19
                },
                {
                    "question_text": "Quel est le type de proposition dans 'Je pense qu'il viendra' ?",
                    "question_type": "multiple_choice",
                    "subject": "Français",
                    "difficulty": "hard",
                    "options": json.dumps(["Principale", "Subordonnée relative", "Subordonnée complétive", "Subordonnée circonstancielle"]),
                    "correct_answer": "Subordonnée complétive",
                    "points": 1.0,
                    "order": 20
                }
            ]
            
            # Créer la table des questions si elle n'existe pas
            self._ensure_questions_table_exists()
            
            # Insérer toutes les questions
            for question_data in questions_data:
                self.db.execute(text("""
                    INSERT INTO assessment_questions 
                    (assessment_id, question_text, question_type, subject, difficulty, 
                     options, correct_answer, points, order_index)
                    VALUES (:assessment_id, :question_text, :question_type, :subject, :difficulty,
                            :options, :correct_answer, :points, :order_index)
                """), {
                    "assessment_id": assessment_id,
                    **question_data
                })
            
            self.db.commit()
            print(f"✅ {len(questions_data)} questions créées pour l'évaluation {assessment_id}")
            return True
            
        except Exception as e:
            print(f"❌ Erreur lors de la création des questions: {e}")
            self.db.rollback()
            return False
    
    def _ensure_assessment_table_exists(self):
        """S'assurer que la table des évaluations existe"""
        try:
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
                    questions_sequence TEXT,
                    current_question_order INTEGER DEFAULT 1
                )
            """))
            
            self.db.commit()
            
        except Exception as e:
            print(f"⚠️ Erreur lors de la création de la table des évaluations: {e}")
    
    def _ensure_questions_table_exists(self):
        """S'assurer que la table des questions existe"""
        try:
            self.db.execute(text("""
                CREATE TABLE IF NOT EXISTS assessment_questions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    assessment_id INTEGER NOT NULL,
                    question_text TEXT NOT NULL,
                    question_type VARCHAR NOT NULL,
                    subject VARCHAR NOT NULL,
                    difficulty VARCHAR NOT NULL,
                    options TEXT,
                    correct_answer VARCHAR NOT NULL,
                    points FLOAT DEFAULT 1.0,
                    order_index INTEGER DEFAULT 0
                )
            """))
            
            self.db.commit()
            
        except Exception as e:
            print(f"⚠️ Erreur lors de la création de la table des questions: {e}")
    
    def get_student_onboarding_status(self, student_id: int) -> Dict[str, Any]:
        """
        Obtenir le statut complet d'onboarding d'un étudiant
        """
        try:
            onboarding_info = self.check_and_initialize_student(student_id)
            
            # Ajouter des informations supplémentaires
            if onboarding_info["status"] == "needs_initial_evaluation":
                # Démarrer automatiquement l'évaluation
                assessment_result = self.auto_start_initial_assessment(student_id)
                onboarding_info["assessment_result"] = assessment_result
                
                if assessment_result["success"]:
                    onboarding_info["next_step"] = "start_french_assessment"
                    onboarding_info["assessment_ready"] = True
                else:
                    onboarding_info["next_step"] = "contact_support"
                    onboarding_info["assessment_ready"] = False
            
            return onboarding_info
            
        except Exception as e:
            print(f"❌ Erreur lors de la récupération du statut d'onboarding: {e}")
            return {
                "student_id": student_id,
                "status": "error",
                "message": f"Erreur lors de la récupération du statut: {str(e)}",
                "next_step": "contact_support"
            }





