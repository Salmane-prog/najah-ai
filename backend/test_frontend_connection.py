#!/usr/bin/env python3
"""
Script de test pour vérifier la connectivité entre le frontend et le backend
"""

import requests
import json

def test_backend_connectivity():
    """Tester la connectivité du backend"""
    print("🔍 Test de connectivité du backend...")
    
    try:
        # Test de base
        response = requests.get("http://localhost:8000/", timeout=5)
        print(f"✅ Backend accessible: {response.status_code}")
        print(f"   Réponse: {response.json()}")
        
        # Test CORS
        response = requests.options("http://localhost:8000/api/v1/auth/login", timeout=5)
        print(f"✅ CORS configuré: {response.status_code}")
        print(f"   Headers CORS: {dict(response.headers)}")
        
        return True
        
    except requests.exceptions.ConnectionError:
        print("❌ Impossible de se connecter au backend")
        return False
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")
        return False

def test_api_endpoints():
    """Tester les endpoints API spécifiques"""
    print("\n🔍 Test des endpoints API...")
    
    endpoints = [
        "/api/v1/activity/user/1/recent",
        "/api/v1/reports/subject-progress",
        "/api/v1/ai_advanced/recommendations",
        "/api/v1/calendar/events",
        "/api/v1/collaboration/study-groups",
        "/api/v1/homework/student/1",
        "/api/v1/assessments/student/1"
    ]
    
    for endpoint in endpoints:
        try:
            response = requests.get(f"http://localhost:8000{endpoint}", timeout=5)
            if response.status_code == 401:
                print(f"✅ {endpoint}: Authentification requise (normal)")
            elif response.status_code == 404:
                print(f"⚠️  {endpoint}: Endpoint non trouvé")
            else:
                print(f"✅ {endpoint}: {response.status_code}")
        except Exception as e:
            print(f"❌ {endpoint}: Erreur - {e}")

def test_frontend_simulation():
    """Simuler une requête frontend"""
    print("\n🔍 Simulation d'une requête frontend...")
    
    headers = {
        'Origin': 'http://localhost:3000',
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    
    try:
        response = requests.get(
            "http://localhost:8000/api/v1/activity/user/1/recent",
            headers=headers,
            timeout=5
        )
        print(f"✅ Requête frontend simulée: {response.status_code}")
        print(f"   Headers de réponse: {dict(response.headers)}")
        
        # Vérifier les headers CORS
        cors_headers = ['access-control-allow-origin', 'access-control-allow-methods', 'access-control-allow-headers']
        for header in cors_headers:
            if header in response.headers:
                print(f"   {header}: {response.headers[header]}")
            else:
                print(f"   ⚠️ {header}: manquant")
                
    except Exception as e:
        print(f"❌ Erreur lors de la simulation frontend: {e}")

if __name__ == "__main__":
    print("🚀 Test de connectivité Frontend-Backend\n")
    
    # Test 1: Connectivité de base
    if test_backend_connectivity():
        # Test 2: Endpoints API
        test_api_endpoints()
        
        # Test 3: Simulation frontend
        test_frontend_simulation()
        
        print("\n✅ Tests terminés!")
    else:
        print("\n❌ Le backend n'est pas accessible. Vérifiez qu'il est démarré.")











