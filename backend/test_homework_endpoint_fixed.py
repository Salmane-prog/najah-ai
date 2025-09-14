#!/usr/bin/env python3
"""
Test de l'endpoint homework corrigé
"""

import requests
import json

def test_homework_endpoint_fixed():
    """Test de l'endpoint homework avec le nouveau router_no_prefix"""
    
    print("🧪 Test de l'endpoint homework corrigé")
    print("=" * 50)
    
    base_urls = [
        "http://localhost:8000/api/v1/student-organization",  # Avec prefix complet
        "http://localhost:8000/student-organization"         # Sans prefix (nouveau)
    ]
    
    headers = {
        'Content-Type': 'application/json'
    }
    
    for i, base_url in enumerate(base_urls, 1):
        print(f"\n{i}. 📋 Test de {base_url}/homework...")
        
        try:
            response = requests.get(f"{base_url}/homework", headers=headers, timeout=5)
            
            print(f"Status: {response.status_code}")
            if response.status_code == 403:
                print("✅ Endpoint protégé correctement (403 Forbidden)")
            elif response.status_code == 200:
                print("✅ Endpoint accessible (200 OK)")
                data = response.json()
                print(f"Données reçues: {len(data) if isinstance(data, list) else 'non-liste'}")
            else:
                print(f"⚠️  Statut inattendu: {response.status_code}")
                print(f"Réponse: {response.text}")
                
        except requests.exceptions.ConnectionError:
            print("❌ Serveur non accessible")
        except Exception as e:
            print(f"❌ Erreur: {e}")
    
    # Test avec OPTIONS (preflight CORS)
    print(f"\n3. 🔍 Test OPTIONS pour CORS...")
    try:
        response = requests.options("http://localhost:8000/student-organization/homework", headers=headers, timeout=5)
        print(f"OPTIONS Status: {response.status_code}")
        if response.status_code == 200:
            print("✅ CORS preflight OK")
        else:
            print(f"⚠️  CORS preflight: {response.status_code}")
    except Exception as e:
        print(f"❌ Erreur CORS: {e}")
    
    print("\n✅ Test terminé!")

if __name__ == "__main__":
    test_homework_endpoint_fixed()