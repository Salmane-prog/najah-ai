import requests
import json

# Configuration
BASE_URL = "http://localhost:8000"
API_URL = f"{BASE_URL}/api/v1"

def test_learning_goals_api():
    """Test de l'API des objectifs d'apprentissage"""
    
    # Simuler un token JWT (vous devrez utiliser un vrai token)
    headers = {
        "Authorization": "Bearer test_token",
        "Content-Type": "application/json"
    }
    
    print("🧪 Test de l'API des objectifs d'apprentissage")
    print("=" * 50)
    
    # Test 1: Récupérer les objectifs
    print("\n1. Test GET /api/v1/learning-goals")
    try:
        response = requests.get(f"{API_URL}/learning-goals", headers=headers)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            goals = response.json()
            print(f"Nombre d'objectifs trouvés: {len(goals)}")
            for goal in goals[:3]:  # Afficher les 3 premiers
                print(f"  - {goal.get('title', 'Sans titre')} ({goal.get('status', 'N/A')})")
        else:
            print(f"Erreur: {response.text}")
    except Exception as e:
        print(f"Erreur de connexion: {e}")
    
    # Test 2: Créer un objectif
    print("\n2. Test POST /api/v1/learning-goals")
    new_goal = {
        "title": "Maîtriser les équations du second degré",
        "description": "Apprendre à résoudre les équations ax² + bx + c = 0",
        "subject": "Mathématiques",
        "target_date": "2024-02-15"
    }
    
    try:
        response = requests.post(f"{API_URL}/learning-goals", 
                               headers=headers, 
                               json=new_goal)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            created_goal = response.json()
            print(f"Objectif créé: {created_goal.get('title')}")
            goal_id = created_goal.get('id')
        else:
            print(f"Erreur: {response.text}")
            goal_id = None
    except Exception as e:
        print(f"Erreur de connexion: {e}")
        goal_id = None
    
    # Test 3: Mettre à jour un objectif (si créé avec succès)
    if goal_id:
        print(f"\n3. Test POST /api/v1/learning-goals/{goal_id}/update")
        update_data = {
            "progress": 0.5,
            "status": "active"
        }
        
        try:
            response = requests.post(f"{API_URL}/learning-goals/{goal_id}/update", 
                                   headers=headers, 
                                   json=update_data)
            print(f"Status: {response.status_code}")
            if response.status_code == 200:
                updated_goal = response.json()
                print(f"Objectif mis à jour: {updated_goal.get('title')} - Progression: {updated_goal.get('progress', 0) * 100}%")
            else:
                print(f"Erreur: {response.text}")
        except Exception as e:
            print(f"Erreur de connexion: {e}")
    
    print("\n" + "=" * 50)
    print("✅ Test terminé")

if __name__ == "__main__":
    test_learning_goals_api() 