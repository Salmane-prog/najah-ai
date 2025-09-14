#!/usr/bin/env python3
"""
Script pour tester le nouvel endpoint d'analytics des étudiants
"""

import requests
import json

def test_student_analytics():
    """Tester l'endpoint d'analytics des étudiants."""
    base_url = "http://localhost:8000"
    
    # D'abord, se connecter pour obtenir un token
    login_data = {
        "email": "marie.dubois@najah.ai",
        "password": "password123"
    }
    
    try:
        response = requests.post(f"{base_url}/api/v1/auth/login", json=login_data)
        if response.status_code != 200:
            print("❌ Échec de connexion")
            return
        
        data = response.json()
        token = data.get('access_token')
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        
        print("=== TEST DE L'ENDPOINT STUDENT ANALYTICS ===")
        
        # Tester l'endpoint pour tous les étudiants
        response = requests.get(f"{base_url}/api/v1/student_analytics/students/analytics", headers=headers)
        print(f"📡 Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Données récupérées avec succès!")
            print(f"   Total étudiants: {data.get('total_students', 0)}")
            
            # Afficher les données pour chaque étudiant
            for i, student_data in enumerate(data.get('students', [])):
                student = student_data.get('student', {})
                analytics = student_data.get('analytics', {})
                
                print(f"\n--- Étudiant {i+1} ---")
                print(f"   Nom: {student.get('name', 'N/A')}")
                print(f"   Email: {student.get('email', 'N/A')}")
                print(f"   Progression: {analytics.get('overall_progress', 0)}%")
                print(f"   Quiz complétés: {analytics.get('quizzes_completed', 0)}")
                print(f"   Score moyen: {analytics.get('average_score', 0)}%")
                print(f"   Classes: {analytics.get('classes_count', 0)}")
                print(f"   Badges: {analytics.get('badges_count', 0)}")
                print(f"   Dernière activité: {analytics.get('last_activity', 'N/A')}")
                
                # Afficher les classes
                classes = student_data.get('classes', [])
                if classes:
                    print(f"   Classes:")
                    for class_info in classes:
                        print(f"     - {class_info.get('name', 'N/A')} ({class_info.get('subject', 'N/A')}): {class_info.get('progress', 0)}%")
                else:
                    print(f"   Classes: Aucune classe")
                    
        else:
            print(f"❌ Erreur: {response.status_code}")
            print(f"   Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")

if __name__ == "__main__":
    test_student_analytics() 