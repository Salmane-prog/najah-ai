#!/usr/bin/env python3
"""
Script pour déboguer la requête SQL exacte utilisée dans l'API
"""

import sqlite3
import os

def debug_api_query():
    print("🔍 Débogage de la requête SQL de l'API")
    
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
        
        # 2. Requête qui fonctionne (comme dans check_specific_teacher.py)
        print("\n📊 Requête qui fonctionne (6 étudiants):")
        cursor.execute("""
            SELECT DISTINCT 
                u.id, 
                u.username, 
                u.email, 
                u.role
            FROM users u
            JOIN class_students cs ON u.id = cs.student_id
            JOIN class_groups cg ON cs.class_id = cg.id
            WHERE cg.teacher_id = ? AND u.role = 'student'
            ORDER BY u.username
        """, (teacher_id,))
        
        working_students = cursor.fetchall()
        print(f"   Résultat: {len(working_students)} étudiants")
        for student in working_students:
            student_id, username, email, role = student
            print(f"   - {username} (ID: {student_id}, rôle: {role})")
        
        # 3. Requête comme dans l'API (avec DISTINCT et COUNT)
        print("\n🔧 Requête comme dans l'API:")
        cursor.execute("""
            SELECT COUNT(DISTINCT cs.student_id)
            FROM class_students cs
            JOIN class_groups cg ON cs.class_id = cg.id
            JOIN users u ON cs.student_id = u.id
            WHERE cg.teacher_id = ? AND u.role = 'student'
        """, (teacher_id,))
        
        api_count = cursor.fetchone()[0]
        print(f"   Résultat API: {api_count} étudiants")
        
        # 4. Vérifier les étudiants qui sont comptés dans l'API
        cursor.execute("""
            SELECT DISTINCT cs.student_id, u.username, u.role
            FROM class_students cs
            JOIN class_groups cg ON cs.class_id = cg.id
            JOIN users u ON cs.student_id = u.id
            WHERE cg.teacher_id = ? AND u.role = 'student'
            ORDER BY u.username
        """, (teacher_id,))
        
        api_students = cursor.fetchall()
        print(f"   Étudiants comptés par l'API ({len(api_students)}):")
        for student in api_students:
            student_id, username, role = student
            print(f"   - {username} (ID: {student_id}, rôle: {role})")
        
        # 5. Comparer les deux listes
        working_ids = {student[0] for student in working_students}
        api_ids = {student[0] for student in api_students}
        
        print(f"\n🔍 Comparaison:")
        print(f"   - Requête qui fonctionne: {len(working_ids)} étudiants")
        print(f"   - Requête API: {len(api_ids)} étudiants")
        
        if working_ids == api_ids:
            print("   ✅ Les deux requêtes donnent le même résultat")
        else:
            print("   ❌ Les requêtes donnent des résultats différents")
            missing_in_api = working_ids - api_ids
            extra_in_api = api_ids - working_ids
            
            if missing_in_api:
                print(f"   - Manquants dans l'API: {missing_in_api}")
            if extra_in_api:
                print(f"   - En trop dans l'API: {extra_in_api}")
        
        # 6. Vérifier les assignations de classes
        print(f"\n🏫 Assignations de classes:")
        cursor.execute("""
            SELECT cs.student_id, u.username, cg.name, cg.id
            FROM class_students cs
            JOIN users u ON cs.student_id = u.id
            JOIN class_groups cg ON cs.class_id = cg.id
            WHERE cg.teacher_id = ? AND u.role = 'student'
            ORDER BY u.username, cg.name
        """, (teacher_id,))
        
        assignments = cursor.fetchall()
        for assignment in assignments:
            student_id, username, class_name, class_id = assignment
            print(f"   - {username} (ID: {student_id}) dans {class_name} (ID: {class_id})")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    debug_api_query() 