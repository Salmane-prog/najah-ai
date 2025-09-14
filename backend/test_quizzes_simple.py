#!/usr/bin/env python3
"""
Test simple pour isoler le problème dans list_quizzes.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.database import SessionLocal
from models.user import User, UserRole
from models.quiz import Quiz
from schemas.quiz import QuizRead
from datetime import datetime

def test_list_quizzes_logic():
    """Tester la logique de list_quizzes sans FastAPI."""
    
    print("🧪 Test de la logique list_quizzes")
    print("=" * 40)
    
    try:
        # Créer une session de base de données
        db = SessionLocal()
        
        # Simuler un utilisateur teacher
        current_user = User(
            id=2,
            username="marie.dubois",
            email="marie.dubois@najah.ai",
            role=UserRole.teacher
        )
        
        print(f"✅ Utilisateur simulé: {current_user.username}, role: {current_user.role}")
        
        # Tester la logique de filtrage
        if current_user.role == UserRole.admin:
            quizzes = db.query(Quiz).all()
            print("🔍 Mode admin: tous les quizzes")
        else:
            quizzes = db.query(Quiz).filter(Quiz.created_by == current_user.id).all()
            print("🔍 Mode teacher: quizzes créés par l'utilisateur")
        
        print(f"✅ Quizzes trouvés: {len(quizzes)}")
        
        # Tester l'assignation de created_at
        for quiz in quizzes:
            if quiz.created_at is None:
                quiz.created_at = datetime.utcnow()
                print(f"✅ Date assignée au quiz {quiz.id}")
        
        # Tester la sérialisation
        print("\n🧪 Test de sérialisation des schémas")
        for quiz in quizzes[:1]:  # Tester avec le premier quiz
            try:
                quiz_read = QuizRead.from_orm(quiz)
                print(f"✅ QuizRead sérialisé: {quiz_read.id} - {quiz_read.title}")
            except Exception as e:
                print(f"❌ Erreur de sérialisation: {str(e)}")
        
        print("✅ Test terminé avec succès")
        
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
    finally:
        db.close()

if __name__ == "__main__":
    test_list_quizzes_logic() 