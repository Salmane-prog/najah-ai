#!/usr/bin/env python3
"""
Script pour tester l'accès à l'API depuis le frontend
"""

import requests
import json

# Configuration
BASE_URL = "http://localhost:8000"
API_BASE = f"{BASE_URL}/api/v1"

def test_frontend_access():
    """Tester l'accès à l'API depuis le frontend"""
    try:
        print("🧪 Test d'accès à l'API depuis le frontend")
        print("=" * 50)
        
        # Test 1: Endpoint de base (sans auth)
        print("\n1️⃣ Test de l'endpoint de base...")
        response = requests.get(f"{BASE_URL}/")
        print(f"   Status: {response.status_code}")
        print(f"   Réponse: {response.text[:100]}...")
        
        # Test 2: Endpoint des tests (sans auth - doit retourner 401/403)
        print("\n2️⃣ Test de l'endpoint des tests (sans auth)...")
        response = requests.get(f"{API_BASE}/teacher-adaptive-evaluation/tests/teacher/33")
        print(f"   Status: {response.status_code}")
        if response.status_code in [401, 403]:
            print("   ✅ Attendu: Accès refusé sans authentification")
        else:
            print(f"   ⚠️ Réponse inattendue: {response.text[:200]}...")
        
        # Test 3: Endpoint avec authentification
        print("\n3️⃣ Test de l'endpoint avec authentification...")
        
        # Se connecter
        login_data = {
            "email": "marizee.dubois@najah.ai",
            "password": "password123"
        }
        
        auth_response = requests.post(f"{API_BASE}/auth/login", json=login_data)
        if auth_response.status_code == 200:
            token = auth_response.json().get("access_token")
            print("   ✅ Connexion réussie")
            
            # Tester l'endpoint des tests
            headers = {"Authorization": f"Bearer {token}"}
            response = requests.get(f"{API_BASE}/teacher-adaptive-evaluation/tests/teacher/33", headers=headers)
            
            print(f"   Status: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ Données reçues!")
                print(f"   Success: {data.get('success')}")
                print(f"   Tests: {len(data.get('tests', []))}")
                
                if data.get('tests'):
                    print("   📋 Détails des tests:")
                    for i, test in enumerate(data['tests'][:3]):
                        print(f"     Test {i+1}: ID={test.get('id')}, Titre={test.get('title')[:30]}...")
                        print(f"       - Matière: {test.get('subject')}")
                        print(f"       - Actif: {test.get('is_active')}")
            else:
                print(f"   ❌ Erreur: {response.text[:200]}...")
        else:
            print(f"   ❌ Erreur de connexion: {auth_response.status_code}")
        
        print("\n🎯 Conclusion:")
        print("Si l'API fonctionne mais le frontend ne charge pas, le problème est dans:")
        print("1. L'authentification côté frontend")
        print("2. Le format des données")
        print("3. Les erreurs JavaScript")
        
        print("\n✅ Test terminé")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    test_frontend_access()





















