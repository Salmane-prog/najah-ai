#!/usr/bin/env python3
"""
Script pour démarrer le serveur avec debug complet
"""
import sys
import os
import uvicorn
from pathlib import Path

# Ajouter le répertoire au path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def check_dependencies():
    """Vérifie que toutes les dépendances sont installées"""
    print("🔍 Vérification des dépendances...")
    
    try:
        import fastapi
        print("✅ FastAPI")
    except ImportError:
        print("❌ FastAPI manquant: pip install fastapi")
        return False
    
    try:
        import uvicorn
        print("✅ Uvicorn")
    except ImportError:
        print("❌ Uvicorn manquant: pip install uvicorn")
        return False
    
    try:
        import sqlalchemy
        print("✅ SQLAlchemy")
    except ImportError:
        print("❌ SQLAlchemy manquant: pip install sqlalchemy")
        return False
    
    try:
        import passlib
        print("✅ Passlib")
    except ImportError:
        print("❌ Passlib manquant: pip install passlib")
        return False
    
    try:
        import python_jose
        print("✅ Python-Jose")
    except ImportError:
        print("❌ Python-Jose manquant: pip install python-jose")
        return False
    
    return True

def check_database():
    """Vérifie la base de données"""
    print("\n🔍 Vérification de la base de données...")
    
    try:
        from core.config import settings
        db_path = settings.SQLALCHEMY_DATABASE_URL.replace("sqlite:///", "")
        if db_path.startswith("../"):
            db_path = os.path.join(os.path.dirname(__file__), db_path)
        
        print(f"   Base de données: {db_path}")
        
        if not os.path.exists(db_path):
            print("❌ Base de données non trouvée")
            return False
        
        # Test de connexion
        from core.database import SessionLocal
        from sqlalchemy import text
        
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        db.close()
        
        print("✅ Base de données accessible")
        return True
        
    except Exception as e:
        print(f"❌ Erreur de base de données: {e}")
        return False

def check_users():
    """Vérifie qu'il y a des utilisateurs dans la base"""
    print("\n👥 Vérification des utilisateurs...")
    
    try:
        from core.database import SessionLocal
        from models.user import User
        
        db = SessionLocal()
        users = db.query(User).all()
        db.close()
        
        print(f"   {len(users)} utilisateurs trouvés")
        
        if len(users) == 0:
            print("⚠️ Aucun utilisateur dans la base")
            print("   Créez des utilisateurs de test avec:")
            print("   python create_test_users.py")
            return False
        
        # Afficher les premiers utilisateurs
        for user in users[:3]:
            print(f"   - {user.email} ({user.role})")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la vérification des utilisateurs: {e}")
        return False

def create_test_users():
    """Crée des utilisateurs de test"""
    print("\n👥 Création d'utilisateurs de test...")
    
    try:
        from core.database import SessionLocal
        from models.user import User, UserRole
        from core.security import get_password_hash
        
        db = SessionLocal()
        
        # Vérifier si les utilisateurs existent déjà
        existing_users = db.query(User).filter(
            User.email.in_([
                "student@test.com",
                "teacher@test.com", 
                "parent@test.com"
            ])
        ).all()
        
        if existing_users:
            print("✅ Utilisateurs de test existent déjà")
            return True
        
        # Créer les utilisateurs de test
        test_users = [
            {
                "username": "student",
                "email": "student@test.com",
                "password": "password123",
                "role": UserRole.student
            },
            {
                "username": "teacher",
                "email": "teacher@test.com", 
                "password": "password123",
                "role": UserRole.teacher
            },
            {
                "username": "parent",
                "email": "parent@test.com",
                "password": "password123", 
                "role": UserRole.parent
            }
        ]
        
        for user_data in test_users:
            hashed_password = get_password_hash(user_data["password"])
            user = User(
                username=user_data["username"],
                email=user_data["email"],
                hashed_password=hashed_password,
                role=user_data["role"]
            )
            db.add(user)
        
        db.commit()
        print("✅ Utilisateurs de test créés")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la création des utilisateurs: {e}")
        db.rollback()
        return False
    finally:
        db.close()

def start_server():
    """Démarre le serveur avec debug"""
    print("\n🚀 Démarrage du serveur...")
    print("=" * 50)
    
    # Vérifications préalables
    if not check_dependencies():
        print("❌ Dépendances manquantes")
        return
    
    if not check_database():
        print("❌ Problème de base de données")
        return
    
    if not check_users():
        print("⚠️ Création d'utilisateurs de test...")
        if not create_test_users():
            print("❌ Impossible de créer les utilisateurs de test")
            return
    
    print("\n✅ Toutes les vérifications sont passées!")
    print("🌐 Démarrage du serveur sur http://localhost:8000")
    print("📚 Documentation: http://localhost:8000/docs")
    print("🔧 Debug activé")
    print("\n" + "=" * 50)
    
    # Démarrer le serveur
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="debug"
    )

if __name__ == "__main__":
    start_server() 