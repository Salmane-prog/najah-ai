#!/usr/bin/env python3
"""
Script pour tester l'endpoint teacher-adaptive-evaluation
"""

import requests

def test_endpoint():
    """Tester l'endpoint"""
    base_url = "http://localhost:8000"
    
    print("🔍 Test de l'endpoint teacher-adaptive-evaluation...")
    print("=" * 50)
    
    # Test 1: Vérifier que l'endpoint existe
    print("\n1️⃣ Test de l'endpoint...")
    try:
        response = requests.get(f"{base_url}/api/v1/teacher-adaptive-evaluation/tests/teacher/33", timeout=10)
        print(f"   - Status: {response.status_code}")
        print(f"   - Réponse: {response.text[:200]}...")
        
        if response.status_code == 401:
            print("   ❌ Erreur d'authentification - Token requis")
        elif response.status_code == 404:
            print("   ❌ Endpoint non trouvé - Router non enregistré")
        elif response.status_code == 200:
            print("   ✅ Endpoint fonctionne !")
        else:
            print(f"   ❌ Erreur: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Erreur lors du test: {e}")
    
    # Test 2: Vérifier la documentation
    print("\n2️⃣ Test de la documentation...")
    try:
        response = requests.get(f"{base_url}/docs", timeout=5)
        if response.status_code == 200:
            print("   ✅ Documentation accessible")
            # Chercher les endpoints teacher-adaptive-evaluation
            if "teacher-adaptive-evaluation" in response.text:
                print("   ✅ Endpoint teacher-adaptive-evaluation trouvé dans la doc")
            else:
                print("   ❌ Endpoint teacher-adaptive-evaluation NON trouvé dans la doc")
        else:
            print(f"   ❌ Documentation retourne: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Erreur lors du test de la doc: {e}")
    
    print("\n" + "=" * 50)
    print("📋 Résumé:")
    print("   - Si 404: Le router n'est pas enregistré")
    print("   - Si 401: Problème d'authentification")
    print("   - Si 200: L'endpoint fonctionne")

if __name__ == "__main__":
    test_endpoint() 