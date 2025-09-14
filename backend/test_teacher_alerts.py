#!/usr/bin/env python3
"""
Script pour tester l'endpoint teacher-alerts
"""

import requests
import json

def test_teacher_alerts():
    # D'abord, obtenir un token en se connectant
    login_url = "http://localhost:8000/api/v1/auth/login"
    login_data = {
        "email": "marie.dubois@najah.ai",
        "password": "salmane123@"
    }
    
    try:
        print("🔐 Connexion pour obtenir le token...")
        login_response = requests.post(login_url, json=login_data)
        
        if login_response.status_code != 200:
            print(f"❌ Erreur de connexion: {login_response.status_code}")
            print(f"   Réponse: {login_response.text}")
            return
            
        login_result = login_response.json()
        token = login_result.get('access_token')
        print(f"✅ Token obtenu: {token[:20]}...")
        
        # Maintenant tester l'endpoint teacher-alerts
        alerts_url = "http://localhost:8000/api/v1/notifications/teacher-alerts"
        headers = {"Authorization": f"Bearer {token}"}
        
        print("\n🔔 Test de l'endpoint teacher-alerts...")
        alerts_response = requests.get(alerts_url, headers=headers)
        
        print(f"📊 Status Code: {alerts_response.status_code}")
        print(f"📊 Headers: {dict(alerts_response.headers)}")
        
        if alerts_response.status_code == 200:
            alerts_data = alerts_response.json()
            print(f"✅ Teacher alerts récupérées!")
            print(f"   Alerts: {json.dumps(alerts_data, indent=2)}")
        else:
            print(f"❌ Erreur teacher-alerts!")
            print(f"   Erreur: {alerts_response.text}")
            
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")

if __name__ == "__main__":
    test_teacher_alerts() 