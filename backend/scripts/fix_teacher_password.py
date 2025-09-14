#!/usr/bin/env python3
"""
Script pour corriger le mot de passe de teacher@test.com
"""

import sqlite3
import hashlib
import os

def fix_teacher_password():
    print("🔧 Correction du mot de passe de teacher@test.com...")
    
    # Chemin vers la base de données
    db_path = "data/app.db"
    
    if not os.path.exists(db_path):
        print(f"❌ Base de données non trouvée: {db_path}")
        return
    
    try:
        # Connexion à la base de données
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Vérifier si l'utilisateur existe
        cursor.execute("SELECT id, email, username FROM users WHERE email = ?", ("teacher@test.com",))
        user = cursor.fetchone()
        
        if not user:
            print("❌ Utilisateur teacher@test.com non trouvé")
            return
        
        user_id, email, username = user
        print(f"✅ Utilisateur trouvé: ID={user_id}, Email={email}, Username={username}")
        
        # Hasher le nouveau mot de passe
        password = "password123"
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        
        # Mettre à jour le mot de passe
        cursor.execute(
            "UPDATE users SET hashed_password = ? WHERE id = ?",
            (password_hash, user_id)
        )
        
        conn.commit()
        print("✅ Mot de passe mis à jour avec succès")
        print(f"   Nouveau hash: {password_hash[:20]}...")
        
        # Vérifier la mise à jour
        cursor.execute("SELECT hashed_password FROM users WHERE id = ?", (user_id,))
        updated_hash = cursor.fetchone()[0]
        print(f"   Hash en base: {updated_hash[:20]}...")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    fix_teacher_password() 