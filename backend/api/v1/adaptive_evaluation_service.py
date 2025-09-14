from typing import List, Dict, Optional, Tuple
import math
import random
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import text
import json

class AdaptiveEvaluationService:
    """
    Service pour la gestion des évaluations adaptatives en temps réel
    Utilise l'algorithme IRT (Item Response Theory) pour l'adaptation
    """
    
    def __init__(self, db: Session):
        self.db = db
    
    def create_adaptive_evaluation(
        self,
        teacher_id: int,
        title: str,
        subject: str,
        description: str,
        evaluation_type: str,
        difficulty_range: Tuple[int, int],
        target_duration: int,
        student_ids: List[int]
    ) -> Dict:
        """
        Crée une nouvelle évaluation adaptative et l'assigne aux étudiants
        """
        try:
            # Créer l'évaluation
            evaluation_data = {
                'title': title,
                'subject': subject,
                'description': description,
                'evaluation_type': evaluation_type,
                'difficulty_min': difficulty_range[0],
                'difficulty_max': difficulty_range[1],
                'target_duration': target_duration,
                'created_by': teacher_id,
                'created_at': datetime.now().isoformat(),
                'status': 'active',
                'current_question': 1,
                'total_questions': 0,  # Sera calculé dynamiquement
                'adaptation_algorithm': 'irt_adaptive',
                'irt_parameters': {
                    'discrimination': 1.0,
                    'difficulty': (difficulty_range[0] + difficulty_range[1]) / 2,
                    'guessing': 0.25
                }
            }
            
            # Insérer dans la base de données
            cursor = self.db.execute(text("""
                INSERT INTO formative_evaluations (
                    title, subject, description, evaluation_type, 
                    difficulty_min, difficulty_max, target_duration,
                    created_by, created_at, status, current_question,
                    total_questions, adaptation_algorithm, irt_parameters
                ) VALUES (
                    :title, :subject, :description, :evaluation_type,
                    :difficulty_min, :difficulty_max, :target_duration,
                    :created_by, :created_at, :status, :current_question,
                    :total_questions, :adaptation_algorithm, :irt_parameters
                )
            """), evaluation_data)
            
            evaluation_id = cursor.lastrowid
            
            # Assigner aux étudiants
            self._assign_to_students(evaluation_id, teacher_id, student_ids)
            
            # Générer les questions initiales
            questions = self._generate_initial_questions(
                subject, difficulty_range, evaluation_id
            )
            
            return {
                'id': evaluation_id,
                'title': title,
                'subject': subject,
                'status': 'active',
                'assigned_students': len(student_ids),
                'questions_generated': len(questions),
                'message': f'Évaluation adaptative créée et assignée à {len(student_ids)} étudiants'
            }
            
        except Exception as e:
            raise Exception(f"Erreur lors de la création de l'évaluation: {str(e)}")
    
    def _assign_to_students(
        self, 
        evaluation_id: int, 
        teacher_id: int, 
        student_ids: List[int]
    ):
        """Assigne l'évaluation aux étudiants spécifiés"""
        due_date = datetime.now() + timedelta(days=7)
        
        for student_id in student_ids:
            self.db.execute(text("""
                INSERT INTO formative_evaluation_assignments (
                    evaluation_id, student_id, assigned_by, assigned_at,
                    due_date, status, created_at, updated_at
                ) VALUES (
                    :evaluation_id, :student_id, :assigned_by, :assigned_at,
                    :due_date, :status, :created_at, :updated_at
                )
            """), {
                'evaluation_id': evaluation_id,
                'student_id': student_id,
                'assigned_by': teacher_id,
                'assigned_at': datetime.now().isoformat(),
                'due_date': due_date.isoformat(),
                'status': 'assigned',
                'created_at': datetime.now().isoformat(),
                'updated_at': datetime.now().isoformat()
            })
        
        self.db.commit()
    
    def _generate_initial_questions(
        self, 
        subject: str, 
        difficulty_range: Tuple[int, int], 
        evaluation_id: int
    ) -> List[Dict]:
        """Génère les questions initiales basées sur la matière et la difficulté"""
        
        # Questions par matière (simulation - à remplacer par vraies questions)
        subject_questions = {
            'Mathématiques': [
                {
                    'question': 'Résoudre l\'équation: 2x + 5 = 13',
                    'options': ['x = 4', 'x = 3', 'x = 5', 'x = 6'],
                    'correct_answer': 0,
                    'difficulty': 3,
                    'explanation': '2x + 5 = 13 → 2x = 8 → x = 4'
                },
                {
                    'question': 'Calculer l\'aire d\'un cercle de rayon 5',
                    'options': ['25π', '50π', '75π', '100π'],
                    'correct_answer': 0,
                    'difficulty': 4,
                    'explanation': 'A = πr² = π × 5² = 25π'
                },
                {
                    'question': 'Factoriser: x² - 9',
                    'options': ['(x+3)(x-3)', '(x+9)(x-9)', '(x+3)(x+3)', '(x-3)(x-3)'],
                    'correct_answer': 0,
                    'difficulty': 5,
                    'explanation': 'x² - 9 = x² - 3² = (x+3)(x-3)'
                }
            ],
            'Français': [
                {
                    'question': 'Quel est le genre du mot "table" ?',
                    'options': ['Masculin', 'Féminin', 'Neutre', 'Variable'],
                    'correct_answer': 1,
                    'difficulty': 2,
                    'explanation': '"Table" est un nom féminin'
                },
                {
                    'question': 'Conjuguez le verbe "avoir" à la 1ère personne du pluriel du présent',
                    'options': ['J\'ai', 'Tu as', 'Il a', 'Nous avons'],
                    'correct_answer': 3,
                    'difficulty': 3,
                    'explanation': 'Nous avons (1ère personne du pluriel)'
                }
            ],
            'Histoire': [
                {
                    'question': 'En quelle année a eu lieu la Révolution française ?',
                    'options': ['1789', '1799', '1769', '1779'],
                    'correct_answer': 0,
                    'difficulty': 3,
                    'explanation': 'La Révolution française a commencé en 1789'
                }
            ]
        }
        
        questions = subject_questions.get(subject, [])
        
        # Insérer les questions dans la base
        for question in questions:
            self.db.execute(text("""
                INSERT INTO formative_evaluation_questions (
                    evaluation_id, question_text, options, correct_answer,
                    difficulty_level, explanation, question_order
                ) VALUES (
                    :evaluation_id, :question_text, :options, :correct_answer,
                    :difficulty_level, :explanation, :question_order
                )
            """), {
                'evaluation_id': evaluation_id,
                'question_text': question['question'],
                'options': json.dumps(question['options']),
                'correct_answer': question['correct_answer'],
                'difficulty_level': question['difficulty'],
                'explanation': question['explanation'],
                'question_order': question.get('order', 1)
            })
        
        self.db.commit()
        return questions
    
    def get_next_question(
        self, 
        evaluation_id: int, 
        student_id: int, 
        previous_answers: List[Dict]
    ) -> Optional[Dict]:
        """
        Détermine la prochaine question basée sur les réponses précédentes
        Utilise l'algorithme IRT pour l'adaptation
        """
        try:
            # Récupérer les questions disponibles
            questions = self.db.execute(text("""
                SELECT id, question_text, options, difficulty_level, explanation
                FROM formative_evaluation_questions
                WHERE evaluation_id = :evaluation_id
                ORDER BY question_order
            """), {'evaluation_id': evaluation_id}).fetchall()
            
            if not questions:
                return None
            
            # Si c'est la première question
            if not previous_answers:
                return self._format_question(questions[0])
            
            # Calculer la capacité estimée de l'étudiant (IRT)
            estimated_ability = self._calculate_irt_ability(previous_answers)
            
            # Sélectionner la prochaine question optimale
            next_question = self._select_optimal_question(
                questions, estimated_ability, previous_answers
            )
            
            return self._format_question(next_question)
            
        except Exception as e:
            raise Exception(f"Erreur lors de la récupération de la question: {str(e)}")
    
    def _calculate_irt_ability(self, previous_answers: List[Dict]) -> float:
        """Calcule la capacité estimée de l'étudiant selon la théorie IRT"""
        if not previous_answers:
            return 0.0
        
        # Algorithme simplifié d'estimation de capacité
        correct_answers = sum(1 for answer in previous_answers if answer['is_correct'])
        total_questions = len(previous_answers)
        
        # Logit transformation
        if correct_answers == 0:
            return -2.0
        elif correct_answers == total_questions:
            return 2.0
        else:
            p = correct_answers / total_questions
            return math.log(p / (1 - p))
    
    def _select_optimal_question(
        self, 
        questions: List, 
        estimated_ability: float, 
        previous_answers: List[Dict]
    ):
        """Sélectionne la question optimale basée sur la capacité estimée"""
        
        # Filtrer les questions déjà répondues
        answered_question_ids = {answer['question_id'] for answer in previous_answers}
        available_questions = [q for q in questions if q[0] not in answered_question_ids]
        
        if not available_questions:
            return None
        
        # Sélectionner la question avec la difficulté la plus proche de la capacité
        optimal_question = min(
            available_questions,
            key=lambda q: abs(q[3] - estimated_ability)
        )
        
        return optimal_question
    
    def _format_question(self, question) -> Dict:
        """Formate la question pour l'affichage"""
        return {
            'id': question[0],
            'question_text': question[1],
            'options': json.loads(question[2]),
            'difficulty_level': question[3],
            'explanation': question[4]
        }
    
    def submit_student_answer(
        self,
        evaluation_id: int,
        student_id: int,
        question_id: int,
        selected_answer: int,
        time_spent: int
    ) -> Dict:
        """Enregistre la réponse d'un étudiant et calcule l'adaptation"""
        try:
            # Récupérer la question
            question = self.db.execute(text("""
                SELECT options, correct_answer, difficulty_level
                FROM formative_evaluation_questions
                WHERE id = :question_id
            """), {'question_id': question_id}).fetchone()
            
            if not question:
                raise Exception("Question non trouvée")
            
            options = json.loads(question[0])
            correct_answer = question[1]
            difficulty = question[2]
            
            # Vérifier la réponse
            is_correct = selected_answer == correct_answer
            
            # Calculer le score IRT
            irt_score = self._calculate_irt_score(
                is_correct, difficulty, selected_answer, correct_answer
            )
            
            # Enregistrer la réponse
            self.db.execute(text("""
                INSERT INTO formative_evaluation_responses (
                    evaluation_id, student_id, question_id, selected_answer,
                    is_correct, irt_score, time_spent, submitted_at
                ) VALUES (
                    :evaluation_id, :student_id, :question_id, :selected_answer,
                    :is_correct, :irt_score, :time_spent, :submitted_at
                )
            """), {
                'evaluation_id': evaluation_id,
                'student_id': student_id,
                'question_id': question_id,
                'selected_answer': selected_answer,
                'is_correct': is_correct,
                'irt_score': irt_score,
                'time_spent': time_spent,
                'submitted_at': datetime.now().isoformat()
            })
            
            # Mettre à jour le statut de l'étudiant
            self.db.execute(text("""
                UPDATE formative_evaluation_assignments
                SET current_question = current_question + 1,
                    updated_at = :updated_at
                WHERE evaluation_id = :evaluation_id AND student_id = :student_id
            """), {
                'evaluation_id': evaluation_id,
                'student_id': student_id,
                'updated_at': datetime.now().isoformat()
            })
            
            self.db.commit()
            
            return {
                'is_correct': is_correct,
                'correct_answer': correct_answer,
                'explanation': options[correct_answer] if correct_answer < len(options) else '',
                'irt_score': irt_score,
                'feedback': self._generate_adaptive_feedback(is_correct, difficulty, irt_score)
            }
            
        except Exception as e:
            raise Exception(f"Erreur lors de la soumission de la réponse: {str(e)}")
    
    def _calculate_irt_score(
        self, 
        is_correct: bool, 
        difficulty: int, 
        selected: int, 
        correct: int
    ) -> float:
        """Calcule le score IRT pour la réponse"""
        if is_correct:
            # Score basé sur la difficulté (plus difficile = plus de points)
            base_score = 1.0 + (difficulty / 10.0)
            return min(base_score, 2.0)
        else:
            # Pénalité basée sur la distance de la bonne réponse
            distance = abs(selected - correct)
            penalty = distance * 0.2
            return max(-1.0, -penalty)
    
    def _generate_adaptive_feedback(
        self, 
        is_correct: bool, 
        difficulty: int, 
        irt_score: float
    ) -> str:
        """Génère un feedback adaptatif basé sur la performance"""
        if is_correct:
            if irt_score > 1.5:
                return "Excellent ! Vous maîtrisez parfaitement ce concept."
            elif irt_score > 1.0:
                return "Très bien ! Continuez dans cette direction."
            else:
                return "Bien ! Vous progressez dans l'apprentissage."
        else:
            if difficulty > 7:
                return "Cette question était difficile. Ne vous découragez pas !"
            elif difficulty > 4:
                return "Prenez le temps de revoir ce concept."
            else:
                return "Vérifiez votre raisonnement pour ce type de question."
    
    def get_student_progress(
        self, 
        evaluation_id: int, 
        student_id: int
    ) -> Dict:
        """Récupère le progrès détaillé d'un étudiant"""
        try:
            # Récupérer les réponses de l'étudiant
            responses = self.db.execute(text("""
                SELECT q.question_text, r.selected_answer, r.is_correct, 
                       r.irt_score, r.time_spent, r.submitted_at
                FROM formative_evaluation_responses r
                JOIN formative_evaluation_questions q ON r.question_id = q.id
                WHERE r.evaluation_id = :evaluation_id AND r.student_id = :student_id
                ORDER BY r.submitted_at
            """), {
                'evaluation_id': evaluation_id,
                'student_id': student_id
            }).fetchall()
            
            # Calculer les statistiques
            total_questions = len(responses)
            correct_answers = sum(1 for r in responses if r[2])
            average_irt_score = sum(r[3] for r in responses) / total_questions if total_questions > 0 else 0
            total_time = sum(r[4] for r in responses)
            
            # Déterminer le niveau de maîtrise
            mastery_level = self._determine_mastery_level(average_irt_score, total_questions)
            
            return {
                'total_questions': total_questions,
                'correct_answers': correct_answers,
                'accuracy': (correct_answers / total_questions * 100) if total_questions > 0 else 0,
                'average_irt_score': round(average_irt_score, 2),
                'total_time_spent': total_time,
                'mastery_level': mastery_level,
                'responses': [
                    {
                        'question': r[0],
                        'selected_answer': r[1],
                        'is_correct': r[2],
                        'irt_score': r[3],
                        'time_spent': r[4],
                        'submitted_at': r[5]
                    } for r in responses
                ]
            }
            
        except Exception as e:
            raise Exception(f"Erreur lors de la récupération du progrès: {str(e)}")
    
    def _determine_mastery_level(self, average_irt_score: float, total_questions: int) -> str:
        """Détermine le niveau de maîtrise de l'étudiant"""
        if total_questions < 3:
            return "En cours d'évaluation"
        
        if average_irt_score >= 1.5:
            return "Maîtrise excellente"
        elif average_irt_score >= 1.0:
            return "Maîtrise bonne"
        elif average_irt_score >= 0.5:
            return "Maîtrise partielle"
        elif average_irt_score >= 0.0:
            return "Maîtrise basique"
        else:
            return "Besoin de soutien"
    
    def get_evaluation_analytics(self, evaluation_id: int) -> Dict:
        """Récupère les analytics complètes d'une évaluation"""
        try:
            # Statistiques globales
            stats = self.db.execute(text("""
                SELECT 
                    COUNT(DISTINCT a.student_id) as total_students,
                    COUNT(CASE WHEN a.status = 'completed' THEN 1 END) as completed_students,
                    COUNT(CASE WHEN a.status = 'in_progress' THEN 1 END) as in_progress_students,
                    AVG(CASE WHEN r.irt_score IS NOT NULL THEN r.irt_score END) as avg_irt_score
                FROM formative_evaluation_assignments a
                LEFT JOIN formative_evaluation_responses r ON a.evaluation_id = r.evaluation_id
                WHERE a.evaluation_id = :evaluation_id
            """), {'evaluation_id': evaluation_id}).fetchone()
            
            # Performance par question
            question_performance = self.db.execute(text("""
                SELECT 
                    q.question_text,
                    q.difficulty_level,
                    COUNT(r.id) as total_responses,
                    COUNT(CASE WHEN r.is_correct THEN 1 END) as correct_responses,
                    AVG(r.irt_score) as avg_irt_score,
                    AVG(r.time_spent) as avg_time
                FROM formative_evaluation_questions q
                LEFT JOIN formative_evaluation_responses r ON q.id = r.question_id
                WHERE q.evaluation_id = :evaluation_id
                GROUP BY q.id
                ORDER BY q.question_order
            """), {'evaluation_id': evaluation_id}).fetchall()
            
            return {
                'evaluation_id': evaluation_id,
                'statistics': {
                    'total_students': stats[0] or 0,
                    'completed_students': stats[1] or 0,
                    'in_progress_students': stats[2] or 0,
                    'completion_rate': (stats[1] / stats[0] * 100) if stats[0] > 0 else 0,
                    'average_irt_score': round(stats[3] or 0, 2)
                },
                'question_analytics': [
                    {
                        'question': q[0],
                        'difficulty': q[1],
                        'total_responses': q[2],
                        'correct_responses': q[3],
                        'accuracy': (q[3] / q[2] * 100) if q[2] > 0 else 0,
                        'average_irt_score': round(q[4] or 0, 2),
                        'average_time': round(q[5] or 0, 1)
                    } for q in question_performance
                ]
            }
            
        except Exception as e:
            raise Exception(f"Erreur lors de la récupération des analytics: {str(e)}")

# Instance du service
adaptive_evaluation_service = AdaptiveEvaluationService(None)
