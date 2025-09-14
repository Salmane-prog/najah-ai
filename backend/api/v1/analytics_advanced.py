from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from core.database import get_db
from models.user import User
from api.v1.users import require_role
from models.quiz import Quiz, QuizResult
from models.class_group import ClassGroup, ClassStudent
from models.badge import UserBadge
from models.learning_history import LearningHistory
import json
from datetime import datetime, timedelta
from typing import List, Dict, Any
import pandas as pd
from io import BytesIO
import base64

router = APIRouter()

@router.get("/interactive-charts/{user_id}")
def get_interactive_charts(
    user_id: int,
    chart_type: str = "performance",
    period: str = "month",
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['teacher', 'admin']))
):
    """Obtenir des graphiques interactifs pour une classe."""
    try:
        # Vérifier que la classe appartient au professeur
        class_group = db.query(ClassGroup).filter(
            ClassGroup.id == user_id,
            ClassGroup.teacher_id == current_user.id
        ).first()
        
        if not class_group:
            raise HTTPException(status_code=404, detail="Classe non trouvée")
        
        # Récupérer les étudiants de la classe
        students = db.query(ClassStudent).filter(ClassStudent.class_id == user_id).all()
        
        if chart_type == "performance":
            return get_performance_chart_data(students, db, period)
        elif chart_type == "progress":
            return get_progress_chart_data(students, db, period)
        elif chart_type == "engagement":
            return get_engagement_chart_data(students, db, period)
        else:
            raise HTTPException(status_code=400, detail="Type de graphique non supporté")
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur de graphique: {str(e)}")

def get_performance_chart_data(students: List, db: Session, period: str) -> Dict[str, Any]:
    """Données pour le graphique de performance."""
    chart_data = {
        "labels": [],
        "datasets": [
            {
                "label": "Score Moyen",
                "data": [],
                "backgroundColor": "rgba(59, 130, 246, 0.2)",
                "borderColor": "rgba(59, 130, 246, 1)",
                "borderWidth": 2
            },
            {
                "label": "Taux de Réussite",
                "data": [],
                "backgroundColor": "rgba(34, 197, 94, 0.2)",
                "borderColor": "rgba(34, 197, 94, 1)",
                "borderWidth": 2
            }
        ]
    }
    
    # Calculer les périodes
    end_date = datetime.utcnow()
    if period == "week":
        start_date = end_date - timedelta(days=7)
        interval = timedelta(days=1)
    elif period == "month":
        start_date = end_date - timedelta(days=30)
        interval = timedelta(days=7)
    else:  # year
        start_date = end_date - timedelta(days=365)
        interval = timedelta(days=30)
    
    current_date = start_date
    while current_date <= end_date:
        chart_data["labels"].append(current_date.strftime("%Y-%m-%d"))
        
        # Calculer les scores pour cette période
        period_start = current_date
        period_end = current_date + interval
        
        total_score = 0
        total_quizzes = 0
        successful_quizzes = 0
        
        for student_relation in students:
            student_results = db.query(QuizResult).filter(
                QuizResult.student_id == student_relation.student_id,
                QuizResult.created_at >= period_start,
                QuizResult.created_at < period_end
            ).all()
            
            for result in student_results:
                if result.score:
                    total_score += result.score
                    total_quizzes += 1
                    if result.score >= 60:
                        successful_quizzes += 1
        
        avg_score = total_score / total_quizzes if total_quizzes > 0 else 0
        success_rate = (successful_quizzes / total_quizzes * 100) if total_quizzes > 0 else 0
        
        chart_data["datasets"][0]["data"].append(round(avg_score, 1))
        chart_data["datasets"][1]["data"].append(round(success_rate, 1))
        
        current_date += interval
    
    return chart_data

def get_progress_chart_data(students: List, db: Session, period: str) -> Dict[str, Any]:
    """Données pour le graphique de progression."""
    chart_data = {
        "labels": [],
        "datasets": []
    }
    
    # Créer un dataset pour chaque étudiant
    colors = [
        "rgba(59, 130, 246, 1)", "rgba(34, 197, 94, 1)", "rgba(251, 191, 36, 1)",
        "rgba(239, 68, 68, 1)", "rgba(168, 85, 247, 1)", "rgba(236, 72, 153, 1)"
    ]
    
    for i, student_relation in enumerate(students):
        student = db.query(User).filter(User.id == student_relation.student_id).first()
        if not student:
            continue
        
        # Récupérer les résultats de l'étudiant
        results = db.query(QuizResult).filter(
            QuizResult.student_id == student.id
        ).order_by(QuizResult.created_at).all()
        
        if results:
            dataset = {
                "label": student.username,
                "data": [r.score for r in results if r.score],
                "borderColor": colors[i % len(colors)],
                "backgroundColor": colors[i % len(colors)].replace("1)", "0.1)"),
                "borderWidth": 2,
                "fill": False
            }
            chart_data["datasets"].append(dataset)
            
            # Ajouter les labels (dates)
            if not chart_data["labels"]:
                chart_data["labels"] = [r.created_at.strftime("%Y-%m-%d") for r in results if r.created_at]
    
    return chart_data

def get_engagement_chart_data(students: List, db: Session, period: str) -> Dict[str, Any]:
    """Données pour le graphique d'engagement."""
    chart_data = {
        "labels": ["Quiz", "Badges", "Activités", "Messages"],
        "datasets": [
            {
                "label": "Engagement",
                "data": [0, 0, 0, 0],
                "backgroundColor": [
                    "rgba(59, 130, 246, 0.8)",
                    "rgba(34, 197, 94, 0.8)",
                    "rgba(251, 191, 36, 0.8)",
                    "rgba(239, 68, 68, 0.8)"
                ]
            }
        ]
    }
    
    # Compter les activités pour tous les étudiants
    total_quizzes = 0
    total_badges = 0
    total_activities = 0
    total_messages = 0
    
    for student_relation in students:
        # Quiz
        quiz_count = db.query(QuizResult).filter(
            QuizResult.student_id == student_relation.student_id
        ).count()
        total_quizzes += quiz_count
        
        # Badges
        badge_count = db.query(UserBadge).filter(
            UserBadge.user_id == student_relation.student_id
        ).count()
        total_badges += badge_count
        
        # Activités d'apprentissage
        activity_count = db.query(LearningHistory).filter(
            LearningHistory.student_id == student_relation.student_id
        ).count()
        total_activities += activity_count
    
    chart_data["datasets"][0]["data"] = [total_quizzes, total_badges, total_activities, total_messages]
    
    return chart_data

@router.get("/export-pdf/{class_id}")
def export_analytics_pdf(
    class_id: int,
    report_type: str = "comprehensive",
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['teacher']))
):
    """Exporter un rapport PDF des analytics."""
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import inch
        from reportlab.lib import colors
        
        # Vérifier que la classe appartient au professeur
        class_group = db.query(ClassGroup).filter(
            ClassGroup.id == class_id,
            ClassGroup.teacher_id == current_user.id
        ).first()
        
        if not class_group:
            raise HTTPException(status_code=404, detail="Classe non trouvée")
        
        # Créer le PDF
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        styles = getSampleStyleSheet()
        story = []
        
        # Titre
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            alignment=1
        )
        story.append(Paragraph(f"Rapport Analytics - {class_group.name}", title_style))
        story.append(Spacer(1, 12))
        
        # Informations de la classe
        students = db.query(ClassStudent).filter(ClassStudent.class_id == class_id).all()
        story.append(Paragraph(f"Nombre d'étudiants: {len(students)}", styles['Normal']))
        story.append(Paragraph(f"Date du rapport: {datetime.utcnow().strftime('%Y-%m-%d')}", styles['Normal']))
        story.append(Spacer(1, 12))
        
        # Statistiques de performance
        story.append(Paragraph("Statistiques de Performance", styles['Heading2']))
        
        total_quizzes = 0
        total_score = 0
        successful_quizzes = 0
        
        for student_relation in students:
            results = db.query(QuizResult).filter(
                QuizResult.student_id == student_relation.student_id
            ).all()
            
            for result in results:
                if result.score:
                    total_score += result.score
                    total_quizzes += 1
                    if result.score >= 60:
                        successful_quizzes += 1
        
        avg_score = total_score / total_quizzes if total_quizzes > 0 else 0
        success_rate = (successful_quizzes / total_quizzes * 100) if total_quizzes > 0 else 0
        
        stats_data = [
            ['Métrique', 'Valeur'],
            ['Quiz total', str(total_quizzes)],
            ['Score moyen', f"{avg_score:.1f}"],
            ['Taux de réussite', f"{success_rate:.1f}%"],
            ['Étudiants', str(len(students))]
        ]
        
        stats_table = Table(stats_data)
        stats_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 14),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(stats_table)
        story.append(Spacer(1, 12))
        
        # Générer le PDF
        doc.build(story)
        buffer.seek(0)
        
        # Encoder en base64
        pdf_content = buffer.getvalue()
        pdf_base64 = base64.b64encode(pdf_content).decode()
        
        return {
            "pdf_base64": pdf_base64,
            "filename": f"rapport_analytics_{class_group.name}_{datetime.utcnow().strftime('%Y%m%d')}.pdf"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur d'export PDF: {str(e)}")

@router.get("/export-excel/{class_id}")
def export_analytics_excel(
    class_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['teacher']))
):
    """Exporter les analytics en Excel."""
    try:
        # Vérifier que la classe appartient au professeur
        class_group = db.query(ClassGroup).filter(
            ClassGroup.id == class_id,
            ClassGroup.teacher_id == current_user.id
        ).first()
        
        if not class_group:
            raise HTTPException(status_code=404, detail="Classe non trouvée")
        
        # Récupérer les données
        students = db.query(ClassStudent).filter(ClassStudent.class_id == class_id).all()
        
        # Créer un DataFrame avec les données des étudiants
        student_data = []
        
        for student_relation in students:
            student = db.query(User).filter(User.id == student_relation.student_id).first()
            if not student:
                continue
            
            # Récupérer les résultats de l'étudiant
            results = db.query(QuizResult).filter(
                QuizResult.student_id == student.id
            ).all()
            
            # Calculer les statistiques
            total_quizzes = len(results)
            completed_quizzes = len([r for r in results if r.is_completed])
            avg_score = sum(r.score for r in results if r.score) / len(results) if results else 0
            successful_quizzes = len([r for r in results if r.score and r.score >= 60])
            
            # Récupérer les badges
            badges = db.query(UserBadge).filter(UserBadge.user_id == student.id).all()
            
            student_data.append({
                'ID': student.id,
                'Nom': student.username,
                'Email': student.email,
                'Quiz Total': total_quizzes,
                'Quiz Complétés': completed_quizzes,
                'Score Moyen': round(avg_score, 2),
                'Quiz Réussis': successful_quizzes,
                'Taux de Réussite': round((successful_quizzes / total_quizzes * 100) if total_quizzes > 0 else 0, 1),
                'Badges': len(badges),
                'Dernière Activité': max([r.created_at for r in results if r.created_at]).strftime('%Y-%m-%d') if results else 'N/A'
            })
        
        # Créer le DataFrame
        df = pd.DataFrame(student_data)
        
        # Créer le fichier Excel
        buffer = BytesIO()
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Analytics', index=False)
            
            # Ajouter un graphique
            workbook = writer.book
            worksheet = writer.sheets['Analytics']
            
            # Créer un graphique de performance
            from openpyxl.chart import BarChart, Reference
            
            chart = BarChart()
            chart.title = "Performance des Étudiants"
            chart.x_axis.title = "Étudiants"
            chart.y_axis.title = "Score Moyen"
            
            data = Reference(worksheet, min_col=6, min_row=1, max_row=len(student_data)+1)
            cats = Reference(worksheet, min_col=2, min_row=2, max_row=len(student_data)+1)
            chart.add_data(data, titles_from_data=True)
            chart.set_categories(cats)
            
            worksheet.add_chart(chart, "J2")
        
        buffer.seek(0)
        excel_content = buffer.getvalue()
        excel_base64 = base64.b64encode(excel_content).decode()
        
        return {
            "excel_base64": excel_base64,
            "filename": f"analytics_{class_group.name}_{datetime.utcnow().strftime('%Y%m%d')}.xlsx"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur d'export Excel: {str(e)}")

@router.get("/custom-reports")
def get_custom_reports(
    report_type: str = "performance",
    filters: Dict[str, Any] = {},
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['teacher']))
):
    """Générer des rapports personnalisés."""
    try:
        if report_type == "performance":
            return generate_performance_report(current_user.id, filters, db)
        elif report_type == "engagement":
            return generate_engagement_report(current_user.id, filters, db)
        elif report_type == "progress":
            return generate_progress_report(current_user.id, filters, db)
        else:
            raise HTTPException(status_code=400, detail="Type de rapport non supporté")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur de rapport: {str(e)}")

def generate_performance_report(teacher_id: int, filters: Dict[str, Any], db: Session) -> Dict[str, Any]:
    """Générer un rapport de performance."""
    # Récupérer les classes du professeur
    classes = db.query(ClassGroup).filter(ClassGroup.teacher_id == teacher_id).all()
    
    report_data = {
        "teacher_id": teacher_id,
        "report_type": "performance",
        "generated_at": datetime.utcnow().isoformat(),
        "classes": []
    }
    
    for class_group in classes:
        students = db.query(ClassStudent).filter(ClassStudent.class_id == class_group.id).all()
        
        class_stats = {
            "class_id": class_group.id,
            "class_name": class_group.name,
            "student_count": len(students),
            "performance_metrics": {
                "average_score": 0,
                "completion_rate": 0,
                "success_rate": 0
            }
        }
        
        total_score = 0
        total_quizzes = 0
        successful_quizzes = 0
        completed_quizzes = 0
        
        for student_relation in students:
            results = db.query(QuizResult).filter(
                QuizResult.student_id == student_relation.student_id
            ).all()
            
            for result in results:
                if result.score:
                    total_score += result.score
                    total_quizzes += 1
                    if result.score >= 60:
                        successful_quizzes += 1
                if result.is_completed:
                    completed_quizzes += 1
        
        if total_quizzes > 0:
            class_stats["performance_metrics"]["average_score"] = round(total_score / total_quizzes, 2)
            class_stats["performance_metrics"]["success_rate"] = round((successful_quizzes / total_quizzes * 100), 1)
        
        if total_quizzes > 0:
            class_stats["performance_metrics"]["completion_rate"] = round((completed_quizzes / total_quizzes * 100), 1)
        
        report_data["classes"].append(class_stats)
    
    return report_data 