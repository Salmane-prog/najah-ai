#!/usr/bin/env python3
"""
Script pour corriger les données et l'authentification
"""

import sqlite3
import os
from datetime import datetime, timedelta
import random

def fix_data_and_auth():
    """Corriger les données et l'authentification"""
    
    print("🔧 Correction des données et authentification...")
    
    # Chemin vers la base de données
    db_path = "data/app.db"
    
    if not os.path.exists(db_path):
        print(f"❌ Base de données non trouvée : {db_path}")
        return
    
    try:
        # Connexion à la base de données
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 1. Créer l'utilisateur professeur avec le bon hash
        print("👤 Création de l'utilisateur professeur...")
        cursor.execute("""
            INSERT OR REPLACE INTO users (id, username, email, hashed_password, role, is_active)
            VALUES (1, 'marie.dubois', 'marie.dubois@najah.ai', 
                   '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/8HqHh6.', 
                   'teacher', 1)
        """)
        
        # 2. Créer des étudiants
        print("👥 Création des étudiants...")
        students_data = [
            (2, 'jean.martin', 'jean.martin@najah.ai', 'student'),
            (3, 'sophie.bernard', 'sophie.bernard@najah.ai', 'student'),
            (4, 'pierre.durand', 'pierre.durand@najah.ai', 'student'),
            (5, 'marie.laurent', 'marie.laurent@najah.ai', 'student')
        ]
        
        for student_id, username, email, role in students_data:
            cursor.execute("""
                INSERT OR REPLACE INTO users (id, username, email, hashed_password, role, is_active)
                VALUES (?, ?, ?, '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/8HqHh6.', ?, 1)
            """, (student_id, username, email, role))
        
        # 3. Créer des badges
        print("🏆 Création des badges...")
        badges_data = [
            (1, 'Premier Quiz', 'A complété son premier quiz avec succès', 'quiz_completed >= 1', '/badges/first-quiz.png', 0),
            (2, 'Élève Assidu', 'A participé à 10 sessions d\'apprentissage', 'learning_sessions >= 10', '/badges/dedicated-student.png', 0),
            (3, 'Maître des Sciences', 'A obtenu 100% dans un quiz de sciences', 'science_quiz_score = 100', '/badges/science-master.png', 0),
            (4, 'Littéraire Confirmé', 'A complété 5 quiz de littérature', 'literature_quizzes >= 5', '/badges/literature-expert.png', 0)
        ]
        
        for badge_id, name, description, criteria, image_url, secret in badges_data:
            cursor.execute("""
                INSERT OR REPLACE INTO badges (id, name, description, criteria, image_url, secret)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (badge_id, name, description, criteria, image_url, secret))
        
        # 4. Attribuer des badges aux étudiants
        print("🎖️ Attribution des badges...")
        user_badges_data = [
            (2, 1, 1.0, datetime.now() - timedelta(days=5)),  # Jean - Premier Quiz
            (3, 1, 1.0, datetime.now() - timedelta(days=3)),  # Sophie - Premier Quiz
            (3, 2, 1.0, datetime.now() - timedelta(days=2)),  # Sophie - Élève Assidu
            (4, 1, 1.0, datetime.now() - timedelta(days=1)),  # Pierre - Premier Quiz
            (5, 1, 1.0, datetime.now() - timedelta(hours=12)), # Marie - Premier Quiz
            (5, 3, 1.0, datetime.now() - timedelta(hours=6))   # Marie - Maître des Sciences
        ]
        
        for user_id, badge_id, progression, awarded_at in user_badges_data:
            cursor.execute("""
                INSERT OR REPLACE INTO user_badge (user_id, badge_id, progression, awarded_at)
                VALUES (?, ?, ?, ?)
            """, (user_id, badge_id, progression, awarded_at))
        
        # 5. Créer des classes
        print("🏫 Création des classes...")
        classes_data = [
            (1, '6ème A', 'Classe de 6ème A', 1),
            (2, '6ème B', 'Classe de 6ème B', 1),
            (3, '5ème A', 'Classe de 5ème A', 1)
        ]
        
        for class_id, name, description, teacher_id in classes_data:
            cursor.execute("""
                INSERT OR REPLACE INTO class_groups (id, name, description, teacher_id)
                VALUES (?, ?, ?, ?)
            """, (class_id, name, description, teacher_id))
        
        # 6. Assigner des étudiants aux classes
        print("👥 Assignation des étudiants aux classes...")
        class_students_data = [
            (1, 2), (1, 3),  # 6ème A : Jean, Sophie
            (2, 4), (2, 5),  # 6ème B : Pierre, Marie
            (3, 2), (3, 4)   # 5ème A : Jean, Pierre
        ]
        
        for class_id, student_id in class_students_data:
            cursor.execute("""
                INSERT OR REPLACE INTO class_students (class_id, student_id)
                VALUES (?, ?)
            """, (class_id, student_id))
        
        # 7. Créer des quiz
        print("📝 Création des quiz...")
        quizzes_data = [
            (1, 'Quiz de Mathématiques', 'Quiz sur les fractions', 'Mathématiques', 30, 10.0, 1),
            (2, 'Quiz de Français', 'Quiz sur la grammaire', 'Français', 20, 8.0, 1),
            (3, 'Quiz de Sciences', 'Quiz sur la biologie', 'Sciences', 25, 12.0, 1)
        ]
        
        for quiz_id, title, description, subject, time_limit, total_points, created_by in quizzes_data:
            cursor.execute("""
                INSERT OR REPLACE INTO quizzes (id, title, description, subject, time_limit, total_points, created_by)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (quiz_id, title, description, subject, time_limit, total_points, created_by))
        
        # 8. Créer des résultats de quiz
        print("📊 Création des résultats de quiz...")
        quiz_results_data = [
            (2, 1, 8, 10, 80.0, datetime.now() - timedelta(days=5)),  # Jean - Math
            (3, 1, 9, 10, 90.0, datetime.now() - timedelta(days=3)),  # Sophie - Math
            (4, 2, 7, 8, 87.5, datetime.now() - timedelta(days=2)),   # Pierre - Français
            (5, 3, 10, 12, 83.3, datetime.now() - timedelta(days=1))  # Marie - Sciences
        ]
        
        for student_id, quiz_id, score, max_score, percentage, completed_at in quiz_results_data:
            cursor.execute("""
                INSERT OR REPLACE INTO quiz_results (student_id, quiz_id, score, max_score, percentage, completed_at, is_completed)
                VALUES (?, ?, ?, ?, ?, ?, 1)
            """, (student_id, quiz_id, score, max_score, percentage, completed_at))
        
        # Valider les changements
        conn.commit()
        print("✅ Données corrigées avec succès !")
        
        # Afficher les informations de connexion
        print("\n🔑 INFORMATIONS DE CONNEXION :")
        print("Email : marie.dubois@najah.ai")
        print("Mot de passe : teacher123")
        print("\n📊 DONNÉES CRÉÉES :")
        print("- 1 professeur")
        print("- 4 étudiants")
        print("- 4 badges")
        print("- 3 classes")
        print("- 3 quiz")
        print("- 4 résultats de quiz")
        
    except Exception as e:
        print(f"❌ Erreur : {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    fix_data_and_auth()