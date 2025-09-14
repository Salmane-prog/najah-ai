import requests
import json

def test_cors_request():
    """Test de requête CORS depuis le frontend"""
    url = "http://localhost:8000/notes-advanced/"
    
    # Headers simulés du frontend
    headers = {
        'Content-Type': 'application/json',
        'Origin': 'http://localhost:3001',
        'Referer': 'http://localhost:3001/'
    }
    
    note_data = {
        "title": "Test CORS",
        "content": "Test de connexion depuis le frontend",
        "subject": "Mathématiques",
        "chapter": "Test",
        "tags": "[\"cors\", \"test\"]",
        "color": "bg-blue-100"
    }
    
    try:
        print(f"Test de requête CORS vers: {url}")
        print(f"Headers: {headers}")
        print(f"Données: {json.dumps(note_data, indent=2)}")
        
        # Test OPTIONS (preflight)
        print("\n1. Test OPTIONS (preflight):")
        options_response = requests.options(url, headers=headers)
        print(f"Status: {options_response.status_code}")
        print(f"Headers: {dict(options_response.headers)}")
        
        # Test POST
        print("\n2. Test POST:")
        post_response = requests.post(url, json=note_data, headers=headers)
        print(f"Status: {post_response.status_code}")
        print(f"Response: {post_response.text}")
        
        if post_response.status_code == 200:
            print("✅ Requête CORS réussie!")
        else:
            print("❌ Erreur CORS")
            
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    test_cors_request() 