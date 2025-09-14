#!/usr/bin/env python3
"""
Script de test final pour confirmer la correction des erreurs 405 des notes avancées
"""

import requests
import json

def test_final_notes_fix():
    """Test final de la correction des erreurs 405"""
    base_url = "http://localhost:8000"
    
    try:
        print("🧪 TEST FINAL DE CORRECTION DES ERREURS 405 - NOTES AVANCÉES")
        print("=" * 70)
        
        # Test 1: NotesAPI.getSubjects (erreur 405 originale)
        print("\n1. Test de NotesAPI.getSubjects...")
        response = requests.get(f"{base_url}/notes-advanced/subjects")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            subjects = response.json()
            print(f"   ✅ SUCCÈS: {len(subjects)} matières récupérées")
            for subject in subjects:
                print(f"      - {subject['name']} ({subject['note_count']} notes)")
        else:
            print(f"   ❌ ERREUR: {response.status_code} - {response.text}")
            return False
        
        # Test 2: NotesAPI.getChapters (erreur 405 originale)
        print("\n2. Test de NotesAPI.getChapters...")
        response = requests.get(f"{base_url}/notes-advanced/chapters")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            chapters = response.json()
            print(f"   ✅ SUCCÈS: {len(chapters)} chapitres récupérés")
            for chapter in chapters:
                print(f"      - {chapter['name']} (matière ID: {chapter['subject_id']})")
        else:
            print(f"   ❌ ERREUR: {response.status_code} - {response.text}")
            return False
        
        # Test 3: NotesAPI.getNotes (erreur 405 originale)
        print("\n3. Test de NotesAPI.getNotes...")
        response = requests.get(f"{base_url}/notes-advanced/")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            notes = response.json()
            print(f"   ✅ SUCCÈS: {len(notes)} notes récupérées")
            for note in notes:
                print(f"      - {note['title']} ({note['subject']})")
        else:
            print(f"   ❌ ERREUR: {response.status_code} - {response.text}")
            return False
        
        # Test 4: Test avec paramètres de filtrage
        print("\n4. Test avec paramètres de filtrage...")
        response = requests.get(f"{base_url}/notes-advanced/?subject=Mathématiques&chapter=Géométrie")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            notes = response.json()
            print(f"   ✅ SUCCÈS: {len(notes)} notes trouvées avec filtres")
        else:
            print(f"   ❌ ERREUR: {response.status_code} - {response.text}")
            return False
        
        # Test 5: Test avec recherche
        print("\n5. Test avec recherche...")
        response = requests.get(f"{base_url}/notes-advanced/?search=mathématiques")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            notes = response.json()
            print(f"   ✅ SUCCÈS: {len(notes)} notes trouvées avec recherche")
        else:
            print(f"   ❌ ERREUR: {response.status_code} - {response.text}")
            return False
        
        # Test 6: Test avec subject_id pour chapitres
        print("\n6. Test avec subject_id pour chapitres...")
        response = requests.get(f"{base_url}/notes-advanced/chapters?subject_id=1")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            chapters = response.json()
            print(f"   ✅ SUCCÈS: {len(chapters)} chapitres trouvés pour matière ID 1")
        else:
            print(f"   ❌ ERREUR: {response.status_code} - {response.text}")
            return False
        
        print("\n" + "=" * 70)
        print("🎉 TEST FINAL DE CORRECTION TERMINÉ AVEC SUCCÈS!")
        print("✅ Toutes les erreurs 405 sont RÉSOLUES!")
        print("✅ NotesAPI.getSubjects fonctionne correctement!")
        print("✅ NotesAPI.getChapters fonctionne correctement!")
        print("✅ NotesAPI.getNotes fonctionne correctement!")
        print("✅ Le filtrage et la recherche fonctionnent correctement!")
        print("✅ Les endpoints sont accessibles sans authentification!")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du test final: {e}")
        return False

if __name__ == "__main__":
    success = test_final_notes_fix()
    if success:
        print("\n🎯 RÉSOLUTION COMPLÈTE: Les erreurs 405 des notes avancées sont corrigées!")
    else:
        print("\n❌ PROBLÈME: Il reste des erreurs à corriger.") 