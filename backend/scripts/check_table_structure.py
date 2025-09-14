#!/usr/bin/env python3
"""
Script pour vérifier la structure de la table users
"""

import sqlite3
import os

def check_table_structure():
    print("🔍 Vérification de la structure de la table users...")
    
    # Chemin vers la base de données
    db_path = "data/app.db"
    
    if not os.path.exists(db_path):
        print(f"❌ Base de données non trouvée: {db_path}")
        return
    
    try:
        # Connexion à la base de données
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Obtenir la structure de la table users
        cursor.execute("PRAGMA table_info(users)")
        columns = cursor.fetchall()
        
        print("📋 Structure de la table users:")
        for col in columns:
            print(f"   - {col[1]} ({col[2]}) - {'NOT NULL' if col[3] else 'NULL'}")
        
        # Vérifier les données d'un utilisateur
        cursor.execute("SELECT * FROM users WHERE email = 'teacher@test.com'")
        user = cursor.fetchone()
        
        if user:
            print(f"\n👤 Données de teacher@test.com:")
            for i, col in enumerate(columns):
                value = user[i]
                if col[1] == 'hashed_password' and value:
                    value = value[:20] + "..." if len(str(value)) > 20 else value
                print(f"   {col[1]}: {value}")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    check_table_structure() 