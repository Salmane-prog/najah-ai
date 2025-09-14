#!/usr/bin/env python3
"""
Script pour recréer l'utilisateur de test
"""

import sqlite3
import os
import bcrypt

def recreate_test_user():
    """Recréer l'utilisateur de test"""
    
    # Chemin vers la base de données
    db_path = os.path.join(os.path.dirname(__file__), "..", "data", "app.db")
    
    if not os.path.exists(db_path):
        print(f"Base de données non trouvée: {db_path}")
        return
    
    print(f"Connexion à la base de données: {db_path}")
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Supprimer l'utilisateur existant
        test_email = "test@student.com"
        cursor.execute("DELETE FROM users WHERE email = ?", (test_email,))
        deleted_count = cursor.rowcount
        
        if deleted_count > 0:
            print(f"✅ Utilisateur {test_email} supprimé")
        else:
            print(f"ℹ️ Utilisateur {test_email} n'existait pas")
        
        # Créer un hash de mot de passe avec bcrypt
        password = "password123"
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        password_hash_str = password_hash.decode('utf-8')
        
        print(f"🔐 Hash créé: {password_hash_str[:20]}...")
        
        # Insérer le nouvel utilisateur
        cursor.execute("""
            INSERT INTO users (username, email, hashed_password, role, first_name, last_name, is_active, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, datetime('now'))
        """, ("teststudent", test_email, password_hash_str, "student", "Étudiant", "Test", True))
        
        user_id = cursor.lastrowid
        conn.commit()
        
        print(f"✅ Utilisateur de test recréé avec succès!")
        print(f"  ID: {user_id}")
        print(f"  Email: {test_email}")
        print(f"  Mot de passe: {password}")
        print(f"  Role: student")
        
        # Vérifier que l'utilisateur a été créé
        cursor.execute("SELECT * FROM users WHERE email = ?", (test_email,))
        user = cursor.fetchone()
        if user:
            print(f"  Hash en base: {user[3][:20]}...")
        
        conn.close()
        return user_id
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return None

if __name__ == "__main__":
    recreate_test_user()











