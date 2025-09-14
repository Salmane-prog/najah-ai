#!/usr/bin/env python3
import requests

print("Test final...")
BASE_URL = "http://localhost:8000"

try:
    # Login
    login = requests.post(f"{BASE_URL}/api/v1/auth/login", json={
        "email": "marizee.dubois@najah.ai",
        "password": "password123"
    })
    
    if login.status_code == 200:
        token = login.json().get("access_token")
        headers = {"Authorization": f"Bearer {token}"}
        print("✅ Login OK")
        
        # Test endpoint
        response = requests.get(f"{BASE_URL}/api/v1/teacher-dashboard/students", headers=headers)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            students = data.get('students', [])
            print(f"✅ {len(students)} étudiants")
            
            # Check duplicates
            ids = [s.get('id') for s in students]
            unique = set(ids)
            print(f"IDs uniques: {len(unique)} sur {len(ids)}")
            
            if len(unique) == len(ids):
                print("🎉 Pas de doublons!")
            else:
                print("❌ Doublons détectés")
                
        else:
            print(f"❌ Erreur {response.status_code}")
    else:
        print(f"❌ Login échoué: {login.status_code}")
        
except Exception as e:
    print(f"❌ Erreur: {e}")






