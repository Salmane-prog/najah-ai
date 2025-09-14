#!/usr/bin/env python3
"""
Script pour vérifier les contraintes cachées, triggers et autres éléments
qui pourraient causer l'erreur NOT NULL
"""

import sqlite3
import os

def check_hidden_constraints():
    """Vérifie les contraintes cachées de la table"""
    
    # Chemin EXACT utilisé par le backend
    db_path = "F:/IMT/stage/Yancode/Najah__AI/data/app.db"
    
    print(f"🔍 Vérification des contraintes cachées: {db_path}")
    
    try:
        # Connexion à la base de données
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 1. Vérifier les triggers
        print("\n🔍 1. Vérification des triggers")
        cursor.execute("SELECT name, sql FROM sqlite_master WHERE type='trigger' AND tbl_name='french_adaptive_tests'")
        triggers = cursor.fetchall()
        
        if triggers:
            print("⚠️ Triggers trouvés sur french_adaptive_tests:")
            for trigger in triggers:
                print(f"   - {trigger[0]}: {trigger[1]}")
        else:
            print("✅ Aucun trigger trouvé")
        
        # 2. Vérifier les contraintes de vérification
        print("\n🔍 2. Vérification des contraintes CHECK")
        cursor.execute("PRAGMA table_info(french_adaptive_tests)")
        columns = cursor.fetchall()
        
        for col in columns:
            if col[1] == 'total_questions':
                print(f"   - total_questions: type={col[2]}, nullable={col[3]}, default={col[4]}, pk={col[5]}")
                if col[4]:  # default value
                    print(f"     Valeur par défaut: {col[4]}")
        
        # 3. Vérifier la définition complète de la table
        print("\n🔍 3. Définition complète de la table")
        cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='french_adaptive_tests'")
        table_def = cursor.fetchone()
        
        if table_def:
            print("📋 Définition SQL de la table:")
            print(f"   {table_def[0]}")
        else:
            print("❌ Table non trouvée")
        
        # 4. Vérifier les contraintes de clés étrangères
        print("\n🔍 4. Contraintes de clés étrangères")
        cursor.execute("PRAGMA foreign_key_list(french_adaptive_tests)")
        foreign_keys = cursor.fetchall()
        
        if foreign_keys:
            print("🔗 Clés étrangères trouvées:")
            for fk in foreign_keys:
                print(f"   - {fk}")
        else:
            print("✅ Aucune clé étrangère")
        
        # 5. Vérifier les index et leurs contraintes
        print("\n🔍 5. Index et leurs contraintes")
        cursor.execute("PRAGMA index_list(french_adaptive_tests)")
        indexes = cursor.fetchall()
        
        if indexes:
            print("📊 Index trouvés:")
            for idx in indexes:
                print(f"   - {idx}")
                # Vérifier les colonnes de l'index
                cursor.execute(f"PRAGMA index_info({idx[1]})")
                index_cols = cursor.fetchall()
                for col in index_cols:
                    print(f"     Colonne: {col}")
        else:
            print("✅ Aucun index")
        
        # 6. Test de création d'une table temporaire
        print("\n🔍 6. Test de création d'une table temporaire")
        try:
            cursor.execute("""
                CREATE TABLE temp_test (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    student_id INTEGER NOT NULL,
                    test_type TEXT NOT NULL,
                    current_question_index INTEGER DEFAULT 0,
                    total_questions INTEGER,
                    current_difficulty TEXT NOT NULL,
                    status TEXT DEFAULT 'in_progress',
                    started_at DATETIME,
                    completed_at DATETIME,
                    final_score REAL,
                    difficulty_progression TEXT
                )
            """)
            print("✅ Table temporaire créée avec succès")
            
            # Test d'insertion dans la table temporaire
            try:
                cursor.execute("""
                    INSERT INTO temp_test 
                    (student_id, test_type, current_question_index, total_questions, 
                     current_difficulty, status, started_at) 
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (999, 'test', 0, None, 'easy', 'in_progress', '2025-08-20 19:44:36.063345'))
                
                print("✅ Insertion réussie dans la table temporaire avec total_questions = NULL")
                
                # Supprimer la table temporaire
                cursor.execute("DROP TABLE temp_test")
                print("✅ Table temporaire supprimée")
                
            except Exception as e:
                print(f"❌ Échec insertion dans la table temporaire: {e}")
                
        except Exception as e:
            print(f"❌ Échec création de la table temporaire: {e}")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Erreur lors de la vérification: {e}")
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    check_hidden_constraints()











