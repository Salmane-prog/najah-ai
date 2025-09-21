#!/usr/bin/env python3
"""
Script pour tester directement l'insertion dans la base de données
et identifier le vrai problème
"""

import sqlite3
import os

def test_database_insert():
    """Teste directement l'insertion qui échoue"""
    
    # Chemin EXACT utilisé par le backend
    db_path = "F:/IMT/stage/Yancode/Najah__AI/data/app.db"
    
    print(f"🧪 Test direct de la base de données: {db_path}")
    
    try:
        # Connexion à la base de données
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Vérifier la structure actuelle de la table
        cursor.execute("PRAGMA table_info(french_adaptive_tests)")
        columns = cursor.fetchall()
        
        print("📋 Structure actuelle de la table french_adaptive_tests:")
        for col in columns:
            print(f"  - {col[1]} ({col[2]}) - nullable: {col[3]}")
        
        # Test 1: Insertion avec total_questions = NULL
        print("\n🧪 Test 1: Insertion avec total_questions = NULL")
        try:
            cursor.execute("""
                INSERT INTO french_adaptive_tests 
                (student_id, test_type, current_question_index, total_questions, 
                 current_difficulty, status, started_at) 
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (999, 'test', 0, None, 'easy', 'in_progress', '2025-08-20 19:44:36.063345'))
            
            print("✅ Insertion réussie avec total_questions = NULL")
            
            # Récupérer l'ID inséré
            test_id = cursor.lastrowid
            print(f"   ID inséré: {test_id}")
            
            # Supprimer le test de test
            cursor.execute("DELETE FROM french_adaptive_tests WHERE id = ?", (test_id,))
            print("   Test supprimé")
            
        except Exception as e:
            print(f"❌ Échec insertion avec total_questions = NULL: {e}")
        
        # Test 2: Insertion avec total_questions = 10
        print("\n🧪 Test 2: Insertion avec total_questions = 10")
        try:
            cursor.execute("""
                INSERT INTO french_adaptive_tests 
                (student_id, test_type, current_question_index, total_questions, 
                 current_difficulty, status, started_at) 
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (999, 'test', 0, 10, 'easy', 'in_progress', '2025-08-20 19:44:36.063345'))
            
            print("✅ Insertion réussie avec total_questions = 10")
            
            # Récupérer l'ID inséré
            test_id = cursor.lastrowid
            print(f"   ID inséré: {test_id}")
            
            # Supprimer le test de test
            cursor.execute("DELETE FROM french_adaptive_tests WHERE id = ?", (test_id,))
            print("   Test supprimé")
            
        except Exception as e:
            print(f"❌ Échec insertion avec total_questions = 10: {e}")
        
        # Test 3: Vérifier les contraintes de la table
        print("\n🧪 Test 3: Vérification des contraintes")
        cursor.execute("PRAGMA foreign_key_list(french_adaptive_tests)")
        foreign_keys = cursor.fetchall()
        
        if foreign_keys:
            print("🔗 Contraintes de clés étrangères trouvées:")
            for fk in foreign_keys:
                print(f"   - {fk}")
        else:
            print("✅ Aucune contrainte de clé étrangère")
        
        # Test 4: Vérifier les index
        print("\n🧪 Test 4: Vérification des index")
        cursor.execute("PRAGMA index_list(french_adaptive_tests)")
        indexes = cursor.fetchall()
        
        if indexes:
            print("📊 Index trouvés:")
            for idx in indexes:
                print(f"   - {idx}")
        else:
            print("✅ Aucun index")
        
        conn.commit()
        conn.close()
        
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    test_database_insert()














