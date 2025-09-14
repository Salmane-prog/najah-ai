import requests
import json

def test_users_endpoint():
    """Tester l'endpoint users pour voir les données retournées"""
    
    # URL de l'endpoint
    url = "http://localhost:8000/api/v1/users/students-by-role"
    
    # Headers (sans token pour voir l'erreur)
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"\nNombre d'étudiants: {len(data)}")
            for i, student in enumerate(data[:3]):  # Afficher les 3 premiers
                print(f"\nÉtudiant {i+1}:")
                print(f"  - Nom: {student.get('name')}")
                print(f"  - Email: {student.get('email')}")
                print(f"  - Classe: {student.get('class')}")
                
    except Exception as e:
        print(f"Erreur: {e}")

if __name__ == "__main__":
    test_users_endpoint() 