#!/usr/bin/env python3
"""
Script pour tester les routes assessment
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_assessment_routes():
    print("=== TEST DES ROUTES ASSESSMENT ===")
    
    try:
        from fastapi import FastAPI
        from api.v1 import assessment
        
        # Créer l'app FastAPI
        app = FastAPI()
        
        # Ajouter les routes assessment
        app.include_router(assessment.router, prefix="/api/v1/assessment", tags=["assessment"])
        
        print("✅ Application créée")
        print("✅ Routes assessment incluses")
        
        # Lister toutes les routes
        routes = []
        for route in app.routes:
            if hasattr(route, 'path'):
                routes.append(f"{route.methods} {route.path}")
        
        print(f"\n📋 Routes disponibles ({len(routes)}):")
        for route in routes:
            print(f"  - {route}")
        
        # Vérifier si l'endpoint spécifique existe
        target_route = "GET /api/v1/assessment/student/{student_id}/start"
        if any(target_route in route for route in routes):
            print(f"\n✅ Endpoint trouvé: {target_route}")
        else:
            print(f"\n❌ Endpoint manquant: {target_route}")
        
        print("\n✅ Test terminé")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_assessment_routes() 