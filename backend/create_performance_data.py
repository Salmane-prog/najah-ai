#!/usr/bin/env python3
"""
Script pour créer des données de performance réalistes
"""

import sqlite3
import os
from datetime import datetime, timedelta
import random

def create_performance_data():
    """Créer des données de performance pour les étudiants"""
    
    db_path = "F:/IMT/stage/Yancode/Najah__AI/data/app.db"
    
    if not os.path.exists(db_path):
        print(f"❌ Base de données non trouvée: {db_path}")
        return
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("🎯 Création des données de performance...")
        
        # Récupérer les étudiants
        cursor.execute("SELECT id, username FROM users WHERE role = 'student'")
        students = cursor.fetchall()
        
        # Récupérer les quiz
        cursor.execute("SELECT id, title, subject FROM quizzes WHERE is_active = 1")
        quizzes = cursor.fetchall()
        
        if not students:
            print("❌ Aucun étudiant trouvé")
            return
            
        if not quizzes:
            print("❌ Aucun quiz trouvé")
            return
        
        print(f"👥 {len(students)} étudiants trouvés")
        print(f"📝 {len(quizzes)} quiz trouvés")
        
        # Créer des résultats de quiz pour chaque étudiant
        for student_id, student_name in students:
            print(f"📊 Création des données pour {student_name}...")
            
            # Créer 3-5 résultats de quiz par étudiant
            num_quizzes = random.randint(3, 5)
            selected_quizzes = random.sample(quizzes, min(num_quizzes, len(quizzes)))
            
            for quiz_id, quiz_title, subject in selected_quizzes:
                # Score réaliste (40-95%)
                score = random.randint(40, 95)
                max_score = 100
                percentage = score
                
                # Date aléatoire dans les 30 derniers jours
                days_ago = random.randint(0, 30)
                completed_at = datetime.now() - timedelta(days=days_ago)
                
                # Insérer le résultat
                cursor.execute("""
                    INSERT INTO quiz_results 
                    (student_id, quiz_id, score, max_score, percentage, is_completed, 
                     completed_at, sujet, user_id, created_at, time_spent, answers)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    student_id, quiz_id, score, max_score, percentage, True,
                    completed_at.strftime('%Y-%m-%d %H:%M:%S'), subject, student_id,
                    datetime.now().strftime('%Y-%m-%d %H:%M:%S'), random.randint(10, 45),
                    '{"answers": []}'
                ))
        
        # Créer des données d'activité dans learning_history
        print("📈 Création des données d'activité...")
        
        for student_id, student_name in students:
            # Créer des activités d'apprentissage
            for i in range(random.randint(5, 15)):
                days_ago = random.randint(0, 30)
                activity_date = datetime.now() - timedelta(days=days_ago)
                
                activities = [
                    "Quiz complété",
                    "Contenu consulté", 
                    "Parcours avancé",
                    "Badge obtenu",
                    "Défi relevé"
                ]
                
                activity = random.choice(activities)
                
                cursor.execute("""
                    INSERT INTO learning_history 
                    (student_id, content_id, learning_path_id, progress, time_spent, 
                     completed, started_at, action, score, progression, details, timestamp)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    student_id, random.randint(1, 5), random.randint(1, 3),
                    random.uniform(0.1, 1.0), random.randint(10, 45), True,
                    activity_date.strftime('%Y-%m-%d %H:%M:%S'), activity,
                    random.randint(60, 95), random.uniform(0.1, 1.0),
                    '{"duration": 15, "score": 85}',
                    activity_date.strftime('%Y-%m-%d %H:%M:%S')
                ))
        
        # Créer des données de progression
        print("📊 Création des données de progression...")
        
        for student_id, student_name in students:
            # Progression dans un parcours
            progress = random.randint(20, 80)
            current_step = random.randint(1, 5)
            
            cursor.execute("""
                INSERT INTO student_progress 
                (student_id, learning_path_id, current_step_id, completed_steps, progress_percentage, 
                 started_at, last_activity, is_active)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                student_id, 1, current_step, '[]', progress,
                datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                datetime.now().strftime('%Y-%m-%d %H:%M:%S'), True
            ))
        
        # Valider les changements
        conn.commit()
        print("✅ Données de performance créées avec succès !")
        
        # Afficher un résumé
        cursor.execute("SELECT COUNT(*) FROM quiz_results")
        quiz_results_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM learning_history")
        activities_count = cursor.fetchone()[0]
        
        print(f"📊 Résumé créé:")
        print(f"   - {quiz_results_count} résultats de quiz")
        print(f"   - {activities_count} activités utilisateur")
        print(f"   - Progression pour {len(students)} étudiants")
        
    except Exception as e:
        print(f"❌ Erreur lors de la création: {str(e)}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    create_performance_data() 