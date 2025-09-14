#!/usr/bin/env python3
"""
Moteur d'évaluation avec questions adaptatives
"""

from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from datetime import datetime
import random

from models.assessment import Assessment
from models.assessment_question import AssessmentQuestion
from models.assessment_result import AssessmentResult

class AssessmentEngine:
    """Moteur d'évaluation intelligent avec questions adaptatives"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create_initial_assessment(self, student_id: int, subject: str = "Général") -> Assessment:
        """Créer une évaluation initiale pour un étudiant"""
        
        # Créer l'évaluation
        assessment = Assessment(
            student_id=student_id,
            assessment_type="initial_evaluation",
            title=f"Évaluation Initiale - {subject}",
            description="Évaluation pour déterminer votre niveau et vos besoins d'apprentissage",
            subject=subject,
            priority="high",
            estimated_time=45,
            status="pending",
            created_by=student_id,
            created_at=datetime.utcnow()
        )
        
        self.db.add(assessment)
        self.db.commit()
        self.db.refresh(assessment)
        
        # Créer les questions de base (5 questions fixes)
        base_questions = self._generate_base_questions(subject)
        for i, question_data in enumerate(base_questions):
            question = AssessmentQuestion(
                assessment_id=assessment.id,
                question_text=question_data["question_text"],
                question_type="multiple_choice",
                subject=subject,
                difficulty="easy",
                options=question_data["options"],
                correct_answer=question_data["correct_answer"],
                points=1.0,
                order=i + 1
            )
            self.db.add(question)
        
        self.db.commit()
        return assessment
    
    def _generate_base_questions(self, subject: str) -> List[Dict[str, Any]]:
        """Générer les questions de base par matière"""
        
        if subject == "Mathématiques":
            return [
                {
                    "question_text": "Quel est le résultat de 7 + 5 ?",
                    "options": "A) 10, B) 11, C) 12, D) 13",
                    "correct_answer": "C) 12"
                },
                {
                    "question_text": "Combien font 3 × 4 ?",
                    "options": "A) 7, B) 10, C) 12, D) 15",
                    "correct_answer": "C) 12"
                },
                {
                    "question_text": "Quelle est la moitié de 18 ?",
                    "options": "A) 7, B) 8, C) 9, D) 10",
                    "correct_answer": "C) 9"
                },
                {
                    "question_text": "Quel nombre vient après 25 ?",
                    "options": "A) 24, B) 25, C) 26, D) 27",
                    "correct_answer": "C) 26"
                },
                {
                    "question_text": "Combien de côtés a un carré ?",
                    "options": "A) 3, B) 4, C) 5, D) 6",
                    "correct_answer": "B) 4"
                }
            ]
        elif subject == "Français":
            return [
                {
                    "question_text": "Quel est le pluriel de 'chat' ?",
                    "options": "A) chat, B) chats, C) chate, D) chates",
                    "correct_answer": "B) chats"
                },
                {
                    "question_text": "Conjuguez 'être' à la 1ère personne du singulier au présent",
                    "options": "A) suis, B) es, C) est, D) sommes",
                    "correct_answer": "A) suis"
                },
                {
                    "question_text": "Quel est le genre du mot 'maison' ?",
                    "options": "A) masculin, B) féminin, C) neutre",
                    "correct_answer": "B) féminin"
                },
                {
                    "question_text": "Quel est l'antonyme de 'grand' ?",
                    "options": "A) petit, B) gros, C) long, D) large",
                    "correct_answer": "A) petit"
                },
                {
                    "question_text": "Combien de syllabes dans 'ordinateur' ?",
                    "options": "A) 3, B) 4, C) 5, D) 6",
                    "correct_answer": "B) 4"
                }
            ]
        else:  # Général
            return [
                {
                    "question_text": "Quel est votre niveau en mathématiques ?",
                    "options": "A) Débutant, B) Intermédiaire, C) Avancé",
                    "correct_answer": "A) Débutant"
                },
                {
                    "question_text": "Connaissez-vous les bases de la grammaire française ?",
                    "options": "A) Oui, B) Non, C) Un peu",
                    "correct_answer": "C) Un peu"
                },
                {
                    "question_text": "Avez-vous des connaissances en sciences ?",
                    "options": "A) Aucune, B) Basiques, C) Bonnes",
                    "correct_answer": "B) Basiques"
                },
                {
                    "question_text": "Quel est votre objectif principal d'apprentissage ?",
                    "options": "A) Révision, B) Progression, C) Perfectionnement",
                    "correct_answer": "B) Progression"
                },
                {
                    "question_text": "Combien de temps pouvez-vous consacrer à l'apprentissage par jour ?",
                    "options": "A) 15 minutes, B) 30 minutes, C) 1 heure, D) Plus",
                    "correct_answer": "B) 30 minutes"
                }
            ]
    
    def generate_adaptive_questions(self, assessment_id: int, student_answers: List[Dict]) -> List[AssessmentQuestion]:
        """Générer des questions adaptatives basées sur les réponses"""
        
        # Analyser les réponses pour déterminer le niveau
        correct_answers = sum(1 for answer in student_answers if answer["is_correct"])
        total_questions = len(student_answers)
        success_rate = correct_answers / total_questions if total_questions > 0 else 0
        
        # Déterminer le niveau et la difficulté des questions adaptatives
        if success_rate >= 0.8:
            difficulty = "advanced"
            question_count = 3
        elif success_rate >= 0.6:
            difficulty = "intermediate"
            question_count = 4
        else:
            difficulty = "easy"
            question_count = 5
        
        # Récupérer la matière de l'évaluation
        assessment = self.db.query(Assessment).filter(Assessment.id == assessment_id).first()
        subject = assessment.subject if assessment else "Général"
        
        # Générer les questions adaptatives
        adaptive_questions = self._generate_adaptive_questions(subject, difficulty, question_count)
        
        # Ajouter les questions à la base de données
        questions = []
        existing_count = self.db.query(AssessmentQuestion).filter(
            AssessmentQuestion.assessment_id == assessment_id
        ).count()
        
        for i, question_data in enumerate(adaptive_questions):
            question = AssessmentQuestion(
                assessment_id=assessment_id,
                question_text=question_data["question_text"],
                question_type="multiple_choice",
                subject=subject,
                difficulty=difficulty,
                options=question_data["options"],
                correct_answer=question_data["correct_answer"],
                points=1.5,  # Questions adaptatives valent plus de points
                order=existing_count + i + 1
            )
            self.db.add(question)
            questions.append(question)
        
        self.db.commit()
        return questions
    
    def _generate_adaptive_questions(self, subject: str, difficulty: str, count: int) -> List[Dict[str, Any]]:
        """Générer des questions adaptatives selon la difficulté"""
        
        if subject == "Mathématiques":
            if difficulty == "easy":
                return [
                    {
                        "question_text": "Quel est le résultat de 15 - 8 ?",
                        "options": "A) 5, B) 6, C) 7, D) 8",
                        "correct_answer": "C) 7"
                    },
                    {
                        "question_text": "Combien font 6 ÷ 2 ?",
                        "options": "A) 2, B) 3, C) 4, D) 6",
                        "correct_answer": "B) 3"
                    },
                    {
                        "question_text": "Quel est le double de 9 ?",
                        "options": "A) 16, B) 17, C) 18, D) 19",
                        "correct_answer": "C) 18"
                    }
                ]
            elif difficulty == "intermediate":
                return [
                    {
                        "question_text": "Quel est le résultat de 12 × 11 ?",
                        "options": "A) 120, B) 132, C) 144, D) 156",
                        "correct_answer": "B) 132"
                    },
                    {
                        "question_text": "Quelle est la racine carrée de 64 ?",
                        "options": "A) 6, B) 7, C) 8, D) 9",
                        "correct_answer": "C) 8"
                    },
                    {
                        "question_text": "Quel est le périmètre d'un carré de côté 5 ?",
                        "options": "A) 15, B) 20, C) 25, D) 30",
                        "correct_answer": "B) 20"
                    },
                    {
                        "question_text": "Quel est le résultat de 3² + 4² ?",
                        "options": "A) 7, B) 12, C) 25, D) 49",
                        "correct_answer": "C) 25"
                    }
                ]
            else:  # advanced
                return [
                    {
                        "question_text": "Quel est le résultat de 15% de 200 ?",
                        "options": "A) 20, B) 25, C) 30, D) 35",
                        "correct_answer": "C) 30"
                    },
                    {
                        "question_text": "Quelle est l'aire d'un cercle de rayon 3 ? (π ≈ 3.14)",
                        "options": "A) 18.84, B) 28.26, C) 37.68, D) 56.52",
                        "correct_answer": "B) 28.26"
                    },
                    {
                        "question_text": "Quel est le résultat de 2³ × 3² ?",
                        "options": "A) 36, B) 54, C) 72, D) 108",
                        "correct_answer": "C) 72"
                    }
                ]
        else:  # Général ou autres matières
            return [
                {
                    "question_text": "Quel est votre rythme d'apprentissage préféré ?",
                    "options": "A) Rapide, B) Modéré, C) Lent",
                    "correct_answer": "B) Modéré"
                },
                {
                    "question_text": "Préférez-vous apprendre seul ou en groupe ?",
                    "options": "A) Seul, B) En groupe, C) Les deux",
                    "correct_answer": "C) Les deux"
                },
                {
                    "question_text": "Quel type de contenu vous motive le plus ?",
                    "options": "A) Vidéos, B) Textes, C) Exercices pratiques, D) Quiz",
                    "correct_answer": "C) Exercices pratiques"
                }
            ]
    
    def analyze_results(self, assessment_id: int, student_answers: List[Dict]) -> Dict[str, Any]:
        """Analyser les résultats et générer des recommandations"""
        
        # Calculer le score
        total_score = 0
        max_score = 0
        subject_scores = {}
        difficulty_scores = {}
        
        for answer in student_answers:
            question = self.db.query(AssessmentQuestion).filter(
                AssessmentQuestion.id == answer["question_id"]
            ).first()
            
            if question:
                max_score += question.points
                if answer["is_correct"]:
                    total_score += question.points
                
                # Analyser par matière
                subject = question.subject
                if subject not in subject_scores:
                    subject_scores[subject] = {"correct": 0, "total": 0}
                subject_scores[subject]["total"] += 1
                if answer["is_correct"]:
                    subject_scores[subject]["correct"] += 1
                
                # Analyser par difficulté
                difficulty = question.difficulty
                if difficulty not in difficulty_scores:
                    difficulty_scores[difficulty] = {"correct": 0, "total": 0}
                difficulty_scores[difficulty]["total"] += 1
                if answer["is_correct"]:
                    difficulty_scores[difficulty]["correct"] += 1
        
        percentage = (total_score / max_score * 100) if max_score > 0 else 0
        
        # Déterminer le niveau global
        if percentage >= 80:
            level = "Avancé"
        elif percentage >= 60:
            level = "Intermédiaire"
        else:
            level = "Débutant"
        
        # Générer des recommandations
        recommendations = self._generate_recommendations(percentage, subject_scores, difficulty_scores)
        
        return {
            "total_score": total_score,
            "max_score": max_score,
            "percentage": percentage,
            "level": level,
            "subject_scores": subject_scores,
            "difficulty_scores": difficulty_scores,
            "recommendations": recommendations
        }
    
    def _generate_recommendations(self, percentage: float, subject_scores: Dict, difficulty_scores: Dict) -> List[str]:
        """Générer des recommandations personnalisées"""
        
        recommendations = []
        
        # Recommandations basées sur le score global
        if percentage >= 80:
            recommendations.append("Excellent travail ! Vous pouvez passer à des défis plus avancés.")
            recommendations.append("Considérez des parcours d'apprentissage de niveau supérieur.")
        elif percentage >= 60:
            recommendations.append("Bon travail ! Continuez à renforcer vos bases.")
            recommendations.append("Pratiquez régulièrement pour améliorer vos compétences.")
        else:
            recommendations.append("Pas de panique ! Commençons par les fondamentaux.")
            recommendations.append("Nous allons créer un parcours personnalisé pour vous.")
        
        # Recommandations par matière
        for subject, scores in subject_scores.items():
            subject_percentage = (scores["correct"] / scores["total"] * 100) if scores["total"] > 0 else 0
            if subject_percentage < 60:
                recommendations.append(f"Concentrez-vous sur {subject} pour améliorer vos compétences.")
            elif subject_percentage >= 80:
                recommendations.append(f"Excellente maîtrise de {subject} !")
        
        # Recommandations par difficulté
        for difficulty, scores in difficulty_scores.items():
            difficulty_percentage = (scores["correct"] / scores["total"] * 100) if scores["total"] > 0 else 0
            if difficulty == "easy" and difficulty_percentage < 70:
                recommendations.append("Revenez aux bases pour consolider vos connaissances.")
            elif difficulty == "intermediate" and difficulty_percentage >= 80:
                recommendations.append("Vous êtes prêt pour des défis plus complexes !")
        
        return recommendations[:5]  # Limiter à 5 recommandations
