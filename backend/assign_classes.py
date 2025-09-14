#!/usr/bin/env python3
"""
Script pour assigner des classes au professeur marie.dubois@najah.ai
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# Configuration de la base de données
DATABASE_URL = "sqlite:///data/app.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def assign_classes():
    """Assigner des classes au professeur marie.dubois@najah.ai"""
    db = SessionLocal()
    
    try:
        print("🔧 ASSIGNATION DES CLASSES AU PROFESSEUR")
        print("=" * 50)
        
        # 1. Trouver l'ID du professeur marie.dubois@najah.ai
        teacher = db.execute(text("SELECT id FROM users WHERE email = 'marie.dubois@najah.ai'")).fetchone()
        if not teacher:
            print("❌ Professeur marie.dubois@najah.ai non trouvé")
            return
        
        teacher_id = teacher[0]
        print(f"👩‍🏫 Professeur trouvé: ID {teacher_id}")
        
        # 2. Vérifier les classes existantes
        classes = db.execute(text("SELECT id, name, teacher_id FROM class_groups")).fetchall()
        print(f"\n🏫 Classes existantes: {len(classes)}")
        
        # 3. Assigner quelques classes au professeur
        classes_to_assign = [1, 5, 6, 7]  # Classes avec des étudiants
        
        for class_id in classes_to_assign:
            # Vérifier si la classe existe
            class_exists = db.execute(text("SELECT id FROM class_groups WHERE id = :class_id"), {"class_id": class_id}).fetchone()
            if class_exists:
                # Assigner la classe au professeur
                db.execute(text("UPDATE class_groups SET teacher_id = :teacher_id WHERE id = :class_id"), {"teacher_id": teacher_id, "class_id": class_id})
                print(f"✅ Classe {class_id} assignée au professeur {teacher_id}")
            else:
                print(f"❌ Classe {class_id} n'existe pas")
        
        db.commit()
        
        # 4. Vérifier les classes du professeur
        teacher_classes = db.execute(text("SELECT id, name FROM class_groups WHERE teacher_id = :teacher_id"), {"teacher_id": teacher_id}).fetchall()
        print(f"\n📚 Classes du professeur {teacher_id}: {len(teacher_classes)}")
        for class_ in teacher_classes:
            print(f"   - ID: {class_[0]}, Nom: {class_[1]}")
        
        # 5. Vérifier les étudiants dans ces classes
        for class_ in teacher_classes:
            students = db.execute(text("""
                SELECT cs.student_id, u.email 
                FROM class_students cs 
                JOIN users u ON cs.student_id = u.id 
                WHERE cs.class_id = :class_id
            """), {"class_id": class_[0]}).fetchall()
            print(f"\n👨‍🎓 Étudiants dans la classe {class_[1]} ({class_[0]}): {len(students)}")
            for student in students:
                print(f"   - ID: {student[0]}, Email: {student[1]}")
        
        print("\n" + "=" * 50)
        print("✅ Assignation terminée!")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    assign_classes() 