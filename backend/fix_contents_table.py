#!/usr/bin/env python3
"""
Script pour ajouter toutes les colonnes manquantes à la table contents
"""

import sqlite3
import os

def fix_contents_table():
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
        # Vérifier les colonnes existantes
        cursor.execute("PRAGMA table_info(contents)")
        existing_columns = [col[1] for col in cursor.fetchall()]
        print("Colonnes existantes:", existing_columns)
        
        # Colonnes manquantes à ajouter
        missing_columns = [
            ("difficulty", "FLOAT DEFAULT 1.0"),
            ("estimated_time", "INTEGER DEFAULT 15"),
            ("content_data", "TEXT"),
            ("thumbnail_url", "VARCHAR(500)"),
            ("tags", "TEXT"),
            ("learning_objectives", "TEXT"),
            ("prerequisites", "TEXT"),
            ("skills_targeted", "TEXT"),
            ("created_at", "DATETIME DEFAULT CURRENT_TIMESTAMP"),
            ("updated_at", "DATETIME DEFAULT CURRENT_TIMESTAMP"),
            ("is_active", "BOOLEAN DEFAULT 1")
        ]
        
        # Ajouter chaque colonne manquante
        for column_name, column_def in missing_columns:
            if column_name not in existing_columns:
                print(f"Ajout de la colonne '{column_name}'...")
                cursor.execute(f"ALTER TABLE contents ADD COLUMN {column_name} {column_def}")
                print(f"Colonne '{column_name}' ajoutée avec succès!")
            else:
                print(f"Colonne '{column_name}' existe déjà")
        
        # Vérifier les colonnes après modification
        cursor.execute("PRAGMA table_info(contents)")
        columns = cursor.fetchall()
        print("\nColonnes finales:")
        for col in columns:
            print(f"  - {col[1]} ({col[2]})")
        
        conn.commit()
        print("\nOpération terminée avec succès!")
        
    except Exception as e:
        print(f"Erreur: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    fix_contents_table() 