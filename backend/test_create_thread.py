#!/usr/bin/env python3
"""
Script pour tester la création de thread
"""

import requests
import json

def test_create_thread():
    """Tester la création de thread"""
    base_url = "http://localhost:8000/api/v1/forum"
    
    try:
        # Test de création de thread
        print("Test de création de thread...")
        thread_data = {
            "title": "Test thread via API - Création",
            "content": "Ceci est un test de création de thread via l'API. Le contenu est riche et détaillé pour tester le système.",
            "category_id": 1,
            "tags": ["test", "api", "création"]
        }
        
        response = requests.post(f"{base_url}/threads/test", json=thread_data)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print("   ✅ Thread créé avec succès!")
            print(f"   - ID: {result['id']}")
            print(f"   - Titre: {result['title']}")
            print(f"   - Auteur: {result['author']['name']}")
            print(f"   - Catégorie: {result['category']}")
            print(f"   - Tags: {result['tags']}")
        else:
            print(f"   ❌ Erreur: {response.text}")
        
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")

if __name__ == "__main__":
    test_create_thread() 