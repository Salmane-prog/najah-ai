#!/usr/bin/env python3
"""
Script pour créer un test adaptatif simple
"""

import sqlite3
import os
from datetime import datetime

def create_simple_test():
    # Chemin vers la base de données
    db_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'app.db')
    print(f"🔧 Création d'un test adaptatif simple")
    print(f"📁 Base de données: {db_path}")
    print("=" * 60)
    
    try:
        # Connexion à la base
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 1. Créer un test adaptatif
        print("📝 Création du test...")
        cursor.execute("""
            INSERT INTO adaptive_tests (
                title, subject, description, difficulty_min, difficulty_max,
                estimated_duration, adaptation_type, learning_objectives,
                is_active, created_by, created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            "Test de Mathématiques - Niveau Débutant",
            "Mathématiques",
            "Test adaptatif pour évaluer les compétences en mathématiques de base",
            1, 5, 30, "difficulty", "Addition, Soustraction, Multiplication",
            True, 33, datetime.now(), datetime.now()
        ))
        
        test_id = cursor.lastrowid
        print(f"✅ Test créé avec l'ID: {test_id}")
        
        # 2. Créer des questions
        questions = [
            {
                "text": "Quel est le résultat de 5 + 3 ?",
                "type": "multiple_choice",
                "difficulty": 1,
                "options": '["5", "6", "7", "8"]',
                "correct": "8",
                "explanation": "5 + 3 = 8",
                "order": 1,
                "objective": "Addition simple"
            },
            {
                "text": "Combien font 10 - 4 ?",
                "type": "multiple_choice", 
                "difficulty": 1,
                "options": '["4", "5", "6", "7"]',
                "correct": "6",
                "explanation": "10 - 4 = 6",
                "order": 2,
                "objective": "Soustraction simple"
            },
            {
                "text": "Quel est le résultat de 2 × 6 ?",
                "type": "multiple_choice",
                "difficulty": 2,
                "options": '["8", "10", "12", "14"]',
                "correct": "12",
                "explanation": "2 × 6 = 12",
                "order": 3,
                "objective": "Multiplication simple"
            }
        ]
        
        print(f"\n📝 Création des questions...")
        for i, q in enumerate(questions):
            cursor.execute("""
                INSERT INTO adaptive_questions (
                    test_id, question_text, question_type, difficulty_level,
                    options, correct_answer, explanation, question_order,
                    learning_objective, is_active
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                test_id, q["text"], q["type"], q["difficulty"],
                q["options"], q["correct"], q["explanation"], q["order"],
                q["objective"], True
            ))
            print(f"✅ Question {i+1} créée")
        
        # Valider les changements
        conn.commit()
        
        # Vérifier
        cursor.execute("SELECT COUNT(*) FROM adaptive_tests")
        tests_count = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM adaptive_questions")
        questions_count = cursor.fetchone()[0]
        
        print(f"\n📊 Résultat:")
        print(f"  - Tests: {tests_count}")
        print(f"  - Questions: {questions_count}")
        
        conn.close()
        print("\n✅ Test créé avec succès!")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    create_simple_test()


















