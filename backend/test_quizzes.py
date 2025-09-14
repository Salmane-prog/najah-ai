#!/usr/bin/env python3
"""
Script pour tester l'endpoint quizzes
"""

import requests
import json

def test_quizzes():
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
        
        # Maintenant tester l'endpoint quizzes
        quizzes_url = "http://localhost:8000/api/v1/quizzes/"
        headers = {"Authorization": f"Bearer {token}"}
        
        print("\n📝 Test de l'endpoint quizzes...")
        quizzes_response = requests.get(quizzes_url, headers=headers)
        
        print(f"📊 Status Code: {quizzes_response.status_code}")
        print(f"📊 Headers: {dict(quizzes_response.headers)}")
        
        if quizzes_response.status_code == 200:
            quizzes_data = quizzes_response.json()
            print(f"✅ Quizzes récupérés!")
            print(f"   Nombre de quizzes: {len(quizzes_data)}")
            if quizzes_data:
                print(f"   Premier quiz: {quizzes_data[0]}")
        else:
            print(f"❌ Erreur quizzes!")
            print(f"   Erreur: {quizzes_response.text}")
            
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")

if __name__ == "__main__":
    test_quizzes() 