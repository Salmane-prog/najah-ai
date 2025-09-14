import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, desc, and_
from core.database import get_db
from models.user import User
from models.quiz import Quiz, QuizResult, Question
from models.learning_history import LearningHistory
from api.v1.auth import get_current_user
from typing import List, Dict, Any
from datetime import datetime, timedelta
import json
import random

from data.question_bank import get_questions_by_subject_and_level, get_available_subjects, get_available_levels

router = APIRouter()

@router.post("/generate/{student_id}")
def generate_adaptive_quiz(
    student_id: int,
    subject: str = Query("Français", description="Matière du quiz"),
    question_count: int = Query(10, description="Nombre de questions"),
    difficulty_preference: str = Query("auto", description="Préférence de difficulté"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Générer un quiz adaptatif basé sur le profil de l'étudiant"""
    raise HTTPException(status_code=501, detail="Utilisez l'endpoint -test pour les tests")

@router.post("/generate-test/{student_id}")
def generate_adaptive_quiz_test(
    student_id: int,
    subject: str = Query("Français", description="Matière du quiz"),
    question_count: int = Query(10, description="Nombre de questions"),
    difficulty_preference: str = Query("auto", description="Préférence de difficulté"),
    db: Session = Depends(get_db)
):
    """Générer un quiz adaptatif basé sur le profil de l'étudiant"""
    try:
        # Vérifier que l'étudiant existe
        student = db.query(User).filter(User.id == student_id).first()
        if not student:
            raise HTTPException(status_code=404, detail="Étudiant non trouvé")
        
        # Récupérer l'historique des performances de l'étudiant
        quiz_results = db.query(QuizResult).filter(
            QuizResult.student_id == student_id,
            QuizResult.is_completed == True
        ).order_by(QuizResult.created_at.desc()).all()
        
        # Déterminer le niveau de difficulté adaptatif
        if difficulty_preference == "auto":
            if quiz_results:
                avg_score = sum(r.score for r in quiz_results) / len(quiz_results)
                if avg_score >= 80:
                    difficulty = "hard"
                elif avg_score >= 60:
                    difficulty = "medium"
                else:
                    difficulty = "easy"
            else:
                difficulty = "easy"
        else:
            difficulty = difficulty_preference
        
        # Récupérer les questions disponibles pour la matière et la difficulté
        questions_query = db.query(Question).join(Quiz).filter(
            Quiz.subject == subject,
            Quiz.is_active == True
        )
        
        # Filtrer par difficulté si spécifiée
        if difficulty != "auto":
            questions_query = questions_query.filter(Quiz.difficulty == difficulty)
        
        available_questions = questions_query.all()
        
        if not available_questions:
            # Si aucune question trouvée, utiliser des questions par défaut
            available_questions = db.query(Question).join(Quiz).filter(
                Quiz.subject == subject
            ).limit(20).all()
        
        if not available_questions:
            raise HTTPException(status_code=404, detail=f"Aucune question disponible pour {subject}")
        
        # Sélectionner aléatoirement les questions
        selected_questions = random.sample(
            available_questions, 
            min(question_count, len(available_questions))
        )
        
        # Formater les questions pour le frontend
        formatted_questions = []
        for i, question in enumerate(selected_questions):
            # Récupérer les options de réponse
            options = []
            if question.options:
                try:
                    options = json.loads(question.options)
                except:
                    options = ["Option A", "Option B", "Option C", "Option D"]
            else:
                # Options par défaut si aucune n'est définie
                options = ["Option A", "Option B", "Option C", "Option D"]
            
            formatted_questions.append({
                "id": question.id,
                "question_text": question.question_text,
                "options": options,
                "correct_answer": question.correct_answer,
                "explanation": getattr(question, 'explanation', "") or "",
                "difficulty": question.quiz.difficulty if question.quiz else "medium",
                "topic": getattr(question, 'topic', "") or "Général",
                "question_number": i + 1
            })
        
        # Créer le quiz adaptatif
        adaptive_quiz = {
            "quiz_id": f"adaptive_{student_id}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}",
            "student_id": student_id,
            "subject": subject,
            "difficulty": difficulty,
            "total_questions": len(formatted_questions),
            "estimated_duration": len(formatted_questions) * 2,  # 2 minutes par question
            "questions": formatted_questions,
            "created_at": datetime.utcnow().isoformat(),
            "adaptive_features": {
                "difficulty_adjusted": difficulty != "auto",
                "performance_based": len(quiz_results) > 0,
                "personalized": True
            }
        }
        
        return adaptive_quiz
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Erreur generate_adaptive_quiz: {e}")
        raise HTTPException(status_code=500, detail=f"Erreur lors de la génération du quiz: {str(e)}")

@router.post("/generate-test/{student_id}")
def generate_adaptive_quiz_test(
    student_id: int,
    subject: str = Query(..., description="Matière pour le quiz"),
    question_count: int = Query(10, description="Nombre de questions"),
    db: Session = Depends(get_db)
):
    """Version de test sans authentification pour le développement."""
    try:
        print(f"🔍 [ADAPTIVE_QUIZZES] Génération de quiz test pour étudiant {student_id}, matière {subject}")
        
        # Vérifier que l'étudiant existe
        student = db.query(User).filter(User.id == student_id).first()
        if not student:
            raise HTTPException(status_code=404, detail="Étudiant non trouvé")
        
        # Déterminer le niveau de l'étudiant pour cette matière
        student_level = determine_student_level_for_subject(student_id, subject, db)
        print(f"📊 [ADAPTIVE_QUIZZES] Niveau de l'étudiant pour {subject}: {student_level}")
        
        # Récupérer les questions de la banque
        questions = get_questions_by_subject_and_level(subject, student_level, question_count)
        
        if not questions:
            # Si pas de questions pour ce niveau, utiliser le niveau débutant
            questions = get_questions_by_subject_and_level(subject, "débutant", question_count)
            student_level = "débutant"
            print(f"⚠️ [ADAPTIVE_QUIZZES] Utilisation du niveau débutant par défaut")
        
        # Créer un quiz de test
        quiz_data = {
            "quiz_id": random.randint(1000, 9999),
            "title": f"Quiz Adaptatif {subject} - Niveau {student_level.capitalize()}",
            "subject": subject,
            "difficulty": student_level.capitalize(),
            "question_count": len(questions),
            "estimated_duration": len(questions) * 2,
            "adaptation_reason": f"Quiz adaptatif généré pour {student.first_name} en {subject} (niveau {student_level})",
            "questions": questions
        }
        
        print(f"✅ [ADAPTIVE_QUIZZES] Quiz généré avec {len(questions)} questions de niveau {student_level}")
        return quiz_data
        
    except Exception as e:
        print(f"❌ [ADAPTIVE_QUIZZES] Erreur génération quiz test: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erreur génération quiz test: {str(e)}")

@router.post("/{quiz_id}/submit")
def submit_quiz_results(
    quiz_id: str,
    student_id: int,
    answers: Dict[str, Any],
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Soumettre les résultats d'un quiz adaptatif"""
    try:
        # Vérifier les permissions
        if current_user.role.value == 'student' and current_user.id != student_id:
            raise HTTPException(status_code=403, detail="Accès non autorisé")
        
        # Extraire les données
        student_answers = answers.get("answers", {})
        time_spent = answers.get("time_spent", 0)
        subject = answers.get("subject", "Français")
        
        # Calculer le score
        correct_answers = 0
        total_questions = len(student_answers)
        
        for question_id, student_answer in student_answers.items():
            question = db.query(Question).filter(Question.id == int(question_id)).first()
            if question and question.correct_answer == student_answer:
                correct_answers += 1
        
        score = (correct_answers / total_questions * 100) if total_questions > 0 else 0
        
        # Créer un résultat de quiz
        quiz_result = QuizResult(
            student_id=student_id,
            quiz_id=1,  # Quiz par défaut pour les quiz adaptatifs
            score=score,
            answers=json.dumps(student_answers),
            time_spent=time_spent,
            is_completed=True,
            sujet=subject,
            created_at=datetime.utcnow()
        )
        
        db.add(quiz_result)
        db.commit()
        
        # Générer des recommandations basées sur le score
        recommendations = []
        if score < 50:
            recommendations.append("Considérez réviser les concepts de base")
            recommendations.append("Pratiquez avec des exercices plus simples")
        elif score < 70:
            recommendations.append("Continuez à pratiquer pour améliorer")
            recommendations.append("Concentrez-vous sur vos points faibles")
        else:
            recommendations.append("Excellent travail ! Continuez ainsi")
            recommendations.append("Essayez des questions plus difficiles")
        
        return {
            "score": round(score, 2),
            "correct_answers": correct_answers,
            "total_questions": total_questions,
            "time_spent": time_spent,
            "recommendations": recommendations,
            "next_difficulty": "harder" if score >= 80 else "same" if score >= 60 else "easier"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Erreur submit_quiz_results: {e}")
        raise HTTPException(status_code=500, detail=f"Erreur lors de la soumission: {str(e)}")

@router.post("/{quiz_id}/submit-test")
def submit_adaptive_quiz_test(
    quiz_id: int,
    answers: Dict[str, Any],
    student_id: int = Query(..., description="ID de l'étudiant"),
    score: float = Query(..., description="Score obtenu"),
    db: Session = Depends(get_db)
):
    """Version de test sans authentification pour soumettre un quiz adaptatif."""
    try:
        print(f"🔍 [ADAPTIVE_QUIZZES] Soumission de quiz test pour étudiant {student_id}, score {score}")
        
        # Vérifier que l'étudiant existe
        student = db.query(User).filter(User.id == student_id).first()
        if not student:
            raise HTTPException(status_code=404, detail="Étudiant non trouvé")
        
        # Créer un résultat de quiz de test
        result = QuizResult(
            student_id=student_id,
            quiz_id=quiz_id,
            score=score,
            max_score=100,
            percentage=score,
            is_completed=True,
            completed_at=datetime.utcnow(),
            sujet="Test",  # À adapter selon le quiz
            user_id=student_id
        )
        db.add(result)
        db.commit()
        
        # Analyser la performance et ajuster la difficulté future
        difficulty_adjustment = analyze_and_adjust_difficulty(student_id, score, "Test", db)
        
        # Générer des recommandations
        recommendations = generate_adaptive_recommendations([], "Test", db)
        
        response_data = {
            "success": True,
            "score": score,
            "difficulty_adjustment": difficulty_adjustment,
            "recommendations": recommendations,
            "message": f"Quiz terminé avec succès. Score: {score}%"
        }
        
        print(f"✅ [ADAPTIVE_QUIZZES] Quiz soumis avec succès, score: {score}%")
        return response_data
        
    except Exception as e:
        print(f"❌ [ADAPTIVE_QUIZZES] Erreur soumission quiz test: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erreur soumission quiz test: {str(e)}")

@router.get("/student/{student_id}/progress")
def get_adaptive_progress(
    student_id: int,
    subject: str = Query(None, description="Matière spécifique (optionnel)"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Obtenir la progression adaptative d'un étudiant."""
    try:
        # Récupérer l'historique des quiz adaptatifs
        query = db.query(QuizResult).filter(QuizResult.student_id == student_id)
        if subject:
            query = query.filter(QuizResult.sujet == subject)
        
        adaptive_results = query.order_by(QuizResult.created_at.desc()).all()
        
        if not adaptive_results:
            return {
                "student_id": student_id,
                "message": "Aucun quiz adaptatif trouvé",
                "progress": {}
            }
        
        # Analyser la progression
        progress_analysis = analyze_adaptive_progress(adaptive_results)
        
        # Calculer les tendances de difficulté
        difficulty_trends = calculate_difficulty_trends(adaptive_results, db)
        
        return {
            "student_id": student_id,
            "subject": subject,
            "total_adaptive_quizzes": len(adaptive_results),
            "average_score": round(sum(r.score for r in adaptive_results) / len(adaptive_results), 2),
            "progress_analysis": progress_analysis,
            "difficulty_trends": difficulty_trends,
            "recommendations": generate_progress_recommendations(progress_analysis, difficulty_trends)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur progression adaptative: {str(e)}")

@router.get("/dashboard-data")
def get_adaptive_quizzes_dashboard_data(
    student_id: int = Query(None, description="ID de l'étudiant spécifique (optionnel)"),
    db: Session = Depends(get_db)
):
    """Récupérer les données pour le dashboard des tests adaptatifs."""
    try:
        print("🔍 [ADAPTIVE_QUIZZES] Début de récupération des données...")
        
        # Récupérer les étudiants
        students = db.query(User).filter(User.role == "student").all()
        print(f"📊 [ADAPTIVE_QUIZZES] Étudiants trouvés: {len(students)}")
        
        student_list = []
        for s in students:
            name = f"{s.first_name} {s.last_name}" if s.first_name and s.last_name else s.email
            student_list.append({"id": s.id, "name": name})
            print(f"  - Étudiant: ID={s.id}, Nom={name}")
        
        # Récupérer les matières disponibles depuis les quiz
        subjects = db.query(Quiz.subject).distinct().all()
        print(f"📊 [ADAPTIVE_QUIZZES] Matières trouvées: {len(subjects)}")
        
        subject_list = []
        for s in subjects:
            if s[0]:  # Vérifier que le sujet n'est pas None
                subject_list.append({"id": s[0], "name": s[0]})
                print(f"  - Matière: {s[0]}")
        
        # Si un étudiant spécifique est demandé, calculer ses données personnelles
        if student_id:
            print(f"📊 [ADAPTIVE_QUIZZES] Calcul des données pour étudiant {student_id}")
            
            # Récupérer les résultats de cet étudiant spécifique
            student_results = db.query(QuizResult).filter(
                QuizResult.student_id == student_id,
                QuizResult.is_completed == True
            ).order_by(QuizResult.created_at.desc()).all()
            
            if student_results:
                scores = [r.score for r in student_results]
                avg_score = sum(scores) / len(scores)
                completed_quizzes = len(student_results)
                
                print(f"📊 [ADAPTIVE_QUIZZES] Étudiant {student_id}: {completed_quizzes} quiz, score moyen {avg_score:.1f}%")
                
                # Calculer la tendance (évolution des scores)
                if len(scores) >= 3:
                    recent_scores = scores[:3]  # 3 derniers quiz
                    older_scores = scores[-3:] if len(scores) >= 6 else scores[3:6] if len(scores) >= 6 else scores[:3]
                    
                    recent_avg = sum(recent_scores) / len(recent_scores)
                    older_avg = sum(older_scores) / len(older_scores)
                    
                    # Calculer la progression
                    progression_change = recent_avg - older_avg
                    difficulty_progression = min(100, max(-100, progression_change * 2))
                    
                    # Déterminer la tendance
                    if progression_change > 5:
                        trend = "amélioration"
                    elif progression_change < -5:
                        trend = "régression"
                    else:
                        trend = "stable"
                else:
                    difficulty_progression = 0
                    trend = "insuffisant de données"
                
                # Calculer la cohérence (stabilité des scores)
                if len(scores) >= 2:
                    variance = sum((score - avg_score) ** 2 for score in scores) / len(scores)
                    coherence_percentage = max(0, 100 - (variance / 10))
                else:
                    coherence_percentage = 50
                
                # Calculer le niveau actuel basé sur le score moyen
                if avg_score >= 80:
                    current_level = "Avancé"
                elif avg_score >= 60:
                    current_level = "Intermédiaire"
                elif avg_score >= 40:
                    current_level = "Débutant"
                else:
                    current_level = "Débutant"
                
                # Déterminer le prochain niveau recommandé
                if trend == "amélioration" and avg_score >= 70:
                    next_recommended_level = "Avancé" if current_level == "Intermédiaire" else "Intermédiaire"
                elif trend == "régression" and avg_score <= 30:
                    next_recommended_level = "Débutant"
                else:
                    next_recommended_level = "Intermédiaire" if current_level == "Débutant" else "Avancé"
                
                # Calculer la progression dans le niveau actuel (0-10)
                if current_level == "Débutant":
                    level_progression = min(10, max(0, int(avg_score / 10)))
                elif current_level == "Intermédiaire":
                    level_progression = min(10, max(0, int((avg_score - 60) / 2)))
                else:  # Avancé
                    level_progression = min(10, max(0, int((avg_score - 80) / 2)))
                
                response_data = {
                    "students": student_list,
                    "subjects": subject_list,
                    "current_level": current_level,
                    "completed_quizzes": completed_quizzes,
                    "average_score": round(avg_score, 1),
                    "coherence_percentage": round(coherence_percentage, 1),
                    "difficulty_progression": round(difficulty_progression, 1),
                    "trend": trend,
                    "next_recommended_level": next_recommended_level,
                    "level_progression": level_progression,
                    "student_specific": True,
                    "student_id": student_id
                }
                
                print(f"✅ [ADAPTIVE_QUIZZES] Données personnalisées pour étudiant {student_id}")
                return response_data
            else:
                # Aucun résultat pour cet étudiant
                response_data = {
                    "students": student_list,
                    "subjects": subject_list,
                    "current_level": "Débutant",
                    "completed_quizzes": 0,
                    "average_score": 0,
                    "coherence_percentage": 0,
                    "difficulty_progression": 0,
                    "trend": "aucune donnée",
                    "next_recommended_level": "Débutant",
                    "level_progression": 0,
                    "student_specific": True,
                    "student_id": student_id
                }
                return response_data
        
        # Sinon, calculer les statistiques globales (pour le prof)
        print("📊 [ADAPTIVE_QUIZZES] Calcul des données globales (vue prof)")
        
        # Calculer les statistiques de progression globales
        total_results = db.query(QuizResult).count()
        print(f"📊 [ADAPTIVE_QUIZZES] Total résultats: {total_results}")
        
        if total_results > 0:
            # Utiliser is_completed pour filtrer les résultats valides
            completed_results = db.query(QuizResult).filter(QuizResult.is_completed == True).all()
            print(f"📊 [ADAPTIVE_QUIZZES] Résultats complétés: {len(completed_results)}")
            
            if completed_results:
                scores = [r.score for r in completed_results]
                avg_score = sum(scores) / len(scores)
                completed_quizzes = len(completed_results)
                print(f"📊 [ADAPTIVE_QUIZZES] Score moyen global: {avg_score:.1f}%, Quiz complétés: {completed_quizzes}")
                
                # Calculer la tendance globale
                if len(scores) >= 3:
                    recent_scores = scores[:3]
                    older_scores = scores[-3:] if len(scores) >= 6 else scores[3:6] if len(scores) >= 6 else scores[:3]
                    
                    recent_avg = sum(recent_scores) / len(recent_scores)
                    older_avg = sum(older_scores) / len(older_scores)
                    
                    progression_change = recent_avg - older_avg
                    difficulty_progression = min(100, max(-100, progression_change * 2))
                    
                    if progression_change > 5:
                        trend = "amélioration"
                    elif progression_change < -5:
                        trend = "régression"
                    else:
                        trend = "stable"
                else:
                    difficulty_progression = 0
                    trend = "insuffisant de données"
                
                # Calculer la cohérence globale
                if len(scores) >= 2:
                    variance = sum((score - avg_score) ** 2 for score in scores) / len(scores)
                    coherence_percentage = max(0, 100 - (variance / 10))
                else:
                    coherence_percentage = 50
                
            else:
                avg_score = 0
                completed_quizzes = 0
                difficulty_progression = 0
                trend = "aucune donnée"
                coherence_percentage = 0
                print("⚠️ [ADAPTIVE_QUIZZES] Aucun résultat complété trouvé")
        else:
            avg_score = 0
            completed_quizzes = 0
            difficulty_progression = 0
            trend = "aucune donnée"
            coherence_percentage = 0
            print("⚠️ [ADAPTIVE_QUIZZES] Aucun résultat trouvé")
        
        # Calculer le niveau global
        if avg_score >= 80:
            current_level = "Avancé"
        elif avg_score >= 60:
            current_level = "Intermédiaire"
        elif avg_score >= 40:
            current_level = "Débutant"
        else:
            current_level = "Débutant"
        
        # Recommandation globale
        if trend == "amélioration" and avg_score >= 70:
            next_recommended_level = "Avancé" if current_level == "Intermédiaire" else "Intermédiaire"
        elif trend == "régression" and avg_score <= 30:
            next_recommended_level = "Débutant"
        else:
            next_recommended_level = "Intermédiaire" if current_level == "Débutant" else "Avancé"
        
        # Progression globale
        if current_level == "Débutant":
            level_progression = min(10, max(0, int(avg_score / 10)))
        elif current_level == "Intermédiaire":
            level_progression = min(10, max(0, int((avg_score - 60) / 2)))
        else:  # Avancé
            level_progression = min(10, max(0, int((avg_score - 80) / 2)))
        
        response_data = {
            "students": student_list,
            "subjects": subject_list,
            "current_level": current_level,
            "completed_quizzes": completed_quizzes,
            "average_score": round(avg_score, 1),
            "coherence_percentage": round(coherence_percentage, 1),
            "difficulty_progression": round(difficulty_progression, 1),
            "trend": trend,
            "next_recommended_level": next_recommended_level,
            "level_progression": level_progression,
            "student_specific": False,
            "student_id": None
        }
        
        print(f"✅ [ADAPTIVE_QUIZZES] Données globales préparées: {len(student_list)} étudiants, {len(subject_list)} matières")
        return response_data
        
    except Exception as e:
        print(f"❌ [ADAPTIVE_QUIZZES] Erreur: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erreur récupération données: {str(e)}")

@router.get("/dashboard-data-test")
def get_adaptive_quizzes_dashboard_data_test(
    student_id: int = Query(..., description="ID de l'étudiant"),
    db: Session = Depends(get_db)
):
    """Données du dashboard de quiz adaptatifs (version test sans auth)."""
    try:
        # Récupérer les résultats de quiz pour l'étudiant
        student_results = db.query(QuizResult).filter(QuizResult.student_id == student_id).all()
        
        if not student_results:
            return {
                "student_list": [],
                "subject_list": [],
                "completed_quizzes": 0,
                "average_score": 0,
                "coherence_percentage": 0,
                "current_level": "Débutant",
                "next_recommended_level": "Intermédiaire",
                "difficulty_progression": 1,
                "trend": "stable",
                "level_progression": 1
            }
        
        # Calculer les métriques
        completed_quizzes = len(student_results)
        average_score = sum(r.score for r in student_results) / completed_quizzes if completed_quizzes > 0 else 0
        
        # Déterminer le niveau actuel
        if average_score >= 80:
            current_level = "Avancé"
            next_level = "Expert"
        elif average_score >= 60:
            current_level = "Intermédiaire"
            next_level = "Avancé"
        else:
            current_level = "Débutant"
            next_level = "Intermédiaire"
        
        # Calculer la cohérence (variance des scores)
        if len(student_results) > 1:
            scores = [r.score for r in student_results]
            mean_score = sum(scores) / len(scores)
            variance = sum((score - mean_score) ** 2 for score in scores) / len(scores)
            coherence = max(0, 100 - (variance / 10))
        else:
            coherence = 100
        
        # Déterminer la tendance
        recent_results = sorted(student_results, key=lambda x: x.created_at, reverse=True)[:5]
        if len(recent_results) >= 2:
            recent_avg = sum(r.score for r in recent_results[:2]) / 2
            older_avg = sum(r.score for r in recent_results[2:]) / (len(recent_results) - 2) if len(recent_results) > 2 else recent_avg
            trend = "amélioration" if recent_avg > older_avg else "dégradation" if recent_avg < older_avg else "stable"
        else:
            trend = "stable"
        
        # Calculer la progression de niveau
        level_progression = min(10, max(1, int(average_score / 10)))
        
        # Liste des sujets
        subjects = list(set(r.sujet for r in student_results if r.sujet))
        
        return {
            "student_list": [{"id": student_id, "name": f"Étudiant {student_id}"}],
            "subject_list": subjects,
            "completed_quizzes": completed_quizzes,
            "average_score": round(average_score, 2),
            "coherence_percentage": round(coherence, 2),
            "current_level": current_level,
            "next_recommended_level": next_level,
            "difficulty_progression": level_progression,
            "trend": trend,
            "level_progression": level_progression
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur quiz adaptatifs: {str(e)}")

def analyze_student_performance(student_id: int, subject: str, db: Session) -> Dict[str, Any]:
    """Analyser les performances passées d'un étudiant."""
    # Récupérer les 10 derniers résultats pour cette matière
    recent_results = db.query(QuizResult).filter(
        QuizResult.student_id == student_id,
        QuizResult.sujet == subject
    ).order_by(QuizResult.created_at.desc()).limit(10).all()
    
    if not recent_results:
        return {
            "average_score": 50,  # Score par défaut
            "trend": "stable",
            "confidence_level": "low",
            "adaptation_reason": "Premier quiz dans cette matière"
        }
    
    # Calculer les statistiques
    scores = [r.score for r in recent_results]
    avg_score = sum(scores) / len(scores)
    
    # Analyser la tendance
    if len(scores) >= 3:
        recent_avg = sum(scores[:3]) / 3
        older_avg = sum(scores[3:]) / (len(scores) - 3) if len(scores) > 3 else recent_avg
        trend = "improving" if recent_avg > older_avg else "declining" if recent_avg < older_avg else "stable"
    else:
        trend = "insufficient_data"
    
    # Déterminer le niveau de confiance
    variance = sum((score - avg_score) ** 2 for score in scores) / len(scores)
    confidence_level = "high" if variance < 100 else "medium" if variance < 400 else "low"
    
    return {
        "average_score": round(avg_score, 2),
        "trend": trend,
        "confidence_level": confidence_level,
        "recent_scores": scores[:5],
        "adaptation_reason": f"Performance moyenne: {avg_score:.1f}% avec tendance {trend}"
    }

def determine_optimal_difficulty(performance: Dict, preference: str) -> str:
    """Déterminer le niveau de difficulté optimal."""
    if preference != "auto":
        return preference
    
    avg_score = performance.get("average_score", 50)
    trend = performance.get("trend", "stable")
    
    # Logique d'adaptation basée sur la performance
    if avg_score >= 85:
        if trend == "improving":
            return "hard"
        else:
            return "medium"
    elif avg_score >= 70:
        return "medium"
    elif avg_score >= 50:
        return "easy"
    else:
        return "easy"  # Niveau de base pour les très faibles performances

def select_adaptive_questions(subject: str, difficulty: str, count: int, student_id: int, db: Session) -> List[Dict]:
    """Sélectionner les questions adaptées au niveau de difficulté."""
    # Récupérer les questions disponibles
    questions = db.query(Question).join(Quiz).filter(
        Quiz.subject == subject,
        Quiz.is_active == True
    ).all()
    
    if not questions:
        return []
    
    # Filtrer par difficulté si disponible
    difficulty_questions = [q for q in questions if hasattr(q, 'difficulty') and q.difficulty == difficulty]
    if not difficulty_questions:
        difficulty_questions = questions  # Utiliser toutes les questions si pas de filtrage par difficulté
    
    # Sélectionner aléatoirement
    selected_questions = random.sample(difficulty_questions, min(count, len(difficulty_questions)))
    
    # Formater les questions
    formatted_questions = []
    for question in selected_questions:
        formatted_questions.append({
            "id": question.id,
            "text": question.text,
            "type": question.question_type,
            "options": json.loads(question.options) if question.options else [],
            "difficulty": getattr(question, 'difficulty', 'medium')
        })
    
    return formatted_questions

def create_adaptive_quiz(questions: List[Dict], student_id: int, subject: str, db: Session) -> Quiz:
    """Créer un quiz adaptatif."""
    quiz = Quiz(
        title=f"Quiz adaptatif - {subject}",
        description=f"Quiz personnalisé généré automatiquement",
        subject=subject,
        level="adaptive",
        is_active=True,
        created_by=1,  # Système
        time_limit=len(questions) * 2,  # 2 minutes par question
        is_adaptive=True
    )
    
    db.add(quiz)
    db.commit()
    db.refresh(quiz)
    
    return quiz

def calculate_adaptive_score(quiz: Quiz, answers: Dict, db: Session) -> tuple:
    """Calculer le score d'un quiz adaptatif."""
    questions = db.query(Question).filter(Question.quiz_id == quiz.id).all()
    
    correct_count = 0
    correct_answers = []
    
    for question in questions:
        student_answer = answers.get(str(question.id))
        if student_answer:
            # Comparer avec la réponse correcte
            correct_answer = question.correct_answer
            if student_answer == correct_answer:
                correct_count += 1
                correct_answers.append(question.id)
    
    score = (correct_count / len(questions)) * 100 if questions else 0
    
    return round(score, 2), correct_answers

def analyze_and_adjust_difficulty(student_id: int, score: float, subject: str, db: Session) -> Dict[str, Any]:
    """Analyser la performance et ajuster la difficulté future."""
    # Récupérer l'historique récent
    recent_results = db.query(QuizResult).filter(
        QuizResult.student_id == student_id,
        QuizResult.sujet == subject
    ).order_by(QuizResult.created_at.desc()).limit(5).all()
    
    if len(recent_results) < 2:
        return {
            "current_difficulty": "medium",
            "suggested_difficulty": "medium",
            "adjustment_reason": "Données insuffisantes"
        }
    
    # Analyser la tendance
    recent_scores = [r.score for r in recent_results[:3]]
    avg_recent = sum(recent_scores) / len(recent_scores)
    
    # Logique d'ajustement
    if avg_recent >= 85:
        suggested_difficulty = "hard"
        reason = "Performance excellente - Augmenter la difficulté"
    elif avg_recent >= 70:
        suggested_difficulty = "medium"
        reason = "Performance bonne - Maintenir le niveau"
    elif avg_recent >= 50:
        suggested_difficulty = "easy"
        reason = "Performance moyenne - Réduire la difficulté"
    else:
        suggested_difficulty = "easy"
        reason = "Performance faible - Niveau de base recommandé"
    
    return {
        "current_difficulty": "adaptive",
        "suggested_difficulty": suggested_difficulty,
        "adjustment_reason": reason,
        "recent_average": round(avg_recent, 2)
    }

def generate_adaptive_recommendations(correct_answers: List[int], subject: str, db: Session) -> List[str]:
    """Générer des recommandations basées sur les erreurs."""
    recommendations = []
    
    if len(correct_answers) < 5:  # Moins de 50% de réussite
        recommendations.append(f"Réviser les concepts de base en {subject}")
        recommendations.append("Consulter les ressources de remédiation")
    
    if len(correct_answers) >= 8:  # Plus de 80% de réussite
        recommendations.append("Prêt pour des exercices plus avancés")
        recommendations.append("Considérer des défis supplémentaires")
    
    return recommendations

def suggest_next_quiz_difficulty(student_id: int, score: float, subject: str, db: Session) -> str:
    """Suggérer la difficulté du prochain quiz."""
    if score >= 85:
        return "hard"
    elif score >= 70:
        return "medium"
    else:
        return "easy"

def analyze_adaptive_progress(results: List[QuizResult]) -> Dict[str, Any]:
    """Analyser la progression adaptative."""
    if not results:
        return {}
    
    scores = [r.score for r in results]
    avg_score = sum(scores) / len(scores)
    
    # Analyser la progression temporelle
    recent_scores = scores[:5] if len(scores) >= 5 else scores
    older_scores = scores[5:10] if len(scores) >= 10 else []
    
    if older_scores:
        recent_avg = sum(recent_scores) / len(recent_scores)
        older_avg = sum(older_scores) / len(older_scores)
        improvement = recent_avg - older_avg
    else:
        improvement = 0
    
    return {
        "average_score": round(avg_score, 2),
        "total_quizzes": len(results),
        "improvement": round(improvement, 2),
        "consistency": calculate_score_consistency(scores),
        "best_score": max(scores),
        "worst_score": min(scores)
    }

def calculate_difficulty_trends(results: List[QuizResult], db: Session) -> Dict[str, Any]:
    """Calculer les tendances de difficulté."""
    # Pour l'instant, on utilise une logique simplifiée
    # Dans une implémentation complète, on analyserait les niveaux de difficulté des quiz
    
    recent_scores = [r.score for r in results[:5]]
    if len(recent_scores) >= 3:
        trend = "improving" if recent_scores[0] > recent_scores[-1] else "declining"
    else:
        trend = "stable"
    
    return {
        "trend": trend,
        "suggested_next_difficulty": "medium",  # Simplifié
        "confidence": "medium"
    }

def calculate_score_consistency(scores: List[float]) -> float:
    """Calculer la cohérence des scores."""
    if len(scores) < 2:
        return 100.0
    
    mean_score = sum(scores) / len(scores)
    variance = sum((score - mean_score) ** 2 for score in scores) / len(scores)
    
    # Plus la variance est faible, plus la cohérence est élevée
    consistency = max(0, 100 - (variance / 10))
    return round(consistency, 2)

def generate_progress_recommendations(progress: Dict, trends: Dict) -> List[str]:
    """Générer des recommandations basées sur la progression."""
    recommendations = []
    
    if progress.get("improvement", 0) > 10:
        recommendations.append("Progression excellente - Continuer sur cette voie")
    elif progress.get("improvement", 0) < -10:
        recommendations.append("Progression en baisse - Considérer un soutien supplémentaire")
    
    if progress.get("consistency", 100) < 70:
        recommendations.append("Performance irrégulière - Travailler la régularité")
    
    return recommendations 

def generate_test_questions(subject: str, count: int) -> List[Dict]:
    """Générer des questions de test basées sur la matière."""
    questions = []
    
    if subject.lower() == "français":
        questions = [
            {
                "id": 1,
                "question": "Quel est le genre du mot 'table' ?",
                "options": ["Masculin", "Féminin", "Neutre", "Variable"],
                "correct_answer": 1
            },
            {
                "id": 2,
                "question": "Conjuguez le verbe 'être' au présent de l'indicatif à la 1ère personne :",
                "options": ["Je suis", "Je serai", "J'étais", "Je serais"],
                "correct_answer": 0
            },
            {
                "id": 3,
                "question": "Identifiez la fonction du mot 'rapidement' dans la phrase : 'Il court rapidement'",
                "options": ["Sujet", "Verbe", "Complément", "Adverbe"],
                "correct_answer": 3
            }
        ]
    elif subject.lower() == "mathématiques":
        questions = [
            {
                "id": 1,
                "question": "Résolvez l'équation : 2x + 5 = 13",
                "options": ["x = 3", "x = 4", "x = 5", "x = 6"],
                "correct_answer": 1
            },
            {
                "id": 2,
                "question": "Calculez l'aire d'un rectangle de longueur 8 cm et largeur 5 cm",
                "options": ["13 cm²", "26 cm²", "40 cm²", "45 cm²"],
                "correct_answer": 2
            },
            {
                "id": 3,
                "question": "Simplifiez l'expression : 3x + 2x - x",
                "options": ["4x", "5x", "6x", "7x"],
                "correct_answer": 0
            }
        ]
    elif subject.lower() == "histoire":
        questions = [
            {
                "id": 1,
                "question": "En quelle année a eu lieu la Révolution française ?",
                "options": ["1789", "1799", "1809", "1819"],
                "correct_answer": 0
            },
            {
                "id": 2,
                "question": "Qui était Napoléon Bonaparte ?",
                "options": ["Un roi", "Un empereur", "Un président", "Un général"],
                "correct_answer": 1
            },
            {
                "id": 3,
                "question": "Quel événement marque le début de la Révolution française ?",
                "options": ["La prise de la Bastille", "Le serment du Jeu de Paume", "La Déclaration des Droits de l'Homme", "L'exécution de Louis XVI"],
                "correct_answer": 0
            }
        ]
    else:
        # Questions génériques pour les autres matières
        questions = [
            {
                "id": 1,
                "question": f"Question 1 sur {subject}",
                "options": ["Option A", "Option B", "Option C", "Option D"],
                "correct_answer": 0
            },
            {
                "id": 2,
                "question": f"Question 2 sur {subject}",
                "options": ["Option A", "Option B", "Option C", "Option D"],
                "correct_answer": 1
            },
            {
                "id": 3,
                "question": f"Question 3 sur {subject}",
                "options": ["Option A", "Option B", "Option C", "Option D"],
                "correct_answer": 2
            }
        ]
    
    # Retourner le nombre demandé de questions
    return questions[:count] 

def determine_student_level_for_subject(student_id: int, subject: str, db: Session) -> str:
    """Déterminer le niveau de l'étudiant pour une matière spécifique."""
    try:
        # Récupérer les 5 derniers résultats pour cette matière
        recent_results = db.query(QuizResult).filter(
            QuizResult.student_id == student_id,
            QuizResult.sujet == subject
        ).order_by(QuizResult.created_at.desc()).limit(5).all()
        
        if not recent_results:
            return "débutant"
        
        # Calculer le score moyen
        scores = [r.score for r in recent_results]
        avg_score = sum(scores) / len(scores)
        
        # Déterminer le niveau basé sur le score moyen
        if avg_score >= 80:
            return "avancé"
        elif avg_score >= 60:
            return "intermédiaire"
        else:
            return "débutant"
            
    except Exception as e:
        print(f"⚠️ [ADAPTIVE_QUIZZES] Erreur détermination niveau: {str(e)}")
        return "débutant" 