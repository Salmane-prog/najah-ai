#!/usr/bin/env python3
"""
Script pour générer des données de test pour les résultats de quiz
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.database import SessionLocal
from sqlalchemy import text
from datetime import datetime, timedelta
import random

def generate_test_results():
    """Génère des résultats de test pour les quiz existants."""
    db = SessionLocal()
    
    try:
        print("🎯 Génération de données de test pour les résultats de quiz...")
        
        # Récupérer tous les quiz
        result = db.execute(text("SELECT id, title, subject, total_points FROM quizzes"))
        quizzes = result.fetchall()
        if not quizzes:
            print("❌ Aucun quiz trouvé dans la base de données")
            return
        
        print(f"📚 {len(quizzes)} quiz trouvés")
        
        # Récupérer tous les étudiants
        result = db.execute(text("SELECT id, username, email FROM users WHERE role = 'student'"))
        students = result.fetchall()
        if not students:
            print("❌ Aucun étudiant trouvé dans la base de données")
            return
        
        print(f"👥 {len(students)} étudiants trouvés")
        
        # Générer des résultats pour chaque quiz
        results_created = 0
        
        for quiz in quizzes:
            print(f"  📝 Traitement du quiz '{quiz.title}' (ID: {quiz.id})")
            
            # Choisir aléatoirement 1-3 étudiants pour ce quiz
            num_students = random.randint(1, min(3, len(students)))
            selected_students = random.sample(students, num_students)
            
            for student in selected_students:
                # Générer un score aléatoire (plus réaliste)
                if random.random() < 0.7:  # 70% de chance d'avoir un bon score
                    score = random.randint(60, 95)
                else:
                    score = random.randint(30, 70)
                
                # Date aléatoire dans les 7 derniers jours
                days_ago = random.randint(0, 7)
                completed_date = datetime.utcnow() - timedelta(days=days_ago)
                started_date = completed_date - timedelta(minutes=random.randint(10, 45))
                
                # Créer le résultat de quiz
                db.execute(text("""
                    INSERT INTO quiz_results 
                    (user_id, student_id, quiz_id, sujet, score, max_score, percentage, 
                     completed, is_completed, started_at, completed_at, created_at)
                    VALUES (:user_id, :student_id, :quiz_id, :sujet, :score, :max_score, :percentage,
                           :completed, :is_completed, :started_at, :completed_at, :created_at)
                """), {
                    'user_id': student.id,
                    'student_id': student.id,
                    'quiz_id': quiz.id,
                    'sujet': quiz.subject,
                    'score': score,
                    'max_score': quiz.total_points or 100,
                    'percentage': score,
                    'completed': 1,
                    'is_completed': True,
                    'started_at': started_date,
                    'completed_at': completed_date,
                    'created_at': completed_date
                })
                
                results_created += 1
                print(f"    ✅ Résultat créé pour {student.username or student.email}: {score}%")
        
        # Sauvegarder tous les changements
        db.commit()
        print(f"\n🎉 {results_created} résultats de quiz créés avec succès!")
        
        # Afficher un résumé
        print("\n📊 Résumé des données créées:")
        for quiz in quizzes:
            result = db.execute(text("""
                SELECT COUNT(*) as count, AVG(percentage) as avg_score 
                FROM quiz_results 
                WHERE quiz_id = :quiz_id
            """), {'quiz_id': quiz.id})
            stats = result.fetchone()
            if stats.count > 0:
                print(f"  📝 {quiz.title}: {stats.count} étudiants, moyenne {stats.avg_score:.1f}%")
        
    except Exception as e:
        print(f"❌ Erreur lors de la génération: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    generate_test_results() 