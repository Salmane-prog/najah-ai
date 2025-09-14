#!/usr/bin/env python3
"""
Script simplifié pour générer des données de performance des élèves
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

def generate_simple_performance_data():
    """Génère des données de performance simples pour les élèves existants."""
    db = SessionLocal()
    
    try:
        print("🎯 Génération des données de performance des élèves...")
        
        # Récupérer tous les élèves
        students = db.query(User).filter(User.role == "student").all()
        if not students:
            print("❌ Aucun élève trouvé.")
            return
        
        # Récupérer tous les quiz
        quizzes = db.query(Quiz).all()
        if not quizzes:
            print("❌ Aucun quiz trouvé.")
            return
        
        # Récupérer tous les badges
        badges = db.query(Badge).all()
        
        print(f"📊 Génération des performances pour {len(students)} élèves...")
        
        # Générer des performances pour chaque élève
        for student in students:
            print(f"  👤 Traitement de {student.username or student.email}...")
            
            # Générer 2-5 résultats de quiz par élève
            num_quizzes = random.randint(2, 5)
            selected_quizzes = random.sample(quizzes, min(num_quizzes, len(quizzes)))
            
            for quiz in selected_quizzes:
                # Générer un score aléatoire
                score = random.randint(30, 95)
                
                # Date aléatoire dans les 30 derniers jours
                days_ago = random.randint(0, 30)
                completed_date = datetime.utcnow() - timedelta(days=days_ago)
                started_date = completed_date - timedelta(minutes=random.randint(10, 45))
                
                # Créer le résultat de quiz avec la structure existante
                quiz_result = QuizResult(
                    user_id=student.id,  # Utiliser user_id au lieu de student_id
                    sujet=quiz.subject,  # Utiliser sujet au lieu de quiz_id
                    score=score,
                    completed=1,  # Utiliser completed au lieu de is_completed
                    # Les nouvelles colonnes seront NULL par défaut
                    quiz_id=quiz.id,
                    student_id=student.id,
                    max_score=100,
                    percentage=score,
                    started_at=started_date,
                    completed_at=completed_date,
                    is_completed=True
                )
                db.add(quiz_result)
            
            # Attribuer 1-2 badges aléatoires à chaque élève
            if badges:
                num_badges = random.randint(1, min(2, len(badges)))
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
        
    except Exception as e:
        print(f"❌ Erreur lors de la génération des données: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    generate_simple_performance_data() 