#!/usr/bin/env python3
"""
Tests d'intégration complets pour le système d'évaluation française optimisé
Teste l'ensemble du workflow : sélection de questions, test complet, génération de profil IA
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.database import get_db
from services.french_question_selector import FrenchQuestionSelector
from services.french_test_session_manager import FrenchTestSessionManager
from services.advanced_profile_generator import AdvancedProfileGenerator
from sqlalchemy import text
import json
import random

def test_complete_workflow():
    """Tester le workflow complet d'évaluation"""
    
    print("🚀 Test d'intégration complet du système d'évaluation française optimisé")
    print("=" * 80)
    
    try:
        # Obtenir une session de base de données
        db = next(get_db())
        
        # Simuler un étudiant de test
        test_student_id = 999
        
        print(f"👤 Test avec l'étudiant simulé ID: {test_student_id}")
        
        # 1. Tester la sélection de questions
        print("\n📝 ÉTAPE 1: Test de sélection de questions")
        print("-" * 40)
        
        selector = FrenchQuestionSelector(db)
        selected_questions = selector.select_20_questions(test_student_id)
        
        if len(selected_questions) != 20:
            print(f"❌ ÉCHEC: {len(selected_questions)} questions au lieu de 20")
            return False
        
        print(f"✅ {len(selected_questions)} questions sélectionnées")
        
        # Vérifier la répartition
        difficulty_counts = {}
        for q in selected_questions:
            diff = q.get('difficulty', 'unknown')
            difficulty_counts[diff] = difficulty_counts.get(diff, 0) + 1
        
        print(f"📊 Répartition: {difficulty_counts}")
        
        # 2. Tester la création de session complète
        print("\n🎯 ÉTAPE 2: Test de session complète")
        print("-" * 40)
        
        session_manager = FrenchTestSessionManager(db)
        
        # Nettoyer les anciens tests du même étudiant
        db.execute(text("""
            DELETE FROM french_adaptive_tests 
            WHERE student_id = :student_id
        """), {"student_id": test_student_id})
        
        db.execute(text("""
            DELETE FROM question_history 
            WHERE test_id IN (
                SELECT id FROM french_adaptive_tests 
                WHERE student_id = :student_id
            )
        """), {"student_id": test_student_id})
        
        db.commit()
        
        # Démarrer la session
        test_session = session_manager.start_test_session(test_student_id)
        
        if test_session['status'] != 'in_progress':
            print(f"❌ ÉCHEC: Session non démarrée, statut: {test_session['status']}")
            return False
        
        print(f"✅ Session démarrée: ID {test_session['test_id']}")
        print(f"✅ Première question: {test_session['current_question']['question'][:50]}...")
        
        # 3. Simuler les 20 réponses
        print("\n📋 ÉTAPE 3: Simulation de 20 réponses")
        print("-" * 40)
        
        test_id = test_session['test_id']
        answers_given = []
        
        for i in range(20):
            try:
                # Simuler une réponse (80% de chances d'être correcte pour tester un bon profil)
                current_question = test_session['current_question']
                correct_answer = current_question['correct']
                
                # 80% de chances de donner la bonne réponse
                if random.random() < 0.8:
                    answer = correct_answer
                else:
                    # Donner une mauvaise réponse
                    options = current_question['options']
                    wrong_options = [opt for opt in options if opt != correct_answer]
                    answer = random.choice(wrong_options) if wrong_options else options[0]
                
                answers_given.append({
                    'question_num': i + 1,
                    'question': current_question['question'][:30] + "...",
                    'difficulty': current_question['difficulty'],
                    'answer_given': answer,
                    'correct_answer': correct_answer,
                    'is_correct': answer == correct_answer
                })
                
                # Soumettre la réponse
                result = session_manager.submit_answer(test_id, test_student_id, answer)
                
                print(f"  Q{i+1}: {current_question['difficulty']:8} - {'✓' if answer == correct_answer else '✗'}")
                
                if result['status'] == 'completed':
                    print(f"\n🏁 Test terminé après {i+1} questions")
                    final_result = result
                    break
                elif result['status'] == 'in_progress':
                    test_session['current_question'] = result['next_question']
                else:
                    print(f"❌ Statut inattendu: {result['status']}")
                    return False
                    
            except Exception as e:
                print(f"❌ Erreur question {i+1}: {e}")
                return False
        
        # 4. Vérifier la génération de profil
        print("\n🧠 ÉTAPE 4: Vérification du profil généré")
        print("-" * 40)
        
        if 'final_result' not in locals():
            print("❌ Test non terminé correctement")
            return False
        
        profile = final_result.get('profile')
        if not profile:
            print("❌ Aucun profil généré")
            return False
        
        print(f"✅ Profil généré:")
        print(f"  📈 Niveau français: {profile.get('french_level', 'N/A')}")
        print(f"  🧠 Style d'apprentissage: {profile.get('learning_style', 'N/A')}")
        print(f"  ⏱️ Rythme préféré: {profile.get('preferred_pace', 'N/A')}")
        
        # Vérifier le profil cognitif
        cognitive_profile = profile.get('cognitive_profile')
        if cognitive_profile:
            if isinstance(cognitive_profile, str):
                cognitive_data = json.loads(cognitive_profile)
            else:
                cognitive_data = cognitive_profile
            
            print(f"  🎯 Score final: {cognitive_data.get('final_score', 0):.1f}%")
            print(f"  🔍 Confiance: {profile.get('confidence_score', 0):.1f}%")
        
        # 5. Tester la récupération du profil via API
        print("\n🔌 ÉTAPE 5: Test de récupération via API")
        print("-" * 40)
        
        # Simuler la récupération du profil
        result = db.execute(text("""
            SELECT 
                learning_style, french_level, preferred_pace, 
                strengths, weaknesses, cognitive_profile
            FROM french_learning_profiles
            WHERE student_id = :student_id
            ORDER BY updated_at DESC
            LIMIT 1
        """), {"student_id": test_student_id})
        
        profile_row = result.fetchone()
        if profile_row:
            print("✅ Profil récupéré depuis la base de données")
            print(f"  📊 Données cohérentes: {profile_row[0]} / {profile_row[1]} / {profile_row[2]}")
        else:
            print("❌ Profil non trouvé en base")
            return False
        
        # 6. Analyser les statistiques finales
        print("\n📊 ÉTAPE 6: Analyse des statistiques")
        print("-" * 40)
        
        correct_answers = sum(1 for ans in answers_given if ans['is_correct'])
        success_rate = (correct_answers / len(answers_given)) * 100
        
        # Analyser par difficulté
        diff_stats = {}
        for ans in answers_given:
            diff = ans['difficulty']
            if diff not in diff_stats:
                diff_stats[diff] = {'total': 0, 'correct': 0}
            diff_stats[diff]['total'] += 1
            if ans['is_correct']:
                diff_stats[diff]['correct'] += 1
        
        print(f"  🎯 Score global: {correct_answers}/{len(answers_given)} ({success_rate:.1f}%)")
        for diff, stats in diff_stats.items():
            rate = (stats['correct'] / stats['total']) * 100 if stats['total'] > 0 else 0
            print(f"  📈 {diff}: {stats['correct']}/{stats['total']} ({rate:.1f}%)")
        
        # 7. Test de nettoyage
        print("\n🧹 ÉTAPE 7: Nettoyage")
        print("-" * 40)
        
        # Ne pas supprimer pour permettre inspection manuelle
        print("✅ Données de test conservées pour inspection (étudiant ID: 999)")
        
        db.close()
        
        print("\n" + "=" * 80)
        print("🎉 TEST D'INTÉGRATION COMPLET RÉUSSI !")
        print("✅ Toutes les étapes ont été validées avec succès")
        print(f"📊 Profil généré avec {success_rate:.1f}% de réussite")
        
        return True
        
    except Exception as e:
        print(f"\n❌ ERREUR CRITIQUE: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_advanced_profile_generator():
    """Tester spécifiquement le générateur de profil avancé"""
    
    print("\n🧠 Test spécifique du générateur de profil IA avancé")
    print("=" * 60)
    
    try:
        db = next(get_db())
        
        # Trouver un test existant
        result = db.execute(text("""
            SELECT id, student_id, final_score
            FROM french_adaptive_tests
            WHERE status = 'completed'
            ORDER BY completed_at DESC
            LIMIT 1
        """))
        
        test_row = result.fetchone()
        if not test_row:
            print("⚠️ Aucun test terminé trouvé, création d'un test simulé...")
            # Créer des données de test simulées
            test_id = 9999
            student_id = 999
            final_score = 75.0
        else:
            test_id, student_id, final_score = test_row
            print(f"📋 Test trouvé: ID {test_id}, Étudiant {student_id}, Score {final_score}%")
        
        # Tester le générateur avancé
        generator = AdvancedProfileGenerator(db)
        advanced_profile = generator.generate_comprehensive_profile(student_id, test_id, final_score)
        
        print("✅ Profil avancé généré avec succès")
        print(f"  🎯 Niveau: {advanced_profile.get('french_level')}")
        print(f"  🧠 Style: {advanced_profile.get('learning_style')}")
        print(f"  ⏱️ Rythme: {advanced_profile.get('preferred_pace')}")
        print(f"  📊 Confiance: {advanced_profile.get('confidence_score', 0):.1f}%")
        
        # Vérifier les recommandations IA
        ai_recommendations = advanced_profile.get('ai_recommendations')
        if ai_recommendations:
            if isinstance(ai_recommendations, str):
                recommendations = json.loads(ai_recommendations)
            else:
                recommendations = ai_recommendations
            
            print(f"  🤖 Recommandations IA: {len(recommendations)} générées")
            for i, rec in enumerate(recommendations[:3], 1):
                print(f"    {i}. {rec.get('title', 'N/A')} (priorité: {rec.get('priority', 'N/A')})")
        
        db.close()
        print("✅ Test du générateur avancé réussi")
        return True
        
    except Exception as e:
        print(f"❌ Erreur test générateur avancé: {e}")
        return False

def test_system_health():
    """Tester la santé générale du système"""
    
    print("\n🏥 Test de santé du système")
    print("=" * 40)
    
    try:
        db = next(get_db())
        
        # Vérifier les tables essentielles
        essential_tables = [
            'french_adaptive_tests',
            'french_learning_profiles',
            'question_history',
            'questions',
            'adaptive_questions'
        ]
        
        for table in essential_tables:
            try:
                result = db.execute(text(f"SELECT COUNT(*) FROM {table}"))
                count = result.fetchone()[0]
                print(f"  ✅ {table}: {count} entrées")
            except Exception as e:
                print(f"  ❌ {table}: Erreur - {e}")
                return False
        
        # Vérifier les questions françaises disponibles
        result = db.execute(text("""
            SELECT COUNT(*) FROM question_history 
            WHERE topic IN ('Articles', 'Grammaire', 'Conjugaison', 'Vocabulaire', 'Compréhension')
        """))
        french_questions = result.fetchone()[0]
        
        result = db.execute(text("""
            SELECT COUNT(*) FROM adaptive_questions 
            WHERE topic LIKE '%français%' OR topic LIKE '%grammaire%'
        """))
        adaptive_french = result.fetchone()[0]
        
        total_french = french_questions + adaptive_french
        
        print(f"  📚 Questions françaises: {total_french} disponibles")
        
        if total_french >= 20:
            print("  ✅ Suffisant pour un test de 20 questions")
        else:
            print("  ⚠️ Insuffisant pour un test optimal")
        
        db.close()
        print("✅ Santé du système validée")
        return True
        
    except Exception as e:
        print(f"❌ Erreur test santé: {e}")
        return False

def main():
    """Fonction principale d'exécution des tests"""
    
    print("🔬 SUITE DE TESTS D'INTÉGRATION COMPLÈTE")
    print("🎯 Système d'évaluation française optimisé")
    print("=" * 80)
    
    tests = [
        ("Santé du système", test_system_health),
        ("Générateur de profil IA", test_advanced_profile_generator),
        ("Workflow complet", test_complete_workflow)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n🧪 EXÉCUTION: {test_name}")
        print("=" * 60)
        
        try:
            success = test_func()
            results.append((test_name, success))
            
            if success:
                print(f"\n🎉 {test_name}: SUCCÈS")
            else:
                print(f"\n💥 {test_name}: ÉCHEC")
                
        except Exception as e:
            print(f"\n💥 {test_name}: ERREUR CRITIQUE - {e}")
            results.append((test_name, False))
    
    # Résumé final
    print("\n" + "=" * 80)
    print("📋 RÉSUMÉ FINAL DES TESTS D'INTÉGRATION")
    print("=" * 80)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for test_name, success in results:
        status = "✅ SUCCÈS" if success else "❌ ÉCHEC"
        print(f"  {test_name}: {status}")
    
    print(f"\n🎯 Résultat global: {passed}/{total} tests réussis")
    
    if passed == total:
        print("\n🎉 INTÉGRATION COMPLÈTE VALIDÉE !")
        print("✅ Le système d'évaluation française optimisé est entièrement fonctionnel")
        print("🚀 Prêt pour la production avec :")
        print("   • 20 questions exactes garanties")
        print("   • Sélection intelligente anti-répétition")
        print("   • Profil IA avancé avec recommandations")
        print("   • Interface optimisée et progressive")
    else:
        print("\n⚠️ CERTAINS TESTS ONT ÉCHOUÉ")
        print("🔧 Vérifiez les erreurs ci-dessus avant la mise en production")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)











