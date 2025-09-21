#!/usr/bin/env python3
"""
Test de l'endpoint /test-tests
"""

import requests
import json

# Configuration
BASE_URL = "http://localhost:8000"
TEST_ENDPOINT = f"{BASE_URL}/api/v1/adaptive-evaluation/test-tests"

def test_test_tests_endpoint():
    """Test de l'endpoint /test-tests"""
    
    print("🧪 Test de l'endpoint /test-tests")
    print("=" * 50)
    
    # 1. Connexion et récupération du token
    print("1️⃣ Connexion et récupération du token...")
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
            user_role = token_data.get("role")
            user_id = token_data.get("id")
            print(f"   ✅ Connexion réussie")
            print(f"   🔑 Token: {access_token[:50]}...")
            print(f"   👤 Rôle: {user_role}")
            print(f"   🆔 ID: {user_id}")
        else:
            print(f"   ❌ Échec de la connexion: {login_response.text}")
            return False
            
    except Exception as e:
        print(f"   ❌ Erreur lors de la connexion: {e}")
        return False
    
    # 2. Test de l'endpoint /test-tests
    print("\n2️⃣ Test de l'endpoint /test-tests...")
    headers = {"Authorization": f"Bearer {access_token}"}
    
    test_data = {"test": "data", "message": "Test de l'endpoint /test-tests"}
    
    try:
        print(f"   📤 Envoi de la requête à: {TEST_ENDPOINT}")
        print(f"   📋 Données: {json.dumps(test_data, indent=2)}")
        
        response = requests.post(TEST_ENDPOINT, json=test_data, headers=headers)
        
        print(f"\n   📥 Réponse reçue:")
        print(f"   Status: {response.status_code}")
        print(f"   Body: {response.text}")
        
        if response.status_code == 200:
            print("   ✅ Endpoint /test-tests fonctionne !")
            return True
        else:
            print(f"   ❌ Erreur {response.status_code}: {response.text}")
            return False
            
    except Exception as e:
        print(f"   ❌ Erreur lors de la requête: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Test de l'endpoint /test-tests")
    print(f"📍 URL: {TEST_ENDPOINT}")
    
    success = test_test_tests_endpoint()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 Endpoint /test-tests fonctionne !")
    else:
        print("❌ Endpoint /test-tests a des problèmes")
    
    print("🏁 Fin du test")













