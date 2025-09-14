#!/usr/bin/env python3
"""
Script pour changer le mot de passe de l'utilisateur admin
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.database import SessionLocal
from models.user import User
from core.security import get_password_hash

def fix_admin_password():
    """Change le mot de passe de l'utilisateur admin"""
    db = SessionLocal()
    try:
        # Trouver l'utilisateur admin
        admin = db.query(User).filter(User.email == "admin@najah.ai").first()
        if not admin:
            print("❌ Utilisateur admin non trouvé")
            return False
        
        # Changer le mot de passe
        new_password = "password123"
        admin.hashed_password = get_password_hash(new_password)
        db.commit()
        
        print(f"✅ Mot de passe de l'admin changé vers: {new_password}")
        print(f"📧 Email: {admin.email}")
        print(f"👤 Username: {admin.username}")
        print(f"🔑 Role: {admin.role}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False
    finally:
        db.close()

if __name__ == "__main__":
    print("🔧 Changement du mot de passe admin...")
    if fix_admin_password():
        print("✅ Succès!")
    else:
        print("❌ Échec!") 