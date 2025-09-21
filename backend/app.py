# Configuration Railway en premier
try:
    import railway_config
    print("✅ Configuration Railway chargée")
except ImportError:
    print("⚠️ Configuration Railway non trouvée, utilisation des paramètres par défaut")

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
import json
from datetime import datetime

# Renommer l'application pour éviter les conflits avec Flask
fastapi_app = FastAPI(title="Plateforme éducative IA", version="1.0")

# CORS configuration - CORRIGÉE
fastapi_app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3001",  # Frontend Next.js
        "http://localhost:3000",  # Port alternatif
        "http://127.0.0.1:3001",  # IP locale
        "http://127.0.0.1:3000",  # IP locale port alternatif
        "*"  # Temporairement pour le développement
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH", "HEAD"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=86400,  # Cache preflight pour 24h
)

# --- ROUTEURS API v1 ---
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from api.v1 import (
    auth, users, quizzes, quiz_results,
    badges, class_groups, contents, learning_paths,
    learning_history, messages, ai_analytics, student_performance,
    assessment, recommendations, gamification, advanced_analytics,
    performance_monitoring, gap_analysis, adaptive_quizzes, cognitive_diagnostic,
    teacher_tasks, student_learning_paths, progress_tracking
)
from api.v1 import ai, reports, notifications, notifications_ws, threads, notification_preferences, categories, quiz_json
from api.v1 import settings, score_corrections
from api.v1 import teacher_messaging, student_messaging, teacher_schedule, auto_correction, remediation, teacher_collaboration, calendar, continuous_assessment, export_reports, ai_advanced, external_integrations, dashboard_data, student_analytics, notes, teacher_classes
from api.v1 import forum, organization
from api.v1 import library
from api.v1 import organization_advanced, teacher_assignments, student_organization_real, notifications_advanced
from api.v1 import content_sharing, assignments
from api.v1 import student_organization, learning_goals
from api.v1 import homework, collaboration
from api.v1 import activity
from api.v1 import students
from api.v1 import files

# Nouveaux routers français
from api.v1 import french_initial_assessment, french_learning_paths, french_recommendations

# Nouveaux routers pour l'évaluation adaptative et l'IA
from api.v1 import adaptive_evaluation, ai_analytics, ai_models, teacher_dashboard, ai_analytics_real, real_student_analytics, ai_formative_evaluations, formative_evaluations, analytics

# Nouveaux routers pour les fonctionnalités IA avancées
from api.v1 import data_collection, training_sessions

# Nouveaux routers pour les quiz assignés et assessments
from api.v1 import quiz_assignments, assessments, test_endpoints

# Nouveaux routers pour les recommandations IA et analytics
from api.v1 import ai_recommendations, learning_analytics

fastapi_app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
fastapi_app.include_router(users.router, prefix="/api/v1/users", tags=["users"])
fastapi_app.include_router(quizzes.router, prefix="/api/v1/quizzes", tags=["quizzes"])
fastapi_app.include_router(quiz_results.router, prefix="/api/v1/quiz_results", tags=["quiz_results"])
fastapi_app.include_router(badges.router, prefix="/api/v1/badges", tags=["badges"])
fastapi_app.include_router(class_groups.router, prefix="/api/v1/class_groups", tags=["class_groups"])
fastapi_app.include_router(contents.router, prefix="/api/v1/contents", tags=["contents"])
fastapi_app.include_router(learning_paths.router, prefix="/api/v1/learning_paths", tags=["learning_paths"])
fastapi_app.include_router(learning_history.router, prefix="/api/v1/learning_history", tags=["learning_history"])
fastapi_app.include_router(messages.router, prefix="/api/v1/messages", tags=["messages"])
# Routeurs principaux
fastapi_app.include_router(analytics.router, prefix="/api/v1/analytics", tags=["analytics"])
fastapi_app.include_router(ai_analytics.router, prefix="/api/v1/ai-analytics", tags=["ai_analytics"])
fastapi_app.include_router(student_performance.router, prefix="/api/v1/student_performance", tags=["student_performance"])
fastapi_app.include_router(assessment.router, prefix="/api/v1/assessment", tags=["assessment"])
fastapi_app.include_router(recommendations.router, prefix="/api/v1/recommendations", tags=["recommendations"])
fastapi_app.include_router(gamification.router, prefix="/api/v1/gamification", tags=["gamification"])
fastapi_app.include_router(advanced_analytics.router, prefix="/api/v1/advanced_analytics", tags=["advanced_analytics"])
fastapi_app.include_router(performance_monitoring.router, prefix="/api/v1/performance_monitoring", tags=["performance_monitoring"])
fastapi_app.include_router(gap_analysis.router, prefix="/api/v1/gap_analysis", tags=["gap_analysis"])
fastapi_app.include_router(adaptive_quizzes.router, prefix="/api/v1/adaptive_quizzes", tags=["adaptive_quizzes"])
fastapi_app.include_router(ai.router, prefix="/api/v1/ai", tags=["ai"])
fastapi_app.include_router(reports.router, prefix="/api/v1/reports", tags=["reports"])
fastapi_app.include_router(notifications.router, prefix="/api/v1/notifications", tags=["notifications"])
fastapi_app.include_router(notifications_ws.router, prefix="/api/v1/notifications_ws", tags=["notifications_ws"])
fastapi_app.include_router(threads.router, prefix="/api/v1/threads", tags=["threads"])
fastapi_app.include_router(notification_preferences.router, prefix="/api/v1/notification_preferences", tags=["notification_preferences"])
fastapi_app.include_router(categories.router, prefix="/api/v1/categories", tags=["categories"])
fastapi_app.include_router(quiz_json.router, prefix="/api/v1/quiz_json", tags=["quiz_json"])
fastapi_app.include_router(settings.router, prefix="/api/v1/settings", tags=["settings"])
fastapi_app.include_router(score_corrections.router, prefix="/api/v1/score_corrections", tags=["score_corrections"])
fastapi_app.include_router(teacher_tasks.router, prefix="/api/v1", tags=["teacher_tasks"])
fastapi_app.include_router(cognitive_diagnostic.router, prefix="/api/v1/cognitive_diagnostic", tags=["cognitive_diagnostic"])
fastapi_app.include_router(progress_tracking.router, prefix="/api/v1/progress", tags=["progress_tracking"])

# Nouveaux routers pour les fonctionnalités avancées du professeur
fastapi_app.include_router(teacher_classes.router, prefix="/api/v1/teacher/classes", tags=["teacher_classes"])
fastapi_app.include_router(content_sharing.router, prefix="/api/v1/content-sharing", tags=["content_sharing"])
fastapi_app.include_router(assignments.router, prefix="/api/v1/assignments", tags=["assignments"])
fastapi_app.include_router(files.router, prefix="/api/v1", tags=["files"])
fastapi_app.include_router(teacher_messaging.router, prefix="/api/v1/teacher_messaging", tags=["teacher_messaging"])
fastapi_app.include_router(teacher_schedule.router, prefix="/api/v1/teacher_schedule", tags=["teacher_schedule"])
fastapi_app.include_router(auto_correction.router, prefix="/api/v1/auto_correction", tags=["auto_correction"])
fastapi_app.include_router(remediation.router, prefix="/api/v1/remediation", tags=["remediation"])
fastapi_app.include_router(teacher_collaboration.router, prefix="/api/v1/teacher_collaboration", tags=["teacher_collaboration"])
fastapi_app.include_router(calendar.router, prefix="/api/v1/calendar", tags=["calendar"])
fastapi_app.include_router(continuous_assessment.router, prefix="/api/v1/continuous_assessment", tags=["continuous_assessment"])
fastapi_app.include_router(export_reports.router, prefix="/api/v1/export_reports", tags=["export_reports"])
fastapi_app.include_router(ai_advanced.router, prefix="/api/v1/ai_advanced", tags=["ai_advanced"])
# Alias pour la compatibilité avec le frontend
fastapi_app.include_router(ai_advanced.router, prefix="/api/v1/ai-advanced", tags=["ai_advanced"])

# Nouveaux routers pour l'évaluation adaptative et l'IA
fastapi_app.include_router(adaptive_evaluation.router, prefix="/api/v1/adaptive-evaluation", tags=["adaptive_evaluation"])
# fastapi_app.include_router(teacher_adaptive_evaluation.router, prefix="/api/v1/teacher-adaptive-evaluation", tags=["teacher_adaptive_evaluation"])
# FICHIER EN CONFLIT COMPLÈTEMENT DÉSACTIVÉ
fastapi_app.include_router(ai_analytics.router, prefix="/api/v1/ai-analytics", tags=["ai_analytics"])
fastapi_app.include_router(ai_models.router, prefix="/api/v1/ai-models", tags=["ai_models"])

# Nouveau router pour le dashboard du professeur avec données réelles
fastapi_app.include_router(teacher_dashboard.router, prefix="/api/v1/teacher-dashboard", tags=["teacher_dashboard"])

# Nouveau router pour les analytics IA avancées avec données réelles
fastapi_app.include_router(ai_analytics_real.router, prefix="/api/v1/ai-analytics", tags=["ai_analytics_real"])

# Nouveaux routers pour les fonctionnalités IA avancées
fastapi_app.include_router(data_collection.router, prefix="/api/v1/data_collection", tags=["data_collection"])
fastapi_app.include_router(training_sessions.router, prefix="/api/v1/training_sessions", tags=["training_sessions"])

# Nouveau router pour les analytics réelles des étudiants
fastapi_app.include_router(real_student_analytics.router, prefix="/api/v1/real-student-analytics", tags=["real_student_analytics"])

# Alias pour advanced_analytics avec le préfixe ai-advanced
fastapi_app.include_router(advanced_analytics.router, prefix="/api/v1/ai-advanced-alias", tags=["advanced_analytics"])
fastapi_app.include_router(external_integrations.router, prefix="/api/v1/integrations", tags=["external_integrations"])

# Nouveau router pour les données du dashboard
fastapi_app.include_router(dashboard_data.router, prefix="/api/v1/dashboard", tags=["dashboard_data"])

# Nouveau router pour les analytics des étudiants
fastapi_app.include_router(student_analytics.router, prefix="/api/v1/student_analytics", tags=["student_analytics"])

# Nouveau router pour les endpoints analytics des étudiants (graphiques)
from api.v1 import student_analytics_endpoints
fastapi_app.include_router(student_analytics_endpoints.router, prefix="/api/v1/analytics", tags=["student_analytics_endpoints"])

# Nouveau router pour la messagerie des étudiants
fastapi_app.include_router(student_messaging.router, prefix="/api/v1/student_messaging", tags=["student_messaging"])

# Router pour les notes
fastapi_app.include_router(notes.router, prefix="/api/v1/notes", tags=["notes"])

# Router pour les étudiants
fastapi_app.include_router(students.router, prefix="/api/v1/students", tags=["students"])

# Router pour les parcours d'apprentissage des étudiants
fastapi_app.include_router(student_learning_paths.router, prefix="/api/v1/student_learning_paths", tags=["student_learning_paths"])

# Nouveau router pour les objectifs d'apprentissage
fastapi_app.include_router(learning_goals.router, prefix="/api/v1", tags=["learning_goals"])

# Nouveau router pour les assignations du professeur
fastapi_app.include_router(teacher_assignments.router, prefix="/api/v1/teacher-assignments", tags=["teacher_assignments"])

# Nouveau router pour l'IA des évaluations formatives
fastapi_app.include_router(ai_formative_evaluations.router, prefix="/api/v1", tags=["ai_formative_evaluations"])

# Nouveau router pour les évaluations formatives
fastapi_app.include_router(formative_evaluations.router, prefix="/api/v1", tags=["formative_evaluations"])

# Nouveaux routers pour les quiz assignés et assessments
fastapi_app.include_router(quiz_assignments.router, prefix="/api/v1/quiz_assignments", tags=["quiz_assignments"])
fastapi_app.include_router(assessments.router, prefix="/api/v1/assessments", tags=["assessments"])
fastapi_app.include_router(test_endpoints.router, prefix="/api/v1/test", tags=["test"])

# Nouveaux routers pour les recommandations IA et analytics
fastapi_app.include_router(ai_recommendations.router, prefix="/api/v1/ai-recommendations", tags=["ai_recommendations"])
fastapi_app.include_router(learning_analytics.router, prefix="/api/v1/learning-analytics", tags=["learning_analytics"])

# Nouveau router pour l'organisation avancée
fastapi_app.include_router(organization_advanced.router, prefix="/api/v1/organization_advanced", tags=["organization_advanced"])

# Nouveaux routers pour les fonctionnalités développées
fastapi_app.include_router(homework.router, prefix="/api/v1/homework", tags=["homework"])
fastapi_app.include_router(collaboration.router, prefix="/api/v1/collaboration", tags=["collaboration"])
fastapi_app.include_router(activity.router, prefix="/api/v1/activity", tags=["activity"])

# Nouveaux routers pour les services de test (sans authentification)
from api.v1 import quiz_assignments as quiz_assignments_test
from api.v1 import student_analytics as student_analytics_test
from api.v1 import calendar as calendar_test
from api.v1 import student_quizzes as student_quizzes_test
from api.v1 import notifications as notifications_test
from api.v1 import analytics as analytics_test

fastapi_app.include_router(quiz_assignments_test.router, prefix="/api/v1/quiz_assignments", tags=["quiz_assignments_test"])
fastapi_app.include_router(student_analytics_test.router, prefix="/api/v1/student_analytics", tags=["student_analytics_test"])
fastapi_app.include_router(calendar_test.router, prefix="/api/v1/calendar", tags=["calendar_test"])
fastapi_app.include_router(student_quizzes_test.router, prefix="/api/v1/student_quizzes", tags=["student_quizzes_test"])
fastapi_app.include_router(notifications_test.router, prefix="/api/v1/notifications", tags=["notifications_test"])
fastapi_app.include_router(analytics_test.router, prefix="/api/v1/analytics", tags=["analytics_test"])

# Router pour l'organisation
fastapi_app.include_router(organization.router, prefix="/api/v1", tags=["organization"])

# Router pour le forum
fastapi_app.include_router(forum.router, prefix="/api/v1/forum", tags=["forum"])

# Nouveaux routers français pour l'apprentissage adaptatif
fastapi_app.include_router(french_initial_assessment.router, prefix="/api/v1/french", tags=["french_initial_assessment"])
fastapi_app.include_router(french_learning_paths.router, prefix="/api/v1/french", tags=["french_learning_paths"])
fastapi_app.include_router(french_recommendations.router, prefix="/api/v1/french", tags=["french_recommendations"])

# Router pour l'onboarding automatique des étudiants
from api.v1 import student_onboarding
fastapi_app.include_router(student_onboarding.router, prefix="/api/v1/onboarding", tags=["student_onboarding"])

# NOUVELLE API OPTIMISÉE pour l'évaluation française (20 questions)
try:
    from api.v1.french_initial_assessment_optimized import router as french_optimized_router
    fastapi_app.include_router(french_optimized_router, prefix="/api/v1/french-optimized", tags=["french_optimized"])
    print("✅ API française optimisée intégrée avec succès")
except ImportError as e:
    print(f"⚠️ Impossible d'importer l'API française optimisée: {e}")

# --- ROUTEURS API v2 (si nécessaire) ---

# --- ROUTEURS SPÉCIAUX ---

@fastapi_app.get("/")
def read_root():
    return {"message": "Bienvenue sur l'API de la plateforme éducative IA", "version": "1.0"}

@fastapi_app.get("/health")
def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}

# --- GESTION DES ERREURS ---

@fastapi_app.exception_handler(404)
async def not_found_handler(request, exc):
    return Response(
        content=json.dumps({"detail": "Endpoint non trouvé"}),
        status_code=404,
        media_type="application/json"
    )

@fastapi_app.exception_handler(500)
async def internal_error_handler(request, exc):
    return Response(
        content=json.dumps({"detail": "Erreur interne du serveur"}),
        status_code=500,
        media_type="application/json"
    )

# --- MIDDLEWARE PERSONNALISÉ ---

@fastapi_app.middleware("http")
async def add_process_time_header(request, call_next):
    import time
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

# Variable pour uvicorn
app = fastapi_app 