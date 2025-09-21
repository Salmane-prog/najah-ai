#!/usr/bin/env python3
"""
Script pour créer un vrai test avec les bonnes valeurs (CORRECTION FINALE)
"""

import sqlite3
import os
import json
from datetime import datetime

def create_real_test_final():
    # Chemin vers la base de données
    db_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'app.db')
    print(f"🚀 Création d'un vrai test (CORRECTION FINALE)")
    print(f"📁 Base de données: {db_path}")
    print("=" * 60)
    
    try:
        # Connexion à la base
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 1. Créer un nouveau test
        test_title = f"Test Réel Créé - {datetime.now().strftime('%H:%M:%S')}"
        print(f"📝 Création du test: {test_title}")
        
        cursor.execute("""
            INSERT INTO adaptive_tests (
                title, subject, description, difficulty_min, difficulty_max,
                estimated_duration, adaptation_type, learning_objectives,
                is_active, created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            test_title,
            "Test Manuel",
            "Test créé manuellement pour vérifier l'affichage",
            1, 5, 20, "difficulty", "Vérifier le système",
            1, datetime.now(), datetime.now()
        ))
        
        test_id = cursor.lastrowid
        print(f"✅ Test créé avec l'ID: {test_id}")
        
        # 2. Créer des questions avec les BONNES valeurs pour cognitive_level
        questions_data = [
            {
                "question_text": "Quelle est la capitale de la France?",
                "question_type": "multiple_choice",
                "options": json.dumps(["Paris", "Londres", "Berlin", "Madrid"]),
                "correct_answer": "Paris",
                "explanation": "C'est la capitale de la France",
                "difficulty_level": 1,
                "topic": "Géographie",
                "cognitive_level": "remember"  # ✅ Valeur valide
            },
            {
                "question_text": "Combien font 2 + 2?",
                "question_type": "multiple_choice",
                "options": json.dumps(["3", "4", "5", "6"]),
                "correct_answer": "4",
                "explanation": "Opération mathématique simple",
                "difficulty_level": 1,
                "topic": "Mathématiques",
                "cognitive_level": "apply"  # ✅ Valeur valide
            },
            {
                "question_text": "Quel est le symbole chimique de l'eau?",
                "question_type": "multiple_choice",
                "options": json.dumps(["H2O", "CO2", "O2", "N2"]),
                "correct_answer": "H2O",
                "explanation": "Formule chimique de l'eau",
                "difficulty_level": 2,
                "topic": "Chimie",
                "cognitive_level": "understand"  # ✅ Valeur valide
            }
        ]
        
        print(f"\n🔍 Création de {len(questions_data)} questions (avec les bonnes valeurs):")
        for i, q_data in enumerate(questions_data, 1):
            cursor.execute("""
                INSERT INTO adaptive_questions (
                    test_id, question_text, question_type, options, correct_answer,
                    explanation, difficulty_level, topic, cognitive_level,
                    question_order, is_active
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                test_id,
                q_data["question_text"],
                q_data["question_type"],
                q_data["options"],
                q_data["correct_answer"],
                q_data["explanation"],
                q_data["difficulty_level"],
                q_data["topic"],
                q_data["cognitive_level"],  # ✅ Maintenant avec les bonnes valeurs
                i,  # question_order
                1   # is_active
            ))
            print(f"  ✅ Question {i}: {q_data['question_text'][:30]}...")
        
        # 3. Valider les changements
        conn.commit()
        print(f"\n💾 Changements sauvegardés dans la base")
        
        # 4. Vérifier que le test est bien créé
        print(f"\n🔍 Vérification du test créé:")
        cursor.execute("""
            SELECT t.id, t.title, t.is_active, COUNT(q.id) as question_count
            FROM adaptive_tests t
            LEFT JOIN adaptive_questions q ON t.id = q.test_id
            WHERE t.id = ?
            GROUP BY t.id
        """, (test_id,))
        
        test_info = cursor.fetchone()
        if test_info:
            status = "✅ ACTIF" if test_info[2] else "❌ INACTIF"
            print(f"  ID {test_info[0]}: {test_info[1]} - {status} - {test_info[3]} questions")
        
        # 5. Vérifier l'endpoint /tests/simple/ maintenant
        print(f"\n🧪 Test de l'endpoint /tests/simple/ après création:")
        cursor.execute("""
            SELECT 
                t.id,
                t.title,
                COUNT(q.id) as question_count
            FROM adaptive_tests t
            LEFT JOIN adaptive_questions q ON t.id = q.test_id AND q.is_active = 1
            WHERE t.is_active = 1
            GROUP BY t.id
            ORDER BY t.id
        """)
        
        endpoint_results = cursor.fetchall()
        print(f"  Résultats de l'endpoint: {len(endpoint_results)} tests")
        for result in endpoint_results:
            print(f"    ID {result[0]}: {result[1]} - {result[2]} questions")
        
        conn.close()
        print(f"\n✅ Test créé avec succès!")
        print(f"🎯 Maintenant va sur le frontend et rafraîchis la page!")
        print(f"   Le test '{test_title}' devrait apparaître!")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    create_real_test_final()


















