#!/usr/bin/env python3
"""
Script de test complet pour le système d'évaluation initiale
Teste tous les composants : services, endpoints, base de données
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.database import SessionLocal
from models.user import User, UserRole
from core.security import get_password_hash
from services.student_onboarding_service import StudentOnboardingService
from services.french_question_selector import FrenchQuestionSelector
from services.french_test_session_manager import FrenchTestSessionManager
from datetime import datetime

def test_complete_assessment_system():
    """Test complet du système d'évaluation initiale"""
    print("🧪 TEST COMPLET DU SYSTÈME D'ÉVALUATION INITIALE")
    print("=" * 60)
    
    db = SessionLocal()
    try:
        # 1. Créer un étudiant de test
        print("\n1️⃣ Création d'un étudiant de test...")
        test_student = create_test_student(db)
        if not test_student:
            print("❌ Impossible de créer l'étudiant de test")
            return False
        
        print(f"✅ Étudiant de test créé: {test_student.username} (ID: {test_student.id})")
        
        # 2. Tester le service d'onboarding
        print("\n2️⃣ Test du service d'onboarding...")
        onboarding_service = StudentOnboardingService(db)
        
        # Vérifier le statut initial
        initial_status = onboarding_service.check_and_initialize_student(test_student.id)
        print(f"   📊 Statut initial: {initial_status['status']}")
        print(f"   📝 Message: {initial_status['message']}")
        
        # 3. Tester la création automatique de l'évaluation
        print("\n3️⃣ Test de la création automatique de l'évaluation...")
        assessment_result = onboarding_service.auto_start_initial_assessment(test_student.id)
        
        if assessment_result["success"]:
            print(f"   ✅ Évaluation créée avec succès (ID: {assessment_result['assessment_id']})")
            print(f"   📋 Questions créées: {assessment_result['questions_count']}")
        else:
            print(f"   ❌ Erreur lors de la création: {assessment_result['message']}")
            return False
        
        # 4. Tester le sélecteur de questions
        print("\n4️⃣ Test du sélecteur de questions...")
        question_selector = FrenchQuestionSelector(db)
        questions = question_selector.select_questions_for_assessment(test_student.id)
        
        if len(questions) == 20:
            print(f"   ✅ {len(questions)} questions sélectionnées correctement")
            
            # Vérifier la répartition
            easy_count = len([q for q in questions if q["difficulty"] == "easy"])
            medium_count = len([q for q in questions if q["difficulty"] == "medium"])
            hard_count = len([q for q in questions if q["difficulty"] == "hard"])
            
            print(f"   📊 Répartition: {easy_count} facile, {medium_count} moyen, {hard_count} difficile")
            
            if easy_count == 7 and medium_count == 6 and hard_count == 7:
                print("   ✅ Répartition correcte (7-6-7)")
            else:
                print("   ❌ Répartition incorrecte")
                return False
        else:
            print(f"   ❌ Nombre de questions incorrect: {len(questions)} au lieu de 20")
            return False
        
        # 5. Tester le gestionnaire de session de test
        print("\n5️⃣ Test du gestionnaire de session de test...")
        session_manager = FrenchTestSessionManager(db)
        
        # Démarrer une session
        test_session = session_manager.start_test_session(test_student.id)
        if test_session["status"] == "in_progress":
            print(f"   ✅ Session démarrée (ID: {test_session['test_id']})")
            print(f"   📝 Question actuelle: {test_session['current_question']['question'][:50]}...")
        else:
            print(f"   ❌ Erreur lors du démarrage de la session: {test_session['status']}")
            return False
        
        # 6. Tester la soumission de réponses
        print("\n6️⃣ Test de la soumission de réponses...")
        
        # Simuler quelques réponses
        test_answers = ["Le", "Je suis", "Féminin", "Chevaux", "Petit"]
        questions_answered = 0
        
        for i, answer in enumerate(test_answers):
            if i >= 5:  # Limiter à 5 questions pour le test
                break
                
            try:
                result = session_manager.submit_answer(
                    test_session["test_id"], 
                    test_student.id, 
                    answer
                )
                
                if result["status"] == "in_progress":
                    questions_answered += 1
                    print(f"   ✅ Question {i+1} répondue: {answer}")
                elif result["status"] == "completed":
                    print(f"   🎉 Test terminé après {i+1} questions")
                    break
                else:
                    print(f"   ❌ Erreur question {i+1}: {result}")
                    return False
                    
            except Exception as e:
                print(f"   ❌ Erreur lors de la réponse {i+1}: {e}")
                return False
        
        print(f"   📊 Total questions répondues: {questions_answered}")
        
        # 7. Vérifier le statut final
        print("\n7️⃣ Vérification du statut final...")
        final_status = onboarding_service.check_and_initialize_student(test_student.id)
        print(f"   📊 Statut final: {final_status['status']}")
        print(f"   📝 Message: {final_status['message']}")
        
        # 8. Nettoyer les données de test
        print("\n8️⃣ Nettoyage des données de test...")
        cleanup_test_data(db, test_student.id)
        print("   ✅ Données de test supprimées")
        
        print("\n🎉 TOUS LES TESTS SONT PASSÉS AVEC SUCCÈS !")
        print("✅ Le système d'évaluation initiale fonctionne parfaitement")
        return True
        
    except Exception as e:
        print(f"\n❌ ERREUR LORS DES TESTS: {e}")
        import traceback
        traceback.print_exc()
        return False
        
    finally:
        db.close()

def create_test_student(db):
    """Créer un étudiant de test"""
    try:
        # Vérifier si l'étudiant existe déjà
        existing_student = db.query(User).filter(
            User.email == "test_assessment@najah.ai"
        ).first()
        
        if existing_student:
            # Supprimer l'ancien étudiant de test
            db.delete(existing_student)
            db.commit()
        
        # Créer un nouvel étudiant de test
        test_student = User(
            username="test_assessment",
            email="test_assessment@najah.ai",
            hashed_password=get_password_hash("test123"),
            role=UserRole.student,
            created_at=datetime.utcnow()
        )
        
        db.add(test_student)
        db.commit()
        db.refresh(test_student)
        
        return test_student
        
    except Exception as e:
        print(f"❌ Erreur lors de la création de l'étudiant de test: {e}")
        db.rollback()
        return None

def cleanup_test_data(db, student_id):
    """Nettoyer les données de test"""
    try:
        # Supprimer les profils d'apprentissage
        db.execute("""
            DELETE FROM french_learning_profiles 
            WHERE student_id = :student_id
        """, {"student_id": student_id})
        
        # Supprimer les tests
        db.execute("""
            DELETE FROM french_adaptive_tests 
            WHERE student_id = :student_id
        """, {"student_id": student_id})
        
        # Supprimer les réponses
        db.execute("""
            DELETE FROM french_test_answers 
            WHERE student_id = :student_id
        """, {"student_id": student_id})
        
        # Supprimer les questions d'évaluation
        db.execute("""
            DELETE FROM assessment_questions 
            WHERE assessment_id IN (
                SELECT id FROM french_adaptive_tests WHERE student_id = :student_id
            )
        """, {"student_id": student_id})
        
        # Supprimer l'étudiant de test
        db.execute("""
            DELETE FROM users 
            WHERE id = :student_id
        """, {"student_id": student_id})
        
        db.commit()
        
    except Exception as e:
        print(f"⚠️ Erreur lors du nettoyage: {e}")
        db.rollback()

def test_individual_components():
    """Test des composants individuels"""
    print("\n🔍 TEST DES COMPOSANTS INDIVIDUELS")
    print("=" * 40)
    
    db = SessionLocal()
    try:
        # Test du sélecteur de questions
        print("\n📋 Test du sélecteur de questions...")
        selector = FrenchQuestionSelector(db)
        total_questions = selector.get_total_questions()
        print(f"   Total questions disponibles: {total_questions}")
        
        if total_questions >= 20:
            print("   ✅ Nombre de questions suffisant")
        else:
            print("   ❌ Nombre de questions insuffisant")
            return False
        
        # Test du gestionnaire de session
        print("\n🎯 Test du gestionnaire de session...")
        session_manager = FrenchTestSessionManager(db)
        print("   ✅ Gestionnaire de session initialisé")
        
        # Test du service d'onboarding
        print("\n🎓 Test du service d'onboarding...")
        onboarding_service = StudentOnboardingService(db)
        print("   ✅ Service d'onboarding initialisé")
        
        print("\n✅ Tous les composants sont initialisés correctement")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors des tests des composants: {e}")
        return False
        
    finally:
        db.close()

if __name__ == "__main__":
    print("🚀 DÉMARRAGE DES TESTS DU SYSTÈME D'ÉVALUATION INITIALE")
    
    # Test des composants individuels
    if not test_individual_components():
        print("❌ Tests des composants échoués")
        sys.exit(1)
    
    # Test complet du système
    if test_complete_assessment_system():
        print("\n🎉 SYSTÈME D'ÉVALUATION INITIALE VALIDÉ AVEC SUCCÈS !")
        print("✅ Prêt pour la production")
        sys.exit(0)
    else:
        print("\n❌ TESTS ÉCHOUÉS - Vérifiez les erreurs ci-dessus")
        sys.exit(1)





