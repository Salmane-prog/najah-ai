#!/usr/bin/env python3
"""
Script pour vérifier pourquoi le nouveau test n'apparaît pas
"""

import sqlite3
import os

def check_new_test():
    # Chemin vers la base de données
    db_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'app.db')
    print(f"🔍 Vérification du nouveau test créé")
    print(f"📁 Base de données: {db_path}")
    print("=" * 60)
    
    try:
        # Connexion à la base
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 1. Vérifier tous les tests (du plus récent au plus ancien)
        print("📋 Tous les tests (du plus récent au plus ancien):")
        cursor.execute("""
            SELECT id, title, is_active, created_at 
            FROM adaptive_tests 
            ORDER BY id DESC
        """)
        tests = cursor.fetchall()
        for test in tests:
            status = "✅ ACTIF" if test[2] else "❌ INACTIF"
            print(f"  ID {test[0]}: {test[1]} - {status} - Créé: {test[3]}")
        
        # 2. Vérifier les tests actifs vs inactifs
        print(f"\n📊 Statistiques des tests:")
        cursor.execute("SELECT COUNT(*) FROM adaptive_tests WHERE is_active = 1")
        active_tests = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM adaptive_tests WHERE is_active = 0")
        inactive_tests = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM adaptive_tests WHERE is_active IS NULL")
        null_tests = cursor.fetchone()[0]
        
        print(f"  Tests actifs (is_active = 1): {active_tests}")
        print(f"  Tests inactifs (is_active = 0): {inactive_tests}")
        print(f"  Tests avec is_active NULL: {null_tests}")
        
        # 3. Vérifier les questions par test
        print(f"\n🔍 Questions par test:")
        cursor.execute("""
            SELECT t.id, t.title, COUNT(q.id) as question_count
            FROM adaptive_tests t
            LEFT JOIN adaptive_questions q ON t.id = q.test_id
            GROUP BY t.id, t.title
            ORDER BY t.id DESC
        """)
        questions_per_test = cursor.fetchall()
        for test in questions_per_test:
            status = "✅" if test[2] > 0 else "❌"
            print(f"  {status} Test {test[0]}: {test[1]} - {test[2]} questions")
        
        # 4. Vérifier l'endpoint /tests/simple/ exactement
        print(f"\n🧪 Test de l'endpoint /tests/simple/ exactement:")
        cursor.execute("""
            SELECT 
                t.id,
                t.title,
                t.subject,
                t.description,
                t.difficulty_min,
                t.difficulty_max,
                t.estimated_duration,
                t.adaptation_type,
                t.learning_objectives,
                t.is_active,
                t.created_by,
                t.created_at,
                t.updated_at,
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
            print(f"    ID {result[0]}: {result[1]} - {result[13]} questions")
        
        conn.close()
        print("\n✅ Vérification terminée!")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_new_test()















