#!/usr/bin/env python3
"""
Script pour vérifier les données existantes dans la base
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

def check_data():
    """Vérifier les données existantes"""
    db = SessionLocal()
    
    try:
        print("🔍 VÉRIFICATION DES DONNÉES EXISTANTES")
        print("=" * 50)
        
        # 1. Vérifier les utilisateurs
        users = db.execute(text("SELECT id, email, role FROM users")).fetchall()
        print(f"👥 Utilisateurs: {len(users)}")
        for user in users[:5]:  # Afficher les 5 premiers
            print(f"   - ID: {user[0]}, Email: {user[1]}, Role: {user[2]}")
        
        # 2. Vérifier les classes
        classes = db.execute(text("SELECT id, name, teacher_id FROM class_groups")).fetchall()
        print(f"\n🏫 Classes: {len(classes)}")
        for class_ in classes:
            print(f"   - ID: {class_[0]}, Nom: {class_[1]}, Prof: {class_[2]}")
        
        # 3. Vérifier les étudiants dans les classes
        class_students = db.execute(text("SELECT class_id, student_id FROM class_students")).fetchall()
        print(f"\n👨‍🎓 Étudiants dans les classes: {len(class_students)}")
        for cs in class_students:
            print(f"   - Classe {cs[0]}, Étudiant {cs[1]}")
        
        # 4. Vérifier les quiz
        quizzes = db.execute(text("SELECT id, title FROM quizzes")).fetchall()
        print(f"\n📝 Quiz: {len(quizzes)}")
        
        # 5. Vérifier les résultats de quiz
        quiz_results = db.execute(text("SELECT student_id, score, completed FROM quiz_results")).fetchall()
        print(f"\n📊 Résultats de quiz: {len(quiz_results)}")
        if quiz_results:
            completed = sum(1 for r in quiz_results if r[2])
            avg_score = sum(r[1] for r in quiz_results if r[1]) / len([r for r in quiz_results if r[1]])
            print(f"   - Complétés: {completed}")
            print(f"   - Score moyen: {avg_score:.1f}%")
        
        # 6. Vérifier les badges
        badges = db.execute(text("SELECT user_id FROM user_badges")).fetchall()
        print(f"\n🏆 Badges: {len(badges)}")
        if badges:
            unique_users = len(set(badge[0] for badge in badges))
            print(f"   - Utilisateurs avec badges: {unique_users}")
        
        # 7. Vérifier la progression des étudiants
        progress = db.execute(text("SELECT student_id, progress_percentage FROM student_progress")).fetchall()
        print(f"\n📈 Progression: {len(progress)}")
        if progress:
            avg_progress = sum(p[1] for p in progress if p[1]) / len([p for p in progress if p[1]])
            print(f"   - Progression moyenne: {avg_progress:.1f}%")
        
        print("\n" + "=" * 50)
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    check_data() 