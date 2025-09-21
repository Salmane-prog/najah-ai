#!/usr/bin/env python3
"""
Test de la récupération des données détaillées des étudiants
"""

import requests
import json

def test_donnees_etudiants():
    """Tester la récupération des données détaillées"""
    print("🧪 Test de la récupération des données détaillées des étudiants")
    print("=" * 70)
    
    BASE_URL = "http://localhost:8000"
    
    # Connexion
    try:
        print("1️⃣ Connexion professeur...")
        login_response = requests.post(f"{BASE_URL}/api/v1/auth/login", json={
            "email": "marizee.dubois@najah.ai",
            "password": "password123"
        })
        
        if login_response.status_code == 200:
            token = login_response.json().get("access_token")
            headers = {"Authorization": f"Bearer {token}"}
            print("✅ Connexion réussie")
            
            # Test endpoint
            print("\n2️⃣ Test endpoint /api/v1/teacher-dashboard/students...")
            response = requests.get(f"{BASE_URL}/api/v1/teacher-dashboard/students", headers=headers)
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                students = data.get('students', [])
                print(f"✅ {len(students)} étudiants récupérés")
                
                # Vérifier les données détaillées
                print("\n3️⃣ Vérification des données détaillées...")
                
                for i, student in enumerate(students):
                    print(f"\n📊 Étudiant {i+1}:")
                    print(f"   ID: {student.get('id')}")
                    print(f"   Nom: {student.get('name')}")
                    print(f"   Email: {student.get('email')}")
                    print(f"   Classe: {student.get('class_name')}")
                    print(f"   Score moyen: {student.get('average_score')}%")
                    print(f"   Tentatives: {student.get('total_attempts')}")
                    print(f"   Progression: {student.get('progression')}%")
                    print(f"   Dernière activité: {student.get('last_activity')}")
                    print(f"   XP total: {student.get('total_xp')}")
                    print(f"   Badges: {student.get('badges_count')}")
                    print(f"   Niveau: {student.get('level')}")
                
                # Vérifier si les données sont plus complètes
                print(f"\n4️⃣ Analyse des données...")
                
                emails_defined = sum(1 for s in students if s.get('email') != "Email non défini")
                scores_above_zero = sum(1 for s in students if s.get('average_score', 0) > 0)
                activities_defined = sum(1 for s in students if s.get('last_activity') is not None)
                
                print(f"   Emails définis: {emails_defined}/{len(students)}")
                print(f"   Scores > 0: {scores_above_zero}/{len(students)}")
                print(f"   Activités définies: {activities_defined}/{len(students)}")
                
                if emails_defined > 0 or scores_above_zero > 0 or activities_defined > 0:
                    print("🎉 Certaines données sont maintenant récupérées !")
                else:
                    print("⚠️ Les données sont toujours à 0 ou non définies")
                    
            else:
                print(f"❌ Erreur {response.status_code}")
                
        else:
            print(f"❌ Connexion échouée: {login_response.status_code}")
            
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    test_donnees_etudiants()









