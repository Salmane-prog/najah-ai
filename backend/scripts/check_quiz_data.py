#!/usr/bin/env python3
"""
Script pour vérifier les données des quiz dans la base de données
"""

import sqlite3
import os

def check_quiz_data():
    """Vérifier les données des quiz dans la base de données"""
    
    # Utiliser le bon chemin de la base de données
    db_path = "../data/app.db"
    
    if not os.path.exists(db_path):
        print(f"❌ Base de données non trouvée: {db_path}")
        return
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("🔍 Vérification des données des quiz...")
        
        # Vérifier les utilisateurs disponibles
        print("\n👥 Utilisateurs disponibles:")
        cursor.execute("SELECT id, username, email, role FROM users LIMIT 10")
        users = cursor.fetchall()
        for user in users:
            user_id, username, email, role = user
            print(f"  - ID: {user_id}, Username: {username}, Email: {email}, Role: {role}")
        
        # Vérifier la table quizzes
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='quizzes'")
        if cursor.fetchone():
            print("\n✅ Table 'quizzes' existe")
            
            # Compter les quiz
            cursor.execute("SELECT COUNT(*) FROM quizzes")
            quiz_count = cursor.fetchone()[0]
            print(f"📊 Nombre total de quiz: {quiz_count}")
            
            # Lister tous les quiz avec leurs détails
            cursor.execute("""
                SELECT id, title, description, subject, difficulty, max_score, is_active, created_at, created_by
                FROM quizzes
                ORDER BY created_at DESC
            """)
            
            quizzes = cursor.fetchall()
            
            if quizzes:
                print("\n📋 Liste des quiz dans la base de données:")
                print("-" * 80)
                for quiz in quizzes:
                    quiz_id, title, description, subject, difficulty, max_score, is_active, created_at, created_by = quiz
                    status = "✅ Actif" if is_active else "❌ Inactif"
                    print(f"ID: {quiz_id}")
                    print(f"Titre: {title}")
                    print(f"Description: {description}")
                    print(f"Matière: {subject}")
                    print(f"Difficulté: {difficulty}")
                    print(f"Points max: {max_score}")
                    print(f"Statut: {status}")
                    print(f"Créé par: {created_by}")
                    print(f"Créé le: {created_at}")
                    print("-" * 40)
                    
                    # Compter les questions pour ce quiz
                    cursor.execute("SELECT COUNT(*) FROM questions WHERE quiz_id = ?", (quiz_id,))
                    question_count = cursor.fetchone()[0]
                    print(f"Nombre de questions: {question_count}")
                    print()
            else:
                print("❌ Aucun quiz trouvé dans la base de données")
        else:
            print("❌ Table 'quizzes' n'existe pas")
        
        # Vérifier la table questions
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='questions'")
        if cursor.fetchone():
            print("✅ Table 'questions' existe")
            
            cursor.execute("SELECT COUNT(*) FROM questions")
            question_count = cursor.fetchone()[0]
            print(f"📊 Nombre total de questions: {question_count}")
        else:
            print("❌ Table 'questions' n'existe pas")
        
        # Vérifier les résultats de quiz
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='quiz_results'")
        if cursor.fetchone():
            print("✅ Table 'quiz_results' existe")
            
            cursor.execute("SELECT COUNT(*) FROM quiz_results")
            result_count = cursor.fetchone()[0]
            print(f"📊 Nombre total de résultats: {result_count}")
        else:
            print("❌ Table 'quiz_results' n'existe pas")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Erreur lors de la vérification: {e}")

if __name__ == "__main__":
    check_quiz_data() 