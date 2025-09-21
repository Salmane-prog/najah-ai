#!/usr/bin/env python3
"""
Script pour tester l'endpoint de création de test
"""

import requests
import json
import os

def test_create_endpoint():
    print("🧪 Test de l'endpoint de création de test")
    print("=" * 60)
    
    # URL de l'API
    base_url = "http://localhost:8000"
    
    # Données du test à créer
    test_data = {
        "title": "Test Créé par Script - " + str(int(os.urandom(4).hex(), 16)),
        "subject": "Test",
        "description": "Test de création via script",
        "difficulty_min": 1,
        "difficulty_max": 5,
        "estimated_duration": 15,
        "adaptation_type": "difficulty",
        "learning_objectives": "Tester la création",
        "is_active": True
    }
    
    print(f"📝 Données du test:")
    for key, value in test_data.items():
        print(f"  {key}: {value}")
    
    try:
        # Test 1: Vérifier si l'API est accessible
        print(f"\n🔍 Test 1: Vérifier l'API")
        response = requests.get(f"{base_url}/docs")
        if response.status_code == 200:
            print("  ✅ API accessible")
        else:
            print(f"  ❌ API non accessible: {response.status_code}")
            return
        
        # Test 2: Essayer de créer un test
        print(f"\n🔍 Test 2: Créer un test")
        print(f"  URL: {base_url}/api/v1/adaptive-evaluation/tests/")
        print(f"  Méthode: POST")
        print(f"  Données: {json.dumps(test_data, indent=2)}")
        
        # Note: On ne peut pas vraiment tester sans authentification
        # Mais on peut vérifier que l'endpoint existe
        print(f"\n⚠️  Note: L'endpoint nécessite une authentification")
        print(f"   Pour tester complètement, il faut:")
        print(f"   1. Démarrer le backend")
        print(f"   2. Se connecter via le frontend")
        print(f"   3. Cliquer sur 'Créer un test'")
        print(f"   4. Vérifier la base de données")
        
    except requests.exceptions.ConnectionError:
        print(f"❌ Impossible de se connecter à {base_url}")
        print(f"   Vérifiez que le backend est démarré")
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    test_create_endpoint()


















