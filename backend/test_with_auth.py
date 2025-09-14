#!/usr/bin/env python3
"""
Script de test avec authentification pour vérifier que les endpoints fonctionnent
"""

import requests
import json

def test_with_authentication():
    """Tester les endpoints avec authentification"""
    print("🔐 TEST DES ENDPOINTS AVEC AUTHENTIFICATION")
    print("=" * 60)
    
    base_url = "http://localhost:8000"
    
    # Informations de connexion (utilisez un étudiant existant)
    login_data = {
        "email": "salmane.hamidi@najah.ai",  # Étudiant existant
        "password": "salmane123@"
    }
    
    print("🔑 Tentative de connexion...")
    try:
        # Connexion
        response = requests.post(f"{base_url}/api/v1/auth/login", json=login_data, timeout=10)
        if response.status_code == 200:
            auth_data = response.json()
            token = auth_data.get("access_token")
            user = auth_data.get("user", {})
            user_id = user.get("id")
            
            print(f"   ✅ Connecté avec succès! User ID: {user_id}")
            print(f"   🔑 Token: {token[:20]}...")
            
            # Headers avec authentification
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
            
            # Test 1: Endpoint assessments avec authentification
            print(f"\n1️⃣ Test endpoint /api/v1/assessments/student/{user_id}")
            try:
                response = requests.get(f"{base_url}/api/v1/assessments/student/{user_id}", headers=headers, timeout=10)
                print(f"   Status: {response.status_code}")
                if response.status_code == 200:
                    data = response.json()
                    print(f"   ✅ Succès! {data['summary']['total_assessments']} évaluations trouvées")
                    print(f"   📊 Résumé: {data['summary']}")
                else:
                    print(f"   ❌ Erreur: {response.text}")
            except Exception as e:
                print(f"   ❌ Erreur de connexion: {e}")
            
            # Test 2: Endpoint learning_paths avec authentification
            print(f"\n2️⃣ Test endpoint /api/v1/learning_paths/student/{user_id}")
            try:
                response = requests.get(f"{base_url}/api/v1/learning_paths/student/{user_id}", headers=headers, timeout=10)
                print(f"   Status: {response.status_code}")
                if response.status_code == 200:
                    data = response.json()
                    print(f"   ✅ Succès! {data['summary']['total_available']} parcours disponibles")
                    print(f"   📊 Résumé: {data['summary']}")
                else:
                    print(f"   ❌ Erreur: {response.text}")
            except Exception as e:
                print(f"   ❌ Erreur de connexion: {e}")
            
        else:
            print(f"   ❌ Échec de connexion: {response.status_code}")
            print(f"   Détails: {response.text}")
            
    except Exception as e:
        print(f"   ❌ Erreur de connexion: {e}")
    
    print("\n" + "=" * 60)
    print("🎯 RÉSUMÉ DES TESTS")
    print("✅ 200 = Succès complet avec authentification")
    print("⚠️ 403 = Problème d'authentification")
    print("❌ 404 = Endpoint non trouvé")
    print("❌ 500 = Erreur serveur")

if __name__ == "__main__":
    print("🚀 Démarrage des tests avec authentification...")
    print("Assurez-vous que votre serveur backend est démarré sur http://localhost:8000")
    print("Appuyez sur Entrée pour continuer...")
    input()
    
    test_with_authentication() 