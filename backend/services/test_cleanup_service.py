#!/usr/bin/env python3
"""
Service de nettoyage automatique des tests français abandonnés
Supprime les tests inachevés et orphelins
"""

import logging
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from models.french_learning import FrenchAdaptiveTest
from models.question_history import QuestionHistory
from models.french_learning import FrenchLearningProfile

logger = logging.getLogger(__name__)

class TestCleanupService:
    """Service de nettoyage automatique des tests"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def cleanup_abandoned_tests(self, max_age_hours: int = 2):
        """Nettoie les tests abandonnés plus vieux que max_age_hours"""
        try:
            cutoff_time = datetime.utcnow() - timedelta(hours=max_age_hours)
            
            # Trouver les tests abandonnés
            abandoned_tests = self.db.query(FrenchAdaptiveTest).filter(
                FrenchAdaptiveTest.status == "in_progress",
                FrenchAdaptiveTest.started_at < cutoff_time
            ).all()
            
            if not abandoned_tests:
                logger.info("Aucun test abandonné trouvé")
                return 0
            
            logger.info(f"🧹 Nettoyage de {len(abandoned_tests)} tests abandonnés")
            
            cleaned_count = 0
            for test in abandoned_tests:
                try:
                    # Supprimer l'historique des questions
                    question_history_deleted = self.db.query(QuestionHistory).filter(
                        QuestionHistory.test_id == test.id
                    ).delete()
                    
                    # Supprimer le test
                    self.db.delete(test)
                    
                    cleaned_count += 1
                    logger.info(f"✅ Test {test.id} (étudiant {test.student_id}) supprimé")
                    
                except Exception as e:
                    logger.error(f"❌ Erreur lors de la suppression du test {test.id}: {e}")
                    continue
            
            # Valider les changements
            self.db.commit()
            logger.info(f"🎉 Nettoyage terminé: {cleaned_count} tests supprimés")
            
            return cleaned_count
            
        except Exception as e:
            logger.error(f"❌ Erreur lors du nettoyage: {e}")
            self.db.rollback()
            return 0
    
    def cleanup_orphaned_profiles(self):
        """Nettoie les profils d'apprentissage orphelins"""
        try:
            # Trouver les profils sans test associé
            orphaned_profiles = self.db.query(FrenchLearningProfile).outerjoin(
                FrenchAdaptiveTest,
                FrenchLearningProfile.student_id == FrenchAdaptiveTest.student_id
            ).filter(
                FrenchAdaptiveTest.id.is_(None)
            ).all()
            
            if not orphaned_profiles:
                logger.info("Aucun profil orphelin trouvé")
                return 0
            
            logger.info(f"🧹 Nettoyage de {len(orphaned_profiles)} profils orphelins")
            
            # Supprimer les profils orphelins
            for profile in orphaned_profiles:
                self.db.delete(profile)
                logger.info(f"✅ Profil orphelin {profile.id} supprimé")
            
            # Valider les changements
            self.db.commit()
            logger.info(f"🎉 Nettoyage des profils terminé: {len(orphaned_profiles)} supprimés")
            
            return len(orphaned_profiles)
            
        except Exception as e:
            logger.error(f"❌ Erreur lors du nettoyage des profils: {e}")
            self.db.rollback()
            return 0
    
    def cleanup_old_completed_tests(self, max_age_days: int = 30):
        """Nettoie les tests terminés très anciens"""
        try:
            cutoff_time = datetime.utcnow() - timedelta(days=max_age_days)
            
            # Trouver les anciens tests terminés
            old_tests = self.db.query(FrenchAdaptiveTest).filter(
                FrenchAdaptiveTest.status == "completed",
                FrenchAdaptiveTest.completed_at < cutoff_time
            ).all()
            
            if not old_tests:
                logger.info("Aucun ancien test terminé trouvé")
                return 0
            
            logger.info(f"🧹 Nettoyage de {len(old_tests)} anciens tests terminés")
            
            cleaned_count = 0
            for test in old_tests:
                try:
                    # Supprimer l'historique des questions
                    question_history_deleted = self.db.query(QuestionHistory).filter(
                        QuestionHistory.test_id == test.id
                    ).delete()
                    
                    # Supprimer le test
                    self.db.delete(test)
                    
                    cleaned_count += 1
                    logger.info(f"✅ Ancien test {test.id} supprimé")
                    
                except Exception as e:
                    logger.error(f"❌ Erreur lors de la suppression de l'ancien test {test.id}: {e}")
                    continue
            
            # Valider les changements
            self.db.commit()
            logger.info(f"🎉 Nettoyage des anciens tests terminé: {cleaned_count} supprimés")
            
            return cleaned_count
            
        except Exception as e:
            logger.error(f"❌ Erreur lors du nettoyage des anciens tests: {e}")
            self.db.rollback()
            return 0
    
    def full_cleanup(self):
        """Effectue un nettoyage complet"""
        try:
            logger.info("🧹 Début du nettoyage complet")
            
            # Nettoyage des tests abandonnés
            abandoned_cleaned = self.cleanup_abandoned_tests()
            
            # Nettoyage des profils orphelins
            profiles_cleaned = self.cleanup_orphaned_profiles()
            
            # Nettoyage des anciens tests terminés
            old_tests_cleaned = self.cleanup_old_completed_tests()
            
            total_cleaned = abandoned_cleaned + profiles_cleaned + old_tests_cleaned
            
            logger.info(f"🎉 Nettoyage complet terminé: {total_cleaned} éléments supprimés")
            
            return {
                "abandoned_tests": abandoned_cleaned,
                "orphaned_profiles": profiles_cleaned,
                "old_completed_tests": old_tests_cleaned,
                "total": total_cleaned
            }
            
        except Exception as e:
            logger.error(f"❌ Erreur lors du nettoyage complet: {e}")
            return {
                "abandoned_tests": 0,
                "orphaned_profiles": 0,
                "old_completed_tests": 0,
                "total": 0,
                "error": str(e)
            }
    
    def get_cleanup_stats(self):
        """Retourne les statistiques de nettoyage"""
        try:
            # Tests en cours
            in_progress_tests = self.db.query(FrenchAdaptiveTest).filter(
                FrenchAdaptiveTest.status == "in_progress"
            ).count()
            
            # Tests terminés
            completed_tests = self.db.query(FrenchAdaptiveTest).filter(
                FrenchAdaptiveTest.status == "completed"
            ).count()
            
            # Profils d'apprentissage
            profiles_count = self.db.query(FrenchLearningProfile).count()
            
            # Historique des questions
            question_history_count = self.db.query(QuestionHistory).count()
            
            return {
                "in_progress_tests": in_progress_tests,
                "completed_tests": completed_tests,
                "profiles_count": profiles_count,
                "question_history_count": question_history_count,
                "total_tests": in_progress_tests + completed_tests
            }
            
        except Exception as e:
            logger.error(f"❌ Erreur lors de la récupération des stats: {e}")
            return {}














