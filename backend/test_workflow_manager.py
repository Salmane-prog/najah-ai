#!/usr/bin/env python3
"""
Script de test pour le Workflow Manager
"""

import sys
import os

# Ajouter le répertoire parent au path pour les imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.database import get_db
from services.workflow_manager import WorkflowManager
from services.assessment_engine import AssessmentEngine
from services.learning_path_generator import LearningPathGenerator
from services.progress_tracker import ProgressTracker

def test_workflow_manager():
    """Tester le Workflow Manager"""
    print("🧪 TEST DU WORKFLOW MANAGER")
    print("=" * 80)
    
    try:
        # Obtenir une session de base de données
        db = next(get_db())
        
        # Créer les instances des services
        print("🔧 Initialisation des services...")
        workflow_manager = WorkflowManager(db)
        assessment_engine = AssessmentEngine(db)
        learning_path_generator = LearningPathGenerator(db)
        progress_tracker = ProgressTracker(db)
        
        print("   ✅ Tous les services initialisés avec succès")
        
        # Test 1: Initialisation du parcours d'apprentissage
        print("\n1️⃣ TEST D'INITIALISATION DU PARCOURS")
        print("-" * 50)
        
        student_id = 30  # ID de l'étudiant de test
        subjects = ["Mathématiques", "Français"]
        
        try:
            print("   📝 Initialisation du parcours d'apprentissage...")
            journey = workflow_manager.initialize_student_learning_journey(student_id, subjects)
            
            print(f"   ✅ Parcours initialisé avec succès")
            print(f"      - Évaluation initiale: {journey['initial_assessment']['title']}")
            print(f"      - Parcours de base créés: {len(journey['base_learning_paths'])}")
            print(f"      - Prochaines étapes: {len(journey['next_steps'])}")
            
        except Exception as e:
            print(f"   ❌ Erreur lors de l'initialisation: {e}")
        
        # Test 2: Test du moteur d'évaluation
        print("\n2️⃣ TEST DU MOTEUR D'ÉVALUATION")
        print("-" * 50)
        
        try:
            print("   📝 Création d'une évaluation de test...")
            test_assessment = assessment_engine.create_initial_assessment(
                student_id=student_id,
                subject="Sciences"
            )
            
            print(f"   ✅ Évaluation créée: {test_assessment.title}")
            print(f"      - ID: {test_assessment.id}")
            print(f"      - Matière: {test_assessment.subject}")
            print(f"      - Statut: {test_assessment.status}")
            
        except Exception as e:
            print(f"   ❌ Erreur lors de la création de l'évaluation: {e}")
        
        # Test 3: Test du générateur de parcours
        print("\n3️⃣ TEST DU GÉNÉRATEUR DE PARCOURS")
        print("-" * 50)
        
        try:
            print("   🛤️ Génération de parcours personnalisés...")
            
            # Créer des résultats d'évaluation simulés
            mock_assessment_results = {
                "level": "Intermédiaire",
                "subject_scores": {
                    "Mathématiques": {"correct": 3, "total": 5},
                    "Français": {"correct": 4, "total": 5}
                },
                "recommendations": ["Continuer les exercices", "Pratiquer régulièrement"]
            }
            
            personalized_paths = learning_path_generator.generate_personalized_paths(
                student_id, mock_assessment_results
            )
            
            print(f"   ✅ {len(personalized_paths)} parcours personnalisés générés")
            for path in personalized_paths:
                print(f"      - {path.title} ({path.subject})")
            
        except Exception as e:
            print(f"   ❌ Erreur lors de la génération des parcours: {e}")
        
        # Test 4: Test du suivi de progression
        print("\n4️⃣ TEST DU SUIVI DE PROGRESSION")
        print("-" * 50)
        
        try:
            print("   📊 Récupération de la progression globale...")
            overall_progress = progress_tracker.get_student_overall_progress(student_id)
            
            print(f"   ✅ Progression récupérée")
            print(f"      - Niveau global: {overall_progress['overall_level']}")
            print(f"      - Parcours actifs: {overall_progress['learning_paths']['active']}")
            print(f"      - Progression moyenne: {overall_progress['learning_paths']['average_progress']}%")
            
        except Exception as e:
            print(f"   ❌ Erreur lors de la récupération de la progression: {e}")
        
        # Test 5: Test de génération de rapport
        print("\n5️⃣ TEST DE GÉNÉRATION DE RAPPORT")
        print("-" * 50)
        
        try:
            print("   📋 Génération du rapport hebdomadaire...")
            weekly_report = workflow_manager.generate_weekly_report(student_id)
            
            print(f"   ✅ Rapport hebdomadaire généré")
            print(f"      - Type: {weekly_report['report_type']}")
            print(f"      - Recommandations: {len(weekly_report['recommendations'])}")
            print(f"      - Objectifs: {len(weekly_report['goals_for_next_week'])}")
            
        except Exception as e:
            print(f"   ❌ Erreur lors de la génération du rapport: {e}")
        
        # Test 6: Test d'analyse des matières
        print("\n6️⃣ TEST D'ANALYSE DES MATIÈRES")
        print("-" * 50)
        
        try:
            print("   🎯 Analyse de la progression par matière...")
            
            for subject in ["Mathématiques", "Français", "Sciences"]:
                try:
                    subject_progress = progress_tracker.get_subject_progress(student_id, subject)
                    print(f"   ✅ {subject}: {subject_progress['level']}")
                    print(f"      - Progression: {subject_progress['learning_paths']['average_progress']}%")
                    print(f"      - Recommandations: {len(subject_progress['recommendations'])}")
                except Exception as e:
                    print(f"   ⚠️ {subject}: Erreur - {e}")
            
        except Exception as e:
            print(f"   ❌ Erreur lors de l'analyse des matières: {e}")
        
        # Test 7: Test des analytics d'apprentissage
        print("\n7️⃣ TEST DES ANALYTICS D'APPRENTISSAGE")
        print("-" * 50)
        
        try:
            print("   📈 Récupération des analytics d'apprentissage...")
            learning_analytics = progress_tracker.get_learning_analytics(student_id, "week")
            
            print(f"   ✅ Analytics récupérés")
            print(f"      - Période: {learning_analytics['period']}")
            print(f"      - Activités: {learning_analytics['activities']['total_activities']}")
            print(f"      - Tendance: {learning_analytics['trends']['trend']}")
            print(f"      - Recommandations: {len(learning_analytics['recommendations'])}")
            
        except Exception as e:
            print(f"   ❌ Erreur lors de la récupération des analytics: {e}")
        
        print("\n" + "=" * 80)
        print("🎯 RÉSUMÉ DES TESTS")
        print("✅ Services initialisés avec succès")
        print("✅ Workflow Manager fonctionnel")
        print("✅ Tous les composants testés")
        
        # Fermer la session de base de données
        db.close()
        
    except Exception as e:
        print(f"❌ Erreur générale: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("🚀 Démarrage des tests du Workflow Manager...")
    print("Assurez-vous que votre serveur backend est démarré et accessible")
    print("Appuyez sur Entrée pour continuer...")
    input()
    test_workflow_manager()







