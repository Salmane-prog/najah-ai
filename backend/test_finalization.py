#!/usr/bin/env python3
"""
🧪 TEST DE FINALISATION DU TEST
Vérifie que le test se termine correctement après 20 questions
et que le profil est bien généré
"""

import sys
import os
from pathlib import Path

# Ajouter le répertoire parent au path
sys.path.append(str(Path(__file__).parent))

from services.french_test_session_manager import FrenchTestSessionManager
from services.french_question_selector import FrenchQuestionSelector
from core.database import get_db

def test_test_finalization():
    """Tester la finalisation complète du test"""
    
    print("🧪 TEST DE FINALISATION DU TEST")
    print("=" * 50)
    
    try:
        db = next(get_db())
        
        # Test 1: Démarrer une session de test
        print("\n📋 Test 1: Démarrage d'une session de test...")
        session_manager = FrenchTestSessionManager(db)
        
        test_session = session_manager.start_test_session(student_id=999)
        print(f"✅ Session démarrée: {test_session['test_id']}")
        print(f"   Status: {test_session['status']}")
        print(f"   Question actuelle: {test_session['progress']['current']}/20")
        
        # Test 2: Simuler les 20 questions
        print("\n📝 Test 2: Simulation des 20 questions...")
        
        test_id = test_session['test_id']
        questions_sequence = test_session['questions_sequence']
        
        for question_num in range(1, 21):
            print(f"   Question {question_num}/20...")
            
            # Récupérer la question actuelle
            current_question_id = questions_sequence[question_num - 1]
            current_question = session_manager._get_question_by_id(current_question_id)
            
            if not current_question:
                print(f"❌ Question {question_num} non trouvée")
                return False
            
            # Soumettre une réponse (toujours correcte pour ce test)
            result = session_manager.submit_answer(
                test_id=test_id,
                student_id=999,
                answer=current_question['correct']
            )
            
            print(f"      Réponse soumise: {result['status']}")
            
            if question_num == 20:
                # Vérifier que le test est terminé
                if result['status'] == 'completed':
                    print(f"✅ Test terminé avec succès!")
                    print(f"   Score final: {result.get('final_score', 'N/A')}")
                    print(f"   Profil généré: {result.get('profile', 'MISSING')}")
                    
                    # Vérifier que le profil est bien en base
                    profile_check = session_manager._get_profile_from_db(999)
                    if profile_check:
                        print(f"✅ Profil sauvegardé en base: {profile_check}")
                    else:
                        print(f"❌ Profil non trouvé en base")
                        return False
                else:
                    print(f"❌ Test non terminé après 20 questions")
                    print(f"   Status reçu: {result['status']}")
                    return False
            else:
                # Vérifier que la question suivante est disponible
                if result['status'] != 'in_progress' or 'next_question' not in result:
                    print(f"❌ Pas de question suivante après la question {question_num}")
                    return False
        
        # Test 3: Vérifier que le test est verrouillé
        print("\n🔒 Test 3: Vérification du verrouillage...")
        
        try:
            # Essayer de soumettre une réponse supplémentaire
            result = session_manager.submit_answer(
                test_id=test_id,
                student_id=999,
                answer="test"
            )
            print(f"❌ Le test n'est pas verrouillé, réponse acceptée: {result}")
            return False
        except Exception as e:
            if "n'est pas en cours" in str(e):
                print(f"✅ Test correctement verrouillé: {e}")
            else:
                print(f"⚠️ Erreur inattendue lors du verrouillage: {e}")
        
        # Test 4: Vérifier le statut en base
        print("\n📊 Test 4: Vérification du statut en base...")
        
        test_info = session_manager._get_test_info(test_id, 999)
        if test_info and test_info['status'] == 'completed':
            print(f"✅ Statut en base: {test_info['status']}")
            print(f"   Score final: {test_info.get('final_score', 'N/A')}")
            print(f"   Date de fin: {test_info.get('completed_at', 'N/A')}")
        else:
            print(f"❌ Statut incorrect en base: {test_info}")
            return False
        
        print("\n" + "=" * 50)
        print("🎉 TOUS LES TESTS DE FINALISATION SONT PASSÉS !")
        print("✅ Le test se termine correctement après 20 questions")
        print("✅ Le profil est bien généré et sauvegardé")
        print("✅ Le test est correctement verrouillé")
        
        return True
        
    except Exception as e:
        print(f"\n❌ ERREUR LORS DU TEST: {e}")
        import traceback
        traceback.print_exc()
        return False
        
    finally:
        if 'db' in locals():
            db.close()

if __name__ == "__main__":
    print("🧪 TEST DE FINALISATION DU TEST")
    print("=" * 50)
    
    success = test_test_finalization()
    
    if success:
        print("\n🚀 PROCHAINES ÉTAPES:")
        print("   1. ✅ Finalisation testée et validée")
        print("   2. 🚀 Démarrer le serveur: python start_assessment_system.py")
        print("   3. 📱 Tester le frontend: http://localhost:3001/dashboard/student/assessment")
        print("   4. 🎯 L'évaluation devrait maintenant se verrouiller après 20 questions")
    else:
        print("\n❌ LE TEST DE FINALISATION A ÉCHOUÉ")
        print("   Vérifiez les erreurs ci-dessus et corrigez-les")
    
    print("\n" + "=" * 50)





