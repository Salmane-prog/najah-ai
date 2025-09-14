#!/usr/bin/env python3
"""
Script de test pour vérifier la connectivité des endpoints étudiants avec authentification
"""

import requests
import json
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:8000"
TEST_USER_ID = 2  # ID de l'étudiant test

def get_auth_token():
    """Obtenir un token d'authentification pour l'étudiant test"""
    try:
        # Utiliser les identifiants de l'étudiant test que nous avons créé
        login_data = {
            "username": "etudiant1_real",
            "password": "password123"
        }
        
        response = requests.post(f"{BASE_URL}/api/v1/auth/login", json=login_data)
        
        if response.status_code == 200:
            data = response.json()
            token = data.get("access_token")
            if token:
                print(f"✅ Token d'authentification obtenu pour {login_data['username']}")
                return token
            else:
                print("❌ Token non trouvé dans la réponse")
                return None
        else:
            print(f"❌ Échec de connexion: {response.status_code}")
            print(f"   Réponse: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Erreur lors de l'authentification: {str(e)}")
        return None

def test_student_endpoints_with_auth(token):
    """Tester les endpoints étudiants avec authentification"""
    
    if not token:
        print("❌ Impossible de tester sans token d'authentification")
        return
    
    print("\n🧪 TEST DES ENDPOINTS ÉTUDIANTS AVEC AUTHENTIFICATION")
    print("=" * 60)
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # Endpoints à tester avec authentification
    endpoints = [
        # Analytics étudiant
        f"/api/v1/student_analytics/student/{TEST_USER_ID}/analytics",
        
        # Quiz assignés
        f"/api/v1/quizzes/assigned/{TEST_USER_ID}",
        
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
        "forbidden": [],
        "data_samples": {}
    }
    
    for endpoint in endpoints:
        try:
            print(f"\n🔍 Test de: {endpoint}")
            
            response = requests.get(f"{BASE_URL}{endpoint}", headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ 200 OK - Données reçues: {len(str(data))} caractères")
                
                # Stocker un échantillon des données
                if data:
                    results["data_samples"][endpoint] = str(data)[:200] + "..." if len(str(data)) > 200 else str(data)
                    print(f"   📊 Exemple de données: {str(data)[:100]}...")
                    
                    # Vérifier si ce sont des données réelles ou mockées
                    if "mock" in str(data).lower() or "default" in str(data).lower() or "example" in str(data).lower():
                        print("   ⚠️  Données potentiellement mockées")
                    else:
                        print("   ✅ Données réelles détectées")
                        
                results["success"].append(endpoint)
                
            elif response.status_code == 404:
                print(f"❌ 404 Not Found - Endpoint inexistant")
                results["not_found"].append(endpoint)
                
            elif response.status_code == 403:
                print(f"🔒 403 Forbidden - Accès refusé même avec authentification")
                results["forbidden"].append(endpoint)
                
            elif response.status_code == 401:
                print(f"🔑 401 Unauthorized - Token invalide ou expiré")
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
    print("\n" + "=" * 60)
    print("📊 RÉSUMÉ DES TESTS AVEC AUTHENTIFICATION")
    print("=" * 60)
    
    print(f"✅ Endpoints fonctionnels: {len(results['success'])}")
    for endpoint in results["success"]:
        print(f"   - {endpoint}")
    
    print(f"\n🔒 Endpoints avec erreur d'authentification: {len(results['forbidden'])}")
    for endpoint in results["forbidden"]:
        print(f"   - {endpoint}")
    
    print(f"\n❌ Endpoints non trouvés: {len(results['not_found'])}")
    for endpoint in results["not_found"]:
        print(f"   - {endpoint}")
    
    print(f"\n⚠️ Erreurs: {len(results['errors'])}")
    for error in results["errors"]:
        print(f"   - {error}")
    
    # Afficher les échantillons de données
    if results["data_samples"]:
        print(f"\n📊 ÉCHANTILLONS DE DONNÉES RÉCUPÉRÉES")
        print("=" * 60)
        for endpoint, sample in results["data_samples"].items():
            print(f"\n🔍 {endpoint}:")
            print(f"   {sample}")
    
    # Calcul du pourcentage de connectivité
    total_endpoints = len(endpoints)
    working_endpoints = len(results["success"])
    connectivity_percentage = (working_endpoints / total_endpoints) * 100
    
    print(f"\n🎯 CONNECTIVITÉ GLOBALE: {connectivity_percentage:.1f}%")
    print(f"   - Total testé: {total_endpoints}")
    print(f"   - Fonctionnels: {working_endpoints}")
    print(f"   - Non fonctionnels: {total_endpoints - working_endpoints}")
    
    return results

def main():
    """Fonction principale"""
    print("🚀 DÉMARRAGE DES TESTS DES ENDPOINTS ÉTUDIANTS")
    print("=" * 60)
    
    # Étape 1: Authentification
    print("\n🔑 ÉTAPE 1: AUTHENTIFICATION")
    token = get_auth_token()
    
    if not token:
        print("❌ Impossible de continuer sans authentification")
        return
    
    # Étape 2: Test des endpoints avec authentification
    print("\n🔍 ÉTAPE 2: TEST DES ENDPOINTS")
    results = test_student_endpoints_with_auth(token)
    
    # Étape 3: Conclusion
    print("\n🎯 CONCLUSION")
    print("=" * 60)
    
    if results["success"]:
        print("✅ Les endpoints étudiants sont connectés et fonctionnels !")
        print(f"   - {len(results['success'])} endpoints retournent des données")
        
        # Vérifier la qualité des données
        real_data_count = 0
        for endpoint in results["success"]:
            sample = results["data_samples"].get(endpoint, "")
            if "mock" not in sample.lower() and "default" not in sample.lower() and "example" not in sample.lower():
                real_data_count += 1
        
        print(f"   - {real_data_count} endpoints retournent des données réelles")
        print(f"   - {len(results['success']) - real_data_count} endpoints retournent des données mockées")
        
    else:
        print("❌ Aucun endpoint étudiant n'est fonctionnel")
    
    if results["forbidden"]:
        print(f"\n🔒 {len(results['forbidden'])} endpoints nécessitent des permissions supplémentaires")
    
    if results["not_found"]:
        print(f"\n❌ {len(results['not_found'])} endpoints n'existent pas")

if __name__ == "__main__":
    main()
