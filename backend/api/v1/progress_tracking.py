#!/usr/bin/env python3
"""
API pour le suivi des progrès des étudiants
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import text, func
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import json

from core.database import get_db
from core.security import get_current_user
from models.user import User, UserRole

router = APIRouter(tags=["progress_tracking"])

# ============================================================================
# ENDPOINTS POUR LE SUIVI DES PROGRÈS
# ============================================================================

@router.get("/student/{student_id}/metrics")
async def get_student_progress_metrics(
    student_id: int,
    subject: str = "Français",
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Récupérer les métriques de progrès d'un étudiant"""
    
    try:
        print(f"📊 Récupération des métriques de progrès pour étudiant {student_id}, matière: {subject}")
        
        # Vérifier que l'utilisateur a accès à ces données
        if current_user.role == UserRole.student and current_user.id != student_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Accès non autorisé aux données d'un autre étudiant"
            )
        
        # Récupérer les résultats des quiz adaptatifs
        adaptive_results = db.execute(text("""
            SELECT 
                total_score,
                max_score,
                started_at,
                completed_at
            FROM test_attempts 
            WHERE student_id = :student_id 
            AND status = 'completed'
            ORDER BY completed_at DESC
        """), {"student_id": student_id}).fetchall()
        
        # Récupérer les résultats des quiz normaux
        normal_results = db.execute(text("""
            SELECT 
                score,
                max_score,
                completed_at
            FROM quiz_results 
            WHERE student_id = :student_id
            ORDER BY completed_at DESC
        """), {"student_id": student_id}).fetchall()
        
        # Récupérer les résultats de remédiation
        remediation_results = db.execute(text("""
            SELECT 
                score,
                max_score,
                completed_at
            FROM remediation_results 
            WHERE student_id = :student_id
            ORDER BY completed_at DESC
        """), {"student_id": student_id}).fetchall()
        
        # Calculer les métriques
        all_results = []
        
        # Traiter les résultats adaptatifs
        for result in adaptive_results:
            if result.total_score is not None and result.max_score is not None:
                all_results.append({
                    'score': result.total_score,
                    'max_score': result.max_score,
                    'percentage': (result.total_score / result.max_score) * 100,
                    'date': result.completed_at or result.started_at
                })
        
        # Traiter les résultats normaux
        for result in normal_results:
            if result.score is not None and result.max_score is not None:
                all_results.append({
                    'score': result.score,
                    'max_score': result.max_score,
                    'percentage': (result.score / result.max_score) * 100,
                    'date': result.completed_at
                })
        
        # Traiter les résultats de remédiation
        for result in remediation_results:
            if result.score is not None and result.max_score is not None:
                all_results.append({
                    'score': result.score,
                    'max_score': result.max_score,
                    'percentage': (result.score / result.max_score) * 100,
                    'date': result.completed_at
                })
        
        if not all_results:
            # Aucun résultat trouvé, retourner des métriques par défaut
            return {
                "student_id": student_id,
                "subject": subject,
                "current_score": 0,
                "previous_score": 0,
                "improvement_rate": 0,
                "trend": "stable",
                "weak_areas_progress": [],
                "study_time_logged": 0,
                "quizzes_completed": 0,
                "last_updated": datetime.now().isoformat()
            }
        
        # Trier par date
        all_results.sort(key=lambda x: x['date'] if x['date'] else datetime.min.replace(tzinfo=None))
        
        # Calculer le score actuel (derniers résultats)
        recent_results = all_results[-5:] if len(all_results) >= 5 else all_results
        current_score = sum(r['percentage'] for r in recent_results) / len(recent_results)
        
        # Calculer le score précédent (résultats antérieurs)
        if len(all_results) >= 10:
            previous_results = all_results[-10:-5]
            previous_score = sum(r['percentage'] for r in previous_results) / len(previous_results)
        else:
            previous_score = current_score
        
        # Calculer l'amélioration
        improvement_rate = current_score - previous_score
        
        # Déterminer la tendance
        if improvement_rate > 5:
            trend = "improving"
        elif improvement_rate < -5:
            trend = "declining"
        else:
            trend = "stable"
        
        # Calculer le temps d'étude (estimation basée sur le nombre de quiz)
        study_time_logged = len(all_results) * 20  # 20 minutes par quiz en moyenne
        
        # Analyser les domaines faibles et créer des données de graphiques
        weak_areas_progress = []
        
        # Toujours créer des données pour les graphiques, même si pas de domaines faibles
        if current_score < 70:
            # Domaines faibles identifiés
            weak_areas_progress = [
                {
                    "topic": "Fondamentaux",
                    "initial_score": max(0, int(current_score - 20)),
                    "current_score": int(current_score),
                    "improvement": int(current_score - max(0, int(current_score - 20))),
                    "status": "improved" if improvement_rate > 0 else "stable",
                    "exercises_completed": len(all_results),
                    "time_spent": study_time_logged
                }
            ]
        else:
            # Même avec un bon score, créer des données pour les graphiques
            weak_areas_progress = [
                {
                    "topic": "Fondamentaux",
                    "initial_score": max(0, int(current_score - 15)),
                    "current_score": int(current_score),
                    "improvement": int(current_score - max(0, int(current_score - 15))),
                    "status": "excellent",
                    "exercises_completed": len(all_results),
                    "time_spent": study_time_logged
                },
                {
                    "topic": "Conjugaison",
                    "initial_score": max(0, int(current_score - 10)),
                    "current_score": int(current_score),
                    "improvement": int(current_score - max(0, int(current_score - 10))),
                    "status": "excellent",
                    "exercises_completed": len(all_results),
                    "time_spent": study_time_logged
                }
            ]
        
        # Créer des données de progression par semaine pour les graphiques
        weekly_progress = []
        if len(all_results) >= 4:
            # Diviser les résultats en 4 semaines
            week_size = max(1, len(all_results) // 4)
            for week in range(4):
                start_idx = week * week_size
                end_idx = min((week + 1) * week_size, len(all_results))
                week_results = all_results[start_idx:end_idx]
                
                if week_results:
                    week_avg = sum(r['percentage'] for r in week_results) / len(week_results)
                    weekly_progress.append({
                        "week": f"Semaine {week + 1}",
                        "score": round(week_avg, 1),
                        "quizzes_count": len(week_results)
                    })
                else:
                    weekly_progress.append({
                        "week": f"Semaine {week + 1}",
                        "score": 0,
                        "quizzes_count": 0
                    })
        else:
            # Si pas assez de données, créer des semaines factices
            for week in range(4):
                weekly_progress.append({
                    "week": f"Semaine {week + 1}",
                    "score": round(current_score, 1),
                    "quizzes_count": len(all_results)
                })

        metrics = {
            "student_id": student_id,
            "subject": subject,
            "current_score": round(current_score, 1),
            "previous_score": round(previous_score, 1),
            "improvement_rate": round(improvement_rate, 1),
            "trend": trend,
            "weak_areas_progress": weak_areas_progress,
            "study_time_logged": study_time_logged,
            "quizzes_completed": len(all_results),
            "weekly_progress": weekly_progress,
            "skill_breakdown": {
                "grammar": round(current_score * 0.9, 1),
                "vocabulary": round(current_score * 0.95, 1),
                "comprehension": round(current_score * 0.85, 1),
                "expression": round(current_score * 0.88, 1)
            },
            "last_updated": datetime.now().isoformat()
        }
        
        print(f"✅ Métriques de progrès calculées: {metrics}")
        return metrics
        
    except Exception as e:
        print(f"❌ Erreur lors du calcul des métriques: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors du calcul des métriques: {str(e)}"
        )

@router.get("/student/{student_id}/trends")
async def get_student_progress_trends(
    student_id: int,
    period: str = "4_weeks",
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Récupérer les tendances de progrès d'un étudiant"""
    
    try:
        print(f"📈 Récupération des tendances pour étudiant {student_id}, période: {period}")
        
        # Vérifier l'accès
        if current_user.role == UserRole.student and current_user.id != student_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Accès non autorisé"
            )
        
        # Calculer la date de début selon la période
        if period == "4_weeks":
            start_date = datetime.now() - timedelta(weeks=4)
        elif period == "2_months":
            start_date = datetime.now() - timedelta(weeks=8)
        else:
            start_date = datetime.now() - timedelta(weeks=4)
        
        # Récupérer les résultats par semaine
        weekly_results = db.execute(text("""
            SELECT 
                strftime('%Y-%W', completed_at) as week,
                AVG(CASE 
                    WHEN total_score IS NOT NULL THEN (total_score * 100.0 / max_score)
                    WHEN score IS NOT NULL THEN (score * 100.0 / max_score)
                    ELSE 0
                END) as avg_score
            FROM (
                SELECT completed_at, total_score, max_score, NULL as score, NULL as max_score_2
                FROM test_attempts 
                WHERE student_id = :student_id AND status = 'completed' AND completed_at >= :start_date
                UNION ALL
                SELECT completed_at, NULL, NULL, score, max_score
                FROM quiz_results 
                WHERE student_id = :student_id AND completed_at >= :start_date
            )
            WHERE completed_at IS NOT NULL
            GROUP BY week
            ORDER BY week
        """), {"student_id": student_id, "start_date": start_date}).fetchall()
        
        # Formater les résultats
        trends = []
        for i, result in enumerate(weekly_results):
            week_num = i + 1
            trends.append({
                "week": f"Semaine {week_num}",
                "score": round(result.avg_score or 0, 1)
            })
        
        # Compléter avec des semaines manquantes
        while len(trends) < 4:
            week_num = len(trends) + 1
            trends.append({
                "week": f"Semaine {week_num}",
                "score": 0
            })
        
        print(f"✅ Tendances calculées: {trends}")
        return {"trends": trends}
        
    except Exception as e:
        print(f"❌ Erreur lors du calcul des tendances: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors du calcul des tendances: {str(e)}"
        )

