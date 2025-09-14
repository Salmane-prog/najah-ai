#!/usr/bin/env python3
"""
Script pour tester le statut d'authentification
"""

import requests
import json

def test_auth_status():
    """Tester le statut d'authentification"""
    base_url = "http://localhost:8000"
    
    print("🔍 Test du statut d'authentification...")
    
    # 1. Test sans token
    print("\n1. 📋 Test sans token")
    try:
        response = requests.get(f"{base_url}/api/v1/auth/me")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text}")
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
    
    # 2. Test avec un token invalide
    print("\n2. 📋 Test avec token invalide")
    try:
        response = requests.get(
            f"{base_url}/api/v1/auth/me",
            headers={"Authorization": "Bearer invalid_token"}
        )
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text}")
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
    
    # 3. Test de login pour obtenir un token valide
    print("\n3. 🔐 Test de login")
    try:
        login_data = {
            "email": "teacher@test.com",
            "password": "password123"
        }
        
        response = requests.post(f"{base_url}/api/v1/auth/login", json=login_data)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            token = data.get("access_token")
            print(f"   ✅ Login réussi")
            print(f"   Token: {token[:20]}...")
            print(f"   Role: {data.get('role')}")
            print(f"   User ID: {data.get('id')}")
            
            # 4. Test avec token valide
            print("\n4. 📋 Test avec token valide")
            response = requests.get(
                f"{base_url}/api/v1/auth/me",
                headers={"Authorization": f"Bearer {token}"}
            )
            print(f"   Status: {response.status_code}")
            print(f"   Response: {response.text}")
            
            # 5. Test des conversations avec token valide
            print("\n5. 💬 Test des conversations")
            response = requests.get(
                f"{base_url}/api/v1/teacher_messaging/conversations",
                headers={"Authorization": f"Bearer {token}"}
            )
            print(f"   Status: {response.status_code}")
            print(f"   Response: {response.text}")
            
        else:
            print(f"   ❌ Login échoué: {response.text}")
            
    except Exception as e:
        print(f"   ❌ Erreur: {e}")

if __name__ == "__main__":
    test_auth_status() 