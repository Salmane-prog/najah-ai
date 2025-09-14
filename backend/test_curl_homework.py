#!/usr/bin/env python3
"""
Test simple avec requests pour vérifier l'endpoint homework
"""

import requests

def test_homework_endpoint():
    """Test de l'endpoint homework sans authentification"""
    
    print("🧪 Test de l'endpoint homework sans authentification")
    print("=" * 50)
    
    try:
        response = requests.get(
            "http://localhost:8000/student-organization/homework",
            headers={"Content-Type": "application/json"},
            timeout=5
        )
        
        print(f"Status: {response.status_code}")
        print(f"Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            print("✅ Endpoint accessible!")
            data = response.json()
            print(f"Nombre de devoirs: {len(data)}")
            for hw in data:
                print(f"   - {hw.get('title')} ({hw.get('subject')}) - {hw.get('status')}")
        else:
            print(f"❌ Erreur: {response.status_code}")
            print(f"Réponse: {response.text}")
            
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    test_homework_endpoint() 