#!/usr/bin/env python3
"""
Script de test pour vérifier l'intégration des nouveaux services
Teste tous les endpoints et services avancés
"""

import requests
import json
import time
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:8000"
API_BASE = f"{BASE_URL}/api/v1"

def test_health_endpoint():
    """Tester l'endpoint de santé"""
    print("🏥 Test de l'endpoint de santé...")
    
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Santé: {data.get('status', 'unknown')}")
            print(f"   Version: {data.get('version', 'unknown')}")
            print(f"   Services: {len(data.get('services', {}))}")
            return True
        else:
            print(f"❌ Erreur HTTP: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erreur de connexion: {e}")
        return False

def test_advanced_services_health():
    """Tester la santé des services avancés"""
    print("\n🧠 Test de la santé des services avancés...")
    
    try:
        response = requests.get(f"{API_BASE}/advanced/health/advanced-services")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Services avancés: {data.get('status', 'unknown')}")
            
            services = data.get('services_health', {})
            for service, status in services.items():
                status_icon = "✅" if "active" in str(status) else "❌"
                print(f"   {status_icon} {service}: {status}")
            
            return True
        else:
            print(f"❌ Erreur HTTP: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erreur de connexion: {e}")
        return False

def test_cognitive_analysis():
    """Tester l'analyse cognitive"""
    print("\n🧠 Test de l'analyse cognitive...")
    
    # Données de test
    test_responses = [
        {
            "question_id": 1,
            "student_id": 1,
            "response_time": 45,
            "is_correct": True,
            "answer_text": "42",
            "question_difficulty": 5
        },
        {
            "question_id": 2,
            "student_id": 1,
            "response_time": 120,
            "is_correct": False,
            "answer_text": "dormir",
            "question_difficulty": 6
        }
    ]
    
    try:
        # Test d'analyse de réponse individuelle
        print("   📝 Test d'analyse de réponse...")
        response = requests.post(
            f"{API_BASE}/advanced/cognitive/analyze-response",
            json=test_responses[0]
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Analyse de réponse: {data.get('status', 'unknown')}")
            print(f"      Pattern détecté: {data.get('analysis', {}).get('pattern', 'unknown')}")
        else:
            print(f"   ❌ Erreur HTTP: {response.status_code}")
            return False
        
        # Test de génération de profil cognitif
        print("   👤 Test de génération de profil...")
        response = requests.post(
            f"{API_BASE}/advanced/cognitive/generate-profile",
            json={"student_responses": test_responses}
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Profil cognitif: {data.get('status', 'unknown')}")
            profile = data.get('cognitive_profile', {})
            print(f"      Style d'apprentissage: {profile.get('learning_style', 'unknown')}")
        else:
            print(f"   ❌ Erreur HTTP: {response.status_code}")
            return False
        
        return True
        
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        return False

def test_irt_engine():
    """Tester le moteur IRT"""
    print("\n📈 Test du moteur IRT...")
    
    try:
        # Test d'estimation de capacité
        print("   🎯 Test d'estimation de capacité...")
        response = requests.post(
            f"{API_BASE}/advanced/irt/estimate-ability",
            json={
                "student_id": 1,
                "responses": [
                    {"question_id": 1, "is_correct": True, "difficulty": 5},
                    {"question_id": 2, "is_correct": False, "difficulty": 6}
                ]
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Estimation IRT: {data.get('status', 'unknown')}")
            print(f"      Capacité estimée: {data.get('estimated_ability', 'unknown')}")
        else:
            print(f"   ❌ Erreur HTTP: {response.status_code}")
            return False
        
        # Test d'adaptation de difficulté
        print("   🔄 Test d'adaptation de difficulté...")
        response = requests.post(
            f"{API_BASE}/advanced/irt/adapt-difficulty",
            json={
                "student_id": 1,
                "current_performance": 0.7,
                "current_difficulty": 5
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Adaptation IRT: {data.get('status', 'unknown')}")
            print(f"      Difficulté adaptée: {data.get('adapted_difficulty', 'unknown')}")
        else:
            print(f"   ❌ Erreur HTTP: {response.status_code}")
            return False
        
        return True
        
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        return False

def test_extended_question_bank():
    """Tester la banque de questions étendue"""
    print("\n🗃️ Test de la banque de questions étendue...")
    
    try:
        # Test de récupération de questions
        print("   📚 Test de récupération de questions...")
        response = requests.get(f"{API_BASE}/advanced/questions/extended?subject=math&limit=5")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Questions récupérées: {data.get('status', 'unknown')}")
            print(f"      Nombre de questions: {data.get('total_count', 0)}")
            
            if data.get('questions'):
                first_question = data['questions'][0]
                print(f"      Première question: {first_question.get('question_text', 'N/A')[:50]}...")
        else:
            print(f"   ❌ Erreur HTTP: {response.status_code}")
            return False
        
        # Test des métadonnées
        print("   📊 Test des métadonnées...")
        response = requests.get(f"{API_BASE}/advanced/questions/metadata")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Métadonnées: {data.get('status', 'unknown')}")
            
            metadata = data.get('metadata', {})
            if metadata.get('subject_statistics'):
                print(f"      Sujets disponibles: {len(metadata['subject_statistics'])}")
        else:
            print(f"   ❌ Erreur HTTP: {response.status_code}")
            return False
        
        return True
        
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        return False

def test_advanced_dashboard():
    """Tester le dashboard avancé"""
    print("\n📊 Test du dashboard avancé...")
    
    try:
        # Test de vue d'ensemble de classe
        print("   👥 Test de vue d'ensemble de classe...")
        response = requests.get(f"{API_BASE}/advanced/dashboard/class-overview?class_id=1")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Vue d'ensemble: {data.get('status', 'unknown')}")
            
            overview = data.get('class_overview', {})
            print(f"      Classe: {overview.get('class_name', 'N/A')}")
            print(f"      Étudiants: {overview.get('total_students', 0)}")
        else:
            print(f"   ❌ Erreur HTTP: {response.status_code}")
            return False
        
        return True
        
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        return False

def test_real_time_analytics():
    """Tester les analytics en temps réel"""
    print("\n🔄 Test des analytics en temps réel...")
    
    try:
        # Test de l'endpoint d'overview
        print("   📈 Test de l'overview analytics...")
        response = requests.get(f"{API_BASE}/analytics/overview")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Analytics temps réel: {data.get('status', 'unknown')}")
            
            if 'data' in data:
                print(f"      Données récupérées: {len(data['data'])} éléments")
        else:
            print(f"   ❌ Erreur HTTP: {response.status_code}")
            return False
        
        return True
        
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        return False

def run_all_tests():
    """Exécuter tous les tests"""
    print("🚀 Démarrage des tests d'intégration...")
    print("=" * 60)
    
    tests = [
        ("Santé générale", test_health_endpoint),
        ("Santé des services avancés", test_advanced_services_health),
        ("Analyse cognitive", test_cognitive_analysis),
        ("Moteur IRT", test_irt_engine),
        ("Banque de questions étendue", test_extended_question_bank),
        ("Dashboard avancé", test_advanced_dashboard),
        ("Analytics temps réel", test_real_time_analytics)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n🔍 {test_name}")
        print("-" * 40)
        
        start_time = time.time()
        try:
            success = test_func()
            duration = time.time() - start_time
            results.append((test_name, success, duration))
        except Exception as e:
            print(f"❌ Erreur lors du test: {e}")
            results.append((test_name, False, 0))
    
    # Résumé des tests
    print("\n" + "=" * 60)
    print("📊 RÉSUMÉ DES TESTS")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, success, duration in results:
        status_icon = "✅" if success else "❌"
        status_text = "PASSÉ" if success else "ÉCHOUÉ"
        duration_text = f"{duration:.2f}s" if duration > 0 else "N/A"
        
        print(f"{status_icon} {test_name}: {status_text} ({duration_text})")
        
        if success:
            passed += 1
    
    print(f"\n🎯 Résultat: {passed}/{total} tests passés")
    
    if passed == total:
        print("🎉 Tous les tests sont passés avec succès!")
        print("✅ Votre système est prêt à être utilisé!")
    else:
        print("⚠️ Certains tests ont échoué.")
        print("🔧 Vérifiez la configuration et redémarrez le serveur si nécessaire.")
    
    return passed == total

if __name__ == "__main__":
    print("🧪 Tests d'intégration - Najah AI Backend")
    print("=" * 60)
    
    try:
        success = run_all_tests()
        exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n⏹️ Tests interrompus par l'utilisateur")
        exit(1)
    except Exception as e:
        print(f"\n💥 Erreur fatale: {e}")
        exit(1)















