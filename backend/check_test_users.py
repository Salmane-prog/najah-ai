#!/usr/bin/env python3
import sqlite3

def check_test_users():
    conn = sqlite3.connect('data/app.db')
    cursor = conn.cursor()
    
    print("🔍 Vérification des utilisateurs test...")
    
    # Vérifier tous les utilisateurs
    cursor.execute('SELECT id, username, email, first_name, last_name, role FROM users ORDER BY id')
    users = cursor.fetchall()
    
    print(f"\n📊 Total utilisateurs: {len(users)}")
    print("\n👥 Liste des utilisateurs:")
    print("-" * 80)
    print(f"{'ID':<3} | {'Username':<20} | {'Email':<30} | {'Nom':<25} | {'Rôle':<10}")
    print("-" * 80)
    
    for user in users:
        id, username, email, first_name, last_name, role = user
        full_name = f"{first_name or ''} {last_name or ''}".strip() or "N/A"
        print(f"{id:<3} | {username or 'N/A':<20} | {email or 'N/A':<30} | {full_name:<25} | {role or 'N/A':<10}")
    
    # Chercher spécifiquement les utilisateurs test
    print(f"\n🔍 Recherche des utilisateurs test (avec 'real' dans le nom):")
    test_users = [u for u in users if 'real' in str(u[1]).lower() or 'real' in str(u[2]).lower()]
    
    if test_users:
        print("✅ Utilisateurs test trouvés:")
        for user in test_users:
            id, username, email, first_name, last_name, role = user
            print(f"   - ID: {id}, Username: {username}, Email: {email}, Rôle: {role}")
    else:
        print("❌ Aucun utilisateur test trouvé")
    
    conn.close()

if __name__ == "__main__":
    check_test_users()
