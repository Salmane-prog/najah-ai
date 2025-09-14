#!/usr/bin/env python3
"""
Script pour vérifier les utilisateurs dans la base de données
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.database import get_db
from models.user import User
from sqlalchemy.orm import Session

def main():
    print("🔍 Vérification des utilisateurs...")
    
    try:
        session = next(get_db())
        users = session.query(User).all()
        
        print(f"✅ Utilisateurs trouvés: {len(users)}")
        
        if users:
            print("\n📋 Liste des utilisateurs:")
            for user in users[:10]:  # Limiter à 10 utilisateurs
                print(f"- ID: {user.id}")
                print(f"  Email: {user.email}")
                print(f"  Nom: {user.first_name} {user.last_name}")
                print(f"  Rôle: {user.role}")
                print(f"  Actif: {user.is_active}")
                print()
        else:
            print("❌ Aucun utilisateur trouvé")
            
        # Trouver un étudiant pour les tests
        students = session.query(User).filter(User.role == 'student').all()
        print(f"👥 Étudiants trouvés: {len(students)}")
        
        if students:
            student = students[0]
            print(f"🎯 Premier étudiant: {student.id} - {student.email}")
            
            # Vérifier les quiz results pour cet étudiant
            from models.quiz import QuizResult
            quiz_results = session.query(QuizResult).filter(QuizResult.student_id == student.id).all()
            print(f"📊 Résultats de quiz pour cet étudiant: {len(quiz_results)}")
            
            if quiz_results:
                print("📈 Quelques résultats:")
                for result in quiz_results[:3]:
                    print(f"  - Quiz: {result.sujet}, Score: {result.score}%, Date: {result.created_at}")
        
        session.close()
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()