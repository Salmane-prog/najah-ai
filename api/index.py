from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import random
import asyncio
from contextlib import asynccontextmanager

# Import des routers
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))
from api_router import api_router

# Configuration CORS pour Vercel
app = FastAPI(
    title="Najah AI Analytics Backend",
    description="Backend pour le système d'analytics en temps réel avec remédiation",
    version="1.0.0"
)

# Middleware CORS - autoriser toutes les origines pour Vercel
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Vercel gère les CORS
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclure les routers de l'API
app.include_router(api_router)

# Sécurité
security = HTTPBearer()

# Modèles de données
class TestAttempt(BaseModel):
    attempt_id: str
    test_id: int
    student_id: int
    student_name: str
    start_time: str

class TestProgress(BaseModel):
    attempt_id: str
    questions_answered: int
    total_questions: int
    time_spent: int

class TestCompletion(BaseModel):
    attempt_id: str
    score: float
    end_time: str
    time_spent: int
    questions_answered: int
    total_questions: int

class TestAbandon(BaseModel):
    attempt_id: str
    end_time: str
    time_spent: int
    questions_answered: int
    total_questions: int

# Base de données simulée (remplacer par une vraie DB)
class MockDatabase:
    def __init__(self):
        self.test_attempts = {}
        self.student_performances = {}
        self.test_performances = {}
        self.analytics_data = {}
        self.active_sessions = {}
        self.initialize_mock_data()
    
    def initialize_mock_data(self):
        # Données d'étudiants simulées (plus réalistes)
        self.student_performances = {
            1: {"id": 1, "name": "Alice Martin", "email": "alice.martin@najah.ai", "testsCompleted": 12, "averageScore": 87, "progressPercentage": 87, "lastTestDate": datetime.now().isoformat(), "improvementTrend": "up"},
            2: {"id": 2, "name": "Bob Dupont", "email": "bob.dupont@najah.ai", "testsCompleted": 15, "averageScore": 82, "progressPercentage": 82, "lastTestDate": datetime.now().isoformat(), "improvementTrend": "stable"},
            3: {"id": 3, "name": "Claire Moreau", "email": "claire.moreau@najah.ai", "testsCompleted": 18, "averageScore": 91, "progressPercentage": 91, "lastTestDate": datetime.now().isoformat(), "improvementTrend": "up"},
            4: {"id": 4, "name": "David Leroy", "email": "david.leroy@najah.ai", "testsCompleted": 9, "averageScore": 78, "progressPercentage": 78, "lastTestDate": datetime.now().isoformat(), "improvementTrend": "down"},
            5: {"id": 5, "name": "Emma Dubois", "email": "emma.dubois@najah.ai", "testsCompleted": 21, "averageScore": 94, "progressPercentage": 94, "lastTestDate": datetime.now().isoformat(), "improvementTrend": "up"},
            6: {"id": 6, "name": "François Rousseau", "email": "francois.rousseau@najah.ai", "testsCompleted": 14, "averageScore": 85, "progressPercentage": 85, "lastTestDate": datetime.now().isoformat(), "improvementTrend": "up"},
            7: {"id": 7, "name": "Gabrielle Blanc", "email": "gabrielle.blanc@najah.ai", "testsCompleted": 16, "averageScore": 89, "progressPercentage": 89, "lastTestDate": datetime.now().isoformat(), "improvementTrend": "stable"},
            8: {"id": 8, "name": "Hugo Petit", "email": "hugo.petit@najah.ai", "testsCompleted": 11, "averageScore": 76, "progressPercentage": 76, "lastTestDate": datetime.now().isoformat(), "improvementTrend": "down"},
            9: {"id": 9, "name": "Isabelle Roux", "email": "isabelle.roux@najah.ai", "testsCompleted": 19, "averageScore": 92, "progressPercentage": 92, "lastTestDate": datetime.now().isoformat(), "improvementTrend": "up"},
            10: {"id": 10, "name": "Jules Simon", "email": "jules.simon@najah.ai", "testsCompleted": 13, "averageScore": 83, "progressPercentage": 83, "lastTestDate": datetime.now().isoformat(), "improvementTrend": "stable"}
        }
        
        # Données de tests simulées (plus réalistes)
        self.test_performances = {
            1: {"id": 1, "title": "Test Mathématiques Avancé", "subject": "Mathématiques", "participants": 25, "averageScore": 92.5, "completionRate": 96, "difficultyLevel": 8, "timeSpent": 45, "successRate": 88, "lastAttemptDate": datetime.now().isoformat()},
            2: {"id": 2, "title": "Test Français Grammaire", "subject": "Français", "participants": 30, "averageScore": 88.3, "completionRate": 92, "difficultyLevel": 6, "timeSpent": 35, "successRate": 85, "lastAttemptDate": datetime.now().isoformat()},
            3: {"id": 3, "title": "Test Histoire Moderne", "subject": "Histoire", "participants": 22, "averageScore": 85.7, "completionRate": 89, "difficultyLevel": 7, "timeSpent": 40, "successRate": 82, "lastAttemptDate": datetime.now().isoformat()},
            4: {"id": 4, "title": "Test Sciences Physiques", "subject": "Sciences", "participants": 28, "averageScore": 79.2, "completionRate": 87, "difficultyLevel": 9, "timeSpent": 50, "successRate": 76, "lastAttemptDate": datetime.now().isoformat()},
            5: {"id": 5, "title": "Test Géographie", "subject": "Géographie", "participants": 20, "averageScore": 83.1, "completionRate": 90, "difficultyLevel": 5, "timeSpent": 30, "successRate": 89, "lastAttemptDate": datetime.now().isoformat()},
            6: {"id": 6, "title": "Test Biologie Cellulaire", "subject": "Biologie", "participants": 18, "averageScore": 81.4, "completionRate": 85, "difficultyLevel": 8, "timeSpent": 55, "successRate": 79, "lastAttemptDate": datetime.now().isoformat()},
            7: {"id": 7, "title": "Test Littérature Française", "subject": "Littérature", "participants": 24, "averageScore": 86.2, "completionRate": 91, "difficultyLevel": 7, "timeSpent": 38, "successRate": 84, "lastAttemptDate": datetime.now().isoformat()},
            8: {"id": 8, "title": "Test Chimie Organique", "subject": "Chimie", "participants": 16, "averageScore": 77.8, "completionRate": 83, "difficultyLevel": 9, "timeSpent": 60, "successRate": 72, "lastAttemptDate": datetime.now().isoformat()},
        }

# Instance globale de la base de données
db = MockDatabase()

# Routes de base
@app.get("/")
async def root():
    return {"message": "Najah AI Backend API", "status": "running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

# Routes pour les analytics
@app.get("/analytics/students")
async def get_students_analytics():
    """Récupérer les analytics des étudiants"""
    return {
        "students": list(db.student_performances.values()),
        "total_students": len(db.student_performances),
        "average_score": sum(s["averageScore"] for s in db.student_performances.values()) / len(db.student_performances)
    }

@app.get("/analytics/tests")
async def get_tests_analytics():
    """Récupérer les analytics des tests"""
    return {
        "tests": list(db.test_performances.values()),
        "total_tests": len(db.test_performances),
        "average_completion_rate": sum(t["completionRate"] for t in db.test_performances.values()) / len(db.test_performances)
    }

# Routes pour les tentatives de test
@app.post("/test-attempts/start")
async def start_test_attempt(attempt: TestAttempt):
    """Démarrer une tentative de test"""
    attempt_id = attempt.attempt_id
    db.test_attempts[attempt_id] = {
        **attempt.dict(),
        "status": "active",
        "start_time": datetime.now().isoformat()
    }
    db.active_sessions[attempt_id] = {
        "student_id": attempt.student_id,
        "test_id": attempt.test_id,
        "start_time": datetime.now()
    }
    return {"message": "Test attempt started", "attempt_id": attempt_id}

@app.post("/test-attempts/progress")
async def update_test_progress(progress: TestProgress):
    """Mettre à jour le progrès d'une tentative"""
    if progress.attempt_id not in db.test_attempts:
        raise HTTPException(status_code=404, detail="Test attempt not found")
    
    db.test_attempts[progress.attempt_id].update({
        "questions_answered": progress.questions_answered,
        "time_spent": progress.time_spent,
        "last_update": datetime.now().isoformat()
    })
    return {"message": "Progress updated"}

@app.post("/test-attempts/complete")
async def complete_test_attempt(completion: TestCompletion):
    """Terminer une tentative de test"""
    if completion.attempt_id not in db.test_attempts:
        raise HTTPException(status_code=404, detail="Test attempt not found")
    
    db.test_attempts[completion.attempt_id].update({
        "status": "completed",
        "score": completion.score,
        "end_time": completion.end_time,
        "time_spent": completion.time_spent,
        "questions_answered": completion.questions_answered
    })
    
    # Mettre à jour les performances de l'étudiant
    student_id = db.test_attempts[completion.attempt_id]["student_id"]
    if student_id in db.student_performances:
        student = db.student_performances[student_id]
        student["testsCompleted"] += 1
        student["averageScore"] = (student["averageScore"] * (student["testsCompleted"] - 1) + completion.score) / student["testsCompleted"]
        student["lastTestDate"] = completion.end_time
    
    # Nettoyer la session active
    if completion.attempt_id in db.active_sessions:
        del db.active_sessions[completion.attempt_id]
    
    return {"message": "Test completed successfully", "score": completion.score}

@app.post("/test-attempts/abandon")
async def abandon_test_attempt(abandon: TestAbandon):
    """Abandonner une tentative de test"""
    if abandon.attempt_id not in db.test_attempts:
        raise HTTPException(status_code=404, detail="Test attempt not found")
    
    db.test_attempts[abandon.attempt_id].update({
        "status": "abandoned",
        "end_time": abandon.end_time,
        "time_spent": abandon.time_spent,
        "questions_answered": abandon.questions_answered
    })
    
    # Nettoyer la session active
    if abandon.attempt_id in db.active_sessions:
        del db.active_sessions[abandon.attempt_id]
    
    return {"message": "Test abandoned"}

# Route pour les sessions actives
@app.get("/active-sessions")
async def get_active_sessions():
    """Récupérer les sessions actives"""
    return {
        "active_sessions": len(db.active_sessions),
        "sessions": list(db.active_sessions.values())
    }

# Route pour les statistiques globales
@app.get("/stats")
async def get_global_stats():
    """Récupérer les statistiques globales"""
    total_students = len(db.student_performances)
    total_tests = len(db.test_performances)
    active_sessions = len(db.active_sessions)
    
    return {
        "total_students": total_students,
        "total_tests": total_tests,
        "active_sessions": active_sessions,
        "average_student_score": sum(s["averageScore"] for s in db.student_performances.values()) / total_students if total_students > 0 else 0,
        "average_test_completion": sum(t["completionRate"] for t in db.test_performances.values()) / total_tests if total_tests > 0 else 0
    }

# Handler pour Vercel
def handler(request):
    return app
