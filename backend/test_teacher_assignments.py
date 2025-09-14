#!/usr/bin/env python3
"""
Script de test pour les API des assignations du professeur
"""

import requests
import json
from datetime import datetime, timedelta

# Configuration
BASE_URL = "http://localhost:8000"
API_BASE = f"{BASE_URL}/api/v1"

def test_teacher_assignments():
    """Tester les API des assignations du professeur"""
    
    print("🧪 Test des API des assignations du professeur")
    print("=" * 50)
    
    # 1. Test de connexion
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✅ Serveur accessible")
        else:
            print("❌ Serveur non accessible")
            return
    except Exception as e:
        print(f"❌ Erreur de connexion: {e}")
        return
    
    # 2. Test de récupération des étudiants
    print("\n📚 Test de récupération des étudiants...")
    try:
        response = requests.get(f"{API_BASE}/teacher-assignments/students")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            students = response.json()
            print(f"✅ {len(students)} étudiants trouvés")
            for student in students[:3]:  # Afficher les 3 premiers
                print(f"   - {student.get('first_name', '')} {student.get('last_name', '')} ({student.get('username', '')})")
        else:
            print(f"❌ Erreur: {response.text}")
    except Exception as e:
        print(f"❌ Erreur: {e}")
    
    # 3. Test de récupération des devoirs
    print("\n📝 Test de récupération des devoirs...")
    try:
        response = requests.get(f"{API_BASE}/teacher-assignments/homework")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            homeworks = response.json()
            print(f"✅ {len(homeworks)} devoirs trouvés")
            for homework in homeworks[:3]:  # Afficher les 3 premiers
                print(f"   - {homework.get('title', '')} (Status: {homework.get('status', '')})")
        else:
            print(f"❌ Erreur: {response.text}")
    except Exception as e:
        print(f"❌ Erreur: {e}")
    
    # 4. Test de récupération des objectifs
    print("\n🎯 Test de récupération des objectifs...")
    try:
        response = requests.get(f"{API_BASE}/teacher-assignments/learning-goals")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            goals = response.json()
            print(f"✅ {len(goals)} objectifs trouvés")
            for goal in goals[:3]:  # Afficher les 3 premiers
                print(f"   - {goal.get('title', '')} (Progress: {goal.get('progress', 0)}%)")
        else:
            print(f"❌ Erreur: {response.text}")
    except Exception as e:
        print(f"❌ Erreur: {e}")
    
    # 5. Test des statistiques
    print("\n📊 Test des statistiques...")
    try:
        response = requests.get(f"{API_BASE}/teacher-assignments/homework/stats")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            stats = response.json()
            print(f"✅ Statistiques récupérées:")
            print(f"   - Total devoirs: {stats.get('total_homework', 0)}")
            print(f"   - Terminés: {stats.get('completed_homework', 0)}")
            print(f"   - En attente: {stats.get('pending_homework', 0)}")
            print(f"   - En retard: {stats.get('overdue_homework', 0)}")
        else:
            print(f"❌ Erreur: {response.text}")
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    test_teacher_assignments() 