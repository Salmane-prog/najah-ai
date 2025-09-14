#!/usr/bin/env python3
from core.database import SessionLocal
from models.user import User
from core.security import get_password_hash, verify_password

def fix_marie_password():
    """Corriger le mot de passe de marie.dubois@najah.ai"""
    print("🔧 Correction du mot de passe de marie.dubois@najah.ai...")
    
    db = SessionLocal()
    try:
        # Rechercher l'utilisateur marie
        user = db.query(User).filter(User.email == "marie.dubois@najah.ai").first()
        
        if not user:
            print("❌ Utilisateur marie.dubois@najah.ai non trouvé")
            return False
            
        print(f"✅ Utilisateur trouvé: {user.username} ({user.email})")
        print(f"   Role: {user.role}")
        print(f"   Ancien hash: {user.hashed_password[:30]}...")
        
        # Vérifier si le mot de passe actuel fonctionne
        current_password = "salmane123@"
        if verify_password(current_password, user.hashed_password):
            print("✅ Le mot de passe actuel fonctionne déjà!")
            return True
            
        # Si le mot de passe ne fonctionne pas, le corriger
        print("⚠️ Le mot de passe actuel ne fonctionne pas, correction en cours...")
        
        # Créer un nouveau hash pour le mot de passe
        new_hash = get_password_hash(current_password)
        user.hashed_password = new_hash
        
        db.commit()
        
        # Vérifier que le nouveau mot de passe fonctionne
        if verify_password(current_password, user.hashed_password):
            print("✅ Mot de passe corrigé avec succès!")
            print(f"   Nouveau hash: {user.hashed_password[:30]}...")
            return True
        else:
            print("❌ Erreur lors de la correction du mot de passe")
            return False
            
    except Exception as e:
        print(f"❌ Erreur: {e}")
        db.rollback()
        return False
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

def create_test_users():
    """Créer des utilisateurs de test avec des mots de passe connus"""
    print("\n🔧 Création d'utilisateurs de test...")
    
    db = SessionLocal()
    try:
        test_users = [
            {
                "username": "student_test",
                "email": "student@test.com",
                "password": "password123",
                "role": "student"
            },
            {
                "username": "teacher_test", 
                "email": "teacher@test.com",
                "password": "password123",
                "role": "teacher"
            },
            {
                "username": "parent_test",
                "email": "parent@test.com", 
                "password": "password123",
                "role": "parent"
            },
            {
                "username": "admin_test",
                "email": "admin@test.com",
                "password": "password123", 
                "role": "admin"
            }
        ]
        
        for user_data in test_users:
            # Vérifier si l'utilisateur existe déjà
            existing_user = db.query(User).filter(User.email == user_data["email"]).first()
            if existing_user:
                print(f"   ⚠️ Utilisateur {user_data['email']} existe déjà")
                # Mettre à jour le mot de passe
                existing_user.hashed_password = get_password_hash(user_data["password"])
                print(f"   ✅ Mot de passe mis à jour pour {user_data['email']}")
            else:
                # Créer le nouvel utilisateur
                hashed_password = get_password_hash(user_data["password"])
                new_user = User(
                    username=user_data["username"],
                    email=user_data["email"],
                    hashed_password=hashed_password,
                    role=user_data["role"]
                )
                db.add(new_user)
                print(f"   ✅ Utilisateur créé: {user_data['email']} (mot de passe: {user_data['password']})")
        
        db.commit()
        print("✅ Utilisateurs de test configurés avec succès!")
        
    except Exception as e:
        print(f"❌ Erreur lors de la création: {e}")
        db.rollback()
    finally:
        db.close()

def main():
    print("🔐 Correction des mots de passe - Najah AI")
    print("=" * 50)
    
    # Corriger le mot de passe de marie
    if fix_marie_password():
        # Tester la connexion
        test_login_marie()
    
    # Créer/mettre à jour les utilisateurs de test
    create_test_users()
    
    print("\n" + "=" * 50)
    print("🏁 Correction terminée")
    print("\n📋 Comptes disponibles:")
    print("   • marie.dubois@najah.ai (salmane123@) - Enseignant")
    print("   • student@test.com (password123) - Étudiant")
    print("   • teacher@test.com (password123) - Enseignant")
    print("   • parent@test.com (password123) - Parent")
    print("   • admin@test.com (password123) - Administrateur")

if __name__ == "__main__":
    main() 