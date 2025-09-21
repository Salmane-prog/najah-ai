#!/usr/bin/env python3
"""
Script pour tester l'authentification avec les utilisateurs existants
"""

import requests
import json

def test_existing_users_login():
    """Teste la connexion avec les utilisateurs existants de la base de données"""
    
    print("🧪 Test d'authentification avec les utilisateurs existants")
    print("=" * 70)
    
    # Utilisateurs de test trouvés dans ta base de données
    test_users = [
        {
            "email": "teacher1@najah.ai",
            "password": "teacher123",  # Mot de passe probable
            "description": "Marie Dupont (Teacher)"
        },
        {
            "email": "teacher2@najah.ai", 
            "password": "teacher123",
            "description": "Jean Martin (Teacher)"
        },
        {
            "email": "admin@najah.ai",
            "password": "admin123",  # Mot de passe probable
            "description": "Admin Najah (Admin)"
        }
    ]
    
    for user in test_users:
        print(f"\n🔐 Test de connexion pour: {user['description']}")
        print(f"   Email: {user['email']}")
        print(f"   Mot de passe: {user['password']}")
        
        try:
            # Appel à l'API de connexion
            response = requests.post(
                "http://localhost:8000/api/v1/auth/login",
                json={
                    "email": user['email'],
                    "password": user['password']
                }
            )
            
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                token = data.get("access_token")
                print(f"   ✅ Connexion réussie !")
                print(f"   Token: {token[:50]}...")
                
                # Tester le token avec l'endpoint protégé
                print(f"   🔍 Test de l'endpoint protégé...")
                headers = {"Authorization": f"Bearer {token}"}
                
                test_response = requests.post(
                    "http://localhost:8000/api/v1/ai-formative-evaluations/generate-evaluation/",
                    headers=headers,
                    json={
                        "title": "Test d'évaluation",
                        "subject": "Mathématiques",
                        "assessment_type": "project",
                        "description": "Test de génération d'évaluation formative",
                        "target_level": "intermediate",
                        "duration_minutes": 60,
                        "max_students": 30,
                        "learning_objectives": ["Compétence 1", "Compétence 2"],
                        "custom_requirements": "Aucune"
                    }
                )
                
                print(f"   Endpoint protégé - Status: {test_response.status_code}")
                
                if test_response.status_code == 200:
                    print(f"   🎯 SUCCÈS ! L'API fonctionne parfaitement !")
                    return token  # Retourner le premier token qui fonctionne
                else:
                    print(f"   ❌ Endpoint protégé échoue: {test_response.text}")
                    
            else:
                print(f"   ❌ Échec de la connexion: {response.text}")
                
        except Exception as e:
            print(f"   ❌ Erreur: {e}")
    
    print(f"\n❌ Aucun utilisateur n'a pu se connecter")
    return None

def test_with_known_password():
    """Test avec des mots de passe connus"""
    
    print(f"\n🔍 Test avec des mots de passe alternatifs...")
    
    # Essayer des mots de passe courants
    passwords = ["password", "123456", "admin", "teacher", "student", "najah", "test"]
    
    for password in passwords:
        print(f"   Test avec: {password}")
        
        try:
            response = requests.post(
                "http://localhost:8000/api/v1/auth/login",
                json={
                    "email": "teacher1@najah.ai",
                    "password": password
                }
            )
            
            if response.status_code == 200:
                print(f"   ✅ Mot de passe trouvé: {password}")
                return response.json().get("access_token")
            else:
                print(f"   ❌ {password} ne fonctionne pas")
                
        except Exception as e:
            print(f"   ❌ Erreur: {e}")
    
    return None

if __name__ == "__main__":
    print("🔐 Test d'authentification avec la base de données existante")
    print("=" * 80)
    
    # Test 1: Utilisateurs avec mots de passe probables
    token = test_existing_users_login()
    
    if not token:
        # Test 2: Mots de passe alternatifs
        token = test_with_known_password()
    
    if token:
        print(f"\n🎉 SUCCÈS ! Authentification réussie !")
        print(f"Token valide: {token[:50]}...")
        print(f"\n🔧 POUR TESTER LE FRONTEND :")
        print(f"1. Ouvre la console du navigateur (F12)")
        print(f"2. Exécute: localStorage.setItem('najah_token', '{token}')")
        print(f"3. Rafraîchis la page")
        print(f"4. Essaie de créer une évaluation formative")
    else:
        print(f"\n❌ ÉCHEC ! Aucune authentification n'a fonctionné")
        print(f"🔍 Vérification nécessaire des mots de passe dans la base de données")


















