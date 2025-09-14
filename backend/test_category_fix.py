#!/usr/bin/env python3
"""
Script pour tester la correction de la catégorie
"""

import requests
import json

def test_category_fix():
    """Tester la correction de la catégorie"""
    base_url = "http://localhost:8000"
    
    try:
        print("🧪 TEST DE CORRECTION DE LA CATÉGORIE")
        print("=" * 50)
        
        # Test 1: Récupérer les catégories disponibles
        print("\n1. Récupération des catégories disponibles...")
        response = requests.get(f"{base_url}/forum/categories")
        if response.status_code == 200:
            categories = response.json()
            print(f"   ✅ {len(categories)} catégories trouvées:")
            for cat in categories:
                print(f"      - ID: {cat['id']}, Nom: {cat['name']}")
        else:
            print(f"   ❌ Erreur: {response.status_code}")
            return
        
        # Test 2: Créer un nouveau thread avec catégorie "Sciences"
        print("\n2. Création d'un nouveau thread avec catégorie 'Sciences'...")
        thread_data = {
            "title": "Test correction catégorie - Sciences",
            "content": "Ce thread teste la correction de la catégorie. Il devrait rester dans la catégorie Sciences après actualisation.",
            "category_id": 2,  # ID de la catégorie Sciences
            "tags": ["test", "catégorie", "sciences"]
        }
        
        response = requests.post(f"{base_url}/forum/threads/test", json=thread_data)
        if response.status_code == 200:
            result = response.json()
            print("   ✅ Thread créé avec succès!")
            print(f"      - ID: {result['id']}")
            print(f"      - Titre: {result['title']}")
            print(f"      - Catégorie: {result['category']}")
            print(f"      - Catégorie ID: {thread_data['category_id']}")
        else:
            print(f"   ❌ Erreur: {response.status_code} - {response.text}")
            return
        
        # Test 3: Récupérer tous les threads et vérifier la catégorie
        print("\n3. Vérification de la catégorie après création...")
        response = requests.get(f"{base_url}/forum/threads")
        if response.status_code == 200:
            threads = response.json()
            print(f"   ✅ {len(threads)} threads récupérés")
            
            # Chercher le thread créé
            created_thread = None
            for thread in threads:
                if thread['title'] == "Test correction catégorie - Sciences":
                    created_thread = thread
                    break
            
            if created_thread:
                print(f"   ✅ Thread trouvé!")
                print(f"      - ID: {created_thread['id']}")
                print(f"      - Titre: {created_thread['title']}")
                print(f"      - Catégorie: {created_thread['category']}")
                
                if created_thread['category'] == "Sciences":
                    print("   ✅ SUCCÈS: La catégorie est correctement conservée!")
                else:
                    print(f"   ❌ ERREUR: La catégorie devrait être 'Sciences' mais est '{created_thread['category']}'")
            else:
                print("   ❌ Thread créé non trouvé dans la liste")
        else:
            print(f"   ❌ Erreur: {response.status_code}")
        
        print("\n" + "=" * 50)
        print("🎉 TEST DE CORRECTION TERMINÉ!")
        
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")

if __name__ == "__main__":
    test_category_fix() 