#!/usr/bin/env python3
"""
Script pour créer des tests adaptatifs de démonstration
"""

import sqlite3
import os
from datetime import datetime, timedelta
import json

def create_sample_adaptive_tests():
    """Créer des tests adaptatifs de démonstration"""
    
    # Chemin vers la base de données
    db_path = os.path.join(os.path.dirname(__file__), "..", "data", "app.db")
    
    if not os.path.exists(db_path):
        print(f"❌ Base de données non trouvée: {db_path}")
        return False
    
    print(f"🔍 Connexion à la base de données: {db_path}")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Vérifier si les tables existent
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='adaptive_tests'")
        if not cursor.fetchone():
            print("❌ Table adaptive_tests n'existe pas. Créez d'abord les tables.")
            return False
        
        # Vérifier s'il y a déjà des tests
        cursor.execute("SELECT COUNT(*) FROM adaptive_tests")
        existing_count = cursor.fetchone()[0]
        
        if existing_count > 0:
            print(f"✅ {existing_count} tests adaptatifs existent déjà")
            return True
        
        print("🚀 Création des tests adaptatifs de démonstration...")
        
        # Récupérer un utilisateur enseignant
        cursor.execute("SELECT id FROM users WHERE role = 'teacher' LIMIT 1")
        teacher_result = cursor.fetchone()
        
        if not teacher_result:
            print("❌ Aucun enseignant trouvé dans la base de données")
            return False
        
        teacher_id = teacher_result[0]
        print(f"👨‍🏫 Enseignant trouvé: ID {teacher_id}")
        
        # Tests de démonstration
    sample_tests = [
        {
            "title": "Test de Grammaire Française Niveau Intermédiaire",
            "subject": "Français",
                "description": "Test adaptatif pour évaluer les compétences en grammaire française, incluant la conjugaison, les accords et la syntaxe.",
                "difficulty_range_min": 3,
                "difficulty_range_max": 7,
            "estimated_duration": 25,
            "is_active": True
        },
        {
            "title": "Évaluation Mathématiques - Algèbre",
            "subject": "Mathématiques",
                "description": "Test adaptatif sur les équations du premier degré, les inéquations et les systèmes d'équations.",
                "difficulty_range_min": 4,
                "difficulty_range_max": 8,
            "estimated_duration": 30,
            "is_active": True
        },
        {
            "title": "Histoire - Révolution Française",
            "subject": "Histoire",
                "description": "Test adaptatif sur la période révolutionnaire française, les événements clés et les personnages importants.",
                "difficulty_range_min": 2,
                "difficulty_range_max": 6,
            "estimated_duration": 20,
                "is_active": True
            },
            {
                "title": "Sciences - Cycle de l'Eau et Écosystèmes",
                "subject": "Sciences",
                "description": "Test adaptatif sur le cycle de l'eau, les écosystèmes et l'impact humain sur l'environnement.",
                "difficulty_range_min": 3,
                "difficulty_range_max": 7,
                "estimated_duration": 25,
                "is_active": True
            },
            {
                "title": "Géographie - Cartographie et Climat",
                "subject": "Géographie",
                "description": "Test adaptatif sur la lecture de cartes, les climats du monde et la géographie physique.",
                "difficulty_range_min": 2,
                "difficulty_range_max": 6,
                "estimated_duration": 20,
                "is_active": True
            }
        ]
        
        # Insérer les tests
        for test_data in sample_tests:
            cursor.execute("""
                INSERT INTO adaptive_tests (
                    title, subject, description, difficulty_range_min, difficulty_range_max,
                    estimated_duration, is_active, created_by, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                test_data["title"],
                test_data["subject"],
                test_data["description"],
                test_data["difficulty_range_min"],
                test_data["difficulty_range_max"],
                test_data["estimated_duration"],
                test_data["is_active"],
                teacher_id,
                datetime.now().isoformat(),
                datetime.now().isoformat()
            ))
            
            test_id = cursor.lastrowid
            print(f"✅ Test créé: {test_data['title']} (ID: {test_id})")
            
            # Créer quelques questions d'exemple pour chaque test
            create_sample_questions(cursor, test_id, test_data["subject"])
        
        # Créer les tables de support si elles n'existent pas
        create_support_tables(cursor)
        
        # Créer des assignations de démonstration
        create_sample_assignments(cursor, teacher_id)
        
        conn.commit()
        print(f"🎉 {len(sample_tests)} tests adaptatifs créés avec succès !")
        
        return True
                
        except Exception as e:
        print(f"❌ Erreur lors de la création des tests: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()

def create_sample_questions(cursor, test_id, subject):
    """Créer des questions d'exemple pour un test"""
    
    questions_data = {
        "Français": [
            {
                "question_text": "Quel est le temps du verbe dans la phrase 'Je mange une pomme' ?",
                "question_type": "multiple_choice",
                "options": json.dumps(["Présent", "Imparfait", "Futur", "Passé composé"]),
                "correct_answer": "Présent",
                "explanation": "Le verbe 'mange' est au présent de l'indicatif.",
                "difficulty_level": 3,
                "topic": "Conjugaison"
            },
            {
                "question_text": "Complétez : 'Les enfants ___ dans le jardin.'",
                "question_type": "fill_blank",
                "options": json.dumps([]),
                "correct_answer": "jouent",
                "explanation": "Avec le sujet 'Les enfants' (pluriel), le verbe 'jouer' prend la terminaison '-ent'.",
                "difficulty_level": 4,
                "topic": "Accords"
            }
        ],
        "Mathématiques": [
            {
                "question_text": "Résolvez l'équation : 2x + 5 = 13",
                "question_type": "fill_blank",
                "options": json.dumps([]),
                "correct_answer": "4",
                "explanation": "2x + 5 = 13 → 2x = 8 → x = 4",
                "difficulty_level": 4,
                "topic": "Équations"
            },
            {
                "question_text": "Quelle est la solution de l'inéquation 3x - 2 > 7 ?",
                "question_type": "multiple_choice",
                "options": json.dumps(["x > 3", "x < 3", "x ≥ 3", "x ≤ 3"]),
                "correct_answer": "x > 3",
                "explanation": "3x - 2 > 7 → 3x > 9 → x > 3",
                "difficulty_level": 5,
                "topic": "Inéquations"
            }
        ],
        "Histoire": [
            {
                "question_text": "En quelle année a eu lieu la prise de la Bastille ?",
                "question_type": "multiple_choice",
                "options": json.dumps(["1789", "1790", "1791", "1792"]),
                "correct_answer": "1789",
                "explanation": "La prise de la Bastille a eu lieu le 14 juillet 1789.",
                "difficulty_level": 3,
                "topic": "Révolution Française"
            },
            {
                "question_text": "Qui était Maximilien de Robespierre ?",
                "question_type": "multiple_choice",
                "options": json.dumps(["Un roi", "Un révolutionnaire", "Un général", "Un écrivain"]),
                "correct_answer": "Un révolutionnaire",
                "explanation": "Robespierre était un avocat et révolutionnaire français, figure de la Terreur.",
                "difficulty_level": 4,
                "topic": "Personnages"
            }
        ],
        "Sciences": [
            {
                "question_text": "Quel est le nom du processus par lequel l'eau passe de l'état liquide à l'état gazeux ?",
                "question_type": "multiple_choice",
                "options": json.dumps(["Condensation", "Évaporation", "Solidification", "Fusion"]),
                "correct_answer": "Évaporation",
                "explanation": "L'évaporation est le passage de l'état liquide à l'état gazeux.",
                "difficulty_level": 3,
                "topic": "Cycle de l'Eau"
            },
            {
                "question_text": "Qu'est-ce qu'un écosystème ?",
                "question_type": "multiple_choice",
                "options": json.dumps(["Un animal", "Un ensemble d'êtres vivants et leur environnement", "Une plante", "Un minéral"]),
                "correct_answer": "Un ensemble d'êtres vivants et leur environnement",
                "explanation": "Un écosystème est un ensemble formé par une communauté d'êtres vivants et son environnement.",
                "difficulty_level": 4,
                "topic": "Écosystèmes"
            }
        ],
        "Géographie": [
            {
                "question_text": "Quel type de carte montre les reliefs et l'altitude ?",
                "question_type": "multiple_choice",
                "options": json.dumps(["Carte politique", "Carte topographique", "Carte climatique", "Carte économique"]),
                "correct_answer": "Carte topographique",
                "explanation": "Une carte topographique montre les reliefs, l'altitude et les formes du terrain.",
                "difficulty_level": 3,
                "topic": "Cartographie"
            },
            {
                "question_text": "Quel est le climat dominant en France métropolitaine ?",
                "question_type": "multiple_choice",
                "options": json.dumps(["Climat tropical", "Climat océanique", "Climat désertique", "Climat polaire"]),
                "correct_answer": "Climat océanique",
                "explanation": "La France métropolitaine a principalement un climat océanique tempéré.",
                "difficulty_level": 4,
                "topic": "Climat"
            }
        ]
    }
    
    questions = questions_data.get(subject, questions_data["Français"])
    
    for question_data in questions:
        cursor.execute("""
            INSERT INTO adaptive_questions (
                test_id, question_text, question_type, options, correct_answer,
                explanation, difficulty_level, subject, topic, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            test_id,
            question_data["question_text"],
            question_data["question_type"],
            question_data["options"],
            question_data["correct_answer"],
            question_data["explanation"],
            question_data["difficulty_level"],
            subject,
            question_data["topic"],
            datetime.now().isoformat()
        ))
    
    print(f"  📝 {len(questions)} questions créées pour le test {subject}")

def create_support_tables(cursor):
    """Créer les tables de support si elles n'existent pas"""
    
    # Table test_assignments
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS test_assignments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            test_id INTEGER NOT NULL,
            assignment_type TEXT NOT NULL CHECK (assignment_type IN ('class', 'individual')),
            target_id INTEGER NOT NULL,
            assigned_by INTEGER NOT NULL,
            assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            due_date TIMESTAMP,
            is_active INTEGER DEFAULT 1,
            FOREIGN KEY (test_id) REFERENCES adaptive_tests (id) ON DELETE CASCADE,
            FOREIGN KEY (assigned_by) REFERENCES users (id) ON DELETE CASCADE
        )
    """)
    
    # Table adaptive_test_responses
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS adaptive_test_responses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            test_id INTEGER NOT NULL,
            student_id INTEGER NOT NULL,
            status TEXT DEFAULT 'in_progress' CHECK (status IN ('not_started', 'in_progress', 'completed')),
            final_score REAL,
            questions_answered INTEGER DEFAULT 0,
            correct_answers INTEGER DEFAULT 0,
            start_time TIMESTAMP,
            completion_time TIMESTAMP,
            difficulty_adjustments INTEGER DEFAULT 0,
            FOREIGN KEY (test_id) REFERENCES adaptive_tests (id) ON DELETE CASCADE,
            FOREIGN KEY (student_id) REFERENCES users (id) ON DELETE CASCADE
        )
    """)
    
    # Table adaptive_test_performance
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS adaptive_test_performance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            test_id INTEGER NOT NULL,
            status TEXT DEFAULT 'not_started',
            final_score REAL,
            questions_answered INTEGER DEFAULT 0,
            correct_answers INTEGER DEFAULT 0,
            average_response_time REAL,
            difficulty_adjustments INTEGER DEFAULT 0,
            start_time TIMESTAMP,
            completion_time TIMESTAMP,
            FOREIGN KEY (student_id) REFERENCES users (id) ON DELETE CASCADE,
            FOREIGN KEY (test_id) REFERENCES adaptive_tests (id) ON DELETE CASCADE
        )
    """)
    
    print("  ✅ Tables de support créées")

def create_sample_assignments(cursor, teacher_id):
    """Créer des assignations de démonstration"""
    
    # Récupérer les classes de l'enseignant
    cursor.execute("""
        SELECT id FROM class_groups WHERE teacher_id = ?
    """, (teacher_id,))
    
    classes = cursor.fetchall()
    
    if not classes:
        print("  ⚠️ Aucune classe trouvée pour créer des assignations")
        return
    
    # Récupérer les tests créés
    cursor.execute("SELECT id FROM adaptive_tests WHERE created_by = ?", (teacher_id,))
    tests = cursor.fetchall()
    
    if not tests:
        print("  ⚠️ Aucun test trouvé pour créer des assignations")
        return
    
    # Créer quelques assignations de démonstration
    for i, test in enumerate(tests[:3]):  # Assigner les 3 premiers tests
        test_id = test[0]
        class_id = classes[i % len(classes)][0]  # Distribuer entre les classes
        
        cursor.execute("""
            INSERT INTO test_assignments (
                test_id, assignment_type, target_id, assigned_by, assigned_at, is_active
            ) VALUES (?, 'class', ?, ?, ?, 1)
        """, (test_id, class_id, teacher_id, datetime.now().isoformat()))
        
        print(f"  📋 Test {test_id} assigné à la classe {class_id}")
    
    print("  ✅ Assignations de démonstration créées")

if __name__ == "__main__":
    print("🚀 Script de création des tests adaptatifs de démonstration")
    print("=" * 60)
    
    success = create_sample_adaptive_tests()
    
    if success:
        print("\n🎉 Tests adaptatifs créés avec succès !")
        print("Vous pouvez maintenant accéder à la page d'évaluation adaptative.")
    else:
        print("\n❌ Échec de la création des tests adaptatifs")
        print("Vérifiez que les tables existent et que vous avez un utilisateur enseignant.")
