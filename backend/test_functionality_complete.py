#!/usr/bin/env python3
"""
Script de test complet pour vérifier la fonctionnalité de l'évaluation initiale 
et des parcours d'apprentissage selon le cahier des charges.
"""

import sys
import os
import requests
import json
import time
from datetime import datetime

# Ajouter le répertoire parent au path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_backend_connection():
    """Tester la connexion au backend"""
    print("🔌 Test de connexion au backend...")
    
    try:
        response = requests.get("http://localhost:8000/docs", timeout=5)
        if response.status_code == 200:
            print("✅ Backend accessible sur http://localhost:8000")
            return True
        else:
            print(f"❌ Backend accessible mais erreur {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Backend non accessible sur http://localhost:8000")
        print("   Démarrez le serveur avec: python app.py")
        return False
    except Exception as e:
        print(f"❌ Erreur de connexion: {e}")
        return False

def test_authentication():
    """Tester l'authentification"""
    print("\n🔐 Test de l'authentification...")
    
    try:
        # Test de connexion avec un compte étudiant
        login_data = {
            "username": "student1@example.com",
            "password": "studentpass"
        }
        
        response = requests.post(
            "http://localhost:8000/api/v1/auth/login",
            data=login_data,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            token = data.get("access_token")
            if token:
                print("✅ Authentification réussie")
                print(f"   Token obtenu: {token[:20]}...")
                return token
            else:
                print("❌ Token non reçu dans la réponse")
                return None
        else:
            print(f"❌ Échec de l'authentification: {response.status_code}")
            print(f"   Réponse: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Erreur lors de l'authentification: {e}")
        return None

def test_initial_assessment(token):
    """Tester l'évaluation initiale"""
    print("\n🎯 Test de l'évaluation initiale...")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        # 1. Démarrer l'évaluation initiale
        print("   📝 Démarrage de l'évaluation...")
        response = requests.post(
            "http://localhost:8000/api/v1/assessments/initial/start",
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            assessment_data = response.json()
            assessment_id = assessment_data.get("id")
            print(f"✅ Évaluation initiale démarrée (ID: {assessment_id})")
            
            # 2. Récupérer les questions
            print("   📋 Récupération des questions...")
            questions_response = requests.get(
                f"http://localhost:8000/api/v1/assessments/{assessment_id}/questions",
                headers=headers,
                timeout=10
            )
            
            if questions_response.status_code == 200:
                questions = questions_response.json()
                print(f"✅ {len(questions)} questions récupérées")
                
                # 3. Simuler des réponses
                print("   ✍️ Simulation des réponses...")
                answers = []
                for i, question in enumerate(questions[:3]):  # Répondre aux 3 premières
                    answer = {
                        "question_id": question["id"],
                        "answer": "Réponse de test",
                        "time_taken": 30
                    }
                    answers.append(answer)
                
                # 4. Soumettre l'évaluation
                submit_response = requests.post(
                    f"http://localhost:8000/api/v1/assessments/{assessment_id}/submit",
                    headers=headers,
                    json={"answers": answers},
                    timeout=10
                )
                
                if submit_response.status_code == 200:
                    result = submit_response.json()
                    print("✅ Évaluation soumise avec succès")
                    print(f"   Score: {result.get('percentage', 'N/A')}%")
                    return True
                else:
                    print(f"❌ Échec de soumission: {submit_response.status_code}")
                    return False
            else:
                print(f"❌ Impossible de récupérer les questions: {questions_response.status_code}")
                return False
        else:
            print(f"❌ Impossible de démarrer l'évaluation: {response.status_code}")
            print(f"   Réponse: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur lors du test d'évaluation: {e}")
        return False

def test_learning_paths(token):
    """Tester les parcours d'apprentissage"""
    print("\n🛤️ Test des parcours d'apprentissage...")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        # 1. Récupérer les parcours disponibles
        print("   📚 Récupération des parcours...")
        response = requests.get(
            "http://localhost:8000/api/v1/learning_paths/",
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            paths = response.json()
            print(f"✅ {len(paths)} parcours disponibles")
            
            if paths:
                # 2. Tester la génération d'un parcours adaptatif
                print("   🎯 Test de génération de parcours adaptatif...")
                student_id = 1  # ID de l'étudiant de test
                
                generate_response = requests.post(
                    f"http://localhost:8000/api/v1/learning_paths/generate/{student_id}",
                    headers=headers,
                    timeout=10
                )
                
                if generate_response.status_code == 200:
                    generated_path = generate_response.json()
                    print("✅ Parcours adaptatif généré avec succès")
                    print(f"   Titre: {generated_path.get('title', 'N/A')}")
                    print(f"   Niveau: {generated_path.get('level', 'N/A')}")
                    return True
                else:
                    print(f"❌ Échec de génération: {generate_response.status_code}")
                    return False
            else:
                print("⚠️ Aucun parcours disponible pour le test")
                return False
        else:
            print(f"❌ Impossible de récupérer les parcours: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur lors du test des parcours: {e}")
        return False

def test_learning_analytics(token):
    """Tester les analytics d'apprentissage"""
    print("\n📊 Test des analytics d'apprentissage...")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        # Test des endpoints d'analytics
        endpoints = [
            "/api/v1/analytics/student/1/stats",
            "/api/v1/analytics/interactive-charts/1?chart_type=performance",
            "/api/v1/analytics/subject-progress"
        ]
        
        success_count = 0
        for endpoint in endpoints:
            try:
                response = requests.get(
                    f"http://localhost:8000{endpoint}",
                    headers=headers,
                    timeout=10
                )
                
                if response.status_code == 200:
                    print(f"✅ {endpoint} - Fonctionnel")
                    success_count += 1
                else:
                    print(f"❌ {endpoint} - Erreur {response.status_code}")
                    
            except Exception as e:
                print(f"❌ {endpoint} - Erreur: {e}")
        
        if success_count >= 2:
            print(f"✅ {success_count}/3 endpoints analytics fonctionnels")
            return True
        else:
            print(f"❌ Seulement {success_count}/3 endpoints analytics fonctionnels")
            return False
            
    except Exception as e:
        print(f"❌ Erreur lors du test des analytics: {e}")
        return False

def run_complete_test():
    """Exécuter tous les tests"""
    print("🚀 TEST COMPLET - ÉVALUATION INITIALE & PARCOURS D'APPRENTISSAGE")
    print("=" * 70)
    
    # Test 1: Connexion backend
    if not test_backend_connection():
        print("\n❌ Test arrêté: Backend non accessible")
        return False
    
    # Test 2: Authentification
    token = test_authentication()
    if not token:
        print("\n❌ Test arrêté: Authentification échouée")
        return False
    
    # Test 3: Évaluation initiale
    assessment_ok = test_initial_assessment(token)
    
    # Test 4: Parcours d'apprentissage
    paths_ok = test_learning_paths(token)
    
    # Test 5: Analytics d'apprentissage
    analytics_ok = test_learning_analytics(token)
    
    # Résumé final
    print("\n" + "=" * 70)
    print("📋 RÉSUMÉ DES TESTS")
    print("=" * 70)
    
    results = {
        "🔌 Connexion Backend": True,
        "🔐 Authentification": bool(token),
        "🎯 Évaluation Initiale": assessment_ok,
        "🛤️ Parcours d'Apprentissage": paths_ok,
        "📊 Analytics d'Apprentissage": analytics_ok
    }
    
    for test_name, result in results.items():
        status = "✅ FONCTIONNEL" if result else "❌ NON FONCTIONNEL"
        print(f"{test_name}: {status}")
    
    # Calcul du score global
    functional_count = sum(results.values())
    total_count = len(results)
    score_percentage = (functional_count / total_count) * 100
    
    print(f"\n📊 SCORE GLOBAL: {functional_count}/{total_count} ({score_percentage:.1f}%)")
    
    if score_percentage >= 80:
        print("🎉 EXCELLENT! La plateforme est prête pour la production")
    elif score_percentage >= 60:
        print("⚠️ BON - Quelques ajustements nécessaires")
    else:
        print("❌ CRITIQUE - Révision majeure requise")
    
    # Recommandations
    print("\n💡 RECOMMANDATIONS:")
    if not assessment_ok:
        print("   - Vérifier les tables d'évaluation dans la base de données")
        print("   - Exécuter: python init_assessment_direct.py")
    
    if not paths_ok:
        print("   - Vérifier les tables de parcours d'apprentissage")
        print("   - Exécuter: python create_real_data.py")
    
    if not analytics_ok:
        print("   - Vérifier les endpoints d'analytics")
        print("   - Vérifier les permissions utilisateur")
    
    return score_percentage >= 60

if __name__ == "__main__":
    try:
        success = run_complete_test()
        if success:
            print("\n✅ Tests terminés avec succès!")
            sys.exit(0)
        else:
            print("\n❌ Tests échoués - Révision requise")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n⏹️ Tests interrompus par l'utilisateur")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Erreur critique: {e}")
        sys.exit(1)







