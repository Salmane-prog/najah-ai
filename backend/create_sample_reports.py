#!/usr/bin/env python3
"""
Script pour créer des rapports d'exemple
"""

import sys
import os

# Ajouter le répertoire parent au path pour les imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.database import SessionLocal
from sqlalchemy import text

def create_sample_reports():
    """Crée des rapports d'exemple"""
    print("=== CRÉATION DE RAPPORTS D'EXEMPLE ===")
    
    db = SessionLocal()
    try:
        # 1. Créer des rapports détaillés
        print("\n1. Création de rapports détaillés...")
        detailed_reports = [
            {
                "user_id": 1,
                "report_type": "performance",
                "title": "Rapport de performance - Mathématiques",
                "description": "Analyse détaillée des performances en mathématiques",
                "period_start": "2024-01-01 00:00:00",
                "period_end": "2024-01-31 23:59:59",
                "data": '{"quiz_count": 15, "average_score": 78.5, "topics": ["Algèbre", "Géométrie"]}',
                "insights": "Progression constante en algèbre, difficultés en géométrie",
                "recommendations": "Renforcer la pratique de la géométrie",
                "is_exported": False
            },
            {
                "user_id": 1,
                "report_type": "progress",
                "title": "Rapport de progression - Sciences",
                "description": "Suivi de la progression en sciences",
                "period_start": "2024-01-01 00:00:00",
                "period_end": "2024-01-31 23:59:59",
                "data": '{"experiments": 8, "understanding": "good", "areas": ["Physique", "Chimie"]}',
                "insights": "Excellente compréhension des concepts théoriques",
                "recommendations": "Plus de pratique expérimentale",
                "is_exported": True,
                "exported_at": "2024-01-31 10:00:00"
            }
        ]
        
        for report in detailed_reports:
            # Gérer le cas où exported_at peut être None
            exported_at = report.get('exported_at') if report.get('is_exported') else None
            
            db.execute(text("""
                INSERT INTO detailed_reports 
                (user_id, report_type, title, description, period_start, period_end, data, insights, recommendations, is_exported, exported_at)
                VALUES (:user_id, :report_type, :title, :description, :period_start, :period_end, :data, :insights, :recommendations, :is_exported, :exported_at)
            """), {**report, 'exported_at': exported_at})
        
        print(f"  - {len(detailed_reports)} rapports détaillés créés")
        
        # 2. Créer des rapports de progression par matière
        print("\n2. Création de rapports de progression...")
        subject_reports = [
            {
                "user_id": 1,
                "subject": "Mathématiques",
                "period_start": "2024-01-01 00:00:00",
                "period_end": "2024-01-31 23:59:59",
                "total_score": 785.0,
                "max_score": 1000.0,
                "percentage": 78.5,
                "improvement_rate": 0.15,
                "topics_covered": "Algèbre, Géométrie, Trigonométrie",
                "strengths": "Calcul mental, Résolution d'équations",
                "weaknesses": "Géométrie dans l'espace",
                "recommendations": "Plus d'exercices de géométrie"
            },
            {
                "user_id": 1,
                "subject": "Sciences",
                "period_start": "2024-01-01 00:00:00",
                "period_end": "2024-01-31 23:59:59",
                "total_score": 920.0,
                "max_score": 1000.0,
                "percentage": 92.0,
                "improvement_rate": 0.08,
                "topics_covered": "Physique, Chimie, Biologie",
                "strengths": "Compréhension théorique, Analyse",
                "weaknesses": "Calculs numériques",
                "recommendations": "Pratiquer les calculs"
            }
        ]
        
        for report in subject_reports:
            db.execute(text("""
                INSERT INTO subject_progress_reports 
                (user_id, subject, period_start, period_end, total_score, max_score, percentage, improvement_rate, topics_covered, strengths, weaknesses, recommendations)
                VALUES (:user_id, :subject, :period_start, :period_end, :total_score, :max_score, :percentage, :improvement_rate, :topics_covered, :strengths, :weaknesses, :recommendations)
            """), report)
        
        print(f"  - {len(subject_reports)} rapports de progression créés")
        
        # 3. Créer des rapports d'analytics
        print("\n3. Création de rapports d'analytics...")
        analytics_reports = [
            {
                "user_id": 1,
                "analytics_type": "learning_patterns",
                "period_start": "2024-01-01 00:00:00",
                "period_end": "2024-01-31 23:59:59",
                "metrics": '{"study_time": 45, "quiz_completion": 85, "content_engagement": 92}',
                "trends": "Amélioration constante du temps d'étude",
                "insights": "L'étudiant est plus efficace le matin",
                "recommendations": "Programmer les sessions importantes le matin"
            },
            {
                "user_id": 1,
                "analytics_type": "performance_analysis",
                "period_start": "2024-01-01 00:00:00",
                "period_end": "2024-01-31 23:59:59",
                "metrics": '{"overall_score": 85.2, "consistency": 78, "growth_rate": 12}',
                "trends": "Croissance stable des performances",
                "insights": "Bonne régularité dans l'apprentissage",
                "recommendations": "Maintenir le rythme actuel"
            }
        ]
        
        for report in analytics_reports:
            db.execute(text("""
                INSERT INTO analytics_reports 
                (user_id, analytics_type, period_start, period_end, metrics, trends, insights, recommendations)
                VALUES (:user_id, :analytics_type, :period_start, :period_end, :metrics, :trends, :insights, :recommendations)
            """), report)
        
        print(f"  - {len(analytics_reports)} rapports d'analytics créés")
        
        # Valider les changements
        db.commit()
        print("\n=== RAPPORTS D'EXEMPLE CRÉÉS AVEC SUCCÈS ===")
        
    except Exception as e:
        print(f"ERREUR: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("Démarrage de la création de rapports d'exemple...")
    create_sample_reports()
    print("Script terminé!")
