#!/usr/bin/env python3
from core.database import SessionLocal
from models.user import User
from core.security import verify_password, get_password_hash

def check_user_passwords():
    """Vérifier les mots de passe des utilisateurs"""
    print("🔍 Vérification des mots de passe des utilisateurs...")
    
    db = SessionLocal()
    try:
        users = db.query(User).all()
        
        print(f"\n📋 {len(users)} utilisateurs trouvés:")
        
        for user in users:
            print(f"\n👤 Utilisateur: {user.username} ({user.email})")
            print(f"   Role: {user.role}")
            print(f"   Hash: {user.hashed_password[:30]}...")
            
            # Test avec des mots de passe courants
            test_passwords = [
                "password123",
                "salmane123@", 
                "test123",
                "password",
                "123456",
                user.username,  # Essayer le nom d'utilisateur comme mot de passe
                "admin",
                "teacher",
                "student"
            ]
            
            for password in test_passwords:
                if verify_password(password, user.hashed_password):
                    print(f"   ✅ Mot de passe trouvé: '{password}'")
                    break
            else:
                print(f"   ❌ Aucun mot de passe trouvé")
                
    finally:
        db.close()

def create_test_users():
    """Créer des utilisateurs de test avec des mots de passe connus"""
    print("\n🔧 Création d'utilisateurs de test...")
    
    db = SessionLocal()
    try:
        # Supprimer les anciens utilisateurs de test
        db.query(User).filter(User.email.in_([
            "student@test.com",
            "teacher@test.com", 
            "parent@test.com",
            "admin@test.com"
        ])).delete()
        
        # Créer de nouveaux utilisateurs de test
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
                continue
                
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
        print("✅ Utilisateurs de test créés avec succès!")
        
    except Exception as e:
        print(f"❌ Erreur lors de la création: {e}")
        db.rollback()
    finally:
        db.close()

def main():
    print("🔐 Diagnostic des mots de passe - Najah AI")
    print("=" * 50)
    
    check_user_passwords()
    create_test_users()
    
    print("\n" + "=" * 50)
    print("🏁 Diagnostic terminé")

if __name__ == "__main__":
    main() 