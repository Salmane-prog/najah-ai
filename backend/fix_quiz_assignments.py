#!/usr/bin/env python3
"""
Script pour corriger la table quiz_assignments
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.database import engine, SessionLocal
from sqlalchemy import text

def fix_quiz_assignments_table():
    """Ajouter les colonnes manquantes à la table quiz_assignments"""
    
    with engine.connect() as conn:
        try:
            # Vérifier les colonnes existantes
            result = conn.execute(text("PRAGMA table_info(quiz_assignments)"))
            columns = [row[1] for row in result.fetchall()]
            
            print(f"Colonnes existantes: {columns}")
            
            # Ajouter is_active si manquant
            if 'is_active' not in columns:
                print("Ajout de la colonne is_active à quiz_assignments...")
                conn.execute(text("ALTER TABLE quiz_assignments ADD COLUMN is_active BOOLEAN DEFAULT 1"))
                print("✅ Colonne is_active ajoutée avec succès")
            else:
                print("✅ La colonne is_active existe déjà")
            
            # Ajouter created_at si manquant
            if 'created_at' not in columns:
                print("Ajout de la colonne created_at à quiz_assignments...")
                conn.execute(text("ALTER TABLE quiz_assignments ADD COLUMN created_at DATETIME"))
                print("✅ Colonne created_at ajoutée avec succès")
            else:
                print("✅ La colonne created_at existe déjà")
            
            # Mettre à jour les enregistrements existants avec created_at = maintenant
            print("Mise à jour des enregistrements existants...")
            conn.execute(text("UPDATE quiz_assignments SET created_at = datetime('now') WHERE created_at IS NULL"))
            updated_rows = conn.execute(text("SELECT changes()")).scalar()
            print(f"✅ {updated_rows} enregistrements mis à jour")
                
            conn.commit()
                
        except Exception as e:
            print(f"❌ Erreur lors de la modification de la table: {e}")
            conn.rollback()

if __name__ == "__main__":
    print("🔧 Correction de la table quiz_assignments...")
    fix_quiz_assignments_table()
    print("✅ Script terminé") 