#!/usr/bin/env python3
"""
Script pour tester le token généré
"""

import requests
import json

# Configuration
BASE_URL = "http://localhost:8000"
TEST_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZWFjaGVyQGV4YW1wbGUuY29tIiwicm9sZSI6InRlYWNoZXIiLCJleHAiOjE3NTgwNzM5NTIsImlhdCI6MTc1NTQ4MTk1Mn0.VMZzGZ6G9taBlXwqtU0Y_wpml1c-guYCS4fCYB8vBkw"

def test_generate_evaluation():
    """Test de l'endpoint de génération d'évaluation avec le token valide"""
    
    print("🧪 Test de l'endpoint de génération d'évaluation...")
    
    headers = {
        "Authorization": f"Bearer {TEST_TOKEN}",
        "Content-Type": "application/json"
    }
    
    # Données de test
    test_data = {
        "title": "Test d'évaluation",
        "subject": "Mathématiques",
        "assessment_type": "project",
        "description": "Test de génération d'évaluation formative",
        "target_level": "intermediate",
        "duration_minutes": 60,
        "max_students": 30,
        "learning_objectives": ["Compétence 1", "Compétence 2"],
        "custom_requirements": "Aucune"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/v1/ai-formative-evaluations/generate-evaluation/",
            headers=headers,
            json=test_data
        )
        
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("✅ SUCCÈS ! L'endpoint fonctionne avec le token valide.")
        else:
            print("❌ ÉCHEC ! L'endpoint ne fonctionne pas.")
            
    except Exception as e:
        print(f"❌ Erreur: {e}")

def test_available_types():
    """Test de l'endpoint des types disponibles avec le token valide"""
    
    print("\n🧪 Test de l'endpoint des types disponibles...")
    
    headers = {
        "Authorization": f"Bearer {TEST_TOKEN}"
    }
    
    try:
        response = requests.get(
            f"{BASE_URL}/api/v1/ai-formative-evaluations/available-types/",
            headers=headers
        )
        
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("✅ SUCCÈS ! L'endpoint des types fonctionne.")
        else:
            print("❌ ÉCHEC ! L'endpoint des types ne fonctionne pas.")
            
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    print("🔐 Test du token de test pour l'API formative evaluations")
    print("=" * 70)
    
    test_generate_evaluation()
    test_available_types()
    
    print("\n✅ Tests terminés")









