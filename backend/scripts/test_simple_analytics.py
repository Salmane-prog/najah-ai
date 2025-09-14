#!/usr/bin/env python3
"""
Script de test simple pour l'endpoint analytics
"""

import requests
import json

def test_simple_analytics():
    """Tester l'endpoint analytics de manière simple."""
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
        
        print("=== TEST SIMPLE ANALYTICS ===")
        
        # Tester l'endpoint pour un étudiant spécifique
        student_id = 4  # student1
        response = requests.get(f"{base_url}/api/v1/student_analytics/student/{student_id}/analytics", headers=headers)
        print(f"📡 Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Données récupérées avec succès!")
            print(f"   Étudiant: {data.get('student', {}).get('name', 'N/A')}")
            analytics = data.get('analytics', {})
            print(f"   Progression: {analytics.get('overall_progress', 0)}%")
            print(f"   Quiz complétés: {analytics.get('quizzes_completed', 0)}")
            print(f"   Score moyen: {analytics.get('average_score', 0)}%")
            print(f"   Classes: {analytics.get('classes_count', 0)}")
            print(f"   Badges: {analytics.get('badges_count', 0)}")
            print(f"   Dernière activité: {analytics.get('last_activity', 'N/A')}")
        else:
            print(f"❌ Erreur: {response.status_code}")
            print(f"   Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")

if __name__ == "__main__":
    test_simple_analytics() 