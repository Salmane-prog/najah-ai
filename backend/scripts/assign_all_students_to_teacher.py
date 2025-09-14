#!/usr/bin/env python3
"""
Script pour assigner tous les élèves au professeur teacher@test.com
"""

import sqlite3
import os
from datetime import datetime

def assign_all_students_to_teacher():
    print("👥 Assignation de tous les élèves au professeur teacher@test.com...")
    
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
        
        # 2. Vérifier s'il a déjà des classes
        cursor.execute("SELECT id, name FROM class_groups WHERE teacher_id = ?", (teacher_id,))
        existing_classes = cursor.fetchall()
        
        if not existing_classes:
            print("⚠️ Aucune classe trouvée pour le professeur. Création d'une classe par défaut...")
            
            # Créer une classe par défaut
            cursor.execute("""
                INSERT INTO class_groups (name, level, subject, teacher_id, created_at)
                VALUES (?, ?, ?, ?, ?)
            """, ("Classe Générale", "intermediate", "Général", teacher_id, datetime.utcnow()))
            
            class_id = cursor.lastrowid
            print(f"✅ Classe créée: Classe Générale (ID: {class_id})")
            existing_classes = [(class_id, "Classe Générale")]
        else:
            print(f"✅ {len(existing_classes)} classes trouvées pour le professeur")
            for class_info in existing_classes:
                print(f"   - {class_info[1]} (ID: {class_info[0]})")
        
        # 3. Récupérer tous les élèves
        cursor.execute("SELECT id, username, email FROM users WHERE role = 'student'")
        students = cursor.fetchall()
        print(f"\n👥 {len(students)} élèves trouvés")
        
        # 4. Assigner tous les élèves à la première classe du professeur
        class_id = existing_classes[0][0]
        assignments_count = 0
        
        for student in students:
            student_id = student[0]
            student_username = student[1]
            
            # Vérifier si l'élève est déjà assigné à cette classe
            cursor.execute("""
                SELECT COUNT(*) FROM class_students 
                WHERE student_id = ? AND class_id = ?
            """, (student_id, class_id))
            
            already_assigned = cursor.fetchone()[0] > 0
            
            if not already_assigned:
                cursor.execute("""
                    INSERT INTO class_students (student_id, class_id, enrolled_at)
                    VALUES (?, ?, ?)
                """, (student_id, class_id, datetime.utcnow()))
                
                print(f"   ✅ Élève {student_username} assigné à la classe")
                assignments_count += 1
            else:
                print(f"   ⏭️ Élève {student_username} déjà assigné")
        
        conn.commit()
        print(f"\n✅ {assignments_count} nouveaux élèves assignés au professeur")
        
        # 5. Vérifier le résultat
        cursor.execute("""
            SELECT COUNT(DISTINCT cs.student_id) as student_count
            FROM class_students cs
            JOIN class_groups cg ON cs.class_id = cg.id
            WHERE cg.teacher_id = ?
        """, (teacher_id,))
        
        total_students = cursor.fetchone()[0]
        print(f"📊 Total élèves assignés au professeur: {total_students}")
        
        # 6. Afficher la liste des élèves assignés
        cursor.execute("""
            SELECT u.username, u.email, cg.name as class_name
            FROM class_students cs
            JOIN users u ON cs.student_id = u.id
            JOIN class_groups cg ON cs.class_id = cg.id
            WHERE cg.teacher_id = ?
            ORDER BY u.username
        """, (teacher_id,))
        
        assigned_students = cursor.fetchall()
        print(f"\n📋 Élèves assignés au professeur:")
        for student in assigned_students:
            print(f"   - {student[0]} ({student[1]}) dans {student[2]}")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    assign_all_students_to_teacher() 