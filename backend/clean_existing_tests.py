#!/usr/bin/env python3
"""
Script pour nettoyer les tests français existants
Permet de recommencer l'évaluation depuis zéro
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from models.french_learning import FrenchAdaptiveTest, FrenchLearningProfile
from models.question_history import QuestionHistory
import json

def clean_existing_tests():
    """Nettoie tous les tests français existants"""
    try:
        # Connexion à la base de données
        db_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'app.db')
        print(f"🗄️ Connexion à la base: {db_path}")
        
        engine = create_engine(f"sqlite:///{db_path}")
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = SessionLocal()
        
        try:
            # Vérifier les tests existants
            existing_tests = db.query(FrenchAdaptiveTest).all()
            print(f"📊 Tests existants trouvés: {len(existing_tests)}")
            
            for test in existing_tests:
                print(f"  - Test ID {test.id}: {test.student_id} - {test.status} - {test.test_type}")
            
            # Nettoyer l'historique des questions
            question_history_count = db.query(QuestionHistory).count()
            print(f"📝 Historique des questions: {question_history_count} entrées")
            
            # Nettoyer les profils d'apprentissage
            profiles_count = db.query(FrenchLearningProfile).count()
            print(f"👤 Profils d'apprentissage: {profiles_count} entrées")
            
            # Demander confirmation
            response = input("\n❓ Voulez-vous nettoyer tous les tests existants ? (oui/non): ")
            
            if response.lower() in ['oui', 'o', 'yes', 'y']:
                print("\n🧹 Nettoyage en cours...")
                
                # Supprimer l'historique des questions
                db.query(QuestionHistory).delete()
                print("✅ Historique des questions supprimé")
                
                # Supprimer les profils d'apprentissage
                db.query(FrenchLearningProfile).delete()
                print("✅ Profils d'apprentissage supprimés")
                
                # Supprimer tous les tests
                db.query(FrenchAdaptiveTest).delete()
                print("✅ Tests français supprimés")
                
                # Valider les changements
                db.commit()
                print("✅ Base de données mise à jour")
                
                # Vérifier le nettoyage
                remaining_tests = db.query(FrenchAdaptiveTest).count()
                remaining_profiles = db.query(FrenchLearningProfile).count()
                remaining_history = db.query(QuestionHistory).count()
                
                print(f"\n📊 État après nettoyage:")
                print(f"  - Tests: {remaining_tests}")
                print(f"  - Profils: {remaining_profiles}")
                print(f"  - Historique: {remaining_history}")
                
                print("\n🎉 Nettoyage terminé ! Vous pouvez maintenant recommencer l'évaluation.")
                
            else:
                print("❌ Nettoyage annulé")
                
        except Exception as e:
            print(f"❌ Erreur lors du nettoyage: {e}")
            db.rollback()
            
        finally:
            db.close()
            
    except Exception as e:
        print(f"❌ Erreur de connexion: {e}")

def reset_specific_student(student_id: int):
    """Réinitialise les tests pour un étudiant spécifique"""
    try:
        # Connexion à la base de données
        db_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'app.db')
        print(f"🗄️ Connexion à la base: {db_path}")
        
        engine = create_engine(f"sqlite:///{db_path}")
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = SessionLocal()
        
        try:
            # Vérifier les tests de l'étudiant
            student_tests = db.query(FrenchAdaptiveTest).filter(
                FrenchAdaptiveTest.student_id == student_id
            ).all()
            
            print(f"📊 Tests trouvés pour l'étudiant {student_id}: {len(student_tests)}")
            
            for test in student_tests:
                print(f"  - Test ID {test.id}: {test.status} - {test.test_type}")
            
            if student_tests:
                # Demander confirmation
                response = input(f"\n❓ Voulez-vous réinitialiser les tests pour l'étudiant {student_id} ? (oui/non): ")
                
                if response.lower() in ['oui', 'o', 'yes', 'y']:
                    print(f"\n🧹 Réinitialisation pour l'étudiant {student_id}...")
                    
                    # Supprimer l'historique des questions
                    db.query(QuestionHistory).filter(
                        QuestionHistory.test_id.in_([test.id for test in student_tests])
                    ).delete()
                    print("✅ Historique des questions supprimé")
                    
                    # Supprimer les profils d'apprentissage
                    db.query(FrenchLearningProfile).filter(
                        FrenchLearningProfile.student_id == student_id
                    ).delete()
                    print("✅ Profils d'apprentissage supprimés")
                    
                    # Supprimer les tests
                    for test in student_tests:
                        db.delete(test)
                    print("✅ Tests supprimés")
                    
                    # Valider les changements
                    db.commit()
                    print("✅ Base de données mise à jour")
                    
                    print(f"\n🎉 Réinitialisation terminée pour l'étudiant {student_id} !")
                    
                else:
                    print("❌ Réinitialisation annulée")
            else:
                print(f"ℹ️ Aucun test trouvé pour l'étudiant {student_id}")
                
        except Exception as e:
            print(f"❌ Erreur lors de la réinitialisation: {e}")
            db.rollback()
            
        finally:
            db.close()
            
    except Exception as e:
        print(f"❌ Erreur de connexion: {e}")

def main():
    """Fonction principale"""
    print("🧹 SCRIPT DE NETTOYAGE DES TESTS FRANÇAIS")
    print("=" * 50)
    
    if len(sys.argv) > 1:
        try:
            student_id = int(sys.argv[1])
            print(f"🎯 Réinitialisation pour l'étudiant {student_id}")
            reset_specific_student(student_id)
        except ValueError:
            print("❌ ID étudiant invalide. Utilisez un nombre.")
    else:
        print("🎯 Nettoyage complet de tous les tests")
        clean_existing_tests()
    
    print("\n" + "=" * 50)

if __name__ == "__main__":
    main()














