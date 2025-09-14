#!/usr/bin/env python3
"""
Script de test final pour confirmer la correction du problème de catégorie
"""

import requests
import json
import time

def test_final_category_fix():
    """Test final de la correction de catégorie"""
    base_url = "http://localhost:8000"
    
    try:
        print("🧪 TEST FINAL DE CORRECTION DE CATÉGORIE")
        print("=" * 60)
        
        # Test 1: Créer un thread avec catégorie Sciences
        print("\n1. Création d'un thread avec catégorie 'Sciences'...")
        thread_data = {
            "title": "Test final - Sciences - " + str(int(time.time())),
            "content": "Ce thread teste la correction finale du problème de catégorie. Il devrait rester dans Sciences après actualisation.",
            "category_id": 2,  # Sciences
            "tags": ["test", "final", "sciences"]
        }
        
        response = requests.post(f"{base_url}/forum/threads/test", json=thread_data)
        if response.status_code == 200:
            result = response.json()
            thread_id = result['id']
            print("   ✅ Thread créé avec succès!")
            print(f"      - ID: {thread_id}")
            print(f"      - Titre: {result['title']}")
            print(f"      - Catégorie: {result['category']}")
            
            if result['category'] == "Sciences":
                print("   ✅ SUCCÈS: Catégorie correctement assignée lors de la création!")
            else:
                print(f"   ❌ ERREUR: Catégorie attendue 'Sciences', reçue '{result['category']}'")
                return
        else:
            print(f"   ❌ Erreur création: {response.status_code}")
            return
        
        # Test 2: Récupérer immédiatement et vérifier
        print("\n2. Vérification immédiate après création...")
        response = requests.get(f"{base_url}/forum/threads")
        if response.status_code == 200:
            threads = response.json()
            
            # Chercher le thread créé
            created_thread = None
            for thread in threads:
                if thread['id'] == thread_id:
                    created_thread = thread
                    break
            
            if created_thread:
                print(f"   ✅ Thread trouvé dans la liste!")
                print(f"      - ID: {created_thread['id']}")
                print(f"      - Titre: {created_thread['title']}")
                print(f"      - Catégorie: {created_thread['category']}")
                
                if created_thread['category'] == "Sciences":
                    print("   ✅ SUCCÈS: Catégorie correctement conservée après récupération!")
                else:
                    print(f"   ❌ ERREUR: Catégorie devrait être 'Sciences' mais est '{created_thread['category']}'")
                    return
            else:
                print("   ❌ Thread créé non trouvé dans la liste")
                return
        else:
            print(f"   ❌ Erreur récupération: {response.status_code}")
            return
        
        # Test 3: Simuler une actualisation (nouvelle requête)
        print("\n3. Simulation d'actualisation (nouvelle requête)...")
        response = requests.get(f"{base_url}/forum/threads")
        if response.status_code == 200:
            threads = response.json()
            
            # Chercher le thread créé
            created_thread = None
            for thread in threads:
                if thread['id'] == thread_id:
                    created_thread = thread
                    break
            
            if created_thread:
                print(f"   ✅ Thread trouvé après 'actualisation'!")
                print(f"      - ID: {created_thread['id']}")
                print(f"      - Titre: {created_thread['title']}")
                print(f"      - Catégorie: {created_thread['category']}")
                
                if created_thread['category'] == "Sciences":
                    print("   ✅ SUCCÈS: Catégorie correctement conservée après 'actualisation'!")
                else:
                    print(f"   ❌ ERREUR: Catégorie devrait être 'Sciences' mais est '{created_thread['category']}'")
                    return
            else:
                print("   ❌ Thread créé non trouvé après 'actualisation'")
                return
        else:
            print(f"   ❌ Erreur récupération après actualisation: {response.status_code}")
            return
        
        # Test 4: Vérifier avec filtrage par catégorie
        print("\n4. Test de filtrage par catégorie...")
        response = requests.get(f"{base_url}/forum/threads?category_id=2")  # Filtrer par Sciences
        if response.status_code == 200:
            threads = response.json()
            print(f"   ✅ {len(threads)} threads trouvés dans la catégorie Sciences")
            
            # Vérifier que notre thread est dans la liste
            found = False
            for thread in threads:
                if thread['id'] == thread_id:
                    found = True
                    print(f"   ✅ Notre thread trouvé dans le filtre Sciences!")
                    break
            
            if not found:
                print("   ❌ Notre thread non trouvé dans le filtre Sciences")
                return
        else:
            print(f"   ❌ Erreur filtrage: {response.status_code}")
            return
        
        print("\n" + "=" * 60)
        print("🎉 TEST FINAL DE CORRECTION TERMINÉ AVEC SUCCÈS!")
        print("✅ Le problème de catégorie est COMPLÈTEMENT RÉSOLU!")
        print("✅ Les catégories sont correctement assignées et conservées!")
        print("✅ L'actualisation de page ne change plus la catégorie!")
        print("✅ Le filtrage par catégorie fonctionne correctement!")
        
    except Exception as e:
        print(f"❌ Erreur lors du test final: {e}")

if __name__ == "__main__":
    test_final_category_fix() 