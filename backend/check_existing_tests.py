#!/usr/bin/env python3
"""
Script pour vérifier les tests existants dans la base de données
"""

import sqlite3
import os
import json

def check_existing_tests():
    """Vérifie les tests existants dans la base de données"""
    
    # Chemin vers la base de données
    db_path = os.path.join(os.path.dirname(__file__), "..", "data", "app.db")
    
    if not os.path.exists(db_path):
        print(f"❌ Base de données {db_path} non trouvée!")
        return
    
    print(f"🔍 Vérification des tests existants dans: {db_path}")
    print("=" * 60)
    
    try:
        # Connexion à la base
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Vérifier la structure de la table adaptive_tests
        print("📋 Structure de la table 'adaptive_tests':")
        cursor.execute("PRAGMA table_info(adaptive_tests);")
        columns = cursor.fetchall()
        
        for col in columns:
            col_id, name, type_name, not_null, default_val, pk = col
            print(f"  - {name}: {type_name} {'NOT NULL' if not_null else 'NULL'} {'PK' if pk else ''}")
        
        print("\n" + "=" * 60)
        
        # Compter les tests
        cursor.execute("SELECT COUNT(*) FROM adaptive_tests;")
        test_count = cursor.fetchone()[0]
        print(f"📊 Nombre total de tests: {test_count}")
        
        if test_count > 0:
            print("\n🔍 Détails des tests existants:")
            print("-" * 40)
            
            # Récupérer tous les tests avec leurs détails
            cursor.execute("""
                SELECT id, title, subject, description, difficulty_min, difficulty_max,
                       estimated_duration, total_questions, adaptation_type, learning_objectives,
                       is_active, created_by, created_at, updated_at
                FROM adaptive_tests
                ORDER BY id
            """)
            
            tests = cursor.fetchall()
            
            for test in tests:
                test_id, title, subject, description, diff_min, diff_max, duration, questions, \
                adapt_type, objectives, active, created_by, created_at, updated_at = test
                
                print(f"\n📝 Test ID: {test_id}")
                print(f"   Titre: {title}")
                print(f"   Matière: {subject}")
                print(f"   Description: {description[:50]}{'...' if description and len(description) > 50 else ''}")
                print(f"   Difficulté: {diff_min}-{diff_max}")
                print(f"   Durée: {duration} min")
                print(f"   Questions: {questions}")
                print(f"   Type d'adaptation: {adapt_type}")
                print(f"   Actif: {'✅ Oui' if active else '❌ Non'}")
                print(f"   Créé par: {created_by}")
                print(f"   Créé le: {created_at}")
                print(f"   Modifié le: {updated_at}")
                
                # Vérifier les questions de ce test
                cursor.execute("SELECT COUNT(*) FROM adaptive_questions WHERE test_id = ?", (test_id,))
                question_count = cursor.fetchone()[0]
                print(f"   Questions en base: {question_count}")
                
                if question_count > 0:
                    cursor.execute("""
                        SELECT id, question_text, question_type, difficulty_level, 
                               learning_objective, is_active
                        FROM adaptive_questions 
                        WHERE test_id = ? 
                        ORDER BY question_order
                        LIMIT 3
                    """, (test_id,))
                    
                    questions = cursor.fetchall()
                    print(f"   Aperçu des questions:")
                    for q in questions:
                        q_id, q_text, q_type, q_diff, q_obj, q_active = q
                        print(f"     - Q{q_id}: {q_text[:40]}{'...' if len(q_text) > 40 else ''} ({q_type}, Niveau {q_diff})")
                    
                    if question_count > 3:
                        print(f"     ... et {question_count - 3} autres questions")
        
        # Vérifier la table adaptive_questions
        print("\n" + "=" * 60)
        print("🔍 Vérification de la table 'adaptive_questions':")
        
        cursor.execute("SELECT COUNT(*) FROM adaptive_questions;")
        total_questions = cursor.fetchone()[0]
        print(f"📊 Nombre total de questions: {total_questions}")
        
        if total_questions > 0:
            cursor.execute("""
                SELECT test_id, COUNT(*) as question_count
                FROM adaptive_questions
                GROUP BY test_id
                ORDER BY test_id
            """)
            
            question_distribution = cursor.fetchall()
            print(f"\n📋 Distribution des questions par test:")
            for test_id, count in question_distribution:
                print(f"  - Test {test_id}: {count} questions")
        
        # Vérifier la table users
        print("\n" + "=" * 60)
        print("🔍 Vérification de la table 'users':")
        
        cursor.execute("SELECT COUNT(*) FROM users;")
        user_count = cursor.fetchone()[0]
        print(f"📊 Nombre total d'utilisateurs: {user_count}")
        
        if user_count > 0:
            cursor.execute("""
                SELECT id, username, email, role, is_active, first_name, last_name
                FROM users
                ORDER BY id
                LIMIT 5
            """)
            
            users = cursor.fetchall()
            print(f"\n📋 Aperçu des utilisateurs:")
            for user in users:
                user_id, username, email, role, active, first_name, last_name = user
                print(f"  - ID {user_id}: {first_name} {last_name} ({email}) - Rôle: {role} - Actif: {'✅' if active else '❌'}")
            
            if user_count > 5:
                print(f"  ... et {user_count - 5} autres utilisateurs")
        
        conn.close()
        print("\n✅ Vérification terminée!")
        
    except Exception as e:
        print(f"❌ Erreur lors de la vérification: {e}")
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    check_existing_tests()


















