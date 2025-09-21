#!/usr/bin/env python3
"""
Test de l'endpoint simple analytics
"""

import requests

print("🧪 Test de l'endpoint simple analytics")
print("=" * 50)

BASE_URL = "http://localhost:8000"

try:
    # Test sans authentification
    print("📊 Test 1: Endpoint simple sans authentification")
    response = requests.get(f"{BASE_URL}/api/v1/analytics/test")
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"   ✅ Succès: {data}")
    else:
        print(f"   ❌ Erreur: {response.text}")
    
    # Test avec authentification
    print(f"\n📊 Test 2: Endpoint simple avec authentification")
    
    login = requests.post(f"{BASE_URL}/api/v1/auth/login", json={
        "email": "marizee.dubois@najah.ai",
        "password": "password123"
    })
    
    if login.status_code == 200:
        token = login.json().get("access_token")
        headers = {"Authorization": f"Bearer {token}"}
        print("   ✅ Login réussi")
        
        response = requests.get(f"{BASE_URL}/api/v1/analytics/test", headers=headers)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Succès: {data}")
        else:
            print(f"   ❌ Erreur: {response.text}")
    else:
        print(f"   ❌ Login échoué: {login.status_code}")
    
    print(f"\n🔍 Résumé:")
    print(f"   - Si l'endpoint simple fonctionne, le problème est dans les autres endpoints")
    print(f"   - Si l'endpoint simple échoue aussi, il y a un problème de configuration")

except Exception as e:
    print(f"❌ Erreur générale: {e}")

print(f"\n✅ Test terminé")









