#!/usr/bin/env python3
"""
Script pour vérifier les données d'assignations dans la base
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine, text

def check_assignments_data():
    """Vérifier les données d'assignations dans la base"""
    
    # Créer une connexion directe à la base de données
    engine = create_engine("sqlite:///../data/app.db")
    
    try:
        with engine.connect() as conn:
            print("🔍 Vérification des données d'assignations")
            print("=" * 50)
            
            # 1. Vérifier les devoirs
            print("\n📝 Devoirs:")
            result = conn.execute(text("SELECT COUNT(*) FROM homework"))
            homework_count = result.fetchone()[0]
            print(f"   Total: {homework_count}")
            
            if homework_count > 0:
                result = conn.execute(text("""
                    SELECT h.id, h.title, h.subject, h.status, h.priority, h.due_date,
                           u1.username as assigned_by, u2.username as assigned_to
                    FROM homework h
                    LEFT JOIN users u1 ON h.assigned_by = u1.id
                    LEFT JOIN users u2 ON h.assigned_to = u2.id
                    LIMIT 5
                """))
                homeworks = result.fetchall()
                for hw in homeworks:
                    print(f"   - {hw[1]} ({hw[2]}) - Status: {hw[3]}, Priorité: {hw[4]}")
                    print(f"     Assigné par: {hw[6]}, Assigné à: {hw[7]}")
                    print(f"     Date limite: {hw[5]}")
            
            # 2. Vérifier les objectifs d'apprentissage
            print("\n🎯 Objectifs d'apprentissage:")
            result = conn.execute(text("SELECT COUNT(*) FROM learning_goals"))
            goals_count = result.fetchone()[0]
            print(f"   Total: {goals_count}")
            
            if goals_count > 0:
                result = conn.execute(text("""
                    SELECT lg.id, lg.title, lg.subject, lg.status, lg.progress, lg.target_date,
                           u.username as user
                    FROM learning_goals lg
                    LEFT JOIN users u ON lg.user_id = u.id
                    LIMIT 5
                """))
                goals = result.fetchall()
                for goal in goals:
                    print(f"   - {goal[1]} ({goal[2]}) - Status: {goal[3]}, Progression: {goal[4]*100}%")
                    print(f"     Utilisateur: {goal[6]}, Date cible: {goal[5]}")
            
            # 3. Vérifier les classes
            print("\n📚 Classes:")
            result = conn.execute(text("SELECT COUNT(*) FROM class_groups"))
            classes_count = result.fetchone()[0]
            print(f"   Total: {classes_count}")
            
            if classes_count > 0:
                result = conn.execute(text("""
                    SELECT cg.id, cg.name, cg.subject, cg.level, u.username as teacher
                    FROM class_groups cg
                    LEFT JOIN users u ON cg.teacher_id = u.id
                    LIMIT 5
                """))
                classes = result.fetchall()
                for cls in classes:
                    print(f"   - {cls[1]} ({cls[2]}) - Niveau: {cls[3]}, Professeur: {cls[4]}")
            
            # 4. Vérifier les étudiants par classe
            print("\n👥 Étudiants par classe:")
            result = conn.execute(text("""
                SELECT cg.name as class_name, COUNT(cs.student_id) as student_count
                FROM class_groups cg
                LEFT JOIN class_students cs ON cg.id = cs.class_id
                GROUP BY cg.id, cg.name
            """))
            class_students = result.fetchall()
            for cs in class_students:
                print(f"   - {cs[0]}: {cs[1]} étudiants")
            
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")

if __name__ == "__main__":
    check_assignments_data() 