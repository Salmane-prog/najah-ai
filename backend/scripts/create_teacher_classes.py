#!/usr/bin/env python3
"""
Script pour créer des classes et assigner des élèves au professeur teacher@test.com
"""

import sqlite3
import os
from datetime import datetime

def create_teacher_classes():
    print("🏫 Création de classes pour teacher@test.com...")
    
    # Chemin vers la base de données
    db_path = "data/app.db"
    
    if not os.path.exists(db_path):
        print(f"❌ Base de données non trouvée: {db_path}")
        return
    
    try:
        # Connexion à la base de données
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 1. Récupérer l'ID du professeur
        cursor.execute("SELECT id FROM users WHERE email = 'teacher@test.com'")
        teacher_result = cursor.fetchone()
        
        if not teacher_result:
            print("❌ Professeur teacher@test.com non trouvé")
            return
        
        teacher_id = teacher_result[0]
        print(f"✅ Professeur trouvé: ID={teacher_id}")
        
        # 2. Créer des classes pour le professeur
        classes_data = [
            ("Mathématiques Avancées", "advanced", "Mathématiques", teacher_id),
            ("Français Littéraire", "intermediate", "Français", teacher_id),
            ("Sciences Expérimentales", "beginner", "Sciences", teacher_id),
            ("Histoire Moderne", "intermediate", "Histoire", teacher_id)
        ]
        
        created_classes = []
        for class_name, level, subject, teacher_id in classes_data:
            cursor.execute("""
                INSERT INTO class_groups (name, level, subject, teacher_id, created_at)
                VALUES (?, ?, ?, ?, ?)
            """, (class_name, level, subject, teacher_id, datetime.utcnow()))
            
            class_id = cursor.lastrowid
            created_classes.append((class_id, class_name))
            print(f"   ✅ Classe créée: {class_name} (ID: {class_id})")
        
        # 3. Récupérer tous les élèves
        cursor.execute("SELECT id FROM users WHERE role = 'student'")
        students = cursor.fetchall()
        student_ids = [student[0] for student in students]
        
        print(f"\n👥 {len(student_ids)} élèves trouvés")
        
        # 4. Assigner les élèves aux classes
        assignments = [
            # Mathématiques Avancées (classe 1)
            (student_ids[0], created_classes[0][0]),  # student1
            (student_ids[1], created_classes[0][0]),  # student2
            (student_ids[2], created_classes[0][0]),  # student3
            
            # Français Littéraire (classe 2)
            (student_ids[3], created_classes[1][0]),  # student_test
            (student_ids[4], created_classes[1][0]),  # marie.dubois
            (student_ids[5], created_classes[1][0]),  # jean.martin
            
            # Sciences Expérimentales (classe 3)
            (student_ids[6], created_classes[2][0]),  # sophie.bernard
            (student_ids[7], created_classes[2][0]),  # pierre.durand
        ]
        
        for student_id, class_id in assignments:
            cursor.execute("""
                INSERT INTO class_students (student_id, class_id, enrolled_at)
                VALUES (?, ?, ?)
            """, (student_id, class_id, datetime.utcnow()))
            print(f"   ✅ Élève {student_id} assigné à la classe {class_id}")
        
        conn.commit()
        print(f"\n✅ {len(created_classes)} classes créées avec {len(assignments)} assignations d'élèves")
        
        # 5. Vérifier les classes créées
        cursor.execute("""
            SELECT cg.id, cg.name, cg.level, cg.subject, COUNT(cs.student_id) as student_count
            FROM class_groups cg
            LEFT JOIN class_students cs ON cg.id = cs.class_id
            WHERE cg.teacher_id = ?
            GROUP BY cg.id
        """, (teacher_id,))
        
        classes_info = cursor.fetchall()
        print(f"\n📊 Classes du professeur:")
        for class_info in classes_info:
            print(f"   - {class_info[1]} ({class_info[2]}): {class_info[4]} élèves")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    create_teacher_classes() 