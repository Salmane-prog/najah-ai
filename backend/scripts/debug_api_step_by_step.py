#!/usr/bin/env python3
"""
Script pour déboguer étape par étape le calcul dans l'API
"""

import sqlite3
import os

def debug_api_step_by_step():
    print("🔍 Débogage étape par étape du calcul API")
    
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
        
        # 2. Étape 1: Récupérer tous les student_ids des classes du professeur
        cursor.execute("""
            SELECT DISTINCT cs.student_id
            FROM class_students cs
            JOIN class_groups cg ON cs.class_id = cg.id
            WHERE cg.teacher_id = ?
        """, (teacher_id,))
        
        all_student_ids = cursor.fetchall()
        print(f"\n📊 Étape 1 - Tous les student_ids ({len(all_student_ids)}):")
        for student_id_tuple in all_student_ids:
            student_id = student_id_tuple[0]
            print(f"   - Student ID: {student_id}")
        
        # 3. Étape 2: Vérifier le rôle de chaque étudiant
        print(f"\n🔍 Étape 2 - Vérification des rôles:")
        valid_student_ids = []
        for student_id_tuple in all_student_ids:
            student_id = student_id_tuple[0]
            cursor.execute("SELECT username, role FROM users WHERE id = ?", (student_id,))
            user_result = cursor.fetchone()
            if user_result:
                username, role = user_result
                print(f"   - {username} (ID: {student_id}): rôle = {role}")
                if role == 'student':
                    valid_student_ids.append(student_id)
                    print(f"     ✅ Ajouté (rôle étudiant)")
                else:
                    print(f"     ❌ Ignoré (rôle non-étudiant)")
            else:
                print(f"   - ID {student_id}: utilisateur non trouvé")
        
        print(f"\n📊 Résultats:")
        print(f"   - Total student_ids: {len(all_student_ids)}")
        print(f"   - Étudiants valides: {len(valid_student_ids)}")
        print(f"   - Étudiants valides: {valid_student_ids}")
        
        # 4. Comparer avec la requête qui fonctionne
        print(f"\n🔍 Comparaison avec la requête qui fonctionne:")
        cursor.execute("""
            SELECT DISTINCT cs.student_id, u.username, u.role
            FROM class_students cs
            JOIN class_groups cg ON cs.class_id = cg.id
            JOIN users u ON cs.student_id = u.id
            WHERE cg.teacher_id = ? AND u.role = 'student'
        """, (teacher_id,))
        
        working_students = cursor.fetchall()
        print(f"   - Requête qui fonctionne: {len(working_students)} étudiants")
        for student in working_students:
            student_id, username, role = student
            print(f"     - {username} (ID: {student_id}, rôle: {role})")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    debug_api_step_by_step() 