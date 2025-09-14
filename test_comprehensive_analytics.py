#!/usr/bin/env python3
"""
Script de test complet pour les endpoints analytics incluant tous les types de tests
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
            
            # Analyse des données
            if 'datasets' in data and data['datasets']:
                print(f"📊 Nombre de points de données: {len(data['datasets'][0].get('data', []))}")
                if data['datasets'][0].get('data'):
                    scores = data['datasets'][0]['data']
                    print(f"📈 Scores: {scores}")
                    print(f"📊 Score moyen: {sum(scores) / len(scores):.1f}")
                    print(f"🎯 Score max: {max(scores)}")
                    print(f"📉 Score min: {min(scores)}")
            
        else:
            print(f"❌ Erreur: {response.text}")
            
    except Exception as e:
        print(f"❌ Exception: {e}")

def test_gamification_endpoint():
    """Test spécial pour l'endpoint de gamification"""
    print(f"\n🔍 Test de Gamification complète")
    print(f"URL: {BASE_URL}/api/v1/analytics/gamification/user-progress")
    
    try:
        response = requests.get(f"{BASE_URL}/api/v1/analytics/gamification/user-progress")
        
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Succès!")
            print(f"Données reçues: {json.dumps(data, indent=2, ensure_ascii=False)}")
            
            # Analyse des données de gamification
            if 'test_breakdown' in data:
                breakdown = data['test_breakdown']
                print(f"\n📊 Répartition des tests:")
                print(f"   📝 Quiz classiques: {breakdown.get('quiz_classic', 0)}")
                print(f"   🧠 Tests adaptatifs: {breakdown.get('adaptive_tests', 0)}")
                print(f"   🔧 Remédiations: {breakdown.get('remediation', 0)}")
                print(f"   🎯 Évaluations initiales: {breakdown.get('initial_assessments', 0)}")
            
            print(f"🏆 Niveau actuel: {data.get('level', 0)}")
            print(f"⭐ Points totaux: {data.get('total_points', 0)}")
            print(f"📈 Progression: {data.get('progress_percentage', 0):.1f}%")
            
        else:
            print(f"❌ Erreur: {response.text}")
            
    except Exception as e:
        print(f"❌ Exception: {e}")

def main():
    """Fonction principale de test"""
    print("🚀 Test complet des endpoints analytics (tous types de tests)")
    print("=" * 70)
    
    # Test des endpoints de test (sans authentification)
    test_endpoint(
        f"/api/v1/analytics/test/student/{STUDENT_ID}/performance",
        "Performance étudiant (tous types de tests)"
    )
    
    test_endpoint(
        f"/api/v1/analytics/test/student/{STUDENT_ID}/progress",
        "Progression étudiant (tous types de tests)"
    )
    
    test_endpoint(
        f"/api/v1/analytics/test/student/{STUDENT_ID}/subjects",
        "Matières étudiant (tous types de tests)"
    )
    
    # Test spécial de l'endpoint gamification
    test_gamification_endpoint()
    
    print("\n" + "=" * 70)
    print("🏁 Tests terminés!")
    
    # Vérification de la base de données
    print(f"\n📊 Vérification des données pour l'étudiant {STUDENT_ID}")
    print("Note: Ces endpoints incluent maintenant:")
    print("   📝 Quiz classiques")
    print("   🧠 Tests adaptatifs")
    print("   🔧 Remédiations")
    print("   🎯 Évaluations initiales")
    print("   📊 Tous les résultats d'évaluation")

if __name__ == "__main__":
    main()
