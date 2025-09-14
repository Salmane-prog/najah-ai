#!/usr/bin/env python3
import requests
import json
import traceback
from datetime import datetime

def test_backend_connection():
    """Test de connexion au backend"""
    print("🔍 Test de connexion au backend...")
    try:
        response = requests.get("http://localhost:8000/", timeout=5)
        print(f"✅ Backend accessible: {response.status_code}")
        return True
    except Exception as e:
        print(f"❌ Backend inaccessible: {e}")
        return False

def test_login_endpoint():
    """Test de l'endpoint de connexion"""
    print("\n🔐 Test de l'endpoint de connexion...")
    
    # Test avec un utilisateur existant
    test_cases = [
        {
            "email": "marie.dubois@najah.ai",
            "password": "salmane123@",
            "description": "Utilisateur existant"
        },
        {
            "email": "student@test.com", 
            "password": "password123",
            "description": "Compte de test étudiant"
        },
        {
            "email": "teacher@test.com",
            "password": "password123", 
            "description": "Compte de test enseignant"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n--- Test {i}: {test_case['description']} ---")
        try:
            response = requests.post(
                "http://localhost:8000/api/v1/auth/login",
                json={
                    "email": test_case["email"],
                    "password": test_case["password"]
                },
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            
            print(f"Status: {response.status_code}")
            print(f"Headers: {dict(response.headers)}")
            
            try:
                response_data = response.json()
                print(f"Response JSON: {json.dumps(response_data, indent=2)}")
            except json.JSONDecodeError:
                print(f"Response Text: {response.text}")
                
            if response.status_code == 200:
                print("✅ Connexion réussie!")
            else:
                print("❌ Échec de connexion")
                
        except Exception as e:
            print(f"❌ Erreur: {e}")
            print(f"Traceback: {traceback.format_exc()}")

def test_database_connection():
    """Test de connexion à la base de données"""
    print("\n🗄️ Test de connexion à la base de données...")
    try:
        from core.database import SessionLocal
        from models.user import User
        
        db = SessionLocal()
        try:
            users = db.query(User).all()
            print(f"✅ Base de données accessible: {len(users)} utilisateurs trouvés")
            
            for user in users[:3]:  # Afficher les 3 premiers utilisateurs
                print(f"  - {user.email} (role: {user.role})")
                
        finally:
            db.close()
            
    except Exception as e:
        print(f"❌ Erreur base de données: {e}")
        print(f"Traceback: {traceback.format_exc()}")

def test_security_functions():
    """Test des fonctions de sécurité"""
    print("\n🔒 Test des fonctions de sécurité...")
    try:
        from core.security import get_password_hash, verify_password, create_access_token
        
        # Test de hashage
        test_password = "test123"
        hashed = get_password_hash(test_password)
        print(f"✅ Hashage de mot de passe: {hashed[:20]}...")
        
        # Test de vérification
        is_valid = verify_password(test_password, hashed)
        print(f"✅ Vérification de mot de passe: {is_valid}")
        
        # Test de création de token
        token_data = {"sub": "test@example.com", "role": "student"}
        token = create_access_token(token_data)
        print(f"✅ Création de token: {token[:20]}...")
        
    except Exception as e:
        print(f"❌ Erreur fonctions de sécurité: {e}")
        print(f"Traceback: {traceback.format_exc()}")

def main():
    print("🚀 Diagnostic d'authentification - Najah AI")
    print("=" * 50)
    print(f"Date: {datetime.now()}")
    
    # Tests
    test_backend_connection()
    test_database_connection()
    test_security_functions()
    test_login_endpoint()
    
    print("\n" + "=" * 50)
    print("🏁 Diagnostic terminé")

if __name__ == "__main__":
    main() 