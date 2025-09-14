#!/usr/bin/env python3
"""
Script pour changer le mot de passe du professeur ou en créer un nouveau
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.database import SessionLocal
from models.user import User, UserRole
from core.security import get_password_hash

def change_teacher_password():
    """Change le mot de passe du professeur ou en crée un nouveau"""
    db = SessionLocal()
    
    try:
        print("🔧 Changement du mot de passe du professeur...")
        
        # Chercher un professeur existant
        teacher = db.query(User).filter(User.role == UserRole.teacher).first()
        
        if teacher:
            print(f"✅ Professeur trouvé: {teacher.email}")
            print(f"   Ancien nom d'utilisateur: {teacher.username}")
            
            # Mettre à jour le mot de passe
            teacher.hashed_password = get_password_hash("salmane123@")
            teacher.username = "salmane"  # Optionnel: changer aussi le nom d'utilisateur
            
            db.commit()
            print("✅ Mot de passe mis à jour avec succès!")
            print(f"   📧 Email: {teacher.email}")
            print(f"   👤 Nom d'utilisateur: {teacher.username}")
            print(f"   🔑 Nouveau mot de passe: salmane123@")
            
        else:
            print("❌ Aucun professeur trouvé, création d'un nouveau compte...")
            
            # Créer un nouveau professeur
            new_teacher = User(
                username="salmane",
                email="salmane@najah.ai",
                hashed_password=get_password_hash("salmane123@"),
                role=UserRole.teacher
            )
            
            db.add(new_teacher)
            db.commit()
            db.refresh(new_teacher)
            
            print("✅ Nouveau professeur créé avec succès!")
            print(f"   📧 Email: salmane@najah.ai")
            print(f"   👤 Nom d'utilisateur: salmane")
            print(f"   🔑 Mot de passe: salmane123@")
        
        # Afficher tous les professeurs pour vérification
        print("\n📋 Liste de tous les professeurs:")
        teachers = db.query(User).filter(User.role == UserRole.teacher).all()
        for t in teachers:
            print(f"   • {t.username} ({t.email}) - ID: {t.id}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du changement de mot de passe: {e}")
        db.rollback()
        return False
    finally:
        db.close()

if __name__ == "__main__":
    success = change_teacher_password()
    if success:
        print("\n🎉 Opération terminée avec succès!")
        print("   Vous pouvez maintenant vous connecter avec:")
        print("   📧 Email: salmane@najah.ai")
        print("   🔑 Mot de passe: salmane123@")
    else:
        print("\n❌ Échec de l'opération") 