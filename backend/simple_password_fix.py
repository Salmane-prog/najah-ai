#!/usr/bin/env python3
"""
Script simple pour changer le mot de passe
"""

import sqlite3
import bcrypt

def fix_password():
    """Change le mot de passe de l'utilisateur admin"""
    try:
        # Connexion à la base de données
        conn = sqlite3.connect('../data/app.db')
        cursor = conn.cursor()
        
        # Nouveau mot de passe
        password = "password123"
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        # Mettre à jour le mot de passe de l'admin
        cursor.execute(
            "UPDATE users SET hashed_password = ? WHERE email = ?",
            (hashed.decode('utf-8'), "admin@najah.ai")
        )
        
        conn.commit()
        conn.close()
        
        print("✅ Mot de passe de l'admin changé vers: password123")
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

if __name__ == "__main__":
    print("🔧 Changement du mot de passe admin...")
    if fix_password():
        print("✅ Succès!")
    else:
        print("❌ Échec!") 