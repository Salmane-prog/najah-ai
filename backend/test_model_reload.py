#!/usr/bin/env python3
"""
Script pour tester le rechargement du modèle AdaptiveTest
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine, text
from models.adaptive_evaluation import AdaptiveTest
from models.user import User

def test_model_reload():
    """Tester le rechargement du modèle"""
    try:
        print("🔧 Test de rechargement du modèle AdaptiveTest...")
        print("=" * 50)
        
        # Créer une connexion directe
        engine = create_engine("sqlite:///./data/app.db")
        
        # Test 1: Vérifier la structure de la table
        print("📋 Test 1: Structure de la table...")
        with engine.connect() as conn:
            result = conn.execute(text("PRAGMA table_info(adaptive_tests)"))
            columns = result.fetchall()
            print(f"Colonnes trouvées: {len(columns)}")
            for col in columns:
                print(f"  - {col[1]} ({col[2]})")
        
        # Test 2: Vérifier si le modèle peut être instancié
        print("\n📋 Test 2: Instanciation du modèle...")
        try:
            # Créer une instance vide pour tester
            test_instance = AdaptiveTest()
            print("✅ Modèle instancié avec succès")
            
            # Vérifier les attributs
            print(f"  - created_by: {hasattr(test_instance, 'created_by')}")
            print(f"  - difficulty_range: {hasattr(test_instance, 'difficulty_range')}")
            print(f"  - question_pool_size: {hasattr(test_instance, 'question_pool_size')}")
            print(f"  - adaptation_algorithm: {hasattr(test_instance, 'adaptation_algorithm')}")
            
        except Exception as e:
            print(f"❌ Erreur lors de l'instanciation: {e}")
        
        # Test 3: Vérifier les données existantes
        print("\n📋 Test 3: Données existantes...")
        with engine.connect() as conn:
            result = conn.execute(text("SELECT COUNT(*) FROM adaptive_tests"))
            count = result.fetchone()[0]
            print(f"Nombre de tests: {count}")
            
            if count > 0:
                result = conn.execute(text("SELECT id, title, created_by FROM adaptive_tests LIMIT 3"))
                tests = result.fetchall()
                print("Exemples de tests:")
                for test in tests:
                    print(f"  - ID: {test[0]}, Titre: {test[1]}, Créé par: {test[2]}")
        
        print("\n" + "=" * 50)
        print("✅ Test terminé")
        
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_model_reload()




















