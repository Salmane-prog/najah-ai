#!/usr/bin/env python3
"""
Script pour générer des données de performance avec SQL direct
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.database import SessionLocal
from sqlalchemy import text
from datetime import datetime, timedelta
import random

def generate_performance_with_sql():
    """Génère des données de performance en utilisant SQL direct."""
    db = SessionLocal()
    
    try:
        print("🎯 Génération des données de performance avec SQL...")
        
        # Récupérer les élèves
        result = db.execute(text("SELECT id, username, email FROM users WHERE role = 'student'"))
        students = result.fetchall()
        
        if not students:
            print("❌ Aucun élève trouvé.")
            return
        
        # Récupérer les quiz
        result = db.execute(text("SELECT id, title, subject FROM quizzes"))
        quizzes = result.fetchall()
        
        if not quizzes:
            print("❌ Aucun quiz trouvé.")
            return
        
        # Récupérer les badges
        result = db.execute(text("SELECT id, name FROM badges"))
        badges = result.fetchall()
        
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
                
                # Insérer le résultat de quiz
                db.execute(text("""
                    INSERT INTO quiz_results 
                    (user_id, sujet, score, completed, quiz_id, student_id, max_score, percentage, started_at, completed_at, is_completed, created_at)
                    VALUES (:user_id, :sujet, :score, :completed, :quiz_id, :student_id, :max_score, :percentage, :started_at, :completed_at, :is_completed, :created_at)
                """), {
                    'user_id': student.id,
                    'sujet': quiz.subject,
                    'score': score,
                    'completed': 1,
                    'quiz_id': quiz.id,
                    'student_id': student.id,
                    'max_score': 100,
                    'percentage': score,
                    'started_at': started_date,
                    'completed_at': completed_date,
                    'is_completed': True,
                    'created_at': datetime.utcnow()
                })
            
            # Attribuer 1-2 badges aléatoires à chaque élève
            if badges:
                num_badges = random.randint(1, min(2, len(badges)))
                selected_badges = random.sample(badges, num_badges)
                
                for badge in selected_badges:
                    # Vérifier si l'élève n'a pas déjà ce badge
                    result = db.execute(text("""
                        SELECT id FROM user_badge 
                        WHERE user_id = :user_id AND badge_id = :badge_id
                    """), {
                        'user_id': student.id,
                        'badge_id': badge.id
                    })
                    
                    if not result.fetchone():
                        awarded_date = datetime.utcnow() - timedelta(days=random.randint(0, 60))
                        db.execute(text("""
                            INSERT INTO user_badge (user_id, badge_id, awarded_at)
                            VALUES (:user_id, :badge_id, :awarded_at)
                        """), {
                            'user_id': student.id,
                            'badge_id': badge.id,
                            'awarded_at': awarded_date
                        })
        
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
    generate_performance_with_sql() 