#!/usr/bin/env python3
"""
Test des endpoints Analytics avec l'utilisateur marizee.dubois@najah.ai
"""

import requests

print("🧪 Test des Endpoints Analytics - Utilisateur Marizee")
print("=" * 60)

BASE_URL = "http://localhost:8000"

try:
    # Login avec l'utilisateur qui fonctionne
    print("🔑 Tentative de login avec marizee.dubois@najah.ai...")
    
    login = requests.post(f"{BASE_URL}/api/v1/auth/login", json={
        "email": "marizee.dubois@najah.ai",
        "password": "password123"
    })
    
    if login.status_code == 200:
        token = login.json().get("access_token")
        headers = {"Authorization": f"Bearer {token}"}
        print("✅ Login réussi")
        
        # Vérifier le rôle
        response = requests.get(f"{BASE_URL}/api/v1/auth/me", headers=headers)
        if response.status_code == 200:
            user_info = response.json()
            print(f"   Rôle: {user_info.get('role')}")
            print(f"   ID: {user_info.get('id')}")
        else:
            print(f"   ❌ Erreur /me: {response.status_code}")
            exit(1)
        
        # Test des endpoints analytics
        endpoints = [
            "/api/v1/analytics/class-overview",
            "/api/v1/analytics/weekly-progress",
            "/api/v1/analytics/monthly-stats",
            "/api/v1/analytics/test-performances"
        ]
        
        for endpoint in endpoints:
            print(f"\n📊 Test de {endpoint}")
            try:
                response = requests.get(f"{BASE_URL}{endpoint}", headers=headers)
                print(f"   Status: {response.status_code}")
                
                if response.status_code == 200:
                    data = response.json()
                    print(f"   ✅ Succès - Données: {type(data)}")
                    if isinstance(data, dict):
                        print(f"      Clés: {list(data.keys())}")
                    elif isinstance(data, list):
                        print(f"      Nombre d'éléments: {len(data)}")
                        if data:
                            print(f"      Premier élément: {data[0]}")
                elif response.status_code == 422:
                    print(f"   ❌ Erreur 422 - Détail:")
                    try:
                        error_detail = response.json()
                        print(f"      {error_detail}")
                    except:
                        print(f"      {response.text}")
                else:
                    print(f"   ❌ Erreur {response.status_code}: {response.text}")
                    
            except Exception as e:
                print(f"   ❌ Exception: {e}")
        
        print(f"\n🎉 Test terminé !")
        
    else:
        print(f"❌ Login échoué: {login.status_code}")
        print(f"   Détail: {login.text}")

except Exception as e:
    print(f"❌ Erreur générale: {e}")

print(f"\n🔍 Résumé:")
print(f"   - Si tous les endpoints retournent 200, les analytics sont fonctionnels")
print(f"   - Si certains endpoints retournent encore 422, il y a encore des problèmes")
print(f"   - Les données affichées seront maintenant réelles au lieu de factices")









