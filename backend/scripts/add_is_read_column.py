#!/usr/bin/env python3
"""
Script pour ajouter la colonne is_read à la table messages
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import text
from core.database import engine

def add_is_read_column():
    """Ajouter la colonne is_read à la table messages."""
    try:
        with engine.connect() as conn:
            # Vérifier si la colonne existe déjà
            result = conn.execute(text("""
                SELECT name FROM pragma_table_info('messages') 
                WHERE name = 'is_read'
            """))
            
            if result.fetchone():
                print("La colonne is_read existe déjà.")
                return
            
            # Ajouter la colonne is_read
            conn.execute(text("""
                ALTER TABLE messages 
                ADD COLUMN is_read BOOLEAN DEFAULT FALSE
            """))
            
            conn.commit()
            print("✅ Colonne is_read ajoutée avec succès !")
            
    except Exception as e:
        print(f"Erreur lors de l'ajout de la colonne is_read: {str(e)}")

if __name__ == "__main__":
    add_is_read_column() 