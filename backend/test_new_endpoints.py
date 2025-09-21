#!/usr/bin/env python3
"""
Script de test pour tous les nouveaux endpoints de test
"""

import requests
import json
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:8000"
STUDENT_ID = 5  # ID de l'étudiant de test

def test_endpoint(url, description):
    """Teste un endpoint et affiche le résultat"""
    print(f"\n🧪 Test: {description}")
    print(f"URL: {url}")
    
    try:
        response = requests.get(url)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Succès!")
            print(f"Données reçues: {len(str(data))} caractères")
            
            # Afficher un aperçu des données
            if isinstance(data, dict):
                for key, value in data.items():
                    if isinstance(value, list):
                        print(f"  {key}: {len(value)} éléments")
                    elif isinstance(value, dict):
                        print(f"  {key}: {len(value)} clés")
                    else:
                        print(f"  {key}: {value}")
            elif isinstance(data, list):
                print(f"  Liste de {len(data)} éléments")
            else:
                print(f"  Données: {type(data)}")
                
        else:
            print(f"❌ Erreur: {response.text}")
            
    except Exception as e:
        print(f"❌ Exception: {e}")

def main():
    """Teste tous les endpoints"""
    print("🚀 Test des nouveaux endpoints de test")
    print("=" * 50)
    
    # Test des quiz assignés
    test_endpoint(
        f"{BASE_URL}/api/v1/quiz_assignments/student/{STUDENT_ID}",
        "Quiz assignés à l'étudiant"
    )
    
    # Test des analytics étudiant
    test_endpoint(
        f"{BASE_URL}/api/v1/student_analytics/student/{STUDENT_ID}",
        "Analytics de l'étudiant"
    )
    
    # Test du calendrier
    test_endpoint(
        f"{BASE_URL}/api/v1/calendar/user/{STUDENT_ID}/events",
        "Événements du calendrier"
    )
    
    # Test des quiz étudiant
    test_endpoint(
        f"{BASE_URL}/api/v1/student_quizzes/student/{STUDENT_ID}",
        "Quiz de l'étudiant"
    )
    
    # Test des performances
    test_endpoint(
        f"{BASE_URL}/api/v1/student_quizzes/student/{STUDENT_ID}/performance",
        "Performances de l'étudiant"
    )
    
    # Test des recommandations
    test_endpoint(
        f"{BASE_URL}/api/v1/student_quizzes/student/{STUDENT_ID}/recommendations",
        "Recommandations de quiz"
    )
    
    print("\n" + "=" * 50)
    print("✅ Tests terminés!")

if __name__ == "__main__":
    main()













