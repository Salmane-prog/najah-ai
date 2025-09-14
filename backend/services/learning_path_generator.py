#!/usr/bin/env python3
"""
Générateur de parcours d'apprentissage personnalisés
"""

from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from datetime import datetime
import random

from models.learning_path import LearningPath
from models.learning_path_step import LearningPathStep
from models.student_learning_path import StudentLearningPath
from models.assessment_result import AssessmentResult

class LearningPathGenerator:
    """Générateur de parcours d'apprentissage personnalisés"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def generate_personalized_paths(self, student_id: int, assessment_results: Dict[str, Any]) -> List[LearningPath]:
        """Générer des parcours personnalisés basés sur les résultats d'évaluation"""
        
        # Analyser les résultats pour déterminer les besoins
        level = assessment_results.get("level", "Débutant")
        subject_scores = assessment_results.get("subject_scores", {})
        recommendations = assessment_results.get("recommendations", [])
        
        # Déterminer les matières prioritaires
        priority_subjects = self._identify_priority_subjects(subject_scores)
        
        # Générer des parcours pour chaque matière prioritaire
        generated_paths = []
        
        for subject in priority_subjects:
            # Créer un parcours personnalisé pour cette matière
            learning_path = self._create_personalized_path(
                student_id=student_id,
                subject=subject,
                level=level,
                assessment_results=assessment_results
            )
            
            if learning_path:
                generated_paths.append(learning_path)
        
        # Créer un parcours général de consolidation si nécessaire
        if level == "Débutant":
            general_path = self._create_consolidation_path(student_id, assessment_results)
            if general_path:
                generated_paths.append(general_path)
        
        return generated_paths
    
    def _identify_priority_subjects(self, subject_scores: Dict[str, Any]) -> List[str]:
        """Identifier les matières prioritaires basées sur les scores"""
        
        priority_subjects = []
        
        # Ajouter les matières avec des scores faibles (priorité haute)
        for subject, scores in subject_scores.items():
            if scores["total"] > 0:
                percentage = (scores["correct"] / scores["total"]) * 100
                if percentage < 60:
                    priority_subjects.append(subject)
        
        # Si aucune matière prioritaire, ajouter les matières principales
        if not priority_subjects:
            priority_subjects = ["Mathématiques", "Français", "Sciences"]
        
        # Limiter à 3 matières maximum
        return priority_subjects[:3]
    
    def _create_personalized_path(self, student_id: int, subject: str, level: str, assessment_results: Dict[str, Any]) -> Optional[LearningPath]:
        """Créer un parcours personnalisé pour une matière spécifique"""
        
        # Déterminer la difficulté et la durée selon le niveau
        difficulty, estimated_duration, step_count = self._determine_path_parameters(level, subject)
        
        # Créer le parcours
        learning_path = LearningPath(
            title=f"Parcours {subject} - Niveau {level}",
            description=f"Parcours personnalisé en {subject} adapté à votre niveau {level.lower()}",
            objectives=f"Maîtriser les concepts de base en {subject} et progresser vers des notions plus avancées",
            subject=subject,
            level=level.lower(),
            difficulty=difficulty,
            estimated_duration=estimated_duration,
            is_adaptive=True,
            created_by=student_id,
            created_at=datetime.utcnow()
        )
        
        self.db.add(learning_path)
        self.db.commit()
        self.db.refresh(learning_path)
        
        # Créer les étapes du parcours
        steps = self._generate_path_steps(learning_path.id, subject, level, step_count)
        
        # Assigner le parcours à l'étudiant
        student_path = StudentLearningPath(
            student_id=student_id,
            learning_path_id=learning_path.id,
            progress=0.0,
            is_completed=False,
            started_at=datetime.utcnow(),
            current_step=1,
            total_steps=len(steps)
        )
        
        self.db.add(student_path)
        self.db.commit()
        
        return learning_path
    
    def _determine_path_parameters(self, level: str, subject: str) -> tuple:
        """Déterminer les paramètres du parcours selon le niveau"""
        
        if level == "Débutant":
            difficulty = "easy"
            estimated_duration = 30  # minutes
            step_count = 5
        elif level == "Intermédiaire":
            difficulty = "intermediate"
            estimated_duration = 45
            step_count = 7
        else:  # Avancé
            difficulty = "advanced"
            estimated_duration = 60
            step_count = 10
        
        return difficulty, estimated_duration, step_count
    
    def _generate_path_steps(self, learning_path_id: int, subject: str, level: str, step_count: int) -> List[LearningPathStep]:
        """Générer les étapes d'un parcours d'apprentissage"""
        
        steps = []
        
        if subject == "Mathématiques":
            steps = self._generate_math_steps(learning_path_id, level, step_count)
        elif subject == "Français":
            steps = self._generate_french_steps(learning_path_id, level, step_count)
        elif subject == "Sciences":
            steps = self._generate_science_steps(learning_path_id, level, step_count)
        else:
            steps = self._generate_general_steps(learning_path_id, level, step_count)
        
        # Ajouter les étapes à la base de données
        for step in steps:
            self.db.add(step)
        
        self.db.commit()
        return steps
    
    def _generate_math_steps(self, learning_path_id: int, level: str, step_count: int) -> List[LearningPathStep]:
        """Générer les étapes pour les mathématiques"""
        
        if level == "Débutant":
            step_data = [
                ("Nombres de 1 à 20", "Apprendre à compter et reconnaître les nombres", "video", 5),
                ("Addition simple", "Additionner des nombres de 1 à 10", "exercise", 8),
                ("Soustraction simple", "Soustraire des nombres de 1 à 10", "exercise", 8),
                ("Formes géométriques", "Reconnaître les formes de base", "interactive", 6),
                ("Évaluation", "Quiz de validation des acquis", "quiz", 3)
            ]
        elif level == "Intermédiaire":
            step_data = [
                ("Tables de multiplication", "Maîtriser les tables de 2 à 5", "video", 10),
                ("Multiplication à 2 chiffres", "Multiplier des nombres à 2 chiffres", "exercise", 12),
                ("Division simple", "Diviser des nombres par 2, 3, 4, 5", "exercise", 12),
                ("Fractions simples", "Comprendre les fractions 1/2, 1/3, 1/4", "interactive", 8),
                ("Périmètre et aire", "Calculer le périmètre et l'aire des formes", "exercise", 15),
                ("Problèmes", "Résoudre des problèmes simples", "exercise", 15),
                ("Évaluation finale", "Quiz de validation complète", "quiz", 5)
            ]
        else:  # Avancé
            step_data = [
                ("Tables complètes", "Maîtriser toutes les tables de multiplication", "video", 8),
                ("Multiplication complexe", "Multiplier des nombres à 3 chiffres", "exercise", 15),
                ("Division avec reste", "Diviser des nombres avec reste", "exercise", 15),
                ("Fractions et décimaux", "Travailler avec fractions et décimaux", "interactive", 12),
                ("Pourcentages", "Calculer des pourcentages", "exercise", 12),
                ("Géométrie avancée", "Calculer volumes et surfaces", "exercise", 15),
                ("Problèmes complexes", "Résoudre des problèmes multi-étapes", "exercise", 20),
                ("Algèbre simple", "Introduction aux équations", "interactive", 15),
                ("Statistiques", "Moyennes et graphiques", "exercise", 12),
                ("Évaluation avancée", "Quiz de validation avancée", "quiz", 8)
            ]
        
        steps = []
        for i, (title, description, content_type, duration) in enumerate(step_data[:step_count]):
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
            steps.append(step)
        
        return steps
    
    def _generate_french_steps(self, learning_path_id: int, level: str, step_count: int) -> List[LearningPathStep]:
        """Générer les étapes pour le français"""
        
        if level == "Débutant":
            step_data = [
                ("Alphabet et sons", "Apprendre l'alphabet et les sons", "video", 8),
                ("Vocabulaire de base", "Mots du quotidien", "interactive", 10),
                ("Articles définis", "Le, la, les", "exercise", 8),
                ("Pluriel simple", "Formation du pluriel", "exercise", 8),
                ("Évaluation", "Quiz de validation", "quiz", 6)
            ]
        elif level == "Intermédiaire":
            step_data = [
                ("Conjugaison présent", "Être, avoir, aller au présent", "video", 12),
                ("Adjectifs", "Accord des adjectifs", "exercise", 15),
                ("Pronoms personnels", "Je, tu, il, elle, nous, vous, ils, elles", "exercise", 15),
                ("Questions", "Formation des questions", "interactive", 10),
                ("Négation", "Ne...pas, ne...plus", "exercise", 12),
                ("Lecture simple", "Compréhension de textes courts", "exercise", 15),
                ("Évaluation", "Quiz de validation", "quiz", 6)
            ]
        else:  # Avancé
            step_data = [
                ("Temps composés", "Passé composé et imparfait", "video", 15),
                ("Subjonctif", "Formation et emploi du subjonctif", "exercise", 20),
                ("Conditionnel", "Formation et emploi du conditionnel", "exercise", 18),
                ("Subordonnées", "Propositions subordonnées", "exercise", 15),
                ("Vocabulaire avancé", "Expressions idiomatiques", "interactive", 12),
                ("Grammaire avancée", "Accord du participe passé", "exercise", 20),
                ("Compréhension", "Textes littéraires", "exercise", 25),
                ("Expression écrite", "Rédaction de textes", "exercise", 30),
                ("Culture", "Histoire de la littérature", "video", 15),
                ("Évaluation", "Quiz de validation", "quiz", 10)
            ]
        
        steps = []
        for i, (title, description, content_type, duration) in enumerate(step_data[:step_count]):
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
            steps.append(step)
        
        return steps
    
    def _generate_science_steps(self, learning_path_id: int, level: str, step_count: int) -> List[LearningPathStep]:
        """Générer les étapes pour les sciences"""
        
        if level == "Débutant":
            step_data = [
                ("Les 5 sens", "Découvrir nos sens", "video", 8),
                ("Animaux et plantes", "Classification simple", "interactive", 10),
                ("Matières", "Solide, liquide, gaz", "exercise", 8),
                ("Énergie", "Sources d'énergie simples", "exercise", 8),
                ("Évaluation", "Quiz de validation", "quiz", 6)
            ]
        elif level == "Intermédiaire":
            step_data = [
                ("Système solaire", "Planètes et étoiles", "video", 15),
                ("Chaînes alimentaires", "Relations entre êtres vivants", "exercise", 12),
                ("Électricité", "Circuits simples", "interactive", 15),
                ("Chimie de base", "Mélanges et solutions", "exercise", 15),
                ("Écosystèmes", "Environnements naturels", "exercise", 12),
                ("Météo", "Phénomènes météorologiques", "interactive", 10),
                ("Évaluation", "Quiz de validation", "quiz", 8)
            ]
        else:  # Avancé
            step_data = [
                ("Atomes et molécules", "Structure de la matière", "video", 20),
                ("Forces et mouvement", "Lois de Newton", "exercise", 25),
                ("Évolution", "Théorie de l'évolution", "exercise", 20),
                ("Génétique", "Hérédité et ADN", "interactive", 18),
                ("Écologie", "Impact humain sur l'environnement", "exercise", 20),
                ("Technologies", "Innovations scientifiques", "video", 15),
                ("Expérimentation", "Méthode scientifique", "exercise", 30),
                ("Débats", "Questions éthiques", "interactive", 20),
                ("Projets", "Projets scientifiques", "project", 40),
                ("Évaluation", "Quiz de validation", "quiz", 12)
            ]
        
        steps = []
        for i, (title, description, content_type, duration) in enumerate(step_data[:step_count]):
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
            steps.append(step)
        
        return steps
    
    def _generate_general_steps(self, learning_path_id: int, level: str, step_count: int) -> List[LearningPathStep]:
        """Générer des étapes générales"""
        
        step_data = [
            ("Découverte", "Exploration du sujet", "video", 10),
            ("Pratique", "Exercices d'application", "exercise", 15),
            ("Renforcement", "Consolidation des acquis", "interactive", 12),
            ("Application", "Mise en situation", "exercise", 18),
            ("Évaluation", "Validation des compétences", "quiz", 8)
        ]
        
        steps = []
        for i, (title, description, content_type, duration) in enumerate(step_data[:step_count]):
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
            steps.append(step)
        
        return steps
    
    def _create_consolidation_path(self, student_id: int, assessment_results: Dict[str, Any]) -> Optional[LearningPath]:
        """Créer un parcours de consolidation pour les débutants"""
        
        learning_path = LearningPath(
            title="Parcours de Consolidation - Fondamentaux",
            description="Parcours pour consolider les bases et gagner en confiance",
            objectives="Renforcer les compétences de base et développer la confiance en soi",
            subject="Général",
            level="beginner",
            difficulty="easy",
            estimated_duration=40,
            is_adaptive=True,
            created_by=student_id,
            created_at=datetime.utcnow()
        )
        
        self.db.add(learning_path)
        self.db.commit()
        self.db.refresh(learning_path)
        
        # Créer les étapes de consolidation
        consolidation_steps = [
            ("Bienvenue", "Présentation du parcours", "video", 5),
            ("Méthodes d'apprentissage", "Techniques pour mieux apprendre", "interactive", 10),
            ("Organisation", "Planifier son apprentissage", "exercise", 8),
            ("Motivation", "Trouver sa motivation", "interactive", 8),
            ("Premiers pas", "Premiers exercices simples", "exercise", 10),
            ("Évaluation", "Validation des acquis", "quiz", 5)
        ]
        
        for i, (title, description, content_type, duration) in enumerate(consolidation_steps):
            step = LearningPathStep(
                learning_path_id=learning_path.id,
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
        
        # Assigner le parcours à l'étudiant
        student_path = StudentLearningPath(
            student_id=student_id,
            learning_path_id=learning_path.id,
            progress=0.0,
            is_completed=False,
            started_at=datetime.utcnow(),
            current_step=1,
            total_steps=len(consolidation_steps)
        )
        
        self.db.add(student_path)
        self.db.commit()
        
        return learning_path
