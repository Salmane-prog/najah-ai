#!/usr/bin/env python3
"""
Script pour tester l'endpoint dashboard-data et vérifier le calcul des étudiants
"""

import requests
import json

def test_dashboard_data():
    print("🧪 Test de l'endpoint dashboard-data")
    
    # URL de l'API
    base_url = "http://localhost:8000"
    
    # 1. Login avec marie.dubois@najah.ai
    login_data = {
        "email": "marie.dubois@najah.ai",
        "password": "password123"
    }
    
    try:
        # Login
        print("🔐 Connexion avec marie.dubois@najah.ai...")
        login_response = requests.post(f"{base_url}/api/v1/auth/login", json=login_data)
        
        if login_response.status_code != 200:
            print(f"❌ Erreur de connexion: {login_response.status_code}")
            print(login_response.text)
            return
        
        login_result = login_response.json()
        token = login_result.get("access_token")
        
        if not token:
            print("❌ Token non trouvé dans la réponse")
            return
        
        print("✅ Connexion réussie")
        
        # 2. Appeler l'endpoint dashboard-data
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        print("📊 Récupération des données du dashboard...")
        dashboard_response = requests.get(f"{base_url}/api/v1/dashboard/dashboard-data", headers=headers)
        
        if dashboard_response.status_code != 200:
            print(f"❌ Erreur dashboard-data: {dashboard_response.status_code}")
            print(dashboard_response.text)
            return
        
        dashboard_data = dashboard_response.json()
        
        # 3. Afficher les résultats
        print("\n📋 Résultats du dashboard:")
        print(f"   - Token: {token[:20]}...")
        
        if "overview" in dashboard_data:
            overview = dashboard_data["overview"]
            print(f"   - Classes: {overview.get('classes', 0)}")
            print(f"   - Étudiants: {overview.get('students', 0)}")
            print(f"   - Quiz: {overview.get('quizzes', 0)}")
            print(f"   - Progression moyenne: {overview.get('average_progression', 0)}%")
            print(f"   - Activité récente: {overview.get('recent_activity', {}).get('quiz_results_week', 0)}")
        else:
            print("   ❌ Section 'overview' non trouvée dans la réponse")
            print(f"   📄 Réponse complète: {json.dumps(dashboard_data, indent=2)}")
        
        # 4. Comparer avec les données du script check_specific_teacher.py
        print("\n🔍 Comparaison avec check_specific_teacher.py:")
        print("   - Script: 6 étudiants")
        print(f"   - Dashboard: {overview.get('students', 0)} étudiants")
        
        if overview.get('students', 0) == 6:
            print("   ✅ Les nombres correspondent !")
        else:
            print("   ❌ Les nombres ne correspondent pas")
            print("   🔧 Le calcul dans dashboard_data.py doit être corrigé")
        
    except requests.exceptions.ConnectionError:
        print("❌ Impossible de se connecter au serveur. Assurez-vous que le backend est démarré.")
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    test_dashboard_data() 