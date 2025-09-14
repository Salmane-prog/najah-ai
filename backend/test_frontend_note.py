import requests
import json

def test_frontend_note_creation():
    """Test de création d'une note avec les mêmes données que le frontend"""
    url = "http://localhost:8000/notes-advanced/"
    
    # Données exactes que le frontend envoie
    note_data = {
        "title": "Test frontend",
        "content": "Contenu de test",
        "subject": "Mathématiques",
        "chapter": "Test chapitre",
        "tags": "[\"test\", \"frontend\"]",
        "color": "bg-blue-100"
    }
    
    try:
        print(f"Envoi de la requête à: {url}")
        print(f"Données: {json.dumps(note_data, indent=2)}")
        
        response = requests.post(url, json=note_data)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("✅ Note créée avec succès!")
            note = response.json()
            print(f"ID: {note['id']}")
            print(f"Titre: {note['title']}")
            print(f"Sujet: {note['subject']}")
        else:
            print("❌ Erreur lors de la création")
            
    except Exception as e:
        print(f"❌ Erreur de connexion: {e}")

if __name__ == "__main__":
    test_frontend_note_creation() 