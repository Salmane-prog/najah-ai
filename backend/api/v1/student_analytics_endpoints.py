from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, desc, and_
from core.database import get_db
from models.user import User
from models.quiz import QuizResult, Quiz
from models.learning_history import LearningHistory
from models.badge import Badge, UserBadge
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import json

router = APIRouter()

# ============================================================================
# ENDPOINT PERFORMANCE ÉTUDIANT
# ============================================================================

@router.get("/student/{student_id}/performance")
async def get_student_performance_analytics(
    student_id: int,
    period: str = Query("6m", description="Période: 1m, 3m, 6m, 1y"),
    db: Session = Depends(get_db)
):
    """Récupérer les données de performance d'un étudiant pour les graphiques"""
    try:
        # Vérifier que l'étudiant existe
        student = db.query(User).filter(User.id == student_id).first()
        if not student:
            raise HTTPException(status_code=404, detail="Étudiant non trouvé")
        
        # Déterminer la période
        now = datetime.utcnow()
        if period == "1m":
            start_date = now - timedelta(days=30)
            months = 1
        elif period == "3m":
            start_date = now - timedelta(days=90)
            months = 3
        elif period == "6m":
            start_date = now - timedelta(days=180)
            months = 6
        elif period == "1y":
            start_date = now - timedelta(days=365)
            months = 12
        else:
            start_date = now - timedelta(days=180)
            months = 6
        
        # Récupérer TOUS les types de résultats d'évaluation de la période
        # 1. Résultats de quiz classiques
        quiz_results = db.query(QuizResult).filter(
            QuizResult.student_id == student_id,
            QuizResult.created_at >= start_date,
            QuizResult.is_completed == True
        ).all()
        
        # 2. Tests adaptatifs (depuis TestAttempt)
        from models.adaptive_evaluation import TestAttempt, QuestionResponse
        adaptive_results = db.query(TestAttempt).filter(
            TestAttempt.student_id == student_id,
            TestAttempt.started_at >= start_date
        ).all()
        
        # 3. Résultats de remédiation
        from models.remediation import RemediationResult
        remediation_results = db.query(RemediationResult).filter(
            RemediationResult.student_id == student_id,
            RemediationResult.completed_at >= start_date
        ).all()
        
        # 4. Évaluations initiales
        from models.assessment import Assessment, AssessmentResult
        initial_assessments = db.query(AssessmentResult).join(Assessment).filter(
            Assessment.student_id == student_id,
            AssessmentResult.completed_at >= start_date
        ).all()
        
        # Combiner tous les résultats
        all_results = []
        
        # Ajouter les quiz classiques
        for result in quiz_results:
            all_results.append({
                'type': 'quiz',
                'score': result.score,
                'max_score': result.max_score,
                'date': result.created_at,
                'subject': result.sujet or 'Général',
                'title': f"Quiz {result.id}"
            })
        
        # Ajouter les tests adaptatifs
        for attempt in adaptive_results:
            if attempt.completed_at:  # Seulement les tests terminés
                # Calculer le score du test adaptatif
                responses = db.query(QuestionResponse).filter(
                    QuestionResponse.attempt_id == attempt.id
                ).all()
                
                if responses:
                    correct_answers = sum(1 for r in responses if r.is_correct)
                    total_questions = len(responses)
                    score_percentage = (correct_answers / total_questions * 100) if total_questions > 0 else 0
                    
                    all_results.append({
                        'type': 'adaptive',
                        'score': score_percentage,
                        'max_score': 100,
                        'date': attempt.completed_at,
                        'subject': 'Test Adaptatif',
                        'title': f"Test {attempt.id}"
                    })
        
        # Ajouter les résultats de remédiation
        for result in remediation_results:
            all_results.append({
                'type': 'remediation',
                'score': result.score,
                'max_score': result.max_score,
                'date': result.completed_at,
                'subject': result.topic or 'Remédiation',
                'title': f"Remédiation {result.exercise_type}"
            })
        
        # Ajouter les évaluations initiales
        for result in initial_assessments:
            if result.percentage is not None:
                all_results.append({
                    'type': 'initial_assessment',
                    'score': result.percentage,
                    'max_score': 100,
                    'date': result.completed_at,
                    'subject': 'Évaluation Initiale',
                    'title': 'Évaluation Initiale'
                })
        
        # Trier par date
        all_results.sort(key=lambda x: x['date'])
        
        if not all_results:
            # Retourner des données vides si aucun résultat
            return {
                "labels": [],
                "datasets": [{"data": []}]
            }
        
        # Grouper les résultats par mois
        monthly_data = {}
        for result in all_results:
            month_key = result['date'].strftime("%Y-%m")
            if month_key not in monthly_data:
                monthly_data[month_key] = []
            monthly_data[month_key].append(result['score'])
        
        # Créer les labels et données pour le graphique
        labels = []
        data = []
        
        # Générer les 6 derniers mois
        for i in range(months - 1, -1, -1):
            month_date = now - timedelta(days=30 * i)
            month_key = month_date.strftime("%Y-%m")
            
            # Format court pour l'affichage
            month_label = month_date.strftime("%b")
            labels.append(month_label)
            
            # Score moyen du mois ou 0 si pas de données
            if month_key in monthly_data:
                avg_score = sum(monthly_data[month_key]) / len(monthly_data[month_key])
                data.append(round(avg_score, 1))
            else:
                data.append(0)
        
        return {
            "labels": labels,
            "datasets": [{"data": data}]
        }
        
    except Exception as e:
        print(f"❌ Erreur get_student_performance_analytics: {e}")
        raise HTTPException(status_code=500, detail=f"Erreur lors de la récupération: {str(e)}")

# ============================================================================
# ENDPOINT PROGRESSION ÉTUDIANT
# ============================================================================

@router.get("/student/{student_id}/progress")
async def get_student_progress_analytics(
    student_id: int,
    limit: int = Query(10, description="Nombre de quiz à récupérer"),
    db: Session = Depends(get_db)
):
    """Récupérer la progression d'un étudiant (derniers quiz)"""
    try:
        # Vérifier que l'étudiant existe
        student = db.query(User).filter(User.id == student_id).first()
        if not student:
            raise HTTPException(status_code=404, detail="Étudiant non trouvé")
        
        # Récupérer TOUS les types de résultats d'évaluation
        all_results = []
        
        # 1. Résultats de quiz classiques
        quiz_results = db.query(QuizResult).filter(
            QuizResult.student_id == student_id,
            QuizResult.is_completed == True
        ).all()
        
        for result in quiz_results:
            all_results.append({
                'type': 'quiz',
                'score': result.score,
                'max_score': result.max_score,
                'date': result.created_at,
                'subject': result.sujet or 'Général',
                'title': f"Quiz {result.id}"
            })
        
        # 2. Tests adaptatifs
        from models.adaptive_evaluation import TestAttempt, QuestionResponse
        adaptive_results = db.query(TestAttempt).filter(
            TestAttempt.student_id == student_id
        ).all()
        
        for attempt in adaptive_results:
            if attempt.completed_at:
                responses = db.query(QuestionResponse).filter(
                    QuestionResponse.attempt_id == attempt.id
                ).all()
                
                if responses:
                    correct_answers = sum(1 for r in responses if r.is_correct)
                    total_questions = len(responses)
                    score_percentage = (correct_answers / total_questions * 100) if total_questions > 0 else 0
                    
                    all_results.append({
                        'type': 'adaptive',
                        'score': score_percentage,
                        'max_score': 100,
                        'date': attempt.completed_at,
                        'subject': 'Test Adaptatif',
                        'title': f"Test {attempt.id}"
                    })
        
        # 3. Résultats de remédiation
        from models.remediation import RemediationResult
        remediation_results = db.query(RemediationResult).filter(
            RemediationResult.student_id == student_id
        ).all()
        
        for result in remediation_results:
            all_results.append({
                'type': 'remediation',
                'score': result.score,
                'max_score': result.max_score,
                'date': result.completed_at,
                'subject': result.topic or 'Remédiation',
                'title': f"Remédiation {result.exercise_type}"
            })
        
        # 4. Évaluations initiales
        from models.assessment import Assessment, AssessmentResult
        initial_assessments = db.query(AssessmentResult).join(Assessment).filter(
            Assessment.student_id == student_id
        ).all()
        
        for result in initial_assessments:
            if result.percentage is not None:
                all_results.append({
                    'type': 'initial_assessment',
                    'score': result.percentage,
                    'max_score': 100,
                    'title': 'Évaluation Initiale',
                    'date': result.completed_at
                })
        
        # Trier par date et limiter (gérer les dates None)
        all_results = [r for r in all_results if r['date'] is not None]  # Filtrer les résultats sans date
        all_results.sort(key=lambda x: x['date'], reverse=True)
        all_results = all_results[:limit]
        
        if not all_results:
            return {
                "labels": [],
                "datasets": [{"data": []}]
            }
        
        # Formater les données pour le graphique
        labels = []
        data = []
        
        # Inverser l'ordre pour avoir la progression chronologique
        for result in reversed(all_results):
            # Label court avec type d'évaluation
            title = result['title']
            if len(title) > 15:
                title = title[:15] + "..."
            
            # Ajouter un indicateur de type
            type_icon = {
                'quiz': '📝',
                'adaptive': '🧠',
                'remediation': '🔧',
                'initial_assessment': '🎯'
            }.get(result['type'], '📊')
            
            labels.append(f"{type_icon} {title}")
            
            # Score en pourcentage
            score_percentage = (result['score'] / result['max_score'] * 100) if result['max_score'] > 0 else 0
            data.append(round(score_percentage, 1))
        
        return {
            "labels": labels,
            "datasets": [{"data": data}]
        }
        
    except Exception as e:
        print(f"❌ Erreur get_student_progress_analytics: {e}")
        raise HTTPException(status_code=500, detail=f"Erreur lors de la récupération: {str(e)}")

# ============================================================================
# ENDPOINT MATIÈRES ÉTUDIANT
# ============================================================================

@router.get("/student/{student_id}/subjects")
async def get_student_subjects_analytics(
    student_id: int,
    db: Session = Depends(get_db)
):
    """Récupérer la progression par matière d'un étudiant"""
    try:
        # Vérifier que l'étudiant existe
        student = db.query(User).filter(User.id == student_id).first()
        if not student:
            raise HTTPException(status_code=404, detail="Étudiant non trouvé")
        
        # Récupérer TOUS les types de résultats d'évaluation
        all_results = []
        
        # 1. Résultats de quiz classiques
        quiz_results = db.query(QuizResult).filter(
            QuizResult.student_id == student_id,
            QuizResult.is_completed == True
        ).all()
        
        for result in quiz_results:
            all_results.append({
                'type': 'quiz',
                'score': result.score,
                'max_score': result.max_score,
                'subject': result.sujet or 'Général'
            })
        
        # 2. Tests adaptatifs
        from models.adaptive_evaluation import TestAttempt, QuestionResponse
        adaptive_results = db.query(TestAttempt).filter(
            TestAttempt.student_id == student_id
        ).all()
        
        for attempt in adaptive_results:
            if attempt.completed_at:
                responses = db.query(QuestionResponse).filter(
                    QuestionResponse.attempt_id == attempt.id
                ).all()
                
                if responses:
                    correct_answers = sum(1 for r in responses if r.is_correct)
                    total_questions = len(responses)
                    score_percentage = (correct_answers / total_questions * 100) if total_questions > 0 else 0
                    
                    all_results.append({
                        'type': 'adaptive',
                        'score': score_percentage,
                        'max_score': 100,
                        'subject': 'Test Adaptatif'
                    })
        
        # 3. Résultats de remédiation
        from models.remediation import RemediationResult
        remediation_results = db.query(RemediationResult).filter(
            RemediationResult.student_id == student_id
        ).all()
        
        for result in remediation_results:
            all_results.append({
                'type': 'remediation',
                'score': result.score,
                'max_score': result.max_score,
                'subject': result.topic or 'Remédiation'
            })
        
        # 4. Évaluations initiales
        from models.assessment import Assessment, AssessmentResult
        initial_assessments = db.query(AssessmentResult).join(Assessment).filter(
            Assessment.student_id == student_id
        ).all()
        
        for result in initial_assessments:
            if result.percentage is not None:
                all_results.append({
                    'type': 'initial_assessment',
                    'score': result.percentage,
                    'max_score': 100,
                    'subject': 'Évaluation Initiale'
                })
        
        if not all_results:
            return []
        
        # Grouper par matière et calculer les statistiques
        subject_stats = {}
        for result in all_results:
            subject = result['subject']
            if subject not in subject_stats:
                subject_stats[subject] = {
                    "total_score": 0,
                    "max_score": 0,
                    "count": 0
                }
            
            subject_stats[subject]["total_score"] += result['score']
            subject_stats[subject]["max_score"] += result['max_score']
            subject_stats[subject]["count"] += 1
        
        # Calculer la progression par matière
        subjects_data = []
        for subject, stats in subject_stats.items():
            if stats["max_score"] > 0:
                progress_percentage = (stats["total_score"] / stats["max_score"]) * 100
                subjects_data.append({
                    "subject": subject,
                    "progress": round(progress_percentage, 1),
                    "quiz_count": stats["count"],
                    "average_score": round(stats["total_score"] / stats["count"], 1)
                })
        
        # Trier par progression décroissante
        subjects_data.sort(key=lambda x: x["progress"], reverse=True)
        
        return subjects_data
        
    except Exception as e:
        print(f"❌ Erreur get_student_subjects_analytics: {e}")
        raise HTTPException(status_code=500, detail=f"Erreur lors de la récupération: {str(e)}")

# ============================================================================
# ENDPOINT GAMIFICATION ÉTUDIANT
# ============================================================================

@router.get("/gamification/user-progress")
async def get_user_gamification_progress(
    db: Session = Depends(get_db)
):
    """Récupérer les données de gamification pour l'utilisateur connecté"""
    try:
        # Calculer le niveau basé sur TOUS les types de tests
        total_points = 0
        total_tests = 0
        
        # 1. Points des quiz classiques
        quiz_results = db.query(QuizResult).filter(QuizResult.is_completed == True).all()
        for result in quiz_results:
            if result.max_score > 0:
                score_percentage = (result.score / result.max_score) * 100
                if score_percentage >= 80:
                    total_points += 150  # Excellent
                elif score_percentage >= 60:
                    total_points += 100  # Bon
                else:
                    total_points += 50   # À améliorer
                total_tests += 1
        
        # 2. Points des tests adaptatifs
        from models.adaptive_evaluation import TestAttempt, QuestionResponse
        adaptive_results = db.query(TestAttempt).filter(TestAttempt.completed_at.isnot(None)).all()
        for attempt in adaptive_results:
            responses = db.query(QuestionResponse).filter(QuestionResponse.attempt_id == attempt.id).all()
            if responses:
                correct_answers = sum(1 for r in responses if r.is_correct)
                total_questions = len(responses)
                score_percentage = (correct_answers / total_questions * 100) if total_questions > 0 else 0
                
                if score_percentage >= 80:
                    total_points += 200  # Tests adaptatifs donnent plus de points
                elif score_percentage >= 60:
                    total_points += 150
                else:
                    total_points += 75
                total_tests += 1
        
        # 3. Points des remédiations
        from models.remediation import RemediationResult
        remediation_results = db.query(RemediationResult).all()
        for result in remediation_results:
            if result.max_score > 0:
                score_percentage = (result.score / result.max_score) * 100
                if score_percentage >= 80:
                    total_points += 120  # Remédiation réussie
                elif score_percentage >= 60:
                    total_points += 80
                else:
                    total_points += 40
                total_tests += 1
        
        # 4. Points des évaluations initiales
        from models.assessment import Assessment, AssessmentResult
        initial_assessments = db.query(AssessmentResult).join(Assessment).all()
        for result in initial_assessments:
            if result.percentage is not None:
                if result.percentage >= 80:
                    total_points += 300  # Évaluations initiales importantes
                elif result.percentage >= 60:
                    total_points += 200
                else:
                    total_points += 100
                total_tests += 1
        
        # Calculer le niveau
        current_level = min(20, (total_points // 500) + 1)  # Niveau max 20, 500 points par niveau
        
        return {
            "level": current_level,
            "total_points": total_points,
            "current_xp": total_points % 500,
            "xp_to_next_level": 500 - (total_points % 500),
            "progress_percentage": (total_points % 500) / 5,
            "total_tests": total_tests,
            "test_breakdown": {
                "quiz_classic": len(quiz_results),
                "adaptive_tests": len(adaptive_results),
                "remediation": len(remediation_results),
                "initial_assessments": len(initial_assessments)
            }
        }
        
    except Exception as e:
        print(f"❌ Erreur get_user_gamification_progress: {e}")
        raise HTTPException(status_code=500, detail=f"Erreur lors de la récupération: {str(e)}")

# ============================================================================
# ENDPOINT D'ATTRIBUTION AUTOMATIQUE DES BADGES
# ============================================================================

@router.post("/student/{student_id}/check-badges")
async def check_and_award_badges(
    student_id: int,
    db: Session = Depends(get_db)
):
    """Vérifier et attribuer automatiquement les badges basés sur les points"""
    try:
        # Vérifier que l'étudiant existe
        student = db.query(User).filter(User.id == student_id).first()
        if not student:
            raise HTTPException(status_code=404, detail="Étudiant non trouvé")
        
        # Récupérer les statistiques actuelles de l'étudiant
        from models.quiz import QuizResult
        from models.adaptive_evaluation import TestAttempt, QuestionResponse
        from models.remediation import RemediationResult
        from models.assessment import Assessment, AssessmentResult
        
        # Utiliser la même logique que la gamification pour la cohérence
        # 1. Points des quiz classiques
        quiz_results = db.query(QuizResult).filter(QuizResult.is_completed == True).all()
        quiz_count = len(quiz_results)
        
        # 2. Tests adaptatifs
        adaptive_results = db.query(TestAttempt).filter(TestAttempt.completed_at.isnot(None)).all()
        adaptive_count = len(adaptive_results)
        
        # 3. Remédiations
        remediation_results = db.query(RemediationResult).all()
        remediation_count = len(remediation_results)
        
        # 4. Évaluations initiales
        initial_assessments = db.query(AssessmentResult).join(Assessment).all()
        assessment_count = len(initial_assessments)
        
        # Calculer les points totaux avec la même logique que la gamification
        total_points = 0
        total_tests = 0
        
        # Points des quiz classiques
        for result in quiz_results:
            if result.max_score > 0:
                score_percentage = (result.score / result.max_score) * 100
                if score_percentage >= 80:
                    total_points += 150
                elif score_percentage >= 60:
                    total_points += 100
                else:
                    total_points += 50
                total_tests += 1
        
        # Points des tests adaptatifs
        for attempt in adaptive_results:
            responses = db.query(QuestionResponse).filter(QuestionResponse.attempt_id == attempt.id).all()
            if responses:
                correct_answers = sum(1 for r in responses if r.is_correct)
                total_questions = len(responses)
                score_percentage = (correct_answers / total_questions * 100) if total_questions > 0 else 0
                
                if score_percentage >= 80:
                    total_points += 200
                elif score_percentage >= 60:
                    total_points += 150
                else:
                    total_points += 75
                total_tests += 1
        
        # Points des remédiations
        for result in remediation_results:
            if result.max_score > 0:
                score_percentage = (result.score / result.max_score) * 100
                if score_percentage >= 80:
                    total_points += 120
                elif score_percentage >= 60:
                    total_points += 80
                else:
                    total_points += 40
                total_tests += 1
        
        # Points des évaluations initiales
        for result in initial_assessments:
            if result.percentage is not None:
                if result.percentage >= 80:
                    total_points += 300
                elif result.percentage >= 60:
                    total_points += 200
                else:
                    total_points += 100
                total_tests += 1
        
        # Calculer le niveau actuel avec la même logique
        current_level = min(20, (total_points // 500) + 1)
        
        # Vérifier et attribuer les badges automatiquement
        badges_awarded = []
        
        # Badges basés sur le niveau
        level_badges = [
            {"name": "Débutant", "description": "Premier pas dans l'apprentissage", "level": 1},
            {"name": "Apprenti", "description": "Niveau 5 atteint", "level": 5},
            {"name": "Élève Confirmé", "description": "Niveau 10 atteint", "level": 10},
            {"name": "Expert", "description": "Niveau 15 atteint", "level": 15},
            {"name": "Maître", "description": "Niveau 20 atteint", "level": 20}
        ]
        
        for badge_info in level_badges:
            if current_level >= badge_info["level"]:
                # Vérifier si le badge existe, sinon le créer
                badge = db.query(Badge).filter(Badge.name == badge_info["name"]).first()
                if not badge:
                    badge = Badge(
                        name=badge_info["name"],
                        description=badge_info["description"],
                        criteria=f"level >= {badge_info['level']}",
                        image_url=f"/badges/level-{badge_info['level']}.png",
                        secret=False
                    )
                    db.add(badge)
                    db.commit()
                    db.refresh(badge)
                
                # Vérifier si l'étudiant a déjà ce badge
                existing_badge = db.query(UserBadge).filter(
                    UserBadge.user_id == student_id,
                    UserBadge.badge_id == badge.id
                ).first()
                
                if not existing_badge:
                    user_badge = UserBadge(
                        user_id=student_id,
                        badge_id=badge.id,
                        progression=1.0,
                        awarded_at=datetime.utcnow()
                    )
                    db.add(user_badge)
                    badges_awarded.append(badge_info["name"])
        
        # Badges basés sur le nombre de tests
        test_badges = [
            {"name": "Premier Pas", "description": "Premier test complété", "count": 1},
            {"name": "Débutant Actif", "description": "10 tests complétés", "count": 10},
            {"name": "Étudiant Régulier", "description": "50 tests complétés", "count": 50},
            {"name": "Étudiant Assidu", "description": "100 tests complétés", "count": 100},
            {"name": "Étudiant Expert", "description": "500 tests complétés", "count": 500}
        ]
        
        for badge_info in test_badges:
            if total_tests >= badge_info["count"]:
                badge = db.query(Badge).filter(Badge.name == badge_info["name"]).first()
                if not badge:
                    badge = Badge(
                        name=badge_info["name"],
                        description=badge_info["description"],
                        criteria=f"total_tests >= {badge_info['count']}",
                        image_url=f"/badges/tests-{badge_info['count']}.png",
                        secret=False
                    )
                    db.add(badge)
                    db.commit()
                    db.refresh(badge)
                
                existing_badge = db.query(UserBadge).filter(
                    UserBadge.user_id == student_id,
                    UserBadge.badge_id == badge.id
                ).first()
                
                if not existing_badge:
                    user_badge = UserBadge(
                        user_id=student_id,
                        badge_id=badge.id,
                        progression=1.0,
                        awarded_at=datetime.utcnow()
                    )
                    db.add(user_badge)
                    badges_awarded.append(badge_info["name"])
        
        # Badges basés sur les points
        points_badges = [
            {"name": "Premiers Points", "description": "100 points accumulés", "points": 100},
            {"name": "Élève Motivé", "description": "1000 points accumulés", "points": 1000},
            {"name": "Élève Déterminé", "description": "5000 points accumulés", "points": 5000},
            {"name": "Élève Exceptionnel", "description": "10000 points accumulés", "points": 10000},
            {"name": "Légende", "description": "50000 points accumulés", "points": 50000}
        ]
        
        for badge_info in points_badges:
            if total_points >= badge_info["points"]:
                badge = db.query(Badge).filter(Badge.name == badge_info["name"]).first()
                if not badge:
                    badge = Badge(
                        name=badge_info["name"],
                        description=badge_info["description"],
                        criteria=f"total_points >= {badge_info['points']}",
                        image_url=f"/badges/points-{badge_info['points']}.png",
                        secret=False
                    )
                    db.add(badge)
                    db.commit()
                    db.refresh(badge)
                
                existing_badge = db.query(UserBadge).filter(
                    UserBadge.user_id == student_id,
                    UserBadge.badge_id == badge.id
                ).first()
                
                if not existing_badge:
                    user_badge = UserBadge(
                        user_id=student_id,
                        badge_id=badge.id,
                        progression=1.0,
                        awarded_at=datetime.utcnow()
                    )
                    db.add(user_badge)
                    badges_awarded.append(badge_info["name"])
        
        # Badges spécialisés par type de test
        if quiz_count >= 5:
            badge = db.query(Badge).filter(Badge.name == "Quiz Master").first()
            if not badge:
                badge = Badge(
                    name="Quiz Master",
                    description="5 quiz classiques complétés",
                    criteria="quiz_count >= 5",
                    image_url="/badges/quiz-master.png",
                    secret=False
                )
                db.add(badge)
                db.commit()
                db.refresh(badge)
            
            existing_badge = db.query(UserBadge).filter(
                UserBadge.user_id == student_id,
                UserBadge.badge_id == badge.id
            ).first()
            
            if not existing_badge:
                user_badge = UserBadge(
                    user_id=student_id,
                    badge_id=badge.id,
                    progression=1.0,
                    awarded_at=datetime.utcnow()
                )
                db.add(user_badge)
                badges_awarded.append("Quiz Master")
        
        if adaptive_count >= 3:
            badge = db.query(Badge).filter(Badge.name == "Test Adaptatif Expert").first()
            if not badge:
                badge = Badge(
                    name="Test Adaptatif Expert",
                    description="3 tests adaptatifs complétés",
                    criteria="adaptive_count >= 3",
                    image_url="/badges/adaptive-expert.png",
                    secret=False
                )
                db.add(badge)
                db.commit()
                db.refresh(badge)
            
            existing_badge = db.query(UserBadge).filter(
                UserBadge.user_id == student_id,
                UserBadge.badge_id == badge.id
            ).first()
            
            if not existing_badge:
                user_badge = UserBadge(
                    user_id=student_id,
                    badge_id=badge.id,
                    progression=1.0,
                    awarded_at=datetime.utcnow()
                )
                db.add(user_badge)
                badges_awarded.append("Test Adaptatif Expert")
        
        # Valider toutes les modifications
        db.commit()
        
        # Retourner le résumé
        return {
            "student_id": student_id,
            "current_level": current_level,
            "total_points": total_points,
            "total_tests": total_tests,
            "test_breakdown": {
                "quiz": quiz_count,
                "adaptive": adaptive_count,
                "remediation": remediation_count,
                "assessment": assessment_count
            },
            "badges_awarded": badges_awarded,
            "message": f"Vérification terminée. {len(badges_awarded)} nouveau(x) badge(s) attribué(s) !" if badges_awarded else "Aucun nouveau badge à attribuer."
        }
        
    except Exception as e:
        print(f"❌ Erreur check_and_award_badges: {e}")
        raise HTTPException(status_code=500, detail=f"Erreur lors de la vérification des badges: {str(e)}")

# ============================================================================
# ENDPOINT DE TEST SANS AUTHENTIFICATION
# ============================================================================

@router.get("/test/student/{student_id}/performance")
async def test_student_performance(
    student_id: int,
    db: Session = Depends(get_db)
):
    """Version de test sans authentification pour le développement"""
    return await get_student_performance_analytics(student_id, "6m", db)

@router.get("/test/student/{student_id}/progress")
async def test_student_progress(
    student_id: int,
    db: Session = Depends(get_db)
):
    """Version de test sans authentification pour le développement"""
    return await get_student_progress_analytics(student_id, 10, db)

@router.get("/test/student/{student_id}/subjects")
async def test_student_subjects(
    student_id: int,
    db: Session = Depends(get_db)
):
    """Version de test sans authentification pour le développement"""
    return await get_student_subjects_analytics(student_id, db)

@router.post("/test/student/{student_id}/check-badges")
async def test_check_badges(
    student_id: int,
    db: Session = Depends(get_db)
):
    """Version de test sans authentification pour le développement"""
    return await check_and_award_badges(student_id, db)

@router.get("/test/student/{student_id}/badges")
async def test_get_student_badges(
    student_id: int,
    db: Session = Depends(get_db)
):
    """Version de test sans authentification pour récupérer les badges d'un étudiant"""
    try:
        # Vérifier que l'étudiant existe
        student = db.query(User).filter(User.id == student_id).first()
        if not student:
            raise HTTPException(status_code=404, detail="Étudiant non trouvé")
        
        # Récupérer les badges de l'étudiant
        from models.badge import UserBadge, Badge
        
        user_badges = db.query(UserBadge).filter(UserBadge.user_id == student_id).all()
        
        badges_data = []
        for user_badge in user_badges:
            badge_info = db.query(Badge).filter(Badge.id == user_badge.badge_id).first()
            if badge_info:
                badges_data.append({
                    "id": user_badge.id,
                    "user_id": user_badge.user_id,
                    "badge_id": user_badge.badge_id,
                    "progression": user_badge.progression,
                    "awarded_at": user_badge.awarded_at.isoformat() if user_badge.awarded_at else None,
                    "badge": {
                        "name": badge_info.name,
                        "description": badge_info.description,
                        "image_url": badge_info.image_url,
                        "criteria": badge_info.criteria
                    }
                })
        
        return {
            "student_id": student_id,
            "total_badges": len(badges_data),
            "badges": badges_data
        }
        
    except Exception as e:
        print(f"❌ Erreur test_get_student_badges: {e}")
        raise HTTPException(status_code=500, detail=f"Erreur lors de la récupération: {str(e)}")
