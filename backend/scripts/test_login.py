#!/usr/bin/env python3
"""
Script de test pour vérifier l'endpoint de login
"""

import requests
import json

def test_login():
    """Test de l'endpoint de login"""
    url = "http://localhost:8000/api/v1/auth/login"
    
    # Test avec un compte enseignant
    data = {
        "email": "teacher@test.com",
        "password": "password123"
    }
    
    print("🔍 Test de l'endpoint de login...")
    print(f"URL: {url}")
    print(f"Data: {json.dumps(data, indent=2)}")
    
    try:
        response = requests.post(url, json=data, headers={"Content-Type": "application/json"})
        
        print(f"\n📊 Réponse:")
        print(f"Status Code: {response.status_code}")
        print(f"Headers: {dict(response.headers)}")
        print(f"Response Text: {response.text}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Login réussi!")
            print(f"Token: {result.get('access_token', 'N/A')[:20]}...")
            print(f"User: {result.get('name', 'N/A')}")
            print(f"Role: {result.get('role', 'N/A')}")
        else:
            print(f"❌ Échec du login")
            print(f"Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Erreur de connexion - Le backend n'est pas démarré")
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    test_login() 