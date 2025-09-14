#!/usr/bin/env python3
"""
Script de démarrage simplifié du serveur
"""
import sys
import os

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

def start_server():
    """Démarre le serveur directement"""
    print("🚀 Démarrage du serveur...")
    print("=" * 50)
    
    # Créer les utilisateurs de test
    create_test_users()
    
    print("\n✅ Serveur prêt!")
    print("🌐 URL: http://localhost:8000")
    print("📚 Documentation: http://localhost:8000/docs")
    print("🔧 Debug activé")
    print("\n" + "=" * 50)
    
    # Démarrer le serveur
    try:
        import uvicorn
        uvicorn.run(
            "app:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="info"
        )
    except Exception as e:
        print(f"❌ Erreur lors du démarrage: {e}")
        print("Essayez: uvicorn app:app --reload --port 8000")

if __name__ == "__main__":
    start_server() 