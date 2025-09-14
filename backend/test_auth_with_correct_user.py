#!/usr/bin/env python3
"""
Script pour tester l'authentification avec l'utilisateur correct
"""

import requests
import json

def test_auth_with_correct_user():
    """Tester l'authentification avec l'utilisateur correct"""
    
    base_url = "http://localhost:8000"
    
    # Test avec l'utilisateur salmane
    print("🔍 Test d'authentification avec salmane.hajouji@najah.ai")
    
    # Essayer différents mots de passe
    test_passwords = [
        "password123",
        "password",
        "123456",
        "student1",  # Le username
        "salmane",
        "hajouji",
        "najah",
        "test"
    ]
    
    for password in test_passwords:
        print(f"\n🔑 Test avec le mot de passe: '{password}'")
        
        try:
            login_data = {
                "email": "salmane.hajouji@najah.ai",
                "password": password
            }
            
            login_response = requests.post(f"{base_url}/api/v1/auth/login", json=login_data)
            print(f"   Status: {login_response.status_code}")
            
            if login_response.status_code == 200:
                print("   ✅ Connexion réussie!")
                token_data = login_response.json()
                token = token_data.get("access_token")
                
                if token:
                    print(f"   Token: {token[:50]}...")
                    
                    # Test avec le token
                    headers = {"Authorization": f"Bearer {token}"}
                    response = requests.get(f"{base_url}/api/v1/student-organization/study-sessions", headers=headers)
                    print(f"   Study sessions status: {response.status_code}")
                    print(f"   Study sessions response: {response.text[:200]}")
                    
                    # Test de création de session
                    session_data = {
                        "title": "Test Session",
                        "description": "Description de test",
                        "subject": "Mathématiques",
                        "start_time": "2025-01-20T10:00:00",
                        "end_time": "2025-01-20T12:00:00",
                        "duration": 120,
                        "goals": ["Objectif 1", "Objectif 2"],
                        "notes": "Notes de test"
                    }
                    
                    create_response = requests.post(
                        f"{base_url}/api/v1/student-organization/study-sessions", 
                        headers=headers,
                        json=session_data
                    )
                    print(f"   Create session status: {create_response.status_code}")
                    print(f"   Create session response: {create_response.text[:200]}")
                    
                    return  # Arrêter après le premier succès
                else:
                    print("   ❌ Pas de token dans la réponse")
            else:
                print(f"   ❌ Erreur: {login_response.text}")
                
        except Exception as e:
            print(f"   ❌ Erreur: {str(e)}")

if __name__ == "__main__":
    test_auth_with_correct_user() 