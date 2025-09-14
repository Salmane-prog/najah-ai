#!/usr/bin/env python3
"""
Script pour corriger la structure de la base de données Najah AI
"""

import sqlite3
import os

def fix_database_schema():
    """Corriger la structure de la base de données"""
    
    # Créer le dossier data s'il n'existe pas
    os.makedirs('./data', exist_ok=True)
    
    conn = sqlite3.connect('./data/app.db')
    cursor = conn.cursor()
    
    print("🔧 Correction de la structure de la base de données...")
    
    # 1. Créer la table users si elle n'existe pas
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            full_name TEXT NOT NULL,
            role TEXT CHECK(role IN ('student', 'teacher', 'admin')) DEFAULT 'student',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # 2. Ajouter des utilisateurs de test
    test_users = [
        ('student1', 'student1@najah.ai', 'Étudiant Test 1', 'student'),
        ('student2', 'student2@najah.ai', 'Étudiant Test 2', 'student'),
        ('teacher1', 'teacher1@najah.ai', 'Enseignant Test 1', 'teacher'),
        ('admin1', 'admin1@najah.ai', 'Administrateur Test 1', 'admin')
    ]
    
    for user in test_users:
        try:
            cursor.execute('''
                INSERT OR IGNORE INTO users (username, email, full_name, role)
                VALUES (?, ?, ?, ?)
            ''', user)
        except Exception as e:
            print(f"⚠️ Utilisateur {user[0]} déjà existant")
    
    # 3. Corriger la table student_assessment_results
    # Supprimer la contrainte de clé étrangère problématique
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS student_assessment_results_new (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER,
            assessment_id INTEGER,
            score INTEGER DEFAULT 0,
            total_possible INTEGER DEFAULT 0,
            percentage REAL DEFAULT 0.0,
            time_taken INTEGER DEFAULT 0,
            completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Copier les données existantes
    cursor.execute('''
        INSERT INTO student_assessment_results_new 
        SELECT * FROM student_assessment_results
    ''')
    
    # Supprimer l'ancienne table
    cursor.execute('DROP TABLE student_assessment_results')
    
    # Renommer la nouvelle table
    cursor.execute('ALTER TABLE student_assessment_results_new RENAME TO student_assessment_results')
    
    # 4. Corriger la table student_answers
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS student_answers_new (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER,
            question_id INTEGER,
            assessment_id INTEGER,
            answer_text TEXT,
            selected_answer_id INTEGER,
            is_correct BOOLEAN,
            points_earned INTEGER DEFAULT 0,
            answered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Copier les données existantes
    cursor.execute('''
        INSERT INTO student_answers_new 
        SELECT * FROM student_answers
    ''')
    
    # Supprimer l'ancienne table
    cursor.execute('DROP TABLE student_answers')
    
    # Renommer la nouvelle table
    cursor.execute('ALTER TABLE student_answers_new RENAME TO student_answers')
    
    # 5. Ajouter des données de test pour les évaluations
    # Créer des résultats d'évaluation de test
    test_results = [
        (1, 1, 15, 20, 0.75, 300, '2024-01-15 10:00:00'),
        (1, 2, 18, 20, 0.90, 280, '2024-01-16 14:30:00'),
        (2, 1, 12, 20, 0.60, 350, '2024-01-15 11:00:00'),
        (2, 3, 16, 20, 0.80, 320, '2024-01-17 09:15:00')
    ]
    
    for result in test_results:
        cursor.execute('''
            INSERT OR IGNORE INTO student_assessment_results 
            (student_id, assessment_id, score, total_possible, percentage, time_taken, completed_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', result)
    
    # 6. Ajouter des réponses d'étudiants de test
    test_answers = [
        (1, 1, 1, 1, True, 1, '2024-01-15 10:00:00'),
        (1, 2, 1, 2, False, 0, '2024-01-15 10:00:00'),
        (1, 3, 1, 1, True, 1, '2024-01-15 10:00:00'),
        (2, 1, 1, 1, True, 1, '2024-01-15 11:00:00'),
        (2, 2, 1, 2, False, 0, '2024-01-15 11:00:00')
    ]
    
    for answer in test_answers:
        cursor.execute('''
            INSERT OR IGNORE INTO student_answers 
            (student_id, question_id, assessment_id, selected_answer_id, is_correct, points_earned, answered_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', answer)
    
    # Valider les changements
    conn.commit()
    
    print("✅ Structure de la base de données corrigée !")
    
    # Vérifier la structure finale
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    
    print(f"📊 Tables disponibles : {len(tables)}")
    for table in tables:
        print(f"   • {table[0]}")
    
    # Vérifier les données
    cursor.execute("SELECT COUNT(*) FROM users")
    users_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM student_assessment_results")
    results_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM student_answers")
    answers_count = cursor.fetchone()[0]
    
    print(f"\n📈 Données de test ajoutées :")
    print(f"   • Utilisateurs : {users_count}")
    print(f"   • Résultats d'évaluation : {results_count}")
    print(f"   • Réponses d'étudiants : {answers_count}")
    
    conn.close()

if __name__ == "__main__":
    fix_database_schema() 