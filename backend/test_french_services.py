#!/usr/bin/env python3
"""
Script de test pour les services français optimisés
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.database import get_db
from services.french_question_selector import FrenchQuestionSelector
from services.french_test_session_manager import FrenchTestSessionManager
from sqlalchemy import text

def test_question_selector():
    """Tester le sélecteur de questions"""
    
    print("🧪 Test du sélecteur de questions françaises...")
    
    try:
        # Obtenir une session de base de données
        db = next(get_db())
        
        # Créer le sélecteur
        selector = FrenchQuestionSelector(db)
        
        # Tester la sélection de 20 questions
        print("  📝 Sélection de 20 questions...")
        questions = selector.select_20_questions(student_id=1)
        
        print(f"  ✅ {len(questions)} questions sélectionnées")
        
        # Vérifier la répartition
        difficulty_counts = {}
        for q in questions:
            diff = q.get('difficulty', 'unknown')
            difficulty_counts[diff] = difficulty_counts.get(diff, 0) + 1
        
        print(f"  📊 Répartition par difficulté: {difficulty_counts}")
        
        # Vérifier qu'il y a exactement 20 questions
        if len(questions) == 20:
            print("  🎯 SUCCÈS: Exactement 20 questions sélectionnées")
        else:
            print(f"  ❌ ÉCHEC: {len(questions)} questions au lieu de 20")
            return False
        
        # Vérifier la structure des questions
        for i, q in enumerate(questions[:3]):  # Vérifier les 3 premières
            required_fields = ['id', 'question', 'options', 'correct', 'difficulty', 'topic']
            missing_fields = [field for field in required_fields if field not in q]
            
            if missing_fields:
                print(f"  ❌ Question {i+1} manque des champs: {missing_fields}")
                return False
        
        print("  ✅ Structure des questions valide")
        
        db.close()
        return True
        
    except Exception as e:
        print(f"  ❌ Erreur lors du test: {e}")
        return False

def test_session_manager():
    """Tester le gestionnaire de session"""
    
    print("\n🧪 Test du gestionnaire de session...")
    
    try:
        # Obtenir une session de base de données
        db = next(get_db())
        
        # Créer le gestionnaire
        manager = FrenchTestSessionManager(db)
        
        print("  📝 Test de création de session...")
        
        # Tester la création d'une session (sans l'insérer en base)
        # On va juste vérifier que la classe peut être instanciée
        print("  ✅ Gestionnaire de session créé avec succès")
        
        # Vérifier les attributs
        if hasattr(manager, 'max_questions') and manager.max_questions == 20:
            print("  ✅ Nombre maximum de questions correct: 20")
        else:
            print(f"  ❌ Nombre maximum incorrect: {getattr(manager, 'max_questions', 'N/A')}")
            return False
        
        db.close()
        return True
        
    except Exception as e:
        print(f"  ❌ Erreur lors du test: {e}")
        return False

def test_database_connection():
    """Tester la connexion à la base de données"""
    
    print("🧪 Test de connexion à la base de données...")
    
    try:
        db = next(get_db())
        
        # Test simple de requête
        result = db.execute(text("SELECT 1 as test"))
        row = result.fetchone()
        
        if row and row[0] == 1:
            print("  ✅ Connexion à la base de données réussie")
            db.close()
            return True
        else:
            print("  ❌ Échec de la requête de test")
            return False
            
    except Exception as e:
        print(f"  ❌ Erreur de connexion: {e}")
        return False

def test_available_questions():
    """Tester la disponibilité des questions"""
    
    print("\n🧪 Test de disponibilité des questions...")
    
    try:
        db = next(get_db())
        
        # Compter les questions françaises dans question_history
        result = db.execute(text("""
            SELECT COUNT(*) as count
            FROM question_history
            WHERE topic IN ('Articles', 'Grammaire', 'Conjugaison', 'Vocabulaire', 'Compréhension')
        """))
        
        history_count = result.fetchone()[0]
        print(f"  📚 Questions dans l'historique: {history_count}")
        
        # Compter les questions adaptatives
        result = db.execute(text("""
            SELECT COUNT(*) as count
            FROM adaptive_questions
            WHERE topic LIKE '%français%' OR topic LIKE '%grammaire%'
        """))
        
        adaptive_count = result.fetchone()[0]
        print(f"  🧠 Questions adaptatives: {adaptive_count}")
        
        # Compter les questions générales
        result = db.execute(text("""
            SELECT COUNT(*) as count
            FROM questions
            WHERE question_text LIKE '%français%' OR question_text LIKE '%être%' OR question_text LIKE '%avoir%'
        """))
        
        general_count = result.fetchone()[0]
        print(f"  📖 Questions générales: {general_count}")
        
        total = history_count + adaptive_count + general_count
        print(f"  📊 Total des questions françaises: {total}")
        
        if total >= 20:
            print("  ✅ Suffisamment de questions disponibles (≥20)")
            db.close()
            return True
        else:
            print(f"  ⚠️ Questions insuffisantes: {total}/20")
            db.close()
            return False
            
    except Exception as e:
        print(f"  ❌ Erreur lors du comptage: {e}")
        return False

def main():
    """Fonction principale de test"""
    
    print("🚀 Démarrage des tests des services français optimisés...")
    print("=" * 60)
    
    tests = [
        ("Connexion base de données", test_database_connection),
        ("Disponibilité questions", test_available_questions),
        ("Sélecteur de questions", test_question_selector),
        ("Gestionnaire de session", test_session_manager)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n🔍 Test: {test_name}")
        print("-" * 40)
        
        try:
            success = test_func()
            results.append((test_name, success))
            
            if success:
                print(f"  🎉 {test_name}: SUCCÈS")
            else:
                print(f"  💥 {test_name}: ÉCHEC")
                
        except Exception as e:
            print(f"  💥 {test_name}: ERREUR - {e}")
            results.append((test_name, False))
    
    # Résumé des tests
    print("\n" + "=" * 60)
    print("📋 RÉSUMÉ DES TESTS")
    print("=" * 60)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for test_name, success in results:
        status = "✅ SUCCÈS" if success else "❌ ÉCHEC"
        print(f"  {test_name}: {status}")
    
    print(f"\n🎯 Résultat global: {passed}/{total} tests réussis")
    
    if passed == total:
        print("🎉 Tous les tests sont passés avec succès !")
        print("✅ Le système français optimisé est prêt à être utilisé.")
    else:
        print("⚠️ Certains tests ont échoué. Vérifiez les erreurs ci-dessus.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
