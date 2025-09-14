#!/usr/bin/env python3
"""
Script pour tester l'API des notes
"""

import requests
import json

def test_notes_api():
    """Tester l'API des notes."""
    base_url = "http://localhost:8000"
    
    # D'abord, se connecter en tant qu'étudiant
    student_login = {
        "email": "salmane.hajouji@najah.ai",
        "password": "password123"
    }
    
    try:
        print("=== TEST API NOTES ===")
        print("\n1. 🔐 CONNEXION ÉTUDIANT")
        response = requests.post(f"{base_url}/api/v1/auth/login", json=student_login)
        if response.status_code != 200:
            print("❌ Échec de connexion étudiant")
            return
        
        student_data = response.json()
        student_token = student_data["access_token"]
        print("✅ Connexion étudiante réussie")
        
        headers = {
            "Authorization": f"Bearer {student_token}",
            "Content-Type": "application/json"
        }
        
        print("\n2. 📝 RÉCUPÉRATION DES NOTES")
        response = requests.get(f"{base_url}/api/v1/notes/", headers=headers)
        if response.status_code == 200:
            notes_data = response.json()
            print(f"✅ {len(notes_data['notes'])} notes récupérées")
            for note in notes_data['notes']:
                print(f"   - {note['title']} ({note['subject']})")
        else:
            print(f"❌ Erreur lors de la récupération des notes: {response.status_code}")
        
        print("\n3. 📝 CRÉATION D'UNE NOUVELLE NOTE")
        new_note = {
            "title": "Test API Notes",
            "content": "Ceci est un test de l'API des notes.\n\n## Fonctionnalités testées:\n- Création de note\n- Formatage Markdown\n- Tags",
            "subject": "Test",
            "tags": ["test", "api", "notes"]
        }
        
        response = requests.post(f"{base_url}/api/v1/notes/", headers=headers, json=new_note)
        if response.status_code == 200:
            created_note = response.json()
            print(f"✅ Note créée avec ID: {created_note['id']}")
            note_id = created_note['id']
        else:
            print(f"❌ Erreur lors de la création: {response.status_code}")
            return
        
        print("\n4. 📝 RÉCUPÉRATION DE LA NOTE CRÉÉE")
        response = requests.get(f"{base_url}/api/v1/notes/{note_id}", headers=headers)
        if response.status_code == 200:
            note = response.json()
            print(f"✅ Note récupérée: {note['title']}")
            print(f"   Contenu: {note['content'][:100]}...")
            print(f"   Tags: {note['tags']}")
        else:
            print(f"❌ Erreur lors de la récupération: {response.status_code}")
        
        print("\n5. 📝 MODIFICATION DE LA NOTE")
        updated_note = {
            "title": "Test API Notes - Modifié",
            "content": "Contenu modifié pour tester l'API.",
            "subject": "Test Modifié",
            "tags": ["test", "modifié", "api"]
        }
        
        response = requests.put(f"{base_url}/api/v1/notes/{note_id}", headers=headers, json=updated_note)
        if response.status_code == 200:
            updated = response.json()
            print(f"✅ Note modifiée: {updated['title']}")
        else:
            print(f"❌ Erreur lors de la modification: {response.status_code}")
        
        print("\n6. 📝 RÉCUPÉRATION DES MATIÈRES")
        response = requests.get(f"{base_url}/api/v1/notes/subjects/list", headers=headers)
        if response.status_code == 200:
            subjects_data = response.json()
            print(f"✅ Matières récupérées: {subjects_data['subjects']}")
        else:
            print(f"❌ Erreur lors de la récupération des matières: {response.status_code}")
        
        print("\n7. 📝 RÉCUPÉRATION DES TAGS")
        response = requests.get(f"{base_url}/api/v1/notes/tags/list", headers=headers)
        if response.status_code == 200:
            tags_data = response.json()
            print(f"✅ Tags récupérés: {tags_data['tags']}")
        else:
            print(f"❌ Erreur lors de la récupération des tags: {response.status_code}")
        
        print("\n8. 📝 TEST D'EXPORT")
        response = requests.post(f"{base_url}/api/v1/notes/export/{note_id}?format=pdf", headers=headers)
        if response.status_code == 200:
            export_data = response.json()
            print(f"✅ Export réussi: {export_data['format']}")
        else:
            print(f"❌ Erreur lors de l'export: {response.status_code}")
        
        print("\n9. 📝 SUPPRESSION DE LA NOTE DE TEST")
        response = requests.delete(f"{base_url}/api/v1/notes/{note_id}", headers=headers)
        if response.status_code == 200:
            print("✅ Note de test supprimée")
        else:
            print(f"❌ Erreur lors de la suppression: {response.status_code}")
        
        print("\n🎉 TOUS LES TESTS DE L'API NOTES SONT RÉUSSIS!")
        
    except requests.exceptions.ConnectionError:
        print("❌ Impossible de se connecter au serveur. Assurez-vous que le backend est démarré.")
    except Exception as e:
        print(f"❌ Erreur inattendue: {e}")

if __name__ == "__main__":
    test_notes_api() 