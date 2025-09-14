from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, desc, and_
from core.database import get_db
from models.user import User
from models.quiz import QuizResult, Quiz, Question
from models.learning_history import LearningHistory
from models.content import Content
from api.v1.auth import get_current_user
from typing import List, Dict, Any
from datetime import datetime, timedelta
import json

router = APIRouter()

@router.post("/student/{student_id}/analyze")
def analyze_student_gaps_real(
    student_id: int,
    subject: str = "Français",
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Analyser les lacunes réelles d'apprentissage d'un étudiant basé sur ses performances."""
    raise HTTPException(status_code=501, detail="Utilisez l'endpoint -test pour les tests")

@router.post("/student/{student_id}/analyze-test")
def analyze_student_gaps_test(
    student_id: int,
    subject: str = "Français",
    db: Session = Depends(get_db)
):
    """Analyser les lacunes d'apprentissage d'un étudiant (version test sans auth)"""
    try:
        # Vérifier que l'étudiant existe
        student = db.query(User).filter(User.id == student_id).first()
        if not student:
            raise HTTPException(status_code=404, detail="Étudiant non trouvé")
        
        # Récupérer tous les résultats de quiz de l'étudiant
        quiz_results = db.query(QuizResult).filter(
            QuizResult.student_id == student_id,
            QuizResult.is_completed == True
        ).order_by(QuizResult.created_at.desc()).all()
        
        if not quiz_results:
            # Retourner des données de test si aucun quiz
            return {
                "student_id": student_id,
                "student_name": student.username or "Étudiant",
                "subject": subject,
                "identified_gaps": [
                    {
                        "topic": "Grammaire",
                        "current_level": "A1",
                        "target_level": "A2",
                        "gap_size": "medium",
                        "impact_score": 7,
                        "evidence": ["Aucun quiz disponible"],
                        "recommended_resources": ["Cours de grammaire A1", "Exercices pratiques"],
                        "estimated_time_to_close": "4-6 semaines"
                    }
                ],
                "priority_level": "medium",
                "analysis_date": datetime.utcnow().isoformat()
            }
        
        # Analyser les performances par sujet
        from collections import defaultdict
        subject_performance = defaultdict(list)
        
        for result in quiz_results:
            result_subject = result.sujet or "Général"
            subject_performance[result_subject].append(result.score)
        
        # Identifier les lacunes spécifiques
        identified_gaps = []
        total_performance = 0
        subject_count = 0
        
        for subj, scores in subject_performance.items():
            avg_score = sum(scores) / len(scores)
            total_performance += avg_score
            subject_count += 1
            
            # Déterminer le niveau actuel et cible
            if avg_score >= 80:
                current_level = "A2"
                target_level = "B1"
                gap_size = "small"
            elif avg_score >= 60:
                current_level = "A1"
                target_level = "A2"
                gap_size = "medium"
            else:
                current_level = "Débutant"
                target_level = "A1"
                gap_size = "large"
            
            # Calculer l'impact
            impact_score = max(1, min(10, int((100 - avg_score) / 10)))
            
            if avg_score < 70:  # Considérer comme une lacune si < 70%
                identified_gaps.append({
                    "topic": subj,
                    "current_level": current_level,
                    "target_level": target_level,
                    "gap_size": gap_size,
                    "impact_score": impact_score,
                    "evidence": [f"Score moyen: {avg_score:.1f}%", f"Basé sur {len(scores)} quiz"],
                    "recommended_resources": [
                        f"Cours de révision en {subj}",
                        f"Exercices pratiques {subj}",
                        f"Quiz d'entraînement {subj}"
                    ],
                    "estimated_time_to_close": "2-4 semaines" if gap_size == "small" else "4-6 semaines" if gap_size == "medium" else "6-8 semaines"
                })
        
        # Calculer le niveau de priorité global
        avg_performance = total_performance / subject_count if subject_count > 0 else 0
        
        if avg_performance < 50:
            priority_level = "high"
        elif avg_performance < 70:
            priority_level = "medium"
        else:
            priority_level = "low"
        
        # Générer des recommandations
        recommendations = []
        if len(identified_gaps) > 3:
            recommendations.append("Se concentrer sur 2-3 domaines prioritaires")
        if avg_performance < 60:
            recommendations.append("Réviser les concepts fondamentaux")
        if any(gap["gap_size"] == "large" for gap in identified_gaps):
            recommendations.append("Envisager un soutien pédagogique personnalisé")
        
        # Calculer le temps estimé de complétion
        estimated_completion_time = sum(
            {"small": 3, "medium": 5, "large": 7}.get(gap["gap_size"], 5) 
            for gap in identified_gaps
        )
        
        return {
            "student_id": student_id,
            "subject": subject,
            "analysis_date": datetime.utcnow().isoformat(),
            "identified_gaps": identified_gaps,
            "remediation_plan": [],  # Sera généré par un autre endpoint
            "estimated_completion_time": estimated_completion_time,
            "priority_level": priority_level,
            "overall_gap_score": round((100 - avg_performance) / 100, 2),
            "recommendations": recommendations,
            "data_based_on": f"{len(quiz_results)} quiz analysés"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Erreur analyze_student_gaps_real: {e}")
        raise HTTPException(status_code=500, detail=f"Erreur lors de l'analyse des lacunes: {str(e)}")

@router.get("/student/{student_id}/gaps")
def identify_student_gaps(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Identifier les lacunes d'apprentissage d'un étudiant."""
    try:
        # Récupérer tous les résultats de quiz de l'étudiant
        quiz_results = db.query(QuizResult).filter(
            QuizResult.student_id == student_id
        ).order_by(QuizResult.created_at.desc()).all()
        
        if not quiz_results:
            return {
                "student_id": student_id,
                "message": "Aucune donnée disponible pour l'analyse",
                "gaps": [],
                "recommendations": []
            }
        
        # Analyser les performances par sujet
        subject_analysis = analyze_subject_performance(quiz_results, db)
        
        # Identifier les lacunes spécifiques
        specific_gaps = identify_specific_gaps(quiz_results, db)
        
        # Analyser les tendances temporelles
        temporal_gaps = analyze_temporal_gaps(quiz_results)
        
        # Générer des recommandations
        recommendations = generate_gap_recommendations(subject_analysis, specific_gaps, temporal_gaps)
        
        return {
            "student_id": student_id,
            "analysis_date": datetime.utcnow().isoformat(),
            "subject_gaps": subject_analysis,
            "specific_gaps": specific_gaps,
            "temporal_gaps": temporal_gaps,
            "recommendations": recommendations,
            "overall_gap_score": calculate_overall_gap_score(subject_analysis)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur analyse lacunes: {str(e)}")

@router.get("/class/{class_id}/gaps")
def identify_class_gaps(
    class_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Identifier les lacunes communes d'une classe."""
    try:
        # Récupérer les étudiants de la classe
        from models.class_group import ClassStudent
        class_students = db.query(ClassStudent).filter(ClassStudent.class_id == class_id).all()
        student_ids = [cs.student_id for cs in class_students]
        
        if not student_ids:
            return {"message": "Aucun étudiant dans cette classe", "gaps": []}
        
        # Récupérer tous les résultats de la classe
        class_results = db.query(QuizResult).filter(
            QuizResult.student_id.in_(student_ids)
        ).all()
        
        # Analyser les lacunes communes
        common_gaps = analyze_common_gaps(class_results, db)
        
        # Identifier les sujets problématiques
        problematic_subjects = identify_problematic_subjects(class_results)
        
        # Générer des recommandations pour la classe
        class_recommendations = generate_class_recommendations(common_gaps, problematic_subjects)
        
        return {
            "class_id": class_id,
            "analysis_date": datetime.utcnow().isoformat(),
            "common_gaps": common_gaps,
            "problematic_subjects": problematic_subjects,
            "recommendations": class_recommendations,
            "students_analyzed": len(student_ids)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur analyse lacunes classe: {str(e)}")

@router.get("/subject/{subject}/gaps")
def identify_subject_gaps(
    subject: str,
    class_id: int = Query(None, description="ID de la classe (optionnel)"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Identifier les lacunes spécifiques à une matière."""
    try:
        # Construire la requête de base
        query = db.query(QuizResult).filter(QuizResult.sujet == subject)
        
        # Filtrer par classe si spécifiée
        if class_id:
            from models.class_group import ClassStudent
            class_students = db.query(ClassStudent).filter(ClassStudent.class_id == class_id).all()
            student_ids = [cs.student_id for cs in class_students]
            query = query.filter(QuizResult.student_id.in_(student_ids))
        
        results = query.all()
        
        if not results:
            return {
                "subject": subject,
                "message": f"Aucune donnée disponible pour {subject}",
                "gaps": []
            }
        
        # Analyser les lacunes spécifiques à la matière
        subject_gaps = analyze_subject_specific_gaps(results, subject, db)
        
        return {
            "subject": subject,
            "analysis_date": datetime.utcnow().isoformat(),
            "total_results": len(results),
            "gaps": subject_gaps,
            "remediation_suggestions": generate_subject_remediation_suggestions(subject_gaps)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur analyse lacunes matière: {str(e)}")

@router.get("/subject/{subject}/gaps-test")
def identify_subject_gaps_test(
    subject: str,
    class_id: int = Query(None, description="ID de la classe (optionnel)"),
    db: Session = Depends(get_db)
):
    """Version de test sans authentification pour le développement."""
    try:
        print(f"🔍 [GAP_ANALYSIS] Test endpoint appelé pour la matière: {subject}")
        
        # Construire la requête de base
        query = db.query(QuizResult).filter(QuizResult.sujet == subject)
        
        # Filtrer par classe si spécifiée
        if class_id:
            from models.class_group import ClassStudent
            class_students = db.query(ClassStudent).filter(ClassStudent.class_id == class_id).all()
            student_ids = [cs.student_id for cs in class_students]
            query = query.filter(QuizResult.student_id.in_(student_ids))
        
        results = query.all()
        print(f"📊 [GAP_ANALYSIS] Résultats trouvés pour {subject}: {len(results)}")
        
        if not results:
            return {
                "subject": subject,
                "message": f"Aucune donnée disponible pour {subject}",
                "gaps": [],
                "recommendations": []
            }
        
        # Analyser les lacunes spécifiques à la matière
        subject_gaps = analyze_subject_specific_gaps(results, subject, db)
        
        # Générer des recommandations de test
        recommendations = [
            f"Renforcer les exercices en {subject}",
            f"Réviser les concepts de base de {subject}",
            f"Proposer des exercices supplémentaires en {subject}"
        ]
        
        response_data = {
            "subject": subject,
            "analysis_date": datetime.utcnow().isoformat(),
            "total_results": len(results),
            "gaps": subject_gaps,
            "recommendations": recommendations,
            "gap_score": 75.5  # Score de test
        }
        
        print(f"✅ [GAP_ANALYSIS] Réponse de test générée pour {subject}")
        return response_data
        
    except Exception as e:
        print(f"❌ [GAP_ANALYSIS] Erreur dans l'endpoint de test: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erreur analyse lacunes matière: {str(e)}")

@router.get("/performance/analysis")
def analyze_performance_gaps(
    db: Session = Depends(get_db)
):
    """Analyse de performance globale sans authentification pour le développement."""
    try:
        print("🔍 [GAP_ANALYSIS] Analyse de performance appelée")
        
        # Récupérer tous les résultats
        all_results = db.query(QuizResult).filter(QuizResult.is_completed == True).all()
        print(f"📊 [GAP_ANALYSIS] Résultats totaux pour analyse performance: {len(all_results)}")
        
        if not all_results:
            return {
                "message": "Aucune donnée disponible pour l'analyse de performance",
                "gaps": [],
                "recommendations": [],
                "performance_metrics": {}
            }
        
        # Calculer les métriques de performance
        scores = [r.score for r in all_results]
        avg_score = sum(scores) / len(scores)
        gap_score = max(0, 100 - avg_score)
        
        # Analyser par matière
        subject_performance = {}
        for result in all_results:
            subject = result.sujet or "Général"
            if subject not in subject_performance:
                subject_performance[subject] = []
            subject_performance[subject].append(result.score)
        
        # Identifier les matières problématiques
        problematic_subjects = []
        for subject, scores_list in subject_performance.items():
            subject_avg = sum(scores_list) / len(scores_list)
            if subject_avg < 70:
                problematic_subjects.append({
                    "subject": subject,
                    "average_score": round(subject_avg, 2),
                    "total_attempts": len(scores_list),
                    "gap_type": "low_performance",
                    "suggestion": f"Renforcer l'enseignement de {subject}"
                })
        
        # Générer des recommandations de performance
        recommendations = []
        if gap_score > 30:
            recommendations.append("Performance globale faible - Considérer une révision générale")
        
        if problematic_subjects:
            worst_subject = min(problematic_subjects, key=lambda x: x["average_score"])
            recommendations.append(f"Focus prioritaire sur {worst_subject['subject']} (moyenne: {worst_subject['average_score']}%)")
        
        if avg_score < 60:
            recommendations.append("Considérer des sessions de remédiation supplémentaires")
        
        response_data = {
            "analysis_date": datetime.utcnow().isoformat(),
            "total_results": len(all_results),
            "average_score": round(avg_score, 2),
            "gap_score": round(gap_score, 2),
            "problematic_subjects": problematic_subjects,
            "recommendations": recommendations,
            "performance_metrics": {
                "total_students": len(set(r.student_id for r in all_results)),
                "total_subjects": len(subject_performance),
                "performance_trend": "stable" if avg_score >= 70 else "declining"
            }
        }
        
        print(f"✅ [GAP_ANALYSIS] Analyse de performance terminée - Score moyen: {avg_score:.2f}%")
        return response_data
        
    except Exception as e:
        print(f"❌ [GAP_ANALYSIS] Erreur dans l'analyse de performance: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erreur analyse performance: {str(e)}")

@router.get("/comprehensive/analysis")
def analyze_comprehensive_gaps(
    db: Session = Depends(get_db)
):
    """Analyse complète sans authentification pour le développement."""
    try:
        print("🔍 [GAP_ANALYSIS] Analyse complète appelée")
        
        # Récupérer tous les résultats
        all_results = db.query(QuizResult).filter(QuizResult.is_completed == True).all()
        print(f"📊 [GAP_ANALYSIS] Résultats totaux pour analyse complète: {len(all_results)}")
        
        if not all_results:
            return {
                "message": "Aucune donnée disponible pour l'analyse complète",
                "gaps": [],
                "recommendations": [],
                "comprehensive_metrics": {}
            }
        
        # 1. Analyse par matière
        subject_analysis = analyze_subject_performance(all_results, db)
        
        # 2. Identifier les lacunes spécifiques
        specific_gaps = identify_specific_gaps(all_results, db)
        
        # 3. Analyser les tendances temporelles
        temporal_gaps = analyze_temporal_gaps(all_results)
        
        # 4. Analyser les lacunes communes
        common_gaps = analyze_common_gaps(all_results, db)
        
        # 5. Calculer le score global
        overall_gap_score = calculate_overall_gap_score(subject_analysis)
        
        # 6. Générer des recommandations complètes
        comprehensive_recommendations = []
        
        # Recommandations basées sur les sujets faibles
        weak_subjects = [subject for subject, data in subject_analysis.items() 
                        if data.get("average_score", 0) < 70]
        if weak_subjects:
            comprehensive_recommendations.append(f"Focus prioritaire sur: {', '.join(weak_subjects)}")
        
        # Recommandations basées sur les lacunes spécifiques
        if specific_gaps:
            high_severity_gaps = [gap for gap in specific_gaps if gap.get("severity") == "high"]
            if high_severity_gaps:
                comprehensive_recommendations.append(f"Réviser {len(high_severity_gaps)} concepts critiques identifiés")
        
        # Recommandations basées sur les tendances
        if temporal_gaps.get("trend") == "declining":
            comprehensive_recommendations.append("Performance en baisse - Considérer un soutien supplémentaire")
        
        # Recommandations basées sur les lacunes communes
        if common_gaps:
            comprehensive_recommendations.append(f"Lacunes communes identifiées dans {len(common_gaps)} matières")
        
        # 7. Préparer la réponse complète
        response_data = {
            "analysis_date": datetime.utcnow().isoformat(),
            "total_results": len(all_results),
            "overall_gap_score": round(overall_gap_score, 2),
            "subject_analysis": subject_analysis,
            "specific_gaps": specific_gaps,
            "temporal_gaps": temporal_gaps,
            "common_gaps": common_gaps,
            "recommendations": comprehensive_recommendations,
            "comprehensive_metrics": {
                "total_students": len(set(r.student_id for r in all_results)),
                "total_subjects": len(subject_analysis),
                "total_gaps_identified": len(specific_gaps) + len(common_gaps),
                "analysis_coverage": "complete"
            }
        }
        
        print(f"✅ [GAP_ANALYSIS] Analyse complète terminée - Score global: {overall_gap_score:.2f}%")
        return response_data
        
    except Exception as e:
        print(f"❌ [GAP_ANALYSIS] Erreur dans l'analyse complète: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erreur analyse complète: {str(e)}")

@router.get("/dashboard-data")
def get_gap_analysis_dashboard_data(
    db: Session = Depends(get_db)
):
    """Récupérer les données pour le dashboard d'analyse des lacunes."""
    try:
        print("🔍 [GAP_ANALYSIS] Début de récupération des données...")
        
        # Récupérer les étudiants
        students = db.query(User).filter(User.role == "student").all()
        print(f"📊 [GAP_ANALYSIS] Étudiants trouvés: {len(students)}")
        
        student_list = []
        for s in students:
            name = f"{s.first_name} {s.last_name}" if s.first_name and s.last_name else s.email
            student_list.append({"id": s.id, "name": name})
            print(f"  - Étudiant: ID={s.id}, Nom={name}")
        
        # Récupérer les types d'analyse disponibles
        analysis_types = [
            {"id": "subject", "name": "Analyse par matière"},
            {"id": "temporal", "name": "Analyse temporelle"},
            {"id": "performance", "name": "Analyse de performance"},
            {"id": "comprehensive", "name": "Analyse complète"}
        ]
        
        # Récupérer les matières disponibles depuis les quiz
        subjects = db.query(Quiz.subject).distinct().all()
        print(f"📊 [GAP_ANALYSIS] Matières trouvées: {len(subjects)}")
        
        subject_list = []
        for s in subjects:
            if s[0]:  # Vérifier que le sujet n'est pas None
                subject_list.append({"id": s[0], "name": s[0]})
                print(f"  - Matière: {s[0]}")
        
        # Calculer un score global des lacunes
        total_results = db.query(QuizResult).count()
        print(f"📊 [GAP_ANALYSIS] Total résultats: {total_results}")
        
        if total_results > 0:
            # Utiliser is_completed pour filtrer les résultats valides
            completed_results = db.query(QuizResult).filter(QuizResult.is_completed == True).all()
            print(f"📊 [GAP_ANALYSIS] Résultats complétés: {len(completed_results)}")
            
            if completed_results:
                scores = [r.score for r in completed_results]
                avg_score = sum(scores) / len(scores)
                gap_score = max(0, 100 - avg_score)
                print(f"📊 [GAP_ANALYSIS] Score moyen: {avg_score:.1f}%, Gap score: {gap_score:.1f}%")
            else:
                gap_score = 0
                print("⚠️ [GAP_ANALYSIS] Aucun résultat complété trouvé")
        else:
            gap_score = 0
            print("⚠️ [GAP_ANALYSIS] Aucun résultat trouvé")
        
        response_data = {
            "students": student_list,
            "analysis_types": analysis_types,
            "subjects": subject_list,
            "gap_score": round(gap_score, 1),
            "total_students": len(student_list),
            "total_quizzes": total_results
        }
        
        print(f"✅ [GAP_ANALYSIS] Données préparées: {len(student_list)} étudiants, {len(analysis_types)} types d'analyse, {len(subject_list)} matières")
        return response_data
        
    except Exception as e:
        print(f"❌ [GAP_ANALYSIS] Erreur: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erreur récupération données: {str(e)}")

@router.get("/dashboard-data-test")
def get_gap_analysis_dashboard_data_test(db: Session = Depends(get_db)):
    """Données du dashboard d'analyse des lacunes (version test sans auth)."""
    try:
        # Récupérer tous les résultats de quiz
        quiz_results = db.query(QuizResult).all()
        
        if not quiz_results:
            return {
                "global_gap_score": 0,
                "gaps": [],
                "message": "Aucune donnée disponible"
            }
        
        # Calculer le score global des lacunes
        total_score = sum(result.score for result in quiz_results)
        avg_score = total_score / len(quiz_results) if quiz_results else 0
        global_gap_score = max(0, 100 - avg_score)
        
        # Analyser les lacunes par sujet
        gaps = []
        subjects = db.query(QuizResult.sujet).distinct().all()
        
        for subject in subjects:
            if subject[0]:  # Vérifier que le sujet n'est pas None
                subject_results = [r for r in quiz_results if r.sujet == subject[0]]
                if subject_results:
                    subject_avg = sum(r.score for r in subject_results) / len(subject_results)
                    gaps.append({
                        "subject": subject[0],
                        "average_score": round(subject_avg, 2),
                        "gap_score": max(0, 100 - subject_avg),
                        "quiz_count": len(subject_results)
                    })
        
        return {
            "global_gap_score": round(global_gap_score, 2),
            "gaps": gaps,
            "total_quizzes": len(quiz_results),
            "overall_average": round(avg_score, 2)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur analyse des lacunes: {str(e)}")

@router.get("/temporal/analysis")
def analyze_temporal_gaps_advanced(
    db: Session = Depends(get_db)
):
    """Analyse temporelle avancée sans authentification pour le développement."""
    try:
        print("🔍 [GAP_ANALYSIS] Analyse temporelle avancée appelée")
        
        # Récupérer tous les résultats avec dates
        all_results = db.query(QuizResult).filter(QuizResult.is_completed == True).order_by(QuizResult.created_at).all()
        print(f"📊 [GAP_ANALYSIS] Résultats totaux pour analyse temporelle: {len(all_results)}")
        
        if not all_results:
            return {
                "message": "Aucune donnée disponible pour l'analyse temporelle",
                "temporal_analysis": {},
                "trends": [],
                "recommendations": []
            }
        
        # 1. Analyse par période (semaine, mois, trimestre)
        weekly_trends = analyze_weekly_trends(all_results)
        monthly_trends = analyze_monthly_trends(all_results)
        quarterly_trends = analyze_quarterly_trends(all_results)
        
        # 2. Détecter les patterns saisonniers
        seasonal_patterns = detect_seasonal_patterns(all_results)
        
        # 3. Identifier les périodes de régression
        regression_periods = identify_regression_periods(all_results)
        
        # 4. Analyser la progression par étudiant
        student_progression = analyze_student_progression(all_results)
        
        # 5. Générer des recommandations temporelles
        temporal_recommendations = generate_temporal_recommendations(
            weekly_trends, monthly_trends, regression_periods, seasonal_patterns
        )
        
        response_data = {
            "analysis_date": datetime.utcnow().isoformat(),
            "total_results": len(all_results),
            "temporal_analysis": {
                "weekly_trends": weekly_trends,
                "monthly_trends": monthly_trends,
                "quarterly_trends": quarterly_trends,
                "seasonal_patterns": seasonal_patterns,
                "regression_periods": regression_periods,
                "student_progression": student_progression
            },
            "trends": [
                {"period": "weekly", "data": weekly_trends},
                {"period": "monthly", "data": monthly_trends},
                {"period": "quarterly", "data": quarterly_trends}
            ],
            "recommendations": temporal_recommendations
        }
        
        print(f"✅ [GAP_ANALYSIS] Analyse temporelle avancée terminée")
        return response_data
        
    except Exception as e:
        print(f"❌ [GAP_ANALYSIS] Erreur dans l'analyse temporelle: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erreur analyse temporelle: {str(e)}")

def analyze_subject_performance(quiz_results: List[QuizResult], db: Session) -> Dict[str, Any]:
    """Analyser les performances par sujet."""
    subject_performance = {}
    
    for result in quiz_results:
        subject = result.sujet or "Général"
        if subject not in subject_performance:
            subject_performance[subject] = {
                "total_quizzes": 0,
                "total_score": 0,
                "scores": [],
                "weak_areas": [],
                "strength_areas": []
            }
        
        subject_performance[subject]["total_quizzes"] += 1
        subject_performance[subject]["total_score"] += result.score
        subject_performance[subject]["scores"].append(result.score)
    
    # Calculer les moyennes et identifier les lacunes
    for subject, data in subject_performance.items():
        data["average_score"] = round(data["total_score"] / data["total_quizzes"], 2)
        
        # Identifier les scores faibles (< 70%)
        weak_scores = [score for score in data["scores"] if score < 70]
        if weak_scores:
            data["weak_areas"] = {
                "count": len(weak_scores),
                "percentage": round((len(weak_scores) / len(data["scores"])) * 100, 2),
                "average_weak_score": round(sum(weak_scores) / len(weak_scores), 2)
            }
        
        # Identifier les forces (> 85%)
        strong_scores = [score for score in data["scores"] if score > 85]
        if strong_scores:
            data["strength_areas"] = {
                "count": len(strong_scores),
                "percentage": round((len(strong_scores) / len(data["scores"])) * 100, 2)
            }
    
    return subject_performance

def identify_specific_gaps(quiz_results: List[QuizResult], db: Session) -> List[Dict]:
    """Identifier les lacunes spécifiques basées sur les questions."""
    gaps = []
    
    for result in quiz_results:
        if result.score < 70:  # Score faible
            # Récupérer les détails du quiz
            quiz = db.query(Quiz).filter(Quiz.id == result.quiz_id).first()
            if quiz:
                gaps.append({
                    "quiz_id": result.quiz_id,
                    "quiz_title": quiz.title,
                    "subject": result.sujet,
                    "score": result.score,
                    "date": result.created_at.isoformat(),
                    "gap_type": "low_performance",
                    "severity": "high" if result.score < 50 else "medium",
                    "suggestion": f"Réviser les concepts de {result.sujet} abordés dans '{quiz.title}'"
                })
    
    return gaps

def analyze_temporal_gaps(quiz_results: List[QuizResult]) -> Dict[str, Any]:
    """Analyser les lacunes temporelles (tendances)."""
    if len(quiz_results) < 3:
        return {"message": "Données insuffisantes pour l'analyse temporelle"}
    
    # Grouper par mois
    monthly_performance = {}
    for result in quiz_results:
        month_key = result.created_at.strftime('%Y-%m')
        if month_key not in monthly_performance:
            monthly_performance[month_key] = []
        monthly_performance[month_key].append(result.score)
    
    # Calculer les moyennes mensuelles
    monthly_averages = {}
    for month, scores in monthly_performance.items():
        monthly_averages[month] = round(sum(scores) / len(scores), 2)
    
    # Identifier les tendances
    months = sorted(monthly_averages.keys())
    if len(months) >= 2:
        recent_avg = monthly_averages[months[-1]]
        previous_avg = monthly_averages[months[-2]]
        trend = "improving" if recent_avg > previous_avg else "declining" if recent_avg < previous_avg else "stable"
    else:
        trend = "insufficient_data"
    
    return {
        "monthly_performance": monthly_averages,
        "trend": trend,
        "recent_performance": monthly_averages.get(months[-1] if months else None, 0),
        "performance_consistency": calculate_performance_consistency(monthly_averages)
    }

def analyze_common_gaps(class_results: List[QuizResult], db: Session) -> List[Dict]:
    """Analyser les lacunes communes à une classe."""
    # Grouper par sujet
    subject_gaps = {}
    for result in class_results:
        subject = result.sujet or "Général"
        if subject not in subject_gaps:
            subject_gaps[subject] = []
        subject_gaps[subject].append(result.score)
    
    common_gaps = []
    for subject, scores in subject_gaps.items():
        avg_score = sum(scores) / len(scores)
        weak_performers = [score for score in scores if score < 70]
        
        if len(weak_performers) > len(scores) * 0.3:  # Plus de 30% d'étudiants en difficulté
            common_gaps.append({
                "subject": subject,
                "average_score": round(avg_score, 2),
                "weak_performers_percentage": round((len(weak_performers) / len(scores)) * 100, 2),
                "gap_type": "common_difficulty",
                "severity": "high" if avg_score < 60 else "medium",
                "suggestion": f"Renforcer l'enseignement de {subject} avec des exercices supplémentaires"
            })
    
    return common_gaps

def identify_problematic_subjects(class_results: List[QuizResult]) -> List[Dict]:
    """Identifier les matières problématiques pour la classe."""
    subject_stats = {}
    
    for result in class_results:
        subject = result.sujet or "Général"
        if subject not in subject_stats:
            subject_stats[subject] = []
        subject_stats[subject].append(result.score)
    
    problematic_subjects = []
    for subject, scores in subject_stats.items():
        avg_score = sum(scores) / len(scores)
        if avg_score < 70:  # Seuil de difficulté
            problematic_subjects.append({
                "subject": subject,
                "average_score": round(avg_score, 2),
                "total_attempts": len(scores),
                "difficulty_level": "high" if avg_score < 50 else "medium",
                "recommendation": f"Considérer une approche pédagogique différente pour {subject}"
            })
    
    return sorted(problematic_subjects, key=lambda x: x["average_score"])

def analyze_subject_specific_gaps(results: List[QuizResult], subject: str, db: Session) -> List[Dict]:
    """Analyser les lacunes spécifiques à une matière."""
    gaps = []
    
    # Analyser par niveau de difficulté
    difficulty_gaps = {}
    for result in results:
        quiz = db.query(Quiz).filter(Quiz.id == result.quiz_id).first()
        if quiz:
            level = getattr(quiz, 'level', 'medium')
            if level not in difficulty_gaps:
                difficulty_gaps[level] = []
            difficulty_gaps[level].append(result.score)
    
    for level, scores in difficulty_gaps.items():
        avg_score = sum(scores) / len(scores)
        if avg_score < 70:
            gaps.append({
                "gap_type": "difficulty_level",
                "level": level,
                "average_score": round(avg_score, 2),
                "suggestion": f"Renforcer les exercices de niveau {level} en {subject}"
            })
    
    # Analyser les tendances temporelles
    recent_results = [r for r in results if r.created_at >= datetime.utcnow() - timedelta(days=30)]
    if recent_results:
        recent_avg = sum(r.score for r in recent_results) / len(recent_results)
        if recent_avg < 70:
            gaps.append({
                "gap_type": "recent_performance",
                "period": "30 derniers jours",
                "average_score": round(recent_avg, 2),
                "suggestion": f"Performance récente faible en {subject}, nécessite une attention immédiate"
            })
    
    return gaps

def generate_gap_recommendations(subject_analysis: Dict, specific_gaps: List[Dict], temporal_gaps: Dict) -> List[str]:
    """Générer des recommandations basées sur l'analyse des lacunes."""
    recommendations = []
    
    # Recommandations basées sur les sujets faibles
    weak_subjects = [subject for subject, data in subject_analysis.items() 
                    if data.get("average_score", 0) < 70]
    
    if weak_subjects:
        recommendations.append(f"Focus prioritaire sur: {', '.join(weak_subjects)}")
    
    # Recommandations basées sur les lacunes spécifiques
    if specific_gaps:
        high_severity_gaps = [gap for gap in specific_gaps if gap.get("severity") == "high"]
        if high_severity_gaps:
            recommendations.append(f"Réviser {len(high_severity_gaps)} concepts critiques identifiés")
    
    # Recommandations basées sur les tendances
    if temporal_gaps.get("trend") == "declining":
        recommendations.append("Performance en baisse - Considérer un soutien supplémentaire")
    
    return recommendations

def generate_class_recommendations(common_gaps: List[Dict], problematic_subjects: List[Dict]) -> List[str]:
    """Générer des recommandations pour la classe."""
    recommendations = []
    
    if common_gaps:
        recommendations.append(f"Lacunes communes identifiées dans {len(common_gaps)} matières")
    
    if problematic_subjects:
        worst_subject = min(problematic_subjects, key=lambda x: x["average_score"])
        recommendations.append(f"Focus prioritaire sur {worst_subject['subject']} (moyenne: {worst_subject['average_score']}%)")
    
    return recommendations

def generate_subject_remediation_suggestions(gaps: List[Dict]) -> List[str]:
    """Générer des suggestions de remédiation pour une matière."""
    suggestions = []
    
    for gap in gaps:
        if gap["gap_type"] == "difficulty_level":
            suggestions.append(f"Exercices supplémentaires niveau {gap['level']}")
        elif gap["gap_type"] == "recent_performance":
            suggestions.append("Séances de remédiation immédiate")
    
    return suggestions

def calculate_overall_gap_score(subject_analysis: Dict) -> float:
    """Calculer un score global de lacunes."""
    if not subject_analysis:
        return 0.0
    
    total_score = 0
    total_weight = 0
    
    for subject, data in subject_analysis.items():
        weight = data["total_quizzes"]  # Plus de quiz = plus de poids
        score = data.get("average_score", 0)
        
        # Convertir en score de lacune (0 = pas de lacune, 100 = lacune maximale)
        gap_score = max(0, 100 - score)
        
        total_score += gap_score * weight
        total_weight += weight
    
    return round(total_score / total_weight, 2) if total_weight > 0 else 0.0

def calculate_performance_consistency(monthly_averages: Dict[str, float]) -> float:
    """Calculer la cohérence des performances."""
    if len(monthly_averages) < 2:
        return 100.0
    
    values = list(monthly_averages.values())
    mean_value = sum(values) / len(values)
    variance = sum((value - mean_value) ** 2 for value in values) / len(values)
    
    # Plus la variance est faible, plus la cohérence est élevée
    consistency = max(0, 100 - (variance / 10))
    return round(consistency, 2) 

def analyze_weekly_trends(results: List[QuizResult]) -> Dict[str, Any]:
    """Analyser les tendances hebdomadaires."""
    weekly_data = {}
    
    for result in results:
        week_key = result.created_at.strftime('%Y-W%U')
        if week_key not in weekly_data:
            weekly_data[week_key] = []
        weekly_data[week_key].append(result.score)
    
    weekly_averages = {}
    for week, scores in weekly_data.items():
        weekly_averages[week] = {
            "average_score": round(sum(scores) / len(scores), 2),
            "total_attempts": len(scores),
            "improvement_rate": calculate_improvement_rate(week, weekly_data)
        }
    
    return weekly_averages

def analyze_monthly_trends(results: List[QuizResult]) -> Dict[str, Any]:
    """Analyser les tendances mensuelles."""
    monthly_data = {}
    
    for result in results:
        month_key = result.created_at.strftime('%Y-%m')
        if month_key not in monthly_data:
            monthly_data[month_key] = []
        monthly_data[month_key].append(result.score)
    
    monthly_averages = {}
    for month, scores in monthly_data.items():
        monthly_averages[month] = {
            "average_score": round(sum(scores) / len(scores), 2),
            "total_attempts": len(scores),
            "consistency_score": calculate_consistency_score(scores),
            "growth_rate": calculate_growth_rate(month, monthly_data)
        }
    
    return monthly_averages

def analyze_quarterly_trends(results: List[QuizResult]) -> Dict[str, Any]:
    """Analyser les tendances trimestrielles."""
    quarterly_data = {}
    
    for result in results:
        quarter = f"{result.created_at.year}-Q{(result.created_at.month-1)//3 + 1}"
        if quarter not in quarterly_data:
            quarterly_data[quarter] = []
        quarterly_data[quarter].append(result.score)
    
    quarterly_averages = {}
    for quarter, scores in quarterly_data.items():
        quarterly_averages[quarter] = {
            "average_score": round(sum(scores) / len(scores), 2),
            "total_attempts": len(scores),
            "performance_trend": "improving" if len(scores) > 10 else "stable"
        }
    
    return quarterly_averages

def detect_seasonal_patterns(results: List[QuizResult]) -> Dict[str, Any]:
    """Détecter les patterns saisonniers."""
    seasonal_data = {}
    
    for result in results:
        month = result.created_at.month
        season = get_season(month)
        if season not in seasonal_data:
            seasonal_data[season] = []
        seasonal_data[season].append(result.score)
    
    seasonal_patterns = {}
    for season, scores in seasonal_data.items():
        seasonal_patterns[season] = {
            "average_score": round(sum(scores) / len(scores), 2),
            "total_attempts": len(scores),
            "performance_level": "high" if sum(scores) / len(scores) > 80 else "medium" if sum(scores) / len(scores) > 60 else "low"
        }
    
    return seasonal_patterns

def identify_regression_periods(results: List[QuizResult]) -> List[Dict]:
    """Identifier les périodes de régression."""
    regression_periods = []
    
    # Grouper par semaine et identifier les baisses
    weekly_data = {}
    for result in results:
        week_key = result.created_at.strftime('%Y-W%U')
        if week_key not in weekly_data:
            weekly_data[week_key] = []
        weekly_data[week_key].append(result.score)
    
    weeks = sorted(weekly_data.keys())
    for i in range(1, len(weeks)):
        current_avg = sum(weekly_data[weeks[i]]) / len(weekly_data[weeks[i]])
        previous_avg = sum(weekly_data[weeks[i-1]]) / len(weekly_data[weeks[i-1]])
        
        if current_avg < previous_avg - 10:  # Baisse de plus de 10%
            regression_periods.append({
                "period": weeks[i],
                "previous_average": round(previous_avg, 2),
                "current_average": round(current_avg, 2),
                "decline_percentage": round(((previous_avg - current_avg) / previous_avg) * 100, 2),
                "severity": "high" if current_avg < previous_avg - 20 else "medium"
            })
    
    return regression_periods

def analyze_student_progression(results: List[QuizResult]) -> Dict[str, Any]:
    """Analyser la progression par étudiant."""
    student_data = {}
    
    for result in results:
        if result.student_id not in student_data:
            student_data[result.student_id] = []
        student_data[result.student_id].append({
            "score": result.score,
            "date": result.created_at,
            "subject": result.sujet
        })
    
    student_progression = {}
    for student_id, attempts in student_data.items():
        # Trier par date
        attempts.sort(key=lambda x: x["date"])
        
        if len(attempts) >= 3:
            # Calculer la progression
            first_third = attempts[:len(attempts)//3]
            last_third = attempts[-len(attempts)//3:]
            
            initial_avg = sum(a["score"] for a in first_third) / len(first_third)
            final_avg = sum(a["score"] for a in last_third) / len(last_third)
            
            progression_rate = ((final_avg - initial_avg) / initial_avg) * 100 if initial_avg > 0 else 0
            
            student_progression[student_id] = {
                "total_attempts": len(attempts),
                "initial_average": round(initial_avg, 2),
                "final_average": round(final_avg, 2),
                "progression_rate": round(progression_rate, 2),
                "progression_status": "improving" if progression_rate > 5 else "stable" if progression_rate > -5 else "declining"
            }
    
    return student_progression

def generate_temporal_recommendations(weekly_trends, monthly_trends, regression_periods, seasonal_patterns):
    """Générer des recommandations basées sur l'analyse temporelle."""
    recommendations = []
    
    # Recommandations basées sur les régressions
    if regression_periods:
        recent_regressions = [r for r in regression_periods if r["severity"] == "high"]
        if recent_regressions:
            recommendations.append(f"Attention: {len(recent_regressions)} périodes de régression détectées")
    
    # Recommandations basées sur les patterns saisonniers
    weak_seasons = [season for season, data in seasonal_patterns.items() if data["performance_level"] == "low"]
    if weak_seasons:
        recommendations.append(f"Performance faible pendant: {', '.join(weak_seasons)}")
    
    # Recommandations basées sur les tendances mensuelles
    if monthly_trends:
        recent_months = sorted(monthly_trends.keys())[-3:]
        if len(recent_months) >= 2:
            recent_trend = monthly_trends[recent_months[-1]]["average_score"]
            previous_trend = monthly_trends[recent_months[-2]]["average_score"]
            if recent_trend < previous_trend:
                recommendations.append("Tendance récente en baisse - Intervention nécessaire")
    
    return recommendations

def get_season(month: int) -> str:
    """Déterminer la saison basée sur le mois."""
    if month in [12, 1, 2]:
        return "Hiver"
    elif month in [3, 4, 5]:
        return "Printemps"
    elif month in [6, 7, 8]:
        return "Été"
    else:
        return "Automne"

def calculate_improvement_rate(week: str, weekly_data: Dict) -> float:
    """Calculer le taux d'amélioration pour une semaine."""
    weeks = sorted(weekly_data.keys())
    week_index = weeks.index(week)
    
    if week_index > 0:
        current_avg = sum(weekly_data[week]) / len(weekly_data[week])
        previous_avg = sum(weekly_data[weeks[week_index-1]]) / len(weekly_data[weeks[week_index-1]])
        return round(((current_avg - previous_avg) / previous_avg) * 100, 2) if previous_avg > 0 else 0
    return 0

def calculate_growth_rate(month: str, monthly_data: Dict) -> float:
    """Calculer le taux de croissance pour un mois."""
    months = sorted(monthly_data.keys())
    month_index = months.index(month)
    
    if month_index > 0:
        current_avg = sum(monthly_data[month]) / len(monthly_data[month])
        previous_avg = sum(monthly_data[months[month_index-1]]) / len(monthly_data[months[month_index-1]])
        return round(((current_avg - previous_avg) / previous_avg) * 100, 2) if previous_avg > 0 else 0
    return 0

def calculate_consistency_score(scores: List[float]) -> float:
    """Calculer un score de cohérence."""
    if len(scores) < 2:
        return 100.0
    
    mean_score = sum(scores) / len(scores)
    variance = sum((score - mean_score) ** 2 for score in scores) / len(scores)
    
    # Plus la variance est faible, plus la cohérence est élevée
    consistency = max(0, 100 - (variance / 10))
    return round(consistency, 2) 