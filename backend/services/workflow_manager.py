#!/usr/bin/env python3
"""
Gestionnaire de workflow pour orchestrer tous les processus d'apprentissage
"""

from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import json

from services.assessment_engine import AssessmentEngine
from services.learning_path_generator import LearningPathGenerator
from services.progress_tracker import ProgressTracker
from models.user import User
from models.assessment import Assessment
from models.learning_path import LearningPath
from models.assessment_result import AssessmentResult

class WorkflowManager:
    """Gestionnaire de workflow pour l'orchestration des processus d'apprentissage"""
    
    def __init__(self, db: Session):
        self.db = db
        self.assessment_engine = AssessmentEngine(db)
        self.learning_path_generator = LearningPathGenerator(db)
        self.progress_tracker = ProgressTracker(db)
    
    def initialize_student_learning_journey(self, student_id: int, subjects: List[str] = None) -> Dict[str, Any]:
        """Initialiser le parcours d'apprentissage complet d'un étudiant"""
        
        print(f"🚀 Initialisation du parcours d'apprentissage pour l'étudiant {student_id}")
        
        # Étape 1: Créer l'évaluation initiale
        print("📝 Création de l'évaluation initiale...")
        initial_assessment = self.assessment_engine.create_initial_assessment(
            student_id=student_id,
            subject=subjects[0] if subjects else "Général"
        )
        
        # Étape 2: Créer des évaluations pour chaque matière si spécifiée
        additional_assessments = []
        if subjects and len(subjects) > 1:
            for subject in subjects[1:]:
                print(f"📝 Création d'évaluation pour {subject}...")
                assessment = self.assessment_engine.create_initial_assessment(
                    student_id=student_id,
                    subject=subject
                )
                additional_assessments.append(assessment)
        
        # Étape 3: Créer des parcours d'apprentissage de base
        print("🛤️ Création des parcours d'apprentissage de base...")
        base_paths = self._create_base_learning_paths(student_id, subjects)
        
        # Étape 4: Initialiser le suivi de progression
        print("📊 Initialisation du suivi de progression...")
        initial_progress = self.progress_tracker.get_student_overall_progress(student_id)
        
        return {
            "student_id": student_id,
            "status": "initialized",
            "initial_assessment": {
                "id": initial_assessment.id,
                "title": initial_assessment.title,
                "subject": initial_assessment.subject
            },
            "additional_assessments": [
                {
                    "id": a.id,
                    "title": a.title,
                    "subject": a.subject
                }
                for a in additional_assessments
            ],
            "base_learning_paths": [
                {
                    "id": p.id,
                    "title": p.title,
                    "subject": p.subject
                }
                for p in base_paths
            ],
            "initial_progress": initial_progress,
            "next_steps": [
                "Compléter l'évaluation initiale",
                "Démarrer les parcours d'apprentissage recommandés",
                "Suivre la progression via le dashboard"
            ],
            "created_at": datetime.utcnow().isoformat()
        }
    
    def process_assessment_completion(self, student_id: int, assessment_id: int, answers: List[Dict]) -> Dict[str, Any]:
        """Traiter la complétion d'une évaluation et générer les parcours personnalisés"""
        
        print(f"🎯 Traitement de la complétion de l'évaluation {assessment_id}")
        
        # Étape 1: Analyser les résultats de l'évaluation
        print("📊 Analyse des résultats...")
        assessment_results = self.assessment_engine.analyze_results(assessment_id, answers)
        
        # Étape 2: Générer des questions adaptatives si nécessaire
        print("🔄 Génération de questions adaptatives...")
        adaptive_questions = []
        if assessment_results["percentage"] < 80:  # Seuil pour questions adaptatives
            adaptive_questions = self.assessment_engine.generate_adaptive_questions(
                assessment_id, answers
            )
            print(f"   ✅ {len(adaptive_questions)} questions adaptatives générées")
        
        # Étape 3: Générer des parcours d'apprentissage personnalisés
        print("🛤️ Génération de parcours personnalisés...")
        personalized_paths = self.learning_path_generator.generate_personalized_paths(
            student_id, assessment_results
        )
        
        # Étape 4: Mettre à jour la progression
        print("📈 Mise à jour de la progression...")
        updated_progress = self.progress_tracker.get_student_overall_progress(student_id)
        
        # Étape 5: Générer des recommandations
        print("💡 Génération de recommandations...")
        recommendations = self._generate_learning_recommendations(
            assessment_results, personalized_paths
        )
        
        return {
            "student_id": student_id,
            "assessment_id": assessment_id,
            "assessment_results": assessment_results,
            "adaptive_questions_generated": len(adaptive_questions),
            "personalized_paths_created": len(personalized_paths),
            "updated_progress": updated_progress,
            "recommendations": recommendations,
            "next_steps": [
                "Compléter les questions adaptatives si générées",
                "Démarrer les nouveaux parcours personnalisés",
                "Suivre la progression via le dashboard"
            ],
            "completed_at": datetime.utcnow().isoformat()
        }
    
    def process_learning_path_completion(self, student_id: int, learning_path_id: int) -> Dict[str, Any]:
        """Traiter la complétion d'un parcours d'apprentissage"""
        
        print(f"🎉 Traitement de la complétion du parcours {learning_path_id}")
        
        # Étape 1: Mettre à jour la progression
        print("📊 Mise à jour de la progression...")
        updated_progress = self.progress_tracker.get_student_overall_progress(student_id)
        
        # Étape 2: Analyser les performances
        print("📈 Analyse des performances...")
        performance_analysis = self._analyze_learning_path_performance(
            student_id, learning_path_id
        )
        
        # Étape 3: Générer de nouveaux parcours si nécessaire
        print("🔄 Génération de nouveaux parcours...")
        new_paths = []
        if performance_analysis["level"] == "Avancé":
            new_paths = self._generate_advanced_paths(student_id, learning_path_id)
        
        # Étape 4: Générer des recommandations
        print("💡 Génération de recommandations...")
        recommendations = self._generate_path_completion_recommendations(
            performance_analysis, new_paths
        )
        
        return {
            "student_id": student_id,
            "learning_path_id": learning_path_id,
            "status": "completed",
            "updated_progress": updated_progress,
            "performance_analysis": performance_analysis,
            "new_paths_generated": len(new_paths),
            "recommendations": recommendations,
            "next_steps": [
                "Célébrer l'achèvement du parcours",
                "Démarrer de nouveaux parcours si disponibles",
                "Participer à des défis avancés"
            ],
            "completed_at": datetime.utcnow().isoformat()
        }
    
    def generate_weekly_report(self, student_id: int) -> Dict[str, Any]:
        """Générer un rapport hebdomadaire complet"""
        
        print(f"📋 Génération du rapport hebdomadaire pour l'étudiant {student_id}")
        
        # Étape 1: Récupérer la progression globale
        print("📊 Récupération de la progression globale...")
        overall_progress = self.progress_tracker.get_student_overall_progress(student_id)
        
        # Étape 2: Récupérer les analytics d'apprentissage
        print("📈 Récupération des analytics...")
        learning_analytics = self.progress_tracker.get_learning_analytics(
            student_id, period="week"
        )
        
        # Étape 3: Analyser les matières
        print("🎯 Analyse des matières...")
        subject_analysis = {}
        subjects = ["Mathématiques", "Français", "Sciences"]
        for subject in subjects:
            subject_progress = self.progress_tracker.get_subject_progress(student_id, subject)
            subject_analysis[subject] = subject_progress
        
        # Étape 4: Générer des recommandations hebdomadaires
        print("💡 Génération de recommandations...")
        weekly_recommendations = self._generate_weekly_recommendations(
            overall_progress, learning_analytics, subject_analysis
        )
        
        return {
            "student_id": student_id,
            "report_type": "weekly",
            "period": "week",
            "generated_at": datetime.utcnow().isoformat(),
            "overall_progress": overall_progress,
            "learning_analytics": learning_analytics,
            "subject_analysis": subject_analysis,
            "recommendations": weekly_recommendations,
            "achievements": self._identify_weekly_achievements(student_id),
            "goals_for_next_week": self._generate_next_week_goals(overall_progress, subject_analysis)
        }
    
    def _create_base_learning_paths(self, student_id: int, subjects: List[str] = None) -> List[LearningPath]:
        """Créer des parcours d'apprentissage de base"""
        
        if not subjects:
            subjects = ["Mathématiques", "Français", "Sciences"]
        
        base_paths = []
        for subject in subjects[:3]:  # Limiter à 3 matières
            # Créer un parcours de base pour chaque matière
            base_path = LearningPath(
                title=f"Parcours de Base - {subject}",
                description=f"Parcours d'introduction à {subject}",
                objectives=f"Acquérir les fondamentaux en {subject}",
                subject=subject,
                level="beginner",
                difficulty="easy",
                estimated_duration=30,
                is_adaptive=False,
                created_by=student_id,
                created_at=datetime.utcnow()
            )
            
            self.db.add(base_path)
            self.db.commit()
            self.db.refresh(base_path)
            
            # Créer les étapes de base
            base_steps = self._create_base_path_steps(base_path.id, subject)
            
            # Assigner le parcours à l'étudiant
            from models.student_learning_path import StudentLearningPath
            student_path = StudentLearningPath(
                student_id=student_id,
                learning_path_id=base_path.id,
                progress=0.0,
                is_completed=False,
                started_at=datetime.utcnow(),
                current_step=1,
                total_steps=len(base_steps)
            )
            
            self.db.add(student_path)
            self.db.commit()
            
            base_paths.append(base_path)
        
        return base_paths
    
    def _create_base_path_steps(self, learning_path_id: int, subject: str) -> List:
        """Créer les étapes de base pour un parcours"""
        
        from models.learning_path_step import LearningPathStep
        
        if subject == "Mathématiques":
            step_data = [
                ("Découverte", "Introduction aux concepts de base", "video", 5),
                ("Pratique", "Exercices simples", "exercise", 10),
                ("Validation", "Quiz de validation", "quiz", 5)
            ]
        elif subject == "Français":
            step_data = [
                ("Découverte", "Introduction à la matière", "video", 5),
                ("Pratique", "Exercices de base", "exercise", 10),
                ("Validation", "Quiz de validation", "quiz", 5)
            ]
        else:  # Sciences
            step_data = [
                ("Découverte", "Introduction aux sciences", "video", 5),
                ("Pratique", "Expériences simples", "exercise", 10),
                ("Validation", "Quiz de validation", "quiz", 5)
            ]
        
        steps = []
        for i, (title, description, content_type, duration) in enumerate(step_data):
            step = LearningPathStep(
                learning_path_id=learning_path_id,
                step_number=i + 1,
                title=title,
                description=description,
                content_type=content_type,
                estimated_duration=duration,
                is_required=True,
                is_active=True,
                created_at=datetime.utcnow()
            )
            self.db.add(step)
            steps.append(step)
        
        self.db.commit()
        return steps
    
    def _generate_learning_recommendations(self, assessment_results: Dict, personalized_paths: List) -> List[str]:
        """Générer des recommandations d'apprentissage"""
        
        recommendations = []
        
        # Recommandations basées sur le niveau
        level = assessment_results.get("level", "Débutant")
        if level == "Débutant":
            recommendations.append("Commencez par les parcours de base pour consolider vos fondations")
            recommendations.append("Pratiquez régulièrement avec des exercices simples")
        elif level == "Intermédiaire":
            recommendations.append("Explorez les parcours intermédiaires pour approfondir vos connaissances")
            recommendations.append("Participez à des quiz pour tester vos compétences")
        else:  # Avancé
            recommendations.append("Tentez les parcours avancés pour des défis stimulants")
            recommendations.append("Aidez les autres étudiants à progresser")
        
        # Recommandations basées sur les matières
        subject_scores = assessment_results.get("subject_scores", {})
        for subject, scores in subject_scores.items():
            if scores["total"] > 0:
                percentage = (scores["correct"] / scores["total"]) * 100
                if percentage < 60:
                    recommendations.append(f"Concentrez-vous sur {subject} pour améliorer vos compétences")
        
        # Recommandations basées sur les parcours générés
        if personalized_paths:
            recommendations.append(f"Vous avez {len(personalized_paths)} nouveaux parcours personnalisés disponibles")
            recommendations.append("Commencez par le parcours qui vous intéresse le plus")
        
        return recommendations[:5]  # Limiter à 5 recommandations
    
    def _analyze_learning_path_performance(self, student_id: int, learning_path_id: int) -> Dict[str, Any]:
        """Analyser les performances d'un parcours d'apprentissage"""
        
        # Récupérer les informations du parcours
        learning_path = self.db.query(LearningPath).filter(
            LearningPath.id == learning_path_id
        ).first()
        
        # Récupérer la progression de l'étudiant
        student_path = self.db.query(StudentLearningPath).filter(
            StudentLearningPath.student_id == student_id,
            StudentLearningPath.learning_path_id == learning_path_id
        ).first()
        
        # Analyser les performances
        if student_path and learning_path:
            # Calculer le temps d'apprentissage
            if student_path.started_at and student_path.completed_at:
                study_time = (student_path.completed_at - student_path.started_at).total_seconds() / 60
            else:
                study_time = 0
            
            # Déterminer le niveau de performance
            if student_path.progress == 100:
                if study_time <= learning_path.estimated_duration * 0.8:
                    performance_level = "Excellent"
                elif study_time <= learning_path.estimated_duration * 1.2:
                    performance_level = "Bon"
                else:
                    performance_level = "Satisfaisant"
            else:
                performance_level = "Incomplet"
            
            return {
                "learning_path_id": learning_path_id,
                "subject": learning_path.subject,
                "level": learning_path.level,
                "difficulty": learning_path.difficulty,
                "completion_time_minutes": round(study_time, 1),
                "estimated_time_minutes": learning_path.estimated_duration,
                "performance_level": performance_level,
                "efficiency": round(learning_path.estimated_duration / study_time * 100, 1) if study_time > 0 else 0
            }
        
        return {"error": "Parcours non trouvé"}
    
    def _generate_advanced_paths(self, student_id: int, completed_path_id: int) -> List[LearningPath]:
        """Générer des parcours avancés pour les étudiants performants"""
        
        # Récupérer le parcours complété pour identifier la matière
        completed_path = self.db.query(LearningPath).filter(
            LearningPath.id == completed_path_id
        ).first()
        
        if not completed_path:
            return []
        
        # Créer un parcours avancé dans la même matière
        advanced_path = LearningPath(
            title=f"Parcours Avancé - {completed_path.subject}",
            description=f"Parcours avancé en {completed_path.subject} pour étudiants performants",
            objectives=f"Explorer des concepts avancés en {completed_path.subject}",
            subject=completed_path.subject,
            level="advanced",
            difficulty="hard",
            estimated_duration=60,
            is_adaptive=True,
            created_by=student_id,
            created_at=datetime.utcnow()
        )
        
        self.db.add(advanced_path)
        self.db.commit()
        self.db.refresh(advanced_path)
        
        # Créer les étapes avancées
        advanced_steps = self._create_advanced_path_steps(advanced_path.id, completed_path.subject)
        
        # Assigner le parcours à l'étudiant
        from models.student_learning_path import StudentLearningPath
        student_path = StudentLearningPath(
            student_id=student_id,
            learning_path_id=advanced_path.id,
            progress=0.0,
            is_completed=False,
            started_at=datetime.utcnow(),
            current_step=1,
            total_steps=len(advanced_steps)
        )
        
        self.db.add(student_path)
        self.db.commit()
        
        return [advanced_path]
    
    def _create_advanced_path_steps(self, learning_path_id: int, subject: str) -> List:
        """Créer les étapes avancées pour un parcours"""
        
        from models.learning_path_step import LearningPathStep
        
        if subject == "Mathématiques":
            step_data = [
                ("Concepts avancés", "Introduction aux concepts complexes", "video", 15),
                ("Problèmes complexes", "Résolution de problèmes avancés", "exercise", 25),
                ("Applications", "Applications pratiques", "project", 30),
                ("Défis", "Défis mathématiques", "challenge", 20),
                ("Évaluation", "Validation des compétences avancées", "quiz", 10)
            ]
        else:
            step_data = [
                ("Concepts avancés", "Introduction aux concepts complexes", "video", 15),
                ("Pratique avancée", "Exercices complexes", "exercise", 25),
                ("Projets", "Projets pratiques", "project", 30),
                ("Défis", "Défis stimulants", "challenge", 20),
                ("Évaluation", "Validation des compétences avancées", "quiz", 10)
            ]
        
        steps = []
        for i, (title, description, content_type, duration) in enumerate(step_data):
            step = LearningPathStep(
                learning_path_id=learning_path_id,
                step_number=i + 1,
                title=title,
                description=description,
                content_type=content_type,
                estimated_duration=duration,
                is_required=True,
                is_active=True,
                created_at=datetime.utcnow()
            )
            self.db.add(step)
            steps.append(step)
        
        self.db.commit()
        return steps
    
    def _generate_path_completion_recommendations(self, performance_analysis: Dict, new_paths: List) -> List[str]:
        """Générer des recommandations après complétion d'un parcours"""
        
        recommendations = []
        
        # Recommandations basées sur la performance
        performance_level = performance_analysis.get("performance_level", "Satisfaisant")
        if performance_level == "Excellent":
            recommendations.append("Performance exceptionnelle ! Vous êtes prêt pour des défis plus complexes")
            recommendations.append("Considérez aider d'autres étudiants à progresser")
        elif performance_level == "Bon":
            recommendations.append("Bonne performance ! Continuez à vous améliorer")
            recommendations.append("Essayez des parcours de difficulté supérieure")
        else:
            recommendations.append("Performance satisfaisante. Pratiquez davantage pour vous améliorer")
            recommendations.append("Revenez aux concepts de base si nécessaire")
        
        # Recommandations basées sur les nouveaux parcours
        if new_paths:
            recommendations.append(f"Vous avez {len(new_paths)} nouveaux parcours avancés disponibles")
            recommendations.append("Commencez par le parcours qui vous intéresse le plus")
        
        return recommendations[:5]  # Limiter à 5 recommandations
    
    def _generate_weekly_recommendations(self, overall_progress: Dict, learning_analytics: Dict, subject_analysis: Dict) -> List[str]:
        """Générer des recommandations hebdomadaires"""
        
        recommendations = []
        
        # Recommandations basées sur la progression globale
        overall_level = overall_progress.get("overall_level", "Débutant")
        if overall_level == "Débutant":
            recommendations.append("Continuez à travailler sur les bases cette semaine")
        elif overall_level == "Intermédiaire":
            recommendations.append("Concentrez-vous sur vos points faibles cette semaine")
        else:
            recommendations.append("Explorez de nouveaux défis cette semaine")
        
        # Recommandations basées sur les analytics
        trends = learning_analytics.get("trends", {})
        if trends.get("trend") == "Déclin":
            recommendations.append("Votre performance a diminué. Revenez aux concepts de base")
        elif trends.get("trend") == "Amélioration":
            recommendations.append("Excellente progression ! Maintenez ce rythme")
        
        # Recommandations basées sur les matières
        for subject, analysis in subject_analysis.items():
            level = analysis.get("level", "Débutant")
            if level == "Débutant":
                recommendations.append(f"Concentrez-vous sur {subject} cette semaine")
        
        return recommendations[:5]  # Limiter à 5 recommandations
    
    def _identify_weekly_achievements(self, student_id: int) -> List[Dict[str, Any]]:
        """Identifier les réalisations de la semaine"""
        
        # Récupérer les activités de la semaine
        week_ago = datetime.utcnow() - timedelta(days=7)
        
        achievements = []
        
        # Évaluations complétées
        assessments_completed = self.db.query(AssessmentResult).filter(
            AssessmentResult.student_id == student_id,
            AssessmentResult.completed_at >= week_ago
        ).count()
        
        if assessments_completed > 0:
            achievements.append({
                "type": "assessment",
                "title": f"{assessments_completed} évaluation(s) complétée(s)",
                "description": "Vous avez terminé des évaluations cette semaine",
                "points": assessments_completed * 10
            })
        
        # Parcours complétés
        paths_completed = self.db.query(StudentLearningPath).filter(
            StudentLearningPath.student_id == student_id,
            StudentLearningPath.completed_at >= week_ago
        ).count()
        
        if paths_completed > 0:
            achievements.append({
                "type": "learning_path",
                "title": f"{paths_completed} parcours complété(s)",
                "description": "Vous avez terminé des parcours d'apprentissage",
                "points": paths_completed * 25
            })
        
        # Étapes complétées
        # (Cette logique nécessiterait une table de suivi des étapes)
        
        return achievements
    
    def _generate_next_week_goals(self, overall_progress: Dict, subject_analysis: Dict) -> List[Dict[str, Any]]:
        """Générer des objectifs pour la semaine suivante"""
        
        goals = []
        
        # Objectif global
        overall_level = overall_progress.get("overall_level", "Débutant")
        if overall_level == "Débutant":
            goals.append({
                "type": "global",
                "title": "Améliorer le niveau global",
                "description": "Atteindre le niveau intermédiaire",
                "target": "60% de progression moyenne",
                "priority": "high"
            })
        elif overall_level == "Intermédiaire":
            goals.append({
                "type": "global",
                "title": "Consolider le niveau intermédiaire",
                "description": "Renforcer les compétences existantes",
                "target": "75% de progression moyenne",
                "priority": "medium"
            })
        
        # Objectifs par matière
        for subject, analysis in subject_analysis.items():
            level = analysis.get("level", "Débutant")
            if level == "Débutant":
                goals.append({
                    "type": "subject",
                    "subject": subject,
                    "title": f"Progresser en {subject}",
                    "description": "Atteindre le niveau intermédiaire",
                    "target": "Compléter 2 étapes de parcours",
                    "priority": "high"
                })
        
        return goals[:5]  # Limiter à 5 objectifs
