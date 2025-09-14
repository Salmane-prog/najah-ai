#!/usr/bin/env python3
"""
Test des données Analytics de l'évaluation adaptative
Vérifier si les données sont réelles ou factices
"""

import requests

print("🔍 Test des données Analytics - Évaluation Adaptative")
print("=" * 60)

BASE_URL = "http://localhost:8000"

try:
    # Login en tant que professeur
    login = requests.post(f"{BASE_URL}/api/v1/auth/login", json={
        "email": "prof@najah.ai",
        "password": "password123"
    })

    if login.status_code == 200:
        token = login.json().get("access_token")
        headers = {"Authorization": f"Bearer {token}"}
        print("✅ Login professeur OK")

        # Test 1: Endpoint des tests adaptatifs
        print(f"\n📊 Test 1: Tests adaptatifs")
        response = requests.get(f"{BASE_URL}/api/v1/adaptive-evaluation/tests", headers=headers)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Données récupérées")
            print(f"   Total tests: {len(data.get('tests', []))}")
            
            if data.get('tests'):
                for test in data['tests'][:3]:  # Afficher les 3 premiers
                    print(f"   - {test.get('title', 'Sans titre')} (ID: {test.get('id')})")
            else:
                print("   ⚠️ Aucun test trouvé")
        else:
            print(f"❌ Erreur: {response.status_code}")
            print(f"   Détail: {response.text}")

        # Test 2: Endpoint des résultats des tests
        print(f"\n📊 Test 2: Résultats des tests")
        response = requests.get(f"{BASE_URL}/api/v1/adaptive-evaluation/results", headers=headers)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Données récupérées")
            print(f"   Total résultats: {len(data.get('results', []))}")
            
            if data.get('results'):
                for result in data['results'][:3]:  # Afficher les 3 premiers
                    print(f"   - Test ID: {result.get('test_id')}, Score: {result.get('score')}%")
            else:
                print("   ⚠️ Aucun résultat trouvé")
        else:
            print(f"❌ Erreur: {response.status_code}")
            print(f"   Détail: {response.text}")

        # Test 3: Endpoint des analytics
        print(f"\n📊 Test 3: Analytics")
        response = requests.get(f"{BASE_URL}/api/v1/adaptive-evaluation/analytics", headers=headers)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Données récupérées")
            print(f"   Contenu: {data}")
        else:
            print(f"❌ Erreur: {response.status_code}")
            print(f"   Détail: {response.text}")

        # Test 4: Endpoint des statistiques
        print(f"\n📊 Test 4: Statistiques")
        response = requests.get(f"{BASE_URL}/api/v1/adaptive-evaluation/stats", headers=headers)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Données récupérées")
            print(f"   Contenu: {data}")
        else:
            print(f"❌ Erreur: {response.status_code}")
            print(f"   Détail: {response.text}")

        # Test 5: Vérifier la base de données directement
        print(f"\n📊 Test 5: Vérification base de données")
        response = requests.get(f"{BASE_URL}/api/v1/teacher-dashboard/overview", headers=headers)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Données récupérées")
            print(f"   Tests créés: {data.get('overview', {}).get('total_quizzes', 'N/A')}")
            print(f"   Classes: {data.get('overview', {}).get('total_classes', 'N/A')}")
            print(f"   Étudiants: {data.get('overview', {}).get('total_students', 'N/A')}")
        else:
            print(f"❌ Erreur: {response.status_code}")
            print(f"   Détail: {response.text}")

    else:
        print(f"❌ Login professeur échoué: {login.status_code}")

except Exception as e:
    print(f"❌ Erreur: {e}")

print(f"\n🔍 Conclusion:")
print("   - Si les endpoints retournent des erreurs 404/500, les données sont factices")
print("   - Si les endpoints retournent des données vides [], les données sont factices")
print("   - Si les endpoints retournent des données cohérentes, les données sont réelles")






