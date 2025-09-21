#!/usr/bin/env python3
"""
Script simple pour tester l'API des tests adaptatifs
"""

import requests
import json

# Configuration
BASE_URL = "http://localhost:8000"
API_BASE = f"{BASE_URL}/api/v1"

def test_api():
    """Tester l'API des tests adaptatifs"""
    try:
        print("🧪 Test de l'API des tests adaptatifs")
        print("=" * 50)
        
        # Test 1: Endpoint de base
        print("\n1️⃣ Test de l'endpoint de base...")
        response = requests.get(f"{BASE_URL}/")
        print(f"   Status: {response.status_code}")
        print(f"   Réponse: {response.text[:100]}...")
        
        # Test 2: Endpoint des tests (sans authentification)
        print("\n2️⃣ Test de l'endpoint des tests (sans auth)...")
        response = requests.get(f"{API_BASE}/teacher-adaptive-evaluation/tests/teacher/33")
        print(f"   Status: {response.status_code}")
        if response.status_code == 401:
            print("   ✅ Attendu: 401 Unauthorized (pas de token)")
        else:
            print(f"   Réponse: {response.text[:200]}...")
        
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
                    for i, test in enumerate(data['tests'][:3]):  # Afficher les 3 premiers
                        print(f"     Test {i+1}: ID={test.get('id')}, Titre={test.get('title')[:30]}...")
            else:
                print(f"   ❌ Erreur: {response.text[:200]}...")
        else:
            print(f"   ❌ Erreur de connexion: {auth_response.status_code}")
        
        print("\n✅ Test terminé")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    test_api()





















