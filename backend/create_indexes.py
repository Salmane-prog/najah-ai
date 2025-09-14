#!/usr/bin/env python3
"""
Script pour créer les index sur les nouvelles tables d'évaluation adaptative, analytics et IA
"""

import sqlite3
from pathlib import Path

def create_indexes():
    """Créer les index sur les nouvelles tables"""
    
    # Chemin vers la base de données
    db_path = Path("../data/app.db")
    
    # Vérifier si la base de données existe
    if not db_path.exists():
        print(f"❌ Base de données non trouvée: {db_path}")
        return False
    
    print(f"🔍 Connexion à la base de données: {db_path}")
    
    # Connexion à la base de données
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print("🔍 Création des index pour les nouvelles tables...")
    
    try:
        # Index pour l'évaluation adaptative
        print("📊 Création des index pour l'évaluation adaptative...")
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_adaptive_tests_subject ON adaptive_tests(subject)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_adaptive_questions_test_id ON adaptive_questions(test_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_student_adaptive_tests_student_id ON student_adaptive_tests(student_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_student_answers_student_test_id ON student_answers(student_test_id)')
        print("  ✅ Index pour l'évaluation adaptative créés")
        
        # Index pour l'analytics
        print("📈 Création des index pour l'analytics...")
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_learning_analytics_student_date ON learning_analytics(student_id, date)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_predictive_models_type ON predictive_models(model_type)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_student_predictions_student_model ON student_predictions(student_id, model_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_learning_patterns_student_type ON learning_patterns(student_id, pattern_type)')
        print("  ✅ Index pour l'analytics créés")
        
        # Index pour l'IA
        print("🤖 Création des index pour l'IA...")
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_ai_models_type ON ai_models(model_type)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_model_training_sessions_model_id ON model_training_sessions(model_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_model_predictions_model_id ON model_predictions(model_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_data_collection_student_type ON data_collection(student_id, data_type)')
        print("  ✅ Index pour l'IA créés")
        
        # Valider et fermer
        conn.commit()
        conn.close()
        
        print("✅ Tous les index ont été créés avec succès !")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la création des index : {e}")
        conn.rollback()
        conn.close()
        import traceback
        traceback.print_exc()
        return False

def verify_tables():
    """Vérifier que toutes les tables existent"""
    
    db_path = Path("../data/app.db")
    if not db_path.exists():
        print(f"❌ Base de données non trouvée: {db_path}")
        return False
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Liste des tables attendues
    expected_tables = [
        'adaptive_tests', 'adaptive_questions', 'student_adaptive_tests', 'student_answers',
        'formative_assessments', 'student_formative_assessments', 'self_assessments',
        'learning_analytics', 'predictive_models', 'student_predictions', 'learning_patterns',
        'blockage_detection', 'teacher_dashboards', 'parent_dashboards', 'automated_reports',
        'report_recipients', 'ai_models', 'model_training_sessions', 'model_predictions',
        'model_deployments', 'data_collection', 'learning_pattern_analysis', 'continuous_improvement'
    ]
    
    print("🔍 Vérification des tables...")
    
    # Récupérer toutes les tables existantes
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    existing_tables = [row[0] for row in cursor.fetchall()]
    
    missing_tables = []
    for table in expected_tables:
        if table in existing_tables:
            print(f"  ✅ {table}")
        else:
            print(f"  ❌ {table} - MANQUANTE")
            missing_tables.append(table)
    
    conn.close()
    
    if missing_tables:
        print(f"\n⚠️  {len(missing_tables)} tables manquantes : {missing_tables}")
        return False
    else:
        print(f"\n✅ Toutes les {len(expected_tables)} tables sont présentes !")
        return True

if __name__ == "__main__":
    print("🚀 Script de création des index")
    print("=" * 50)
    
    # D'abord vérifier que toutes les tables existent
    if verify_tables():
        # Ensuite créer les index
        success = create_indexes()
        if success:
            print("\n🎉 Index créés avec succès !")
            print("💡 Les nouvelles fonctionnalités sont maintenant optimisées")
        else:
            print("\n❌ Erreur lors de la création des index")
    else:
        print("\n❌ Impossible de créer les index - tables manquantes")
        print("💡 Exécutez d'abord create_new_tables.py")





