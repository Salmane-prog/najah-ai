#!/usr/bin/env python3
"""
🧪 TEST D'INTÉGRATION FRONTEND-BACKEND
Vérifie que le backend retourne le bon format pour le frontend
"""

import sys
import os
from pathlib import Path

# Ajouter le répertoire parent au path
sys.path.append(str(Path(__file__).parent))

from services.french_test_session_manager import FrenchTestSessionManager
from services.french_question_selector import FrenchQuestionSelector
from core.database import get_db

def test_frontend_integration():
    """Tester l'intégration frontend-backend"""
    
    print("🧪 TEST D'INTÉGRATION FRONTEND-BACKEND")
    print("=" * 50)
    
    try:
        db = next(get_db())
        
        # Test 1: Démarrer une session de test
        print("\n📋 Test 1: Démarrage d'une session de test...")
        session_manager = FrenchTestSessionManager(db)
        
        test_session = session_manager.start_test_session(student_id=999)
        print(f"✅ Session démarrée: {test_session['test_id']}")
        print(f"   Status: {test_session['status']}")
        print(f"   Success: {test_session.get('success', 'MISSING')}")
        print(f"   Current question: {test_session.get('current_question', 'MISSING')}")
        print(f"   Progress: {test_session.get('progress', 'MISSING')}")
        
        # Vérifier que tous les champs requis sont présents
        required_fields = ['success', 'test_id', 'status', 'current_question', 'progress']
        missing_fields = [field for field in required_fields if field not in test_session]
        
        if missing_fields:
            print(f"❌ Champs manquants: {missing_fields}")
            return False
        else:
            print("✅ Tous les champs requis sont présents")
        
        # Test 2: Soumettre une réponse
        print("\n📝 Test 2: Soumission d'une réponse...")
        
        # Récupérer la question actuelle
        current_question = test_session['current_question']
        test_id = test_session['test_id']
        
        # Soumettre une réponse
        result = session_manager.submit_answer(
            test_id=test_id,
            student_id=999,
            answer=current_question['correct']  # Réponse correcte
        )
        
        print(f"✅ Réponse soumise: {result['status']}")
        print(f"   Success: {result.get('success', 'MISSING')}")
        
        if result['status'] == 'completed':
            print(f"   Test terminé avec score: {result.get('final_score', 'N/A')}")
            print(f"   Profile: {result.get('profile', 'MISSING')}")
        else:
            print(f"   Question suivante: {result.get('next_question', 'MISSING')}")
            print(f"   Progress: {result.get('progress', 'MISSING')}")
        
        # Vérifier que tous les champs requis sont présents
        if result['status'] == 'completed':
            required_fields = ['success', 'test_id', 'status', 'final_score', 'profile']
        else:
            required_fields = ['success', 'test_id', 'status', 'next_question', 'progress']
        
        missing_fields = [field for field in required_fields if field not in result]
        
        if missing_fields:
            print(f"❌ Champs manquants: {missing_fields}")
            return False
        else:
            print("✅ Tous les champs requis sont présents")
        
        # Test 3: Vérifier le format des questions
        print("\n🎯 Test 3: Format des questions...")
        
        question_selector = FrenchQuestionSelector(db)
        questions = question_selector.select_questions_for_assessment(student_id=999)
        
        if len(questions) == 20:
            print(f"✅ 20 questions sélectionnées")
            
            # Vérifier le format de la première question
            first_question = questions[0]
            required_question_fields = ['id', 'question', 'options', 'correct', 'difficulty']
            missing_question_fields = [field for field in required_question_fields if field not in first_question]
            
            if missing_question_fields:
                print(f"❌ Champs manquants dans la question: {missing_question_fields}")
                return False
            else:
                print("✅ Format des questions correct")
        else:
            print(f"❌ Nombre de questions incorrect: {len(questions)}")
            return False
        
        print("\n" + "=" * 50)
        print("🎉 TOUS LES TESTS D'INTÉGRATION SONT PASSÉS !")
        print("✅ Le backend retourne le bon format pour le frontend")
        print("✅ L'intégration frontend-backend fonctionne correctement")
        
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
    print("🧪 TEST D'INTÉGRATION FRONTEND-BACKEND")
    print("=" * 50)
    
    success = test_frontend_integration()
    
    if success:
        print("\n🚀 PROCHAINES ÉTAPES:")
        print("   1. ✅ Intégration testée et validée")
        print("   2. 🚀 Démarrer le serveur: python start_assessment_system.py")
        print("   3. 📱 Tester le frontend: http://localhost:3001/dashboard/student/assessment")
        print("   4. 🎯 L'évaluation devrait maintenant fonctionner sans erreur")
    else:
        print("\n❌ LE TEST D'INTÉGRATION A ÉCHOUÉ")
        print("   Vérifiez les erreurs ci-dessus et corrigez-les")
    
    print("\n" + "=" * 50)





