#!/usr/bin/env python3
"""
Script de test pour les endpoints de monitoring
"""

import requests
import json

# Configuration
BASE_URL = "http://localhost:8000"
API_BASE = f"{BASE_URL}/api/v1"

def test_login():
    """Test de connexion pour obtenir un token"""
    print("🔐 Test de connexion...")
    
    login_data = {
        "username": "marie.dubois@najah.ai",
        "password": "password123"
    }
    
    response = requests.post(f"{API_BASE}/auth/login", json=login_data)
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Connexion réussie: {data['user']['first_name']} {data['user']['last_name']}")
        print(f"📧 Email: {data['user']['email']}")
        print(f"👤 Rôle: {data['user']['role']}")
        print(f"🆔 ID: {data['user']['id']}")
        return data['access_token'], data['user']['id']
    else:
        print(f"❌ Erreur de connexion: {response.status_code}")
        print(response.text)
        return None, None

def test_monitoring_endpoints(token, teacher_id):
    """Test des endpoints de monitoring"""
    headers = {"Authorization": f"Bearer {token}"}
    
    print(f"\n📊 Test des endpoints de monitoring pour l'enseignant ID: {teacher_id}")
    
    # Test 1: Activité des étudiants
    print("\n1️⃣ Test de l'activité des étudiants...")
    response = requests.get(f"{API_BASE}/monitoring/teacher/{teacher_id}/monitoring/students", headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Activité des étudiants récupérée: {len(data['activities'])} activités")
        for activity in data['activities'][:3]:  # Afficher les 3 premières
            print(f"   - {activity['name']}: {activity['testTitle']} (Status: {activity['status']})")
    else:
        print(f"❌ Erreur: {response.status_code}")
        print(response.text)
    
    # Test 2: Performance des tests
    print("\n2️⃣ Test de la performance des tests...")
    response = requests.get(f"{API_BASE}/monitoring/teacher/{teacher_id}/monitoring/tests", headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Performance des tests récupérée: {len(data['performances'])} tests")
        for performance in data['performances'][:3]:  # Afficher les 3 premiers
            print(f"   - {performance['title']}: {performance['activeStudents']} étudiants actifs")
    else:
        print(f"❌ Erreur: {response.status_code}")
        print(response.text)
    
    # Test 3: Aperçu du monitoring
    print("\n3️⃣ Test de l'aperçu du monitoring...")
    response = requests.get(f"{API_BASE}/monitoring/teacher/{teacher_id}/monitoring/overview", headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        overview = data['overview']
        print(f"✅ Aperçu du monitoring récupéré:")
        print(f"   - Étudiants actifs: {overview['activeStudents']}")
        print(f"   - Tests terminés: {overview['completedTests']}")
        print(f"   - Total tests: {overview['totalTests']}")
        print(f"   - Confiance moyenne: {overview['averageConfidence']}%")
    else:
        print(f"❌ Erreur: {response.status_code}")
        print(response.text)

def main():
    print("🚀 Test des endpoints de monitoring")
    print("=" * 50)
    
    # Test de connexion
    token, teacher_id = test_login()
    
    if token and teacher_id:
        # Test des endpoints de monitoring
        test_monitoring_endpoints(token, teacher_id)
    else:
        print("❌ Impossible de continuer sans token d'authentification")

if __name__ == "__main__":
    main()





