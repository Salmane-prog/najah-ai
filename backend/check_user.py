#!/usr/bin/env python3
import sqlite3

def check_user():
    conn = sqlite3.connect('data/app.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT username, email, hashed_password, role FROM users WHERE email='marie.dubois@najah.ai'")
    user = cursor.fetchone()
    
    if user:
        print(f"✅ Utilisateur trouvé:")
        print(f"   Username: {user[0]}")
        print(f"   Email: {user[1]}")
        print(f"   Rôle: {user[3]}")
        print(f"   Mot de passe hashé: {user[2][:20]}...")
    else:
        print("❌ Utilisateur non trouvé")
    
    conn.close()

if __name__ == "__main__":
    check_user() 