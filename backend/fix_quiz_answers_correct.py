#!/usr/bin/env python3
"""
Script pour corriger la table quiz_answers en ajoutant la colonne correct_answer
"""

import sqlite3
from sqlalchemy import create_engine, text
from core.config import settings

def fix_quiz_answers_correct():
    """Ajouter la colonne correct_answer à la table quiz_answers"""
    
    # Créer une connexion directe à SQLite
    engine = create_engine(settings.SQLALCHEMY_DATABASE_URL)
    
    with engine.connect() as conn:
        # Vérifier les colonnes existantes
        result = conn.execute(text("PRAGMA table_info(quiz_answers)"))
        columns = [row[1] for row in result.fetchall()]
        
        print(f"Colonnes existantes dans quiz_answers: {columns}")
        
        # Ajouter la colonne correct_answer si elle n'existe pas
        if 'correct_answer' not in columns:
            print("Ajout de la colonne correct_answer à quiz_answers...")
            conn.execute(text("ALTER TABLE quiz_answers ADD COLUMN correct_answer TEXT"))
            print("✅ Colonne correct_answer ajoutée avec succès")
        else:
            print("✅ La colonne correct_answer existe déjà")
        
        conn.commit()
        print("✅ Table quiz_answers mise à jour avec succès")

if __name__ == "__main__":
    print("🔧 Correction de la table quiz_answers (correct_answer)...")
    fix_quiz_answers_correct()
    print("✅ Script terminé avec succès") 