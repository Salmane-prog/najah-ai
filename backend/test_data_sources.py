#!/usr/bin/env python3
"""
Script pour tester tous les endpoints et identifier les données réelles vs mockées
"""

import requests
import json
from datetime import datetime

def test_data_sources():
    base_url = "http://localhost:8000"
    
    print("🔍 AUDIT DES DONNÉES RÉELLES vs MOCKÉES")
    print("=" * 60)
    
    # 1. Test d'authentification
    print("\n🔐 1. AUTHENTIFICATION")
    login_data = {
        "email": "teacher@test.com",
        "password": "teacher123"
    }
    
    try:
        response = requests.post(f"{base_url}/api/v1/auth/login", json=login_data)
        if response.status_code == 200:
            data = response.json()
            token = data.get("access_token")
            print("✅ Authentification réussie")
            
            headers = {"Authorization": f"Bearer {token}"}
            
            # 2. Test des endpoints principaux
            endpoints_to_test = [
                # Dashboard et Analytics
                ("/api/v1/analytics/dashboard/overview", "Dashboard Overview"),
                ("/api/v1/analytics/recent-activity", "Recent Activity"),
                ("/api/v1/activity/teacher-tasks", "Teacher Tasks"),
                ("/api/v1/notifications/teacher-alerts", "Teacher Alerts"),
                
                # Utilisateurs et Classes
                ("/api/v1/users/students", "Students List"),
                ("/api/v1/classes/", "Classes List"),
                ("/api/v1/users?role=student", "All Students"),
                
                # Quiz et Contenus
                ("/api/v1/quizzes/", "Quizzes List"),
                ("/api/v1/contents/", "Contents List"),
                ("/api/v1/learning_paths/", "Learning Paths"),
                
                # Messages
                ("/api/v1/teacher_messaging/conversations", "Teacher Messages"),
                ("/api/v1/messages/", "General Messages"),
                
                # Performance et Analytics
                ("/api/v1/student_performance/class/1/students-performance", "Student Performance"),
                ("/api/v1/analytics/class-performance", "Class Performance"),
                
                # Badges et Gamification
                ("/api/v1/badges/", "Badges List"),
                ("/api/v1/gamification/leaderboard", "Leaderboard"),
                
                # Rapports
                ("/api/v1/reports/teacher", "Teacher Reports"),
                
                # Quiz JSON (données spéciales)
                ("/api/v1/quiz_json/json/list", "Quiz JSON List"),
                
                # Catégories
                ("/api/v1/categories/", "Categories"),
            ]
            
            print("\n📊 2. TEST DES ENDPOINTS")
            print("-" * 40)
            
            real_data_endpoints = []
            mock_data_endpoints = []
            error_endpoints = []
            
            for endpoint, description in endpoints_to_test:
                try:
                    response = requests.get(f"{base_url}{endpoint}", headers=headers)
                    print(f"\n🔍 {description}")
                    print(f"   Endpoint: {endpoint}")
                    print(f"   Status: {response.status_code}")
                    
                    if response.status_code == 200:
                        data = response.json()
                        
                        # Analyser le contenu pour déterminer si c'est des données réelles
                        if isinstance(data, list):
                            if len(data) > 0:
                                print(f"   ✅ DONNÉES RÉELLES - {len(data)} éléments")
                                real_data_endpoints.append((endpoint, description, len(data)))
                            else:
                                print(f"   ⚠️  LISTE VIDE - Pas de données")
                                mock_data_endpoints.append((endpoint, description, "empty"))
                        elif isinstance(data, dict):
                            # Vérifier si c'est des données de test/mock
                            if any(key in str(data).lower() for key in ['mock', 'test', 'demo', 'example']):
                                print(f"   ❌ DONNÉES MOCKÉES")
                                mock_data_endpoints.append((endpoint, description, "mock"))
                            else:
                                print(f"   ✅ DONNÉES RÉELLES")
                                real_data_endpoints.append((endpoint, description, "dict"))
                        else:
                            print(f"   ❓ TYPE INCONNU: {type(data)}")
                            
                        # Afficher un aperçu des données
                        if isinstance(data, list) and len(data) > 0:
                            sample = data[0]
                            if isinstance(sample, dict):
                                keys = list(sample.keys())[:3]  # Afficher les 3 premières clés
                                print(f"   📋 Champs: {', '.join(keys)}...")
                        elif isinstance(data, dict):
                            keys = list(data.keys())[:3]
                            print(f"   📋 Champs: {', '.join(keys)}...")
                            
                    else:
                        print(f"   ❌ ERREUR {response.status_code}")
                        error_endpoints.append((endpoint, description, response.status_code))
                        
                except Exception as e:
                    print(f"   💥 EXCEPTION: {str(e)}")
                    error_endpoints.append((endpoint, description, str(e)))
            
            # 3. Résumé
            print("\n" + "=" * 60)
            print("📋 RÉSUMÉ DE L'AUDIT")
            print("=" * 60)
            
            print(f"\n✅ DONNÉES RÉELLES ({len(real_data_endpoints)} endpoints):")
            for endpoint, description, count in real_data_endpoints:
                print(f"   • {description} ({endpoint}) - {count} éléments")
            
            print(f"\n❌ DONNÉES MOCKÉES ({len(mock_data_endpoints)} endpoints):")
            for endpoint, description, reason in mock_data_endpoints:
                print(f"   • {description} ({endpoint}) - {reason}")
            
            print(f"\n💥 ERREURS ({len(error_endpoints)} endpoints):")
            for endpoint, description, error in error_endpoints:
                print(f"   • {description} ({endpoint}) - {error}")
            
            # 4. Pourcentage de données réelles
            total_endpoints = len(endpoints_to_test)
            real_percentage = (len(real_data_endpoints) / total_endpoints) * 100
            mock_percentage = (len(mock_data_endpoints) / total_endpoints) * 100
            error_percentage = (len(error_endpoints) / total_endpoints) * 100
            
            print(f"\n📊 STATISTIQUES:")
            print(f"   • Données réelles: {real_percentage:.1f}%")
            print(f"   • Données mockées: {mock_percentage:.1f}%")
            print(f"   • Erreurs: {error_percentage:.1f}%")
            
            if real_percentage >= 80:
                print(f"\n🎉 EXCELLENT! {real_percentage:.1f}% des données sont réelles!")
            elif real_percentage >= 60:
                print(f"\n👍 BON! {real_percentage:.1f}% des données sont réelles")
            else:
                print(f"\n⚠️  ATTENTION! Seulement {real_percentage:.1f}% des données sont réelles")
                
        else:
            print(f"❌ Échec de l'authentification: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Erreur lors des tests: {e}")

if __name__ == "__main__":
    test_data_sources() 