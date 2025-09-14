#!/usr/bin/env python3
"""
Test spécifique de l'endpoint /tests/ qui pose problème
"""

import requests
import json

# Configuration
BASE_URL = "http://localhost:8000"
PROBLEMATIC_ENDPOINT = f"{BASE_URL}/api/v1/adaptive-evaluation/tests/"

def test_problematic_endpoint():
    """Test de l'endpoint problématique /tests/"""
    
    print("🚨 Test de l'endpoint problématique /tests/")
    print("=" * 60)
    
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
    
    # 2. Test de l'endpoint problématique
    print("\n2️⃣ Test de l'endpoint /tests/...")
    headers = {"Authorization": f"Bearer {access_token}"}
    
    # Données de test minimales
    test_data = {
        "title": "Test Debug - Endpoint",
        "subject": "Debug",
        "description": "Test de débogage de l'endpoint",
        "difficulty_min": 1,
        "difficulty_max": 5,
        "estimated_duration": 15,
        "total_questions": 5,
        "adaptation_type": "hybrid",
        "learning_objectives": "Debug"
    }
    
    try:
        print(f"   📤 Envoi de la requête à: {PROBLEMATIC_ENDPOINT}")
        print(f"   📋 Données: {json.dumps(test_data, indent=2)}")
        print(f"   🔑 Headers: {json.dumps(headers, indent=2)}")
        
        response = requests.post(PROBLEMATIC_ENDPOINT, json=test_data, headers=headers)
        
        print(f"\n   📥 Réponse reçue:")
        print(f"   Status: {response.status_code}")
        print(f"   Headers: {dict(response.headers)}")
        print(f"   Body: {response.text}")
        
        if response.status_code == 200:
            print("   ✅ Endpoint /tests/ fonctionne !")
            return True
        elif response.status_code == 403:
            print("   ❌ Erreur 403: Accès refusé")
            print("   💡 Problème d'autorisation malgré l'authentification")
            return False
        elif response.status_code == 401:
            print("   ❌ Erreur 401: Non authentifié")
            print("   💡 Problème avec le token")
            return False
        else:
            print(f"   ❌ Erreur {response.status_code}: {response.text}")
            return False
            
    except Exception as e:
        print(f"   ❌ Erreur lors de la requête: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Test de l'endpoint problématique")
    print(f"📍 URL: {PROBLEMATIC_ENDPOINT}")
    
    success = test_problematic_endpoint()
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 Endpoint /tests/ fonctionne !")
    else:
        print("❌ Endpoint /tests/ a des problèmes")
    
    print("🏁 Fin du test")
