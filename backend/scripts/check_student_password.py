#!/usr/bin/env python3
"""
Script pour vérifier le mot de passe de l'étudiant salmane
"""

import sqlite3
from pathlib import Path
from passlib.context import CryptContext

def check_student_password():
    """Vérifier le mot de passe de l'étudiant salmane."""
    db_path = Path(__file__).parent.parent / "data" / "app.db"
    
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("=== VÉRIFICATION MOT DE PASSE ÉTUDIANT ===")
        
        # Récupérer l'utilisateur salmane
        cursor.execute("""
            SELECT id, email, username, hashed_password 
            FROM users 
            WHERE email = 'salmane.hajouji@najah.ai'
        """)
        
        user = cursor.fetchone()
        
        if not user:
            print("❌ Utilisateur salmane.hajouji@najah.ai non trouvé")
            return
        
        user_id, email, username, hashed_password = user
        print(f"✅ Utilisateur trouvé: {email}")
        print(f"   Username: {username}")
        print(f"   ID: {user_id}")
        print(f"   Hash: {hashed_password[:20]}...")
        
        # Tester différents mots de passe
        test_passwords = [
            "password123",
            "password",
            "123456",
            "salmane",
            "student",
            "test",
            "admin",
            "user"
        ]
        
        print("\n🔍 Test des mots de passe:")
        for password in test_passwords:
            if pwd_context.verify(password, hashed_password):
                print(f"✅ Mot de passe correct: '{password}'")
                break
        else:
            print("❌ Aucun mot de passe testé ne fonctionne")
            print("   Mots de passe testés:", test_passwords)
        
    except sqlite3.Error as e:
        print(f"❌ Erreur SQLite: {e}")
    except Exception as e:
        print(f"❌ Erreur inattendue: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    check_student_password() 