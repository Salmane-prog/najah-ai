#!/usr/bin/env python3
"""
Script simple pour tester l'authentification
"""

import requests
import json

def test_endpoints_without_auth():
    """Teste les endpoints sans authentification"""
    
    base_url = "http://localhost:8000"
    
    print("🧪 TEST DES ENDPOINTS SANS AUTHENTIFICATION")
    print("=" * 50)
    
    # Endpoints à tester
    endpoints = [
        "/api/v1/badges/",
        "/api/v1/ai-advanced/recommendations",
        "/api/v1/reports/detailed",
        "/api/v1/reports/analytics",
        "/api/v1/reports/subject-progress",
        "/api/v1/homework/",
        "/api/v1/ai-advanced/tutoring/sessions",
        "/api/v1/ai-advanced/difficulty-detection"
    ]
    
    for endpoint in endpoints:
        try:
            response = requests.get(f"{base_url}{endpoint}")
            print(f"{endpoint}: {response.status_code} - {response.text[:100]}")
        except Exception as e:
            print(f"{endpoint}: Erreur - {str(e)}")

def test_with_fake_token():
    """Teste avec un token factice pour voir la réponse"""
    
    base_url = "http://localhost:8000"
    fake_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJzdHVkZW50MUB0ZXN0LmNvbSIsInVzZXJfaWQiOjQsInJvbGUiOiJzdHVkZW50IiwiZXhwIjoxNzM0Mzk5OTk5fQ.fake_signature"
    
    headers = {"Authorization": f"Bearer {fake_token}"}
    
    print("\n🔑 TEST AVEC TOKEN FACTICE")
    print("=" * 50)
    
    endpoints = [
        "/api/v1/badges/",
        "/api/v1/ai-advanced/recommendations"
    ]
    
    for endpoint in endpoints:
        try:
            response = requests.get(f"{base_url}{endpoint}", headers=headers)
            print(f"{endpoint}: {response.status_code} - {response.text[:100]}")
        except Exception as e:
            print(f"{endpoint}: Erreur - {str(e)}")

if __name__ == "__main__":
    print("🔍 DIAGNOSTIC DES ENDPOINTS")
    print("=" * 50)
    
    test_endpoints_without_auth()
    test_with_fake_token()
    
    print("\n" + "=" * 50)
    print("📋 ANALYSE:")
    print("- 401 Not authenticated = Endpoint fonctionne mais pas d'auth")
    print("- 404 Not found = Endpoint n'existe pas")
    print("- 500 Internal error = Erreur serveur")
    print("- 200 OK = Endpoint fonctionne avec auth")


