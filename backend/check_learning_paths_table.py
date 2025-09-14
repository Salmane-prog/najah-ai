#!/usr/bin/env python3
"""
Script pour vérifier la structure de la table learning_paths
"""

import sqlite3
import os

def check_learning_paths_table():
    """Vérifier la structure de la table learning_paths"""
    print("🔍 VÉRIFICATION DE LA TABLE LEARNING_PATHS")
    print("=" * 50)
    
    # Chemin vers la base de données
    db_path = "F:/IMT/stage/Yancode/Najah__AI/data/app.db"
    
    if not os.path.exists(db_path):
        print(f"❌ Base de données non trouvée: {db_path}")
        return
    
    try:
        # Connexion à la base de données
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Vérifier la structure de la table learning_paths
        cursor.execute("PRAGMA table_info(learning_paths)")
        columns = cursor.fetchall()
        
        print("📋 Structure de la table learning_paths:")
        for column in columns:
            print(f"  - {column[1]} ({column[2]}) - NOT NULL: {column[3]} - DEFAULT: {column[4]}")
        
        # Vérifier les données existantes
        cursor.execute("SELECT * FROM learning_paths LIMIT 3")
        rows = cursor.fetchall()
        
        print(f"\n📊 Données existantes ({len(rows)} premières lignes):")
        for row in rows:
            print(f"  - {row}")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_learning_paths_table() 