#!/usr/bin/env python3
"""
Script de test d'intégration complète pour Najah AI
Teste tous les endpoints backend et vérifie la connectivité avec le frontend
"""

import requests
import json
import time
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:8000"
FRONTEND_URL = "http://localhost:3001"

def test_backend_health():
    """Test de santé du backend"""
    print("🔍 Test de santé du backend...")
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            print("✅ Backend accessible")
            return True
        else:
            print(f"❌ Backend inaccessible: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Backend non accessible")
        return False

def test_frontend_health():
    """Test de santé du frontend"""
    print("🔍 Test de santé du frontend...")
    try:
        response = requests.get(FRONTEND_URL)
        if response.status_code == 200:
            print("✅ Frontend accessible")
            return True
        else:
            print(f"❌ Frontend inaccessible: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Frontend non accessible")
        return False

def test_authentication():
    """Test d'authentification"""
    print("🔍 Test d'authentification...")
    
    # Test de connexion
    login_data = {
        "username": "student1",
        "password": "password123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/v1/auth/login", json=login_data)
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
            return None
    except Exception as e:
        print(f"❌ Erreur d'authentification: {e}")
        return None

def test_api_endpoints(token):
    """Test des endpoints API"""
    print("🔍 Test des endpoints API...")
    
    headers = {"Authorization": f"Bearer {token}"}
    user_id = 1  # ID de l'étudiant de test
    
    endpoints_to_test = [
        # Dashboard
        f"/api/v1/student_performance/user/{user_id}/overview",
        f"/api/v1/student_performance/user/{user_id}/progress",
        f"/api/v1/student_performance/user/{user_id}/analytics",
        
        # Gamification
        f"/api/v1/gamification/user/{user_id}/level",
        f"/api/v1/gamification/user/{user_id}/points",
        f"/api/v1/gamification/user/{user_id}/achievements",
        f"/api/v1/gamification/user/{user_id}/challenges",
        f"/api/v1/gamification/leaderboard",
        
        # Activity
        f"/api/v1/activity/user/{user_id}/recent",
        f"/api/v1/activity/user/{user_id}/stats",
        f"/api/v1/activity/user/{user_id}/timeline",
        f"/api/v1/activity/user/{user_id}/achievements",
        
        # Settings
        f"/api/v1/settings/user/{user_id}",
        f"/api/v1/settings/user/{user_id}/privacy",
        f"/api/v1/settings/user/{user_id}/notifications",
        f"/api/v1/settings/user/{user_id}/goals",
        
        # Score Corrections
        f"/api/v1/score_corrections/user/{user_id}/corrections",
        f"/api/v1/score_corrections/user/{user_id}/corrections/stats",
        
        # Quizzes
        "/api/v1/quizzes/",
        f"/api/v1/quiz_results/user/{user_id}",
        
        # Messages
        f"/api/v1/messages/user/{user_id}/conversations",
        
        # Learning Paths
        f"/api/v1/learning_paths/user/{user_id}/paths",
        
        # Contents
        "/api/v1/contents/",
        
        # Analytics
        f"/api/v1/analytics/user/{user_id}/overview",
        f"/api/v1/advanced_analytics/user/{user_id}/performance",
    ]
    
    successful_endpoints = 0
    total_endpoints = len(endpoints_to_test)
    
    for endpoint in endpoints_to_test:
        try:
            response = requests.get(f"{BASE_URL}{endpoint}", headers=headers)
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
    
    # Test de connexion à la base de données
    try:
        response = requests.get(f"{BASE_URL}/api/v1/users/")
        if response.status_code == 200:
            users = response.json()
            print(f"✅ {len(users)} utilisateurs trouvés")
            
            # Vérifier les types d'utilisateurs
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

def test_frontend_integration():
    """Test d'intégration avec le frontend"""
    print("🔍 Test d'intégration avec le frontend...")
    
    # Test des pages principales
    pages_to_test = [
        "/",
        "/login",
        "/register",
        "/dashboard/student",
        "/dashboard/teacher"
    ]
    
    successful_pages = 0
    total_pages = len(pages_to_test)
    
    for page in pages_to_test:
        try:
            response = requests.get(f"{FRONTEND_URL}{page}")
            if response.status_code == 200:
                print(f"✅ Page {page}")
                successful_pages += 1
            else:
                print(f"❌ Page {page} - {response.status_code}")
        except Exception as e:
            print(f"❌ Page {page} - Erreur: {e}")
    
    print(f"\n📊 Résultats: {successful_pages}/{total_pages} pages accessibles")
    return successful_pages, total_pages

def generate_report(backend_health, frontend_health, token, api_results, db_data, frontend_results):
    """Générer un rapport complet"""
    print("\n" + "="*60)
    print("📋 RAPPORT D'INTÉGRATION COMPLÈTE")
    print("="*60)
    
    print(f"🕐 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🌐 Backend: {'✅ Opérationnel' if backend_health else '❌ Problème'}")
    print(f"🎨 Frontend: {'✅ Opérationnel' if frontend_health else '❌ Problème'}")
    print(f"🔐 Authentification: {'✅ Fonctionnelle' if token else '❌ Échec'}")
    
    if api_results:
        api_success, api_total = api_results
        api_percentage = (api_success / api_total) * 100
        print(f"🔌 API Endpoints: {api_success}/{api_total} ({api_percentage:.1f}%)")
    
    print(f"💾 Base de données: {'✅ Accessible' if db_data else '❌ Problème'}")
    
    if frontend_results:
        frontend_success, frontend_total = frontend_results
        frontend_percentage = (frontend_success / frontend_total) * 100
        print(f"📱 Pages Frontend: {frontend_success}/{frontend_total} ({frontend_percentage:.1f}%)")
    
    # Évaluation globale
    total_tests = 0
    passed_tests = 0
    
    if backend_health: passed_tests += 1; total_tests += 1
    if frontend_health: passed_tests += 1; total_tests += 1
    if token: passed_tests += 1; total_tests += 1
    if db_data: passed_tests += 1; total_tests += 1
    
    if api_results:
        api_success, api_total = api_results
        if api_success > api_total * 0.8:  # 80% de réussite
            passed_tests += 1
        total_tests += 1
    
    if frontend_results:
        frontend_success, frontend_total = frontend_results
        if frontend_success > frontend_total * 0.8:  # 80% de réussite
            passed_tests += 1
        total_tests += 1
    
    success_rate = (passed_tests / total_tests) * 100 if total_tests > 0 else 0
    
    print(f"\n🎯 ÉVALUATION GLOBALE: {success_rate:.1f}%")
    
    if success_rate >= 90:
        print("🏆 EXCELLENT - Système entièrement fonctionnel")
    elif success_rate >= 75:
        print("✅ BON - Système fonctionnel avec quelques améliorations mineures")
    elif success_rate >= 50:
        print("⚠️ MOYEN - Système partiellement fonctionnel, améliorations nécessaires")
    else:
        print("❌ CRITIQUE - Problèmes majeurs détectés")
    
    print("="*60)

def main():
    """Fonction principale de test"""
    print("🚀 Démarrage des tests d'intégration complète...")
    print("="*60)
    
    # Tests de santé
    backend_health = test_backend_health()
    frontend_health = test_frontend_health()
    
    if not backend_health:
        print("❌ Impossible de continuer sans backend")
        return
    
    # Test d'authentification
    token = test_authentication()
    
    # Test des endpoints API
    api_results = None
    if token:
        api_results = test_api_endpoints(token)
    
    # Test de la base de données
    db_data = test_database_data()
    
    # Test d'intégration frontend
    frontend_results = None
    if frontend_health:
        frontend_results = test_frontend_integration()
    
    # Génération du rapport
    generate_report(backend_health, frontend_health, token, api_results, db_data, frontend_results)

if __name__ == "__main__":
    main() 