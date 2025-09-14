#!/usr/bin/env python3
"""
Script simple pour créer des devoirs de test pour les étudiants
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine, text
from datetime import datetime, timedelta

def create_test_homework():
    """Créer des devoirs de test pour les étudiants"""
    
    # Créer une connexion directe à la base de données
    engine = create_engine("sqlite:///../data/app.db")
    
    try:
        with engine.connect() as conn:
            # Vérifier s'il y a des étudiants et professeurs
            result = conn.execute(text("SELECT id, username, role FROM users WHERE role IN ('student', 'teacher') LIMIT 10"))
            users = result.fetchall()
            
            if len(users) < 2:
                print("❌ Il faut au moins un étudiant et un professeur dans la base de données")
                return
            
            student = None
            teacher = None
            for user in users:
                if user[2] == 'student' and not student:
                    student = user
                elif user[2] == 'teacher' and not teacher:
                    teacher = user
                
                if student and teacher:
                    break
            
            if not student or not teacher:
                print("❌ Il faut au moins un étudiant et un professeur dans la base de données")
                return
            
            print(f"✅ Étudiant trouvé: {student[1]} (ID: {student[0]})")
            print(f"✅ Professeur trouvé: {teacher[1]} (ID: {teacher[0]})")
            
            # Créer des devoirs de test avec des dates en janvier 2024
            test_homework = [
                {
                    "title": "Devoir de mathématiques - Équations du second degré",
                    "description": "Résoudre les exercices 1 à 15 du chapitre 3 sur les équations du second degré",
                    "subject": "Mathématiques",
                    "priority": "high",
                    "estimated_time": 120,
                    "due_date": datetime(2024, 1, 15)  # 15 janvier 2024
                },
                {
                    "title": "Rédaction d'histoire - Révolution française",
                    "description": "Écrire une dissertation de 3 pages sur les causes de la Révolution française",
                    "subject": "Histoire",
                    "priority": "medium",
                    "estimated_time": 180,
                    "due_date": datetime(2024, 1, 20)  # 20 janvier 2024
                },
                {
                    "title": "Révision physique - Mécanique",
                    "description": "Réviser les chapitres 1 à 4 sur la mécanique et faire les exercices",
                    "subject": "Physique",
                    "priority": "medium",
                    "estimated_time": 90,
                    "due_date": datetime(2024, 1, 18)  # 18 janvier 2024
                },
                {
                    "title": "Devoir de français - Analyse littéraire",
                    "description": "Analyser le poème 'Le Lac' de Lamartine",
                    "subject": "Français",
                    "priority": "low",
                    "estimated_time": 60,
                    "due_date": datetime(2024, 1, 12)  # 12 janvier 2024
                },
                {
                    "title": "Présentation sciences - Photosynthèse",
                    "description": "Préparer une présentation de 10 minutes sur la photosynthèse",
                    "subject": "Sciences",
                    "priority": "high",
                    "estimated_time": 120,
                    "due_date": datetime(2024, 1, 25)  # 25 janvier 2024
                }
            ]
            
            # Supprimer les anciens devoirs
            conn.execute(text("DELETE FROM assessment_assignments"))
            conn.execute(text("DELETE FROM assessments"))
            
            # Créer les devoirs
            for i, homework_data in enumerate(test_homework):
                # Créer l'évaluation
                conn.execute(text("""
                    INSERT INTO assessments (
                        student_id, assessment_type, title, description, subject,
                        priority, estimated_time, status, created_by
                    ) VALUES (:student_id, :assessment_type, :title, :description, :subject,
                             :priority, :estimated_time, :status, :created_by)
                """), {
                    "student_id": student[0],
                    "assessment_type": "progress",  # Utiliser "progress" au lieu de "homework"
                    "title": homework_data["title"],
                    "description": homework_data["description"],
                    "subject": homework_data["subject"],
                    "priority": homework_data["priority"],
                    "estimated_time": homework_data["estimated_time"],
                    "status": "in_progress",
                    "created_by": teacher[0]
                })
                
                # Récupérer l'ID de l'évaluation créée
                result = conn.execute(text("SELECT last_insert_rowid()"))
                assessment_id = result.fetchone()[0]
                
                # Créer l'assignation
                conn.execute(text("""
                    INSERT INTO assessment_assignments (
                        assessment_id, student_id, teacher_id, class_id,
                        due_date, status, created_at
                    ) VALUES (:assessment_id, :student_id, :teacher_id, :class_id,
                             :due_date, :status, :created_at)
                """), {
                    "assessment_id": assessment_id,
                    "student_id": student[0],
                    "teacher_id": teacher[0],
                    "class_id": 1,
                    "due_date": homework_data["due_date"],
                    "status": "pending",
                    "created_at": datetime.utcnow()
                })
            
            # Commit les changements
            conn.commit()
            print(f"✅ {len(test_homework)} devoirs de test créés avec succès pour l'étudiant {student[1]}")
            print("📅 Dates des devoirs : 12, 15, 18, 20, 25 janvier 2024")
            
    except Exception as e:
        print(f"❌ Erreur lors de la création des devoirs de test: {str(e)}")

def create_homework_for_today():
    """Créer un devoir pour aujourd'hui"""
    
    # Créer une connexion directe à la base de données
    engine = create_engine("sqlite:///../data/app.db")
    
    try:
        with engine.connect() as conn:
            # Récupérer un étudiant et un professeur
            result = conn.execute(text("SELECT id, username, role FROM users WHERE role IN ('student', 'teacher') LIMIT 10"))
            users = result.fetchall()
            
            student = None
            teacher = None
            for user in users:
                if user[2] == 'student' and not student:
                    student = user
                elif user[2] == 'teacher' and not teacher:
                    teacher = user
                
                if student and teacher:
                    break
            
            if not student or not teacher:
                print("❌ Il faut au moins un étudiant et un professeur dans la base de données")
                return
            
            # Date d'aujourd'hui
            today = datetime.now().replace(hour=23, minute=59, second=0, microsecond=0)
            
            # Créer un devoir pour aujourd'hui
            homework_data = {
                "title": "Devoir urgent - Créé aujourd'hui",
                "description": "Ce devoir a été créé aujourd'hui et doit être rendu aujourd'hui !",
                "subject": "Test",
                "priority": "high",
                "estimated_time": 30,
                "due_date": today
            }
            
            # Créer l'évaluation
            conn.execute(text("""
                INSERT INTO assessments (
                    student_id, assessment_type, title, description, subject,
                    priority, estimated_time, status, created_by
                ) VALUES (:student_id, :assessment_type, :title, :description, :subject,
                         :priority, :estimated_time, :status, :created_by)
            """), {
                "student_id": student[0],
                "assessment_type": "progress",
                "title": homework_data["title"],
                "description": homework_data["description"],
                "subject": homework_data["subject"],
                "priority": homework_data["priority"],
                "estimated_time": homework_data["estimated_time"],
                "status": "in_progress",
                "created_by": teacher[0]
            })
            
            # Récupérer l'ID de l'évaluation créée
            result = conn.execute(text("SELECT last_insert_rowid()"))
            assessment_id = result.fetchone()[0]
            
            # Créer l'assignation
            conn.execute(text("""
                INSERT INTO assessment_assignments (
                    assessment_id, student_id, teacher_id, class_id,
                    due_date, status, created_at
                ) VALUES (:assessment_id, :student_id, :teacher_id, :class_id,
                         :due_date, :status, :created_at)
            """), {
                "assessment_id": assessment_id,
                "student_id": student[0],
                "teacher_id": teacher[0],
                "class_id": 1,
                "due_date": homework_data["due_date"],
                "status": "pending",
                "created_at": datetime.utcnow()
            })
            
            # Commit les changements
            conn.commit()
            print(f"✅ Devoir créé pour aujourd'hui ({today.strftime('%d/%m/%Y')})")
            print(f"📝 Titre: {homework_data['title']}")
            print(f"👤 Étudiant: {student[1]}")
            print(f"👨‍🏫 Professeur: {teacher[1]}")
            
    except Exception as e:
        print(f"❌ Erreur lors de la création du devoir: {str(e)}")

if __name__ == "__main__":
    # create_test_homework()  # Commenté pour éviter de supprimer les devoirs existants
    create_homework_for_today() 