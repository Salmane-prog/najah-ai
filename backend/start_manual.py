#!/usr/bin/env python3
"""
Script pour démarrer le serveur manuellement
"""
import sys
import os
import asyncio
from pathlib import Path

# Ajouter le répertoire au path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def create_test_users():
    """Crée des utilisateurs de test"""
    print("👥 Création d'utilisateurs de test...")
    
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
        if 'db' in locals():
            db.rollback()
        return False
    finally:
        if 'db' in locals():
            db.close()

def start_with_python():
    """Démarre le serveur avec Python directement"""
    print("🚀 Démarrage du serveur avec Python...")
    print("=" * 50)
    
    # Créer les utilisateurs de test
    create_test_users()
    
    print("\n✅ Serveur prêt!")
    print("🌐 URL: http://localhost:8000")
    print("📚 Documentation: http://localhost:8000/docs")
    print("\n" + "=" * 50)
    
    # Démarrer avec Python directement
    try:
        import subprocess
        result = subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "app:app", 
            "--host", "0.0.0.0", 
            "--port", "8000", 
            "--reload"
        ], cwd=os.path.dirname(__file__))
    except Exception as e:
        print(f"❌ Erreur: {e}")
        print("Essayez manuellement:")
        print("python -m uvicorn app:app --host 0.0.0.0 --port 8000 --reload")

def start_with_fastapi():
    """Démarre le serveur avec FastAPI directement"""
    print("🚀 Démarrage du serveur avec FastAPI...")
    print("=" * 50)
    
    # Créer les utilisateurs de test
    create_test_users()
    
    print("\n✅ Serveur prêt!")
    print("🌐 URL: http://localhost:8000")
    print("📚 Documentation: http://localhost:8000/docs")
    print("\n" + "=" * 50)
    
    # Démarrer avec FastAPI directement
    try:
        import uvicorn
        
        uvicorn.run(
            "app:app",  # Utiliser l'app comme string
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="info"
        )
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Essayez: pip install uvicorn --no-deps")
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    print("🚀 Démarrage du serveur...")
    print("=" * 50)
    
    # Essayer différentes méthodes
    try:
        start_with_fastapi()
    except Exception as e:
        print(f"❌ Méthode 1 échouée: {e}")
        print("Tentative avec méthode 2...")
        try:
            start_with_python()
        except Exception as e2:
            print(f"❌ Méthode 2 échouée: {e2}")
            print("\n🔧 SOLUTIONS MANUELLES:")
            print("1. pip install uvicorn --no-deps")
            print("2. python -m uvicorn app:app --host 0.0.0.0 --port 8000")
            print("3. pip install --trusted-host pypi.org uvicorn") 