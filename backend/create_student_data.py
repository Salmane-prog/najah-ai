#!/usr/bin/env python3
"""
Script pour créer des étudiants avec de vrais noms et des données de test
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import sessionmaker
from core.database import engine, Base
from models.user import User, UserRole
from models.class_group import ClassGroup, ClassStudent
from models.quiz import Quiz, QuizResult
from models.content import Content
from models.learning_path import LearningPath
from models.learning_path_step import LearningPathStep
from models.student_learning_path import StudentLearningPath
from models.student_analytics import StudentProgress
from models.badge import Badge, UserBadge
from models.notification import Notification
from models.user_activity import UserActivity
from core.security import get_password_hash
from datetime import datetime, timedelta
import random

def create_student_data():
    """Créer des étudiants avec de vrais noms et des données de test"""
    
    db = SessionLocal()
    
    try:
        print("=== CRÉATION DES DONNÉES ÉTUDIANTS ===")
        
        # Liste d'étudiants avec de vrais noms
        students_data = [
            {
                "first_name": "Salmane",
                "last_name": "Hajouji",
                "email": "salmane.hajouji@najah.ai",
                "username": "salmane.hajouji",
                "password": "password123"
            },
            {
                "first_name": "Fatima",
                "last_name": "Alami",
                "email": "fatima.alami@najah.ai",
                "username": "fatima.alami",
                "password": "password123"
            },
            {
                "first_name": "Omar",
                "last_name": "Benjelloun",
                "email": "omar.benjelloun@najah.ai",
                "username": "omar.benjelloun",
                "password": "password123"
            },
            {
                "first_name": "Amina",
                "last_name": "Tazi",
                "email": "amina.tazi@najah.ai",
                "username": "amina.tazi",
                "password": "password123"
            },
            {
                "first_name": "Youssef",
                "last_name": "Mansouri",
                "email": "youssef.mansouri@najah.ai",
                "username": "youssef.mansouri",
                "password": "password123"
            },
            {
                "first_name": "Layla",
                "last_name": "Bennani",
                "email": "layla.bennani@najah.ai",
                "username": "layla.bennani",
                "password": "password123"
            },
            {
                "first_name": "Karim",
                "last_name": "El Fassi",
                "email": "karim.elfassi@najah.ai",
                "username": "karim.elfassi",
                "password": "password123"
            },
            {
                "first_name": "Nour",
                "last_name": "Zeroual",
                "email": "nour.zeroual@najah.ai",
                "username": "nour.zeroual",
                "password": "password123"
            }
        ]
        
        # Créer ou mettre à jour les étudiants
        for student_data in students_data:
            existing_student = db.query(User).filter(User.email == student_data["email"]).first()
            
            if existing_student:
                # Mettre à jour les noms si l'étudiant existe
                existing_student.first_name = student_data["first_name"]
                existing_student.last_name = student_data["last_name"]
                existing_student.username = student_data["username"]
                print(f"✅ Étudiant mis à jour: {student_data['first_name']} {student_data['last_name']}")
            else:
                # Créer un nouvel étudiant
                hashed_password = get_password_hash(student_data["password"])
                new_student = User(
                    username=student_data["username"],
                    email=student_data["email"],
                    hashed_password=hashed_password,
                    first_name=student_data["first_name"],
                    last_name=student_data["last_name"],
                    role=UserRole.student,
                    is_active=True
                )
                db.add(new_student)
                print(f"✅ Nouvel étudiant créé: {student_data['first_name']} {student_data['last_name']}")
        
        db.commit()
        
        # Créer des données de progression pour chaque étudiant
        students = db.query(User).filter(User.role == UserRole.student).all()
        
        for student in students:
            # Créer des données de progression
            progress = db.query(StudentProgress).filter(StudentProgress.student_id == student.id).first()
            if not progress:
                progress = StudentProgress(
                    student_id=student.id,
                    learning_path_id=1,
                    current_step_id=1,
                    progress_percentage=random.randint(20, 95),
                    time_spent=random.randint(30, 180),
                    completed_steps=random.randint(1, 5),
                    is_active=True,
                    last_activity=datetime.utcnow() - timedelta(days=random.randint(0, 7))
                )
                db.add(progress)
                print(f"✅ Progression créée pour: {student.first_name} {student.last_name}")
        
        # Créer des résultats de quiz pour certains étudiants
        quiz_subjects = ["Mathématiques", "Sciences", "Histoire", "Géographie", "Français"]
        
        for student in students[:5]:  # Pour les 5 premiers étudiants
            for i in range(random.randint(1, 4)):  # 1 à 4 quiz par étudiant
                quiz_result = QuizResult(
                    student_id=student.id,
                    quiz_id=1,
                    score=random.randint(60, 95),
                    completed=True,
                    time_taken=random.randint(300, 900),
                    created_at=datetime.utcnow() - timedelta(days=random.randint(1, 30))
                )
                db.add(quiz_result)
                print(f"✅ Quiz résultat créé pour: {student.first_name} {student.last_name}")
        
        db.commit()
        print("✅ Toutes les données étudiants ont été créées avec succès!")
        
    except Exception as e:
        print(f"❌ Erreur lors de la création des données: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_student_data() 