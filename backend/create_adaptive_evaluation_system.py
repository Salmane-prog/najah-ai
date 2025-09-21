#!/usr/bin/env python3
"""
Script pour recréer complètement le système d'évaluation adaptative
"""

import sqlite3
import os

def create_database():
    """Créer la base de données complète pour l'évaluation adaptative"""
    
    # Chemin vers la base de données
    db_path = "najah_ai.db"
    
    # Supprimer l'ancienne base si elle existe
    if os.path.exists(db_path):
        os.remove(db_path)
        print("🗑️ Ancienne base supprimée")
    
    # Créer la nouvelle base
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print("🚀 Création du système d'évaluation adaptative...")
    
    # 1. Table des tests adaptatifs
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS adaptive_tests (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        subject TEXT NOT NULL,
        description TEXT,
        difficulty_min INTEGER DEFAULT 1,
        difficulty_max INTEGER DEFAULT 10,
        estimated_duration INTEGER DEFAULT 30,
        total_questions INTEGER DEFAULT 20,
        adaptation_type TEXT DEFAULT 'hybrid',
        learning_objectives TEXT,
        is_active BOOLEAN DEFAULT TRUE,
        created_by INTEGER NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (created_by) REFERENCES users (id)
    )
    """)
    
    # 2. Table des questions
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS adaptive_questions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        test_id INTEGER NOT NULL,
        question_text TEXT NOT NULL,
        question_type TEXT DEFAULT 'multiple_choice',
        difficulty_level INTEGER NOT NULL,
        learning_objective TEXT,
        options TEXT, -- JSON des options pour QCM
        correct_answer TEXT,
        explanation TEXT,
        order_index INTEGER DEFAULT 0,
        FOREIGN KEY (test_id) REFERENCES adaptive_tests (id) ON DELETE CASCADE
    )
    """)
    
    # 3. Table des assignations
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS test_assignments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        test_id INTEGER NOT NULL,
        assignment_type TEXT NOT NULL CHECK (assignment_type IN ('class', 'student')),
        target_id INTEGER NOT NULL, -- ID de la classe ou de l'étudiant
        assigned_by INTEGER NOT NULL,
        assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        due_date TIMESTAMP,
        status TEXT DEFAULT 'active' CHECK (status IN ('active', 'inactive', 'completed')),
        FOREIGN KEY (test_id) REFERENCES adaptive_tests (id) ON DELETE CASCADE,
        FOREIGN KEY (assigned_by) REFERENCES users (id)
    )
    """)
    
    # 4. Table des tentatives de test
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS test_attempts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        test_id INTEGER NOT NULL,
        student_id INTEGER NOT NULL,
        assignment_id INTEGER,
        started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        completed_at TIMESTAMP,
        status TEXT DEFAULT 'in_progress' CHECK (status IN ('in_progress', 'completed', 'abandoned')),
        current_question_index INTEGER DEFAULT 0,
        total_score REAL DEFAULT 0,
        max_score REAL DEFAULT 0,
        FOREIGN KEY (test_id) REFERENCES adaptive_tests (id),
        FOREIGN KEY (student_id) REFERENCES users (id),
        FOREIGN KEY (assignment_id) REFERENCES test_assignments (id)
    )
    """)
    
    # 5. Table des réponses aux questions
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS question_responses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        attempt_id INTEGER NOT NULL,
        question_id INTEGER NOT NULL,
        student_answer TEXT,
        is_correct BOOLEAN,
        score REAL DEFAULT 0,
        response_time INTEGER, -- en secondes
        answered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (attempt_id) REFERENCES test_attempts (id),
        FOREIGN KEY (question_id) REFERENCES adaptive_questions (id)
    )
    """)
    
    # 6. Table des compétences analysées
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS competency_analysis (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        attempt_id INTEGER NOT NULL,
        student_id INTEGER NOT NULL,
        test_id INTEGER NOT NULL,
        competency_name TEXT NOT NULL,
        competency_level REAL DEFAULT 0, -- 0-100
        confidence_score REAL DEFAULT 0, -- 0-100
        ai_recommendations TEXT,
        analyzed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (attempt_id) REFERENCES test_attempts (id),
        FOREIGN KEY (student_id) REFERENCES users (id),
        FOREIGN KEY (test_id) REFERENCES adaptive_tests (id)
    )
    """)
    
    # 7. Table des classes (si elle n'existe pas)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS classes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT,
        teacher_id INTEGER NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (teacher_id) REFERENCES users (id)
    )
    """)
    
    # 8. Table des étudiants par classe
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS class_students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        class_id INTEGER NOT NULL,
        student_id INTEGER NOT NULL,
        joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (class_id) REFERENCES classes (id),
        FOREIGN KEY (student_id) REFERENCES users (id),
        UNIQUE(class_id, student_id)
    )
    """)
    
    print("✅ Tables créées avec succès")
    
    # Créer des données d'exemple
    create_sample_data(cursor)
    
    conn.commit()
    conn.close()
    
    print("🎉 Système d'évaluation adaptative créé avec succès !")

def create_sample_data(cursor):
    """Créer des données d'exemple pour tester le système"""
    
    print("📝 Création des données d'exemple...")
    
    # 1. Créer des classes d'exemple
    cursor.execute("""
    INSERT INTO classes (name, description, teacher_id) VALUES 
    ('6ème A - Mathématiques', 'Classe de 6ème spécialisée en mathématiques', 33),
    ('5ème B - Français', 'Classe de 5ème spécialisée en français', 33),
    ('4ème C - Sciences', 'Classe de 4ème spécialisée en sciences', 33)
    """)
    
    # 2. Créer des tests adaptatifs d'exemple
    cursor.execute("""
    INSERT INTO adaptive_tests (title, subject, description, difficulty_min, difficulty_max, 
                               estimated_duration, total_questions, adaptation_type, 
                               learning_objectives, created_by) VALUES 
    ('Test de Grammaire Française - Niveau Intermédiaire', 'Français', 
     'Test adaptatif pour évaluer les compétences en grammaire française', 3, 7, 25, 15, 
     'hybrid', 'Maîtriser la conjugaison, les accords et la syntaxe', 33),
    
    ('Évaluation Mathématiques - Algèbre', 'Mathématiques', 
     'Test adaptatif sur les équations du premier degré et les inéquations', 4, 8, 30, 20, 
     'performance', 'Résoudre des équations et inéquations du premier degré', 33),
    
    ('Histoire - Révolution Française', 'Histoire', 
     'Test adaptatif sur la période révolutionnaire française', 2, 6, 20, 12, 
     'cognitive', 'Comprendre les événements clés et les personnages importants', 33),
    
    ('Sciences - Cycle de l''Eau', 'Sciences', 
     'Test adaptatif sur le cycle de l''eau et les écosystèmes', 3, 7, 25, 18, 
     'hybrid', 'Comprendre le cycle de l''eau et l''impact humain', 33),
    
    ('Géographie - Cartographie', 'Géographie', 
     'Test adaptatif sur la lecture de cartes et les climats', 2, 6, 20, 16, 
     'cognitive', 'Lire des cartes et comprendre les climats du monde', 33)
    """)
    
    # 3. Créer des questions d'exemple pour le premier test
    test_id = 1
    questions = [
        ("Quelle est la forme correcte du verbe 'aller' à la 3ème personne du pluriel du présent ?", 5, "Conjugaison des verbes", "vont", "Le verbe 'aller' se conjugue : je vais, tu vas, il va, nous allons, vous allez, ils vont."),
        ("Dans la phrase 'Les enfants jouent dans le jardin', quel est le sujet ?", 4, "Identification du sujet", "Les enfants", "Le sujet est celui qui fait l'action. Ici, 'Les enfants' est le sujet du verbe 'jouent'."),
        ("Complétez : 'La fille ___ belle.' (choisir le bon accord)", 6, "Accord de l'adjectif", "est", "L'adjectif 'belle' s'accorde avec le sujet féminin singulier 'fille'."),
        ("Quel est le temps du verbe dans 'Nous aurons fini' ?", 7, "Temps composés", "futur antérieur", "Le futur antérieur se forme avec 'avoir' au futur + participe passé."),
        ("Identifiez la fonction de 'très' dans 'Il est très intelligent'", 5, "Fonction des mots", "adverbe de degré", "'Très' modifie l'adjectif 'intelligent' et indique un degré élevé.")
    ]
    
    for i, (question_text, difficulty, objective, correct, explanation) in enumerate(questions):
        cursor.execute("""
        INSERT INTO adaptive_questions (test_id, question_text, difficulty_level, learning_objective, 
                                       correct_answer, explanation, order_index) VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (test_id, question_text, difficulty, objective, correct, explanation, i + 1))
    
    # 4. Créer des assignations d'exemple
    cursor.execute("""
    INSERT INTO test_assignments (test_id, assignment_type, target_id, assigned_by, due_date) VALUES 
    (1, 'class', 1, 33, '2024-12-31 23:59:59'),
    (2, 'class', 2, 33, '2024-12-31 23:59:59'),
    (3, 'class', 3, 33, '2024-12-31 23:59:59')
    """)
    
    print("✅ Données d'exemple créées")
    print(f"   - 3 classes créées")
    print(f"   - 5 tests adaptatifs créés")
    print(f"   - 5 questions créées pour le premier test")
    print(f"   - 3 assignations créées")

if __name__ == "__main__":
    create_database()




















