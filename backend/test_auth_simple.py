#!/usr/bin/env python3
"""
Script de test simple pour vérifier l'authentification et les endpoints d'activité
"""

import requests
import json

# Configuration
BASE_URL = "http://localhost:8000"
TEST_EMAIL = "test@student.com"
TEST_PASSWORD = "password123"

def test_auth_and_activity():
    """Test complet de l'authentification et des endpoints d'activité"""
    
    print("=== Test d'authentification et d'activité ===\n")
    
    # 1. Test de connexion
    print("1. Test de connexion...")
    try:
        login_data = {
            "email": TEST_EMAIL,
            "password": TEST_PASSWORD
        }
        
        response = requests.post(f"{BASE_URL}/api/v1/auth/login", json=login_data)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            token = data.get("access_token")
            user_id = data.get("id")
            print(f"   Connexion réussie! User ID: {user_id}")
            print(f"   Token: {token[:20]}...")
        else:
            print(f"   Erreur de connexion: {response.text}")
            return
            
    except Exception as e:
        print(f"   Erreur lors de la connexion: {e}")
        return
    
    # 2. Test de l'endpoint d'activité récente
    print("\n2. Test de l'endpoint d'activité récente...")
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{BASE_URL}/api/v1/activity/user/{user_id}/recent?limit=5", headers=headers)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   Activités récupérées: {len(data.get('activities', []))}")
            print(f"   Données: {json.dumps(data, indent=2, default=str)}")
        else:
            print(f"   Erreur: {response.text}")
            
    except Exception as e:
        print(f"   Erreur lors de la récupération des activités: {e}")
    
    # 3. Test de l'endpoint de statistiques
    print("\n3. Test de l'endpoint de statistiques...")
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{BASE_URL}/api/v1/activity/user/{user_id}/stats?period=week", headers=headers)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   Statistiques récupérées avec succès")
            print(f"   Données: {json.dumps(data, indent=2, default=str)}")
        else:
            print(f"   Erreur: {response.text}")
            
    except Exception as e:
        print(f"   Erreur lors de la récupération des statistiques: {e}")
    
    # 4. Test de l'endpoint de vérification du token
    print("\n4. Test de vérification du token...")
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{BASE_URL}/api/v1/auth/me", headers=headers)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   Token valide! User: {data.get('email')}")
        else:
            print(f"   Erreur: {response.text}")
            
    except Exception as e:
        print(f"   Erreur lors de la vérification du token: {e}")

if __name__ == "__main__":
    test_auth_and_activity()
