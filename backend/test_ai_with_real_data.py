import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ai_prediction_service import AIPredictionService
from database_service import DatabaseService

def test_ai_with_real_data():
    print("🧠 Test de l'IA avec de vraies données...")
    
    try:
        # Initialiser les services
        ai_service = AIPredictionService()
        db_service = DatabaseService()
        
        # Test 1: Récupérer l'historique d'un étudiant
        print("\n📊 Test 1: Récupération de l'historique étudiant 1")
        history = db_service.get_student_learning_history(1, days=90)
        print(f"  ✅ Historique récupéré: {len(history)} enregistrements")
        
        if history:
            print("  📋 Exemples d'historique:")
            for i, record in enumerate(history[:3]):
                print(f"    {i+1}. Score: {record['score']}%, Matière: {record['subject']}, Date: {record['created_at']}")
        
        # Test 2: Prédiction IA avec vraies données
        print("\n🔮 Test 2: Prédiction IA pour étudiant 1")
        prediction = ai_service.predict_student_performance(1, days_ahead=30)
        
        if "error" not in prediction:
            print(f"  ✅ Prédiction réussie!")
            print(f"  📈 Score actuel moyen: {prediction['current_average']}%")
            print(f"  🔮 Score prédit: {prediction['predicted_score']}%")
            print(f"  📊 Confiance: {prediction['confidence_level']}%")
            print(f"  📈 Tendance: {prediction['trend_analysis']['trend']}")
            print(f"  💡 Recommandations: {prediction['recommendations']}")
        else:
            print(f"  ❌ Erreur de prédiction: {prediction['error']}")
        
        # Test 3: Prédiction pour étudiant 2
        print("\n🔮 Test 3: Prédiction IA pour étudiant 2")
        prediction2 = ai_service.predict_student_performance(2, days_ahead=30)
        
        if "error" not in prediction2:
            print(f"  ✅ Prédiction réussie!")
            print(f"  📈 Score actuel moyen: {prediction2['current_average']}%")
            print(f"  🔮 Score prédit: {prediction2['predicted_score']}%")
            print(f"  📊 Confiance: {prediction2['confidence_level']}%")
        else:
            print(f"  ❌ Erreur de prédiction: {prediction2['error']}")
        
        print("\n🎉 Test terminé!")
        
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_ai_with_real_data()
