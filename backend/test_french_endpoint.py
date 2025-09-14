#!/usr/bin/env python3
"""
Script pour tester l'endpoint français
"""

import requests
import json

def test_french_endpoint():
    print("=== TEST ENDPOINT FRANÇAIS ===")
    
    base_url = "http://localhost:8000"
    
    # Test 1: Endpoint sans authentification
    print("\n🧪 Test 1: Endpoint sans authentification")
    try:
        response = requests.post(f"{base_url}/api/v1/french/initial-assessment/student/start")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
    except Exception as e:
        print(f"Erreur: {e}")
    
    # Test 2: Endpoint avec token invalide
    print("\n🧪 Test 2: Endpoint avec token invalide")
    try:
        headers = {
            'Authorization': 'Bearer invalid_token',
            'Content-Type': 'application/json'
        }
        response = requests.post(f"{base_url}/api/v1/french/initial-assessment/student/start", headers=headers)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
    except Exception as e:
        print(f"Erreur: {e}")
    
    # Test 3: Vérifier que l'endpoint existe
    print("\n🧪 Test 3: Vérifier l'existence de l'endpoint")
    try:
        response = requests.options(f"{base_url}/api/v1/french/initial-assessment/student/start")
        print(f"Status: {response.status_code}")
        print(f"Headers: {dict(response.headers)}")
    except Exception as e:
        print(f"Erreur: {e}")
    
    print("\n✅ Test terminé")

if __name__ == "__main__":
    test_french_endpoint()

