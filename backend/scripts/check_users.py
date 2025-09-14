#!/usr/bin/env python3
"""
Script pour vérifier les utilisateurs dans la base de données
"""

import sqlite3
import os

def check_users():
    """Vérifier les utilisateurs dans la base de données"""
    db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'app.db')
    
    print(f"🔍 Vérification de la base de données: {db_path}")
    
    if not os.path.exists(db_path):
        print("❌ Base de données non trouvée!")
        return
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Vérifier les tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print(f"\n📋 Tables disponibles: {[table[0] for table in tables]}")
        
        # Vérifier les utilisateurs
        cursor.execute("SELECT id, email, username, role FROM users LIMIT 10;")
        users = cursor.fetchall()
        
        print(f"\n👥 Utilisateurs dans la base de données:")
        if users:
            for user in users:
                print(f"  - ID: {user[0]}, Email: {user[1]}, Username: {user[2]}, Role: {user[3]}")
        else:
            print("  ❌ Aucun utilisateur trouvé")
        
        # Vérifier spécifiquement teacher@test.com
        cursor.execute("SELECT id, email, username, role, hashed_password FROM users WHERE email = 'teacher@test.com';")
        teacher = cursor.fetchone()
        
        if teacher:
            print(f"\n✅ Utilisateur teacher@test.com trouvé:")
            print(f"  - ID: {teacher[0]}")
            print(f"  - Email: {teacher[1]}")
            print(f"  - Username: {teacher[2]}")
            print(f"  - Role: {teacher[3]}")
            print(f"  - Password hash: {teacher[4][:20]}...")
        else:
            print(f"\n❌ Utilisateur teacher@test.com non trouvé")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    check_users() 