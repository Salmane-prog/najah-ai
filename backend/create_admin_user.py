#!/usr/bin/env python3
"""
Script pour créer un utilisateur admin
"""

import sqlite3
import bcrypt

def create_admin_user():
    """Créer un utilisateur admin"""
    try:
        # Connexion à la base de données
        conn = sqlite3.connect('../data/app.db')
        cursor = conn.cursor()
        
        # Vérifier si l'utilisateur existe déjà
        cursor.execute("SELECT id FROM users WHERE email = ?", ("superadmin@najah.ai",))
        existing_user = cursor.fetchone()
        
        if existing_user:
            print("✅ Utilisateur superadmin existe déjà")
            return True
        
        # Créer le mot de passe hashé
        password = "password123"
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        # Insérer l'utilisateur admin
        cursor.execute(
            "INSERT INTO users (username, email, hashed_password, role) VALUES (?, ?, ?, ?)",
            ("superadmin", "superadmin@najah.ai", hashed.decode('utf-8'), "admin")
        )
        
        conn.commit()
        conn.close()
        
        print("✅ Utilisateur superadmin créé avec succès")
        print(f"📧 Email: superadmin@najah.ai")
        print(f"🔑 Mot de passe: password123")
        print(f"👤 Rôle: admin")
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

if __name__ == "__main__":
    print("🔧 Création de l'utilisateur superadmin...")
    if create_admin_user():
        print("✅ Succès!")
    else:
        print("❌ Échec!") 