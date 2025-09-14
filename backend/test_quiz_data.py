#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine, text
from core.config import settings

# Créer la connexion à la base de données
engine = create_engine(settings.SQLALCHEMY_DATABASE_URL)

def test_quiz_data():
    """Test pour vérifier les données de quiz dans la base de données"""
    
    with engine.connect() as conn:
        print("=== TEST DES DONNÉES DE QUIZ ===")
        
        # 1. Vérifier les quiz créés par le professeur ID 1
        print("\n1. Quiz créés par le professeur ID 1:")
        result = conn.execute(text("""
            SELECT id, title, subject, level, created_at, max_score, created_by 
            FROM quizzes 
            WHERE created_by = 1
            ORDER BY created_at DESC
        """))
        quizzes = result.fetchall()
        
        if quizzes:
            for quiz in quizzes:
                print(f"  - ID: {quiz.id}, Titre: {quiz.title}, Sujet: {quiz.subject}, Niveau: {quiz.level}, Score max: {quiz.max_score}, Créé le: {quiz.created_at}")
        else:
            print("  Aucun quiz trouvé pour le professeur ID 1")
        
        # 2. Vérifier tous les quiz
        print("\n2. Tous les quiz dans la base:")
        result = conn.execute(text("""
            SELECT id, title, subject, level, created_at, max_score, created_by 
            FROM quizzes 
            ORDER BY created_at DESC
        """))
        all_quizzes = result.fetchall()
        
        if all_quizzes:
            for quiz in all_quizzes:
                print(f"  - ID: {quiz.id}, Titre: {quiz.title}, Sujet: {quiz.subject}, Niveau: {quiz.level}, Score max: {quiz.max_score}, Créé par: {quiz.created_by}, Créé le: {quiz.created_at}")
        else:
            print("  Aucun quiz trouvé dans la base")
        
        # 3. Vérifier les résultats de quiz
        print("\n3. Résultats de quiz:")
        result = conn.execute(text("""
            SELECT qr.id, qr.quiz_id, qr.student_id, qr.score, qr.max_score, qr.percentage, qr.is_completed, qr.created_at,
                   q.title as quiz_title, u.username as student_name
            FROM quiz_results qr
            JOIN quizzes q ON qr.quiz_id = q.id
            JOIN users u ON qr.student_id = u.id
            ORDER BY qr.created_at DESC
            LIMIT 10
        """))
        results = result.fetchall()
        
        if results:
            for result_row in results:
                print(f"  - Quiz: {result_row.quiz_title}, Étudiant: {result_row.student_name}, Score: {result_row.score}/{result_row.max_score} ({result_row.percentage}%), Complété: {result_row.is_completed}")
        else:
            print("  Aucun résultat de quiz trouvé")
        
        # 4. Vérifier les utilisateurs
        print("\n4. Utilisateurs dans la base:")
        result = conn.execute(text("""
            SELECT id, username, email, role 
            FROM users 
            ORDER BY id
        """))
        users = result.fetchall()
        
        if users:
            for user in users:
                print(f"  - ID: {user.id}, Username: {user.username}, Email: {user.email}, Role: {user.role}")
        else:
            print("  Aucun utilisateur trouvé")

if __name__ == "__main__":
    test_quiz_data() 