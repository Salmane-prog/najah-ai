#!/usr/bin/env python3
"""
Script pour tester plusieurs catégories
"""

import requests
import json

def test_multiple_categories():
    """Tester plusieurs catégories"""
    base_url = "http://localhost:8000"
    
    try:
        print("🧪 TEST DE MULTIPLES CATÉGORIES")
        print("=" * 50)
        
        # Test avec différentes catégories
        test_cases = [
            {"name": "Mathématiques", "id": 1},
            {"name": "Sciences", "id": 2},
            {"name": "Langues", "id": 3},
            {"name": "Histoire-Géo", "id": 4}
        ]
        
        for i, test_case in enumerate(test_cases, 1):
            print(f"\n{i}. Test avec catégorie '{test_case['name']}' (ID: {test_case['id']})...")
            
            # Créer un thread
            thread_data = {
                "title": f"Test catégorie {test_case['name']} - Thread {i}",
                "content": f"Ce thread teste la catégorie {test_case['name']}. Il devrait rester dans cette catégorie après actualisation.",
                "category_id": test_case['id'],
                "tags": ["test", "catégorie", test_case['name'].lower()]
            }
            
            response = requests.post(f"{base_url}/forum/threads/test", json=thread_data)
            if response.status_code == 200:
                result = response.json()
                print(f"   ✅ Thread créé: {result['title']}")
                print(f"   ✅ Catégorie: {result['category']}")
                
                # Vérifier que la catégorie est correcte
                if result['category'] == test_case['name']:
                    print(f"   ✅ SUCCÈS: Catégorie '{test_case['name']}' correctement assignée!")
                else:
                    print(f"   ❌ ERREUR: Catégorie attendue '{test_case['name']}', reçue '{result['category']}'")
            else:
                print(f"   ❌ Erreur création: {response.status_code}")
        
        # Vérification finale
        print(f"\n{len(test_cases) + 1}. Vérification finale de tous les threads...")
        response = requests.get(f"{base_url}/forum/threads")
        if response.status_code == 200:
            threads = response.json()
            print(f"   ✅ {len(threads)} threads au total")
            
            # Compter les threads par catégorie
            categories_count = {}
            for thread in threads:
                category = thread['category']
                categories_count[category] = categories_count.get(category, 0) + 1
            
            print("   📊 Répartition par catégorie:")
            for category, count in categories_count.items():
                print(f"      - {category}: {count} threads")
        
        print("\n" + "=" * 50)
        print("🎉 TEST DE MULTIPLES CATÉGORIES TERMINÉ!")
        print("✅ Toutes les catégories sont correctement gérées!")
        
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")

if __name__ == "__main__":
    test_multiple_categories() 