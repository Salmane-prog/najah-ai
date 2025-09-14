#!/usr/bin/env python3
"""
Script pour mettre à jour la table assessments avec les nouvelles colonnes
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine, text

def update_assessments_table():
    """Ajouter les colonnes manquantes à la table assessments"""
    
    # Créer une connexion directe à la base de données
    engine = create_engine("sqlite:///../data/app.db")
    
    try:
        with engine.connect() as conn:
            # Ajouter les nouvelles colonnes
            columns_to_add = [
                ("subject", "VARCHAR(100)"),
                ("priority", "VARCHAR(20) DEFAULT 'medium'"),
                ("estimated_time", "INTEGER"),
                ("created_by", "INTEGER"),
                ("created_at", "TIMESTAMP")  # Sans valeur par défaut pour SQLite
            ]
            
            for column_name, column_type in columns_to_add:
                try:
                    conn.execute(text(f"ALTER TABLE assessments ADD COLUMN {column_name} {column_type}"))
                    print(f"✅ Colonne '{column_name}' ajoutée")
                except Exception as e:
                    if "duplicate column name" in str(e).lower():
                        print(f"ℹ️  Colonne '{column_name}' existe déjà")
                    else:
                        print(f"❌ Erreur lors de l'ajout de la colonne '{column_name}': {str(e)}")
            
            # Commit les changements
            conn.commit()
            print("✅ Table assessments mise à jour avec succès")
            
    except Exception as e:
        print(f"❌ Erreur lors de la mise à jour de la table: {str(e)}")

if __name__ == "__main__":
    update_assessments_table() 