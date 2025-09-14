#!/usr/bin/env python3
"""
Script pour ajouter le champ correct_answer à la table quiz_answers
"""

import sqlite3
import os

def add_correct_answer_field():
    # Chemin vers la base de données
    db_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'app.db')
    
    print(f"Connexion à la base de données: {db_path}")
    
    try:
        # Connexion à la base de données
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Vérifier si le champ existe déjà
        cursor.execute("PRAGMA table_info(quiz_answers)")
        columns = cursor.fetchall()
        column_names = [col[1] for col in columns]
        
        if 'correct_answer' in column_names:
            print("✅ Le champ correct_answer existe déjà")
        else:
            # Ajouter le champ correct_answer
            cursor.execute("ALTER TABLE quiz_answers ADD COLUMN correct_answer TEXT")
            conn.commit()
            print("✅ Champ correct_answer ajouté avec succès")
        
        # Vérifier la structure de la table
        cursor.execute("PRAGMA table_info(quiz_answers)")
        columns = cursor.fetchall()
        print("\nStructure de la table quiz_answers:")
        for col in columns:
            print(f"  - {col[1]} ({col[2]})")
        
        conn.close()
        print("\n✅ Script terminé avec succès")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False
    
    return True

if __name__ == "__main__":
    add_correct_answer_field() 