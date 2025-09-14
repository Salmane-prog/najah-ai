#!/usr/bin/env python3
"""
Test de l'endpoint POST de test
"""

import requests
import json

# Configuration
BASE_URL = "http://localhost:8000"
TEST_ENDPOINT = f"{BASE_URL}/api/v1/adaptive-evaluation/test-post"

def test_post_endpoint():
    """Test de l'endpoint POST de test"""
    
    print("🧪 Test de l'endpoint POST de test")
    print("=" * 50)
    
    # 1. Test sans authentification
    print("1️⃣ Test sans authentification...")
    try:
        response = requests.post(TEST_ENDPOINT, json={"test": "data"})
        print(f"   Status: {response.status_code}")
        if response.status_code == 401:
            print("   ✅ Endpoint protégé (401 attendu)")
        else:
            print(f"   ⚠️ Status inattendu: {response.status_code}")
            print(f"   Réponse: {response.text}")
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
    
    # 2. Connexion et récupération du token
    print("\n2️⃣ Connexion et récupération du token...")
    login_data = {
        "email": "marizee.dubois@najah.ai",
        "password": "password123"
    }
    
    try:
        login_response = requests.post(f"{BASE_URL}/api/v1/auth/login", json=login_data)
        print(f"   Status: {login_response.status_code}")
        
        if login_response.status_code == 200:
            token_data = login_response.json()
            access_token = token_data.get("access_token")
            print(f"   ✅ Connexion réussie")
            print(f"   🔑 Token: {access_token[:50]}...")
        else:
            print(f"   ❌ Échec de la connexion: {login_response.text}")
            return False
            
    except Exception as e:
        print(f"   ❌ Erreur lors de la connexion: {e}")
        return False
    
    # 3. Test avec authentification
    print("\n3️⃣ Test avec authentification...")
    headers = {"Authorization": f"Bearer {access_token}"}
    
    try:
        response = requests.post(TEST_ENDPOINT, json={"test": "data"}, headers=headers)
        print(f"   Status: {response.status_code}")
        print(f"   Réponse: {response.text}")
        
        if response.status_code == 200:
            print("   ✅ Endpoint POST fonctionne !")
            return True
        else:
            print(f"   ❌ Erreur {response.status_code}")
            return False
            
    except Exception as e:
        print(f"   ❌ Erreur lors de la requête: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Test de l'endpoint POST")
    print(f"📍 URL: {TEST_ENDPOINT}")
    
    success = test_post_endpoint()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 Test POST réussi !")
    else:
        print("❌ Test POST échoué")
    
    print("🏁 Fin du test") 