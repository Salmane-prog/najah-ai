#!/usr/bin/env python3
"""
Script pour créer la table de liaison entre tests adaptatifs et étudiants
"""

import sqlite3
import os
from datetime import datetime

def create_adaptive_test_assignments_table():
    """Créer la table de liaison tests adaptatifs - étudiants"""
    
    db_path = 'data/app.db'
    
    if not os.path.exists(db_path):
        print(f"❌ Base de données non trouvée: {db_path}")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("🔧 Création de la table adaptive_test_assignments...")
        
        # Table de liaison tests adaptatifs - étudiants
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS adaptive_test_assignments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            test_id INTEGER NOT NULL,
            student_id INTEGER NOT NULL,
            assigned_by INTEGER NOT NULL,
            assigned_at TEXT NOT NULL,
            due_date TEXT,
            status TEXT DEFAULT 'assigned',
            started_at TEXT,
            completed_at TEXT,
            current_question INTEGER DEFAULT 1,
            total_questions INTEGER NOT NULL,
            current_score REAL DEFAULT 0,
            max_score REAL DEFAULT 100,
            adaptation_level TEXT DEFAULT 'medium',
            questions_answered INTEGER DEFAULT 0,
            time_spent INTEGER DEFAULT 0,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            FOREIGN KEY (test_id) REFERENCES adaptive_tests (id) ON DELETE CASCADE,
            FOREIGN KEY (student_id) REFERENCES users (id) ON DELETE CASCADE,
            FOREIGN KEY (assigned_by) REFERENCES users (id) ON DELETE CASCADE,
            UNIQUE(test_id, student_id)
        )
        ''')
        
        # Table pour les réponses des étudiants aux tests adaptatifs
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS adaptive_test_responses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            assignment_id INTEGER NOT NULL,
            question_id INTEGER NOT NULL,
            student_answer TEXT,
            is_correct BOOLEAN,
            time_spent INTEGER,
            difficulty_level TEXT,
            adaptation_factor REAL,
            answered_at TEXT NOT NULL,
            created_at TEXT NOT NULL,
            FOREIGN KEY (assignment_id) REFERENCES adaptive_test_assignments (id) ON DELETE CASCADE,
            FOREIGN KEY (question_id) REFERENCES adaptive_test_questions (id) ON DELETE CASCADE
        )
        ''')
        
        # Table pour les questions des tests adaptatifs
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS adaptive_test_questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            test_id INTEGER NOT NULL,
            question_text TEXT NOT NULL,
            question_type TEXT NOT NULL,
            difficulty_level TEXT NOT NULL,
            subject TEXT NOT NULL,
            options TEXT,
            correct_answer TEXT NOT NULL,
            explanation TEXT,
            points INTEGER DEFAULT 1,
            created_at TEXT NOT NULL,
            FOREIGN KEY (test_id) REFERENCES adaptive_tests (id) ON DELETE CASCADE
        )
        ''')
        
        # Table pour les tests adaptatifs
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS adaptive_tests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            subject TEXT NOT NULL,
            difficulty_range TEXT NOT NULL,
            total_questions INTEGER NOT NULL,
            estimated_duration INTEGER NOT NULL,
            created_by INTEGER NOT NULL,
            is_active BOOLEAN DEFAULT 1,
            adaptation_algorithm TEXT DEFAULT 'irt',
            min_difficulty INTEGER DEFAULT 1,
            max_difficulty INTEGER DEFAULT 10,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            FOREIGN KEY (created_by) REFERENCES users (id) ON DELETE CASCADE
        )
        ''')
        
        # Index pour optimiser les requêtes
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_adaptive_test_assignments_test_id ON adaptive_test_assignments(test_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_adaptive_test_assignments_student_id ON adaptive_test_assignments(student_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_adaptive_test_assignments_status ON adaptive_test_assignments(status)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_adaptive_test_responses_assignment_id ON adaptive_test_responses(assignment_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_adaptive_test_questions_test_id ON adaptive_test_questions(test_id)')
        
        conn.commit()
        print("✅ Tables et index créés avec succès !")
        
        # Vérifier la structure
        cursor.execute("PRAGMA table_info(adaptive_test_assignments)")
        columns = cursor.fetchall()
        print(f"\n📊 Structure de la table adaptive_test_assignments:")
        for col in columns:
            print(f"   - {col[1]} ({col[2]})")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la création des tables: {str(e)}")
        return False
        
    finally:
        if conn:
            conn.close()

def add_sample_adaptive_test_data():
    """Ajouter des données d'exemple pour les tests adaptatifs"""
    
    try:
        conn = sqlite3.connect('data/app.db')
        cursor = conn.cursor()
        
        print("\n📝 Ajout de données d'exemple...")
        
        # Vérifier si des données existent déjà
        cursor.execute("SELECT COUNT(*) FROM adaptive_tests")
        existing_tests = cursor.fetchone()[0]
        
        if existing_tests == 0:
            # Créer un test adaptatif d'exemple
            cursor.execute('''
            INSERT INTO adaptive_tests (
                title, description, subject, difficulty_range, total_questions, 
                estimated_duration, created_by, adaptation_algorithm, 
                min_difficulty, max_difficulty, created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                "Test de Grammaire Française Niveau Intermédiaire",
                "Test adaptatif pour évaluer les compétences en grammaire française",
                "Français",
                "Niveau 3-7",
                15,
                25,
                1,  # ID du professeur
                "irt",
                3,
                7,
                datetime.now().isoformat(),
                datetime.now().isoformat()
            ))
            
            test_id = cursor.lastrowid
            print(f"✅ Test adaptatif créé avec l'ID: {test_id}")
            
            # Créer des questions d'exemple
            questions = [
                ("Quelle est la forme correcte du verbe 'aller' à la 3ème personne du pluriel ?", "Conjugaison", "medium", "vont", "Ils vont au marché.", 2),
                ("Identifiez le type de phrase : 'Quelle belle journée !'", "Types de phrases", "easy", "Exclamative", "Une phrase qui exprime une émotion.", 1),
                ("Trouvez l'erreur : 'Les enfants joues dans le jardin.'", "Accord", "medium", "joues", "Le verbe doit s'accorder avec le sujet pluriel.", 2),
            ]
            
            for question_text, question_type, difficulty, correct_answer, explanation, points in questions:
                cursor.execute('''
                INSERT INTO adaptive_test_questions (
                    test_id, question_text, question_type, difficulty_level, 
                    subject, correct_answer, explanation, points, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    test_id, question_text, question_type, difficulty, 
                    "Français", correct_answer, explanation, points, 
                    datetime.now().isoformat()
                ))
            
            print(f"✅ {len(questions)} questions créées")
            
            # Assigner le test à des étudiants existants
            cursor.execute("SELECT id FROM users WHERE role = 'student' LIMIT 3")
            students = cursor.fetchall()
            
            for student in students:
                cursor.execute('''
                INSERT INTO adaptive_test_assignments (
                    test_id, student_id, assigned_by, assigned_at, due_date,
                    total_questions, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    test_id,
                    student[0],
                    1,  # Professeur
                    datetime.now().isoformat(),
                    datetime.now().isoformat(),
                    15,
                    datetime.now().isoformat(),
                    datetime.now().isoformat()
                ))
            
            print(f"✅ Test assigné à {len(students)} étudiants")
            
        else:
            print("ℹ️ Des tests adaptatifs existent déjà")
        
        conn.commit()
        print("✅ Données d'exemple ajoutées avec succès !")
        
    except Exception as e:
        print(f"❌ Erreur lors de l'ajout des données: {str(e)}")
        
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    print("🚀 CRÉATION DES TABLES POUR TESTS ADAPTATIFS")
    print("=" * 50)
    
    if create_adaptive_test_assignments_table():
        add_sample_adaptive_test_data()
        print("\n🎉 Configuration des tests adaptatifs terminée !")
    else:
        print("\n❌ Échec de la configuration")























