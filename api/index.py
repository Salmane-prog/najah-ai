from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import random
import asyncio
from contextlib import asynccontextmanager
import hashlib
import jwt
import sqlite3
import os

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

# Sécurité
security = HTTPBearer()

# Modèles de données
class LoginRequest(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    email: str
    name: str
    role: str
    token: str

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

# Base de données simulée avec données réalistes
class MockDatabase:
    def __init__(self):
        self.test_attempts = {}
        self.active_sessions = {}
        self.users = {
            "student@test.com": {
                "id": 1,
                "email": "student@test.com",
                "password": "password123",
                "name": "Lucas Petit",
                "role": "student",
                "first_name": "Lucas",
                "last_name": "Petit"
            },
            "teacher@test.com": {
                "id": 2,
                "email": "teacher@test.com",
                "password": "password123",
                "name": "Marie Dupont",
                "role": "teacher",
                "first_name": "Marie",
                "last_name": "Dupont"
            },
            "admin@test.com": {
                "id": 3,
                "email": "admin@test.com",
                "password": "password123",
                "name": "Admin Najah",
                "role": "admin",
                "first_name": "Admin",
                "last_name": "Najah"
            },
            "student1@najah.ai": {
                "id": 4,
                "email": "student1@najah.ai",
                "password": "password123",
                "name": "Alice Martin",
                "role": "student",
                "first_name": "Alice",
                "last_name": "Martin"
            },
            "teacher1@najah.ai": {
                "id": 5,
                "email": "teacher1@najah.ai",
                "password": "password123",
                "name": "Jean Martin",
                "role": "teacher",
                "first_name": "Jean",
                "last_name": "Martin"
            }
        }
        self.initialize_mock_data()
    
    def initialize_mock_data(self):
        # Données d'étudiants simulées (plus réalistes)
        self.student_performances = {
            1: {"id": 1, "name": "Lucas Petit", "email": "student@test.com", "testsCompleted": 12, "averageScore": 87, "progressPercentage": 87, "lastTestDate": datetime.now().isoformat(), "improvementTrend": "up"},
            2: {"id": 2, "name": "Alice Martin", "email": "student1@najah.ai", "testsCompleted": 15, "averageScore": 82, "progressPercentage": 82, "lastTestDate": datetime.now().isoformat(), "improvementTrend": "stable"},
            3: {"id": 3, "name": "Bob Dupont", "email": "bob.dupont@najah.ai", "testsCompleted": 18, "averageScore": 91, "progressPercentage": 91, "lastTestDate": datetime.now().isoformat(), "improvementTrend": "up"},
            4: {"id": 4, "name": "Claire Moreau", "email": "claire.moreau@najah.ai", "testsCompleted": 9, "averageScore": 78, "progressPercentage": 78, "lastTestDate": datetime.now().isoformat(), "improvementTrend": "down"},
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

# Fonction pour générer un token JWT
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(hours=24)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, "secret_key", algorithm="HS256")
    return encoded_jwt

# Fonction pour vérifier le token
def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = jwt.decode(credentials.credentials, "secret_key", algorithms=["HS256"])
        return payload
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token invalide"
        )

# Routes de base
@app.get("/")
async def root():
    return {"message": "Najah AI Backend API", "status": "running", "database": "mock"}

@app.get("/health")
async def health_check():
    return {
        "status": "healthy", 
        "timestamp": datetime.now().isoformat(),
        "database": "mock",
        "users_count": len(db.users),
        "students_count": len([u for u in db.users.values() if u["role"] == "student"])
    }

# Route d'authentification
@app.post("/auth/login", response_model=UserResponse)
async def login(login_data: LoginRequest):
    """Authentifier un utilisateur"""
    user = db.users.get(login_data.email)
    if not user or user["password"] != login_data.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou mot de passe incorrect"
        )
    
    # Créer un token JWT
    access_token = create_access_token(
        data={"sub": user["email"], "user_id": user["id"], "role": user["role"]}
    )
    
    return UserResponse(
        id=user["id"],
        email=user["email"],
        name=user["name"],
        role=user["role"],
        token=access_token
    )

# Route pour vérifier le token
@app.get("/auth/verify")
async def verify_auth(current_user: dict = Depends(verify_token)):
    """Vérifier si le token est valide"""
    return {"valid": True, "user": current_user}

# Route pour obtenir les informations de l'utilisateur connecté
@app.get("/auth/me")
async def get_current_user_info(current_user: dict = Depends(verify_token)):
    """Récupérer les informations de l'utilisateur connecté"""
    user_id = current_user["user_id"]
    user = next((u for u in db.users.values() if u["id"] == user_id), None)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Utilisateur non trouvé"
        )
    
    return {
        "id": user["id"],
        "email": user["email"],
        "username": user["email"].split("@")[0],
        "name": user["name"],
        "role": user["role"],
        "is_active": True
    }

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

# Routes pour les quiz
@app.get("/quizzes")
async def get_quizzes():
    """Récupérer tous les quiz"""
    mock_quizzes = [
        {"id": 1, "title": "Quiz Mathématiques", "subject": "Mathématiques", "difficulty": "Moyen", "questions_count": 10, "duration": 30},
        {"id": 2, "title": "Quiz Français", "subject": "Français", "difficulty": "Facile", "questions_count": 15, "duration": 25},
        {"id": 3, "title": "Quiz Histoire", "subject": "Histoire", "difficulty": "Difficile", "questions_count": 20, "duration": 45},
        {"id": 4, "title": "Quiz Sciences", "subject": "Sciences", "difficulty": "Moyen", "questions_count": 12, "duration": 35},
    ]
    return {"quizzes": mock_quizzes, "total": len(mock_quizzes)}

@app.get("/quizzes/{quiz_id}")
async def get_quiz(quiz_id: int):
    """Récupérer un quiz spécifique"""
    mock_quizzes = {
        1: {"id": 1, "title": "Quiz Mathématiques", "subject": "Mathématiques", "difficulty": "Moyen", "questions_count": 10, "duration": 30, "description": "Test de connaissances en mathématiques de base"},
        2: {"id": 2, "title": "Quiz Français", "subject": "Français", "difficulty": "Facile", "questions_count": 15, "duration": 25, "description": "Évaluation des compétences en français"},
        3: {"id": 3, "title": "Quiz Histoire", "subject": "Histoire", "difficulty": "Difficile", "questions_count": 20, "duration": 45, "description": "Test d'histoire générale"},
        4: {"id": 4, "title": "Quiz Sciences", "subject": "Sciences", "difficulty": "Moyen", "questions_count": 12, "duration": 35, "description": "Évaluation des sciences naturelles"},
    }
    
    quiz = mock_quizzes.get(quiz_id)
    if not quiz:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quiz non trouvé"
        )
    return quiz

# Routes pour les questions
@app.get("/quizzes/{quiz_id}/questions")
async def get_quiz_questions(quiz_id: int):
    """Récupérer les questions d'un quiz"""
    mock_questions = {
        1: [
            {"id": 1, "question": "Quelle est la dérivée de x² ?", "type": "multiple_choice", "options": ["2x", "x", "2", "x²"], "correct_answer": 0},
            {"id": 2, "question": "Résolvez : 2x + 5 = 15", "type": "multiple_choice", "options": ["x = 5", "x = 10", "x = 3", "x = 7"], "correct_answer": 0},
        ],
        2: [
            {"id": 3, "question": "Quel est le pluriel de 'cheval' ?", "type": "multiple_choice", "options": ["chevals", "chevaux", "chevales", "cheval"], "correct_answer": 1},
            {"id": 4, "question": "Conjuguez 'être' à la 3ème personne du singulier", "type": "multiple_choice", "options": ["est", "êtes", "sont", "es"], "correct_answer": 0},
        ]
    }
    
    questions = mock_questions.get(quiz_id, [])
    return {"questions": questions, "total": len(questions)}

# Routes pour les résultats de quiz
@app.get("/quiz-results")
async def get_quiz_results():
    """Récupérer tous les résultats de quiz"""
    mock_results = [
        {"id": 1, "student_id": 1, "quiz_id": 1, "score": 85, "completed_at": datetime.now().isoformat(), "time_spent": 25},
        {"id": 2, "student_id": 1, "quiz_id": 2, "score": 92, "completed_at": datetime.now().isoformat(), "time_spent": 20},
        {"id": 3, "student_id": 4, "quiz_id": 1, "score": 78, "completed_at": datetime.now().isoformat(), "time_spent": 30},
    ]
    return {"results": mock_results, "total": len(mock_results)}

@app.get("/quiz-results/student/{student_id}")
async def get_student_quiz_results(student_id: int):
    """Récupérer les résultats d'un étudiant"""
    mock_results = [
        {"id": 1, "student_id": student_id, "quiz_id": 1, "score": 85, "completed_at": datetime.now().isoformat(), "time_spent": 25},
        {"id": 2, "student_id": student_id, "quiz_id": 2, "score": 92, "completed_at": datetime.now().isoformat(), "time_spent": 20},
    ]
    return {"results": mock_results, "total": len(mock_results)}

# Routes pour les utilisateurs
@app.get("/users")
async def get_users():
    """Récupérer tous les utilisateurs"""
    users = [
        {
            "id": user["id"],
            "email": user["email"],
            "name": user["name"],
            "role": user["role"],
            "is_active": True,
            "created_at": datetime.now().isoformat()
        }
        for user in db.users.values()
    ]
    return {"users": users, "total": len(users)}

@app.get("/users/students")
async def get_students():
    """Récupérer tous les étudiants"""
    students = [
        {
            "id": user["id"],
            "email": user["email"],
            "name": user["name"],
            "role": user["role"],
            "is_active": True,
            "created_at": datetime.now().isoformat()
        }
        for user in db.users.values() if user["role"] == "student"
    ]
    return {"students": students, "total": len(students)}

@app.get("/users/teachers")
async def get_teachers():
    """Récupérer tous les professeurs"""
    teachers = [
        {
            "id": user["id"],
            "email": user["email"],
            "name": user["name"],
            "role": user["role"],
            "is_active": True,
            "created_at": datetime.now().isoformat()
        }
        for user in db.users.values() if user["role"] == "teacher"
    ]
    return {"teachers": teachers, "total": len(teachers)}

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
    total_students = len([u for u in db.users.values() if u["role"] == "student"])
    total_teachers = len([u for u in db.users.values() if u["role"] == "teacher"])
    total_users = len(db.users)
    active_sessions = len(db.active_sessions)
    
    return {
        "total_users": total_users,
        "total_students": total_students,
        "total_teachers": total_teachers,
        "active_sessions": active_sessions,
        "average_student_score": sum(s["averageScore"] for s in db.student_performances.values()) / len(db.student_performances) if db.student_performances else 0,
        "average_test_completion": sum(t["completionRate"] for t in db.test_performances.values()) / len(db.test_performances) if db.test_performances else 0
    }

# Routes pour les classes
@app.get("/classes")
async def get_classes():
    """Récupérer toutes les classes"""
    mock_classes = [
        {"id": 1, "name": "6ème A", "level": "6ème", "students_count": 25},
        {"id": 2, "name": "5ème B", "level": "5ème", "students_count": 23},
        {"id": 3, "name": "4ème C", "level": "4ème", "students_count": 28},
        {"id": 4, "name": "3ème D", "level": "3ème", "students_count": 26},
    ]
    return {"classes": mock_classes, "total": len(mock_classes)}

# Routes pour les devoirs
@app.get("/assignments")
async def get_assignments():
    """Récupérer tous les devoirs"""
    mock_assignments = [
        {"id": 1, "title": "Devoir de Mathématiques", "subject": "Mathématiques", "due_date": "2024-01-15", "teacher_name": "Marie Dupont", "class_name": "6ème A"},
        {"id": 2, "title": "Rédaction Français", "subject": "Français", "due_date": "2024-01-20", "teacher_name": "Jean Martin", "class_name": "5ème B"},
        {"id": 3, "title": "TP Sciences", "subject": "Sciences", "due_date": "2024-01-18", "teacher_name": "Sophie Bernard", "class_name": "4ème C"},
    ]
    return {"assignments": mock_assignments, "total": len(mock_assignments)}

# Routes pour les notes
@app.get("/notes")
async def get_notes():
    """Récupérer toutes les notes"""
    mock_notes = [
        {"id": 1, "title": "Note importante", "content": "Rappel pour le devoir de mathématiques", "author_name": "Marie Dupont", "created_at": datetime.now().isoformat()},
        {"id": 2, "title": "Annonce", "content": "Examen de français prévu la semaine prochaine", "author_name": "Jean Martin", "created_at": datetime.now().isoformat()},
    ]
    return {"notes": mock_notes, "total": len(mock_notes)}

# Handler pour Vercel
def handler(request):
    return app