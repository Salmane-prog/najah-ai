#!/usr/bin/env python3
"""
Script pour tester les endpoints corrigés
"""

import requests
import json
from typing import Dict, List, Any

# Configuration
BASE_URL = "http://localhost:8000/api/v1"
TEACHER_CREDENTIALS = {
    "username": "salmane",
    "password": "salmane123@"
}

def get_auth_token() -> str:
    """Obtenir un token d'authentification pour un professeur"""
    try:
        response = requests.post(f"{BASE_URL}/auth/login", json=TEACHER_CREDENTIALS)
        if response.status_code == 200:
            return response.json()["access_token"]
        else:
            print(f"❌ Erreur d'authentification: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Erreur de connexion: {e}")
        return None

def test_endpoint(method: str, endpoint: str, headers: Dict = None, data: Dict = None) -> Dict[str, Any]:
    """Tester un endpoint"""
    url = f"{BASE_URL}{endpoint}"
    
    try:
        if method.upper() == "GET":
            response = requests.get(url, headers=headers)
        elif method.upper() == "POST":
            response = requests.post(url, headers=headers, json=data)
        else:
            return {"error": f"Méthode {method} non supportée"}
        
        return {
            "status_code": response.status_code,
            "success": 200 <= response.status_code < 300,
            "data": response.json() if response.content else None,
            "error": response.text if response.status_code >= 400 else None
        }
        
    except Exception as e:
        return {
            "status_code": 0,
            "success": False,
            "error": str(e)
        }

def test_fixed_endpoints():
    """Tester les endpoints corrigés"""
    
    print("🔍 Test des endpoints corrigés...")
    print("=" * 60)
    
    # Obtenir le token d'authentification
    token = get_auth_token()
    if not token:
        print("❌ Impossible d'obtenir le token d'authentification")
        return
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Liste des endpoints corrigés à tester
    endpoints_to_test = [
        # =====================================================
        # ENDPOINTS CORRIGÉS
        # =====================================================
        {"method": "GET", "endpoint": "/analytics/dashboard/overview", "name": "Dashboard Overview (corrigé)"},
        {"method": "GET", "endpoint": "/analytics/recent-activity", "name": "Recent Activity (corrigé)"},
        {"method": "GET", "endpoint": "/student_performance/class/1/students-performance", "name": "Student Performance (corrigé)"},
        {"method": "GET", "endpoint": "/learning_paths/", "name": "Learning Paths (corrigé)"},
        {"method": "GET", "endpoint": "/contents/", "name": "Contents (corrigé)"},
        {"method": "GET", "endpoint": "/notifications/user/2", "name": "Notifications (corrigé)"},
        
        # =====================================================
        # ENDPOINTS EXISTANTS (pour comparaison)
        # =====================================================
        {"method": "GET", "endpoint": "/users/", "name": "Users"},
        {"method": "GET", "endpoint": "/badges/", "name": "Badges"},
        {"method": "GET", "endpoint": "/quizzes/", "name": "Quizzes"},
    ]
    
    results = []
    success_count = 0
    total_count = len(endpoints_to_test)
    
    for endpoint in endpoints_to_test:
        print(f"\n🔍 Test: {endpoint['name']}")
        print(f"   URL: {endpoint['method']} {endpoint['endpoint']}")
        
        result = test_endpoint(endpoint["method"], endpoint["endpoint"], headers)
        
        if result["success"]:
            print(f"   ✅ Succès ({result['status_code']})")
            success_count += 1
        else:
            print(f"   ❌ Échec ({result['status_code']}): {result.get('error', 'Erreur inconnue')}")
        
        results.append({
            "endpoint": endpoint["name"],
            "method": endpoint["method"],
            "url": endpoint["endpoint"],
            "success": result["success"],
            "status_code": result["status_code"],
            "error": result.get("error")
        })
    
    # Résumé
    print("\n" + "=" * 60)
    print("📊 RÉSUMÉ DES TESTS")
    print("=" * 60)
    print(f"✅ Succès: {success_count}/{total_count} ({success_count/total_count*100:.1f}%)")
    print(f"❌ Échecs: {total_count - success_count}/{total_count}")
    
    # Détails des échecs
    failures = [r for r in results if not r["success"]]
    if failures:
        print("\n❌ DÉTAILS DES ÉCHECS:")
        for failure in failures:
            print(f"   • {failure['endpoint']}: {failure['error']}")
    
    # Tests spécifiques des données
    print("\n🎯 TESTS SPÉCIFIQUES DES DONNÉES:")
    
    # Test du dashboard overview
    overview_result = test_endpoint("GET", "/analytics/dashboard/overview", headers)
    if overview_result["success"]:
        data = overview_result["data"]
        print(f"   📈 Dashboard Overview:")
        print(f"      • Classes: {data.get('classes', 0)}")
        print(f"      • Élèves: {data.get('students', 0)}")
        print(f"      • Quiz: {data.get('quizzes', 0)}")
        print(f"      • Progression moyenne: {data.get('average_progression', 0)}%")
    else:
        print("   ❌ Impossible de récupérer les données du dashboard")
    
    # Test des notifications
    notifications_result = test_endpoint("GET", "/notifications/user/2", headers)
    if notifications_result["success"]:
        data = notifications_result["data"]
        print(f"   🔔 Notifications:")
        print(f"      • Notifications: {len(data.get('notifications', []))}")
        print(f"      • Non lues: {data.get('unread_count', 0)}")
    else:
        print("   ❌ Impossible de récupérer les notifications")
    
    print("\n🎉 Test des endpoints corrigés terminé !")

if __name__ == "__main__":
    test_fixed_endpoints() 