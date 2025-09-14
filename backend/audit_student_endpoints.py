#!/usr/bin/env python3
"""
Script d'audit complet des endpoints étudiants
"""

import requests
import json
from datetime import datetime

def audit_student_endpoints():
    """Auditer tous les endpoints étudiants"""
    print("🔍 AUDIT COMPLET DES ENDPOINTS ÉTUDIANTS")
    print("=" * 80)
    
    base_url = "http://localhost:8000"
    
    # Étape 1: Connexion pour obtenir un token
    print("\n1️⃣ CONNEXION ET AUTHENTIFICATION")
    print("-" * 50)
    
    login_data = {
        "email": "salmane.hajouji@najah.ai",
        "password": "password123"
    }
    
    try:
        login_response = requests.post(f"{base_url}/api/v1/auth/login", json=login_data)
        if login_response.status_code == 200:
            auth_data = login_response.json()
            token = auth_data.get('access_token')
            user_id = auth_data.get('id')
            print(f"   ✅ Connexion réussie: User ID {user_id}")
            print(f"   🔑 Token: {token[:30]}...")
        else:
            print(f"   ❌ Échec de la connexion: {login_response.status_code}")
            return
    except Exception as e:
        print(f"   ❌ Erreur de connexion: {e}")
        return
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Étape 2: Audit des endpoints d'évaluation
    print("\n2️⃣ ENDPOINTS D'ÉVALUATION")
    print("-" * 50)
    
    assessment_endpoints = [
        f"/api/v1/assessments/student/{user_id}",
        f"/api/v1/assessments/student/{user_id}/pending",
        f"/api/v1/assessments/student/{user_id}/completed",
        f"/api/v1/assessments/{user_id}/questions",
        f"/api/v1/assessments/{user_id}/start",
        f"/api/v1/assessments/{user_id}/submit",
        f"/api/v1/assessments/{user_id}/results"
    ]
    
    for endpoint in assessment_endpoints:
        try:
            response = requests.get(f"{base_url}{endpoint}", headers=headers)
            status = response.status_code
            if status == 200:
                data = response.json()
                print(f"   ✅ {endpoint}: {status} - Données reçues")
                if isinstance(data, dict) and 'assessments' in data:
                    print(f"      📊 {len(data.get('assessments', []))} évaluations")
            elif status == 404:
                print(f"   ❌ {endpoint}: {status} - Endpoint non trouvé")
            elif status == 403:
                print(f"   ⚠️ {endpoint}: {status} - Accès interdit")
            else:
                print(f"   ⚠️ {endpoint}: {status} - {response.text[:100]}")
        except Exception as e:
            print(f"   ❌ {endpoint}: Erreur - {e}")
    
    # Étape 3: Audit des endpoints de parcours d'apprentissage
    print("\n3️⃣ ENDPOINTS PARCOURS D'APPRENTISSAGE")
    print("-" * 50)
    
    learning_path_endpoints = [
        f"/api/v1/learning_paths/student/{user_id}",
        f"/api/v1/learning_paths/student/{user_id}/active",
        f"/api/v1/learning_paths/student/{user_id}/completed",
        f"/api/v1/learning_paths/{user_id}/steps",
        f"/api/v1/learning_paths/{user_id}/progress",
        f"/api/v1/learning_paths/{user_id}/start",
        f"/api/v1/learning_paths/{user_id}/complete-step"
    ]
    
    for endpoint in learning_path_endpoints:
        try:
            response = requests.get(f"{base_url}{endpoint}", headers=headers)
            status = response.status_code
            if status == 200:
                data = response.json()
                print(f"   ✅ {endpoint}: {status} - Données reçues")
                if isinstance(data, dict) and 'learning_paths' in data:
                    print(f"      🛤️ {len(data.get('learning_paths', []))} parcours")
            elif status == 404:
                print(f"   ❌ {endpoint}: {status} - Endpoint non trouvé")
            elif status == 403:
                print(f"   ⚠️ {endpoint}: {status} - Accès interdit")
            else:
                print(f"   ⚠️ {endpoint}: {status} - {response.text[:100]}")
        except Exception as e:
            print(f"   ❌ {endpoint}: Erreur - {e}")
    
    # Étape 4: Audit des endpoints de quiz et devoirs
    print("\n4️⃣ ENDPOINTS QUIZ ET DEVOIRS")
    print("-" * 50)
    
    quiz_homework_endpoints = [
        f"/api/v1/quizzes/assigned/{user_id}",
        f"/api/v1/quizzes/{user_id}/start",
        f"/api/v1/quizzes/{user_id}/submit",
        f"/api/v1/homework/assigned/{user_id}",
        f"/api/v1/homework/{user_id}/submit",
        f"/api/v1/homework/{user_id}/status"
    ]
    
    for endpoint in quiz_homework_endpoints:
        try:
            response = requests.get(f"{base_url}{endpoint}", headers=headers)
            status = response.status_code
            if status == 200:
                data = response.json()
                print(f"   ✅ {endpoint}: {status} - Données reçues")
                if isinstance(data, dict):
                    if 'quizzes' in data:
                        print(f"      📚 {len(data.get('quizzes', []))} quiz")
                    elif 'homework' in data:
                        print(f"      📝 {len(data.get('homework', []))} devoirs")
            elif status == 404:
                print(f"   ❌ {endpoint}: {status} - Endpoint non trouvé")
            elif status == 403:
                print(f"   ⚠️ {endpoint}: {status} - Accès interdit")
            else:
                print(f"   ⚠️ {endpoint}: {status} - {response.text[:100]}")
        except Exception as e:
            print(f"   ❌ {endpoint}: Erreur - {e}")
    
    # Étape 5: Audit des endpoints d'analytics et progression
    print("\n5️⃣ ENDPOINTS ANALYTICS ET PROGRESSION")
    print("-" * 50)
    
    analytics_endpoints = [
        f"/api/v1/analytics/student/{user_id}/progress",
        f"/api/v1/analytics/student/{user_id}/performance",
        f"/api/v1/analytics/student/{user_id}/subjects",
        f"/api/v1/analytics/student/{user_id}/reports",
        f"/api/v1/analytics/interactive-charts/{user_id}"
    ]
    
    for endpoint in analytics_endpoints:
        try:
            response = requests.get(f"{base_url}{endpoint}", headers=headers)
            status = response.status_code
            if status == 200:
                data = response.json()
                print(f"   ✅ {endpoint}: {status} - Données reçues")
                if isinstance(data, dict):
                    print(f"      📊 Données analytics disponibles")
            elif status == 404:
                print(f"   ❌ {endpoint}: {status} - Endpoint non trouvé")
            elif status == 403:
                print(f"   ⚠️ {endpoint}: {status} - Accès interdit")
            else:
                print(f"   ⚠️ {endpoint}: {status} - {response.text[:100]}")
        except Exception as e:
            print(f"   ❌ {endpoint}: Erreur - {e}")
    
    # Étape 6: Audit des endpoints de calendrier et planning
    print("\n6️⃣ ENDPOINTS CALENDRIER ET PLANNING")
    print("-" * 50)
    
    calendar_endpoints = [
        "/api/v1/calendar/events",
        f"/api/v1/calendar/student/{user_id}/schedule",
        f"/api/v1/calendar/student/{user_id}/deadlines",
        f"/api/v1/calendar/student/{user_id}/study-sessions"
    ]
    
    for endpoint in calendar_endpoints:
        try:
            response = requests.get(f"{base_url}{endpoint}", headers=headers)
            status = response.status_code
            if status == 200:
                data = response.json()
                print(f"   ✅ {endpoint}: {status} - Données reçues")
                if isinstance(data, list):
                    print(f"      📅 {len(data)} événements")
                elif isinstance(data, dict) and 'events' in data:
                    print(f"      📅 {len(data.get('events', []))} événements")
            elif status == 404:
                print(f"   ❌ {endpoint}: {status} - Endpoint non trouvé")
            elif status == 403:
                print(f"   ⚠️ {endpoint}: {status} - Accès interdit")
            else:
                print(f"   ⚠️ {endpoint}: {status} - {response.text[:100]}")
        except Exception as e:
            print(f"   ❌ {endpoint}: Erreur - {e}")
    
    print("\n" + "=" * 80)
    print("🎯 RÉSUMÉ DE L'AUDIT")
    print("✅ 200 = Endpoint fonctionnel avec données")
    print("❌ 404 = Endpoint manquant à implémenter")
    print("⚠️ 403 = Problème d'autorisation")
    print("❌ Erreur = Problème de connexion")

if __name__ == "__main__":
    print("🚀 Démarrage de l'audit des endpoints étudiants...")
    print("Assurez-vous que votre serveur backend est démarré sur http://localhost:8000")
    print("Appuyez sur Entrée pour continuer...")
    input()
    audit_student_endpoints()







