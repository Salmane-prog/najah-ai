#!/usr/bin/env python3
"""
Script pour tester la connexion à l'API et diagnostiquer le problème de création de tests
"""

import requests
import json

def test_api_connection():
    """Tester la connexion à l'API"""
    base_url = "http://localhost:8000"
    
    print("🔍 Test de connexion à l'API...")
    print("=" * 50)
    
    try:
        # Test 1: Vérifier que l'API est accessible
        print("\n1️⃣ Test de connectivité...")
        response = requests.get(f"{base_url}/docs", timeout=5)
        if response.status_code == 200:
            print("✅ API accessible sur /docs")
        else:
            print(f"❌ API /docs retourne: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Impossible de se connecter à l'API")
        print("   Vérifiez que le backend est démarré sur le port 8000")
        return False
    except Exception as e:
        print(f"❌ Erreur de connexion: {e}")
        return False
    
    # Test 2: Vérifier l'endpoint de création de tests
    print("\n2️⃣ Test de l'endpoint de création...")
    try:
        test_data = {
            "title": "Test de Diagnostic",
            "subject": "Diagnostic",
            "level": "Test",
            "duration": 10,
            "question_count": 5,
            "difficulty_range": "1-5",
            "learning_objectives": ["Test de connexion"],
            "adaptation_type": "hybrid"
        }
        
        response = requests.post(
            f"{base_url}/api/v1/teacher-adaptive-evaluation/tests/create",
            json=test_data,
            timeout=10
        )
        
        print(f"   - Status: {response.status_code}")
        print(f"   - Réponse: {response.text[:200]}...")
        
        if response.status_code == 401:
            print("   ❌ Erreur d'authentification - Token requis")
        elif response.status_code == 422:
            print("   ❌ Erreur de validation des données")
        elif response.status_code == 200 or response.status_code == 201:
            print("   ✅ Test créé avec succès !")
        else:
            print(f"   ❌ Erreur inattendue: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Erreur lors du test: {e}")
    
    # Test 3: Vérifier l'endpoint de liste des tests
    print("\n3️⃣ Test de l'endpoint de liste...")
    try:
        response = requests.get(
            f"{base_url}/api/v1/teacher-adaptive-evaluation/tests/teacher/33",
            timeout=10
        )
        
        print(f"   - Status: {response.status_code}")
        print(f"   - Réponse: {response.text[:200]}...")
        
        if response.status_code == 401:
            print("   ❌ Erreur d'authentification - Token requis")
        elif response.status_code == 200:
            print("   ✅ Liste des tests accessible")
        else:
            print(f"   ❌ Erreur: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Erreur lors du test: {e}")
    
    print("\n" + "=" * 50)
    print("📋 Résumé du diagnostic:")
    print("   - Si vous voyez des erreurs 401: Problème d'authentification")
    print("   - Si vous voyez des erreurs 422: Problème de données")
    print("   - Si vous voyez des erreurs 500: Problème serveur")
    print("   - Si tout est 200: L'API fonctionne, problème côté frontend")
    
    return True

if __name__ == "__main__":
    test_api_connection()
