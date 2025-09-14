#!/usr/bin/env python3
"""
Script pour activer tous les tests adaptatifs inactifs
"""

import sqlite3
import os

def activate_all_tests():
    # Chemin vers la base de données
    db_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'app.db')
    print(f"🔧 Activation de tous les tests adaptatifs")
    print(f"📁 Base de données: {db_path}")
    print("=" * 60)
    
    try:
        # Connexion à la base
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Vérifier l'état actuel
        cursor.execute("SELECT COUNT(*) FROM adaptive_tests WHERE is_active = 1")
        active_before = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM adaptive_tests WHERE is_active = 0")
        inactive_before = cursor.fetchone()[0]
        
        print(f"📊 État avant activation:")
        print(f"  ✅ Tests actifs: {active_before}")
        print(f"  ❌ Tests inactifs: {inactive_before}")
        
        # Activer tous les tests
        cursor.execute("UPDATE adaptive_tests SET is_active = 1 WHERE is_active = 0")
        updated_count = cursor.rowcount
        
        print(f"\n🔧 {updated_count} tests activés")
        
        # Vérifier l'état après activation
        cursor.execute("SELECT COUNT(*) FROM adaptive_tests WHERE is_active = 1")
        active_after = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM adaptive_tests WHERE is_active = 0")
        inactive_after = cursor.fetchone()[0]
        
        print(f"\n📊 État après activation:")
        print(f"  ✅ Tests actifs: {active_after}")
        print(f"  ❌ Tests inactifs: {inactive_after}")
        
        # Afficher la liste des tests maintenant actifs
        print(f"\n📋 Tests maintenant actifs:")
        cursor.execute("""
            SELECT id, title, subject, difficulty_min, difficulty_max, total_questions
            FROM adaptive_tests 
            WHERE is_active = 1
            ORDER BY id
        """)
        
        active_tests = cursor.fetchall()
        for test in active_tests:
            test_id, title, subject, diff_min, diff_max, total_q = test
            level = f"{diff_min}-{diff_max}" if diff_min and diff_max else "N/A"
            questions = str(total_q) if total_q else "0"
            print(f"  - ID {test_id}: {title} (Niveau {level}, {questions} questions)")
        
        # Valider les changements
        conn.commit()
        
        conn.close()
        print(f"\n✅ Activation terminée! {updated_count} tests activés.")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    activate_all_tests()
















