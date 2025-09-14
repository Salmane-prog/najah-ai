#!/usr/bin/env python3
"""
Script pour vérifier un utilisateur spécifique
"""

import sqlite3
import os

def check_specific_user():
    """Vérifier l'utilisateur test@student.com"""
    
    db_path = os.path.join(os.path.dirname(__file__), "..", "data", "app.db")
    
    if not os.path.exists(db_path):
        print(f"Base de données non trouvée: {db_path}")
        return
    
    print(f"Connexion à la base de données: {db_path}")
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Vérifier l'utilisateur test@student.com
        cursor.execute("SELECT * FROM users WHERE email = ?", ("test@student.com",))
        user = cursor.fetchone()
        
        if user:
            print(f"\n✅ Utilisateur trouvé:")
            print(f"  ID: {user[0]}")
            print(f"  Username: {user[1]}")
            print(f"  Email: {user[2]}")
            print(f"  Hash: {user[3][:20]}...")
            print(f"  Role: {user[4]}")
            print(f"  First Name: {user[5]}")
            print(f"  Last Name: {user[6]}")
            print(f"  Is Active: {user[11]}")
        else:
            print(f"\n❌ Utilisateur test@student.com non trouvé")
            
            # Lister tous les utilisateurs
            cursor.execute("SELECT id, username, email, role FROM users")
            users = cursor.fetchall()
            print(f"\n📋 Utilisateurs existants ({len(users)}):")
            for u in users:
                print(f"  - ID {u[0]}: {u[1]} ({u[2]}) - {u[3]}")
        
        conn.close()
        
    except Exception as e:
        print(f"Erreur: {e}")

if __name__ == "__main__":
    check_specific_user()











