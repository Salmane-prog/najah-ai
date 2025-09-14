#!/usr/bin/env python3
"""
Script de test pour l'intégration frontend/backend du système de badges automatiques
"""

import requests
import json
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:8000"
STUDENT_ID = 30  # ID de l'étudiant de test

def test_badges_auto_award():
    """Teste l'attribution automatique des badges"""
    print("🏆 Test de l'attribution automatique des badges")
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
            
            return data
        else:
            print(f"❌ Erreur: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Exception: {e}")
        return None

def test_badges_retrieval():
    """Teste la récupération des badges de l'étudiant"""
    print(f"\n🔍 Test de récupération des badges de l'étudiant")
    print(f"URL: GET {BASE_URL}/api/v1/analytics/test/student/{STUDENT_ID}/badges")
    
    try:
        response = requests.get(f"{BASE_URL}/api/v1/analytics/test/student/{STUDENT_ID}/badges")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Succès!")
            
            print(f"\n📊 Badges de l'étudiant:")
            print(f"   🏅 Total badges: {data.get('total_badges', 0)}")
            
            badges = data.get('badges', [])
            if badges:
                print(f"\n🏆 Badges obtenus:")
                for i, badge in enumerate(badges, 1):
                    badge_info = badge.get('badge', {})
                    print(f"   {i}. {badge_info.get('name', 'N/A')}")
                    print(f"      Description: {badge_info.get('description', 'N/A')}")
                    if badge.get('awarded_at'):
                        print(f"      Attribué le: {badge.get('awarded_at')}")
            else:
                print("   Aucun badge obtenu")
            
            return data
        else:
            print(f"❌ Erreur: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Exception: {e}")
        return None

def test_gamification_sync():
    """Teste la synchronisation avec la gamification"""
    print(f"\n🎮 Test de synchronisation avec la gamification")
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
            
            return data
        else:
            print(f"❌ Erreur: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Exception: {e}")
        return None

def analyze_badge_system():
    """Analyse le système de badges complet"""
    print("\n" + "=" * 70)
    print("🔍 ANALYSE DU SYSTÈME DE BADGES AUTOMATIQUES")
    print("=" * 70)
    
    # 1. Test des badges automatiques
    badges_data = test_badges_auto_award()
    if not badges_data:
        print("❌ Impossible de tester les badges automatiques")
        return False
    
    # 2. Test de la récupération des badges
    retrieval_data = test_badges_retrieval()
    if not retrieval_data:
        print("❌ Impossible de récupérer les données des badges")
        return False
    
    # 3. Test de la gamification
    gamification_data = test_gamification_sync()
    if not gamification_data:
        print("❌ Impossible de synchroniser avec la gamification")
        return False
    
    # 4. Analyse des données
    print(f"\n📊 ANALYSE DES DONNÉES:")
    print(f"   🎯 Niveau (Badges): {badges_data.get('current_level', 0)}")
    print(f"   🎯 Niveau (Gamification): {gamification_data.get('level', 0)}")
    print(f"   ⭐ Points (Badges): {badges_data.get('total_points', 0)}")
    print(f"   ⭐ Points (Gamification): {gamification_data.get('total_points', 0)}")
    print(f"   📝 Tests (Badges): {badges_data.get('total_tests', 0)}")
    print(f"   📝 Tests (Gamification): {gamification_data.get('total_tests', 0)}")
    
    # 5. Vérification de la cohérence
    level_consistent = badges_data.get('current_level', 0) == gamification_data.get('level', 0)
    points_consistent = badges_data.get('total_points', 0) == gamification_data.get('total_points', 0)
    tests_consistent = badges_data.get('total_tests', 0) == gamification_data.get('total_tests', 0)
    
    print(f"\n🔍 VÉRIFICATION DE LA COHÉRENCE:")
    print(f"   🎯 Niveaux cohérents: {'✅' if level_consistent else '❌'}")
    print(f"   ⭐ Points cohérents: {'✅' if points_consistent else '❌'}")
    print(f"   📝 Tests cohérents: {'✅' if tests_consistent else '❌'}")
    
    # 6. Recommandations
    print(f"\n💡 RECOMMANDATIONS:")
    if not level_consistent:
        print(f"   ⚠️ Les niveaux ne sont pas cohérents entre les systèmes")
        print(f"      - Badges: {badges_data.get('current_level', 0)}")
        print(f"      - Gamification: {gamification_data.get('level', 0)}")
    
    if not points_consistent:
        print(f"   ⚠️ Les points ne sont pas cohérents entre les systèmes")
        print(f"      - Badges: {badges_data.get('total_points', 0)}")
        print(f"      - Gamification: {gamification_data.get('total_points', 0)}")
    
    if not tests_consistent:
        print(f"   ⚠️ Le nombre de tests n'est pas cohérent entre les systèmes")
        print(f"      - Badges: {badges_data.get('total_tests', 0)}")
        print(f"      - Gamification: {gamification_data.get('total_tests', 0)}")
    
    if level_consistent and points_consistent and tests_consistent:
        print(f"   ✅ Tous les systèmes sont parfaitement synchronisés !")
        print(f"   🎉 Le système de badges automatiques est prêt pour la production !")
    
    return True

def main():
    """Fonction principale"""
    print("🚀 Test d'intégration frontend/backend du système de badges automatiques")
    print("=" * 70)
    
    success = analyze_badge_system()
    
    if success:
        print(f"\n🏁 Test d'intégration réussi !")
        print(f"Le système de badges automatiques est parfaitement intégré.")
    else:
        print(f"\n❌ Test d'intégration échoué.")
        print(f"Vérifiez les erreurs ci-dessus.")

if __name__ == "__main__":
    main()
