#!/usr/bin/env python3
"""
Script pour tester l'authentification frontend
"""

import requests
import json

def test_frontend_auth():
    """Tester l'authentification frontend"""
    base_url = "http://localhost:8000"
    
    print("🔍 Test de l'authentification frontend...")
    
    # Test de l'endpoint /me sans token
    print("\n1. 📋 Test /me sans token")
    try:
        response = requests.get(f"{base_url}/api/v1/auth/me")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text}")
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
    
    # Test de l'endpoint conversations sans token
    print("\n2. 💬 Test conversations sans token")
    try:
        response = requests.get(f"{base_url}/api/v1/teacher_messaging/conversations")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text}")
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
    
    # Test de login pour obtenir un token
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
            
            # Test des conversations avec token
            print("\n4. 💬 Test conversations avec token")
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
    test_frontend_auth() 