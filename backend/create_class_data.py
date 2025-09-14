#!/usr/bin/env python3
"""
Script pour créer des données de classes et assigner des étudiants
"""

import sqlite3
import os
from datetime import datetime

def create_class_data():
    """Créer des classes et assigner des étudiants"""
    
    db_path = "F:/IMT/stage/Yancode/Najah__AI/data/app.db"
    
    if not os.path.exists(db_path):
        print(f"❌ Base de données non trouvée: {db_path}")
        return
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("🏫 Création des données de classes...")
        
        # Créer des classes
        classes = [
            (1, "6ème A", "Niveau débutant", "Français, Mathématiques", 20),
            (2, "5ème B", "Niveau intermédiaire", "Sciences, Histoire", 18),
            (3, "4ème A", "Niveau avancé", "Littérature, Géographie", 22),
            (4, "3ème B", "Niveau expert", "Philosophie, Arts", 16)
        ]
        
        for class_id, name, description, subjects, max_students in classes:
            cursor.execute("""
                INSERT OR REPLACE INTO class_groups 
                (id, name, description, subjects, max_students, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                class_id, name, description, subjects, max_students,
                datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            ))
        
        print(f"✅ {len(classes)} classes créées")
        
        # Récupérer les étudiants
        cursor.execute("SELECT id, username FROM users WHERE role = 'student'")
        students = cursor.fetchall()
        
        print(f"👥 {len(students)} étudiants trouvés")
        
        # Assigner les étudiants aux classes
        class_assignments = [
            (1, 1), (2, 1), (3, 1),  # Étudiants 1,2,3 -> Classe 1
            (4, 2), (5, 2), (6, 2),  # Étudiants 4,5,6 -> Classe 2
            (7, 3), (8, 3), (9, 3),  # Étudiants 7,8,9 -> Classe 3
            (10, 4), (11, 4), (12, 4)  # Étudiants 10,11,12 -> Classe 4
        ]
        
        for student_id, class_id in class_assignments:
            if student_id <= len(students):  # Vérifier que l'étudiant existe
                cursor.execute("""
                    INSERT OR REPLACE INTO class_students 
                    (class_id, student_id, joined_at, status)
                    VALUES (?, ?, ?, ?)
                """, (
                    class_id, student_id,
                    datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'active'
                ))
        
        # Valider les changements
        conn.commit()
        print("✅ Données de classes créées avec succès !")
        
        # Afficher un résumé
        cursor.execute("SELECT COUNT(*) FROM class_groups")
        classes_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM class_students")
        assignments_count = cursor.fetchone()[0]
        
        print(f"📊 Résumé créé:")
        print(f"   - {classes_count} classes")
        print(f"   - {assignments_count} assignations d'étudiants")
        
    except Exception as e:
        print(f"❌ Erreur lors de la création: {str(e)}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    create_class_data() 