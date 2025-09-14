import requests
import json

def test_organization_milestones():
    """Test des endpoints organization pour vérifier les propriétés milestones"""
    
    base_url = "http://localhost:8000/organization"
    
    # Test des objectifs d'apprentissage
    print("🧪 Test des objectifs d'apprentissage...")
    try:
        response = requests.get(f"{base_url}/learning-goals")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            goals = response.json()
            print(f"Nombre d'objectifs: {len(goals)}")
            for goal in goals:
                print(f"  - {goal['title']}: milestones = {len(goal.get('milestones', []))} étapes")
                if 'milestones' in goal:
                    for milestone in goal['milestones']:
                        status = "✅" if milestone.get('completed', False) else "⏳"
                        print(f"    {status} {milestone['title']}")
        else:
            print(f"Erreur: {response.text}")
    except Exception as e:
        print(f"Erreur de connexion: {e}")
    
    # Test des devoirs
    print("\n🧪 Test des devoirs...")
    try:
        response = requests.get(f"{base_url}/homework")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            homework = response.json()
            print(f"Nombre de devoirs: {len(homework)}")
            for hw in homework:
                print(f"  - {hw['title']}: tags = {len(hw.get('tags', []))} tags")
        else:
            print(f"Erreur: {response.text}")
    except Exception as e:
        print(f"Erreur de connexion: {e}")
    
    # Test des sessions d'étude
    print("\n🧪 Test des sessions d'étude...")
    try:
        response = requests.get(f"{base_url}/study-sessions")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            sessions = response.json()
            print(f"Nombre de sessions: {len(sessions)}")
            for session in sessions:
                print(f"  - {session['title']}: goals = {len(session.get('goals', []))} objectifs")
        else:
            print(f"Erreur: {response.text}")
    except Exception as e:
        print(f"Erreur de connexion: {e}")

if __name__ == "__main__":
    test_organization_milestones() 