#!/usr/bin/env python3
"""
Script pour déboguer la réponse exacte de l'API d'évaluation adaptative
"""

import requests
import json

# Configuration
BASE_URL = "http://localhost:8000"
API_BASE = f"{BASE_URL}/api/v1"

def get_auth_token():
    """Obtenir un token d'authentification"""
    try:
        login_data = {
            "email": "marizee.dubois@najah.ai",
            "password": "password123"
        }
        
        response = requests.post(f"{API_BASE}/auth/login", json=login_data)
        
        if response.status_code == 200:
            data = response.json()
            return data.get("access_token")
        else:
            print(f"❌ Erreur de connexion: {response.status_code} - {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Erreur de connexion: {e}")
        return None

def debug_api_response():
    """Déboguer la réponse de l'API"""
    
    print("🔍 Débogage de la réponse de l'API")
    print("=" * 50)
    
    # 1. Authentification
    token = get_auth_token()
    if not token:
        print("❌ Impossible d'obtenir le token d'authentification")
        return
    
    print("✅ Authentification réussie")
    headers = {"Authorization": f"Bearer {token}"}
    
    # 2. Appel à l'API
    print("\n📊 Appel à l'API d'évaluation adaptative...")
    try:
        response = requests.get(f"{API_BASE}/teacher-adaptive-evaluation/tests/teacher/33", headers=headers)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ API répond avec succès")
            print(f"   Total tests: {data.get('total_tests', 0)}")
            
            if data.get('tests'):
                print(f"\n📋 Structure des données reçues:")
                for i, test in enumerate(data['tests']):
                    print(f"\n   Test {i+1}: {test.get('title', 'Sans titre')}")
                    print(f"     - ID: {test.get('id')}")
                    print(f"     - Titre: {test.get('title')}")
                    print(f"     - Matière: {test.get('subject')}")
                    print(f"     - Description: {test.get('description')}")
                    print(f"     - difficulty_range: {test.get('difficulty_range')} (type: {type(test.get('difficulty_range'))})")
                    print(f"     - difficulty_range_min: {test.get('difficulty_range_min')}")
                    print(f"     - difficulty_range_max: {test.get('difficulty_range_max')}")
                    print(f"     - estimated_duration: {test.get('estimated_duration')}")
                    print(f"     - is_active: {test.get('is_active')}")
                    print(f"     - created_at: {test.get('created_at')}")
                    print(f"     - statistics: {test.get('statistics')}")
                    
                    # Vérifier si difficulty_range est correct
                    difficulty_range = test.get('difficulty_range')
                    if difficulty_range and isinstance(difficulty_range, dict):
                        print(f"     ✅ difficulty_range valide: min={difficulty_range.get('min')}, max={difficulty_range.get('max')}")
                    else:
                        print(f"     ❌ difficulty_range invalide ou manquant")
                        print(f"        Valeur reçue: {difficulty_range}")
                        print(f"        Type: {type(difficulty_range)}")
            else:
                print("   Aucun test trouvé")
        else:
            print(f"❌ Erreur API: {response.text}")
            
    except Exception as e:
        print(f"❌ Erreur lors du débogage: {e}")

if __name__ == "__main__":
    debug_api_response()


















