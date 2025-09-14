#!/usr/bin/env python3
"""
Script pour vérifier les résultats des tests dans la base de données
"""

import sqlite3
import os

def check_test_results():
    """Vérifier les résultats des tests"""
    
    # Chemin vers la base de données
    db_path = os.path.join(os.path.dirname(__file__), 'data', 'app.db')
    
    if not os.path.exists(db_path):
        print(f"❌ Base de données non trouvée: {db_path}")
        return
    
    # Connexion à la base de données
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        print("🔍 Vérification des résultats des tests...")
        
        # Vérifier la table test_attempts
        cursor.execute("SELECT * FROM test_attempts ORDER BY id DESC LIMIT 5")
        attempts = cursor.fetchall()
        
        print(f"\n📋 Dernières tentatives de test:")
        for attempt in attempts:
            print(f"  - ID: {attempt[0]}, Test: {attempt[1]}, Étudiant: {attempt[2]}, Status: {attempt[5]}, Score: {attempt[7]}/{attempt[8]}")
        
        # Vérifier les réponses aux questions
        cursor.execute("SELECT * FROM question_responses ORDER BY id DESC LIMIT 10")
        responses = cursor.fetchall()
        
        print(f"\n📋 Dernières réponses aux questions:")
        for response in responses:
            print(f"  - ID: {response[0]}, Tentative: {response[1]}, Question: {response[2]}, Correct: {response[4]}, Score: {response[5]}")
        
        # Vérifier les assignations de tests
        cursor.execute("SELECT * FROM test_assignments ORDER BY id DESC LIMIT 5")
        assignments = cursor.fetchall()
        
        print(f"\n📋 Dernières assignations de tests:")
        for assignment in assignments:
            print(f"  - ID: {assignment[0]}, Test: {assignment[1]}, Type: {assignment[2]}, Cible: {assignment[3]}, Status: {assignment[6]}")
        
        # Vérifier les tests adaptatifs
        cursor.execute("SELECT * FROM adaptive_tests ORDER BY id DESC LIMIT 5")
        tests = cursor.fetchall()
        
        print(f"\n📋 Derniers tests adaptatifs:")
        for test in tests:
            print(f"  - ID: {test[0]}, Titre: {test[1]}, Matière: {test[2]}, Actif: {test[11]}")
            
    except Exception as e:
        print(f"❌ Erreur lors de la vérification: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    check_test_results()








