#!/usr/bin/env python3
"""
Script pour ajouter la colonne type à la table threads
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import text
from core.database import engine

def add_thread_type_column():
    """Ajouter la colonne type à la table threads."""
    try:
        with engine.connect() as conn:
            # Vérifier si la colonne existe déjà
            result = conn.execute(text("""
                SELECT name FROM pragma_table_info('threads') 
                WHERE name = 'type'
            """))
            
            if result.fetchone():
                print("La colonne type existe déjà.")
                return
            
            # Ajouter la colonne type
            conn.execute(text("""
                ALTER TABLE threads 
                ADD COLUMN type TEXT
            """))
            
            conn.commit()
            print("✅ Colonne type ajoutée avec succès !")
            
    except Exception as e:
        print(f"Erreur lors de l'ajout de la colonne type: {str(e)}")

if __name__ == "__main__":
    add_thread_type_column() 