#!/usr/bin/env python3
"""
Script pour initialiser directement les tables d'évaluation
Contourne les problèmes Alembic
"""
import sqlite3
import os
import sys

# Ajouter le répertoire parent au path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def init_assessment_tables_direct():
    # Chemin vers la base de données
    db_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'app.db')
    
    if not os.path.exists(db_path):
        print(f"❌ Base de données non trouvée: {db_path}")
        return False
    
    print(f"🔍 Initialisation directe des tables d'évaluation...")
    print(f"   Base de données: {db_path}")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Vérifier les tables existantes
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        existing_tables = [row[0] for row in cursor.fetchall()]
        print(f"📋 Tables existantes: {existing_tables}")
        
        # Créer la table assessments si elle n'existe pas
        if 'assessments' not in existing_tables:
            cursor.execute("""
                CREATE TABLE assessments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    student_id INTEGER NOT NULL,
                    assessment_type VARCHAR NOT NULL,
                    title VARCHAR NOT NULL,
                    description TEXT,
                    status VARCHAR DEFAULT 'in_progress',
                    started_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    completed_at DATETIME,
                    FOREIGN KEY (student_id) REFERENCES users (id)
                )
            """)
            print("✅ Table 'assessments' créée")
        else:
            print("✅ Table 'assessments' existe déjà")
        
        # Créer la table assessment_questions si elle n'existe pas
        if 'assessment_questions' not in existing_tables:
            cursor.execute("""
                CREATE TABLE assessment_questions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    assessment_id INTEGER NOT NULL,
                    question_text TEXT NOT NULL,
                    question_type VARCHAR NOT NULL,
                    subject VARCHAR NOT NULL,
                    difficulty VARCHAR NOT NULL,
                    options TEXT,
                    correct_answer VARCHAR NOT NULL,
                    points REAL DEFAULT 1.0,
                    "order" INTEGER DEFAULT 0,
                    FOREIGN KEY (assessment_id) REFERENCES assessments (id)
                )
            """)
            print("✅ Table 'assessment_questions' créée")
        else:
            print("✅ Table 'assessment_questions' existe déjà")
        
        # Créer la table assessment_results si elle n'existe pas
        if 'assessment_results' not in existing_tables:
            cursor.execute("""
                CREATE TABLE assessment_results (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    assessment_id INTEGER NOT NULL,
                    student_id INTEGER NOT NULL,
                    total_score REAL NOT NULL,
                    max_score REAL NOT NULL,
                    percentage REAL NOT NULL,
                    subject_scores TEXT,
                    difficulty_scores TEXT,
                    completed_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (assessment_id) REFERENCES assessments (id),
                    FOREIGN KEY (student_id) REFERENCES users (id)
                )
            """)
            print("✅ Table 'assessment_results' créée")
        else:
            print("✅ Table 'assessment_results' existe déjà")
        
        # Créer les index
        cursor.execute("CREATE INDEX IF NOT EXISTS ix_assessments_id ON assessments (id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS ix_assessment_questions_id ON assessment_questions (id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS ix_assessment_results_id ON assessment_results (id)")
        print("✅ Index créés")
        
        conn.commit()
        
        # Vérifier les tables créées
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'assessment%'")
        assessment_tables = [row[0] for row in cursor.fetchall()]
        print(f"📋 Tables d'évaluation disponibles: {assessment_tables}")
        
        # Vérifier la structure des tables
        for table in assessment_tables:
            cursor.execute(f"PRAGMA table_info({table})")
            columns = cursor.fetchall()
            print(f"   {table}: {len(columns)} colonnes")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de l'initialisation: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()

def test_assessment_api():
    """Test simple de l'API d'évaluation"""
    try:
        import requests
        import json
        
        # Test de l'API
        base_url = "http://localhost:8000"
        
        # Test de connexion
        try:
            response = requests.get(f"{base_url}/docs")
            if response.status_code == 200:
                print("✅ API backend accessible")
            else:
                print("⚠️ API backend non accessible")
                return False
        except:
            print("⚠️ Serveur backend non démarré")
            print("   Démarrez avec: python app.py")
            return False
        
        return True
        
    except ImportError:
        print("⚠️ Module 'requests' non installé")
        print("   Installez avec: pip install requests")
        return False

if __name__ == "__main__":
    print("🚀 Initialisation directe des tables d'évaluation...")
    print("=" * 50)
    
    # Étape 1: Initialiser les tables
    success = init_assessment_tables_direct()
    
    if success:
        print("\n✅ Tables d'évaluation initialisées avec succès!")
        
        # Étape 2: Tester l'API
        print("\n🧪 Test de l'API d'évaluation...")
        api_ok = test_assessment_api()
        
        if api_ok:
            print("\n🎉 Tout est prêt pour tester l'évaluation!")
            print("\n📋 Prochaines étapes:")
            print("1. Démarrez le serveur backend: python app.py")
            print("2. Démarrez le frontend: cd frontend && npm run dev")
            print("3. Testez l'évaluation: http://localhost:3000")
        else:
            print("\n⚠️ API non accessible. Démarrez le serveur backend.")
    else:
        print("\n❌ Erreur lors de l'initialisation.")
        print("   Vérifiez les permissions de la base de données.") 