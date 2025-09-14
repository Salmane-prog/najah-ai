#!/usr/bin/env python3
"""
Script pour vérifier les tests créés récemment
"""

import sqlite3
import os
from datetime import datetime, timedelta

def check_recent_tests():
    # Chemin vers la base de données
    db_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'app.db')
    print(f"🔍 Vérification des tests récents")
    print(f"📁 Base de données: {db_path}")
    print("=" * 60)
    
    try:
        # Connexion à la base
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 1. Vérifier les tests créés dans les dernières 24h
        print("📅 Tests créés dans les dernières 24h:")
        yesterday = datetime.now() - timedelta(days=1)
        cursor.execute("""
            SELECT id, title, is_active, created_at, 
                   (SELECT COUNT(*) FROM adaptive_questions q WHERE q.test_id = t.id) as question_count
            FROM adaptive_tests t
            WHERE created_at > ?
            ORDER BY created_at DESC
        """, (yesterday,))
        
        recent_tests = cursor.fetchall()
        if recent_tests:
            for test in recent_tests:
                status = "✅ ACTIF" if test[2] else "❌ INACTIF"
                questions = "✅" if test[4] > 0 else "❌"
                print(f"  {questions} ID {test[0]}: {test[1]} - {status} - {test[4]} questions - Créé: {test[3]}")
        else:
            print("  Aucun test créé dans les dernières 24h")
        
        # 2. Vérifier tous les tests sans questions
        print(f"\n❌ Tests SANS questions:")
        cursor.execute("""
            SELECT t.id, t.title, t.is_active, t.created_at
            FROM adaptive_tests t
            LEFT JOIN adaptive_questions q ON t.id = q.test_id
            WHERE q.id IS NULL
            ORDER BY t.created_at DESC
        """)
        
        tests_without_questions = cursor.fetchall()
        if tests_without_questions:
            for test in tests_without_questions:
                status = "✅ ACTIF" if test[2] else "❌ INACTIF"
                print(f"  ID {test[0]}: {test[1]} - {status} - Créé: {test[3]}")
        else:
            print("  Tous les tests ont des questions ✅")
        
        # 3. Vérifier la table adaptive_questions
        print(f"\n🔍 Détail des questions:")
        cursor.execute("""
            SELECT test_id, COUNT(*) as count, 
                   SUM(CASE WHEN is_active = 1 THEN 1 ELSE 0 END) as active_count
            FROM adaptive_questions
            GROUP BY test_id
            ORDER BY test_id
        """)
        
        questions_detail = cursor.fetchall()
        for q in questions_detail:
            print(f"  Test {q[0]}: {q[1]} questions total, {q[2]} actives")
        
        conn.close()
        print("\n✅ Vérification terminée!")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_recent_tests()

