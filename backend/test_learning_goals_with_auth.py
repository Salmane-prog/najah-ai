import requests
import json

# Configuration
BASE_URL = "http://localhost:8000"
API_URL = f"{BASE_URL}/api/v1"

def test_learning_goals_with_auth():
    """Test de l'API des objectifs d'apprentissage avec authentification"""
    
    print("🧪 Test de l'API des objectifs d'apprentissage avec authentification")
    print("=" * 60)
    
    # 1. Authentification
    print("\n1. Authentification...")
    auth_data = {
        "email": "salmane.hajouji@najah.ai",
        "password": "password123"
    }
    
    try:
        auth_response = requests.post(f"{API_URL}/auth/login", json=auth_data)
        print(f"Status: {auth_response.status_code}")
        
        if auth_response.status_code == 200:
            token_data = auth_response.json()
            token = token_data.get("access_token")
            print(f"✅ Authentification réussie")
            print(f"Token: {token[:20]}...")
        else:
            print(f"❌ Échec de l'authentification: {auth_response.text}")
            return
    except Exception as e:
        print(f"❌ Erreur d'authentification: {e}")
        return
    
    # Headers avec token
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # 2. Récupérer les objectifs existants
    print("\n2. Test GET /api/v1/learning-goals")
    try:
        response = requests.get(f"{API_URL}/learning-goals", headers=headers)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            goals = response.json()
            print(f"✅ {len(goals)} objectifs trouvés")
            for goal in goals[:3]:
                print(f"  - {goal.get('title', 'Sans titre')} ({goal.get('status', 'N/A')})")
        else:
            print(f"❌ Erreur: {response.text}")
    except Exception as e:
        print(f"❌ Erreur de connexion: {e}")
    
    # 3. Créer un nouvel objectif
    print("\n3. Test POST /api/v1/learning-goals")
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
            print(f"✅ Objectif créé: {created_goal.get('title')}")
            goal_id = created_goal.get('id')
        else:
            print(f"❌ Erreur: {response.text}")
            goal_id = None
    except Exception as e:
        print(f"❌ Erreur de connexion: {e}")
        goal_id = None
    
    # 4. Mettre à jour l'objectif (si créé avec succès)
    if goal_id:
        print(f"\n4. Test POST /api/v1/learning-goals/{goal_id}/update")
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
                print(f"✅ Objectif mis à jour: {updated_goal.get('title')} - Progression: {updated_goal.get('progress', 0) * 100}%")
            else:
                print(f"❌ Erreur: {response.text}")
        except Exception as e:
            print(f"❌ Erreur de connexion: {e}")
    
    # 5. Vérifier que l'objectif apparaît dans la liste
    print("\n5. Vérification de la liste mise à jour")
    try:
        response = requests.get(f"{API_URL}/learning-goals", headers=headers)
        if response.status_code == 200:
            goals = response.json()
            print(f"✅ {len(goals)} objectifs au total")
            # Chercher l'objectif créé
            created_goal_found = None
            for goal in goals:
                if goal.get('title') == new_goal['title']:
                    created_goal_found = goal
                    break
            
            if created_goal_found:
                print(f"✅ Objectif trouvé dans la liste: {created_goal_found.get('title')}")
            else:
                print("❌ Objectif créé non trouvé dans la liste")
        else:
            print(f"❌ Erreur lors de la vérification: {response.text}")
    except Exception as e:
        print(f"❌ Erreur de connexion: {e}")
    
    print("\n" + "=" * 60)
    print("✅ Test terminé")

if __name__ == "__main__":
    test_learning_goals_with_auth()
