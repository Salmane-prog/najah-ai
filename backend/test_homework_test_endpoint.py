#!/usr/bin/env python3
"""
Test de l'endpoint homework/test sans authentification
"""

import requests
import json

def test_homework_test_endpoint():
    """Test de l'endpoint homework/test sans authentification"""
    
    print("🧪 Test de l'endpoint homework/test sans authentification")
    print("=" * 60)
    
    base_url = "http://localhost:8000/student-organization"
    headers = {
        'Content-Type': 'application/json'
    }
    
    try:
        # Test de l'endpoint de test
        print("\n1. 📋 Test de /homework/test...")
        response = requests.get(f"{base_url}/homework/test", headers=headers, timeout=5)
        
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print("✅ Endpoint de test accessible (200 OK)")
            data = response.json()
            print(f"Données reçues: {len(data)} devoir(s)")
            for hw in data:
                print(f"   - {hw.get('title', 'N/A')} ({hw.get('subject', 'N/A')}) - {hw.get('status', 'N/A')}")
        else:
            print(f"⚠️  Statut inattendu: {response.status_code}")
            print(f"Réponse: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Serveur non accessible")
    except Exception as e:
        print(f"❌ Erreur: {e}")
    
    # Test de l'endpoint normal (avec auth)
    print("\n2. 📋 Test de /homework (avec auth)...")
    try:
        response = requests.get(f"{base_url}/homework", headers=headers, timeout=5)
        print(f"Status: {response.status_code}")
        if response.status_code == 403:
            print("✅ Endpoint normal protégé correctement (403 Forbidden)")
        else:
            print(f"⚠️  Statut inattendu: {response.status_code}")
    except Exception as e:
        print(f"❌ Erreur: {e}")
    
    print("\n✅ Test terminé!")

if __name__ == "__main__":
    test_homework_test_endpoint() 