#!/usr/bin/env python3
"""
Script pour corriger la table quiz_results
"""

import sqlite3
import os

def fix_quiz_results_table():
    """Corriger la table quiz_results"""
    print("🔧 CORRECTION DE LA TABLE QUIZ_RESULTS")
    print("=" * 50)
    
    # Chemin vers la base de données
    db_path = "data/app.db"
    
    if not os.path.exists(db_path):
        print(f"❌ Base de données non trouvée: {db_path}")
        return
    
    try:
        # Connexion à la base de données
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Vérifier si la colonne time_taken existe
        cursor.execute("PRAGMA table_info(quiz_results)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'time_taken' not in columns:
            print("➕ Ajout de la colonne time_taken...")
            cursor.execute("ALTER TABLE quiz_results ADD COLUMN time_taken INTEGER DEFAULT 0")
            print("✅ Colonne time_taken ajoutée")
        else:
            print("✅ Colonne time_taken existe déjà")
        
        # Vérifier si la colonne completed existe (au lieu de is_completed)
        if 'completed' not in columns:
            print("➕ Ajout de la colonne completed...")
            cursor.execute("ALTER TABLE quiz_results ADD COLUMN completed BOOLEAN DEFAULT 1")
            print("✅ Colonne completed ajoutée")
        else:
            print("✅ Colonne completed existe déjà")
        
        # Vérifier si la colonne sujet existe
        if 'sujet' not in columns:
            print("➕ Ajout de la colonne sujet...")
            cursor.execute("ALTER TABLE quiz_results ADD COLUMN sujet TEXT")
            print("✅ Colonne sujet ajoutée")
        else:
            print("✅ Colonne sujet existe déjà")
        
        conn.commit()
        print("✅ Table quiz_results corrigée avec succès!")
        
    except Exception as e:
        print(f"❌ Erreur lors de la correction: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    fix_quiz_results_table() 