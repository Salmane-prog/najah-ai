#!/usr/bin/env python3
"""
Script pour vérifier le mot de passe de l'utilisateur
"""

import sqlite3
import hashlib

def check_user_password():
    """Vérifie le mot de passe de l'utilisateur dans la base de données"""
    
    try:
        conn = sqlite3.connect("app.db")
        cursor = conn.cursor()
        
        # Récupérer l'utilisateur
        cursor.execute("""
            SELECT id, email, password, role, first_name, last_name 
            FROM users 
            WHERE email = 'teacher@example.com'
        """)
        
        user = cursor.fetchone()
        
        if user:
            user_id, email, stored_password, role, first_name, last_name = user
            
            print(f"👤 Utilisateur trouvé:")
            print(f"   ID: {user_id}")
            print(f"   Email: {email}")
            print(f"   Rôle: {role}")
            print(f"   Nom: {first_name} {last_name}")
            print(f"   Mot de passe hashé: {stored_password}")
            
            # Tester différents hashs
            test_password = "teacher123"
            
            # Hash SHA256
            sha256_hash = hashlib.sha256(test_password.encode()).hexdigest()
            print(f"\n🔍 Test des hashs:")
            print(f"   Mot de passe test: {test_password}")
            print(f"   SHA256 hash: {sha256_hash}")
            print(f"   SHA256 match: {'✅' if sha256_hash == stored_password else '❌'}")
            
            # Hash MD5
            md5_hash = hashlib.md5(test_password.encode()).hexdigest()
            print(f"   MD5 hash: {md5_hash}")
            print(f"   MD5 match: {'✅' if md5_hash == stored_password else '❌'}")
            
            # Hash simple
            simple_hash = test_password
            print(f"   Simple match: {'✅' if simple_hash == stored_password else '❌'}")
            
        else:
            print("❌ Utilisateur non trouvé")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Erreur: {e}")

def test_password_verification():
    """Teste la vérification du mot de passe avec différents algorithmes"""
    
    print("\n🧪 Test de vérification du mot de passe...")
    
    test_password = "teacher123"
    
    # Différents algorithmes de hash
    algorithms = {
        "SHA256": lambda p: hashlib.sha256(p.encode()).hexdigest(),
        "MD5": lambda p: hashlib.md5(p.encode()).hexdigest(),
        "Simple": lambda p: p
    }
    
    for name, hash_func in algorithms.items():
        hashed = hash_func(test_password)
        print(f"   {name}: {hashed}")

if __name__ == "__main__":
    print("🔍 Vérification du mot de passe de l'utilisateur")
    print("=" * 60)
    
    check_user_password()
    test_password_verification()
    
    print("\n✅ Vérification terminée") 