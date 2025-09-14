#!/usr/bin/env python3
"""
Script pour tester l'authentification des sessions d'étude
"""

import requests
import json

def test_study_sessions_auth():
    """Tester l'authentification pour les sessions d'étude"""
    
    base_url = "http://localhost:8000"
    
    # 1. Test sans authentification (doit retourner 401)
    print("🔍 Test 1: Sans authentification")
    try:
        response = requests.get(f"{base_url}/api/v1/student-organization/study-sessions")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text[:200]}")
    except Exception as e:
        print(f"   Erreur: {str(e)}")
    
    print()
    
    # 2. Test avec authentification (utiliser un étudiant)
    print("🔍 Test 2: Avec authentification")
    try:
        # Login avec un étudiant
        login_data = {
            "email": "salmane.hajouji@najah.ai",
            "password": "password123"
        }
        
        login_response = requests.post(f"{base_url}/api/v1/auth/login", json=login_data)
        print(f"   Login status: {login_response.status_code}")
        
        if login_response.status_code == 200:
            token_data = login_response.json()
            token = token_data.get("access_token")
            
            if token:
                print(f"   Token obtenu: {token[:50]}...")
                
                # Test avec le token
                headers = {"Authorization": f"Bearer {token}"}
                response = requests.get(f"{base_url}/api/v1/student-organization/study-sessions", headers=headers)
                print(f"   Study sessions status: {response.status_code}")
                print(f"   Study sessions response: {response.text[:200]}")
            else:
                print("   ❌ Pas de token dans la réponse")
        else:
            print(f"   ❌ Erreur de login: {login_response.text}")
            
    except Exception as e:
        print(f"   Erreur: {str(e)}")
    
    print()
    
    # 3. Test de création de session
    print("🔍 Test 3: Création de session d'étude")
    try:
        # Login avec un étudiant
        login_data = {
            "email": "salmane.hajouji@najah.ai",
            "password": "password123"
        }
        
        login_response = requests.post(f"{base_url}/api/v1/auth/login", json=login_data)
        
        if login_response.status_code == 200:
            token_data = login_response.json()
            token = token_data.get("access_token")
            
            if token:
                headers = {"Authorization": f"Bearer {token}"}
                
                # Données de test pour une session
                session_data = {
                    "title": "Test Session",
                    "description": "Description de test",
                    "subject": "Mathématiques",
                    "start_time": "2025-01-20T10:00:00",
                    "end_time": "2025-01-20T12:00:00",
                    "duration": 120,
                    "goals": ["Objectif 1", "Objectif 2"],
                    "notes": "Notes de test"
                }
                
                response = requests.post(
                    f"{base_url}/api/v1/student-organization/study-sessions", 
                    headers=headers,
                    json=session_data
                )
                print(f"   Create session status: {response.status_code}")
                print(f"   Create session response: {response.text[:200]}")
            else:
                print("   ❌ Pas de token")
        else:
            print(f"   ❌ Erreur de login: {login_response.text}")
            
    except Exception as e:
        print(f"   Erreur: {str(e)}")

if __name__ == "__main__":
    test_study_sessions_auth() 