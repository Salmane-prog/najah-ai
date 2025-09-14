#!/usr/bin/env python3
"""
Test simple de l'endpoint homework
"""

import requests

def test_simple_homework():
    """Test simple de l'endpoint homework"""
    
    print("🧪 Test simple de l'endpoint homework")
    print("=" * 40)
    
    try:
        # Test de l'endpoint
        response = requests.get("http://localhost:8000/student-organization/homework", timeout=5)
        
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print("✅ Endpoint accessible!")
            data = response.json()
            print(f"Nombre de devoirs: {len(data)}")
            for hw in data:
                print(f"   - {hw.get('title')} ({hw.get('subject')})")
        else:
            print(f"❌ Erreur: {response.status_code}")
            print(f"Réponse: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Serveur non accessible")
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    test_simple_homework() 