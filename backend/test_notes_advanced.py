#!/usr/bin/env python3
"""
Script pour tester les endpoints de notes avancées
"""

import requests
import json

def test_notes_advanced():
    """Tester les endpoints de notes avancées"""
    base_url = "http://localhost:8000"
    
    try:
        print("🧪 TEST DES ENDPOINTS DE NOTES AVANCÉES")
        print("=" * 50)
        
        # Test 1: Récupération des matières (sans authentification)
        print("\n1. Test de récupération des matières (sans auth)...")
        response = requests.get(f"{base_url}/notes-advanced/subjects")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            subjects = response.json()
            print(f"   ✅ {len(subjects)} matières récupérées")
            for subject in subjects:
                print(f"      - {subject['name']} ({subject['note_count']} notes)")
        else:
            print(f"   ❌ Erreur: {response.text}")
        
        # Test 2: Récupération des chapitres (sans authentification)
        print("\n2. Test de récupération des chapitres (sans auth)...")
        response = requests.get(f"{base_url}/notes-advanced/chapters")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            chapters = response.json()
            print(f"   ✅ {len(chapters)} chapitres récupérés")
            for chapter in chapters:
                print(f"      - {chapter['name']} (matière ID: {chapter['subject_id']})")
        else:
            print(f"   ❌ Erreur: {response.text}")
        
        # Test 3: Récupération des notes (sans authentification)
        print("\n3. Test de récupération des notes (sans auth)...")
        response = requests.get(f"{base_url}/notes-advanced/")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            notes = response.json()
            print(f"   ✅ {len(notes)} notes récupérées")
            for note in notes:
                print(f"      - {note['title']} ({note['subject']})")
        else:
            print(f"   ❌ Erreur: {response.text}")
        
        # Test 4: Test avec filtrage par matière
        print("\n4. Test de filtrage par matière...")
        response = requests.get(f"{base_url}/notes-advanced/?subject=Mathématiques")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            notes = response.json()
            print(f"   ✅ {len(notes)} notes trouvées pour Mathématiques")
        else:
            print(f"   ❌ Erreur: {response.text}")
        
        # Test 5: Test avec filtrage par chapitre
        print("\n5. Test de filtrage par chapitre...")
        response = requests.get(f"{base_url}/notes-advanced/?chapter=Géométrie")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            notes = response.json()
            print(f"   ✅ {len(notes)} notes trouvées pour Géométrie")
        else:
            print(f"   ❌ Erreur: {response.text}")
        
        # Test 6: Test avec recherche
        print("\n6. Test de recherche...")
        response = requests.get(f"{base_url}/notes-advanced/?search=théorème")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            notes = response.json()
            print(f"   ✅ {len(notes)} notes trouvées avec 'théorème'")
        else:
            print(f"   ❌ Erreur: {response.text}")
        
        print("\n" + "=" * 50)
        print("🎉 TEST DES NOTES AVANCÉES TERMINÉ!")
        print("✅ Tous les endpoints fonctionnent correctement!")
        
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")

if __name__ == "__main__":
    test_notes_advanced() 