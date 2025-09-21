#!/usr/bin/env python3
"""
Script pour ajouter des données d'exemple dans les tables d'évaluation adaptative
"""

import sqlite3
import os
import json
from datetime import datetime, timedelta

def add_sample_adaptive_data():
    """Ajoute des données d'exemple pour les tests adaptatifs et évaluations formatives"""
    
    db_path = 'data/app.db'
    
    if not os.path.exists(db_path):
        print(f"❌ Base de données non trouvée: {db_path}")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("🔧 Ajout de données d'exemple pour l'évaluation adaptative...")
        print("=" * 60)
        
        # Vérifier si l'enseignant existe
        cursor.execute("SELECT id FROM users WHERE role = 'teacher' LIMIT 1")
        teacher_result = cursor.fetchone()
        
        if not teacher_result:
            print("❌ Aucun enseignant trouvé dans la base de données")
            return False
        
        teacher_id = teacher_result[0]
        print(f"✅ Enseignant trouvé: ID {teacher_id}")
        
        # 1. Ajouter des tests adaptatifs
        print("\n1️⃣ Ajout de tests adaptatifs...")
        
        adaptive_tests = [
            {
                "title": "Test de Grammaire Française Niveau Intermédiaire",
                "description": "Test adaptatif sur Français",
                "subject": "Français",
                "difficulty_range": "3-7",
                "total_questions": 15,
                "estimated_duration": 25,
                "created_by": teacher_id,
                "is_active": 1,
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat()
            },
            {
                "title": "Évaluation Mathématiques - Algèbre",
                "description": "Test adaptatif sur Mathématiques",
                "subject": "Mathématiques",
                "difficulty_range": "4-8",
                "total_questions": 20,
                "estimated_duration": 30,
                "created_by": teacher_id,
                "is_active": 1,
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat()
            },
            {
                "title": "Histoire - Révolution Française",
                "description": "Test adaptatif sur Histoire",
                "subject": "Histoire",
                "difficulty_range": "2-6",
                "total_questions": 15,
                "estimated_duration": 25,
                "created_by": teacher_id,
                "is_active": 1,
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat()
            }
        ]
        
        for test in adaptive_tests:
            cursor.execute("""
                INSERT INTO adaptive_tests 
                (title, description, subject, difficulty_range, total_questions, estimated_duration, created_by, is_active, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                test["title"], test["description"], test["subject"], test["difficulty_range"],
                test["total_questions"], test["estimated_duration"], test["created_by"],
                test["is_active"], test["created_at"], test["updated_at"]
            ))
            test_id = cursor.lastrowid
            print(f"   ✅ Test ajouté: {test['title']} (ID: {test_id})")
        
        # 2. Ajouter des évaluations formatives
        print("\n2️⃣ Ajout d'évaluations formatives...")
        
        formative_evaluations = [
            {
                "title": "Projet de Recherche - Écologie",
                "description": "Projet de recherche sur l'écologie",
                "subject": "Sciences",
                "evaluation_type": "project",
                "due_date": (datetime.now() + timedelta(days=30)).isoformat(),
                "total_points": 100,
                "criteria": json.dumps(["Recherche", "Présentation", "Analyse"]),
                "created_by": teacher_id,
                "is_active": 1,
                "status": "active",
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat()
            },
            {
                "title": "Présentation Orale - Littérature",
                "description": "Présentation orale sur la littérature",
                "subject": "Français",
                "evaluation_type": "presentation",
                "due_date": (datetime.now() + timedelta(days=25)).isoformat(),
                "total_points": 80,
                "criteria": json.dumps(["Contenu", "Présentation", "Interaction"]),
                "created_by": teacher_id,
                "is_active": 1,
                "status": "active",
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat()
            },
            {
                "title": "Discussion Critique - Philosophie",
                "description": "Discussion critique sur un sujet philosophique",
                "subject": "Philosophie",
                "evaluation_type": "discussion",
                "due_date": (datetime.now() + timedelta(days=35)).isoformat(),
                "total_points": 60,
                "criteria": json.dumps(["Argumentation", "Réflexion", "Participation"]),
                "created_by": teacher_id,
                "is_active": 1,
                "status": "active",
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat()
            }
        ]
        
        for evaluation in formative_evaluations:
            cursor.execute("""
                INSERT INTO formative_evaluations 
                (title, description, subject, evaluation_type, due_date, total_points, criteria, created_by, is_active, status, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                evaluation["title"], evaluation["description"], evaluation["subject"],
                evaluation["evaluation_type"], evaluation["due_date"], evaluation["total_points"],
                evaluation["criteria"], evaluation["created_by"], evaluation["is_active"],
                evaluation["status"], evaluation["created_at"], evaluation["updated_at"]
            ))
            eval_id = cursor.lastrowid
            print(f"   ✅ Évaluation ajoutée: {evaluation['title']} (ID: {eval_id})")
        
        # 3. Ajouter des attributions aux étudiants
        print("\n3️⃣ Ajout d'attributions aux étudiants...")
        
        # Récupérer les étudiants
        cursor.execute("SELECT id FROM users WHERE role = 'student' LIMIT 5")
        students = cursor.fetchall()
        
        if students:
            # Attribuer les tests adaptatifs
            cursor.execute("SELECT id FROM adaptive_tests")
            tests = cursor.fetchall()
            
            for test in tests:
                for student in students:
                    cursor.execute("""
                        INSERT INTO adaptive_test_assignments 
                        (test_id, student_id, assigned_by, assigned_at, status, total_questions, created_at, updated_at)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        test[0], student[0], teacher_id, datetime.now().isoformat(),
                        "assigned", 15, datetime.now().isoformat(), datetime.now().isoformat()
                    ))
            
            # Attribuer les évaluations formatives
            cursor.execute("SELECT id FROM formative_evaluations")
            evaluations = cursor.fetchall()
            
            for evaluation in evaluations:
                for student in students:
                    cursor.execute("""
                        INSERT INTO formative_evaluation_assignments 
                        (evaluation_id, student_id, assigned_by, assigned_at, due_date, status, created_at, updated_at)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        evaluation[0], student[0], teacher_id, datetime.now().isoformat(),
                        (datetime.now() + timedelta(days=30)).isoformat(), "assigned",
                        datetime.now().isoformat(), datetime.now().isoformat()
                    ))
            
            print(f"   ✅ Attributions ajoutées pour {len(students)} étudiants")
        
        conn.commit()
        print("\n✅ Données d'exemple ajoutées avec succès !")
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")
        return False

if __name__ == "__main__":
    add_sample_adaptive_data()
























