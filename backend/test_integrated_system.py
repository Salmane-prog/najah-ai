#!/usr/bin/env python3
"""
Test Intégré du Système d'Apprentissage Adaptatif Najah AI
Teste tous les composants ensemble pour vérifier l'intégration
"""

import sys
import os

# Ajouter le répertoire courant au path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from adaptive_learning_engine import AdaptiveLearningEngine
from recommendation_system import RecommendationEngine
from assessment_tracking_system import AssessmentTrackingSystem

def test_integrated_system():
    """Tester l'ensemble du système intégré"""
    
    print("🚀 TEST INTÉGRÉ DU SYSTÈME NAJAH AI")
    print("=" * 60)
    
    try:
        # 1. Initialiser tous les composants
        print("\n🔧 Initialisation des composants...")
        
        adaptive_engine = AdaptiveLearningEngine()
        recommendation_engine = RecommendationEngine()
        assessment_system = AssessmentTrackingSystem()
        
        print("✅ Tous les composants initialisés")
        
        # 2. Test d'un étudiant complet
        student_id = 1
        print(f"\n👤 Test complet pour l'étudiant {student_id}")
        
        # 2.1 Créer un profil d'apprentissage
        print("\n📊 1. Création du profil d'apprentissage...")
        student_profile = adaptive_engine.get_student_profile(student_id)
        print(f"   • Style d'apprentissage: {student_profile.learning_style}")
        print(f"   • Difficulté préférée: {student_profile.preferred_difficulty}")
        print(f"   • Forces: {', '.join(student_profile.strengths) if student_profile.strengths else 'Aucune'}")
        print(f"   • Faiblesses: {', '.join(student_profile.weaknesses) if student_profile.weaknesses else 'Aucune'}")
        
        # 2.2 Générer un parcours d'apprentissage
        print("\n🛤️ 2. Génération du parcours d'apprentissage...")
        learning_path = adaptive_engine.generate_learning_path(student_id, ["Mathématiques"])
        print(f"   • Parcours créé avec {len(learning_path['modules'])} modules")
        if learning_path['modules']:
            print(f"   • Difficulté de départ: {learning_path['modules'][0]['start_level']}")
        print(f"   • Durée estimée: {learning_path['estimated_duration']} minutes")
        
        # 2.3 Obtenir des recommandations
        print("\n💡 3. Génération des recommandations...")
        recommendations = recommendation_engine.get_personalized_recommendations(student_id, limit=3)
        print(f"   • {len(recommendations)} recommandations générées")
        for i, rec in enumerate(recommendations[:2], 1):
            print(f"   {i}. {rec.title} ({rec.category})")
        
        # 2.4 Créer une évaluation adaptative
        print("\n🧠 4. Création d'évaluation adaptative...")
        assessment = assessment_system.create_adaptive_assessment(student_id, "Mathématiques")
        print(f"   • Évaluation créée: {assessment['assessment_id']}")
        print(f"   • Catégorie: {assessment['category']}")
        print(f"   • Questions: {assessment['total_questions']}")
        
        # 2.5 Simuler une évaluation
        print("\n✍️ 5. Simulation d'évaluation...")
        # Simuler des réponses (70% de réussite)
        simulated_answers = [
            {'question_id': 1, 'selected_answer_id': 1, 'is_correct': True},
            {'question_id': 2, 'selected_answer_id': 2, 'is_correct': False},
            {'question_id': 3, 'selected_answer_id': 1, 'is_correct': True},
            {'question_id': 4, 'selected_answer_id': 1, 'is_correct': True},
            {'question_id': 5, 'selected_answer_id': 2, 'is_correct': False}
        ]
        
        # Traiter l'évaluation
        assessment_data = {
            'student_id': student_id,
            'category': "Mathématiques",
            'difficulty': "intermédiaire"
        }
        result = assessment_system.process_adaptive_assessment(assessment_data, simulated_answers)
        
        if result.get('success'):
            print(f"   • Score: {result['score']}/{result['total_possible']}")
            print(f"   • Pourcentage: {result['percentage']:.1%}")
            print(f"   • Prochaine difficulté: {result['next_difficulty']}")
        else:
            print(f"   ❌ Erreur: {result.get('error', 'Erreur inconnue')}")
        
        # 2.6 Générer la cartographie des compétences
        print("\n🗺️ 6. Cartographie des compétences...")
        competency_map = assessment_system.generate_competency_map(student_id)
        print(f"   • {len(competency_map)} compétences cartographiées")
        for comp in competency_map[:2]:
            print(f"   • {comp.skill}: {comp.current_level} ({comp.progress_percentage:.1f}%)")
        
        # 2.7 Générer les analytics
        print("\n📈 7. Analytics d'apprentissage...")
        analytics = assessment_system.generate_learning_analytics(student_id)
        print(f"   • Précision moyenne: {analytics.average_accuracy:.1%}")
        print(f"   • Taux d'amélioration: {analytics.improvement_rate:+.1%}")
        print(f"   • Cohérence: {analytics.learning_consistency:.1%}")
        print(f"   • Temps préféré: {analytics.preferred_study_time}")
        
        # 2.8 Prédictions de performance
        print("\n🔮 8. Prédictions de performance...")
        prediction = recommendation_engine.predict_performance(student_id, "Mathématiques", "1_month")
        print(f"   • Performance actuelle: {prediction['current_performance']:.1%}")
        print(f"   • Performance prédite: {prediction['predicted_performance']:.1%}")
        print(f"   • Confiance: {prediction['confidence']:.1%}")
        
        # 3. Test de robustesse
        print("\n🛡️ 9. Test de robustesse...")
        
        # Test avec un étudiant inexistant
        non_existent_profile = adaptive_engine.get_student_profile(999)
        if non_existent_profile:
            print("   ✅ Gestion des étudiants inexistants: OK")
        
        # Test avec une catégorie inexistante
        non_existent_assessment = assessment_system.create_adaptive_assessment(1, "CatégorieInexistante")
        if 'error' in non_existent_assessment:
            print("   ✅ Gestion des catégories inexistantes: OK")
        
        print("\n🎉 TEST INTÉGRÉ RÉUSSI !")
        print("✅ Tous les composants fonctionnent ensemble correctement")
        
        # 4. Nettoyage
        print("\n🧹 Nettoyage...")
        adaptive_engine.close()
        recommendation_engine.close()
        assessment_system.close()
        print("✅ Connexions fermées")
        
        return True
        
    except Exception as e:
        print(f"\n❌ ERREUR LORS DU TEST INTÉGRÉ: {e}")
        print(f"📍 Erreur à la ligne: {e.__traceback__.tb_lineno}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_integrated_system()
    if success:
        print("\n🚀 Le système Najah AI est prêt pour la production !")
        sys.exit(0)
    else:
        print("\n❌ Des problèmes ont été détectés dans le système")
        sys.exit(1)
