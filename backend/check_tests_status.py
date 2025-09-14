#!/usr/bin/env python3
"""
Script pour vérifier l'état des tests adaptatifs
"""

import sqlite3
import os

def check_tests_status():
    # Chemin vers la base de données
    db_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'app.db')
    print(f"🔍 Vérification de l'état des tests adaptatifs")
    print(f"📁 Base de données: {db_path}")
    print("=" * 60)
    
    try:
        # Connexion à la base
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 1. Vérifier la table adaptive_tests
        print("📋 Table adaptive_tests:")
        cursor.execute("PRAGMA table_info(adaptive_tests)")
        columns = cursor.fetchall()
        for col in columns:
            print(f"  - {col[1]} ({col[2]})")
        
        # 2. Compter les tests
        cursor.execute("SELECT COUNT(*) FROM adaptive_tests")
        tests_count = cursor.fetchone()[0]
        print(f"\n📊 Nombre total de tests: {tests_count}")
        
        # 3. Vérifier l'état des tests
        if tests_count > 0:
            print("\n🔍 État des tests:")
            cursor.execute("""
                SELECT id, title, is_active, created_at 
                FROM adaptive_tests 
                ORDER BY id
            """)
            tests = cursor.fetchall()
            for test in tests:
                status = "✅ ACTIF" if test[2] else "❌ INACTIF"
                print(f"  ID {test[0]}: {test[1]} - {status} - Créé: {test[3]}")
        
        # 4. Vérifier les questions
        print(f"\n📋 Table adaptive_questions:")
        cursor.execute("PRAGMA table_info(adaptive_questions)")
        q_columns = cursor.fetchall()
        for col in q_columns:
            print(f"  - {col[1]} ({col[2]})")
        
        cursor.execute("SELECT COUNT(*) FROM adaptive_questions")
        questions_count = cursor.fetchone()[0]
        print(f"\n📊 Nombre total de questions: {questions_count}")
        
        # 5. Vérifier l'état des questions
        if questions_count > 0:
            print("\n🔍 État des questions:")
            cursor.execute("""
                SELECT id, test_id, question_text[:50], is_active 
                FROM adaptive_questions 
                ORDER BY test_id, id
            """)
            questions = cursor.fetchall()
            for question in questions:
                status = "✅ ACTIVE" if question[3] else "❌ INACTIVE"
                text = question[2] + "..." if question[2] and len(question[2]) == 50 else question[2] or "N/A"
                print(f"  ID {question[0]} (Test {question[1]}): {text} - {status}")
        
        # 6. Test de requête simulée
        print(f"\n🧪 Test de requête simulée:")
        cursor.execute("""
            SELECT COUNT(*) 
            FROM adaptive_tests 
            WHERE is_active = 1
        """)
        active_tests = cursor.fetchone()[0]
        print(f"  Tests actifs (is_active = 1): {active_tests}")
        
        cursor.execute("""
            SELECT COUNT(*) 
            FROM adaptive_tests 
            WHERE is_active IS NULL
        """)
        null_tests = cursor.fetchone()[0]
        print(f"  Tests avec is_active NULL: {null_tests}")
        
        cursor.execute("""
            SELECT COUNT(*) 
            FROM adaptive_tests 
            WHERE is_active = 0
        """)
        inactive_tests = cursor.fetchone()[0]
        print(f"  Tests inactifs (is_active = 0): {inactive_tests}")
        
        conn.close()
        print("\n✅ Vérification terminée!")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_tests_status()















