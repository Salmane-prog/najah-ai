#!/usr/bin/env python3
"""
Script pour ajouter la colonne content_type manquante à la table contents
"""

import sqlite3
import os

def add_content_type_column():
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
        # Vérifier si la colonne content_type existe
        cursor.execute("PRAGMA table_info(contents)")
        columns = [col[1] for col in cursor.fetchall()]
        
        if 'content_type' in columns:
            print("La colonne 'content_type' existe déjà")
        else:
            print("Ajout de la colonne 'content_type'...")
            
            # Ajouter la colonne content_type
            cursor.execute("ALTER TABLE contents ADD COLUMN content_type VARCHAR(50) DEFAULT 'text'")
            
            print("Colonne 'content_type' ajoutée avec succès!")
            
            # Mettre à jour les enregistrements existants
            cursor.execute("UPDATE contents SET content_type = 'text' WHERE content_type IS NULL")
            
            print("Enregistrements existants mis à jour!")
        
        # Vérifier les colonnes après modification
        cursor.execute("PRAGMA table_info(contents)")
        columns = cursor.fetchall()
        print("Colonnes actuelles:")
        for col in columns:
            print(f"  - {col[1]} ({col[2]})")
        
        conn.commit()
        print("Opération terminée avec succès!")
        
    except Exception as e:
        print(f"Erreur: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    add_content_type_column() 