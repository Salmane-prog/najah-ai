#!/usr/bin/env python3
"""
Script pour tester l'authentification et obtenir un token
"""

import requests
import json

def test_auth():
    """Tester l'authentification."""
    base_url = "http://localhost:8000"
    
    print("=== TEST D'AUTHENTIFICATION ===")
    
    # Test de connexion avec salmane
    login_data = {
        "email": "marie.dubois@najah.ai",
        "password": "password123"
    }
    
    try:
        response = requests.post(f"{base_url}/api/v1/auth/login", json=login_data)
        print(f"📡 Login response: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Connexion réussie!")
            print(f"   Token: {data.get('access_token', 'N/A')[:20]}...")
            print(f"   User ID: {data.get('id', 'N/A')}")
            print(f"   Role: {data.get('role', 'N/A')}")
            
            # Tester l'endpoint de messagerie avec le token
            token = data.get('access_token')
            headers = {
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            }
            
            response = requests.get(f"{base_url}/api/v1/teacher_messaging/conversations", headers=headers)
            print(f"📨 Messagerie avec token: {response.status_code}")
            
            if response.status_code == 200:
                conversations = response.json()
                print(f"✅ Conversations récupérées: {len(conversations.get('conversations', []))}")
                for conv in conversations.get('conversations', []):
                    print(f"   - {conv.get('student', {}).get('name', 'Unknown')}")
            else:
                print(f"❌ Erreur messagerie: {response.status_code}")
                print(f"   Response: {response.text}")
                
        else:
            print(f"❌ Erreur de connexion: {response.status_code}")
            print(f"   Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")

if __name__ == "__main__":
    test_auth() 