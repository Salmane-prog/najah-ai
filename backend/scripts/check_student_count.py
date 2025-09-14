#!/usr/bin/env python3
"""
Script pour vérifier le nombre d'élèves et comprendre la différence
"""

import sqlite3
import os

def check_student_count():
    print("🔍 Vérification du nombre d'élèves...")
    
    # Chemin vers la base de données
    db_path = "data/app.db"
    
    if not os.path.exists(db_path):
        print(f"❌ Base de données non trouvée: {db_path}")
        return
    
    try:
        # Connexion à la base de données
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 1. Nombre total d'élèves
        cursor.execute("SELECT COUNT(*) FROM users WHERE role = 'student'")
        total_students = cursor.fetchone()[0]
        print(f"📊 Nombre total d'élèves: {total_students}")
        
        # 2. Liste de tous les élèves
        cursor.execute("SELECT id, username, email FROM users WHERE role = 'student'")
        students = cursor.fetchall()
        print(f"\n👥 Liste des élèves:")
        for student in students:
            print(f"   - ID: {student[0]}, Username: {student[1]}, Email: {student[2]}")
        
        # 3. Classes du professeur teacher@test.com
        cursor.execute("""
            SELECT cg.id, cg.name, cg.teacher_id, u.username 
            FROM class_groups cg 
            JOIN users u ON cg.teacher_id = u.id 
            WHERE u.email = 'teacher@test.com'
        """)
        teacher_classes = cursor.fetchall()
        print(f"\n🏫 Classes du professeur teacher@test.com:")
        for class_info in teacher_classes:
            print(f"   - ID: {class_info[0]}, Nom: {class_info[1]}, Teacher: {class_info[3]}")
        
        # 4. Élèves dans les classes du professeur
        if teacher_classes:
            class_ids = [str(class_info[0]) for class_info in teacher_classes]
            class_ids_str = ','.join(class_ids)
            
            cursor.execute(f"""
                SELECT cs.student_id, u.username, u.email, cs.class_id, cg.name
                FROM class_students cs
                JOIN users u ON cs.student_id = u.id
                JOIN class_groups cg ON cs.class_id = cg.id
                WHERE cs.class_id IN ({class_ids_str})
            """)
            enrolled_students = cursor.fetchall()
            
            print(f"\n📚 Élèves inscrits dans les classes du professeur:")
            unique_students = set()
            for student in enrolled_students:
                unique_students.add(student[0])
                print(f"   - ID: {student[0]}, Username: {student[1]}, Email: {student[2]}, Classe: {student[4]}")
            
            print(f"\n📈 Résumé:")
            print(f"   - Total élèves: {total_students}")
            print(f"   - Élèves dans les classes du prof: {len(unique_students)}")
            print(f"   - Différence: {total_students - len(unique_students)} élèves non assignés")
        else:
            print(f"\n⚠️ Aucune classe trouvée pour teacher@test.com")
        
        # 5. Vérifier les quiz résultats
        cursor.execute("SELECT COUNT(*) FROM quiz_results")
        total_quiz_results = cursor.fetchone()[0]
        print(f"\n📝 Total quiz résultats: {total_quiz_results}")
        
        # 6. Quiz résultats par professeur
        cursor.execute("""
            SELECT u.username, COUNT(qr.id) as quiz_count
            FROM quiz_results qr
            JOIN users u ON qr.user_id = u.id
            WHERE u.role = 'student'
            GROUP BY u.username
        """)
        quiz_by_student = cursor.fetchall()
        print(f"\n📊 Quiz par étudiant:")
        for student in quiz_by_student:
            print(f"   - {student[0]}: {student[1]} quiz")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    check_student_count() 