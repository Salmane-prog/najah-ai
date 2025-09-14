#!/usr/bin/env python3
"""
Script pour générer des données de test pour les performances des élèves
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from core.database import SessionLocal, engine
from models.quiz import Quiz, QuizResult, QuizAnswer, Question
from models.user import User
from models.badge import Badge, UserBadge
from models.message import Message
from models.thread import Thread
from datetime import datetime, timedelta
import random

def generate_performance_data():
    """Génère des données de performance pour les élèves existants."""
    db = SessionLocal()
    
    try:
        print("🎯 Génération des données de performance des élèves...")
        
        # Récupérer tous les élèves
        students = db.query(User).filter(User.role == "student").all()
        if not students:
            print("❌ Aucun élève trouvé. Créez d'abord des élèves.")
            return
        
        # Récupérer tous les quiz
        quizzes = db.query(Quiz).all()
        if not quizzes:
            print("❌ Aucun quiz trouvé. Créez d'abord des quiz.")
            return
        
        # Récupérer toutes les questions
        questions = db.query(Question).all()
        if not questions:
            print("❌ Aucune question trouvée. Créez d'abord des questions.")
            return
        
        # Récupérer tous les badges
        badges = db.query(Badge).all()
        
        print(f"📊 Génération des performances pour {len(students)} élèves...")
        
        # Générer des performances pour chaque élève
        for student in students:
            print(f"  👤 Traitement de {student.username or student.email}...")
            
            # Générer 3-8 résultats de quiz par élève
            num_quizzes = random.randint(3, 8)
            selected_quizzes = random.sample(quizzes, min(num_quizzes, len(quizzes)))
            
            for quiz in selected_quizzes:
                # Générer un score aléatoire (plus réaliste)
                if random.random() < 0.7:  # 70% de chance d'avoir un bon score
                    score = random.randint(60, 95)
                else:
                    score = random.randint(30, 70)
                
                # Calculer le nombre de questions correctes
                quiz_questions = [q for q in questions if q.quiz_id == quiz.id]
                if not quiz_questions:
                    continue
                
                correct_answers = int((score / 100) * len(quiz_questions))
                incorrect_answers = len(quiz_questions) - correct_answers
                
                # Date aléatoire dans les 30 derniers jours
                days_ago = random.randint(0, 30)
                completed_date = datetime.utcnow() - timedelta(days=days_ago)
                started_date = completed_date - timedelta(minutes=random.randint(10, 45))
                
                # Créer le résultat de quiz
                quiz_result = QuizResult(
                    student_id=student.id,
                    quiz_id=quiz.id,
                    score=correct_answers,
                    max_score=len(quiz_questions),
                    percentage=score,
                    is_completed=True,
                    started_at=started_date,
                    completed_at=completed_date
                )
                db.add(quiz_result)
                db.flush()  # Pour obtenir l'ID
                
                # Générer les réponses aux questions
                for i, question in enumerate(quiz_questions):
                    is_correct = i < correct_answers
                    
                    # Choisir une réponse aléatoire
                    if question.question_type == "multiple_choice":
                        selected_answer = random.choice(question.options) if question.options else "A"
                    else:
                        selected_answer = "Réponse générée" if is_correct else "Mauvaise réponse"
                    
                    quiz_answer = QuizAnswer(
                        result_id=quiz_result.id,
                        question_id=question.id,
                        selected_answer=selected_answer,
                        is_correct=is_correct
                    )
                    db.add(quiz_answer)
            
            # Attribuer 1-3 badges aléatoires à chaque élève
            if badges:
                num_badges = random.randint(1, min(3, len(badges)))
                selected_badges = random.sample(badges, num_badges)
                
                for badge in selected_badges:
                    # Vérifier si l'élève n'a pas déjà ce badge
                    existing_badge = db.query(UserBadge).filter(
                        UserBadge.user_id == student.id,
                        UserBadge.badge_id == badge.id
                    ).first()
                    
                    if not existing_badge:
                        user_badge = UserBadge(
                            user_id=student.id,
                            badge_id=badge.id,
                            awarded_at=datetime.utcnow() - timedelta(days=random.randint(0, 60))
                        )
                        db.add(user_badge)
        
        # Commit des changements
        db.commit()
        
        print("✅ Données de performance générées avec succès !")
        print(f"   📈 {len(students)} élèves ont maintenant des performances")
        print(f"   🎯 Quiz complétés générés")
        print(f"   🏆 Badges attribués")
        print(f"   📊 Analyses de difficultés disponibles")
        
    except Exception as e:
        print(f"❌ Erreur lors de la génération des données: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    generate_performance_data() 