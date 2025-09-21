#!/usr/bin/env python3
"""
Script de test pour les vrais endpoints backend
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_endpoint(endpoint, method="GET", data=None):
    """Teste un endpoint spécifique"""
    url = f"{BASE_URL}{endpoint}"
    
    try:
        if method == "GET":
            response = requests.get(url)
        elif method == "POST":
            response = requests.post(url, json=data)
        else:
            print(f"❌ Méthode {method} non supportée")
            return False
            
        print(f"🔍 {method} {endpoint}")
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            print(f"   ✅ Succès")
            try:
                response_data = response.json()
                print(f"   📊 Données: {json.dumps(response_data, indent=2, ensure_ascii=False)[:200]}...")
            except:
                print(f"   📄 Réponse: {response.text[:200]}...")
        elif response.status_code == 401:
            print(f"   🔒 Non autorisé (authentification requise)")
        elif response.status_code == 403:
            print(f"   🚫 Interdit (permissions insuffisantes)")
        elif response.status_code == 404:
            print(f"   ❌ Endpoint non trouvé")
        else:
            print(f"   ⚠️ Erreur: {response.text[:200]}...")
            
        print()
        return response.status_code == 200
        
    except requests.exceptions.ConnectionError:
        print(f"🔍 {method} {endpoint}")
        print(f"   ❌ Impossible de se connecter au serveur")
        print(f"   💡 Vérifiez que le serveur est démarré sur {BASE_URL}")
        print()
        return False
    except Exception as e:
        print(f"🔍 {method} {endpoint}")
        print(f"   ❌ Erreur: {str(e)}")
        print()
        return False

def main():
    """Teste tous les vrais endpoints"""
    print("🚀 TEST DES VRAIS ENDPOINTS BACKEND")
    print("=" * 50)
    
    # Test de base - vérifier que le serveur répond
    print("1️⃣ Test de connectivité...")
    test_endpoint("/docs")
    
    # Test des endpoints du dashboard (avec les vrais préfixes)
    print("2️⃣ Test des endpoints du dashboard...")
    test_endpoint("/api/v1/teacher-dashboard/teacher-dashboard/")
    test_endpoint("/api/v1/teacher-dashboard/teacher-dashboard/analytics")
    test_endpoint("/api/v1/teacher-dashboard/teacher-dashboard/students")
    
    # Test des endpoints IA (avec les vrais préfixes)
    print("3️⃣ Test des endpoints IA...")
    test_endpoint("/api/v1/ai-models/ai_models/")
    test_endpoint("/api/v1/data_collection/data_collection/metrics/")
    test_endpoint("/api/v1/training_sessions/training_sessions/")
    
    # Test des endpoints d'évaluation adaptative (avec les vrais préfixes)
    print("4️⃣ Test des endpoints d'évaluation adaptative...")
    test_endpoint("/api/v1/adaptive-evaluation/adaptive-evaluation/tests")
    
    # Test des endpoints analytics IA
    print("5️⃣ Test des endpoints analytics IA...")
    test_endpoint("/api/v1/ai-analytics/ai-analytics/")
    
    print("🏁 Test terminé!")

if __name__ == "__main__":
    main()


























