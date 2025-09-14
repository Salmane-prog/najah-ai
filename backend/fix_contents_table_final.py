#!/usr/bin/env python3
"""
Script pour ajouter toutes les colonnes manquantes à la table contents (version corrigée)
"""

import sqlite3
import os
from datetime import datetime

def fix_contents_table_final():
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
        
        # Colonnes manquantes à ajouter (sans CURRENT_TIMESTAMP)
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
        
        # Ajouter chaque colonne manquante
        for column_name, column_def in missing_columns:
            if column_name not in existing_columns:
                print(f"Ajout de la colonne '{column_name}'...")
                cursor.execute(f"ALTER TABLE contents ADD COLUMN {column_name} {column_def}")
                print(f"Colonne '{column_name}' ajoutée avec succès!")
            else:
                print(f"Colonne '{column_name}' existe déjà")
        
        # Mettre à jour les enregistrements existants avec des timestamps
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute("UPDATE contents SET created_at = ?, updated_at = ? WHERE created_at IS NULL", 
                      (current_time, current_time))
        print("Timestamps mis à jour pour les enregistrements existants!")
        
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
    fix_contents_table_final() 