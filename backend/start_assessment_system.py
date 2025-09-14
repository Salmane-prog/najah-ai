#!/usr/bin/env python3
"""
Script de démarrage rapide pour le système d'évaluation initiale
Démarre le serveur avec tous les composants nécessaires
"""

import uvicorn
import sys
import os

# Ajouter le répertoire courant au path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def start_assessment_system():
    """Démarrer le serveur avec le système d'évaluation initiale"""
    print("🚀 DÉMARRAGE DU SYSTÈME D'ÉVALUATION INITIALE")
    print("=" * 60)
    
    try:
        from fastapi import FastAPI
        from fastapi.middleware.cors import CORSMiddleware
        
        # Créer l'app FastAPI
        app = FastAPI(title="Najah AI - Système d'Évaluation Initiale", version="1.0.0")
        
        # Configuration CORS
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["http://localhost:3001", "http://localhost:3000"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        
        # Importer les routes essentielles
        print("✅ Import des routes...")
        
        # Routes de base
        from api.v1 import auth, users
        app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
        app.include_router(users.router, prefix="/api/v1/users", tags=["users"])
        
        # Routes d'évaluation
        from api.v1 import assessments
        app.include_router(assessments.router, prefix="/api/v1/assessments", tags=["assessments"])
        
        # Routes françaises optimisées
        from api.v1 import french_initial_assessment_optimized
        app.include_router(french_initial_assessment_optimized.router, prefix="/api/v1/french-optimized", tags=["french_optimized"])
        
        # Routes d'onboarding
        from api.v1 import student_onboarding
        app.include_router(student_onboarding.router, prefix="/api/v1/onboarding", tags=["student_onboarding"])
        
        # Routes d'analytics
        from api.v1 import analytics
        app.include_router(analytics.router, prefix="/api/v1/analytics", tags=["analytics"])
        
        # Routes de quiz
        from api.v1 import quizzes, quiz_results
        app.include_router(quizzes.router, prefix="/api/v1/quizzes", tags=["quizzes"])
        app.include_router(quiz_results.router, prefix="/api/v1/quiz_results", tags=["quiz_results"])
        
        # Routes de base de données
        from api.v1 import class_groups, contents, learning_paths
        app.include_router(class_groups.router, prefix="/api/v1/class_groups", tags=["class_groups"])
        app.include_router(contents.router, prefix="/api/v1/contents", tags=["contents"])
        app.include_router(learning_paths.router, prefix="/api/v1/learning_paths", tags=["learning_paths"])
        
        # Routes de gamification
        from api.v1 import badges, gamification
        app.include_router(badges.router, prefix="/api/v1/badges", tags=["badges"])
        app.include_router(gamification.router, prefix="/api/v1/gamification", tags=["gamification"])
        
        # Routes de messagerie
        from api.v1 import messages, notifications
        app.include_router(messages.router, prefix="/api/v1/messages", tags=["messages"])
        app.include_router(notifications.router, prefix="/api/v1/notifications", tags=["notifications"])
        
        # Route de test
        @app.get("/")
        def read_root():
            return {
                "message": "Najah AI - Système d'Évaluation Initiale",
                "version": "1.0.0",
                "status": "running",
                "endpoints": {
                    "auth": "/api/v1/auth",
                    "users": "/api/v1/users",
                    "assessments": "/api/v1/assessments",
                    "french_optimized": "/api/v1/french-optimized",
                    "onboarding": "/api/v1/onboarding",
                    "analytics": "/api/v1/analytics"
                }
            }
        
        @app.get("/health")
        def health_check():
            return {"status": "healthy", "message": "Serveur opérationnel"}
        
        @app.get("/test-assessment")
        def test_assessment_endpoint():
            return {
                "message": "Endpoint de test pour l'évaluation initiale",
                "status": "ready",
                "features": [
                    "Évaluation automatique à la connexion",
                    "20 questions exactes (7-6-7)",
                    "Génération automatique du profil",
                    "Système d'onboarding intelligent"
                ]
            }
        
        print("✅ Application FastAPI créée avec succès")
        print("✅ Routes d'évaluation initiale incluses")
        print("✅ Système d'onboarding configuré")
        print("✅ CORS configuré")
        
        # Afficher les informations de démarrage
        print("\n🚀 DÉMARRAGE DU SERVEUR...")
        print("   URL: http://localhost:8000")
        print("   Health check: http://localhost:8000/health")
        print("   Test évaluation: http://localhost:8000/test-assessment")
        print("   API docs: http://localhost:8000/docs")
        print("   Frontend: http://localhost:3001")
        print("\n   Appuyez sur Ctrl+C pour arrêter")
        
        # Configuration uvicorn
        uvicorn.run(
            app,
            host="127.0.0.1",
            port=8000,
            reload=True,  # Activer le reload pour le développement
            log_level="info"
        )
        
    except Exception as e:
        print(f"❌ Erreur lors du démarrage: {e}")
        print("Détails de l'erreur:")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    start_assessment_system()





