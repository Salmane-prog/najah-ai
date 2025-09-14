#!/usr/bin/env python3
from core.database import SessionLocal
from models.user import User, UserRole
from core.security import get_password_hash

def create_marie_user():
    """Créer l'utilisateur marie.dubois@najah.ai"""
    print("👤 Création de l'utilisateur marie.dubois@najah.ai...")
    
    db = SessionLocal()
    try:
        # Vérifier si l'utilisateur existe déjà
        existing_user = db.query(User).filter(User.email == "marie.dubois@najah.ai").first()
        
        if existing_user:
            print(f"⚠️ L'utilisateur marie.dubois@najah.ai existe déjà")
            print(f"   Username: {existing_user.username}")
            print(f"   Role: {existing_user.role}")
            
            # Mettre à jour le mot de passe
            existing_user.hashed_password = get_password_hash("salmane123@")
            db.commit()
            print("✅ Mot de passe mis à jour")
            return existing_user
        else:
            # Créer le nouvel utilisateur
            hashed_password = get_password_hash("salmane123@")
            new_user = User(
                username="marie.dubois",
                email="marie.dubois@najah.ai",
                hashed_password=hashed_password,
                role=UserRole.teacher
            )
            
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            
            print("✅ Utilisateur marie.dubois@najah.ai créé avec succès!")
            print(f"   Username: {new_user.username}")
            print(f"   Email: {new_user.email}")
            print(f"   Role: {new_user.role}")
            print(f"   Mot de passe: salmane123@")
            
            return new_user
            
    except Exception as e:
        print(f"❌ Erreur lors de la création: {e}")
        db.rollback()
        return None
    finally:
        db.close()

def test_login_marie():
    """Tester la connexion avec marie.dubois@najah.ai"""
    print("\n🔐 Test de connexion avec marie.dubois@najah.ai...")
    
    import requests
    import json
    
    try:
        response = requests.post(
            "http://localhost:8000/api/v1/auth/login",
            json={
                "email": "marie.dubois@najah.ai",
                "password": "salmane123@"
            },
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Connexion réussie!")
            print(f"   Token: {data.get('access_token', '')[:20]}...")
            print(f"   Role: {data.get('role', '')}")
            print(f"   ID: {data.get('id', '')}")
            print(f"   Name: {data.get('name', '')}")
            return True
        else:
            print("❌ Échec de connexion")
            try:
                error_data = response.json()
                print(f"   Erreur: {error_data.get('detail', '')}")
            except:
                print(f"   Réponse: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur de connexion: {e}")
        return False

def list_all_users():
    """Lister tous les utilisateurs"""
    print("\n📋 Liste de tous les utilisateurs:")
    
    db = SessionLocal()
    try:
        users = db.query(User).all()
        
        for user in users:
            print(f"   • {user.username} ({user.email}) - {user.role}")
            
    finally:
        db.close()

def main():
    print("👤 Création de l'utilisateur Marie - Najah AI")
    print("=" * 50)
    
    # Créer l'utilisateur marie
    user = create_marie_user()
    
    if user:
        # Tester la connexion
        test_login_marie()
    
    # Lister tous les utilisateurs
    list_all_users()
    
    print("\n" + "=" * 50)
    print("🏁 Création terminée")

if __name__ == "__main__":
    main() 