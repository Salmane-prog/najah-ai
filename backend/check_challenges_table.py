#!/usr/bin/env python3
"""
Script pour vérifier la structure de la table challenges
"""

import sqlite3
import os

def check_challenges_table():
    db_path = "../data/app.db"
    
    if not os.path.exists(db_path):
        print(f"❌ Base de données non trouvée: {db_path}")
        return
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("🔍 Vérification de la structure de la table challenges...")
        
        # Vérifier si la table existe
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='challenges'")
        if not cursor.fetchone():
            print("❌ Table challenges n'existe pas")
            return
        
        # Obtenir la structure de la table
        cursor.execute("PRAGMA table_info(challenges)")
        columns = cursor.fetchall()
        
        print("📋 Structure de la table challenges:")
        for col in columns:
            print(f"   - {col[1]} ({col[2]})")
        
        # Compter les enregistrements
        cursor.execute("SELECT COUNT(*) FROM challenges")
        count = cursor.fetchone()[0]
        print(f"📊 Nombre d'enregistrements: {count}")
        
        # Afficher quelques exemples
        if count > 0:
            cursor.execute("SELECT * FROM challenges LIMIT 3")
            rows = cursor.fetchall()
            print("📝 Exemples d'enregistrements:")
            for row in rows:
                print(f"   - {row}")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Erreur lors de la vérification: {str(e)}")

if __name__ == "__main__":
    check_challenges_table() 