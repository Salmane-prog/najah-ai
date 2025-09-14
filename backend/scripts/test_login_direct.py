#!/usr/bin/env python3
"""
Script pour tester directement l'authentification
"""

import requests
import hashlib

def test_login():
    print("🔐 Test d'authentification...")
    
    BASE_URL = "http://localhost:8000"
    LOGIN_URL = f"{BASE_URL}/api/v1/auth/login"
    
    # Test avec différents utilisateurs
    test_users = [
        {"email": "teacher@test.com", "password": "password123"},
        {"email": "admin@najah.ai", "password": "password123"},
        {"email": "marie.dubois@najah.ai", "password": "password123"},
        {"email": "student@test.com", "password": "password123"}
    ]
    
    for user in test_users:
        print(f"\n🧪 Test avec {user['email']}...")
        
        try:
            response = requests.post(LOGIN_URL, json=user)
            print(f"   Status: {response.status_code}")
            print(f"   Réponse: {response.text}")
            
            if response.status_code == 200:
                data = response.json()
                token = data.get("access_token")
                print(f"   ✅ Login réussi! Token: {token[:20]}...")
                
                # Test de l'endpoint dashboard
                headers = {
                    "Authorization": f"Bearer {token}",
                    "Content-Type": "application/json"
                }
                
                dashboard_response = requests.get(f"{BASE_URL}/api/v1/dashboard/dashboard-data", headers=headers)
                print(f"   Dashboard status: {dashboard_response.status_code}")
                
                if dashboard_response.status_code == 200:
                    dashboard_data = dashboard_response.json()
                    overview = dashboard_data.get("overview", {})
                    print(f"   📊 Overview:")
                    print(f"      - Classes: {overview.get('classes', 0)}")
                    print(f"      - Élèves: {overview.get('students', 0)}")
                    print(f"      - Quiz: {overview.get('quizzes', 0)}")
                    print(f"      - Progression: {overview.get('average_progression', 0)}%")
                
                return user['email']  # Retourner l'utilisateur qui fonctionne
                
        except Exception as e:
            print(f"   ❌ Erreur: {e}")
    
    return None

if __name__ == "__main__":
    working_user = test_login()
    if working_user:
        print(f"\n✅ Utilisateur fonctionnel: {working_user}")
    else:
        print(f"\n❌ Aucun utilisateur ne fonctionne") 