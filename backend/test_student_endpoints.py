#!/usr/bin/env python3
"""
Script de test pour vérifier la connectivité des endpoints étudiants
"""

import requests
import json
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:8000"
TEST_USER_ID = 2  # ID de l'étudiant test que nous avons créé

def test_student_endpoints():
    """Tester tous les endpoints étudiants"""
    
    print("🧪 TEST DES ENDPOINTS ÉTUDIANTS")
    print("=" * 50)
    
    # Liste des endpoints à tester
    endpoints = [
        # Analytics étudiant
        f"/api/v1/student_analytics/student/{TEST_USER_ID}/analytics",
        
        # Quiz assignés
        f"/api/v1/quizzes/assigned/{TEST_USER_ID}",
        
        # Résultats de quiz
        f"/api/v1/quiz_results/user/{TEST_USER_ID}",
        
        # Badges
        f"/api/v1/badges/user/{TEST_USER_ID}",
        
        # Performance étudiant
        f"/api/v1/student_performance/{TEST_USER_ID}",
        f"/api/v1/student_performance/{TEST_USER_ID}/progress",
        
        # Gamification
        f"/api/v1/gamification/student/{TEST_USER_ID}/stats",
        f"/api/v1/gamification/user/{TEST_USER_ID}/points",
        f"/api/v1/gamification/user/{TEST_USER_ID}/level",
        
        # Parcours d'apprentissage
        f"/api/v1/learning_paths/student/{TEST_USER_ID}/current",
        
        # Messages
        f"/api/v1/messages/user/{TEST_USER_ID}",
        
        # Notifications
        f"/api/v1/notifications/user/{TEST_USER_ID}",
        
        # Analytics IA
        f"/api/v1/ai-analytics/analytics/learning-analytics/{TEST_USER_ID}",
        f"/api/v1/ai-analytics/analytics/predictions/{TEST_USER_ID}",
        
        # Recommandations
        f"/api/v1/recommendations/student/{TEST_USER_ID}/personalized",
        f"/api/v1/recommendations/student/{TEST_USER_ID}/adaptive",
        
        # Tests adaptatifs
        f"/api/v1/adaptive_quizzes/student/{TEST_USER_ID}/progress",
        
        # Analyse des lacunes
        f"/api/v1/gap_analysis/student/{TEST_USER_ID}/gaps",
        
        # Monitoring de performance
        f"/api/v1/performance_monitoring/student/{TEST_USER_ID}/detailed"
    ]
    
    results = {
        "success": [],
        "errors": [],
        "not_found": [],
        "forbidden": []
    }
    
    for endpoint in endpoints:
        try:
            print(f"\n🔍 Test de: {endpoint}")
            
            # Test sans authentification (pour voir si l'endpoint existe)
            response = requests.get(f"{BASE_URL}{endpoint}", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ 200 OK - Données reçues: {len(str(data))} caractères")
                if data:
                    print(f"   📊 Exemple de données: {str(data)[:100]}...")
                results["success"].append(endpoint)
                
            elif response.status_code == 404:
                print(f"❌ 404 Not Found - Endpoint inexistant")
                results["not_found"].append(endpoint)
                
            elif response.status_code == 403:
                print(f"🔒 403 Forbidden - Endpoint trouvé mais nécessite authentification")
                results["forbidden"].append(endpoint)
                
            elif response.status_code == 401:
                print(f"🔑 401 Unauthorized - Endpoint trouvé mais nécessite authentification")
                results["forbidden"].append(endpoint)
                
            else:
                print(f"⚠️ {response.status_code} - Réponse inattendue")
                results["errors"].append(f"{endpoint}: {response.status_code}")
                
        except requests.exceptions.ConnectionError:
            print(f"❌ Erreur de connexion - Serveur non accessible")
            results["errors"].append(f"{endpoint}: Erreur de connexion")
            
        except requests.exceptions.Timeout:
            print(f"⏰ Timeout - Endpoint trop lent")
            results["errors"].append(f"{endpoint}: Timeout")
            
        except Exception as e:
            print(f"❌ Erreur inattendue: {str(e)}")
            results["errors"].append(f"{endpoint}: {str(e)}")
    
    # Résumé des tests
    print("\n" + "=" * 50)
    print("📊 RÉSUMÉ DES TESTS")
    print("=" * 50)
    
    print(f"✅ Endpoints fonctionnels: {len(results['success'])}")
    for endpoint in results["success"]:
        print(f"   - {endpoint}")
    
    print(f"\n🔒 Endpoints nécessitant authentification: {len(results['forbidden'])}")
    for endpoint in results["forbidden"]:
        print(f"   - {endpoint}")
    
    print(f"\n❌ Endpoints non trouvés: {len(results['not_found'])}")
    for endpoint in results["not_found"]:
        print(f"   - {endpoint}")
    
    print(f"\n⚠️ Erreurs: {len(results['errors'])}")
    for error in results["errors"]:
        print(f"   - {error}")
    
    # Calcul du pourcentage de connectivité
    total_endpoints = len(endpoints)
    working_endpoints = len(results["success"]) + len(results["forbidden"])
    connectivity_percentage = (working_endpoints / total_endpoints) * 100
    
    print(f"\n🎯 CONNECTIVITÉ GLOBALE: {connectivity_percentage:.1f}%")
    print(f"   - Total testé: {total_endpoints}")
    print(f"   - Fonctionnels: {working_endpoints}")
    print(f"   - Non fonctionnels: {total_endpoints - working_endpoints}")
    
    return results

if __name__ == "__main__":
    test_student_endpoints()























