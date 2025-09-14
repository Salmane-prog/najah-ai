#!/usr/bin/env python3
"""
Script pour tester les routes disponibles
"""

import requests

def test_routes():
    """Tester les routes disponibles"""
    base_url = "http://localhost:8000"
    
    try:
        # Test 1: Route de test du forum
        print("1. Test de la route /forum/test...")
        response = requests.get(f"{base_url}/forum/test")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print(f"   ✅ Réponse: {response.json()}")
        else:
            print(f"   ❌ Erreur: {response.text}")
        
        # Test 2: Route de test avec préfixe API
        print("\n2. Test de la route /api/v1/forum/test...")
        response = requests.get(f"{base_url}/api/v1/forum/test")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print(f"   ✅ Réponse: {response.json()}")
        else:
            print(f"   ❌ Erreur: {response.text}")
        
        # Test 3: Route des catégories
        print("\n3. Test de la route /forum/categories...")
        response = requests.get(f"{base_url}/forum/categories")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            categories = response.json()
            print(f"   ✅ Catégories trouvées: {len(categories)}")
        else:
            print(f"   ❌ Erreur: {response.text}")
        
        # Test 4: Route des threads
        print("\n4. Test de la route /forum/threads...")
        response = requests.get(f"{base_url}/forum/threads")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            threads = response.json()
            print(f"   ✅ Threads trouvés: {len(threads)}")
        else:
            print(f"   ❌ Erreur: {response.text}")
        
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")

if __name__ == "__main__":
    test_routes() 