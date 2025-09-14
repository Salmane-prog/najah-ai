#!/usr/bin/env python3
"""
Script pour créer les tables de liaison entre évaluations formatives et étudiants
"""

import sqlite3
import os
from datetime import datetime

def create_formative_evaluations_tables():
    """Créer les tables pour les évaluations formatives"""
    
    db_path = 'data/app.db'
    
    if not os.path.exists(db_path):
        print(f"❌ Base de données non trouvée: {db_path}")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("🔧 Création des tables pour évaluations formatives...")
        
        # Table pour les évaluations formatives
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS formative_evaluations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            subject TEXT NOT NULL,
            evaluation_type TEXT NOT NULL,
            due_date TEXT NOT NULL,
            total_points INTEGER DEFAULT 100,
            criteria TEXT,
            created_by INTEGER NOT NULL,
            is_active BOOLEAN DEFAULT 1,
            status TEXT DEFAULT 'draft',
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            FOREIGN KEY (created_by) REFERENCES users (id) ON DELETE CASCADE
        )
        ''')
        
        # Table de liaison évaluations - étudiants
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS formative_evaluation_assignments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            evaluation_id INTEGER NOT NULL,
            student_id INTEGER NOT NULL,
            assigned_by INTEGER NOT NULL,
            assigned_at TEXT NOT NULL,
            due_date TEXT NOT NULL,
            status TEXT DEFAULT 'assigned',
            submitted_at TEXT,
            graded_at TEXT,
            score REAL,
            feedback TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            FOREIGN KEY (evaluation_id) REFERENCES formative_evaluations (id) ON DELETE CASCADE,
            FOREIGN KEY (student_id) REFERENCES users (id) ON DELETE CASCADE,
            FOREIGN KEY (assigned_by) REFERENCES users (id) ON DELETE CASCADE,
            UNIQUE(evaluation_id, student_id)
        )
        ''')
        
        # Table pour les soumissions des étudiants
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS formative_evaluation_submissions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            assignment_id INTEGER NOT NULL,
            submission_type TEXT NOT NULL,
            content TEXT,
            file_path TEXT,
            file_name TEXT,
            file_size INTEGER,
            submitted_at TEXT NOT NULL,
            status TEXT DEFAULT 'submitted',
            created_at TEXT NOT NULL,
            FOREIGN KEY (assignment_id) REFERENCES formative_evaluation_assignments (id) ON DELETE CASCADE
        )
        ''')
        
        # Table pour les critères d'évaluation
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS evaluation_criteria (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            evaluation_id INTEGER NOT NULL,
            criterion_name TEXT NOT NULL,
            description TEXT,
            max_points INTEGER NOT NULL,
            weight REAL DEFAULT 1.0,
            created_at TEXT NOT NULL,
            FOREIGN KEY (evaluation_id) REFERENCES formative_evaluations (id) ON DELETE CASCADE
        )
        ''')
        
        # Table pour les scores par critère
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS criterion_scores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            assignment_id INTEGER NOT NULL,
            criterion_id INTEGER NOT NULL,
            score REAL NOT NULL,
            feedback TEXT,
            graded_by INTEGER NOT NULL,
            graded_at TEXT NOT NULL,
            created_at TEXT NOT NULL,
            FOREIGN KEY (assignment_id) REFERENCES formative_evaluation_assignments (id) ON DELETE CASCADE,
            FOREIGN KEY (criterion_id) REFERENCES evaluation_criteria (id) ON DELETE CASCADE,
            FOREIGN KEY (graded_by) REFERENCES users (id) ON DELETE CASCADE
        )
        ''')
        
        # Index pour optimiser les requêtes
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_formative_evaluations_created_by ON formative_evaluations(created_by)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_formative_evaluations_subject ON formative_evaluations(subject)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_formative_evaluations_status ON formative_evaluations(status)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_formative_evaluation_assignments_evaluation_id ON formative_evaluation_assignments(evaluation_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_formative_evaluation_assignments_student_id ON formative_evaluation_assignments(student_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_formative_evaluation_assignments_status ON formative_evaluation_assignments(status)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_formative_evaluation_submissions_assignment_id ON formative_evaluation_submissions(assignment_id)')
        
        conn.commit()
        print("✅ Tables et index créés avec succès !")
        
        # Vérifier la structure
        cursor.execute("PRAGMA table_info(formative_evaluations)")
        columns = cursor.fetchall()
        print(f"\n📊 Structure de la table formative_evaluations:")
        for col in columns:
            print(f"   - {col[1]} ({col[2]})")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la création des tables: {str(e)}")
        return False
        
    finally:
        if conn:
            conn.close()

def add_sample_formative_evaluation_data():
    """Ajouter des données d'exemple pour les évaluations formatives"""
    
    try:
        conn = sqlite3.connect('data/app.db')
        cursor = conn.cursor()
        
        print("\n📝 Ajout de données d'exemple...")
        
        # Vérifier si des données existent déjà
        cursor.execute("SELECT COUNT(*) FROM formative_evaluations")
        existing_evaluations = cursor.fetchall()[0]
        
        if existing_evaluations == 0:
            # Créer des évaluations formatives d'exemple
            evaluations = [
                (
                    "Projet de Recherche - Écologie",
                    "Projet de recherche sur un écosystème local",
                    "Sciences",
                    "projet",
                    "2024-02-15",
                    100,
                    "Recherche, Présentation, Analyse",
                    1  # ID du professeur
                ),
                (
                    "Présentation Orale - Littérature",
                    "Présentation d'une œuvre littéraire du 19ème siècle",
                    "Français",
                    "presentation",
                    "2024-02-10",
                    80,
                    "Contenu, Expression, Support visuel",
                    1
                ),
                (
                    "Discussion Critique - Philosophie",
                    "Analyse critique d'un texte philosophique",
                    "Philosophie",
                    "discussion",
                    "2024-02-20",
                    60,
                    "Compréhension, Argumentation, Critique",
                    1
                )
            ]
            
            for title, description, subject, eval_type, due_date, points, criteria, created_by in evaluations:
                cursor.execute('''
                INSERT INTO formative_evaluations (
                    title, description, subject, evaluation_type, due_date,
                    total_points, criteria, created_by, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    title, description, subject, eval_type, due_date,
                    points, criteria, created_by,
                    datetime.now().isoformat(),
                    datetime.now().isoformat()
                ))
                
                evaluation_id = cursor.lastrowid
                print(f"✅ Évaluation créée: {title} (ID: {evaluation_id})")
                
                # Créer des critères d'évaluation
                if eval_type == "projet":
                    criteria_list = [
                        ("Recherche", "Qualité et pertinence des sources", 30, 1.0),
                        ("Présentation", "Clarté et structure du projet", 40, 1.0),
                        ("Analyse", "Profondeur de l'analyse", 30, 1.0)
                    ]
                elif eval_type == "presentation":
                    criteria_list = [
                        ("Contenu", "Richesse et pertinence du contenu", 40, 1.0),
                        ("Expression", "Clarté et fluidité de l'expression", 30, 1.0),
                        ("Support visuel", "Qualité des supports", 30, 1.0)
                    ]
                else:
                    criteria_list = [
                        ("Compréhension", "Compréhension du texte", 30, 1.0),
                        ("Argumentation", "Qualité de l'argumentation", 30, 1.0),
                        ("Critique", "Pertinence de la critique", 40, 1.0)
                    ]
                
                for criterion_name, criterion_desc, max_points, weight in criteria_list:
                    cursor.execute('''
                    INSERT INTO evaluation_criteria (
                        evaluation_id, criterion_name, description, max_points, weight, created_at
                    ) VALUES (?, ?, ?, ?, ?, ?)
                    ''', (
                        evaluation_id, criterion_name, criterion_desc, max_points, weight,
                        datetime.now().isoformat()
                    ))
                
                # Assigner l'évaluation à des étudiants existants
                cursor.execute("SELECT id FROM users WHERE role = 'student' LIMIT 5")
                students = cursor.fetchall()
                
                for student in students:
                    cursor.execute('''
                    INSERT INTO formative_evaluation_assignments (
                        evaluation_id, student_id, assigned_by, assigned_at, due_date,
                        created_at, updated_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        evaluation_id,
                        student[0],
                        1,  # Professeur
                        datetime.now().isoformat(),
                        due_date,
                        datetime.now().isoformat(),
                        datetime.now().isoformat()
                    ))
                
                print(f"   ✅ Assignée à {len(students)} étudiants")
                
        else:
            print("ℹ️ Des évaluations formatives existent déjà")
        
        conn.commit()
        print("✅ Données d'exemple ajoutées avec succès !")
        
    except Exception as e:
        print(f"❌ Erreur lors de l'ajout des données: {str(e)}")
        
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    print("🚀 CRÉATION DES TABLES POUR ÉVALUATIONS FORMATIVES")
    print("=" * 60)
    
    if create_formative_evaluations_tables():
        add_sample_formative_evaluation_data()
        print("\n🎉 Configuration des évaluations formatives terminée !")
    else:
        print("\n❌ Échec de la configuration")























