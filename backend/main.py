from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import uvicorn
from datetime import datetime, timedelta
import random
import asyncio
from contextlib import asynccontextmanager

# Import des routers
from api_router import api_router

# Configuration CORS
app = FastAPI(
    title="Najah AI Analytics Backend",
    description="Backend pour le système d'analytics en temps réel avec remédiation",
    version="1.0.0"
)

# Middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
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
            9: {"id": 9, "title": "Test Philosophie Moderne", "subject": "Philosophie", "participants": 19, "averageScore": 84.6, "completionRate": 88, "difficultyLevel": 6, "timeSpent": 42, "successRate": 81, "lastAttemptDate": datetime.now().isoformat()},
            10: {"id": 10, "title": "Test Informatique", "subject": "Informatique", "participants": 26, "averageScore": 89.1, "completionRate": 94, "difficultyLevel": 7, "timeSpent": 33, "successRate": 87, "lastAttemptDate": datetime.now().isoformat()}
        }
        
        # Données d'analytics simulées
        self.analytics_data = {
            "performance_metrics": {
                "overallAverageScore": 78.5,
                "totalTestsCompleted": 156,
                "totalStudents": 24,
                "completionRate": 85.2,
                "difficultTestsPercentage": 25,
                "topPerformingTests": list(self.test_performances.values())[:3],
                "topPerformingStudents": list(self.student_performances.values())[:3],
                "weeklyProgress": [
                    {"week": "S1", "averageScore": 65, "testsCompleted": 15, "studentsActive": 20, "improvementRate": 2.5},
                    {"week": "S2", "averageScore": 68, "testsCompleted": 18, "studentsActive": 22, "improvementRate": 3.2},
                    {"week": "S3", "averageScore": 71, "testsCompleted": 20, "studentsActive": 23, "improvementRate": 2.8},
                    {"week": "S4", "averageScore": 74, "testsCompleted": 22, "studentsActive": 24, "improvementRate": 3.5},
                    {"week": "S5", "averageScore": 76, "testsCompleted": 25, "studentsActive": 24, "improvementRate": 2.9},
                    {"week": "S6", "averageScore": 78, "testsCompleted": 28, "studentsActive": 25, "improvementRate": 3.1},
                    {"week": "S7", "averageScore": 80, "testsCompleted": 30, "studentsActive": 25, "improvementRate": 3.3}
                ],
                "monthlyStats": [
                    {"month": "M1", "testsCreated": 3, "testsCompleted": 20, "newStudents": 2, "averagePerformance": 75},
                    {"month": "M2", "testsCreated": 4, "testsCompleted": 25, "newStudents": 3, "averagePerformance": 77},
                    {"month": "M3", "testsCreated": 5, "testsCompleted": 30, "newStudents": 1, "averagePerformance": 79},
                    {"month": "M4", "testsCreated": 3, "testsCompleted": 22, "newStudents": 2, "averagePerformance": 81},
                    {"month": "M5", "testsCreated": 4, "testsCompleted": 28, "newStudents": 2, "averagePerformance": 83},
                    {"month": "M6", "testsCreated": 5, "testsCompleted": 35, "newStudents": 3, "averagePerformance": 85},
                    {"month": "M7", "testsCreated": 6, "testsCompleted": 40, "newStudents": 1, "averagePerformance": 87}
                ]
            }
        }

# Instance de la base de données
db = MockDatabase()

# Fonction de vérification du token (simulée)
async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    # Ici vous pouvez implémenter une vraie vérification JWT
    if not token or token != "najah_token":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token invalide"
        )
    return token

# Endpoints Analytics
@app.get("/api/v1/analytics/performance-metrics")
async def get_performance_metrics(token: str = Depends(verify_token)):
    """Récupérer les métriques de performance globales"""
    try:
        print(f"📊 Récupération des métriques de performance - Token: {token[:10]}...")
        return db.analytics_data["performance_metrics"]
    except Exception as e:
        print(f"❌ Erreur lors de la récupération des métriques: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/analytics/student-performances")
async def get_student_performances(token: str = Depends(verify_token)):
    """Récupérer les performances des étudiants"""
    try:
        print(f"👥 Récupération des performances étudiants - Token: {token[:10]}...")
        return list(db.student_performances.values())
    except Exception as e:
        print(f"❌ Erreur lors de la récupération des performances étudiants: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/analytics/test-performances")
async def get_test_performances(token: str = Depends(verify_token)):
    """Récupérer les performances des tests"""
    try:
        print(f"📝 Récupération des performances tests - Token: {token[:10]}...")
        return list(db.test_performances.values())
    except Exception as e:
        print(f"❌ Erreur lors de la récupération des performances tests: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/analytics/real-time")
async def get_real_time_data(token: str = Depends(verify_token)):
    """Récupérer les données en temps réel"""
    try:
        print(f"🔄 Récupération des données temps réel - Token: {token[:10]}...")
        
        # Simuler des données en temps réel
        current_time = datetime.now()
        
        real_time_data = {
            "currentActiveTests": len(db.active_sessions),
            "studentsOnline": random.randint(15, 25),
            "testsInProgress": random.randint(5, 12),
            "recentCompletions": [
                {
                    "testId": 1,
                    "testTitle": "Test Mathématiques Avancé",
                    "studentName": "Alice Martin",
                    "score": 92,
                    "completionTime": current_time.isoformat(),
                    "duration": 45
                }
            ],
            "systemHealth": {
                "backendStatus": "online",
                "databaseStatus": "healthy",
                "lastUpdate": current_time.isoformat(),
                "activeConnections": random.randint(30, 50)
            }
        }
        
        return real_time_data
    except Exception as e:
        print(f"❌ Erreur lors de la récupération des données temps réel: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Endpoints Test Tracking
@app.post("/api/v1/test-tracking/start")
async def start_test(attempt: TestAttempt, token: str = Depends(verify_token)):
    """Démarrer un test"""
    try:
        print(f"🚀 Démarrage du test {attempt.test_id} pour {attempt.student_name}")
        
        # Stocker la tentative
        db.test_attempts[attempt.attempt_id] = {
            "id": attempt.attempt_id,
            "testId": attempt.test_id,
            "studentId": attempt.student_id,
            "studentName": attempt.student_name,
            "startTime": attempt.start_time,
            "status": "in_progress",
            "questionsAnswered": 0,
            "totalQuestions": 0,
            "timeSpent": 0
        }
        
        # Mettre à jour la session active
        if attempt.test_id not in db.active_sessions:
            db.active_sessions[attempt.test_id] = {
                "testId": attempt.test_id,
                "testTitle": f"Test {attempt.test_id}",
                "activeStudents": 1,
                "lastActivity": current_time.isoformat()
            }
        else:
            db.active_sessions[attempt.test_id]["activeStudents"] += 1
            db.active_sessions[attempt.test_id]["lastActivity"] = current_time.isoformat()
        
        return {"status": "success", "message": "Test démarré avec succès"}
    except Exception as e:
        print(f"❌ Erreur lors du démarrage du test: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/test-tracking/progress")
async def update_progress(progress: TestProgress, token: str = Depends(verify_token)):
    """Mettre à jour le progrès d'un test"""
    try:
        print(f"📊 Mise à jour du progrès pour {progress.attempt_id}")
        
        if progress.attempt_id in db.test_attempts:
            db.test_attempts[progress.attempt_id].update({
                "questionsAnswered": progress.questions_answered,
                "totalQuestions": progress.total_questions,
                "timeSpent": progress.time_spent
            })
        
        return {"status": "success", "message": "Progrès mis à jour"}
    except Exception as e:
        print(f"❌ Erreur lors de la mise à jour du progrès: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/test-tracking/complete")
async def complete_test(completion: TestCompletion, token: str = Depends(verify_token)):
    """Terminer un test"""
    try:
        print(f"✅ Completion du test {completion.attempt_id}")
        
        if completion.attempt_id in db.test_attempts:
            attempt = db.test_attempts[completion.attempt_id]
            attempt.update({
                "status": "completed",
                "score": completion.score,
                "endTime": completion.end_time,
                "timeSpent": completion.time_spent,
                "questionsAnswered": completion.questions_answered,
                "totalQuestions": completion.total_questions
            })
            
            # Mettre à jour les performances de l'étudiant
            student_id = attempt["studentId"]
            if student_id in db.student_performances:
                student = db.student_performances[student_id]
                student["testsCompleted"] += 1
                student["lastTestDate"] = completion.end_time
                
                # Calculer le nouveau score moyen
                total_score = student["averageScore"] * (student["testsCompleted"] - 1) + completion.score
                student["averageScore"] = total_score / student["testsCompleted"]
                student["progressPercentage"] = student["averageScore"]
        
        return {"status": "success", "message": "Test terminé avec succès"}
    except Exception as e:
        print(f"❌ Erreur lors de la completion du test: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/test-tracking/abandon")
async def abandon_test(abandon: TestAbandon, token: str = Depends(verify_token)):
    """Abandonner un test"""
    try:
        print(f"❌ Abandon du test {abandon.attempt_id}")
        
        if abandon.attempt_id in db.test_attempts:
            db.test_attempts[abandon.attempt_id].update({
                "status": "abandoned",
                "endTime": abandon.end_time,
                "timeSpent": abandon.time_spent,
                "questionsAnswered": abandon.questions_answered,
                "totalQuestions": abandon.total_questions
            })
        
        return {"status": "success", "message": "Test abandonné"}
    except Exception as e:
        print(f"❌ Erreur lors de l'abandon du test: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Endpoints Analytics
@app.get("/api/v1/analytics/performance-metrics")
async def get_performance_metrics(token: str = Depends(verify_token)):
    """Récupérer les métriques de performance globales"""
    try:
        print("📊 Récupération des métriques de performance...")
        
        # Calculer les vraies métriques à partir des données
        total_students = len(db.student_performances)
        total_tests = sum(student["testsCompleted"] for student in db.student_performances.values())
        overall_score = sum(student["averageScore"] for student in db.student_performances.values()) / total_students if total_students > 0 else 0
        
        # Calculer le taux de completion (simulation basée sur les données existantes)
        completion_rate = 85.2  # Basé sur les données simulées
        
        # Calculer le pourcentage de tests difficiles
        difficult_tests = sum(1 for test in db.test_performances.values() if test["difficultyLevel"] >= 8)
        difficult_percentage = (difficult_tests / len(db.test_performances)) * 100 if db.test_performances else 0
        
        # Progrès hebdomadaire (simulation basée sur les données)
        weekly_progress = [
            {"week": "S1", "averageScore": 65, "testsCompleted": 15, "studentsActive": 20, "improvementRate": 2.5},
            {"week": "S2", "averageScore": 68, "testsCompleted": 18, "studentsActive": 22, "improvementRate": 4.6},
            {"week": "S3", "averageScore": 72, "testsCompleted": 20, "studentsActive": 24, "improvementRate": 5.9},
            {"week": "S4", "averageScore": 75, "testsCompleted": 22, "studentsActive": 24, "improvementRate": 4.2}
        ]
        
        # Statistiques mensuelles
        monthly_stats = [
            {"month": "Jan", "testsCreated": 12, "studentsActive": 18, "averageScore": 70},
            {"month": "Fév", "testsCreated": 15, "studentsActive": 20, "averageScore": 73},
            {"month": "Mar", "testsCreated": 18, "studentsActive": 22, "averageScore": 76},
            {"month": "Avr", "testsCreated": 20, "studentsActive": 24, "averageScore": 78}
        ]
        
        metrics = {
            "overallAverageScore": round(overall_score, 1),
            "totalTestsCompleted": total_tests,
            "totalStudents": total_students,
            "completionRate": completion_rate,
            "difficultTestsPercentage": round(difficult_percentage, 1),
            "weeklyProgress": weekly_progress,
            "monthlyStats": monthly_stats
        }
        
        print(f"✅ Métriques récupérées: {metrics}")
        return metrics
        
    except Exception as e:
        print(f"❌ Erreur lors de la récupération des métriques: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/analytics/student-performances")
async def get_student_performances(token: str = Depends(verify_token)):
    """Récupérer les performances des étudiants"""
    try:
        print("👥 Récupération des performances des étudiants...")
        
        # Convertir les données en format attendu par le frontend
        students = []
        for student_id, student_data in db.student_performances.items():
            students.append({
                "id": student_id,
                "name": student_data["name"],
                "email": student_data["email"],
                "testsCompleted": student_data["testsCompleted"],
                "averageScore": student_data["averageScore"],
                "progressPercentage": student_data["progressPercentage"],
                "lastTestDate": student_data["lastTestDate"],
                "improvementTrend": student_data["improvementTrend"]
            })
        
        print(f"✅ {len(students)} étudiants récupérés")
        return students
        
    except Exception as e:
        print(f"❌ Erreur lors de la récupération des étudiants: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/analytics/test-performances")
async def get_test_performances(token: str = Depends(verify_token)):
    """Récupérer les performances des tests"""
    try:
        print("📝 Récupération des performances des tests...")
        
        # Convertir les données en format attendu par le frontend
        tests = []
        for test_id, test_data in db.test_performances.items():
            tests.append({
                "id": test_id,
                "title": test_data["title"],
                "subject": test_data["subject"],
                "participants": test_data["participants"],
                "averageScore": test_data["averageScore"],
                "completionRate": test_data["completionRate"],
                "difficultyLevel": test_data["difficultyLevel"],
                "timeSpent": test_data["timeSpent"],
                "successRate": test_data["successRate"],
                "lastAttemptDate": test_data["lastAttemptDate"]
            })
        
        print(f"✅ {len(tests)} tests récupérés")
        return tests
        
    except Exception as e:
        print(f"❌ Erreur lors de la récupération des tests: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/analytics/real-time-data")
async def get_real_time_data(token: str = Depends(verify_token)):
    """Récupérer les données en temps réel"""
    try:
        print("🔄 Récupération des données en temps réel...")
        
        # Données en temps réel basées sur l'état actuel
        real_time_data = {
            "activeStudents": len(db.active_sessions),
            "ongoingTests": len([a for a in db.test_attempts.values() if a.get("status") == "in_progress"]),
            "completedToday": len([a for a in db.test_attempts.values() if a.get("status") == "completed"]),
            "systemHealth": {
                "status": "healthy",
                "responseTime": random.randint(50, 150),
                "uptime": "99.9%",
                "lastUpdate": datetime.now().isoformat()
            }
        }
        
        print(f"✅ Données temps réel récupérées: {real_time_data}")
        return real_time_data
        
    except Exception as e:
        print(f"❌ Erreur lors de la récupération des données temps réel: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/analytics/simulate-activity")
async def simulate_activity(token: str = Depends(verify_token)):
    """Simuler de l'activité en temps réel pour tester les analytics"""
    try:
        print("🎭 Simulation d'activité en temps réel...")
        
        # Simuler un nouveau test en cours
        import uuid
        new_attempt_id = str(uuid.uuid4())
        
        # Choisir un étudiant et un test aléatoirement
        student_id = random.choice(list(db.student_performances.keys()))
        test_id = random.choice(list(db.test_performances.keys()))
        
        # Créer une nouvelle tentative
        db.test_attempts[new_attempt_id] = {
            "attemptId": new_attempt_id,
            "testId": test_id,
            "studentId": student_id,
            "studentName": db.student_performances[student_id]["name"],
            "startTime": datetime.now().isoformat(),
            "status": "in_progress"
        }
        
        # Ajouter à la session active
        db.active_sessions[new_attempt_id] = {
            "student_id": student_id,
            "test_id": test_id,
            "start_time": datetime.now().isoformat()
        }
        
        print(f"✅ Activité simulée: Test {test_id} commencé par {db.student_performances[student_id]['name']}")
        
        return {
            "status": "success",
            "message": "Activité simulée avec succès",
            "new_attempt": db.test_attempts[new_attempt_id]
        }
        
    except Exception as e:
        print(f"❌ Erreur lors de la simulation: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint de santé
@app.get("/health")
async def health_check():
    """Vérifier la santé du serveur"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0",
        "database": "connected",
        "active_sessions": len(db.active_sessions),
        "total_attempts": len(db.test_attempts)
    }

# Endpoint racine
@app.get("/")
async def root():
    """Page d'accueil de l'API"""
    return {
        "message": "🚀 Najah AI Analytics Backend",
        "version": "1.0.0",
        "endpoints": {
            "analytics": "/api/v1/analytics/*",
            "test_tracking": "/api/v1/test-tracking/*",
            "remediation": "/api/v1/remediation/*",
            "health": "/health"
        },
        "documentation": "/docs"
    }

if __name__ == "__main__":
    print("🚀 Démarrage du serveur Najah AI Analytics...")
    print("📊 Endpoints disponibles:")
    print("   - Analytics: /api/v1/analytics/*")
    print("   - Test Tracking: /api/v1/test-tracking/*")
    print("   - Remediation: /api/v1/remediation/*")
    print("   - Santé: /health")
    print("   - Documentation: /docs")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
