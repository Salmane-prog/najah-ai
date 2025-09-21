#!/usr/bin/env python3
import requests
import json

# Configuration
BASE_URL = "http://localhost:8000/api/v1"

def test_endpoint_sans_auth(endpoint, name):
    try:
        print(f"\n{'='*60}")
        print(f"🔍 TESTING SANS AUTH: {name}")
        print(f"📡 Endpoint: {endpoint}")
        
        response = requests.get(f"{BASE_URL}{endpoint}")
        print(f"📊 Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ DONNÉES RECUES:")
            print(f"📋 Type: {type(data)}")
            print(f"🔍 Contenu:")
            print(json.dumps(data, indent=2, ensure_ascii=False))
        elif response.status_code == 401:
            print(f"🔒 401 Unauthorized (attendu)")
        elif response.status_code == 403:
            print(f"🚫 403 Forbidden (attendu)")
        else:
            print(f"❌ Erreur: {response.text}")
            
    except Exception as e:
        print(f"❌ Exception: {e}")

def main():
    print("🚀 TEST DES ENDPOINTS SANS AUTHENTIFICATION")
    print("="*60)
    
    endpoints = [
        ("/analytics/class-overview", "Class Overview"),
        ("/analytics/weekly-progress", "Weekly Progress"),
        ("/analytics/monthly-stats", "Monthly Stats"),
        ("/analytics/student-performances", "Student Performances"),
        ("/analytics/test-performances", "Test Performances")
    ]
    
    for endpoint, name in endpoints:
        test_endpoint_sans_auth(endpoint, name)
    
    print(f"\n{'='*60}")
    print("🎯 TEST TERMINÉ")
    print("="*60)

if __name__ == "__main__":
    main()









