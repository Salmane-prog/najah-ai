#!/usr/bin/env python3
"""
Script pour vérifier quels étudiants appartiennent à un professeur spécifique
"""

import sqlite3
import os

def check_teacher_students(teacher_email="teacher@test.com"):
    print(f"👨‍🏫 Vérification des étudiants du professeur: {teacher_email}")
    
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
        cursor.execute("SELECT id, username FROM users WHERE email = ?", (teacher_email,))
        teacher_result = cursor.fetchone()
        
        if not teacher_result:
            print(f"❌ Professeur {teacher_email} non trouvé")
            return
        
        teacher_id, teacher_username = teacher_result
        print(f"✅ Professeur trouvé: {teacher_username} (ID: {teacher_id})")
        
        # 2. Récupérer toutes les classes du professeur
        cursor.execute("""
            SELECT id, name, subject, level 
            FROM class_groups 
            WHERE teacher_id = ?
        """, (teacher_id,))
        
        classes = cursor.fetchall()
        print(f"\n🏫 Classes du professeur ({len(classes)}):")
        
        if not classes:
            print("   ⚠️ Aucune classe trouvée pour ce professeur")
            return
        
        for class_info in classes:
            class_id, class_name, subject, level = class_info
            print(f"   - {class_name} (ID: {class_id}) - {subject} ({level})")
        
        # 3. Récupérer tous les étudiants de ce professeur
        cursor.execute("""
            SELECT DISTINCT 
                u.id, 
                u.username, 
                u.email, 
                u.first_name, 
                u.last_name,
                cg.name as class_name,
                cs.enrolled_at
            FROM users u
            JOIN class_students cs ON u.id = cs.student_id
            JOIN class_groups cg ON cs.class_id = cg.id
            WHERE cg.teacher_id = ? AND u.role = 'student'
            ORDER BY u.username
        """, (teacher_id,))
        
        students = cursor.fetchall()
        print(f"\n👥 Étudiants du professeur ({len(students)}):")
        
        if not students:
            print("   ⚠️ Aucun étudiant trouvé pour ce professeur")
        else:
            for student in students:
                student_id, username, email, first_name, last_name, class_name, enrolled_at = student
                name = f"{first_name} {last_name}".strip() if first_name and last_name else username
                print(f"   - {name} ({email}) dans {class_name}")
        
        # 4. Statistiques détaillées
        print(f"\n📊 Statistiques:")
        print(f"   - Nombre de classes: {len(classes)}")
        print(f"   - Nombre d'étudiants: {len(students)}")
        
        # 5. Vérifier les quiz des étudiants de ce professeur
        if students:
            student_ids = [str(student[0]) for student in students]
            student_ids_str = ','.join(student_ids)
            
            cursor.execute(f"""
                SELECT u.username, COUNT(qr.id) as quiz_count, AVG(qr.score) as avg_score
                FROM users u
                LEFT JOIN quiz_results qr ON u.id = qr.user_id
                WHERE u.id IN ({student_ids_str})
                GROUP BY u.id, u.username
            """)
            
            quiz_stats = cursor.fetchall()
            print(f"\n📝 Statistiques des quiz:")
            for stat in quiz_stats:
                username, quiz_count, avg_score = stat
                avg_score = avg_score or 0
                print(f"   - {username}: {quiz_count} quiz, score moyen: {avg_score:.1f}%")
        
        # 6. Vérifier les assignations dans la table class_students
        print(f"\n🔍 Vérification des assignations dans class_students:")
        cursor.execute("""
            SELECT cs.student_id, cs.class_id, u.username, cg.name
            FROM class_students cs
            JOIN users u ON cs.student_id = u.id
            JOIN class_groups cg ON cs.class_id = cg.id
            WHERE cg.teacher_id = ?
            ORDER BY u.username
        """, (teacher_id,))
        
        assignments = cursor.fetchall()
        print(f"   Total assignations: {len(assignments)}")
        for assignment in assignments:
            student_id, class_id, username, class_name = assignment
            print(f"   - Élève {username} (ID: {student_id}) dans classe {class_name} (ID: {class_id})")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Erreur: {e}")

def check_all_teachers():
    print("\n" + "="*50)
    print("👨‍🏫 Vérification de tous les professeurs")
    print("="*50)
    
    db_path = "data/app.db"
    
    if not os.path.exists(db_path):
        print(f"❌ Base de données non trouvée: {db_path}")
        return
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Récupérer tous les professeurs
        cursor.execute("SELECT id, username, email FROM users WHERE role = 'teacher'")
        teachers = cursor.fetchall()
        
        for teacher in teachers:
            teacher_id, username, email = teacher
            print(f"\n👨‍🏫 Professeur: {username} ({email})")
            
            # Compter les classes
            cursor.execute("SELECT COUNT(*) FROM class_groups WHERE teacher_id = ?", (teacher_id,))
            class_count = cursor.fetchone()[0]
            
            # Compter les étudiants
            cursor.execute("""
                SELECT COUNT(DISTINCT cs.student_id) 
                FROM class_students cs
                JOIN class_groups cg ON cs.class_id = cg.id
                WHERE cg.teacher_id = ?
            """, (teacher_id,))
            
            student_count = cursor.fetchone()[0]
            
            print(f"   - Classes: {class_count}")
            print(f"   - Étudiants: {student_count}")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    # Vérifier un professeur spécifique
    check_teacher_students("teacher@test.com")
    
    # Vérifier tous les professeurs
    check_all_teachers() 