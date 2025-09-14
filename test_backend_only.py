#!/usr/bin/env python3
"""
Script de test des endpoints backend uniquement
"""

import requests
import json
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:8000"

def test_backend_health():
    """Test de santé du backend"""
    print("🔍 Test de santé du backend...")
    try:
        response = requests.get(f"{BASE_URL}/", timeout=5)
        if response.status_code == 200:
            print("✅ Backend accessible")
            return True
        else:
            print(f"❌ Backend inaccessible: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Backend non accessible")
        return False
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def test_authentication():
    """Test d'authentification"""
    print("🔍 Test d'authentification...")
    
    login_data = {
        "username": "student1",
        "password": "password123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/v1/auth/login", json=login_data, timeout=5)
        if response.status_code == 200:
            data = response.json()
            token = data.get("access_token")
            if token:
                print("✅ Authentification réussie")
                return token
            else:
                print("❌ Token non trouvé dans la réponse")
                return None
        else:
            print(f"❌ Échec de l'authentification: {response.status_code}")
            print(f"Réponse: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Erreur d'authentification: {e}")
        return None

def test_core_endpoints(token):
    """Test des endpoints principaux"""
    print("🔍 Test des endpoints principaux...")
    
    headers = {"Authorization": f"Bearer {token}"}
    user_id = 1
    
    core_endpoints = [
        # Users
        "/api/v1/users/",
        
        # Quizzes
        "/api/v1/quizzes/",
        
        # Quiz Results
        f"/api/v1/quiz_results/user/{user_id}",
        
        # Gamification
        f"/api/v1/gamification/user/{user_id}/level",
        f"/api/v1/gamification/user/{user_id}/points",
        f"/api/v1/gamification/user/{user_id}/achievements",
        f"/api/v1/gamification/user/{user_id}/challenges",
        
        # Activity
        f"/api/v1/activity/user/{user_id}/recent",
        f"/api/v1/activity/user/{user_id}/stats",
        
        # Settings
        f"/api/v1/settings/user/{user_id}",
        
        # Score Corrections
        f"/api/v1/score_corrections/user/{user_id}/corrections",
        f"/api/v1/score_corrections/user/{user_id}/corrections/stats",
        
        # Messages
        f"/api/v1/messages/user/{user_id}/conversations",
        
        # Contents
        "/api/v1/contents/",
        
        # Learning Paths
        f"/api/v1/learning_paths/user/{user_id}/paths",
    ]
    
    successful_endpoints = 0
    total_endpoints = len(core_endpoints)
    
    for endpoint in core_endpoints:
        try:
            response = requests.get(f"{BASE_URL}{endpoint}", headers=headers, timeout=5)
            if response.status_code == 200:
                print(f"✅ {endpoint}")
                successful_endpoints += 1
            else:
                print(f"❌ {endpoint} - {response.status_code}")
        except Exception as e:
            print(f"❌ {endpoint} - Erreur: {e}")
    
    print(f"\n📊 Résultats: {successful_endpoints}/{total_endpoints} endpoints fonctionnels")
    return successful_endpoints, total_endpoints

def test_database_data():
    """Test des données de la base de données"""
    print("🔍 Test des données de la base de données...")
    
    try:
        response = requests.get(f"{BASE_URL}/api/v1/users/", timeout=5)
        if response.status_code == 200:
            users = response.json()
            print(f"✅ {len(users)} utilisateurs trouvés")
            
            students = [u for u in users if u.get("role") == "student"]
            teachers = [u for u in users if u.get("role") == "teacher"]
            print(f"   - {len(students)} étudiants")
            print(f"   - {len(teachers)} enseignants")
            
            return True
        else:
            print(f"❌ Impossible d'accéder aux utilisateurs: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erreur d'accès à la base de données: {e}")
        return False

def generate_report(backend_health, token, api_results, db_data):
    """Générer un rapport"""
    print("\n" + "="*50)
    print("📋 RAPPORT DE TEST BACKEND")
    print("="*50)
    
    print(f"🕐 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🌐 Backend: {'✅ Opérationnel' if backend_health else '❌ Problème'}")
    print(f"🔐 Authentification: {'✅ Fonctionnelle' if token else '❌ Échec'}")
    
    if api_results:
        api_success, api_total = api_results
        api_percentage = (api_success / api_total) * 100
        print(f"🔌 API Endpoints: {api_success}/{api_total} ({api_percentage:.1f}%)")
    
    print(f"💾 Base de données: {'✅ Accessible' if db_data else '❌ Problème'}")
    
    # Évaluation
    total_tests = 0
    passed_tests = 0
    
    if backend_health: passed_tests += 1; total_tests += 1
    if token: passed_tests += 1; total_tests += 1
    if db_data: passed_tests += 1; total_tests += 1
    
    if api_results:
        api_success, api_total = api_results
        if api_success > api_total * 0.7:  # 70% de réussite
            passed_tests += 1
        total_tests += 1
    
    success_rate = (passed_tests / total_tests) * 100 if total_tests > 0 else 0
    
    print(f"\n🎯 ÉVALUATION: {success_rate:.1f}%")
    
    if success_rate >= 90:
        print("🏆 EXCELLENT - Backend entièrement fonctionnel")
    elif success_rate >= 75:
        print("✅ BON - Backend fonctionnel")
    elif success_rate >= 50:
        print("⚠️ MOYEN - Backend partiellement fonctionnel")
    else:
        print("❌ CRITIQUE - Problèmes majeurs détectés")
    
    print("="*50)

def main():
    """Fonction principale"""
    print("🚀 Test des endpoints backend...")
    print("="*50)
    
    # Test de santé
    backend_health = test_backend_health()
    
    if not backend_health:
        print("❌ Impossible de continuer sans backend")
        return
    
    # Test d'authentification
    token = test_authentication()
    
    # Test des endpoints API
    api_results = None
    if token:
        api_results = test_core_endpoints(token)
    
    # Test de la base de données
    db_data = test_database_data()
    
    # Génération du rapport
    generate_report(backend_health, token, api_results, db_data)

if __name__ == "__main__":
    main() 