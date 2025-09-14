#!/usr/bin/env python3
"""
Test de compatibilité frontend pour l'endpoint homework
"""

import requests
import json

def test_frontend_compatibility():
    """Test de compatibilité avec les appels frontend"""
    
    print("🧪 Test de compatibilité frontend")
    print("=" * 40)
    
    # Simuler un appel frontend sans token
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    
    try:
        # Test de l'endpoint homework
        response = requests.get(
            "http://localhost:8000/student-organization/homework",
            headers=headers,
            timeout=5
        )
        
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Endpoint compatible avec le frontend!")
            data = response.json()
            print(f"Données reçues: {len(data)} devoir(s)")
            
            # Vérifier la structure des données
            if data and len(data) > 0:
                first_homework = data[0]
                required_fields = ['id', 'title', 'subject', 'status', 'due_date']
                missing_fields = [field for field in required_fields if field not in first_homework]
                
                if missing_fields:
                    print(f"⚠️  Champs manquants: {missing_fields}")
                else:
                    print("✅ Structure des données correcte")
                    print(f"   Exemple: {first_homework['title']} ({first_homework['subject']})")
        else:
            print(f"❌ Erreur: {response.status_code}")
            print(f"Réponse: {response.text}")
            
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    test_frontend_compatibility() 