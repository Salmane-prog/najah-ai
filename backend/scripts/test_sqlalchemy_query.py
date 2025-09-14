#!/usr/bin/env python3
"""
Script pour tester exactement la requête SQLAlchemy utilisée dans l'API
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import func, and_
from sqlalchemy.orm import Session
from core.database import SessionLocal
from models.user import User, UserRole
from models.class_group import ClassGroup, ClassStudent

def test_sqlalchemy_query():
    print("🔍 Test de la requête SQLAlchemy exacte de l'API")
    
    db = SessionLocal()
    try:
        # Simuler l'utilisateur marie.dubois@najah.ai
        current_user = db.query(User).filter(User.email == "marie.dubois@najah.ai").first()
        
        if not current_user:
            print("❌ Utilisateur marie.dubois@najah.ai non trouvé")
            return
        
        print(f"✅ Utilisateur trouvé: {current_user.username} (ID: {current_user.id})")
        
        # Requête exacte de l'API
        print("\n📊 Requête SQLAlchemy de l'API:")
        total_students = db.query(func.count(func.distinct(ClassStudent.student_id))).join(
            ClassGroup, ClassStudent.class_id == ClassGroup.id
        ).join(
            User, ClassStudent.student_id == User.id
        ).filter(
            and_(
                ClassGroup.teacher_id == current_user.id,
                User.role == UserRole.student
            )
        ).scalar() or 0
        
        print(f"   Résultat: {total_students} étudiants")
        
        # Vérifier les étudiants qui sont comptés
        students = db.query(func.distinct(ClassStudent.student_id)).join(
            ClassGroup, ClassStudent.class_id == ClassGroup.id
        ).join(
            User, ClassStudent.student_id == User.id
        ).filter(
            and_(
                ClassGroup.teacher_id == current_user.id,
                User.role == UserRole.student
            )
        ).all()
        
        print(f"   Étudiants comptés ({len(students)}):")
        for student_id in students:
            student = db.query(User).filter(User.id == student_id[0]).first()
            if student:
                print(f"   - {student.username} (ID: {student.id})")
        
        # Comparer avec la requête SQL directe
        print(f"\n🔍 Comparaison avec SQL direct:")
        result = db.execute("""
            SELECT COUNT(DISTINCT cs.student_id)
            FROM class_students cs
            JOIN class_groups cg ON cs.class_id = cg.id
            JOIN users u ON cs.student_id = u.id
            WHERE cg.teacher_id = ? AND u.role = 'student'
        """, (current_user.id,)).scalar()
        
        print(f"   SQL direct: {result} étudiants")
        
        if total_students == result:
            print("   ✅ Les deux requêtes donnent le même résultat")
        else:
            print("   ❌ Les requêtes donnent des résultats différents")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    test_sqlalchemy_query() 