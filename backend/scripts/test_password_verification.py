#!/usr/bin/env python3
"""
Script pour tester directement la vérification du mot de passe
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from core.database import SessionLocal
from models.user import User
from core.security import verify_password

def test_password_verification():
    """Tester la vérification du mot de passe"""
    db = SessionLocal()
    
    try:
        print("🔍 Test de vérification du mot de passe...")
        
        # Récupérer l'utilisateur
        user = db.query(User).filter(User.email == "teacher@test.com").first()
        
        if not user:
            print("❌ Utilisateur teacher@test.com non trouvé")
            return
        
        print(f"✅ Utilisateur trouvé: {user.email}")
        print(f"   ID: {user.id}")
        print(f"   Username: {user.username}")
        print(f"   Role: {user.role}")
        print(f"   Hash: {user.hashed_password[:20]}...")
        
        # Tester le mot de passe
        password = "password123"
        print(f"\n🔐 Test du mot de passe: {password}")
        
        is_valid = verify_password(password, user.hashed_password)
        print(f"   Résultat: {'✅ Valide' if is_valid else '❌ Invalide'}")
        
        if not is_valid:
            print(f"   Hash attendu pour '{password}': {user.hashed_password}")
            
            # Tester avec bcrypt directement
            import bcrypt
            test_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            print(f"   Hash bcrypt généré: {test_hash}")
            
            # Vérifier si le hash actuel est valide
            try:
                bcrypt.checkpw(password.encode('utf-8'), user.hashed_password.encode('utf-8'))
                print("   ✅ Hash bcrypt valide")
            except Exception as e:
                print(f"   ❌ Erreur bcrypt: {e}")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    test_password_verification() 