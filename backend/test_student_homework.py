#!/usr/bin/env python3
"""
Script pour tester l'API étudiant
"""

import requests
import json
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:8000"
API_BASE = f"{BASE_URL}/api/v1"

def get_student_auth_token():
    """Obtenir un token d'authentification pour un étudiant"""
    
    # Données de connexion pour un étudiant
    login_data = {
        "email": "salmane.hajouji@najah.ai",  # Email de l'étudiant
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

def test_student_homework():
    """Tester l'API étudiant"""
    
    print("👤 Test de l'API étudiant")
    print("=" * 40)
    
    # 1. Test sans authentification (endpoint de test)
    print("\n📝 Test de récupération des devoirs (sans auth)...")
    try:
        response = requests.get(f"{API_BASE}/student-organization/test-homework")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            homeworks = response.json()
            print(f"✅ {len(homeworks)} devoirs trouvés")
            for homework in homeworks[:3]:
                print(f"   - {homework.get('title', '')} (Status: {homework.get('status', '')})")
                print(f"     Assigné à: {homework.get('assigned_to', '')}, Date: {homework.get('due_date', '')}")
        else:
            print(f"❌ Erreur: {response.text}")
    except Exception as e:
        print(f"❌ Erreur: {e}")
    
    # 2. Test avec authentification étudiant
    print("\n🔑 Obtention du token étudiant...")
    token = get_student_auth_token()
    
    if not token:
        print("❌ Impossible d'obtenir le token étudiant")
        return
    
    print("✅ Token étudiant obtenu avec succès")
    
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    # 3. Test de récupération des devoirs avec auth
    print("\n📝 Test de récupération des devoirs (avec auth)...")
    try:
        response = requests.get(f"{API_BASE}/student-organization/homework", headers=headers)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            homeworks = response.json()
            print(f"✅ {len(homeworks)} devoirs trouvés")
            for homework in homeworks[:3]:
                print(f"   - {homework.get('title', '')} (Status: {homework.get('status', '')})")
                print(f"     Matière: {homework.get('subject', '')}, Priorité: {homework.get('priority', '')}")
                print(f"     Date limite: {homework.get('due_date', '')}")
        else:
            print(f"❌ Erreur: {response.text}")
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    test_student_homework() 