#!/usr/bin/env python3
"""
Script pour tester les assignations avec authentification
"""

import requests
import json
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:8000"
API_BASE = f"{BASE_URL}/api/v1"

def get_auth_token():
    """Obtenir un token d'authentification pour un professeur"""
    
    # Données de connexion pour un professeur
    login_data = {
        "email": "marie.dubois@najah.ai",  # Email de l'utilisateur marie.dubois
        "password": "password123"
    }
    
    try:
        response = requests.post(f"{API_BASE}/auth/login", json=login_data)
        if response.status_code == 200:
            data = response.json()
            return data.get("access_token")
        else:
            print(f"❌ Erreur de connexion: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Erreur de connexion: {e}")
        return None

def test_assignments_with_auth():
    """Tester les assignations avec authentification"""
    
    print("🔐 Test des assignations avec authentification")
    print("=" * 50)
    
    # 1. Obtenir un token
    print("\n🔑 Obtention du token d'authentification...")
    token = get_auth_token()
    
    if not token:
        print("❌ Impossible d'obtenir le token")
        return
    
    print("✅ Token obtenu avec succès")
    
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    # 2. Test de récupération des étudiants
    print("\n👥 Test de récupération des étudiants...")
    try:
        response = requests.get(f"{API_BASE}/teacher-assignments/students", headers=headers)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            students = response.json()
            print(f"✅ {len(students)} étudiants trouvés")
            for student in students[:3]:
                print(f"   - {student.get('first_name', '')} {student.get('last_name', '')} ({student.get('username', '')})")
        else:
            print(f"❌ Erreur: {response.text}")
    except Exception as e:
        print(f"❌ Erreur: {e}")
    
    # 3. Test de récupération des devoirs
    print("\n📝 Test de récupération des devoirs...")
    try:
        response = requests.get(f"{API_BASE}/teacher-assignments/homework", headers=headers)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            homeworks = response.json()
            print(f"✅ {len(homeworks)} devoirs trouvés")
            for homework in homeworks[:3]:
                print(f"   - {homework.get('title', '')} (Status: {homework.get('status', '')})")
                print(f"     Matière: {homework.get('subject', '')}, Priorité: {homework.get('priority', '')}")
        else:
            print(f"❌ Erreur: {response.text}")
    except Exception as e:
        print(f"❌ Erreur: {e}")
    
    # 4. Test de récupération des objectifs
    print("\n🎯 Test de récupération des objectifs...")
    try:
        response = requests.get(f"{API_BASE}/teacher-assignments/learning-goals", headers=headers)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            goals = response.json()
            print(f"✅ {len(goals)} objectifs trouvés")
            for goal in goals[:3]:
                print(f"   - {goal.get('title', '')} (Progress: {goal.get('progress', 0)*100}%)")
                print(f"     Matière: {goal.get('subject', '')}, Status: {goal.get('status', '')}")
        else:
            print(f"❌ Erreur: {response.text}")
    except Exception as e:
        print(f"❌ Erreur: {e}")
    
    # 5. Test de récupération des classes
    print("\n📚 Test de récupération des classes...")
    try:
        response = requests.get(f"{API_BASE}/class_groups/", headers=headers)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            classes = response.json()
            print(f"✅ {len(classes)} classes trouvées")
            for class_group in classes[:3]:
                print(f"   - {class_group.get('name', '')} ({class_group.get('subject', '')})")
        else:
            print(f"❌ Erreur: {response.text}")
    except Exception as e:
        print(f"❌ Erreur: {e}")
    
    # 6. Test de création d'un devoir
    print("\n➕ Test de création d'un devoir...")
    try:
        homework_data = {
            "title": "Devoir de test - Créé via API",
            "description": "Ce devoir a été créé pour tester l'API",
            "subject": "Test",
            "class_id": 4,  # Utiliser une classe existante
            "due_date": (datetime.now().replace(hour=23, minute=59)).isoformat(),
            "priority": "medium",
            "estimated_time": 60
        }
        
        response = requests.post(f"{API_BASE}/teacher-assignments/homework", 
                               json=homework_data, headers=headers)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            created_homeworks = response.json()
            print(f"✅ {len(created_homeworks)} devoir(s) créé(s)")
            for hw in created_homeworks:
                print(f"   - {hw.get('title', '')} (ID: {hw.get('id', '')})")
        else:
            print(f"❌ Erreur: {response.text}")
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    test_assignments_with_auth() 