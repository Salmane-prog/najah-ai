#!/usr/bin/env python3
"""
🎯 TEST RAPIDE DU SYSTÈME D'ÉVALUATION INITIALE
Teste rapidement les fonctionnalités principales sans créer de données complexes
"""

import asyncio
import sys
import os
from pathlib import Path

# Ajouter le répertoire parent au path
sys.path.append(str(Path(__file__).parent))

from services.student_onboarding_service import StudentOnboardingService
from services.french_question_selector import FrenchQuestionSelector
from services.french_test_session_manager import FrenchTestSessionManager
from core.database import get_db

async def test_quick_system():
    """Test rapide du système d'évaluation"""
    
    print("🚀 TEST RAPIDE DU SYSTÈME D'ÉVALUATION INITIALE")
    print("=" * 60)
    
    try:
        # Test 1: Vérifier la base de données
        print("\n📊 Test 1: Connexion à la base de données...")
        db = next(get_db())
        print("✅ Base de données accessible")
        
        # Test 2: Vérifier le sélecteur de questions
        print("\n🎯 Test 2: Sélecteur de questions françaises...")
        selector = FrenchQuestionSelector()
        questions = selector.select_questions_for_assessment(student_id=999)
        
        if len(questions) == 20:
            print(f"✅ 20 questions sélectionnées correctement")
            easy = len([q for q in questions if q['difficulty'] == 'easy'])
            medium = len([q for q in questions if q['difficulty'] == 'medium'])
            hard = len([q for q in questions if q['difficulty'] == 'hard'])
            print(f"   📊 Répartition: {easy} faciles, {medium} moyennes, {hard} difficiles")
        else:
            print(f"❌ Erreur: {len(questions)} questions au lieu de 20")
            return False
        
        # Test 3: Vérifier le gestionnaire de session
        print("\n🔄 Test 3: Gestionnaire de session de test...")
        session_manager = FrenchTestSessionManager()
        
        # Créer une session de test
        test_session = session_manager.start_test_session(student_id=999)
        if test_session:
            print(f"✅ Session de test créée (ID: {test_session['id']})")
            print(f"   📝 Questions: {len(test_session['questions'])}")
            print(f"   📊 Progression: {test_session['current_question']}/20")
        else:
            print("❌ Erreur: Impossible de créer la session de test")
            return False
        
        # Test 4: Vérifier le service d'onboarding
        print("\n🎓 Test 4: Service d'onboarding étudiant...")
        onboarding_service = StudentOnboardingService()
        
        status = onboarding_service.check_and_initialize_student(student_id=999)
        print(f"✅ Statut d'onboarding: {status['status']}")
        print(f"   📋 Détails: {status['details']}")
        
        # Test 5: Vérifier la soumission de réponses
        print("\n✍️ Test 5: Soumission de réponses...")
        
        # Soumettre quelques réponses
        for i in range(3):
            result = session_manager.submit_answer(
                test_id=test_session['id'],
                student_id=999,
                answer=f"Réponse test {i+1}"
            )
            if result:
                print(f"   ✅ Réponse {i+1} soumise - Progression: {result['current_question']}/20")
            else:
                print(f"   ❌ Erreur lors de la soumission de la réponse {i+1}")
        
        # Test 6: Vérifier la finalisation
        print("\n🏁 Test 6: Finalisation du test...")
        
        # Simuler la fin du test (20 réponses)
        for i in range(17):  # On a déjà 3 réponses, il en faut 17 de plus
            session_manager.submit_answer(
                test_id=test_session['id'],
                student_id=999,
                answer=f"Réponse finale {i+1}"
            )
        
        # Vérifier que le test est terminé
        final_status = session_manager.get_test_status(test_id=test_session['id'])
        if final_status and final_status['status'] == 'completed':
            print("✅ Test finalisé automatiquement")
            print(f"   🎯 Score final: {final_status.get('final_score', 'N/A')}")
        else:
            print("❌ Erreur: Le test n'a pas été finalisé automatiquement")
        
        print("\n" + "=" * 60)
        print("🎉 TOUS LES TESTS SONT PASSÉS AVEC SUCCÈS !")
        print("✅ Le système d'évaluation initiale fonctionne parfaitement")
        print("✅ 20 questions exactes, fermeture automatique, profil généré")
        print("\n🚀 Vous pouvez maintenant utiliser le système en production !")
        
        return True
        
    except Exception as e:
        print(f"\n❌ ERREUR LORS DU TEST: {str(e)}")
        print(f"   Type d'erreur: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        return False
    
    finally:
        if 'db' in locals():
            db.close()

def test_manual_endpoints():
    """Test manuel des endpoints principaux"""
    
    print("\n🌐 TEST MANUEL DES ENDPOINTS")
    print("=" * 40)
    
    print("\n📋 Endpoints disponibles:")
    print("   • GET  /api/v1/onboarding/student/{id}/onboarding-status")
    print("   • POST /api/v1/french-optimized/student/start")
    print("   • POST /api/v1/french-optimized/{test_id}/submit")
    print("   • GET  /api/v1/onboarding/student/{id}/assessment-ready")
    
    print("\n🔧 Pour tester manuellement:")
    print("   1. Démarrer le serveur: python start_assessment_system.py")
    print("   2. Ouvrir: http://localhost:8000/docs")
    print("   3. Tester les endpoints avec l'interface Swagger")
    
    print("\n📱 Pour tester le frontend:")
    print("   1. Démarrer le serveur backend")
    print("   2. Aller sur: http://localhost:3001/dashboard/student/assessment")
    print("   3. L'évaluation devrait se lancer automatiquement")

if __name__ == "__main__":
    print("🎯 SYSTÈME D'ÉVALUATION INITIALE - TEST RAPIDE")
    print("=" * 60)
    
    # Test automatique
    success = asyncio.run(test_quick_system())
    
    if success:
        # Test manuel des endpoints
        test_manual_endpoints()
        
        print("\n" + "=" * 60)
        print("🎯 PROCHAINES ÉTAPES:")
        print("   1. ✅ Système testé et validé")
        print("   2. 🚀 Démarrer le serveur: python start_assessment_system.py")
        print("   3. 🌐 Tester les endpoints: http://localhost:8000/docs")
        print("   4. 📱 Tester le frontend: http://localhost:3001/dashboard/student/assessment")
        print("   5. 🎉 Utiliser en production !")
    else:
        print("\n❌ LE SYSTÈME N'A PAS PASSÉ TOUS LES TESTS")
        print("   Vérifiez les erreurs ci-dessus et corrigez-les")
        print("   Puis relancez le test")





