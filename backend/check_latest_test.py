#!/usr/bin/env python3
"""
Script pour vérifier le dernier test créé
"""

import sqlite3
import os
from datetime import datetime, timedelta

def check_latest_test():
    # Chemin vers la base de données
    db_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'app.db')
    print(f"🔍 Vérification du dernier test créé")
    print(f"📁 Base de données: {db_path}")
    print("=" * 60)
    
    try:
        # Connexion à la base
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 1. Vérifier le dernier test créé
        print("📋 Dernier test créé:")
        cursor.execute("""
            SELECT id, title, is_active, created_at, created_by
            FROM adaptive_tests 
            ORDER BY id DESC
            LIMIT 1
        """)
        
        latest_test = cursor.fetchone()
        if latest_test:
            test_id, title, is_active, created_at, created_by = latest_test
            status = "✅ ACTIF" if is_active else "❌ INACTIF"
            print(f"  ID {test_id}: {title}")
            print(f"  Statut: {status}")
            print(f"  Créé: {created_at}")
            print(f"  Créé par: {created_by}")
        else:
            print("  Aucun test trouvé")
            return
        
        # 2. Vérifier les questions de ce test
        print(f"\n🔍 Questions du test {test_id}:")
        cursor.execute("""
            SELECT id, question_text, question_type, is_active, difficulty_level
            FROM adaptive_questions 
            WHERE test_id = ?
            ORDER BY id
        """, (test_id,))
        
        questions = cursor.fetchall()
        if questions:
            print(f"  {len(questions)} questions trouvées:")
            for q in questions:
                q_id, q_text, q_type, q_active, q_diff = q
                status = "✅" if q_active else "❌"
                print(f"    {status} ID {q_id}: {q_text[:50]}... (Type: {q_type}, Niveau: {q_diff})")
        else:
            print("  ❌ AUCUNE QUESTION TROUVÉE !")
        
        # 3. Vérifier l'endpoint /tests/simple/ pour ce test
        print(f"\n🧪 Test de l'endpoint /tests/simple/ pour le test {test_id}:")
        cursor.execute("""
            SELECT 
                t.id,
                t.title,
                COUNT(q.id) as question_count
            FROM adaptive_tests t
            LEFT JOIN adaptive_questions q ON t.id = q.test_id AND q.is_active = 1
            WHERE t.id = ? AND t.is_active = 1
            GROUP BY t.id
        """, (test_id,))
        
        endpoint_result = cursor.fetchone()
        if endpoint_result:
            print(f"  ✅ Test trouvé dans l'endpoint: {endpoint_result[2]} questions")
        else:
            print(f"  ❌ Test NON trouvé dans l'endpoint !")
        
        # 4. Vérifier tous les tests dans l'endpoint
        print(f"\n📊 Tous les tests dans l'endpoint /tests/simple/:")
        cursor.execute("""
            SELECT 
                t.id,
                t.title,
                COUNT(q.id) as question_count
            FROM adaptive_tests t
            LEFT JOIN adaptive_questions q ON t.id = q.test_id AND q.is_active = 1
            WHERE t.is_active = 1
            GROUP BY t.id
            ORDER BY t.id DESC
        """)
        
        all_tests = cursor.fetchall()
        print(f"  {len(all_tests)} tests retournés:")
        for test in all_tests:
            print(f"    ID {test[0]}: {test[1]} - {test[2]} questions")
        
        conn.close()
        print(f"\n✅ Vérification terminée!")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_latest_test()















