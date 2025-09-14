#!/usr/bin/env python3
"""
Script pour tester l'enregistrement du router teacher_adaptive_evaluation
"""

from fastapi import FastAPI
from api.v1 import teacher_adaptive_evaluation

def test_router_registration():
    """Tester l'enregistrement du router"""
    print("🔍 Test de l'enregistrement du router...")
    print("=" * 50)
    
    # Test 1: Vérifier que le router existe
    print("\n1️⃣ Vérification du router...")
    try:
        router = teacher_adaptive_evaluation.router
        print(f"   ✅ Router trouvé: {router}")
        print(f"   - Prefix: {router.prefix}")
        print(f"   - Tags: {router.tags}")
        print(f"   - Routes: {len(router.routes)}")
        
        # Lister les routes
        for route in router.routes:
            print(f"     - {route.methods} {route.path}")
            
    except Exception as e:
        print(f"   ❌ Erreur lors de l'accès au router: {e}")
        return
    
    # Test 2: Créer une app FastAPI et enregistrer le router
    print("\n2️⃣ Test d'enregistrement dans FastAPI...")
    try:
        app = FastAPI()
        app.include_router(router, prefix="/api/v1/teacher-adaptive-evaluation", tags=["teacher_adaptive_evaluation"])
        print("   ✅ Router enregistré avec succès dans FastAPI")
        
        # Vérifier les routes enregistrées
        routes = app.routes
        teacher_routes = [r for r in routes if hasattr(r, 'path') and 'teacher-adaptive-evaluation' in str(r.path)]
        print(f"   - Routes enregistrées: {len(teacher_routes)}")
        
        for route in teacher_routes:
            print(f"     - {route.path}")
            
    except Exception as e:
        print(f"   ❌ Erreur lors de l'enregistrement: {e}")
    
    print("\n" + "=" * 50)
    print("📋 Résumé:")
    print("   - Si le router est trouvé mais pas enregistré: Problème d'import")
    print("   - Si l'enregistrement échoue: Problème de configuration")

if __name__ == "__main__":
    test_router_registration()
