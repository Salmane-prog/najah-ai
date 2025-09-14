#!/usr/bin/env python3
"""
Script de test pour les nouveaux endpoints analytics des étudiants
"""

import requests
import json
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:8000"
STUDENT_ID = 30  # ID de l'étudiant de test

def test_endpoint(endpoint, description):
    """Teste un endpoint et affiche le résultat"""
    print(f"\n🔍 Test de {description}")
    print(f"URL: {BASE_URL}{endpoint}")
    
    try:
        response = requests.get(f"{BASE_URL}{endpoint}")
        
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Succès!")
            print(f"Données reçues: {json.dumps(data, indent=2, ensure_ascii=False)}")
        else:
            print(f"❌ Erreur: {response.text}")
            
    except Exception as e:
        print(f"❌ Exception: {e}")

def main():
    """Fonction principale de test"""
    print("🚀 Test des nouveaux endpoints analytics des étudiants")
    print("=" * 60)
    
    # Test des endpoints de test (sans authentification)
    test_endpoint(
        f"/api/v1/analytics/test/student/{STUDENT_ID}/performance",
        "Performance étudiant (test)"
    )
    
    test_endpoint(
        f"/api/v1/analytics/test/student/{STUDENT_ID}/progress",
        "Progression étudiant (test)"
    )
    
    test_endpoint(
        f"/api/v1/analytics/test/student/{STUDENT_ID}/subjects",
        "Matières étudiant (test)"
    )
    
    # Test de l'endpoint gamification
    test_endpoint(
        "/api/v1/analytics/gamification/user-progress",
        "Gamification utilisateur (test)"
    )
    
    print("\n" + "=" * 60)
    print("🏁 Tests terminés!")
    
    # Vérification de la base de données
    print(f"\n📊 Vérification des données pour l'étudiant {STUDENT_ID}")
    print("Note: Ces endpoints nécessitent des données dans la base pour fonctionner correctement")

if __name__ == "__main__":
    main()
