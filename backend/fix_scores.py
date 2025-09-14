#!/usr/bin/env python3
"""
Script pour corriger les scores anormaux dans la base de données
"""
import sys
import os
from sqlalchemy import text

# Ajouter le répertoire au path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def fix_quiz_scores():
    """Corrige les scores anormaux dans quiz_results"""
    print("🔧 Correction des scores de quiz...")
    
    try:
        from core.database import SessionLocal
        
        db = SessionLocal()
        
        # 1. Identifier les scores anormaux
        print("📊 Analyse des scores existants...")
        
        # Trouver les scores avec des pourcentages > 100%
        abnormal_scores = db.execute(text("""
            SELECT id, score, max_score, percentage, user_id, quiz_id
            FROM quiz_results 
            WHERE percentage > 100 OR score > max_score
        """)).fetchall()
        
        print(f"   {len(abnormal_scores)} scores anormaux trouvés")
        
        # 2. Corriger les scores
        for row in abnormal_scores:
            score = float(row.score) if row.score else 0
            max_score = float(row.max_score) if row.max_score else 1
            
            # Si le score est plus grand que le max, ajuster
            if score > max_score and max_score > 0:
                score = max_score
            
            # Recalculer le pourcentage
            percentage = (score / max_score * 100) if max_score > 0 else 0
            
            # S'assurer que le pourcentage est entre 0 et 100
            percentage = max(0, min(100, percentage))
            
            # Mettre à jour la base de données
            db.execute(text("""
                UPDATE quiz_results 
                SET score = :score, percentage = :percentage
                WHERE id = :id
            """), {
                'score': score,
                'percentage': percentage,
                'id': row.id
            })
            
            print(f"   ✅ Corrigé: ID {row.id} - Score: {score}/{max_score} ({percentage:.1f}%)")
        
        # 3. Corriger les scores avec max_score = 0 ou NULL
        null_max_scores = db.execute(text("""
            SELECT id, score, max_score, percentage
            FROM quiz_results 
            WHERE max_score IS NULL OR max_score = 0
        """)).fetchall()
        
        print(f"   {len(null_max_scores)} scores avec max_score manquant")
        
        for row in null_max_scores:
            score = float(row.score) if row.score else 0
            # Définir un max_score par défaut basé sur le score
            max_score = max(score, 10)  # Au moins 10 points
            percentage = (score / max_score * 100) if max_score > 0 else 0
            
            db.execute(text("""
                UPDATE quiz_results 
                SET max_score = :max_score, percentage = :percentage
                WHERE id = :id
            """), {
                'max_score': max_score,
                'percentage': percentage,
                'id': row.id
            })
            
            print(f"   ✅ Corrigé: ID {row.id} - Max_score ajouté: {max_score}")
        
        # 4. Corriger les pourcentages = 0 quand il y a un score
        zero_percentages = db.execute(text("""
            SELECT id, score, max_score, percentage
            FROM quiz_results 
            WHERE percentage = 0 AND score > 0 AND max_score > 0
        """)).fetchall()
        
        print(f"   {len(zero_percentages)} scores avec pourcentage = 0")
        
        for row in zero_percentages:
            score = float(row.score)
            max_score = float(row.max_score)
            percentage = (score / max_score * 100) if max_score > 0 else 0
            
            db.execute(text("""
                UPDATE quiz_results 
                SET percentage = :percentage
                WHERE id = :id
            """), {
                'percentage': percentage,
                'id': row.id
            })
            
            print(f"   ✅ Corrigé: ID {row.id} - Pourcentage: {percentage:.1f}%")
        
        db.commit()
        print("✅ Tous les scores ont été corrigés!")
        
        # 5. Afficher un résumé
        print("\n📊 Résumé après correction:")
        stats = db.execute(text("""
            SELECT 
                COUNT(*) as total,
                AVG(percentage) as avg_percentage,
                MIN(percentage) as min_percentage,
                MAX(percentage) as max_percentage
            FROM quiz_results 
            WHERE completed = 1 OR is_completed = 1
        """)).fetchone()
        
        print(f"   Total quiz complétés: {stats.total}")
        print(f"   Pourcentage moyen: {stats.avg_percentage:.1f}%")
        print(f"   Pourcentage min: {stats.min_percentage:.1f}%")
        print(f"   Pourcentage max: {stats.max_percentage:.1f}%")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la correction: {e}")
        if 'db' in locals():
            db.rollback()
        return False
    finally:
        if 'db' in locals():
            db.close()

def generate_realistic_scores():
    """Génère des scores réalistes pour remplacer les données de test"""
    print("\n🎲 Génération de scores réalistes...")
    
    try:
        from core.database import SessionLocal
        from models.user import User
        from models.quiz import Quiz, QuizResult
        import random
        from datetime import datetime, timedelta
        
        db = SessionLocal()
        
        # Récupérer tous les quiz et étudiants
        quizzes = db.query(Quiz).filter(Quiz.is_active == True).all()
        students = db.query(User).filter(User.role == 'student').all()
        
        if not quizzes or not students:
            print("❌ Pas de quiz ou d'étudiants trouvés")
            return False
        
        print(f"   {len(quizzes)} quiz trouvés")
        print(f"   {len(students)} étudiants trouvés")
        
        # Supprimer les anciens résultats de test
        db.execute(text("DELETE FROM quiz_results WHERE percentage > 100 OR percentage = 0"))
        db.commit()
        
        # Générer de nouveaux résultats réalistes
        results_created = 0
        
        for student in students:
            # Sélectionner 2-5 quiz aléatoires par étudiant
            num_quizzes = random.randint(2, 5)
            selected_quizzes = random.sample(quizzes, min(num_quizzes, len(quizzes)))
            
            for quiz in selected_quizzes:
                # Générer un score réaliste
                if random.random() < 0.7:  # 70% de chance d'avoir un bon score
                    score = random.randint(60, 95)
                else:
                    score = random.randint(30, 70)
                
                # Calculer le nombre de questions correctes
                questions = db.execute(text("""
                    SELECT COUNT(*) as count FROM questions WHERE quiz_id = :quiz_id
                """), {'quiz_id': quiz.id}).fetchone()
                
                question_count = questions.count if questions else 4
                correct_answers = int((score / 100) * question_count)
                
                # Date aléatoire dans les 30 derniers jours
                days_ago = random.randint(0, 30)
                completed_date = datetime.utcnow() - timedelta(days=days_ago)
                started_date = completed_date - timedelta(minutes=random.randint(10, 45))
                
                # Créer le résultat
                quiz_result = QuizResult(
                    student_id=student.id,
                    user_id=student.id,
                    quiz_id=quiz.id,
                    score=correct_answers,
                    max_score=question_count,
                    percentage=score,
                    is_completed=True,
                    completed=1,
                    started_at=started_date,
                    completed_at=completed_date,
                    sujet=quiz.subject
                )
                
                db.add(quiz_result)
                results_created += 1
        
        db.commit()
        print(f"✅ {results_created} nouveaux résultats réalistes créés!")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la génération: {e}")
        if 'db' in locals():
            db.rollback()
        return False
    finally:
        if 'db' in locals():
            db.close()

if __name__ == "__main__":
    print("🚀 Correction des scores de quiz...")
    print("=" * 50)
    
    # Étape 1: Corriger les scores existants
    if fix_quiz_scores():
        print("\n✅ Scores existants corrigés!")
        
        # Étape 2: Générer des scores réalistes (optionnel)
        print("\n🎲 Voulez-vous générer de nouveaux scores réalistes?")
        print("   Cela remplacera les données de test par des scores plus réalistes.")
        
        # Pour l'instant, on ne génère pas automatiquement
        print("   (Génération automatique désactivée pour éviter la perte de données)")
        
        print("\n🎉 Correction terminée!")
        print("   Vos scores devraient maintenant s'afficher correctement dans le dashboard.")
    else:
        print("\n❌ Erreur lors de la correction") 