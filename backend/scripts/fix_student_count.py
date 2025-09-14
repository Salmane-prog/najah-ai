#!/usr/bin/env python3
"""
Script pour corriger le calcul des étudiants dans l'API
"""

import sqlite3
import os

def fix_student_count():
    print("🔧 Correction du calcul des étudiants")
    
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
        
        # 2. Vérifier les classes du professeur
        cursor.execute("""
            SELECT id, name FROM class_groups WHERE teacher_id = ?
        """, (teacher_id,))
        
        classes = cursor.fetchall()
        print(f"\n🏫 Classes du professeur ({len(classes)}):")
        for class_info in classes:
            class_id, class_name = class_info
            print(f"   - {class_name} (ID: {class_id})")
        
        # 3. Vérifier les étudiants de chaque classe
        total_students = 0
        for class_info in classes:
            class_id, class_name = class_info
            cursor.execute("""
                SELECT COUNT(DISTINCT cs.student_id)
                FROM class_students cs
                JOIN users u ON cs.student_id = u.id
                WHERE cs.class_id = ? AND u.role = 'student'
            """, (class_id,))
            
            student_count = cursor.fetchone()[0]
            print(f"   - {class_name}: {student_count} étudiants")
            total_students += student_count
        
        # 4. Vérifier les étudiants uniques (sans doublons)
        cursor.execute("""
            SELECT COUNT(DISTINCT cs.student_id)
            FROM class_students cs
            JOIN class_groups cg ON cs.class_id = cg.id
            JOIN users u ON cs.student_id = u.id
            WHERE cg.teacher_id = ? AND u.role = 'student'
        """, (teacher_id,))
        
        unique_students = cursor.fetchone()[0]
        print(f"\n📊 Résultats:")
        print(f"   - Total assignations: {total_students}")
        print(f"   - Étudiants uniques: {unique_students}")
        
        # 5. Lister les étudiants uniques
        cursor.execute("""
            SELECT DISTINCT u.id, u.username, u.email
            FROM class_students cs
            JOIN class_groups cg ON cs.class_id = cg.id
            JOIN users u ON cs.student_id = u.id
            WHERE cg.teacher_id = ? AND u.role = 'student'
            ORDER BY u.username
        """, (teacher_id,))
        
        students = cursor.fetchall()
        print(f"\n👥 Étudiants uniques ({len(students)}):")
        for student in students:
            student_id, username, email = student
            print(f"   - {username} ({email})")
        
        conn.close()
        
        print(f"\n✅ Le professeur {teacher_username} a {unique_students} étudiants uniques dans {len(classes)} classes")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    fix_student_count() 