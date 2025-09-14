#!/usr/bin/env python3
"""
Script pour démarrer le serveur avec une configuration propre
"""

import uvicorn
import sys
import os

# Ajouter le répertoire courant au path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def start_clean():
    print("=== DÉMARRAGE PROPRE DU SERVEUR ===")
    
    try:
        from fastapi import FastAPI
        from fastapi.middleware.cors import CORSMiddleware
        
        # Créer l'app FastAPI
        app = FastAPI(title="Najah AI API", version="1.0.0")
        
        # Configuration CORS
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["http://localhost:3001"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        
        # Importer les routes essentielles seulement
        print("✅ Import des routes...")
        
        # Routes de base
        from api.v1 import auth
        app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
        
        # Routes utilisateurs
        from api.v1 import users
        app.include_router(users.router, prefix="/api/v1/users", tags=["users"])
        
        # Routes quiz
        from api.v1 import quiz_results, quizzes
        app.include_router(quiz_results.router, prefix="/api/v1/quiz_results", tags=["quiz_results"])
        app.include_router(quizzes.router, prefix="/api/v1/quizzes", tags=["quizzes"])
        
        # Routes badges
        from api.v1 import badges
        app.include_router(badges.router, prefix="/api/v1/badges", tags=["badges"])
        
        # Routes messages
        from api.v1 import messages
        app.include_router(messages.router, prefix="/api/v1/messages", tags=["messages"])
        
        # Routes learning history
        from api.v1 import learning_history
        app.include_router(learning_history.router, prefix="/api/v1/learning_history", tags=["learning_history"])
        
        # Routes AI (sans Content)
        from api.v1 import ai
        app.include_router(ai.router, prefix="/api/v1/ai", tags=["ai"])
        
        # Routes analytics
        from api.v1 import analytics
        app.include_router(analytics.router, prefix="/api/v1/analytics", tags=["analytics"])
        
        # Routes assessment
        from api.v1 import assessment
        app.include_router(assessment.router, prefix="/api/v1/assessment", tags=["assessment"])
        
        # Route de test
        @app.get("/")
        def read_root():
            return {"message": "Najah AI API - Configuration propre"}
        
        @app.get("/health")
        def health_check():
            return {"status": "healthy", "message": "Serveur opérationnel"}
        
        print("✅ Application FastAPI créée avec succès")
        print("✅ Routes essentielles incluses")
        print("✅ CORS configuré")
        
        # Démarrer le serveur
        print("\n🚀 Démarrage du serveur...")
        print("   URL: http://localhost:8000")
        print("   Health check: http://localhost:8000/health")
        print("   Appuyez sur Ctrl+C pour arrêter")
        
        # Configuration uvicorn sans reload pour éviter l'avertissement
        uvicorn.run(
            app,
            host="127.0.0.1",
            port=8000,
            reload=False,  # Désactivé pour éviter l'avertissement
            log_level="info"
        )
        
    except Exception as e:
        print(f"❌ Erreur lors du démarrage: {e}")
        print("Détails de l'erreur:")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    start_clean() 