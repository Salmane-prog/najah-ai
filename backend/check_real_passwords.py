#!/usr/bin/env python3
"""
Script pour vérifier les vrais mots de passe hashés dans la base de données
"""

import sqlite3
import hashlib
import bcrypt

def check_real_passwords():
    """Vérifie les vrais mots de passe hashés dans la base de données"""
    
    db_path = r"F:\IMT\stage\Yancode\Najah__AI\data\app.db"
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Récupérer les utilisateurs avec leurs mots de passe hashés
        cursor.execute("""
            SELECT id, email, hashed_password, role, first_name, last_name 
            FROM users 
            WHERE hashed_password IS NOT NULL
            LIMIT 10
        """)
        
        users = cursor.fetchall()
        
        print(f"🔍 Vérification des mots de passe hashés dans la base de données")
        print("=" * 80)
        
        for user in users:
            user_id, email, hashed_password, role, first_name, last_name = user
            
            print(f"\n👤 Utilisateur: {first_name} {last_name}")
            print(f"   ID: {user_id}")
            print(f"   Email: {email}")
            print(f"   Rôle: {role}")
            print(f"   Hash: {hashed_password[:50]}...")
            
            # Analyser le type de hash
            if hashed_password:
                if hashed_password.startswith('$2b$') or hashed_password.startswith('$2a$'):
                    print(f"   Type: bcrypt")
                elif len(hashed_password) == 64:
                    print(f"   Type: SHA256")
                elif len(hashed_password) == 32:
                    print(f"   Type: MD5")
                else:
                    print(f"   Type: Inconnu (longueur: {len(hashed_password)})")
            else:
                print(f"   Type: Aucun mot de passe")
        
        conn.close()
        
        # Tester la création de hash avec différents algorithmes
        print(f"\n🧪 Test de création de hash...")
        test_password = "teacher123"
        
        # Hash SHA256
        sha256_hash = hashlib.sha256(test_password.encode()).hexdigest()
        print(f"   SHA256 de '{test_password}': {sha256_hash}")
        
        # Hash MD5
        md5_hash = hashlib.md5(test_password.encode()).hexdigest()
        print(f"   MD5 de '{test_password}': {md5_hash}")
        
        # Hash bcrypt
        try:
            bcrypt_hash = bcrypt.hashpw(test_password.encode(), bcrypt.gensalt()).decode()
            print(f"   bcrypt de '{test_password}': {bcrypt_hash[:50]}...")
        except Exception as e:
            print(f"   bcrypt non disponible: {e}")
        
        return users
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return []

def test_password_verification():
    """Teste la vérification des mots de passe avec différents algorithmes"""
    
    print(f"\n🔐 Test de vérification des mots de passe...")
    
    # Récupérer un utilisateur de test
    db_path = r"F:\IMT\stage\Yancode\Najah__AI\data\app.db"
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Récupérer le premier utilisateur avec un mot de passe
        cursor.execute("""
            SELECT email, hashed_password 
            FROM users 
            WHERE hashed_password IS NOT NULL
            LIMIT 1
        """)
        
        user = cursor.fetchone()
        
        if user:
            email, hashed_password = user
            print(f"   Test avec l'utilisateur: {email}")
            print(f"   Hash stocké: {hashed_password[:50]}...")
            
            # Tester différents mots de passe
            test_passwords = [
                "teacher123", "admin123", "password", "123456", 
                "teacher", "admin", "student", "najah", "test"
            ]
            
            for password in test_passwords:
                # Test SHA256
                sha256_hash = hashlib.sha256(password.encode()).hexdigest()
                if sha256_hash == hashed_password:
                    print(f"   ✅ Mot de passe trouvé (SHA256): {password}")
                    return password
                
                # Test MD5
                md5_hash = hashlib.md5(password.encode()).hexdigest()
                if md5_hash == hashed_password:
                    print(f"   ✅ Mot de passe trouvé (MD5): {password}")
                    return password
            
            print(f"   ❌ Aucun mot de passe ne correspond")
            
        conn.close()
        
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
    
    return None

if __name__ == "__main__":
    print("🔍 Vérification des mots de passe réels dans la base de données")
    print("=" * 80)
    
    # Vérifier les hashs existants
    users = check_real_passwords()
    
    if users:
        # Tester la vérification
        found_password = test_password_verification()
        
        if found_password:
            print(f"\n🎯 MOT DE PASSE TROUVÉ !")
            print(f"   Utilisez '{found_password}' pour vous connecter")
        else:
            print(f"\n❌ Aucun mot de passe n'a été trouvé")
            print(f"🔍 Vérification manuelle nécessaire dans la base de données")
    else:
        print(f"\n❌ Aucun utilisateur avec mot de passe trouvé")


















