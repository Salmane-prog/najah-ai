#!/usr/bin/env python3
"""
Script pour ajouter la colonne category_id à la table threads
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.database import engine
from sqlalchemy import text

def fix_threads_table():
    """Ajouter la colonne category_id à la table threads"""
    try:
        with engine.connect() as conn:
            # Vérifier si la colonne existe déjà
            result = conn.execute(text("PRAGMA table_info(threads)"))
            columns = [row[1] for row in result]
            
            if 'category_id' not in columns:
                print("Ajout de la colonne category_id à la table threads...")
                conn.execute(text("ALTER TABLE threads ADD COLUMN category_id INTEGER"))
                conn.commit()
                print("✅ Colonne category_id ajoutée avec succès !")
            else:
                print("✅ La colonne category_id existe déjà.")
                
    except Exception as e:
        print(f"❌ Erreur lors de la modification de la table : {e}")

if __name__ == "__main__":
    fix_threads_table() 