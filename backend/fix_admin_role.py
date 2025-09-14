#!/usr/bin/env python3
"""
Script pour changer le rôle de l'admin vers teacher
"""

import sqlite3

def fix_admin_role():
    """Change le rôle de l'admin vers teacher"""
    try:
        # Connexion à la base de données
        conn = sqlite3.connect('../data/app.db')
        cursor = conn.cursor()
        
        # Mettre à jour le rôle de l'admin vers teacher
        cursor.execute(
            "UPDATE users SET role = ? WHERE email = ?",
            ("teacher", "admin@najah.ai")
        )
        
        conn.commit()
        conn.close()
        
        print("✅ Rôle de l'admin changé vers: teacher")
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

if __name__ == "__main__":
    print("🔧 Changement du rôle admin...")
    if fix_admin_role():
        print("✅ Succès!")
    else:
        print("❌ Échec!") 