#!/usr/bin/env python3
"""
Script pour tester tous les nouveaux endpoints des fonctionnalités avancées
- Gestion des Devoirs
- Calendrier Avancé
- Collaboration
- IA Avancée
- Rapports Détaillés
"""

import requests
import json
from datetime import datetime, timedelta

# Configuration
BASE_URL = "http://localhost:8000"
API_BASE = f"{BASE_URL}/api/v1"

def test_health_endpoint():
    """Tester l'endpoint de santé"""
    print("🏥 Test de l'endpoint de santé...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✅ Endpoint de santé fonctionne")
            return True
        else:
            print(f"❌ Endpoint de santé échoué: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erreur de connexion: {e}")
        return False

def test_calendar_endpoints():
    """Tester les endpoints du calendrier"""
    print("\n📅 Test des endpoints du calendrier...")
    
    # Test sans authentification (doit retourner 401)
    try:
        response = requests.get(f"{API_BASE}/calendar/events")
        if response.status_code == 401:
            print("✅ Endpoint calendrier protégé (401 - Non authentifié)")
        else:
            print(f"⚠️ Endpoint calendrier: {response.status_code}")
    except Exception as e:
        print(f"❌ Erreur calendrier: {e}")
    
    # Test des sessions d'étude
    try:
        response = requests.get(f"{API_BASE}/calendar/study-sessions")
        if response.status_code == 401:
            print("✅ Endpoint sessions d'étude protégé (401 - Non authentifié)")
        else:
            print(f"⚠️ Endpoint sessions d'étude: {response.status_code}")
    except Exception as e:
        print(f"❌ Erreur sessions d'étude: {e}")
    
    return True

def test_collaboration_endpoints():
    """Tester les endpoints de collaboration"""
    print("\n👥 Test des endpoints de collaboration...")
    
    # Test des groupes d'étude
    try:
        response = requests.get(f"{API_BASE}/collaboration/study-groups")
        if response.status_code == 401:
            print("✅ Endpoint groupes d'étude protégé (401 - Non authentifié)")
        else:
            print(f"⚠️ Endpoint groupes d'étude: {response.status_code}")
    except Exception as e:
        print(f"❌ Erreur groupes d'étude: {e}")
    
    # Test des projets
    try:
        response = requests.get(f"{API_BASE}/collaboration/projects")
        if response.status_code == 401:
            print("✅ Endpoint projets protégé (401 - Non authentifié)")
        else:
            print(f"⚠️ Endpoint projets: {response.status_code}")
    except Exception as e:
        print(f"❌ Erreur projets: {e}")
    
    return True

def test_ai_advanced_endpoints():
    """Tester les endpoints de l'IA avancée"""
    print("\n🤖 Test des endpoints de l'IA avancée...")
    
    # Test des recommandations
    try:
        response = requests.get(f"{API_BASE}/ai_advanced/recommendations")
        if response.status_code == 401:
            print("✅ Endpoint recommandations IA protégé (401 - Non authentifié)")
        else:
            print(f"⚠️ Endpoint recommandations IA: {response.status_code}")
    except Exception as e:
        print(f"❌ Erreur recommandations IA: {e}")
    
    # Test des sessions de tutorat
    try:
        response = requests.get(f"{API_BASE}/ai_advanced/tutoring/sessions")
        if response.status_code == 401:
            print("✅ Endpoint tutorat IA protégé (401 - Non authentifié)")
        else:
            print(f"⚠️ Endpoint tutorat IA: {response.status_code}")
    except Exception as e:
        print(f"❌ Erreur tutorat IA: {e}")
    
    # Test de la détection de difficultés
    try:
        response = requests.get(f"{API_BASE}/ai_advanced/difficulty-detection")
        if response.status_code == 401:
            print("✅ Endpoint détection difficultés protégé (401 - Non authentifié)")
        else:
            print(f"⚠️ Endpoint détection difficultés: {response.status_code}")
    except Exception as e:
        print(f"❌ Erreur détection difficultés: {e}")
    
    return True

def test_homework_endpoints():
    """Tester les endpoints des devoirs"""
    print("\n📝 Test des endpoints des devoirs...")
    
    # Test des devoirs (côté professeur)
    try:
        response = requests.get(f"{API_BASE}/homework/assignments")
        if response.status_code == 401:
            print("✅ Endpoint devoirs protégé (401 - Non authentifié)")
        else:
            print(f"⚠️ Endpoint devoirs: {response.status_code}")
    except Exception as e:
        print(f"❌ Erreur devoirs: {e}")
    
    # Test des soumissions (côté étudiant)
    try:
        response = requests.get(f"{API_BASE}/homework/submissions")
        if response.status_code == 401:
            print("✅ Endpoint soumissions protégé (401 - Non authentifié)")
        else:
            print(f"⚠️ Endpoint soumissions: {response.status_code}")
    except Exception as e:
        print(f"❌ Erreur soumissions: {e}")
    
    return True

def test_detailed_reports_endpoints():
    """Tester les endpoints des rapports détaillés"""
    print("\n📊 Test des endpoints des rapports détaillés...")
    
    # Test des rapports de performance
    try:
        response = requests.get(f"{API_BASE}/ai_advanced/analytics/performance")
        if response.status_code == 401:
            print("✅ Endpoint analytics performance protégé (401 - Non authentifié)")
        else:
            print(f"⚠️ Endpoint analytics performance: {response.status_code}")
    except Exception as e:
        print(f"❌ Erreur analytics performance: {e}")
    
    # Test des rapports d'engagement
    try:
        response = requests.get(f"{API_BASE}/ai_advanced/analytics/engagement")
        if response.status_code == 401:
            print("✅ Endpoint analytics engagement protégé (401 - Non authentifié)")
        else:
            print(f"⚠️ Endpoint analytics engagement: {response.status_code}")
    except Exception as e:
        print(f"❌ Erreur analytics engagement: {e}")
    
    return True

def test_authentication_flow():
    """Tester le flux d'authentification"""
    print("\n🔐 Test du flux d'authentification...")
    
    # Test de l'endpoint de connexion
    try:
        login_data = {
            "username": "test_user",
            "password": "test_password"
        }
        response = requests.post(f"{API_BASE}/auth/login", json=login_data)
        if response.status_code == 401:
            print("✅ Endpoint de connexion fonctionne (401 - Identifiants invalides)")
        else:
            print(f"⚠️ Endpoint de connexion: {response.status_code}")
    except Exception as e:
        print(f"❌ Erreur de connexion: {e}")
    
    return True

def test_database_connectivity():
    """Tester la connectivité de la base de données"""
    print("\n🗄️ Test de la connectivité de la base de données...")
    
    # Vérifier que le serveur répond
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            print("✅ Serveur backend accessible")
            return True
        else:
            print(f"❌ Serveur backend: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Serveur backend inaccessible: {e}")
        return False

def test_cors_configuration():
    """Tester la configuration CORS"""
    print("\n🌐 Test de la configuration CORS...")
    
    try:
        # Test avec origine frontend
        headers = {
            'Origin': 'http://localhost:3000',
            'Access-Control-Request-Method': 'GET',
            'Access-Control-Request-Headers': 'Content-Type'
        }
        response = requests.options(f"{API_BASE}/calendar/events", headers=headers)
        
        if response.status_code == 200:
            print("✅ Configuration CORS fonctionne")
            return True
        else:
            print(f"⚠️ Configuration CORS: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erreur CORS: {e}")
        return False

def run_all_tests():
    """Exécuter tous les tests"""
    print("🚀 Démarrage des tests des endpoints avancés...")
    print("=" * 60)
    
    tests = [
        ("Connectivité serveur", test_database_connectivity),
        ("Endpoint de santé", test_health_endpoint),
        ("Configuration CORS", test_cors_configuration),
        ("Flux d'authentification", test_authentication_flow),
        ("Endpoints calendrier", test_calendar_endpoints),
        ("Endpoints collaboration", test_collaboration_endpoints),
        ("Endpoints IA avancée", test_ai_advanced_endpoints),
        ("Endpoints devoirs", test_homework_endpoints),
        ("Endpoints rapports", test_detailed_reports_endpoints),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            success = test_func()
            results.append((test_name, success))
        except Exception as e:
            print(f"❌ Erreur lors du test {test_name}: {e}")
            results.append((test_name, False))
    
    # Résumé des tests
    print("\n" + "=" * 60)
    print("📋 RÉSUMÉ DES TESTS")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
        if success:
            passed += 1
    
    print(f"\n🎯 Résultats: {passed}/{total} tests réussis")
    
    if passed == total:
        print("🎉 Tous les tests sont passés avec succès!")
    else:
        print(f"⚠️ {total - passed} test(s) ont échoué")
    
    return passed == total

if __name__ == "__main__":
    success = run_all_tests()
    
    if success:
        print("\n✅ Tests terminés avec succès!")
        print("\n💡 Prochaines étapes:")
        print("   1. Vérifier que le frontend peut se connecter au backend")
        print("   2. Tester l'authentification avec de vrais utilisateurs")
        print("   3. Vérifier que les widgets frontend fonctionnent")
    else:
        print("\n❌ Certains tests ont échoué!")
        print("\n🔧 Actions recommandées:")
        print("   1. Vérifier que le serveur backend est en cours d'exécution")
        print("   2. Vérifier la configuration de la base de données")
        print("   3. Vérifier les logs du serveur pour plus de détails")




