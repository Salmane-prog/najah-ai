#!/usr/bin/env python3
"""
Script pour vérifier les classes dans la base de données
"""

import sqlite3
import os

def check_classes():
    print("🔍 Vérification des classes...")
    
    # Chemin vers la base de données
    db_path = "data/app.db"
    
    if not os.path.exists(db_path):
        print(f"❌ Base de données non trouvée: {db_path}")
        return
    
    try:
        # Connexion à la base de données
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 1. Vérifier toutes les classes
        cursor.execute("SELECT id, name, teacher_id, subject, level FROM class_groups")
        classes = cursor.fetchall()
        print(f"📊 Total classes: {len(classes)}")
        
        for class_info in classes:
            print(f"   - ID: {class_info[0]}, Nom: {class_info[1]}, Teacher: {class_info[2]}, Sujet: {class_info[3]}, Niveau: {class_info[4]}")
        
        # 2. Vérifier les professeurs
        cursor.execute("SELECT id, username, email FROM users WHERE role = 'teacher'")
        teachers = cursor.fetchall()
        print(f"\n👨‍🏫 Professeurs:")
        for teacher in teachers:
            print(f"   - ID: {teacher[0]}, Username: {teacher[1]}, Email: {teacher[2]}")
        
        # 3. Vérifier les assignations d'élèves
        cursor.execute("""
            SELECT cs.student_id, cs.class_id, u.username, cg.name
            FROM class_students cs
            JOIN users u ON cs.student_id = u.id
            JOIN class_groups cg ON cs.class_id = cg.id
        """)
        assignments = cursor.fetchall()
        print(f"\n📚 Assignations d'élèves ({len(assignments)}):")
        for assignment in assignments:
            print(f"   - Élève {assignment[2]} (ID: {assignment[0]}) dans classe {assignment[3]} (ID: {assignment[1]})")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    check_classes() 