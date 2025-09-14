#!/usr/bin/env python3
"""
Script pour tester les endpoints des quiz
"""

import requests
import json

def test_quiz_endpoints():
    """Tester les endpoints des quiz"""
    
    base_url = "http://localhost:8000"
    
    print("🧪 Test des endpoints des quiz...")
    
    # 1. Test de connexion
    try:
        response = requests.get(f"{base_url}/docs")
        print("✅ Serveur accessible")
    except Exception as e:
        print(f"❌ Serveur non accessible: {e}")
        return
    
    # 2. Test de login pour obtenir un token
    login_data = {
        "email": "salmane.hajouji@najah.ai",
        "password": "password123"
    }
    
    try:
        response = requests.post(f"{base_url}/api/v1/auth/login", json=login_data)
        if response.status_code == 200:
            token_data = response.json()
            token = token_data.get("access_token")
            print("✅ Login réussi")
            print(f"Token: {token[:20]}...")
        else:
            print(f"❌ Login échoué: {response.status_code}")
            print(response.text)
            return
    except Exception as e:
        print(f"❌ Erreur lors du login: {e}")
        return
    
    # 3. Test de l'endpoint des quiz
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(f"{base_url}/api/v1/quizzes/", headers=headers)
        print(f"\n📊 Test GET /api/v1/quizzes/")
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            quizzes = response.json()
            print(f"✅ Nombre de quiz récupérés: {len(quizzes)}")
            
            if quizzes:
                print("\n📋 Détails des quiz:")
                for quiz in quizzes[:3]:  # Afficher les 3 premiers
                    print(f"  - ID: {quiz.get('id')}")
                    print(f"    Titre: {quiz.get('title')}")
                    print(f"    Matière: {quiz.get('subject')}")
                    print(f"    Difficulté: {quiz.get('difficulty')}")
                    print(f"    Points max: {quiz.get('max_score')}")
                    print(f"    Actif: {quiz.get('is_active')}")
                    print()
            else:
                print("⚠️ Aucun quiz trouvé")
        else:
            print(f"❌ Erreur: {response.text}")
            
    except Exception as e:
        print(f"❌ Erreur lors du test des quiz: {e}")
    
    # 4. Test avec un étudiant
    print("\n👨‍🎓 Test avec un étudiant...")
    student_login = {
        "email": "marie.dupont@student.com", 
        "password": "password123"
    }
    
    try:
        response = requests.post(f"{base_url}/api/v1/auth/login", json=student_login)
        if response.status_code == 200:
            student_token = response.json().get("access_token")
            headers["Authorization"] = f"Bearer {student_token}"
            
            response = requests.get(f"{base_url}/api/v1/quizzes/", headers=headers)
            print(f"Status étudiant: {response.status_code}")
            
            if response.status_code == 200:
                student_quizzes = response.json()
                print(f"Quiz pour étudiant: {len(student_quizzes)}")
            else:
                print(f"Erreur étudiant: {response.text}")
        else:
            print("❌ Login étudiant échoué")
            
    except Exception as e:
        print(f"❌ Erreur test étudiant: {e}")

if __name__ == "__main__":
    test_quiz_endpoints() 