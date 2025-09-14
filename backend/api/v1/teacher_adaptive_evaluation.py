from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import json

from core.database import get_db
from models.user import User
from models.adaptive_evaluation import (
    AdaptiveTest, AdaptiveQuestion, TestAssignment,
    TestAttempt, QuestionResponse, CompetencyAnalysis, Class, AdaptiveClassStudent
)
from core.security import get_current_user, require_role
from sqlalchemy import and_, func, desc, text

router = APIRouter(tags=["Évaluation Adaptative - Enseignants"])

# ============================================================================
# ENDPOINTS POUR LES ENSEIGNANTS - GESTION COMPLÈTE
# ============================================================================

@router.post("/tests/create")
async def create_adaptive_test(
    test_data: Dict[str, Any],
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Créer un nouveau test adaptatif avec questions"""
    try:
        # Créer le test adaptatif
        new_test = AdaptiveTest(
            title=test_data["title"],
            subject=test_data["subject"],
            description=test_data.get("description", ""),
            difficulty_range_min=test_data.get("difficulty_range", {}).get("min", 1),
            difficulty_range_max=test_data.get("difficulty_range", {}).get("max", 10),
            estimated_duration=test_data.get("estimated_duration", 30),
            is_active=test_data.get("is_active", True)
        )
        
        db.add(new_test)
        db.commit()
        db.refresh(new_test)
        
        # Créer les questions si fournies
        questions_created = 0
        if "questions" in test_data and test_data["questions"]:
            for question_data in test_data["questions"]:
                question = AdaptiveQuestion(
                    test_id=new_test.id,
                    question_text=question_data["question_text"],
                    question_type=question_data["question_type"],
                    options=question_data.get("options", {}),
                    correct_answer=question_data["correct_answer"],
                    explanation=question_data.get("explanation", ""),
                    difficulty_level=question_data["difficulty_level"],
                    subject=question_data.get("subject", test_data["subject"]),
                    topic=question_data.get("topic", ""),
                    tags=question_data.get("tags", [])
                )
                db.add(question)
                questions_created += 1
            
            db.commit()
        
        return {
            "success": True,
            "message": f"Test adaptatif créé avec succès avec {questions_created} questions",
            "test": {
                "id": new_test.id,
                "title": new_test.title,
                "subject": new_test.subject,
                "description": new_test.description,
                "difficulty_range": {"min": new_test.difficulty_range_min, "max": new_test.difficulty_range_max},
                "estimated_duration": new_test.estimated_duration,
                "is_active": new_test.is_active,
                "created_at": new_test.created_at,
                "questions_count": questions_created
            }
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erreur lors de la création du test: {str(e)}")

@router.post("/tests/{test_id}/assign")
async def assign_test_to_targets(
    test_id: int,
    assignment_data: Dict[str, Any],
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Assigner un test adaptatif à des classes ou étudiants"""
    try:
        # Vérifier que le test existe et appartient à l'enseignant
        test = db.query(AdaptiveTest).filter(AdaptiveTest.id == test_id).first()
        if not test:
            raise HTTPException(status_code=404, detail="Test non trouvé")
        
        if test.created_by != current_user.id and current_user.role != "admin":
            raise HTTPException(status_code=403, detail="Vous n'êtes pas autorisé à assigner ce test")
        
        assignments_created = []
        
        # Assigner aux classes
        if "class_ids" in assignment_data and assignment_data["class_ids"]:
            for class_id in assignment_data["class_ids"]:
                # Vérifier que la classe appartient à l'enseignant
                class_query = db.execute(text("""
                    SELECT id, name FROM class_groups 
                    WHERE id = :class_id AND teacher_id = :teacher_id
                """), {"class_id": class_id, "teacher_id": current_user.id})
                
                class_group = class_query.fetchone()
                if not class_group:
                    continue
                
                # Créer l'assignation
                db.execute(text("""
                    INSERT INTO test_assignments (test_id, assignment_type, target_id, assigned_by, due_date)
                    VALUES (:test_id, 'class', :target_id, :assigned_by, :due_date)
                """), {
                    "test_id": test_id,
                    "target_id": class_id,
                    "assigned_by": current_user.id,
                    "due_date": assignment_data.get("due_date")
                })
                
                assignments_created.append({
                    "type": "class",
                    "target_id": class_id,
                    "target_name": class_group.name
                })
        
        # Assigner aux étudiants individuels
        if "student_ids" in assignment_data and assignment_data["student_ids"]:
            for student_id in assignment_data["student_ids"]:
                # Vérifier que l'étudiant appartient à une classe de l'enseignant
                student_query = db.execute(text("""
                    SELECT cs.student_id, u.first_name, u.last_name
                    FROM class_students cs
                    JOIN class_groups cg ON cs.class_id = cg.id
                    JOIN users u ON cs.student_id = u.id
                    WHERE cs.student_id = :student_id AND cg.teacher_id = :teacher_id
                """), {"student_id": student_id, "teacher_id": current_user.id})
                
                student = student_query.fetchone()
                if not student:
                    continue
                
                # Créer l'assignation
                db.execute(text("""
                    INSERT INTO test_assignments (test_id, assignment_type, target_id, assigned_by, due_date)
                    VALUES (:test_id, 'individual', :target_id, :assigned_by, :due_date)
                """), {
                    "test_id": test_id,
                    "target_id": student_id,
                    "assigned_by": current_user.id,
                    "due_date": assignment_data.get("due_date")
                })
                
                assignments_created.append({
                    "type": "individual",
                    "target_id": student_id,
                    "student_name": f"{student.first_name or ''} {student.last_name or ''}".strip()
                })
        
        db.commit()
        
        return {
            "success": True,
            "message": f"Test assigné à {len(assignments_created)} cibles",
            "assignments": assignments_created
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erreur lors de l'assignation: {str(e)}")

@router.get("/tests/teacher/{teacher_id}")
async def get_teacher_tests(
    teacher_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Récupérer tous les tests adaptatifs d'un enseignant avec statistiques"""
    try:
        print(f"🔍 DEBUG: Début de get_teacher_tests pour teacher_id={teacher_id}")
        print(f"🔍 DEBUG: current_user.id={current_user.id}, role={current_user.role}")
        
        # Vérifier les permissions
        if current_user.id != teacher_id and current_user.role != "admin":
            raise HTTPException(status_code=403, detail="Accès non autorisé")
        
        print(f"🔍 DEBUG: Permissions vérifiées, récupération des tests...")
        
        # Récupérer les tests créés par l'enseignant
        print("🔍 DEBUG: Exécution de la requête SQL...")
        try:
            tests = db.query(AdaptiveTest).filter(
                AdaptiveTest.created_by == teacher_id
            ).all()
            print(f"🔍 DEBUG: {len(tests)} tests trouvés")
        except Exception as e:
            print(f"❌ DEBUG: Erreur lors de la requête SQL: {e}")
            raise HTTPException(status_code=500, detail=f"Erreur lors de la récupération des tests: {str(e)}")
        
        if not tests:
            print("🔍 DEBUG: Aucun test trouvé, retour de la liste vide")
            return {
                "success": True,
                "tests": [],
                "total_tests": 0
            }
        
        print("🔍 DEBUG: Début du traitement des statistiques...")
        
        # Récupérer les statistiques pour chaque test
        tests_with_stats = []
        print(f"🔍 DEBUG: Début de la boucle de traitement de {len(tests)} tests")
        
        for i, test in enumerate(tests):
            print(f"🔍 DEBUG: Traitement du test {i+1}/{len(tests)}: ID={test.id}, Titre={test.title}")
            
            # Statistiques d'assignation
            try:
                assignment_stats = db.execute(text("""
                    SELECT 
                        COUNT(DISTINCT ta.target_id) as total_assignments,
                        COUNT(DISTINCT CASE WHEN ta.assignment_type = 'class' THEN ta.target_id END) as class_assignments,
                        COUNT(DISTINCT CASE WHEN ta.assignment_type = 'individual' THEN ta.target_id END) as individual_assignments
                    FROM adaptive_test_assignments ta
                    WHERE ta.test_id = :test_id AND ta.is_active = 1
                """), {"test_id": test.id}).fetchone()
                print(f"🔍 DEBUG: Statistiques d'assignation récupérées pour test {test.id}")
            except Exception as e:
                print(f"❌ DEBUG: Erreur lors de la récupération des stats d'assignation: {e}")
                assignment_stats = None
            
            # Statistiques de performance
            try:
                performance_stats = db.execute(text("""
                    SELECT 
                        COUNT(*) as total_students,
                        COUNT(CASE WHEN status = 'completed' THEN 1 END) as completed_students,
                        COUNT(CASE WHEN status = 'in_progress' THEN 1 END) as in_progress_students,
                        AVG(final_score) as average_score
                    FROM adaptive_test_responses
                    WHERE test_id = :test_id
                """), {"test_id": test.id}).fetchone()
                print(f"🔍 DEBUG: Statistiques de performance récupérées pour test {test.id}")
            except Exception as e:
                print(f"❌ DEBUG: Erreur lors de la récupération des stats de performance: {e}")
                performance_stats = None
            
            tests_with_stats.append({
                "id": test.id,
                "title": test.title,
                "subject": test.subject,
                "description": test.description,
                "difficulty_range": {"min": test.difficulty_range_min, "max": test.difficulty_range_max},
                "estimated_duration": test.estimated_duration,
                "is_active": test.is_active,
                "created_at": test.created_at,
                "statistics": {
                    "assignments": {
                        "total": getattr(assignment_stats, 'total_assignments', 0) if assignment_stats else 0,
                        "classes": getattr(assignment_stats, 'class_assignments', 0) if assignment_stats else 0,
                        "individuals": getattr(assignment_stats, 'individual_assignments', 0) if assignment_stats else 0
                    },
                    "performance": {
                        "total_students": getattr(performance_stats, 'total_students', 0) if performance_stats else 0,
                        "completed_students": getattr(performance_stats, 'completed_students', 0) if performance_stats else 0,
                        "in_progress_students": getattr(performance_stats, 'in_progress_students', 0) if performance_stats else 0,
                        "average_score": round(getattr(performance_stats, 'average_score', 0) or 0, 2) if performance_stats else 0
                    }
                }
            })
        
        return {
            "success": True,
            "tests": tests_with_stats,
            "total_tests": len(tests_with_stats)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la récupération des tests: {str(e)}")

@router.get("/tests/{test_id}/results")
async def get_test_results(
    test_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Récupérer les résultats détaillés d'un test adaptatif"""
    try:
        # Vérifier que le test existe et que l'enseignant y a accès
        test = db.query(AdaptiveTest).filter(AdaptiveTest.id == test_id).first()
        if not test:
            raise HTTPException(status_code=404, detail="Test non trouvé")
        
        if test.created_by != current_user.id and current_user.role != "admin":
            raise HTTPException(status_code=403, detail="Accès non autorisé")
        
        # Récupérer les performances des étudiants
        performances = db.execute(text("""
            SELECT 
                atp.*,
                u.first_name,
                u.last_name,
                u.email,
                cg.name as class_name
            FROM adaptive_test_performance atp
            JOIN users u ON atp.student_id = u.id
            LEFT JOIN class_groups cg ON atp.class_id = cg.id
            WHERE atp.test_id = :test_id
            ORDER BY atp.final_score DESC
        """), {"test_id": test_id}).fetchall()
        
        # Statistiques globales
        stats = db.execute(text("""
            SELECT 
                COUNT(*) as total_students,
                COUNT(CASE WHEN status = 'completed' THEN 1 END) as completed_students,
                COUNT(CASE WHEN status = 'in_progress' THEN 1 END) as in_progress_students,
                COUNT(CASE WHEN status = 'not_started' THEN 1 END) as not_started_students,
                AVG(final_score) as average_score,
                AVG(average_response_time) as avg_response_time,
                AVG(difficulty_adjustments) as avg_difficulty_adjustments
            FROM adaptive_test_performance
            WHERE test_id = :test_id
        """), {"test_id": test_id}).fetchone()
        
        # Analyse des questions
        question_analysis = db.execute(text("""
            SELECT 
                aq.question_text,
                aq.difficulty_level,
                COUNT(sa.id) as times_answered,
                AVG(CASE WHEN sa.is_correct THEN 1.0 ELSE 0.0 END) as success_rate,
                AVG(sa.response_time) as avg_response_time
            FROM adaptive_questions aq
            LEFT JOIN student_answers sa ON aq.id = sa.question_id
            LEFT JOIN student_adaptive_tests sat ON sa.student_test_id = sat.id
            WHERE sat.test_id = :test_id
            GROUP BY aq.id, aq.question_text, aq.difficulty_level
            ORDER BY aq.difficulty_level
        """), {"test_id": test_id}).fetchall()
        
        return {
            "success": True,
            "test": {
                "id": test.id,
                "title": test.title,
                "subject": test.subject
            },
            "statistics": {
                "total_students": stats.total_students or 0,
                "completed_students": stats.completed_students or 0,
                "in_progress_students": stats.in_progress_students or 0,
                "not_started_students": stats.not_started_students or 0,
                "average_score": round(stats.average_score or 0, 2),
                "avg_response_time": round(stats.avg_response_time or 0, 2),
                "avg_difficulty_adjustments": round(stats.avg_difficulty_adjustments or 0, 2)
            },
            "student_performances": [
                {
                    "student_id": p.student_id,
                    "student_name": f"{p.first_name or ''} {p.last_name or ''}".strip() or p.email,
                    "email": p.email,
                    "class_name": p.class_name,
                    "status": p.status,
                    "final_score": p.final_score,
                    "questions_answered": p.questions_answered,
                    "correct_answers": p.correct_answers,
                    "completion_time": p.completion_time,
                    "difficulty_adjustments": p.difficulty_adjustments,
                    "start_time": p.start_time
                }
                for p in performances
            ],
            "question_analysis": [
                {
                    "question_text": q.question_text,
                    "difficulty_level": q.difficulty_level,
                    "times_answered": q.times_answered,
                    "success_rate": round(q.success_rate * 100, 2) if q.success_rate else 0,
                    "avg_response_time": round(q.avg_response_time or 0, 2)
                }
                for q in question_analysis
            ]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la récupération des résultats: {str(e)}")

@router.get("/analytics/class/{class_id}")
async def get_class_analytics(
    class_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Récupérer les analytics d'une classe pour l'évaluation adaptative"""
    try:
        # Vérifier que la classe appartient à l'enseignant
        class_query = db.execute(text("""
            SELECT id, name FROM class_groups 
            WHERE id = :class_id AND teacher_id = :teacher_id
        """), {"class_id": class_id, "teacher_id": current_user.id})
        
        class_group = class_query.fetchone()
        if not class_group:
            raise HTTPException(status_code=404, detail="Classe non trouvée ou accès non autorisé")
        
        # Statistiques globales de la classe
        class_stats = db.execute(text("""
            SELECT 
                COUNT(DISTINCT atp.student_id) as total_students,
                COUNT(DISTINCT atp.test_id) as total_tests,
                AVG(atp.final_score) as class_average_score,
                AVG(atp.average_response_time) as avg_response_time,
                SUM(atp.difficulty_adjustments) as total_difficulty_adjustments
            FROM adaptive_test_performance atp
            JOIN class_students cs ON atp.student_id = cs.student_id
            WHERE cs.class_id = :class_id AND atp.status = 'completed'
        """), {"class_id": class_id}).fetchone()
        
        # Performance par matière
        subject_performance = db.execute(text("""
            SELECT 
                at.subject,
                COUNT(DISTINCT atp.student_id) as students_count,
                AVG(atp.final_score) as average_score,
                COUNT(DISTINCT atp.test_id) as tests_count
            FROM adaptive_test_performance atp
            JOIN adaptive_tests at ON atp.test_id = at.id
            JOIN class_students cs ON atp.student_id = cs.student_id
            WHERE cs.class_id = :class_id AND atp.status = 'completed'
            GROUP BY at.subject
            ORDER BY average_score DESC
        """), {"class_id": class_id}).fetchall()
        
        # Progression des étudiants
        student_progress = db.execute(text("""
            SELECT 
                u.first_name,
                u.last_name,
                u.email,
                COUNT(DISTINCT atp.test_id) as tests_completed,
                AVG(atp.final_score) as average_score,
                AVG(atp.average_response_time) as avg_response_time,
                SUM(atp.difficulty_adjustments) as total_adjustments,
                MAX(atp.completion_time) as last_activity
            FROM adaptive_test_performance atp
            JOIN users u ON atp.student_id = u.id
            JOIN class_students cs ON atp.student_id = cs.student_id
            WHERE cs.class_id = :class_id AND atp.status = 'completed'
            GROUP BY u.id, u.first_name, u.last_name, u.email
            ORDER BY average_score DESC
        """), {"class_id": class_id}).fetchall()
        
        return {
            "success": True,
            "class": {
                "id": class_group.id,
                "name": class_group.name
            },
            "statistics": {
                "total_students": class_stats.total_students or 0,
                "total_tests": class_stats.total_tests or 0,
                "class_average_score": round(class_stats.class_average_score or 0, 2),
                "avg_response_time": round(class_stats.avg_response_time or 0, 2),
                "total_difficulty_adjustments": class_stats.total_difficulty_adjustments or 0
            },
            "subject_performance": [
                {
                    "subject": sp.subject,
                    "students_count": sp.students_count,
                    "average_score": round(sp.average_score or 0, 2),
                    "tests_count": sp.tests_count
                }
                for sp in subject_performance
            ],
            "student_progress": [
                {
                    "student_name": f"{sp.first_name or ''} {sp.last_name or ''}".strip() or sp.email,
                    "email": sp.email,
                    "tests_completed": sp.tests_completed,
                    "average_score": round(sp.average_score or 0, 2),
                    "avg_response_time": round(sp.avg_response_time or 0, 2),
                    "total_adjustments": sp.total_adjustments,
                    "last_activity": sp.last_activity
                }
                for sp in student_progress
            ]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la récupération des analytics: {str(e)}")

@router.get("/dashboard/overview")
async def get_teacher_dashboard_overview(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Vue d'ensemble du dashboard enseignant pour l'évaluation adaptative"""
    try:
        # Statistiques globales
        overview_stats = db.execute(text("""
            SELECT 
                COUNT(DISTINCT at.id) as total_tests,
                COUNT(DISTINCT ta.id) as total_assignments,
                COUNT(DISTINCT atp.student_id) as total_students,
                AVG(atp.final_score) as overall_average_score
            FROM adaptive_tests at
            LEFT JOIN test_assignments ta ON at.id = ta.test_id
            LEFT JOIN adaptive_test_performance atp ON at.id = atp.test_id
            WHERE at.created_by = :teacher_id
        """), {"teacher_id": current_user.id}).fetchone()
        
        # Tests récents
        recent_tests = db.execute(text("""
            SELECT 
                at.id,
                at.title,
                at.subject,
                at.created_at,
                COUNT(DISTINCT ta.id) as assignments_count,
                COUNT(DISTINCT atp.student_id) as students_count
            FROM adaptive_tests at
            LEFT JOIN test_assignments ta ON at.id = ta.test_id
            LEFT JOIN adaptive_test_performance atp ON at.id = atp.test_id
            WHERE at.created_by = :teacher_id
            GROUP BY at.id, at.title, at.subject, at.created_at
            ORDER BY at.created_at DESC
            LIMIT 5
        """), {"teacher_id": current_user.id}).fetchall()
        
        # Performance par matière
        subject_performance = db.execute(text("""
            SELECT 
                at.subject,
                COUNT(DISTINCT at.id) as tests_count,
                COUNT(DISTINCT atp.student_id) as students_count,
                AVG(atp.final_score) as average_score
            FROM adaptive_tests at
            LEFT JOIN adaptive_test_performance atp ON at.id = atp.test_id
            WHERE at.created_by = :teacher_id AND atp.status = 'completed'
            GROUP BY at.subject
            ORDER BY average_score DESC
        """), {"teacher_id": current_user.id}).fetchall()
        
        return {
            "success": True,
            "overview": {
                "total_tests": overview_stats.total_tests or 0,
                "total_assignments": overview_stats.total_assignments or 0,
                "total_students": overview_stats.total_students or 0,
                "overall_average_score": round(overview_stats.overall_average_score or 0, 2)
            },
            "recent_tests": [
                {
                    "id": rt.id,
                    "title": rt.title,
                    "subject": rt.subject,
                    "created_at": rt.created_at,
                    "assignments_count": rt.assignments_count,
                    "students_count": rt.students_count
                }
                for rt in recent_tests
            ],
            "subject_performance": [
                {
                    "subject": sp.subject,
                    "tests_count": sp.tests_count,
                    "students_count": sp.students_count,
                    "average_score": round(sp.average_score or 0, 2)
                }
                for sp in subject_performance
            ]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la récupération du dashboard: {str(e)}")
