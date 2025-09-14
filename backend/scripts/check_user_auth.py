#!/usr/bin/env python3
"""
Script pour vérifier les utilisateurs et leurs mots de passe
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from core.database import SessionLocal
from models.user import User, UserRole
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def check_user_auth():
    """Vérifier les utilisateurs et leurs mots de passe."""
    db = SessionLocal()
    
    try:
        print("=== VÉRIFICATION DES UTILISATEURS ===")
        
        # Récupérer tous les utilisateurs
        users = db.query(User).all()
        print(f"Total utilisateurs: {len(users)}")
        
        for user in users:
            print(f"\n--- {user.username} ---")
            print(f"ID: {user.id}")
            print(f"Email: {user.email}")
            print(f"Role: {user.role}")
            print(f"Mot de passe hashé: {user.hashed_password[:20]}..." if user.hashed_password else "Pas de mot de passe")
            
            # Tester quelques mots de passe courants
            test_passwords = ["password123", "123456", "password", "admin", "user"]
            for test_pwd in test_passwords:
                if user.hashed_password and pwd_context.verify(test_pwd, user.hashed_password):
                    print(f"✅ Mot de passe trouvé: '{test_pwd}'")
                    break
            else:
                print("❌ Mot de passe non trouvé dans les tests")
        
        print("\n=== RECOMMANDATIONS ===")
        print("1. Vérifiez que l'utilisateur 'salmane' existe")
        print("2. Vérifiez que le mot de passe est correct")
        print("3. Essayez de vous connecter avec les identifiants affichés ci-dessus")
        
    except Exception as e:
        print(f"Erreur: {str(e)}")
    finally:
        db.close()

if __name__ == "__main__":
    check_user_auth() 