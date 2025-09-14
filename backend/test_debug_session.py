#!/usr/bin/env python3
"""
Test de debug pour identifier le problème de session
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.database import get_db
from services.french_test_session_manager import FrenchTestSessionManager
from sqlalchemy import text
import json

def debug_session_manager():
    """Debug du gestionnaire de session"""
    
    print("🐛 Debug du gestionnaire de session")
    print("=" * 50)
    
    try:
        db = next(get_db())
        
        # Test d'étudiant
        test_student_id = 999
        
        # Nettoyer les anciens tests
        print("🧹 Nettoyage des anciens tests...")
        db.execute(text("""
            DELETE FROM question_history 
            WHERE test_id IN (
                SELECT id FROM french_adaptive_tests 
                WHERE student_id = :student_id
            )
        """), {"student_id": test_student_id})
        
        db.execute(text("""
            DELETE FROM french_adaptive_tests 
            WHERE student_id = :student_id
        """), {"student_id": test_student_id})
        
        db.commit()
        print("✅ Nettoyage terminé")
        
        # Créer le gestionnaire
        session_manager = FrenchTestSessionManager(db)
        
        # Démarrer une session
        print("🚀 Démarrage d'une session de test...")
        test_session = session_manager.start_test_session(test_student_id)
        print(f"✅ Session créée: {test_session}")
        
        test_id = test_session['test_id']
        
        # Vérifier l'état en base
        print(f"🔍 Vérification de l'état en base pour test_id: {test_id}")
        result = db.execute(text("""
            SELECT id, student_id, status, current_question_index, 
                   questions_sequence, current_question_id
            FROM french_adaptive_tests
            WHERE id = :test_id
        """), {"test_id": test_id})
        
        row = result.fetchone()
        if row:
            print(f"  📋 Test trouvé en base:")
            print(f"    ID: {row[0]}")
            print(f"    Student ID: {row[1]}")
            print(f"    Status: {row[2]}")
            print(f"    Current Question Index: {row[3]}")
            print(f"    Questions Sequence: {row[4][:100] if row[4] else 'None'}...")
            print(f"    Current Question ID: {row[5]}")
        else:
            print("❌ Aucun test trouvé en base")
            return False
        
        # Tester la méthode _get_test_session
        print(f"🔍 Test de _get_test_session({test_id}, {test_student_id})")
        session_data = session_manager._get_test_session(test_id, test_student_id)
        if session_data:
            print(f"✅ Session récupérée: {session_data}")
        else:
            print("❌ Session non récupérée")
            return False
        
        # Simuler une soumission de réponse
        print("📝 Test de soumission de réponse...")
        current_question = test_session['current_question']
        test_answer = current_question['correct']  # Donner la bonne réponse
        
        print(f"  Question: {current_question['question'][:50]}...")
        print(f"  Réponse donnée: {test_answer}")
        
        # Appeler submit_answer
        result = session_manager.submit_answer(test_id, test_student_id, test_answer)
        print(f"✅ Réponse soumise: {result}")
        
        db.close()
        print("🎉 Test de debug réussi !")
        return True
        
    except Exception as e:
        print(f"❌ Erreur debug: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = debug_session_manager()
    sys.exit(0 if success else 1)











