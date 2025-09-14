#!/usr/bin/env python3
"""
Script de débogage pour tester tous les endpoints de l'API
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000"

def test_endpoint(endpoint, method="GET", data=None):
    """Teste un endpoint spécifique"""
    url = f"{BASE_URL}{endpoint}"
    try:
        if method == "GET":
            response = requests.get(url, timeout=10)
        elif method == "POST":
            response = requests.post(url, json=data, timeout=10)
        
        print(f"✅ {method} {endpoint}")
        print(f"   Status: {response.status_code}")
        print(f"   Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            try:
                content = response.json()
                print(f"   Content: {json.dumps(content, indent=2)[:200]}...")
            except:
                print(f"   Content: {response.text[:200]}...")
        elif response.status_code == 401:
            print(f"   Content: {response.text}")
            print("   → Authentification requise (normal)")
        elif response.status_code == 403:
            print(f"   Content: {response.text}")
            print("   → Accès refusé (normal)")
        elif response.status_code == 404:
            print(f"   Content: {response.text}")
            print("   → Endpoint non trouvé (PROBLÈME)")
        else:
            print(f"   Content: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print(f"❌ {method} {endpoint}")
        print("   → Erreur de connexion - serveur non accessible")
    except requests.exceptions.Timeout:
        print(f"❌ {method} {endpoint}")
        print("   → Timeout - serveur trop lent")
    except Exception as e:
        print(f"❌ {method} {endpoint}")
        print(f"   → Erreur: {str(e)}")
    
    print()

def main():
    print("🔍 TEST DES ENDPOINTS DE L'API NAJAH AI")
    print("=" * 50)
    print(f"URL de base: {BASE_URL}")
    print(f"Timestamp: {datetime.now()}")
    print()
    
    # Test des endpoints de base
    print("📋 ENDPOINTS DE BASE")
    test_endpoint("/")
    test_endpoint("/health")
    test_endpoint("/docs")
    
    # Test des endpoints AI Advanced
    print("🤖 ENDPOINTS AI AVANCÉE")
    test_endpoint("/api/v1/ai-advanced/recommendations")
    test_endpoint("/api/v1/ai-advanced/tutoring/sessions")
    test_endpoint("/api/v1/ai-advanced/difficulty-detection")
    test_endpoint("/api/v1/ai-advanced/analytics/performance")
    test_endpoint("/api/v1/ai-advanced/analytics/engagement")
    
    # Test des endpoints Calendar
    print("📅 ENDPOINTS CALENDRIER")
    test_endpoint("/api/v1/calendar/events")
    test_endpoint("/api/v1/calendar/study-sessions")
    
    # Test des endpoints Reports
    print("📊 ENDPOINTS RAPPORTS")
    test_endpoint("/api/v1/reports/detailed")
    test_endpoint("/api/v1/reports/subject-progress")
    test_endpoint("/api/v1/reports/analytics")
    
    # Test des endpoints Homework
    print("📚 ENDPOINTS DEVOIRS")
    test_endpoint("/api/v1/homework/")
    
    # Test des endpoints Collaboration
    print("👥 ENDPOINTS COLLABORATION")
    test_endpoint("/api/v1/collaboration/study-groups")
    test_endpoint("/api/v1/collaboration/projects")
    
    print("=" * 50)
    print("✅ Test terminé")

if __name__ == "__main__":
    main() 