#!/usr/bin/env python3
"""
Script de test pour le système de badges automatiques
"""

import requests
import json
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:8000"
STUDENT_ID = 30  # ID de l'étudiant de test

def test_auto_badges():
    """Teste l'attribution automatique des badges"""
    print(f"\n🏆 Test du système de badges automatiques")
    print(f"URL: {BASE_URL}/api/v1/analytics/test/student/{STUDENT_ID}/check-badges")
    
    try:
        response = requests.post(f"{BASE_URL}/api/v1/analytics/test/student/{STUDENT_ID}/check-badges")
        
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Succès!")
            print(f"Données reçues: {json.dumps(data, indent=2, ensure_ascii=False)}")
            
            # Analyse des résultats
            print(f"\n📊 Résumé des badges:")
            print(f"   🎯 Niveau actuel: {data.get('current_level', 0)}")
            print(f"   ⭐ Points totaux: {data.get('total_points', 0)}")
            print(f"   📝 Tests totaux: {data.get('total_tests', 0)}")
            
            breakdown = data.get('test_breakdown', {})
            print(f"\n📋 Répartition des tests:")
            print(f"   📝 Quiz: {breakdown.get('quiz', 0)}")
            print(f"   🧠 Tests adaptatifs: {breakdown.get('adaptive', 0)}")
            print(f"   🔧 Remédiations: {breakdown.get('remediation', 0)}")
            print(f"   🎯 Évaluations: {breakdown.get('assessment', 0)}")
            
            badges_awarded = data.get('badges_awarded', [])
            if badges_awarded:
                print(f"\n🎉 Nouveaux badges attribués:")
                for badge in badges_awarded:
                    print(f"   🏅 {badge}")
            else:
                print(f"\nℹ️ Aucun nouveau badge attribué")
            
            print(f"\n💬 Message: {data.get('message', 'N/A')}")
            
        else:
            print(f"❌ Erreur: {response.text}")
            
    except Exception as e:
        print(f"❌ Exception: {e}")

def test_existing_badges():
    """Teste la récupération des badges existants"""
    print(f"\n🔍 Test de récupération des badges existants")
    print(f"URL: {BASE_URL}/api/v1/badges/user/{STUDENT_ID}")
    
    try:
        response = requests.get(f"{BASE_URL}/api/v1/badges/user/{STUDENT_ID}")
        
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Succès!")
            print(f"Nombre de badges: {len(data)}")
            
            if data:
                print(f"\n🏅 Badges de l'étudiant:")
                for badge in data:
                    badge_info = badge.get('badge', {})
                    print(f"   - {badge_info.get('name', 'N/A')}: {badge_info.get('description', 'N/A')}")
                    if badge.get('awarded_at'):
                        print(f"     Attribué le: {badge.get('awarded_at')}")
            else:
                print("   Aucun badge attribué")
            
        else:
            print(f"❌ Erreur: {response.text}")
            
    except Exception as e:
        print(f"❌ Exception: {e}")

def main():
    """Fonction principale de test"""
    print("🚀 Test du système de badges automatiques")
    print("=" * 60)
    
    # Test de l'attribution automatique
    test_auto_badges()
    
    # Test de la récupération des badges existants
    test_existing_badges()
    
    print("\n" + "=" * 60)
    print("🏁 Tests terminés!")
    
    print(f"\n📋 Types de badges automatiques:")
    print("   🎯 Badges de niveau (1, 5, 10, 15, 20)")
    print("   📝 Badges de tests (1, 10, 50, 100, 500)")
    print("   ⭐ Badges de points (100, 1000, 5000, 10000, 50000)")
    print("   🏆 Badges spécialisés (Quiz Master, Test Adaptatif Expert)")

if __name__ == "__main__":
    main()
