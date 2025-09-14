#!/usr/bin/env python3
"""
Script pour tester l'authentification et récupérer les données
"""

import requests
import json

def test_auth_with_data():
    """Tester l'authentification et récupérer les données"""
    print("🔐 TEST D'AUTHENTIFICATION ET RÉCUPÉRATION DES DONNÉES")
    print("=" * 70)
    
    base_url = "http://localhost:8000"
    
    # Étape 1: Se connecter pour obtenir un token
    print("\n1️⃣ Connexion pour obtenir un token...")
    login_data = {
        "email": "salmane.hajouji@najah.ai",
        "password": "password123"
    }
    
    try:
        login_response = requests.post(f"{base_url}/api/v1/auth/login", json=login_data)
        print(f"   Status: {login_response.status_code}")
        
        if login_response.status_code == 200:
            auth_data = login_response.json()
            token = auth_data.get('access_token')
            user_id = auth_data.get('id')  # user_id est directement dans la réponse
            
            if token and user_id:
                print(f"   ✅ Connexion réussie!")
                print(f"      - User ID: {user_id}")
                print(f"      - Token: {token[:20]}...")
                
                # Étape 2: Tester les endpoints avec authentification
                print(f"\n2️⃣ Test des endpoints avec authentification (User ID: {user_id})...")
                
                headers = {"Authorization": f"Bearer {token}"}
                
                # Test 1: Évaluations
                print(f"\n   📝 Test /api/v1/assessments/student/{user_id}")
                try:
                    response = requests.get(f"{base_url}/api/v1/assessments/student/{user_id}", headers=headers)
                    print(f"      Status: {response.status_code}")
                    if response.status_code == 200:
                        data = response.json()
                        print(f"      ✅ Données reçues:")
                        print(f"         - Type: {type(data)}")
                        print(f"         - Clés: {list(data.keys()) if isinstance(data, dict) else 'N/A'}")
                        print(f"         - Assessments: {len(data.get('assessments', []))} éléments")
                        print(f"         - Structure: {json.dumps(data, indent=4, default=str)}")
                    else:
                        print(f"      ❌ Erreur: {response.text}")
                except Exception as e:
                    print(f"      ❌ Erreur de connexion: {e}")
                
                # Test 2: Parcours d'apprentissage
                print(f"\n   🛤️ Test /api/v1/learning_paths/student/{user_id}")
                try:
                    response = requests.get(f"{base_url}/api/v1/learning_paths/student/{user_id}", headers=headers)
                    print(f"      Status: {response.status_code}")
                    if response.status_code == 200:
                        data = response.json()
                        print(f"      ✅ Données reçues:")
                        print(f"         - Type: {type(data)}")
                        print(f"         - Clés: {list(data.keys()) if isinstance(data, dict) else 'N/A'}")
                        print(f"         - Learning Paths: {len(data.get('learning_paths', []))} éléments")
                        print(f"         - Structure: {json.dumps(data, indent=4, default=str)}")
                    else:
                        print(f"      ❌ Erreur: {response.text}")
                except Exception as e:
                    print(f"      ❌ Erreur de connexion: {e}")
                
                # Test 3: Quiz assignés
                print(f"\n   📚 Test /api/v1/quizzes/assigned/{user_id}")
                try:
                    response = requests.get(f"{base_url}/api/v1/quizzes/assigned/{user_id}", headers=headers)
                    print(f"      Status: {response.status_code}")
                    if response.status_code == 200:
                        data = response.json()
                        print(f"      ✅ Données reçues:")
                        print(f"         - Type: {type(data)}")
                        print(f"         - Clés: {list(data.keys()) if isinstance(data, dict) else 'N/A'}")
                        print(f"         - Quizzes: {len(data.get('quizzes', []))} éléments")
                        print(f"         - Structure: {json.dumps(data, indent=4, default=str)}")
                    else:
                        print(f"      ❌ Erreur: {response.text}")
                except Exception as e:
                    print(f"      ❌ Erreur de connexion: {e}")
                
            else:
                print(f"   ❌ Token ou User ID manquant dans la réponse")
                print(f"      - Réponse complète: {json.dumps(auth_data, indent=2)}")
        else:
            print(f"   ❌ Échec de la connexion: {login_response.text}")
            
    except Exception as e:
        print(f"   ❌ Erreur lors de la connexion: {e}")
    
    print("\n" + "=" * 70)
    print("🎯 RÉSUMÉ DES TESTS")
    print("✅ 200 = Données reçues avec authentification")
    print("⚠️ 403 = Problème d'authentification")
    print("❌ 404 = Endpoint non trouvé")
    print("❌ 500 = Erreur serveur")

if __name__ == "__main__":
    print("🚀 Démarrage du test d'authentification et de récupération des données...")
    print("Assurez-vous que votre serveur backend est démarré sur http://localhost:8000")
    print("Appuyez sur Entrée pour continuer...")
    input()
    
    test_auth_with_data()
