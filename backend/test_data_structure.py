#!/usr/bin/env python3
"""
Script pour vérifier la structure des données retournées par les endpoints
"""

import requests
import json

def test_data_structure():
    """Tester la structure des données des endpoints"""
    print("🔍 VÉRIFICATION DE LA STRUCTURE DES DONNÉES")
    print("=" * 60)
    
    base_url = "http://localhost:8000"
    
    # Test 1: Endpoint quizzes/assigned
    print("\n1️⃣ Test structure /api/v1/quizzes/assigned/30")
    try:
        response = requests.get(f"{base_url}/api/v1/quizzes/assigned/30", timeout=10)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Données reçues:")
            print(f"      - Type: {type(data)}")
            print(f"      - Clés: {list(data.keys()) if isinstance(data, dict) else 'N/A'}")
            print(f"      - Quizzes: {len(data.get('quizzes', []))} éléments")
            print(f"      - Total: {data.get('total', 'N/A')}")
            print(f"      - Structure: {json.dumps(data, indent=2, default=str)}")
        else:
            print(f"   ❌ Erreur: {response.text}")
    except Exception as e:
        print(f"   ❌ Erreur de connexion: {e}")
    
    # Test 2: Endpoint homework/assigned
    print("\n2️⃣ Test structure /api/v1/homework/assigned/30")
    try:
        response = requests.get(f"{base_url}/api/v1/homework/assigned/30", timeout=10)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Données reçues:")
            print(f"      - Type: {type(data)}")
            print(f"      - Clés: {list(data.keys()) if isinstance(data, dict) else 'N/A'}")
            print(f"      - Homework: {len(data.get('homework', []))} éléments")
            print(f"      - Total: {data.get('total', 'N/A')}")
            print(f"      - Structure: {json.dumps(data, indent=2, default=str)}")
        else:
            print(f"   ❌ Erreur: {response.text}")
    except Exception as e:
        print(f"   ❌ Erreur de connexion: {e}")
    
    # Test 3: Endpoint assessments
    print("\n3️⃣ Test structure /api/v1/assessments/student/30")
    try:
        response = requests.get(f"{base_url}/api/v1/assessments/student/30", timeout=10)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Données reçues:")
            print(f"      - Type: {type(data)}")
            print(f"      - Clés: {list(data.keys()) if isinstance(data, dict) else 'N/A'}")
            print(f"      - Assessments: {len(data.get('assessments', []))} éléments")
            print(f"      - Summary: {data.get('summary', 'N/A')}")
            print(f"      - Structure: {json.dumps(data, indent=2, default=str)}")
        else:
            print(f"   ❌ Erreur: {response.text}")
    except Exception as e:
        print(f"   ❌ Erreur de connexion: {e}")
    
    print("\n" + "=" * 60)
    print("🎯 RÉSUMÉ DES TESTS")
    print("✅ 200 = Données reçues, vérifier la structure")
    print("⚠️ 403 = Authentification requise")
    print("❌ 404 = Endpoint non trouvé")
    print("❌ 500 = Erreur serveur")

if __name__ == "__main__":
    print("🚀 Démarrage de la vérification de la structure des données...")
    print("Assurez-vous que votre serveur backend est démarré sur http://localhost:8000")
    print("Appuyez sur Entrée pour continuer...")
    input()
    
    test_data_structure()







