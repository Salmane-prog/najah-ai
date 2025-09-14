#!/usr/bin/env python3
"""
Script pour tester l'endpoint students
"""

import requests
import json

def test_students():
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
        
        # Maintenant tester l'endpoint students
        students_url = "http://localhost:8000/api/v1/users/students"
        headers = {"Authorization": f"Bearer {token}"}
        
        print("\n👥 Test de l'endpoint students...")
        students_response = requests.get(students_url, headers=headers)
        
        print(f"📊 Status Code: {students_response.status_code}")
        print(f"📊 Headers: {dict(students_response.headers)}")
        
        if students_response.status_code == 200:
            students_data = students_response.json()
            print(f"✅ Students récupérés!")
            print(f"   Nombre d'étudiants: {len(students_data)}")
            if students_data:
                print(f"   Premier étudiant: {students_data[0]}")
        else:
            print(f"❌ Erreur students!")
            print(f"   Erreur: {students_response.text}")
            
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")

if __name__ == "__main__":
    test_students() 