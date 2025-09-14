#!/usr/bin/env python3
"""
Test de la correction finale - Vérification des emails et scores
"""

import requests

print("🧪 Test de la correction finale")
print("=" * 50)

BASE_URL = "http://localhost:8000"

try:
    # Login
    login = requests.post(f"{BASE_URL}/api/v1/auth/login", json={
        "email": "marizee.dubois@najah.ai",
        "password": "password123"
    })

    if login.status_code == 200:
        token = login.json().get("access_token")
        headers = {"Authorization": f"Bearer {token}"}
        print("✅ Login OK")

        # Test endpoint teacher-dashboard/students
        response = requests.get(f"{BASE_URL}/api/v1/teacher-dashboard/students", headers=headers)
        print(f"Status: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            students = data.get('students', [])
            print(f"✅ {len(students)} étudiants")

            # Vérifier les données de chaque étudiant
            for i, student in enumerate(students, 1):
                print(f"\n📊 Étudiant {i}:")
                print(f"   ID: {student.get('id')}")
                print(f"   Nom: {student.get('name')}")
                print(f"   Email: {student.get('email')}")
                print(f"   Score moyen: {student.get('average_score')}%")
                print(f"   Tentatives: {student.get('total_attempts')}")
                print(f"   Progression: {student.get('progression')}%")
                print(f"   Dernière activité: {student.get('last_activity')}")

            # Vérifications spécifiques
            print(f"\n🔍 Vérifications:")
            emails_defined = sum(1 for s in students if s.get('email') and s.get('email') != 'Email non défini')
            scores_above_zero = sum(1 for s in students if s.get('average_score', 0) > 0)
            activities_defined = sum(1 for s in students if s.get('last_activity'))
            
            print(f"   Emails définis: {emails_defined}/{len(students)}")
            print(f"   Scores > 0: {scores_above_zero}/{len(students)}")
            print(f"   Activités définies: {activities_defined}/{len(students)}")

            if emails_defined == len(students):
                print("🎉 Tous les emails sont maintenant récupérés !")
            else:
                print("⚠️ Certains emails ne sont pas récupérés")

        else:
            print(f"❌ Erreur {response.status_code}")
    else:
        print(f"❌ Login échoué: {login.status_code}")

except Exception as e:
    print(f"❌ Erreur: {e}")






