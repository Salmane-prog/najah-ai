#!/usr/bin/env python3
"""
Script pour créer des données de calendrier et de devoirs pour tester les widgets
"""

import os
import sys
from datetime import datetime, timedelta
import random

# Ajouter le répertoire parent au path pour importer les modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import SessionLocal, engine
from models.calendar import CalendarEvent
from models.homework import Homework
from models.user import User
from models.quiz import Quiz
from models.quiz_result import QuizResult
from models.quiz_question import QuizQuestion
from models.quiz_answer import QuizAnswer

def create_calendar_data():
    """Créer des événements de calendrier"""
    db = SessionLocal()
    
    try:
        # Récupérer un étudiant existant
        student = db.query(User).filter(User.role == "student").first()
        if not student:
            print("Aucun étudiant trouvé. Créez d'abord un étudiant.")
            return
        
        # Créer des événements de calendrier
        events_data = [
            {
                "title": "Quiz de Mathématiques",
                "type": "quiz",
                "start_time": datetime.now() + timedelta(days=2, hours=10),
                "end_time": datetime.now() + timedelta(days=2, hours=11),
                "description": "Quiz sur les équations du second degré",
                "subject": "Mathématiques",
                "location": "Salle 101",
                "priority": "high",
                "user_id": student.id
            },
            {
                "title": "Devoir de Français",
                "type": "homework",
                "start_time": datetime.now() + timedelta(days=3),
                "description": "Rédaction sur le thème de la liberté",
                "subject": "Français",
                "priority": "medium",
                "user_id": student.id
            },
            {
                "title": "Examen de Sciences",
                "type": "exam",
                "start_time": datetime.now() + timedelta(days=7, hours=14),
                "end_time": datetime.now() + timedelta(days=7, hours=16),
                "description": "Examen sur la biologie cellulaire",
                "subject": "Sciences",
                "location": "Amphithéâtre A",
                "priority": "high",
                "user_id": student.id
            },
            {
                "title": "Cours d'Histoire",
                "type": "course",
                "start_time": datetime.now() + timedelta(days=1, hours=9),
                "end_time": datetime.now() + timedelta(days=1, hours=10),
                "description": "Cours sur la Révolution française",
                "subject": "Histoire",
                "location": "Salle 203",
                "priority": "low",
                "user_id": student.id
            },
            {
                "title": "Rappel: Rendu de projet",
                "type": "reminder",
                "start_time": datetime.now() + timedelta(days=5),
                "description": "N'oubliez pas de rendre votre projet d'informatique",
                "subject": "Informatique",
                "priority": "high",
                "user_id": student.id
            }
        ]
        
        for event_data in events_data:
            event = CalendarEvent(**event_data)
            db.add(event)
        
        db.commit()
        print(f"✅ {len(events_data)} événements de calendrier créés")
        
    except Exception as e:
        print(f"❌ Erreur lors de la création des événements: {e}")
        db.rollback()
    finally:
        db.close()

def create_homework_data():
    """Créer des devoirs assignés"""
    db = SessionLocal()
    
    try:
        # Récupérer un étudiant existant
        student = db.query(User).filter(User.role == "student").first()
        if not student:
            print("Aucun étudiant trouvé. Créez d'abord un étudiant.")
            return
        
        # Créer des devoirs
        homework_data = [
            {
                "title": "Analyse d'un poème",
                "subject": "Français",
                "description": "Analyser le poème 'Le Lac' de Lamartine en 3 pages",
                "assigned_at": datetime.now() - timedelta(days=5),
                "due_date": datetime.now() + timedelta(days=3),
                "priority": "high",
                "status": "pending",
                "estimated_time": 120,
                "instructions": "Inclure une introduction, un développement et une conclusion. Analyser les figures de style et le thème principal.",
                "submission_type": "file",
                "user_id": student.id
            },
            {
                "title": "Exercices de mathématiques",
                "subject": "Mathématiques",
                "description": "Résoudre les exercices 1 à 15 du chapitre 3",
                "assigned_at": datetime.now() - timedelta(days=3),
                "due_date": datetime.now() + timedelta(days=1),
                "priority": "medium",
                "status": "in_progress",
                "estimated_time": 90,
                "instructions": "Montrer tous les calculs. Vérifier vos réponses.",
                "submission_type": "file",
                "user_id": student.id
            },
            {
                "title": "Rapport de laboratoire",
                "subject": "Sciences",
                "description": "Rédiger un rapport sur l'expérience de chimie",
                "assigned_at": datetime.now() - timedelta(days=7),
                "due_date": datetime.now() + timedelta(days=5),
                "priority": "medium",
                "status": "pending",
                "estimated_time": 180,
                "instructions": "Inclure la méthode, les résultats et la discussion. Maximum 5 pages.",
                "submission_type": "file",
                "user_id": student.id
            },
            {
                "title": "Présentation PowerPoint",
                "subject": "Histoire",
                "description": "Créer une présentation sur la Première Guerre mondiale",
                "assigned_at": datetime.now() - timedelta(days=2),
                "due_date": datetime.now() + timedelta(days=4),
                "priority": "low",
                "status": "pending",
                "estimated_time": 60,
                "instructions": "Maximum 10 diapositives. Inclure des images et des dates importantes.",
                "submission_type": "file",
                "user_id": student.id
            }
        ]
        
        for hw_data in homework_data:
            homework = Homework(**hw_data)
            db.add(homework)
        
        db.commit()
        print(f"✅ {len(homework_data)} devoirs créés")
        
    except Exception as e:
        print(f"❌ Erreur lors de la création des devoirs: {e}")
        db.rollback()
    finally:
        db.close()

def create_quiz_data():
    """Créer des quiz assignés et des résultats"""
    db = SessionLocal()
    
    try:
        # Récupérer un étudiant existant
        student = db.query(User).filter(User.role == "student").first()
        if not student:
            print("Aucun étudiant trouvé. Créez d'abord un étudiant.")
            return
        
        # Créer des quiz
        quiz_data = [
            {
                "title": "Quiz de Mathématiques - Équations",
                "subject": "Mathématiques",
                "level": "Intermédiaire",
                "description": "Quiz sur la résolution d'équations du premier et second degré",
                "estimated_time": 30,
                "questions_count": 10,
                "difficulty": "moyen",
                "created_by": 1,  # ID d'un professeur
                "is_active": True
            },
            {
                "title": "Quiz de Français - Grammaire",
                "subject": "Français",
                "level": "Débutant",
                "description": "Quiz sur les règles de grammaire de base",
                "estimated_time": 20,
                "questions_count": 8,
                "difficulty": "facile",
                "created_by": 1,
                "is_active": True
            },
            {
                "title": "Quiz de Sciences - Biologie",
                "subject": "Sciences",
                "level": "Avancé",
                "description": "Quiz sur la biologie cellulaire et la génétique",
                "estimated_time": 45,
                "questions_count": 15,
                "difficulty": "difficile",
                "created_by": 1,
                "is_active": True
            }
        ]
        
        created_quizzes = []
        for quiz_data in quiz_data:
            quiz = Quiz(**quiz_data)
            db.add(quiz)
            db.flush()  # Pour obtenir l'ID
            created_quizzes.append(quiz)
        
        # Créer des résultats de quiz
        for i, quiz in enumerate(created_quizzes):
            # Quiz complété
            if i < 2:
                quiz_result = QuizResult(
                    user_id=student.id,
                    quiz_id=quiz.id,
                    score=random.randint(7, 10),
                    max_score=10,
                    percentage=random.randint(70, 100),
                    completed=True,
                    created_at=datetime.now() - timedelta(days=random.randint(1, 5))
                )
                db.add(quiz_result)
                db.flush()
                
                # Créer des questions et réponses pour le quiz complété
                for j in range(quiz.questions_count):
                    question = QuizQuestion(
                        quiz_id=quiz.id,
                        question_text=f"Question {j+1} du quiz {quiz.title}",
                        question_type="multiple_choice",
                        correct_answer=f"Réponse correcte {j+1}",
                        options=f"Option A, Option B, Option C, Option D",
                        points=1
                    )
                    db.add(question)
                    db.flush()
                    
                    # Réponse de l'étudiant
                    student_answer = QuizAnswer(
                        quiz_result_id=quiz_result.id,
                        question_id=question.id,
                        student_answer=f"Réponse de l'étudiant {j+1}",
                        is_correct=random.choice([True, False]),
                        points_earned=1 if random.choice([True, False]) else 0
                    )
                    db.add(student_answer)
        
        db.commit()
        print(f"✅ {len(created_quizzes)} quiz créés avec résultats")
        
    except Exception as e:
        print(f"❌ Erreur lors de la création des quiz: {e}")
        db.rollback()
    finally:
        db.close()

def main():
    """Fonction principale"""
    print("🚀 Création des données de test pour les widgets...")
    
    print("\n📅 Création des événements de calendrier...")
    create_calendar_data()
    
    print("\n📚 Création des devoirs...")
    create_homework_data()
    
    print("\n🧪 Création des quiz et résultats...")
    create_quiz_data()
    
    print("\n✅ Toutes les données de test ont été créées avec succès!")
    print("🎯 Vous pouvez maintenant tester les nouveaux widgets dans le dashboard étudiant.")

if __name__ == "__main__":
    main()

