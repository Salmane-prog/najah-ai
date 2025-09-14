from fastapi import APIRouter, Depends, HTTPException, Query, Response
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta
import json
import csv
import io
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
import pandas as pd

from core.database import get_db
from api.v1.users import get_current_user
from api.v1.auth import require_role
from models.user import User
from models.quiz import Quiz, QuizResult
from models.class_group import ClassGroup, ClassStudent
from models.learning_history import LearningHistory
from models.continuous_assessment import StudentCompetency, ProgressReport

router = APIRouter()

# === EXPORT PDF ===

@router.get("/export/student/{student_id}/progress-pdf")
def export_student_progress_pdf(
    student_id: int,
    period: str = Query("monthly", description="Période: weekly, monthly, semester"),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['teacher', 'admin']))
):
    """Exporter le rapport de progression d'un étudiant en PDF."""
    try:
        # Récupérer les données de l'étudiant
        student = db.query(User).filter(User.id == student_id).first()
        if not student:
            raise HTTPException(status_code=404, detail="Étudiant non trouvé")
        
        # Créer le PDF
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        styles = getSampleStyleSheet()
        story = []
        
        # Titre
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=16,
            spaceAfter=30,
            alignment=1  # Centré
        )
        story.append(Paragraph(f"Rapport de Progression - {student.username}", title_style))
        story.append(Spacer(1, 20))
        
        # Informations de l'étudiant
        story.append(Paragraph("Informations de l'étudiant", styles['Heading2']))
        student_info = [
            ["Nom:", student.username],
            ["Email:", student.email],
            ["Période:", period],
            ["Date de génération:", datetime.now().strftime("%d/%m/%Y %H:%M")]
        ]
        
        student_table = Table(student_info, colWidths=[2*inch, 4*inch])
        student_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.grey),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('BACKGROUND', (1, 0), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(student_table)
        story.append(Spacer(1, 20))
        
        # Résultats des quiz
        story.append(Paragraph("Résultats des Quiz", styles['Heading2']))
        quiz_results = db.query(QuizResult).filter(QuizResult.student_id == student_id).all()
        
        if quiz_results:
            quiz_data = [["Quiz", "Matière", "Score", "Date"]]
            for result in quiz_results:
                quiz_data.append([
                    result.quiz.title if result.quiz else "Quiz inconnu",
                    result.sujet or "N/A",
                    f"{result.score}/{result.max_score}",
                    result.created_at.strftime("%d/%m/%Y")
                ])
            
            quiz_table = Table(quiz_data, colWidths=[2*inch, 1.5*inch, 1*inch, 1.5*inch])
            quiz_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            story.append(quiz_table)
        else:
            story.append(Paragraph("Aucun résultat de quiz disponible.", styles['Normal']))
        
        story.append(Spacer(1, 20))
        
        # Compétences
        story.append(Paragraph("Compétences", styles['Heading2']))
        competencies = db.query(StudentCompetency).filter(StudentCompetency.student_id == student_id).all()
        
        if competencies:
            comp_data = [["Compétence", "Niveau", "Progression", "Dernière évaluation"]]
            for comp in competencies:
                comp_data.append([
                    comp.competency.name,
                    comp.level_achieved,
                    f"{comp.progress_percentage}%",
                    comp.last_assessed.strftime("%d/%m/%Y") if comp.last_assessed else "N/A"
                ])
            
            comp_table = Table(comp_data, colWidths=[2.5*inch, 1*inch, 1*inch, 1.5*inch])
            comp_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            story.append(comp_table)
        else:
            story.append(Paragraph("Aucune compétence évaluée.", styles['Normal']))
        
        # Générer le PDF
        doc.build(story)
        buffer.seek(0)
        
        return Response(
            content=buffer.getvalue(),
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename=rapport_progression_{student.username}_{period}.pdf"}
        )
        
    except Exception as e:
        print(f"Erreur dans export_student_progress_pdf: {str(e)}")
        raise HTTPException(status_code=500, detail="Erreur lors de la génération du PDF")

@router.get("/export/class/{class_id}/performance-pdf")
def export_class_performance_pdf(
    class_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['teacher', 'admin']))
):
    """Exporter le rapport de performance d'une classe en PDF."""
    try:
        # Récupérer les données de la classe
        class_group = db.query(ClassGroup).filter(ClassGroup.id == class_id).first()
        if not class_group:
            raise HTTPException(status_code=404, detail="Classe non trouvée")
        
        # Créer le PDF
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        styles = getSampleStyleSheet()
        story = []
        
        # Titre
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=16,
            spaceAfter=30,
            alignment=1
        )
        story.append(Paragraph(f"Rapport de Performance - {class_group.name}", title_style))
        story.append(Spacer(1, 20))
        
        # Informations de la classe
        story.append(Paragraph("Informations de la classe", styles['Heading2']))
        class_info = [
            ["Nom de la classe:", class_group.name],
            ["Matière:", class_group.subject],
            ["Nombre d'étudiants:", str(len(class_group.students))],
            ["Date de génération:", datetime.now().strftime("%d/%m/%Y %H:%M")]
        ]
        
        class_table = Table(class_info, colWidths=[2*inch, 4*inch])
        class_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.grey),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('BACKGROUND', (1, 0), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(class_table)
        story.append(Spacer(1, 20))
        
        # Performance des étudiants
        story.append(Paragraph("Performance des étudiants", styles['Heading2']))
        
        students_data = [["Étudiant", "Quiz complétés", "Score moyen", "Progression"]]
        
        for student in class_group.students:
            # Calculer les statistiques de l'étudiant
            quiz_results = db.query(QuizResult).filter(QuizResult.student_id == student.id).all()
            completed_quizzes = len(quiz_results)
            
            if completed_quizzes > 0:
                avg_score = sum(result.score for result in quiz_results) / completed_quizzes
                avg_percentage = (avg_score / sum(result.max_score for result in quiz_results)) * 100
            else:
                avg_score = 0
                avg_percentage = 0
            
            students_data.append([
                student.username,
                str(completed_quizzes),
                f"{avg_score:.1f}",
                f"{avg_percentage:.1f}%"
            ])
        
        students_table = Table(students_data, colWidths=[2*inch, 1.5*inch, 1.5*inch, 1*inch])
        students_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(students_table)
        
        # Générer le PDF
        doc.build(story)
        buffer.seek(0)
        
        return Response(
            content=buffer.getvalue(),
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename=rapport_performance_{class_group.name}.pdf"}
        )
        
    except Exception as e:
        print(f"Erreur dans export_class_performance_pdf: {str(e)}")
        raise HTTPException(status_code=500, detail="Erreur lors de la génération du PDF")

# === EXPORT EXCEL ===

@router.get("/export/student/{student_id}/data-excel")
def export_student_data_excel(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['teacher', 'admin']))
):
    """Exporter toutes les données d'un étudiant en Excel."""
    try:
        # Récupérer les données de l'étudiant
        student = db.query(User).filter(User.id == student_id).first()
        if not student:
            raise HTTPException(status_code=404, detail="Étudiant non trouvé")
        
        # Créer un buffer pour le fichier Excel
        buffer = io.BytesIO()
        
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            # Données des quiz
            quiz_results = db.query(QuizResult).filter(QuizResult.student_id == student_id).all()
            quiz_data = []
            for result in quiz_results:
                quiz_data.append({
                    'Quiz': result.quiz.title if result.quiz else "Quiz inconnu",
                    'Matière': result.sujet or "N/A",
                    'Score': result.score,
                    'Score max': result.max_score,
                    'Pourcentage': (result.score / result.max_score) * 100 if result.max_score > 0 else 0,
                    'Date': result.created_at.strftime("%d/%m/%Y %H:%M")
                })
            
            if quiz_data:
                df_quiz = pd.DataFrame(quiz_data)
                df_quiz.to_excel(writer, sheet_name='Résultats Quiz', index=False)
            
            # Données des compétences
            competencies = db.query(StudentCompetency).filter(StudentCompetency.student_id == student_id).all()
            comp_data = []
            for comp in competencies:
                comp_data.append({
                    'Compétence': comp.competency.name,
                    'Matière': comp.competency.subject,
                    'Niveau': comp.level_achieved,
                    'Progression (%)': comp.progress_percentage,
                    'Dernière évaluation': comp.last_assessed.strftime("%d/%m/%Y") if comp.last_assessed else "N/A"
                })
            
            if comp_data:
                df_comp = pd.DataFrame(comp_data)
                df_comp.to_excel(writer, sheet_name='Compétences', index=False)
            
            # Données d'activité
            activities = db.query(LearningHistory).filter(LearningHistory.user_id == student_id).all()
            activity_data = []
            for activity in activities:
                activity_data.append({
                    'Type': activity.activity_type,
                    'Description': activity.description,
                    'Points': activity.points_earned,
                    'Date': activity.created_at.strftime("%d/%m/%Y %H:%M")
                })
            
            if activity_data:
                df_activity = pd.DataFrame(activity_data)
                df_activity.to_excel(writer, sheet_name='Activités', index=False)
        
        buffer.seek(0)
        
        return Response(
            content=buffer.getvalue(),
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": f"attachment; filename=donnees_etudiant_{student.username}.xlsx"}
        )
        
    except Exception as e:
        print(f"Erreur dans export_student_data_excel: {str(e)}")
        raise HTTPException(status_code=500, detail="Erreur lors de la génération du fichier Excel")

@router.get("/export/class/{class_id}/data-excel")
def export_class_data_excel(
    class_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['teacher', 'admin']))
):
    """Exporter toutes les données d'une classe en Excel."""
    try:
        # Récupérer les données de la classe
        class_group = db.query(ClassGroup).filter(ClassGroup.id == class_id).first()
        if not class_group:
            raise HTTPException(status_code=404, detail="Classe non trouvée")
        
        # Créer un buffer pour le fichier Excel
        buffer = io.BytesIO()
        
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            # Liste des étudiants
            students_data = []
            for student in class_group.students:
                students_data.append({
                    'ID': student.id,
                    'Nom': student.username,
                    'Email': student.email,
                    'Date d\'inscription': student.created_at.strftime("%d/%m/%Y") if student.created_at else "N/A"
                })
            
            if students_data:
                df_students = pd.DataFrame(students_data)
                df_students.to_excel(writer, sheet_name='Étudiants', index=False)
            
            # Résultats des quiz par étudiant
            quiz_results_data = []
            for student in class_group.students:
                quiz_results = db.query(QuizResult).filter(QuizResult.student_id == student.id).all()
                for result in quiz_results:
                    quiz_results_data.append({
                        'Étudiant': student.username,
                        'Quiz': result.quiz.title if result.quiz else "Quiz inconnu",
                        'Matière': result.sujet or "N/A",
                        'Score': result.score,
                        'Score max': result.max_score,
                        'Pourcentage': (result.score / result.max_score) * 100 if result.max_score > 0 else 0,
                        'Date': result.created_at.strftime("%d/%m/%Y %H:%M")
                    })
            
            if quiz_results_data:
                df_quiz_results = pd.DataFrame(quiz_results_data)
                df_quiz_results.to_excel(writer, sheet_name='Résultats Quiz', index=False)
            
            # Compétences par étudiant
            competencies_data = []
            for student in class_group.students:
                competencies = db.query(StudentCompetency).filter(StudentCompetency.student_id == student.id).all()
                for comp in competencies:
                    competencies_data.append({
                        'Étudiant': student.username,
                        'Compétence': comp.competency.name,
                        'Matière': comp.competency.subject,
                        'Niveau': comp.level_achieved,
                        'Progression (%)': comp.progress_percentage,
                        'Dernière évaluation': comp.last_assessed.strftime("%d/%m/%Y") if comp.last_assessed else "N/A"
                    })
            
            if competencies_data:
                df_competencies = pd.DataFrame(competencies_data)
                df_competencies.to_excel(writer, sheet_name='Compétences', index=False)
        
        buffer.seek(0)
        
        return Response(
            content=buffer.getvalue(),
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": f"attachment; filename=donnees_classe_{class_group.name}.xlsx"}
        )
        
    except Exception as e:
        print(f"Erreur dans export_class_data_excel: {str(e)}")
        raise HTTPException(status_code=500, detail="Erreur lors de la génération du fichier Excel")

# === RAPPORTS AUTOMATISÉS ===

@router.post("/reports/schedule")
def schedule_automated_report(
    report_data: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['teacher', 'admin']))
):
    """Programmer un rapport automatisé."""
    try:
        # Ici, vous pourriez intégrer avec un système de tâches comme Celery
        # Pour l'instant, on simule la programmation
        
        return {
            "message": "Rapport programmé avec succès",
            "report_id": "auto_report_123",
            "scheduled_for": report_data.get("scheduled_date"),
            "recipients": report_data.get("recipients", []),
            "report_type": report_data.get("report_type")
        }
        
    except Exception as e:
        print(f"Erreur dans schedule_automated_report: {str(e)}")
        raise HTTPException(status_code=400, detail="Erreur lors de la programmation du rapport")

@router.get("/reports/available")
def get_available_reports(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['teacher', 'admin']))
):
    """Récupérer la liste des rapports disponibles."""
    return [
        {
            "id": "student_progress",
            "name": "Rapport de progression étudiant",
            "description": "Rapport détaillé de la progression d'un étudiant",
            "formats": ["PDF", "Excel"],
            "parameters": ["student_id", "period"]
        },
        {
            "id": "class_performance",
            "name": "Rapport de performance classe",
            "description": "Rapport de performance d'une classe complète",
            "formats": ["PDF", "Excel"],
            "parameters": ["class_id"]
        },
        {
            "id": "quiz_analytics",
            "name": "Analytics des quiz",
            "description": "Analyse détaillée des résultats de quiz",
            "formats": ["Excel"],
            "parameters": ["class_id", "date_range"]
        },
        {
            "id": "competency_summary",
            "name": "Résumé des compétences",
            "description": "Résumé des compétences par classe",
            "formats": ["PDF", "Excel"],
            "parameters": ["class_id", "subject"]
        }
    ] 