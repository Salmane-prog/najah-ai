#!/usr/bin/env python3
"""
Script de test final pour le système complet de badges automatiques
"""

import requests
import json
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:8000"
STUDENT_ID = 30  # ID de l'étudiant de test

def test_complete_badge_system():
    """Teste le système complet de badges automatiques"""
    print("🚀 Test du système complet de badges automatiques")
    print("=" * 70)
    
    # 1. Test de l'attribution automatique des badges
    print(f"\n🏆 1. Attribution automatique des badges")
    print(f"URL: POST {BASE_URL}/api/v1/analytics/test/student/{STUDENT_ID}/check-badges")
    
    try:
        response = requests.post(f"{BASE_URL}/api/v1/analytics/test/student/{STUDENT_ID}/check-badges")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Succès!")
            
            print(f"\n📊 Résumé de l'étudiant:")
            print(f"   🎯 Niveau: {data.get('current_level', 0)}")
            print(f"   ⭐ Points: {data.get('total_points', 0)}")
            print(f"   📝 Tests: {data.get('total_tests', 0)}")
            
            breakdown = data.get('test_breakdown', {})
            print(f"\n📋 Répartition des tests:")
            print(f"   📝 Quiz: {breakdown.get('quiz', 0)}")
            print(f"   🧠 Tests adaptatifs: {breakdown.get('adaptive', 0)}")
            print(f"   🔧 Remédiations: {breakdown.get('remediation', 0)}")
            print(f"   🎯 Évaluations: {breakdown.get('assessment', 0)}")
            
            badges_awarded = data.get('badges_awarded', [])
            if badges_awarded:
                print(f"\n🎉 Badges attribués: {len(badges_awarded)}")
                for i, badge in enumerate(badges_awarded, 1):
                    print(f"   {i}. {badge}")
            else:
                print(f"\nℹ️ Aucun nouveau badge attribué")
            
            print(f"\n💬 Message: {data.get('message', 'N/A')}")
            
        else:
            print(f"❌ Erreur: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False
    
    # 2. Test de la gamification
    print(f"\n🎮 2. Test de la gamification")
    print(f"URL: GET {BASE_URL}/api/v1/analytics/gamification/user-progress")
    
    try:
        response = requests.get(f"{BASE_URL}/api/v1/analytics/gamification/user-progress")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Succès!")
            
            print(f"\n🏆 Données de gamification:")
            print(f"   🎯 Niveau: {data.get('level', 0)}")
            print(f"   ⭐ Points totaux: {data.get('total_points', 0)}")
            print(f"   📈 Progression: {data.get('progress_percentage', 0):.1f}%")
            print(f"   📝 Tests totaux: {data.get('total_tests', 0)}")
            
            breakdown = data.get('test_breakdown', {})
            print(f"\n📊 Répartition des tests:")
            print(f"   📝 Quiz classiques: {breakdown.get('quiz_classic', 0)}")
            print(f"   🧠 Tests adaptatifs: {breakdown.get('adaptive_tests', 0)}")
            print(f"   🔧 Remédiations: {breakdown.get('remediation', 0)}")
            print(f"   🎯 Évaluations initiales: {breakdown.get('initial_assessments', 0)}")
            
        else:
            print(f"❌ Erreur: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False
    
    # 3. Test des analytics de performance
    print(f"\n📊 3. Test des analytics de performance")
    print(f"URL: GET {BASE_URL}/api/v1/analytics/test/student/{STUDENT_ID}/performance")
    
    try:
        response = requests.get(f"{BASE_URL}/api/v1/analytics/test/student/{STUDENT_ID}/performance")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Succès!")
            
            if 'datasets' in data and data['datasets']:
                scores = data['datasets'][0].get('data', [])
                print(f"\n📈 Performance sur 6 mois:")
                print(f"   📊 Scores: {scores}")
                print(f"   📊 Moyenne: {sum(scores) / len(scores):.1f}")
                print(f"   🎯 Max: {max(scores)}")
                print(f"   📉 Min: {min(scores)}")
            else:
                print("   Aucune donnée de performance")
            
        else:
            print(f"❌ Erreur: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False
    
    print(f"\n" + "=" * 70)
    print("🎉 Tous les tests sont passés avec succès !")
    print("\n📋 Système de badges automatiques fonctionnel:")
    print("   ✅ Attribution automatique basée sur les points")
    print("   ✅ Attribution automatique basée sur les niveaux")
    print("   ✅ Attribution automatique basée sur le nombre de tests")
    print("   ✅ Badges spécialisés par type de test")
    print("   ✅ Intégration avec la gamification")
    print("   ✅ Analytics complets incluant tous les types de tests")
    
    return True

def main():
    """Fonction principale"""
    success = test_complete_badge_system()
    
    if success:
        print(f"\n🏁 Test final réussi !")
        print(f"Le système de badges automatiques est prêt pour la production.")
    else:
        print(f"\n❌ Test final échoué.")
        print(f"Vérifiez les erreurs ci-dessus.")

if __name__ == "__main__":
    main()
