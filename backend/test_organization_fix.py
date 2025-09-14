import requests
import json

def test_organization_endpoints():
    """Test des endpoints organization pour vérifier les propriétés tags et goals"""
    
    base_url = "http://localhost:8000/organization"
    
    # Test des devoirs
    print("🧪 Test des devoirs...")
    try:
        response = requests.get(f"{base_url}/homework")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            homework = response.json()
            print(f"Nombre de devoirs: {len(homework)}")
            for hw in homework:
                print(f"  - {hw['title']}: tags = {hw.get('tags', 'MISSING')}")
        else:
            print(f"Erreur: {response.text}")
    except Exception as e:
        print(f"Erreur de connexion: {e}")
    
    print("\n🧪 Test des sessions d'étude...")
    try:
        response = requests.get(f"{base_url}/study-sessions")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            sessions = response.json()
            print(f"Nombre de sessions: {len(sessions)}")
            for session in sessions:
                print(f"  - {session['title']}: goals = {session.get('goals', 'MISSING')}")
        else:
            print(f"Erreur: {response.text}")
    except Exception as e:
        print(f"Erreur de connexion: {e}")
    
    print("\n🧪 Test des rappels...")
    try:
        response = requests.get(f"{base_url}/reminders")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            reminders = response.json()
            print(f"Nombre de rappels: {len(reminders)}")
        else:
            print(f"Erreur: {response.text}")
    except Exception as e:
        print(f"Erreur de connexion: {e}")
    
    print("\n🧪 Test des objectifs d'apprentissage...")
    try:
        response = requests.get(f"{base_url}/learning-goals")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            goals = response.json()
            print(f"Nombre d'objectifs: {len(goals)}")
        else:
            print(f"Erreur: {response.text}")
    except Exception as e:
        print(f"Erreur de connexion: {e}")

if __name__ == "__main__":
    test_organization_endpoints() 