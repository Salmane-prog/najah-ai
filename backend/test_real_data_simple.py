#!/usr/bin/env python3
"""
Script de test simplifié pour vérifier les données réelles
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_real_data():
    """Tester si les endpoints utilisent des données réelles."""
    
    # Se connecter
    login_data = {
        "email": "marie.dubois@najah.ai",
        "password": "salmane123@"
    }
    
    try:
        print("🔐 Tentative de connexion...")
        response = requests.post(f"{BASE_URL}/api/v1/auth/login", json=login_data)
        print(f"Status de connexion: {response.status_code}")
        
        if response.status_code != 200:
            print("❌ Échec de connexion")
            print(f"Réponse: {response.text}")
            return False
        
        data = response.json()
        token = data.get("access_token")
        print("✅ Connexion réussie")
        
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        # Tester les endpoints principaux
        endpoints = [
            "/api/v1/users/?role=student",
            "/api/v1/badges/",
            "/api/v1/analytics/dashboard/overview",
            "/api/v1/gamification/leaderboard?leaderboard_type=global"
        ]
        
        real_data_count = 0
        
        for endpoint in endpoints:
            try:
                response = requests.get(f"{BASE_URL}{endpoint}", headers=headers)
                print(f"\n🔍 Test: {endpoint}")
                print(f"Status: {response.status_code}")
                
                if response.status_code == 200:
                    data = response.json()
                    data_str = json.dumps(data, default=str).lower()
                    
                    # Vérifier les patterns de données mockées
                    mock_patterns = ["alice", "bob", "charlie", "diana", "eve", "demo", "mock", "fake"]
                    has_mock_data = any(pattern in data_str for pattern in mock_patterns)
                    
                    if has_mock_data:
                        print("⚠️ Données mockées détectées")
                    else:
                        print("✅ Données réelles détectées")
                        real_data_count += 1
                else:
                    print(f"❌ Erreur: {response.status_code}")
                    print(f"Réponse: {response.text}")
                    
            except Exception as e:
                print(f"❌ Erreur: {e}")
        
        print(f"\n📊 Résumé: {real_data_count}/{len(endpoints)} endpoints avec données réelles")
        
        if real_data_count == len(endpoints):
            print("🎉 Tous les endpoints utilisent des données réelles !")
            return True
        else:
            print("⚠️ Certains endpoints utilisent encore des données mockées")
            return False
            
    except Exception as e:
        print(f"❌ Erreur générale: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Test des données réelles")
    print("=" * 30)
    test_real_data() 