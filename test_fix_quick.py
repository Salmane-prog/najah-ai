#!/usr/bin/env python3
"""
Test rapide de la correction du routage teacher-dashboard
"""

import requests

def test_quick_fix():
    """Test rapide après correction"""
    print("🧪 Test rapide après correction du routage")
    print("=" * 50)
    
    BASE_URL = "http://localhost:8000"
    
    # Test de l'endpoint students
    print("\n1️⃣ Test de l'endpoint /api/v1/teacher-dashboard/students...")
    try:
        response = requests.get(f"{BASE_URL}/api/v1/teacher-dashboard/students", timeout=5)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Endpoint accessible ! Correction réussie !")
            return True
        elif response.status_code == 401:
            print("✅ Endpoint accessible mais authentification requise (normal)")
            return True
        elif response.status_code == 404:
            print("❌ Endpoint toujours 404 - Correction échouée")
            return False
        else:
            print(f"⚠️ Status inattendu: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

if __name__ == "__main__":
    success = test_quick_fix()
    if success:
        print("\n🎉 La correction semble fonctionner !")
        print("💡 Redémarrez le serveur backend pour appliquer les changements")
    else:
        print("\n💥 La correction n'a pas fonctionné")
        print("💡 Vérifiez la configuration des routes")






