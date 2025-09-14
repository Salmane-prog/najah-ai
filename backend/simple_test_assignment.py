#!/usr/bin/env python3
"""
Script de test simplifié pour vérifier l'assignation de quiz
"""
import sqlite3
import os
from datetime import datetime

def test_quiz_assignment_simple():
    # Chemin vers la base de données
    db_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'app.db')
    
    if not os.path.exists(db_path):
        print(f"❌ Base de données non trouvée: {db_path}")
        return False
    
    print(f"🔍 Vérification de la base de données: {db_path}")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # 1. Vérifier les tables existantes
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        print(f"📋 Tables trouvées: {tables}")
        
        # 2. Vérifier les utilisateurs
        cursor.execute("SELECT id, email, role FROM users LIMIT 5")
        users = cursor.fetchall()
        print(f"👥 Utilisateurs trouvés: {len(users)}")
        for user in users:
            print(f"   - ID: {user[0]}, Email: {user[1]}, Rôle: {user[2]}")
        
        # 3. Vérifier les quiz
        cursor.execute("SELECT id, title, subject FROM quizzes LIMIT 5")
        quizzes = cursor.fetchall()
        print(f"📝 Quiz trouvés: {len(quizzes)}")
        for quiz in quizzes:
            print(f"   - ID: {quiz[0]}, Titre: {quiz[1]}, Sujet: {quiz[2]}")
        
        # 4. Vérifier les assignations
        cursor.execute("SELECT id, quiz_id, student_id, class_id, assigned_at FROM quiz_assignments")
        assignments = cursor.fetchall()
        print(f"📋 Assignations trouvées: {len(assignments)}")
        for assignment in assignments:
            print(f"   - ID: {assignment[0]}, Quiz: {assignment[1]}, Étudiant: {assignment[2]}, Classe: {assignment[3]}, Date: {assignment[4]}")
        
        # 5. Vérifier les classes
        cursor.execute("SELECT id, name, teacher_id FROM class_groups LIMIT 5")
        classes = cursor.fetchall()
        print(f"🏫 Classes trouvées: {len(classes)}")
        for class_group in classes:
            print(f"   - ID: {class_group[0]}, Nom: {class_group[1]}, Prof: {class_group[2]}")
        
        # 6. Test d'assignation pour un étudiant spécifique
        student_email = "hajoujis47@gmail.com"  # Corrigé : sans 'w'
        cursor.execute("SELECT id FROM users WHERE email = ?", (student_email,))
        student = cursor.fetchone()
        
        if student:
            student_id = student[0]
            print(f"\n🎯 Test pour l'étudiant {student_email} (ID: {student_id})")
            
            # Vérifier les assignations de cet étudiant
            cursor.execute("""
                SELECT qa.id, qa.quiz_id, qa.assigned_at, q.title, q.subject
                FROM quiz_assignments qa
                JOIN quizzes q ON qa.quiz_id = q.id
                WHERE qa.student_id = ?
            """, (student_id,))
            
            student_assignments = cursor.fetchall()
            print(f"📚 Quiz assignés à cet étudiant: {len(student_assignments)}")
            
            for assignment in student_assignments:
                print(f"   - Quiz: {assignment[4]} ({assignment[3]}) - Assigné le {assignment[2]}")
            
            if student_assignments:
                print(f"\n✅ L'étudiant a bien des quiz assignés!")
                return True
            else:
                print(f"\n⚠️ L'étudiant n'a pas de quiz assignés")
                return False
        else:
            print(f"\n❌ Étudiant {student_email} non trouvé")
            return False
            
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")
        return False
    finally:
        conn.close()

if __name__ == "__main__":
    print("🧪 Test simplifié du flux d'assignation de quiz...")
    success = test_quiz_assignment_simple()
    
    if success:
        print(f"\n✅ Test réussi! L'étudiant reçoit bien les quiz assignés.")
        print(f"   Tu peux maintenant vérifier le dashboard étudiant.")
    else:
        print(f"\n❌ Test échoué. Il faut assigner des quiz à l'étudiant.")
        print(f"   Connecte-toi en tant que prof et assigne un quiz.") 