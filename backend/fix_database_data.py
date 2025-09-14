#!/usr/bin/env python3
import sys
import os
sys.path.append('.')

from database import get_db
from models.user import User
from models.quiz import Quiz
from models.quiz_result import QuizResult
from sqlalchemy import func, update
from datetime import datetime

def fix_database_data():
    """Corriger les données incohérentes dans la base de données."""
    try:
        db = next(get_db())
        
        print("=== CORRECTION DES DONNÉES DE LA BASE ===")
        
        # 1. Corriger les quiz_results avec user_id NULL
        print("1. Correction des user_id NULL...")
        results_to_fix = db.query(QuizResult).filter(QuizResult.user_id.is_(None)).all()
        
        for result in results_to_fix:
            if result.student_id:
                # Récupérer l'utilisateur correspondant au student_id
                user = db.query(User).filter(User.id == result.student_id).first()
                if user:
                    result.user_id = user.id
                    print(f"  - Corrigé quiz_result {result.id}: user_id = {user.id}")
        
        # 2. Corriger les scores décimaux étranges
        print("\n2. Correction des scores décimaux...")
        results_with_decimal_scores = db.query(QuizResult).filter(
            QuizResult.score < 1.0,
            QuizResult.score > 0.0
        ).all()
        
        for result in results_with_decimal_scores:
            # Convertir le score décimal en pourcentage
            if result.score < 1.0:
                result.score = result.score * 100
                print(f"  - Corrigé quiz_result {result.id}: score {result.score:.1f}%")
        
        # 3. Corriger les flags de completion
        print("\n3. Correction des flags de completion...")
        results_with_inconsistent_flags = db.query(QuizResult).filter(
            QuizResult.completed == 0,
            QuizResult.is_completed == 1
        ).all()
        
        for result in results_with_inconsistent_flags:
            result.completed = 1
            print(f"  - Corrigé quiz_result {result.id}: completed = 1")
        
        # 4. S'assurer que tous les quiz_results ont is_completed défini
        print("\n4. Définition de is_completed manquant...")
        results_without_is_completed = db.query(QuizResult).filter(
            QuizResult.is_completed.is_(None)
        ).all()
        
        for result in results_without_is_completed:
            result.is_completed = True if result.completed == 1 else False
            print(f"  - Corrigé quiz_result {result.id}: is_completed = {result.is_completed}")
        
        # 5. Vérifier et corriger les pourcentages
        print("\n5. Correction des pourcentages...")
        for result in db.query(QuizResult).all():
            if result.max_score > 0:
                expected_percentage = (result.score / result.max_score) * 100
                if abs(result.percentage - expected_percentage) > 1:  # Tolérance de 1%
                    result.percentage = expected_percentage
                    print(f"  - Corrigé quiz_result {result.id}: percentage = {expected_percentage:.1f}%")
        
        # Commit des changements
        db.commit()
        
        print("\n✅ Corrections terminées!")
        
        # Afficher un résumé
        total_results = db.query(QuizResult).count()
        completed_results = db.query(QuizResult).filter(QuizResult.is_completed == True).count()
        students = db.query(User).filter(User.role == "student").count()
        quizzes = db.query(Quiz).count()
        
        print(f"\n📊 Résumé après correction:")
        print(f"  - Total résultats: {total_results}")
        print(f"  - Résultats complétés: {completed_results}")
        print(f"  - Étudiants: {students}")
        print(f"  - Quiz: {quizzes}")
        
        # Vérifier les matières disponibles
        subjects = db.query(Quiz.subject).distinct().all()
        print(f"  - Matières: {[s[0] for s in subjects if s[0]]}")
        
    except Exception as e:
        print(f"❌ Erreur lors de la correction: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()

if __name__ == "__main__":
    fix_database_data() 