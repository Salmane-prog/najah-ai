#!/usr/bin/env python3
"""
Script pour déboguer le calcul des étudiants et comparer les requêtes SQL
"""

import sqlite3
import os

def debug_student_count():
    print("🔍 Débogage du calcul des étudiants pour marie.dubois@najah.ai")
    
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
        cursor.execute("SELECT id, username FROM users WHERE email = ?", ("marie.dubois@najah.ai",))
        teacher_result = cursor.fetchone()
        
        if not teacher_result:
            print("❌ Professeur marie.dubois@najah.ai non trouvé")
            return
        
        teacher_id, teacher_username = teacher_result
        print(f"✅ Professeur trouvé: {teacher_username} (ID: {teacher_id})")
        
        # 2. Requête originale (sans DISTINCT)
        cursor.execute("""
            SELECT cs.student_id, u.username, cg.name as class_name
            FROM class_students cs
            JOIN users u ON cs.student_id = u.id
            JOIN class_groups cg ON cs.class_id = cg.id
            WHERE cg.teacher_id = ? AND u.role = 'student'
            ORDER BY u.username
        """, (teacher_id,))
        
        all_assignments = cursor.fetchall()
        print(f"\n📊 Toutes les assignations ({len(all_assignments)}):")
        for assignment in all_assignments:
            student_id, username, class_name = assignment
            print(f"   - Élève {username} (ID: {student_id}) dans {class_name}")
        
        # 3. Requête avec DISTINCT (comme dans le dashboard)
        cursor.execute("""
            SELECT DISTINCT cs.student_id, u.username
            FROM class_students cs
            JOIN users u ON cs.student_id = u.id
            JOIN class_groups cg ON cs.class_id = cg.id
            WHERE cg.teacher_id = ? AND u.role = 'student'
            ORDER BY u.username
        """, (teacher_id,))
        
        distinct_students = cursor.fetchall()
        print(f"\n👥 Étudiants uniques ({len(distinct_students)}):")
        for student in distinct_students:
            student_id, username = student
            print(f"   - {username} (ID: {student_id})")
        
        # 4. Vérifier les classes du professeur
        cursor.execute("""
            SELECT id, name, subject, level 
            FROM class_groups 
            WHERE teacher_id = ?
        """, (teacher_id,))
        
        classes = cursor.fetchall()
        print(f"\n🏫 Classes du professeur ({len(classes)}):")
        for class_info in classes:
            class_id, class_name, subject, level = class_info
            print(f"   - {class_name} (ID: {class_id}) - {subject} ({level})")
        
        # 5. Compter les étudiants par classe
        for class_info in classes:
            class_id, class_name, subject, level = class_info
            cursor.execute("""
                SELECT COUNT(cs.student_id)
                FROM class_students cs
                JOIN users u ON cs.student_id = u.id
                WHERE cs.class_id = ? AND u.role = 'student'
            """, (class_id,))
            
            student_count = cursor.fetchone()[0]
            print(f"   - {class_name}: {student_count} étudiants")
        
        # 6. Vérifier s'il y a des étudiants dans plusieurs classes
        cursor.execute("""
            SELECT cs.student_id, u.username, COUNT(cs.class_id) as class_count
            FROM class_students cs
            JOIN users u ON cs.student_id = u.id
            JOIN class_groups cg ON cs.class_id = cg.id
            WHERE cg.teacher_id = ? AND u.role = 'student'
            GROUP BY cs.student_id, u.username
            HAVING COUNT(cs.class_id) > 1
        """, (teacher_id,))
        
        multi_class_students = cursor.fetchall()
        print(f"\n🔄 Étudiants dans plusieurs classes ({len(multi_class_students)}):")
        for student in multi_class_students:
            student_id, username, class_count = student
            print(f"   - {username} (ID: {student_id}): {class_count} classes")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    debug_student_count() 