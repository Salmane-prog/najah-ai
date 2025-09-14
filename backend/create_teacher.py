#!/usr/bin/env python3
"""
Script pour créer un compte professeur
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.database import SessionLocal
from models.user import User, UserRole
from core.security import get_password_hash

def create_teacher():
    db = SessionLocal()
    try:
        # Vérifier si le prof existe déjà
        existing_teacher = db.query(User).filter(User.email == "prof@najah.ai").first()
        if existing_teacher:
            print("✅ Le professeur existe déjà!")
            return existing_teacher
        
        # Créer le professeur
        teacher = User(
            username="professeur",
            email="prof@najah.ai",
            hashed_password=get_password_hash("prof123"),
            role=UserRole.teacher
        )
        
        db.add(teacher)
        db.commit()
        db.refresh(teacher)
        
        print("✅ Professeur créé avec succès!")
        print(f"📧 Email: prof@najah.ai")
        print(f"🔑 Mot de passe: prof123")
        print(f"👤 Rôle: {teacher.role.value}")
        
        return teacher
        
    except Exception as e:
        print(f"❌ Erreur lors de la création du professeur: {e}")
        db.rollback()
        return None
    finally:
        db.close()

if __name__ == "__main__":
    print("🎓 Création d'un compte professeur...")
    create_teacher() 