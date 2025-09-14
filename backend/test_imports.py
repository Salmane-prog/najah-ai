#!/usr/bin/env python3
"""
Script simple pour tester les imports
"""

print("🧪 Test des imports...")

try:
    print("1️⃣ Test import assessments...")
    from api.v1 import assessments
    print("   ✅ Assessments importé avec succès")
    
    print("2️⃣ Test import student_learning_paths...")
    from api.v1 import student_learning_paths
    print("   ✅ StudentLearningPaths importé avec succès")
    
    print("3️⃣ Test import app...")
    from app import fastapi_app
    print("   ✅ App importé avec succès")
    
    print("\n🎉 TOUS LES IMPORTS FONCTIONNENT !")
    print("Votre serveur peut maintenant démarrer.")
    
except Exception as e:
    print(f"\n❌ Erreur d'import: {e}")
    import traceback
    traceback.print_exc()







