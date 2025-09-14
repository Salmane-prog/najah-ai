#!/usr/bin/env python3
"""
Simulation des appels API frontend pour vérifier la compatibilité
"""

import requests
import json

def simulate_frontend_api_calls():
    """Simuler les appels API du frontend"""
    
    print("🧪 Simulation des appels API frontend")
    print("=" * 45)
    
    base_url = "http://localhost:8000/student-organization"
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    
    # Test 1: GET /homework (comme HomeworkWidget)
    print("\n1. 📋 Test GET /homework (HomeworkWidget)")
    try:
        response = requests.get(f"{base_url}/homework", headers=headers, timeout=5)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Succès! {len(data)} devoir(s) récupéré(s)")
            for i, hw in enumerate(data[:2]):  # Afficher les 2 premiers
                print(f"   {i+1}. {hw.get('title')} ({hw.get('subject')}) - {hw.get('status')}")
        else:
            print(f"❌ Erreur: {response.status_code}")
            print(f"Réponse: {response.text}")
    except Exception as e:
        print(f"❌ Erreur: {e}")
    
    # Test 2: GET /homework?status_filter=pending (comme CalendarWidget)
    print("\n2. 📅 Test GET /homework?status_filter=pending (CalendarWidget)")
    try:
        response = requests.get(f"{base_url}/homework?status_filter=pending", headers=headers, timeout=5)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Succès! {len(data)} devoir(s) en attente")
            for i, hw in enumerate(data[:2]):
                print(f"   {i+1}. {hw.get('title')} - Échéance: {hw.get('due_date')}")
        else:
            print(f"❌ Erreur: {response.status_code}")
            print(f"Réponse: {response.text}")
    except Exception as e:
        print(f"❌ Erreur: {e}")
    
    # Test 3: PUT /homework/{id}/complete (comme bouton "Terminer")
    print("\n3. ✅ Test PUT /homework/2/complete (Bouton Terminer)")
    try:
        response = requests.put(f"{base_url}/homework/2/complete", headers=headers, timeout=5)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Devoir marqué comme terminé!")
        elif response.status_code == 403:
            print("⚠️  Authentification requise (normal)")
        else:
            print(f"❌ Erreur: {response.status_code}")
            print(f"Réponse: {response.text}")
    except Exception as e:
        print(f"❌ Erreur: {e}")
    
    print("\n✅ Tests terminés!")

if __name__ == "__main__":
    simulate_frontend_api_calls() 