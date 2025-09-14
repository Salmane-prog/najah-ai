#!/usr/bin/env python3
"""
Script pour créer des données de test pour les assignations
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine, text
from datetime import datetime, timedelta

def create_test_assignments_data():
    """Créer des données de test pour les assignations"""
    
    # Créer une connexion directe à la base de données
    engine = create_engine("sqlite:///../data/app.db")
    
    try:
        with engine.connect() as conn:
            # 1. Vérifier s'il y a des utilisateurs
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
            
            # 2. Créer une classe de test si elle n'existe pas
            class_result = conn.execute(text("SELECT id FROM class_groups WHERE teacher_id = :teacher_id LIMIT 1"), {
                "teacher_id": teacher[0]
            })
            class_group = class_result.fetchone()
            
            if not class_group:
                print("📚 Création d'une classe de test...")
                conn.execute(text("""
                    INSERT INTO class_groups (name, description, level, subject, teacher_id, max_students)
                    VALUES (:name, :description, :level, :subject, :teacher_id, :max_students)
                """), {
                    "name": "Classe de test",
                    "description": "Classe créée pour les tests",
                    "level": "Terminale",
                    "subject": "Mathématiques",
                    "teacher_id": teacher[0],
                    "max_students": 30
                })
                
                # Récupérer l'ID de la classe créée
                class_result = conn.execute(text("SELECT last_insert_rowid()"))
                class_id = class_result.fetchone()[0]
                print(f"✅ Classe créée avec l'ID: {class_id}")
            else:
                class_id = class_group[0]
                print(f"✅ Classe existante trouvée: {class_id}")
            
            # 3. Ajouter l'étudiant à la classe si pas déjà fait
            student_in_class = conn.execute(text("""
                SELECT id FROM class_students WHERE class_id = :class_id AND student_id = :student_id
            """), {
                "class_id": class_id,
                "student_id": student[0]
            }).fetchone()
            
            if not student_in_class:
                print("👤 Ajout de l'étudiant à la classe...")
                conn.execute(text("""
                    INSERT INTO class_students (class_id, student_id, enrolled_at, status)
                    VALUES (:class_id, :student_id, :enrolled_at, :status)
                """), {
                    "class_id": class_id,
                    "student_id": student[0],
                    "enrolled_at": datetime.utcnow(),
                    "status": "active"
                })
                print("✅ Étudiant ajouté à la classe")
            else:
                print("✅ Étudiant déjà dans la classe")
            
            # 4. Créer des devoirs de test
            print("📝 Création de devoirs de test...")
            
            # Supprimer les anciens devoirs
            conn.execute(text("DELETE FROM homework"))
            
            test_homeworks = [
                {
                    "title": "Devoir de mathématiques - Équations du second degré",
                    "description": "Résoudre les exercices 1 à 15 du chapitre 3 sur les équations du second degré",
                    "subject": "Mathématiques",
                    "priority": "high",
                    "estimated_time": 120,
                    "due_date": datetime.now() + timedelta(days=7)
                },
                {
                    "title": "Rédaction d'histoire - Révolution française",
                    "description": "Écrire une dissertation de 3 pages sur les causes de la Révolution française",
                    "subject": "Histoire",
                    "priority": "medium",
                    "estimated_time": 180,
                    "due_date": datetime.now() + timedelta(days=14)
                },
                {
                    "title": "Révision physique - Mécanique",
                    "description": "Réviser les chapitres 1 à 4 sur la mécanique et faire les exercices",
                    "subject": "Physique",
                    "priority": "medium",
                    "estimated_time": 90,
                    "due_date": datetime.now() + timedelta(days=5)
                }
            ]
            
            for homework_data in test_homeworks:
                conn.execute(text("""
                    INSERT INTO homework (
                        title, description, subject, class_id, assigned_by, assigned_to,
                        due_date, status, priority, estimated_time, created_at
                    ) VALUES (
                        :title, :description, :subject, :class_id, :assigned_by, :assigned_to,
                        :due_date, :status, :priority, :estimated_time, :created_at
                    )
                """), {
                    "title": homework_data["title"],
                    "description": homework_data["description"],
                    "subject": homework_data["subject"],
                    "class_id": class_id,
                    "assigned_by": teacher[0],
                    "assigned_to": student[0],
                    "due_date": homework_data["due_date"],
                    "status": "pending",
                    "priority": homework_data["priority"],
                    "estimated_time": homework_data["estimated_time"],
                    "created_at": datetime.utcnow()
                })
            
            # 5. Créer des objectifs d'apprentissage de test
            print("🎯 Création d'objectifs de test...")
            
            # Supprimer les anciens objectifs
            conn.execute(text("DELETE FROM learning_goals"))
            
            test_goals = [
                {
                    "title": "Maîtriser les équations du second degré",
                    "description": "Être capable de résoudre tous types d'équations du second degré",
                    "subject": "Mathématiques",
                    "target_date": datetime.now() + timedelta(days=30),
                    "progress": 0.0
                },
                {
                    "title": "Comprendre la Révolution française",
                    "description": "Analyser les causes et conséquences de la Révolution française",
                    "subject": "Histoire",
                    "target_date": datetime.now() + timedelta(days=45),
                    "progress": 0.3
                }
            ]
            
            for goal_data in test_goals:
                conn.execute(text("""
                    INSERT INTO learning_goals (
                        user_id, title, description, subject, target_date, progress, status, created_at
                    ) VALUES (
                        :user_id, :title, :description, :subject, :target_date, :progress, :status, :created_at
                    )
                """), {
                    "user_id": student[0],
                    "title": goal_data["title"],
                    "description": goal_data["description"],
                    "subject": goal_data["subject"],
                    "target_date": goal_data["target_date"],
                    "progress": goal_data["progress"],
                    "status": "active",
                    "created_at": datetime.utcnow()
                })
            
            # Commit les changements
            conn.commit()
            print(f"✅ {len(test_homeworks)} devoirs de test créés")
            print(f"✅ {len(test_goals)} objectifs de test créés")
            print("📊 Données de test créées avec succès !")
            
    except Exception as e:
        print(f"❌ Erreur lors de la création des données de test: {str(e)}")

if __name__ == "__main__":
    create_test_assignments_data() 