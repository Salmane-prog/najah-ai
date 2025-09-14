#!/usr/bin/env python3
"""
Script pour tester l'API assessment
"""

import requests
import json

print("=== TEST API ASSESSMENT ===")

# URL de base
base_url = "http://localhost:8000"

# Token de test (copié depuis les logs)
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJoYWpvdWppczQ3QGdtYWlsLmNvbSIsInJvbGUiOiJzdHVkZW50IiwiZXhwIjoxNzUzMjkwODkwfQ.GRJUO_bCrQOY86Fljp6qxT8VF9e3_Yn2SJcZ_i6xL_s"

# Headers
headers = {
    'Authorization': f'Bearer {token}',
    'Content-Type': 'application/json'
}

# Test 1: Endpoint de test
print("\n🧪 Test 1: Endpoint simple")
try:
    response = requests.get(f"{base_url}/api/v1/assessment/test", headers=headers)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Erreur: {e}")

# Test 2: Endpoint principal
print("\n🧪 Test 2: Endpoint assessment")
try:
    response = requests.get(f"{base_url}/api/v1/assessment/student/5/start", headers=headers)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"\n📊 Données reçues:")
        print(f"  - ID: {data.get('id')}")
        print(f"  - Title: {data.get('title')}")
        print(f"  - Status: {data.get('status')}")
        print(f"  - Questions: {len(data.get('questions', []))}")
        
        if data.get('questions'):
            for i, q in enumerate(data['questions']):
                print(f"    Question {i+1}: {q.get('question_text', '')[:50]}...")
    
except Exception as e:
    print(f"Erreur: {e}")

print("\n✅ Test terminé") 