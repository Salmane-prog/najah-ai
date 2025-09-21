#!/usr/bin/env python3
"""
Script pour tester que le frontend peut maintenant charger les analytics
"""

import requests
import json

def test_frontend_analytics():
    """Teste que le frontend peut charger les analytics"""
    
    print("🧪 Test que le frontend peut charger les analytics")
    print("=" * 70)
    
    # ÉTAPE 1 : Connexion
    print("\n🔐 ÉTAPE 1 : Connexion...")
    
    login_data = {
        "email": "marizee.dubois@najah.ai",
        "password": "password123"
    }
    
    try:
        response = requests.post(
            "http://localhost:8000/api/v1/auth/login",
            json=login_data
        )
        
        if response.status_code != 200:
            print(f"❌ Échec de la connexion: {response.text}")
            return None
        
        data = response.json()
        token = data.get("access_token")
        print(f"✅ Connexion réussie ! Token: {token[:50]}...")
        
        # ÉTAPE 2 : Test des analytics (comme le frontend les appellerait)
        print("\n📊 ÉTAPE 2 : Test des analytics (frontend)...")
        
        headers = {"Authorization": f"Bearer {token}"}
        
        # Test 1 : Analytics du tableau de bord
        print(f"\n🔍 Test 1 : Analytics du tableau de bord...")
        dashboard_response = requests.get(
            "http://localhost:8000/api/v1/analytics/teacher-dashboard/",
            headers=headers
        )
        
        if dashboard_response.status_code == 200:
            dashboard_data = dashboard_response.json()
            print(f"✅ Analytics tableau de bord OK !")
            print(f"   Tests: {dashboard_data['summary']['total_tests']}")
            print(f"   Classes: {dashboard_data['summary']['total_classes']}")
            print(f"   Étudiants: {dashboard_data['summary']['total_students']}")
        else:
            print(f"❌ Échec analytics tableau de bord: {dashboard_response.status_code}")
            return False
        
        # Test 2 : Analytics de performance
        print(f"\n🔍 Test 2 : Analytics de performance...")
        performance_response = requests.get(
            "http://localhost:8000/api/v1/analytics/test-performance/",
            headers=headers
        )
        
        if performance_response.status_code == 200:
            performance_data = performance_response.json()
            print(f"✅ Analytics performance OK !")
            print(f"   Tests performants: {len(performance_data['top_performing_tests'])}")
            print(f"   Progrès étudiants: {len(performance_data['student_progress'])}")
        else:
            print(f"❌ Échec analytics performance: {performance_response.status_code}")
            return False
        
        print(f"\n🎉 TOUS LES TESTS RÉUSSIS !")
        print(f"   Le frontend peut maintenant charger les analytics !")
        return True
        
    except Exception as e:
        print(f"\n❌ Erreur lors du test: {e}")
        return False

if __name__ == "__main__":
    print("🔐 Test des analytics pour le frontend")
    print("=" * 80)
    
    success = test_frontend_analytics()
    
    if success:
        print(f"\n✅ FRONTEND ANALYTICS PRÊT !")
        print(f"   Maintenant, dans le frontend :")
        print(f"   1. Rafraîchis la page")
        print(f"   2. Va sur l'onglet 'Analytics'")
        print(f"   3. Tu devrais voir de VRAIES données ! 🎉")
        print(f"   4. Plus de placeholder, plus de 'ne s'affiche rien ici' !")
    else:
        print(f"\n❌ ÉCHEC ! Vérification nécessaire")


















