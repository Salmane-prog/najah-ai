#!/usr/bin/env python3
"""
Script pour créer des devoirs de test pour les étudiants
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from core.database import get_db, engine
from models.user import User
from models.assessment import Assessment, AssessmentAssignment
from datetime import datetime, timedelta

def create_test_homework():
    """Créer des devoirs de test pour les étudiants"""
    
    # Créer une session de base de données
    db = next(get_db())
    
    try:
        # Récupérer un étudiant existant
        student = db.query(User).filter(User.role == 'student').first()
        if not student:
            print("Aucun étudiant trouvé dans la base de données")
            return
        
        # Récupérer un professeur existant
        teacher = db.query(User).filter(User.role == 'teacher').first()
        if not teacher:
            print("Aucun professeur trouvé dans la base de données")
            return
        
        # Créer des devoirs de test
        test_homework = [
            {
                "title": "Devoir de mathématiques - Équations du second degré",
                "description": "Résoudre les exercices 1 à 15 du chapitre 3 sur les équations du second degré",
                "subject": "Mathématiques",
                "priority": "high",
                "estimated_time": 120,
                "due_date": datetime.now() + timedelta(days=2)
            },
            {
                "title": "Rédaction d'histoire - Révolution française",
                "description": "Écrire une dissertation de 3 pages sur les causes de la Révolution française",
                "subject": "Histoire",
                "priority": "medium",
                "estimated_time": 180,
                "due_date": datetime.now() + timedelta(days=5)
            },
            {
                "title": "Révision physique - Mécanique",
                "description": "Réviser les chapitres 1 à 4 sur la mécanique et faire les exercices",
                "subject": "Physique",
                "priority": "medium",
                "estimated_time": 90,
                "due_date": datetime.now() + timedelta(days=3)
            },
            {
                "title": "Devoir de français - Analyse littéraire",
                "description": "Analyser le poème 'Le Lac' de Lamartine",
                "subject": "Français",
                "priority": "low",
                "estimated_time": 60,
                "due_date": datetime.now() + timedelta(days=1)
            },
            {
                "title": "Présentation sciences - Photosynthèse",
                "description": "Préparer une présentation de 10 minutes sur la photosynthèse",
                "subject": "Sciences",
                "priority": "high",
                "estimated_time": 120,
                "due_date": datetime.now() + timedelta(days=4)
            }
        ]
        
        # Créer les devoirs
        for i, homework_data in enumerate(test_homework):
            # Créer l'évaluation
            assessment = Assessment(
                title=homework_data["title"],
                description=homework_data["description"],
                subject=homework_data["subject"],
                assessment_type="homework",
                priority=homework_data["priority"],
                estimated_time=homework_data["estimated_time"],
                created_by=teacher.id,
                created_at=datetime.utcnow()
            )
            db.add(assessment)
            db.flush()  # Pour obtenir l'ID
            
            # Créer l'assignation
            assignment = AssessmentAssignment(
                assessment_id=assessment.id,
                student_id=student.id,
                teacher_id=teacher.id,
                class_id=1,  # Classe par défaut
                due_date=homework_data["due_date"],
                status="pending",
                created_at=datetime.utcnow()
            )
            db.add(assignment)
        
        # Commit les changements
        db.commit()
        print(f"✅ {len(test_homework)} devoirs de test créés avec succès pour l'étudiant {student.username}")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Erreur lors de la création des devoirs de test: {str(e)}")
    finally:
        db.close()

if __name__ == "__main__":
    create_test_homework() 