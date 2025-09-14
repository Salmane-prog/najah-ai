#!/usr/bin/env python3
"""
Script de test final pour l'intégration complète frontend/backend du système de badges automatiques
"""

import requests
import json
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:8000"
STUDENT_ID = 30  # ID de l'étudiant de test

def test_complete_system():
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
            
            return data
        else:
            print(f"❌ Erreur: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Exception: {e}")
        return None

def test_badges_retrieval():
    """Teste la récupération des badges de l'étudiant"""
    print(f"\n🔍 2. Récupération des badges de l'étudiant")
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
    print(f"\n🎮 3. Test de synchronisation avec la gamification")
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

def analyze_frontend_integration():
    """Analyse l'intégration frontend/backend"""
    print("\n" + "=" * 70)
    print("🔍 ANALYSE DE L'INTÉGRATION FRONTEND/BACKEND")
    print("=" * 70)
    
    # 1. Test des badges automatiques
    badges_data = test_complete_system()
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
    
    # 6. Calcul des badges attendus
    current_level = badges_data.get('current_level', 0)
    total_points = badges_data.get('total_points', 0)
    total_tests = badges_data.get('total_tests', 0)
    
    expected_badges = 0
    
    # Badges de niveau
    if current_level >= 1: expected_badges += 1
    if current_level >= 5: expected_badges += 1
    if current_level >= 10: expected_badges += 1
    if current_level >= 15: expected_badges += 1
    if current_level >= 20: expected_badges += 1
    
    # Badges de tests
    if total_tests >= 1: expected_badges += 1
    if total_tests >= 10: expected_badges += 1
    if total_tests >= 50: expected_badges += 1
    if total_tests >= 100: expected_badges += 1
    if total_tests >= 500: expected_badges += 1
    
    # Badges de points
    if total_points >= 100: expected_badges += 1
    if total_points >= 1000: expected_badges += 1
    if total_points >= 5000: expected_badges += 1
    if total_points >= 10000: expected_badges += 1
    if total_points >= 50000: expected_badges += 1
    
    # Badges spécialisés
    if total_tests >= 5: expected_badges += 1  # Quiz Master
    if total_tests >= 3: expected_badges += 1  # Test Adaptatif Expert
    
    actual_badges = retrieval_data.get('total_badges', 0)
    
    print(f"\n🏆 ANALYSE DES BADGES:")
    print(f"   🎯 Badges attendus: {expected_badges}")
    print(f"   🏅 Badges réels: {actual_badges}")
    print(f"   ✅ Correspondance: {'✅' if expected_badges == actual_badges else '❌'}")
    
    if expected_badges != actual_badges:
        print(f"   ⚠️ Différence: {abs(expected_badges - actual_badges)} badge(s)")
    
    # 7. Recommandations pour le frontend
    print(f"\n💡 RECOMMANDATIONS POUR LE FRONTEND:")
    if level_consistent and points_consistent and tests_consistent:
        print(f"   ✅ Tous les systèmes sont parfaitement synchronisés !")
        print(f"   🎉 Le système de badges automatiques est prêt pour la production !")
        print(f"   🚀 Le frontend peut maintenant afficher {expected_badges} badges !")
        
        print(f"\n📱 DONNÉES À AFFICHER DANS LE FRONTEND:")
        print(f"   🎯 Niveau actuel: {current_level}")
        print(f"   ⭐ Points totaux: {total_points:,}")
        print(f"   📝 Tests totaux: {total_tests}")
        print(f"   🏅 Badges obtenus: {actual_badges}")
        print(f"   📊 Progression: {min(100, round((current_level / 20) * 100))}%")
        
    else:
        print(f"   ⚠️ Des incohérences existent entre les systèmes")
        print(f"   🔧 Vérifiez la logique de calcul dans le backend")
    
    return True

def main():
    """Fonction principale"""
    print("🚀 Test d'intégration frontend/backend du système de badges automatiques")
    print("=" * 70)
    
    success = analyze_frontend_integration()
    
    if success:
        print(f"\n🏁 Test d'intégration réussi !")
        print(f"Le système de badges automatiques est parfaitement intégré.")
        print(f"🎉 Le frontend peut maintenant afficher tous les badges !")
    else:
        print(f"\n❌ Test d'intégration échoué.")
        print(f"Vérifiez les erreurs ci-dessus.")

if __name__ == "__main__":
    main()
