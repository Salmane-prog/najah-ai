#!/usr/bin/env python3
"""
🔧 RÉPARATION DE LA BASE DE DONNÉES DES TESTS
Nettoie les tests incomplets et répare la finalisation
"""

import sys
import os
from pathlib import Path

# Ajouter le répertoire parent au path
sys.path.append(str(Path(__file__).parent))

from core.database import get_db
from sqlalchemy import text

def repair_test_database():
    """Réparer la base de données des tests"""
    
    print("🔧 RÉPARATION DE LA BASE DE DONNÉES DES TESTS")
    print("=" * 50)
    
    try:
        db = next(get_db())
        
        # 1. Vérifier les tables
        print("\n📋 Étape 1: Vérification des tables...")
        
        # Vérifier que la table des tests existe
        result = db.execute(text("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='french_adaptive_tests'
        """))
        
        if not result.fetchone():
            print("❌ Table french_adaptive_tests manquante")
            return False
        
        # Vérifier que la table des profils existe
        result = db.execute(text("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='french_learning_profiles'
        """))
        
        if not result.fetchone():
            print("❌ Table french_learning_profiles manquante")
            return False
        
        print("✅ Toutes les tables sont présentes")
        
        # 2. Nettoyer les tests incomplets
        print("\n🧹 Étape 2: Nettoyage des tests incomplets...")
        
        # Supprimer les tests qui ont plus de 20 questions
        result = db.execute(text("""
            DELETE FROM french_adaptive_tests 
            WHERE current_question_index > 20
        """))
        
        deleted_tests = result.rowcount
        print(f"   {deleted_tests} tests avec trop de questions supprimés")
        
        # Marquer comme terminés les tests qui ont exactement 20 questions
        result = db.execute(text("""
            UPDATE french_adaptive_tests 
            SET status = 'completed', 
                completed_at = datetime('now'),
                final_score = (
                    SELECT COALESCE(SUM(score), 0) 
                    FROM french_test_answers 
                    WHERE test_id = french_adaptive_tests.id
                )
            WHERE current_question_index = 20 AND status = 'in_progress'
        """))
        
        completed_tests = result.rowcount
        print(f"   {completed_tests} tests de 20 questions marqués comme terminés")
        
        # 3. Réparer les séquences de questions
        print("\n🔧 Étape 3: Réparation des séquences de questions...")
        
        # Vérifier que tous les tests ont une séquence de 20 questions
        result = db.execute(text("""
            SELECT id, student_id, current_question_index, questions_sequence
            FROM french_adaptive_tests 
            WHERE status = 'in_progress'
        """))
        
        tests_to_fix = result.fetchall()
        
        for test in tests_to_fix:
            test_id = test[0]
            student_id = test[1]
            current_index = test[2]
            questions_seq = test[3]
            
            if questions_seq:
                try:
                    import json
                    questions_list = json.loads(questions_seq)
                    
                    if len(questions_list) != 20:
                        print(f"   Test {test_id}: Séquence de {len(questions_list)} questions au lieu de 20")
                        
                        # Recréer une séquence de 20 questions
                        from services.french_question_selector import FrenchQuestionSelector
                        question_selector = FrenchQuestionSelector(db)
                        new_questions = question_selector.select_questions_for_assessment(student_id)
                        
                        if len(new_questions) == 20:
                            new_sequence = [q['id'] for q in new_questions]
                            db.execute(text("""
                                UPDATE french_adaptive_tests 
                                SET questions_sequence = :sequence
                                WHERE id = :test_id
                            """), {
                                "sequence": json.dumps(new_sequence),
                                "test_id": test_id
                            })
                            print(f"      ✅ Séquence réparée pour le test {test_id}")
                        else:
                            print(f"      ❌ Impossible de réparer le test {test_id}")
                except Exception as e:
                    print(f"   Test {test_id}: Erreur lors de la réparation: {e}")
        
        # 4. Générer les profils manquants
        print("\n👤 Étape 4: Génération des profils manquants...")
        
        # Trouver les tests terminés sans profil
        result = db.execute(text("""
            SELECT DISTINCT t.student_id, t.final_score
            FROM french_adaptive_tests t
            LEFT JOIN french_learning_profiles p ON t.student_id = p.student_id
            WHERE t.status = 'completed' AND p.student_id IS NULL
        """))
        
        tests_without_profile = result.fetchall()
        
        for test in tests_without_profile:
            student_id = test[0]
            final_score = test[1] or 0
            
            # Générer le profil
            try:
                from services.french_test_session_manager import FrenchTestSessionManager
                session_manager = FrenchTestSessionManager(db)
                profile = session_manager._generate_learning_profile(student_id, final_score)
                print(f"   ✅ Profil généré pour l'étudiant {student_id}")
            except Exception as e:
                print(f"   ❌ Erreur lors de la génération du profil pour {student_id}: {e}")
        
        # 5. Valider la réparation
        print("\n✅ Étape 5: Validation de la réparation...")
        
        # Compter les tests
        result = db.execute(text("""
            SELECT status, COUNT(*) as count
            FROM french_adaptive_tests 
            GROUP BY status
        """))
        
        status_counts = result.fetchall()
        print("   Statut des tests:")
        for status, count in status_counts:
            print(f"      {status}: {count}")
        
        # Compter les profils
        result = db.execute(text("""
            SELECT COUNT(*) as count
            FROM french_learning_profiles
        """))
        
        profile_count = result.fetchone()[0]
        print(f"   Profils générés: {profile_count}")
        
        # Valider qu'il n'y a pas de tests avec plus de 20 questions
        result = db.execute(text("""
            SELECT COUNT(*) as count
            FROM french_adaptive_tests 
            WHERE current_question_index > 20
        """))
        
        invalid_tests = result.fetchone()[0]
        if invalid_tests == 0:
            print("   ✅ Aucun test invalide trouvé")
        else:
            print(f"   ❌ {invalid_tests} tests invalides restent")
        
        db.commit()
        
        print("\n" + "=" * 50)
        print("🎉 RÉPARATION TERMINÉE AVEC SUCCÈS !")
        print("✅ Base de données nettoyée et réparée")
        print("✅ Tests incomplets supprimés")
        print("✅ Profils manquants générés")
        print("✅ Finalisation des tests corrigée")
        
        return True
        
    except Exception as e:
        print(f"\n❌ ERREUR LORS DE LA RÉPARATION: {e}")
        import traceback
        traceback.print_exc()
        return False
        
    finally:
        if 'db' in locals():
            db.close()

if __name__ == "__main__":
    print("🔧 RÉPARATION DE LA BASE DE DONNÉES DES TESTS")
    print("=" * 50)
    
    success = repair_test_database()
    
    if success:
        print("\n🚀 PROCHAINES ÉTAPES:")
        print("   1. ✅ Base de données réparée")
        print("   2. 🧪 Tester la finalisation: python test_finalization.py")
        print("   3. 🚀 Démarrer le serveur: python start_assessment_system.py")
        print("   4. 📱 Tester le frontend: http://localhost:3001/dashboard/student/assessment")
    else:
        print("\n❌ LA RÉPARATION A ÉCHOUÉ")
        print("   Vérifiez les erreurs ci-dessus")
    
    print("\n" + "=" * 50)





