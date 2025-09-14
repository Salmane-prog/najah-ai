from fastapi import APIRouter
from api.v1 import remediation, adaptive_evaluation, french_initial_assessment_optimized, progress_tracking, quiz_results, monitoring

# Router principal de l'API
api_router = APIRouter(prefix="/api/v1")

# Inclure tous les routers
api_router.include_router(remediation.router, prefix="/remediation", tags=["remediation"])
api_router.include_router(adaptive_evaluation.router, prefix="/adaptive-evaluation", tags=["adaptive-evaluation"])
api_router.include_router(french_initial_assessment_optimized.router, prefix="/french-optimized", tags=["french-optimized"])
api_router.include_router(progress_tracking.router, prefix="/progress", tags=["progress"])
api_router.include_router(quiz_results.router, prefix="/quiz-results", tags=["quiz-results"])
api_router.include_router(monitoring.router, prefix="/monitoring", tags=["monitoring"])
