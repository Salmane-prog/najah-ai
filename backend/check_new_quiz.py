#!/usr/bin/env python3
"""
Script pour vérifier les quiz et assignations dans la base de données
"""
import sqlite3
import os

def check_quizzes_and_assignments():
    # Chemin vers la base de données
    db_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'app.db')
    
    if not os.path.exists(db_path):
        print(f"❌ Base de données non trouvée: {db_path}")
        return
    
    print(f"🔍 Vérification de la base de données: {db_path}")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # 1. Vérifier tous les quiz
        print("\n📝 TOUS LES QUIZ:")
        cursor.execute("SELECT id, title, subject, level, time_limit FROM quizzes ORDER BY id")
        quizzes = cursor.fetchall()
        for quiz in quizzes:
            print(f"   - ID: {quiz[0]}, Titre: {quiz[1]}, Sujet: {quiz[2]}, Niveau: {quiz[3]}, Temps: {quiz[4]} min")
        
        # 2. Vérifier les questions pour chaque quiz
        print("\n❓ QUESTIONS PAR QUIZ:")
        for quiz in quizzes:
            cursor.execute("SELECT COUNT(*) FROM questions WHERE quiz_id = ?", (quiz[0],))
            question_count = cursor.fetchone()[0]
            print(f"   - Quiz {quiz[0]} ({quiz[1]}): {question_count} questions")
        
        # 3. Vérifier toutes les assignations
        print("\n📋 TOUTES LES ASSIGNATIONS:")
        cursor.execute("""
            SELECT qa.id, qa.quiz_id, qa.student_id, qa.assigned_at, q.title, q.subject
            FROM quiz_assignments qa
            JOIN quizzes q ON qa.quiz_id = q.id
            ORDER BY qa.assigned_at DESC
        """)
        assignments = cursor.fetchall()
        for assignment in assignments:
            print(f"   - Assignation {assignment[0]}: Quiz {assignment[1]} ({assignment[4]} - {assignment[5]}) pour étudiant {assignment[2]} le {assignment[3]}")
        
        # 4. Vérifier les assignations pour l'étudiant 5
        print("\n🎯 ASSIGNATIONS POUR L'ÉTUDIANT 5:")
        cursor.execute("""
            SELECT qa.id, qa.quiz_id, qa.assigned_at, q.title, q.subject, q.level, q.time_limit,
                   (SELECT COUNT(*) FROM questions WHERE quiz_id = q.id) as question_count
            FROM quiz_assignments qa
            JOIN quizzes q ON qa.quiz_id = q.id
            WHERE qa.student_id = 5
            ORDER BY qa.assigned_at DESC
        """)
        student_assignments = cursor.fetchall()
        for assignment in student_assignments:
            print(f"   - Assignation {assignment[0]}: Quiz {assignment[1]} ({assignment[3]} - {assignment[4]})")
            print(f"     Niveau: {assignment[5]}, Temps: {assignment[6]} min, Questions: {assignment[7]}")
            print(f"     Assigné le: {assignment[2]}")
        
        # 5. Vérifier le dernier quiz créé
        print("\n🆕 DERNIER QUIZ CRÉÉ:")
        cursor.execute("""
            SELECT id, title, subject, level, time_limit, created_at,
                   (SELECT COUNT(*) FROM questions WHERE quiz_id = quizzes.id) as question_count
            FROM quizzes
            ORDER BY created_at DESC
            LIMIT 1
        """)
        latest_quiz = cursor.fetchone()
        if latest_quiz:
            print(f"   - ID: {latest_quiz[0]}")
            print(f"   - Titre: {latest_quiz[1]}")
            print(f"   - Sujet: {latest_quiz[2]}")
            print(f"   - Niveau: {latest_quiz[3]}")
            print(f"   - Temps: {latest_quiz[4]} min")
            print(f"   - Questions: {latest_quiz[6]}")
            print(f"   - Créé le: {latest_quiz[5]}")
        
    except Exception as e:
        print(f"❌ Erreur lors de la vérification: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    print("🔍 Vérification des quiz et assignations...")
    check_quizzes_and_assignments() 