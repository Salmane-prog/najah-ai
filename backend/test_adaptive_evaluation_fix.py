#!/usr/bin/env python3
"""
Script de test pour vérifier que l'endpoint d'évaluation adaptative fonctionne
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

def test_adaptive_evaluation_endpoint():
    """Tester l'endpoint d'évaluation adaptative"""
    
    print("🧪 Test de l'endpoint d'évaluation adaptative")
    print("=" * 50)
    
    # 1. Test de connexion
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✅ Serveur accessible")
        else:
            print("❌ Serveur non accessible")
            return
    except Exception as e:
        print(f"❌ Erreur de connexion: {e}")
        return
    
    # 2. Authentification
    print("\n🔐 Test d'authentification...")
    token = get_auth_token()
    if not token:
        print("❌ Impossible d'obtenir le token d'authentification")
        return
    
    print("✅ Authentification réussie")
    headers = {"Authorization": f"Bearer {token}"}
    
    # 3. Test de l'endpoint d'évaluation adaptative
    print("\n📊 Test de l'endpoint d'évaluation adaptative...")
    try:
        response = requests.get(f"{API_BASE}/teacher-adaptive-evaluation/tests/teacher/33", headers=headers)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Endpoint fonctionne !")
            print(f"   Tests trouvés: {data.get('total_tests', 0)}")
            
            if data.get('tests'):
                for i, test in enumerate(data['tests'][:3]):  # Afficher les 3 premiers
                    print(f"   Test {i+1}: {test.get('title', 'Sans titre')}")
                    print(f"     - Niveau: {test.get('difficulty_range', {}).get('min', '?')}-{test.get('difficulty_range', {}).get('max', '?')}")
                    print(f"     - Durée: {test.get('estimated_duration', '?')} min")
                    print(f"     - Statut: {'Actif' if test.get('is_active') else 'Inactif'}")
            else:
                print("   Aucun test trouvé (c'est normal si la base est vide)")
        else:
            print(f"❌ Erreur: {response.text}")
            
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")

if __name__ == "__main__":
    test_adaptive_evaluation_endpoint()





















