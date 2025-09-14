#!/usr/bin/env python3
"""
Script simple pour vérifier les questions dans la base de données
"""

import sqlite3
import os

def check_questions_simple():
    print("=== VÉRIFICATION SIMPLE DES QUESTIONS ===")
    
    # Chemin de la base
    db_path = "../data/app.db"
    print(f"📊 Base de données: {db_path}")
    
    if not os.path.exists(db_path):
        print("❌ Base de données non trouvée!")
        return
    
    # Connexion SQLite
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Vérifier les tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print(f"📋 Tables: {[table[0] for table in tables]}")
    
    # Vérifier les quizzes
    cursor.execute("SELECT id, title, is_active FROM quizzes;")
    quizzes = cursor.fetchall()
    print(f"\n📊 Quizzes trouvés: {len(quizzes)}")
    for quiz in quizzes:
        print(f"  - Quiz {quiz[0]}: {quiz[1]} (actif: {quiz[2]})")
    
    # Vérifier les questions
    cursor.execute("SELECT id, question_text, quiz_id FROM questions LIMIT 10;")
    questions = cursor.fetchall()
    print(f"\n📊 Questions trouvées: {len(questions)}")
    
    if questions:
        for q in questions:
            print(f"  - Question {q[0]}: {q[1][:50]}... (quiz_id: {q[2]})")
    else:
        print("❌ Aucune question trouvée!")
    
    # Vérifier les questions par quiz actif
    cursor.execute("""
        SELECT q.id, q.title, COUNT(qu.id) as question_count 
        FROM quizzes q 
        LEFT JOIN questions qu ON q.id = qu.quiz_id 
        WHERE q.is_active = 1 
        GROUP BY q.id;
    """)
    active_quizzes = cursor.fetchall()
    print(f"\n📊 Quizzes actifs avec questions:")
    for quiz in active_quizzes:
        print(f"  - Quiz {quiz[0]}: {quiz[1]} ({quiz[2]} questions)")
    
    conn.close()
    print("\n✅ Vérification terminée")

if __name__ == "__main__":
    check_questions_simple() 