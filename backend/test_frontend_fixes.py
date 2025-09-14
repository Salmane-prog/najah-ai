#!/usr/bin/env python3
"""
Script de test pour vérifier que les corrections frontend fonctionnent
"""

import requests
import json

def test_frontend_fixes():
    """Tester que les corrections frontend fonctionnent"""
    print("🧪 TEST DES CORRECTIONS FRONTEND")
    print("=" * 60)
    
    base_url = "http://localhost:8000"
    
    # Test 1: Endpoint analytics avec authentification
    print("\n1️⃣ Test endpoint /api/v1/analytics/interactive-charts/30")
    try:
        # D'abord se connecter pour obtenir un token
        login_data = {
            "email": "salmane.hamidi@najah.ai",
            "password": "salmane123@"
        }
        
        response = requests.post(f"{base_url}/api/v1/auth/login", json=login_data, timeout=10)
        if response.status_code == 200:
            auth_data = response.json()
            token = auth_data.get("access_token")
            
            print(f"   ✅ Connecté avec succès! Token: {token[:20]}...")
            
            # Tester l'endpoint analytics
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
            
            response = requests.get(
                f"{base_url}/api/v1/analytics/interactive-charts/30?chart_type=performance&period=month", 
                headers=headers, 
                timeout=10
            )
            
            print(f"   Status: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ Succès! Données reçues: {len(data.get('data', {}).get('labels', []))} points")
            else:
                print(f"   ❌ Erreur: {response.text}")
        else:
            print(f"   ❌ Échec de connexion: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
    
    # Test 2: Endpoint assessments
    print("\n2️⃣ Test endpoint /api/v1/assessments/student/30")
    try:
        if 'token' in locals():
            response = requests.get(f"{base_url}/api/v1/assessments/student/30", headers=headers, timeout=10)
            print(f"   Status: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ Succès! {data['summary']['total_assessments']} évaluations trouvées")
            else:
                print(f"   ❌ Erreur: {response.text}")
        else:
            print("   ⚠️ Pas de token disponible")
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
    
    # Test 3: Endpoint learning_paths
    print("\n3️⃣ Test endpoint /api/v1/learning_paths/student/30")
    try:
        if 'token' in locals():
            response = requests.get(f"{base_url}/api/v1/learning_paths/student/30", headers=headers, timeout=10)
            print(f"   Status: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ Succès! {data['summary']['total_available']} parcours disponibles")
            else:
                print(f"   ❌ Erreur: {response.text}")
        else:
            print("   ⚠️ Pas de token disponible")
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
    
    print("\n" + "=" * 60)
    print("🎯 RÉSUMÉ DES TESTS")
    print("✅ 200 = Succès complet")
    print("⚠️ 403 = Problème d'authentification")
    print("❌ 404 = Endpoint non trouvé")
    print("❌ 500 = Erreur serveur")

if __name__ == "__main__":
    print("🚀 Démarrage des tests des corrections frontend...")
    print("Assurez-vous que votre serveur backend est démarré sur http://localhost:8000")
    print("Appuyez sur Entrée pour continuer...")
    input()
    
    test_frontend_fixes()







