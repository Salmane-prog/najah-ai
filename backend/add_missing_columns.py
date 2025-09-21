#!/usr/bin/env python3
"""
Script pour ajouter les colonnes manquantes à la table adaptive_tests
"""

import sqlite3
import json

def add_missing_columns():
    """Ajouter les colonnes manquantes"""
    try:
        conn = sqlite3.connect('./data/app.db')
        cursor = conn.cursor()
        
        print("🔧 Ajout des colonnes manquantes à adaptive_tests...")
        print("=" * 50)
        
        # Vérifier les colonnes existantes
        cursor.execute("PRAGMA table_info(adaptive_tests)")
        existing_columns = [col[1] for col in cursor.fetchall()]
        print(f"📋 Colonnes existantes: {existing_columns}")
        
        # Colonnes à ajouter
        columns_to_add = [
            ("difficulty_range", "TEXT", '{"min": 1, "max": 10}'),
            ("question_pool_size", "INTEGER", "100"),
            ("adaptation_algorithm", "TEXT", "irt"),
            ("created_by", "INTEGER", "1"),  # Valeur par défaut
            ("updated_at", "DATETIME", "CURRENT_TIMESTAMP")
        ]
        
        added_columns = []
        for col_name, col_type, default_value in columns_to_add:
            if col_name not in existing_columns:
                try:
                    if col_type == "TEXT" and col_name == "difficulty_range":
                        # Pour difficulty_range, on utilise JSON
                        cursor.execute(f"ALTER TABLE adaptive_tests ADD COLUMN {col_name} TEXT DEFAULT '{default_value}'")
                    elif col_type == "INTEGER":
                        cursor.execute(f"ALTER TABLE adaptive_tests ADD COLUMN {col_name} INTEGER DEFAULT {default_value}")
                    elif col_type == "DATETIME":
                        cursor.execute(f"ALTER TABLE adaptive_tests ADD COLUMN {col_name} DATETIME DEFAULT {default_value}")
                    else:
                        cursor.execute(f"ALTER TABLE adaptive_tests ADD COLUMN {col_name} {col_type} DEFAULT '{default_value}'")
                    
                    added_columns.append(col_name)
                    print(f"✅ Colonne {col_name} ajoutée")
                except Exception as e:
                    print(f"❌ Erreur lors de l'ajout de {col_name}: {e}")
            else:
                print(f"ℹ️ Colonne {col_name} existe déjà")
        
        # Mettre à jour les données existantes
        if "created_by" in added_columns:
            print("🔄 Mise à jour des tests existants avec created_by=1...")
            cursor.execute("UPDATE adaptive_tests SET created_by = 1 WHERE created_by IS NULL")
            print("✅ Tests existants mis à jour")
        
        # Vérifier le résultat final
        cursor.execute("PRAGMA table_info(adaptive_tests)")
        final_columns = [col[1] for col in cursor.fetchall()]
        print(f"\n📋 Colonnes finales: {final_columns}")
        
        # Vérifier les données
        cursor.execute("SELECT COUNT(*) FROM adaptive_tests")
        test_count = cursor.fetchone()[0]
        print(f"📊 Nombre de tests dans la base: {test_count}")
        
        if test_count > 0:
            cursor.execute("SELECT id, title, created_by FROM adaptive_tests LIMIT 3")
            sample_tests = cursor.fetchall()
            print("🔍 Exemple de tests:")
            for test in sample_tests:
                print(f"  - ID: {test[0]}, Titre: {test[1]}, Créé par: {test[2]}")
        
        conn.commit()
        conn.close()
        
        print("\n" + "=" * 50)
        if added_columns:
            print(f"✅ {len(added_columns)} colonnes ajoutées avec succès: {added_columns}")
        else:
            print("✅ Toutes les colonnes nécessaires existent déjà")
        
    except Exception as e:
        print(f"❌ Erreur lors de la mise à jour: {e}")
        if 'conn' in locals():
            conn.rollback()
            conn.close()

if __name__ == "__main__":
    add_missing_columns()























