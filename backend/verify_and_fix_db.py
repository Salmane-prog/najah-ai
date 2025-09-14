#!/usr/bin/env python3
"""
Script pour vérifier et corriger la base de données
"""

import sqlite3
import os

def verify_and_fix_db():
    # Chemin vers la base de données
    db_path = "data/app.db"
    
    # Vérifier si la base de données existe
    if not os.path.exists(db_path):
        print(f"Base de données non trouvée: {db_path}")
        return
    
    # Connexion à la base de données
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        print("=== VÉRIFICATION DE LA TABLE CONTENTS ===")
        
        # Vérifier les colonnes existantes
        cursor.execute("PRAGMA table_info(contents)")
        columns = cursor.fetchall()
        print("Colonnes actuelles:")
        for col in columns:
            print(f"  - {col[1]} ({col[2]})")
        
        # Vérifier si content_type existe
        column_names = [col[1] for col in columns]
        if 'content_type' not in column_names:
            print("\n❌ ERREUR: La colonne 'content_type' n'existe pas!")
            print("Ajout de la colonne 'content_type'...")
            cursor.execute("ALTER TABLE contents ADD COLUMN content_type VARCHAR(50) DEFAULT 'text'")
            print("✅ Colonne 'content_type' ajoutée!")
        else:
            print("\n✅ La colonne 'content_type' existe déjà")
        
        # Vérifier les autres colonnes manquantes
        missing_columns = [
            ("difficulty", "FLOAT DEFAULT 1.0"),
            ("estimated_time", "INTEGER DEFAULT 15"),
            ("content_data", "TEXT"),
            ("thumbnail_url", "VARCHAR(500)"),
            ("tags", "TEXT"),
            ("learning_objectives", "TEXT"),
            ("prerequisites", "TEXT"),
            ("skills_targeted", "TEXT"),
            ("created_at", "DATETIME"),
            ("updated_at", "DATETIME"),
            ("is_active", "BOOLEAN DEFAULT 1")
        ]
        
        print("\n=== AJOUT DES COLONNES MANQUANTES ===")
        for column_name, column_def in missing_columns:
            if column_name not in column_names:
                print(f"Ajout de la colonne '{column_name}'...")
                cursor.execute(f"ALTER TABLE contents ADD COLUMN {column_name} {column_def}")
                print(f"✅ Colonne '{column_name}' ajoutée!")
            else:
                print(f"✅ Colonne '{column_name}' existe déjà")
        
        # Mettre à jour les enregistrements existants
        print("\n=== MISE À JOUR DES DONNÉES ===")
        cursor.execute("UPDATE contents SET content_type = 'text' WHERE content_type IS NULL")
        cursor.execute("UPDATE contents SET difficulty = 1.0 WHERE difficulty IS NULL")
        cursor.execute("UPDATE contents SET estimated_time = 15 WHERE estimated_time IS NULL")
        cursor.execute("UPDATE contents SET is_active = 1 WHERE is_active IS NULL")
        
        # Ajouter des timestamps si manquants
        from datetime import datetime
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute("UPDATE contents SET created_at = ?, updated_at = ? WHERE created_at IS NULL", 
                      (current_time, current_time))
        
        print("✅ Données mises à jour!")
        
        # Vérification finale
        print("\n=== VÉRIFICATION FINALE ===")
        cursor.execute("PRAGMA table_info(contents)")
        final_columns = cursor.fetchall()
        print("Colonnes finales:")
        for col in final_columns:
            print(f"  - {col[1]} ({col[2]})")
        
        # Test d'une requête simple
        print("\n=== TEST DE REQUÊTE ===")
        cursor.execute("SELECT COUNT(*) FROM contents")
        count = cursor.fetchone()[0]
        print(f"Nombre d'enregistrements dans contents: {count}")
        
        if count > 0:
            cursor.execute("SELECT id, title, content_type FROM contents LIMIT 3")
            rows = cursor.fetchall()
            print("Exemples d'enregistrements:")
            for row in rows:
                print(f"  - ID: {row[0]}, Title: {row[1]}, Type: {row[2]}")
        
        conn.commit()
        print("\n🎉 Opération terminée avec succès!")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    verify_and_fix_db() 