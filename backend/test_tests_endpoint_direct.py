#!/usr/bin/env python3
"""
Test direct de l'endpoint /tests/ pour identifier le problème 403
"""

import requests
import json

def test_tests_endpoint():
    print("🚀 Test direct de l'endpoint /tests/")
    print("=" * 50)
    
    # 1. Connexion et récupération du token
    print("1️⃣ Connexion et récupération du token...")
    login_data = {
        "email": "marizee.dubois@najah.ai",
        "password": "password123"
    }
    
    response = requests.post("http://localhost:8000/api/v1/auth/login", json=login_data)
    print(f"   Status: {response.status_code}")
    
    if response.status_code != 200:
        print("   ❌ Échec de la connexion")
        return
    
    data = response.json()
    token = data["access_token"]
    user_role = data["role"]
    user_id = data["id"]
    
    print(f"   ✅ Connexion réussie")
    print(f"   🔑 Token: {token[:50]}...")
    print(f"   👤 Rôle: {user_role}")
    print(f"   🆔 ID: {user_id}")
    
    # 2. Test de l'endpoint /tests/ (avec slash final)
    print("\n2️⃣ Test de l'endpoint /tests/ (avec slash final)...")
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    test_data = {
        "title": "Test Debug",
        "subject": "Debug",
        "description": "Test de debug",
        "difficulty_min": 1,
        "difficulty_max": 5,
        "estimated_duration": 10,
        "learning_objectives": "Debug",
        "total_questions": 5,
        "created_by": user_id,
        "questions": []
    }
    
    print(f"   📤 Envoi de la requête à: http://localhost:8000/api/v1/adaptive-evaluation/tests/")
    print(f"   📋 Données: {json.dumps(test_data, indent=2)}")
    
    response = requests.post(
        "http://localhost:8000/api/v1/adaptive-evaluation/tests/",
        headers=headers,
        json=test_data
    )
    
    print(f"\n   📥 Réponse reçue:")
    print(f"   Status: {response.status_code}")
    print(f"   Headers: {dict(response.headers)}")
    
    if response.status_code == 200:
        print(f"   ✅ Endpoint /tests/ fonctionne !")
        print(f"   📄 Body: {response.text}")
    else:
        print(f"   ❌ Endpoint /tests/ échoue avec status {response.status_code}")
        print(f"   📄 Body: {response.text}")
    
    # 3. Test de l'endpoint /tests (sans slash final)
    print("\n3️⃣ Test de l'endpoint /tests (sans slash final)...")
    
    response = requests.post(
        "http://localhost:8000/api/v1/adaptive-evaluation/tests",
        headers=headers,
        json=test_data
    )
    
    print(f"\n   📥 Réponse reçue:")
    print(f"   Status: {response.status_code}")
    print(f"   Headers: {dict(response.headers)}")
    
    if response.status_code == 200:
        print(f"   ✅ Endpoint /tests fonctionne !")
        print(f"   📄 Body: {response.text}")
    else:
        print(f"   ❌ Endpoint /tests échoue avec status {response.status_code}")
        print(f"   📄 Body: {response.text}")
    
    print("\n" + "=" * 50)
    print("🏁 Fin du test")

if __name__ == "__main__":
    test_tests_endpoint()











