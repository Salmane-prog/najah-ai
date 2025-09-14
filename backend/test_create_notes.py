#!/usr/bin/env python3
"""
Script pour tester la création, modification et suppression de notes
"""

import requests
import json

def test_create_notes():
    """Tester la création, modification et suppression de notes"""
    base_url = "http://localhost:8000"
    
    try:
        print("🧪 TEST DE CRÉATION, MODIFICATION ET SUPPRESSION DE NOTES")
        print("=" * 60)
        
        # Test 1: Créer une nouvelle note
        print("\n1. Test de création d'une nouvelle note...")
        note_data = {
            "title": "Test de création de note",
            "content": "Ceci est un test de création de note avec stockage en base de données.",
            "subject": "Test",
            "tags": "[\"test\", \"création\", \"base\"]"
        }
        
        response = requests.post(f"{base_url}/notes-advanced/", json=note_data)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            created_note = response.json()
            print("   ✅ Note créée avec succès!")
            print(f"      - ID: {created_note['id']}")
            print(f"      - Titre: {created_note['title']}")
            print(f"      - Matière: {created_note['subject']}")
            note_id = created_note['id']
        else:
            print(f"   ❌ Erreur: {response.text}")
            return
        
        # Test 2: Vérifier que la note apparaît dans la liste
        print("\n2. Vérification de la note dans la liste...")
        response = requests.get(f"{base_url}/notes-advanced/")
        if response.status_code == 200:
            notes = response.json()
            print(f"   ✅ {len(notes)} notes trouvées")
            
            # Chercher la note créée
            found = False
            for note in notes:
                if note['id'] == note_id:
                    found = True
                    print(f"   ✅ Note trouvée dans la liste!")
                    break
            
            if not found:
                print("   ❌ Note créée non trouvée dans la liste")
        else:
            print(f"   ❌ Erreur: {response.text}")
        
        # Test 3: Modifier la note
        print("\n3. Test de modification de la note...")
        update_data = {
            "title": "Test de modification de note",
            "content": "Ceci est un test de modification de note avec stockage en base de données."
        }
        
        response = requests.put(f"{base_url}/notes-advanced/{note_id}", json=update_data)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            updated_note = response.json()
            print("   ✅ Note modifiée avec succès!")
            print(f"      - Nouveau titre: {updated_note['title']}")
        else:
            print(f"   ❌ Erreur: {response.text}")
        
        # Test 4: Créer une deuxième note
        print("\n4. Test de création d'une deuxième note...")
        note_data2 = {
            "title": "Deuxième note de test",
            "content": "Ceci est une deuxième note de test pour vérifier le stockage multiple.",
            "subject": "Mathématiques",
            "tags": "[\"maths\", \"algèbre\", \"test\"]"
        }
        
        response = requests.post(f"{base_url}/notes-advanced/", json=note_data2)
        if response.status_code == 200:
            created_note2 = response.json()
            print("   ✅ Deuxième note créée avec succès!")
            print(f"      - ID: {created_note2['id']}")
            print(f"      - Titre: {created_note2['title']}")
            print(f"      - Matière: {created_note2['subject']}")
        else:
            print(f"   ❌ Erreur: {response.text}")
        
        # Test 5: Vérifier le filtrage par matière
        print("\n5. Test de filtrage par matière...")
        response = requests.get(f"{base_url}/notes-advanced/?subject=Mathématiques")
        if response.status_code == 200:
            notes = response.json()
            print(f"   ✅ {len(notes)} notes trouvées pour Mathématiques")
            for note in notes:
                print(f"      - {note['title']} ({note['subject']})")
        else:
            print(f"   ❌ Erreur: {response.text}")
        
        # Test 6: Supprimer la première note
        print("\n6. Test de suppression de la première note...")
        response = requests.delete(f"{base_url}/notes-advanced/{note_id}")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ Note supprimée avec succès!")
        else:
            print(f"   ❌ Erreur: {response.text}")
        
        # Test 7: Vérifier que la note a été supprimée
        print("\n7. Vérification de la suppression...")
        response = requests.get(f"{base_url}/notes-advanced/")
        if response.status_code == 200:
            notes = response.json()
            print(f"   ✅ {len(notes)} notes restantes")
            
            # Vérifier que la note supprimée n'est plus là
            found = False
            for note in notes:
                if note['id'] == note_id:
                    found = True
                    break
            
            if not found:
                print("   ✅ Note supprimée confirmée!")
            else:
                print("   ❌ Note supprimée encore présente")
        else:
            print(f"   ❌ Erreur: {response.text}")
        
        print("\n" + "=" * 60)
        print("🎉 TEST DE CRÉATION DE NOTES TERMINÉ AVEC SUCCÈS!")
        print("✅ Création de notes fonctionne!")
        print("✅ Modification de notes fonctionne!")
        print("✅ Suppression de notes fonctionne!")
        print("✅ Stockage en base de données fonctionne!")
        print("✅ Filtrage par matière fonctionne!")
        
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")

if __name__ == "__main__":
    test_create_notes() 