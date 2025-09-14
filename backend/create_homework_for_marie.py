#!/usr/bin/env python3
"""
Script pour créer des devoirs pour marie.dubois
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine, text
from datetime import datetime, timedelta

def create_homework_for_marie():
    """Créer des devoirs pour marie.dubois"""
    
    # Créer une connexion directe à la base de données
    engine = create_engine("sqlite:///../data/app.db")
    
    try:
        with engine.connect() as conn:
            # 1. Trouver marie.dubois (professeur)
            teacher_result = conn.execute(text("""
                SELECT id, username, email FROM users 
                WHERE email = 'marie.dubois@najah.ai' AND role = 'teacher'
            """))
            teacher = teacher_result.fetchone()
            
            if not teacher:
                print("❌ Professeur marie.dubois non trouvé")
                return
            
            print(f"✅ Professeur trouvé: {teacher[1]} (ID: {teacher[0]})")
            
            # 2. Trouver une classe de ce professeur
            class_result = conn.execute(text("""
                SELECT id, name, subject FROM class_groups 
                WHERE teacher_id = :teacher_id LIMIT 1
            """), {"teacher_id": teacher[0]})
            class_group = class_result.fetchone()
            
            if not class_group:
                print("❌ Aucune classe trouvée pour ce professeur")
                return
            
            print(f"✅ Classe trouvée: {class_group[1]} ({class_group[2]}) - ID: {class_group[0]}")
            
            # 3. Trouver les étudiants de cette classe
            students_result = conn.execute(text("""
                SELECT cs.student_id, u.username, u.email
                FROM class_students cs
                JOIN users u ON cs.student_id = u.id
                WHERE cs.class_id = :class_id
            """), {"class_id": class_group[0]})
            students = students_result.fetchall()
            
            if not students:
                print("❌ Aucun étudiant trouvé dans cette classe")
                return
            
            print(f"✅ {len(students)} étudiants trouvés dans la classe")
            
            # 4. Créer des devoirs pour chaque étudiant
            print("📝 Création de devoirs...")
            
            # Supprimer les anciens devoirs de ce professeur
            conn.execute(text("DELETE FROM homework WHERE assigned_by = :teacher_id"), {
                "teacher_id": teacher[0]
            })
            
            test_homeworks = [
                {
                    "title": "Devoir de français - Analyse littéraire",
                    "description": "Analyser le poème 'Le Lac' de Lamartine et expliquer les thèmes principaux",
                    "subject": "Français",
                    "priority": "high",
                    "estimated_time": 90,
                    "due_date": datetime.now() + timedelta(days=5)
                },
                {
                    "title": "Rédaction d'histoire - Les Lumières",
                    "description": "Écrire une dissertation sur l'influence des Lumières sur la Révolution française",
                    "subject": "Histoire",
                    "priority": "medium",
                    "estimated_time": 120,
                    "due_date": datetime.now() + timedelta(days=10)
                },
                {
                    "title": "Devoir de mathématiques - Géométrie",
                    "description": "Résoudre les exercices 1 à 8 du chapitre sur les triangles",
                    "subject": "Mathématiques",
                    "priority": "medium",
                    "estimated_time": 60,
                    "due_date": datetime.now() + timedelta(days=7)
                }
            ]
            
            created_count = 0
            for homework_data in test_homeworks:
                for student in students:
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
                        "class_id": class_group[0],
                        "assigned_by": teacher[0],
                        "assigned_to": student[0],
                        "due_date": homework_data["due_date"],
                        "status": "pending",
                        "priority": homework_data["priority"],
                        "estimated_time": homework_data["estimated_time"],
                        "created_at": datetime.utcnow()
                    })
                    created_count += 1
            
            # Commit les changements
            conn.commit()
            print(f"✅ {created_count} devoirs créés pour {len(students)} étudiants")
            print("📊 Devoirs créés avec succès pour marie.dubois !")
            
    except Exception as e:
        print(f"❌ Erreur lors de la création des devoirs: {str(e)}")

if __name__ == "__main__":
    create_homework_for_marie() 