#!/usr/bin/env python3
"""
🔧 SCRIPT DE RÉPARATION DE LA BASE DE DONNÉES
Corrige les problèmes de colonnes et de structure des tables
"""

import sys
import os
from pathlib import Path

# Ajouter le répertoire parent au path
sys.path.append(str(Path(__file__).parent))

from core.database import get_db, engine
from sqlalchemy import text

def fix_database():
    """Réparer la base de données"""
    
    print("🔧 RÉPARATION DE LA BASE DE DONNÉES")
    print("=" * 50)
    
    try:
        db = next(get_db())
        
        print("\n📊 Vérification des tables existantes...")
        
        # Vérifier si la table french_adaptive_tests existe
        result = db.execute(text("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='french_adaptive_tests'
        """))
        
        if result.fetchone():
            print("✅ Table french_adaptive_tests trouvée")
            
            # Vérifier la structure de la table
            result = db.execute(text("PRAGMA table_info(french_adaptive_tests)"))
            columns = [row[1] for row in result.fetchall()]
            print(f"   📋 Colonnes actuelles: {', '.join(columns)}")
            
            # Vérifier si current_question_order existe
            if 'current_question_order' in columns:
                print("⚠️  Colonne 'current_question_order' trouvée - suppression en cours...")
                
                # Créer une nouvelle table avec la bonne structure
                db.execute(text("""
                    CREATE TABLE french_adaptive_tests_new (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        student_id INTEGER NOT NULL,
                        test_type VARCHAR NOT NULL,
                        current_question_index INTEGER DEFAULT 1,
                        total_questions INTEGER,
                        current_difficulty VARCHAR NOT NULL,
                        status VARCHAR DEFAULT 'in_progress',
                        started_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                        completed_at DATETIME,
                        final_score FLOAT,
                        difficulty_progression TEXT,
                        level_progression VARCHAR DEFAULT 'A1',
                        current_level VARCHAR DEFAULT 'A1',
                        questions_sequence TEXT
                    )
                """))
                
                # Copier les données existantes
                db.execute(text("""
                    INSERT INTO french_adaptive_tests_new 
                    SELECT id, student_id, test_type, 
                           COALESCE(current_question_index, 1) as current_question_index,
                           total_questions, current_difficulty, status, started_at,
                           completed_at, final_score, difficulty_progression,
                           level_progression, current_level, questions_sequence
                    FROM french_adaptive_tests
                """))
                
                # Supprimer l'ancienne table
                db.execute(text("DROP TABLE french_adaptive_tests"))
                
                # Renommer la nouvelle table
                db.execute(text("ALTER TABLE french_adaptive_tests_new RENAME TO french_adaptive_tests"))
                
                db.commit()
                print("✅ Table french_adaptive_tests réparée")
                
            else:
                print("✅ Structure de la table correcte")
                
        else:
            print("ℹ️  Table french_adaptive_tests n'existe pas - création...")
            create_french_tables(db)
        
        # Vérifier les autres tables
        print("\n📊 Vérification des autres tables...")
        
        # Table french_test_answers
        result = db.execute(text("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='french_test_answers'
        """))
        
        if not result.fetchone():
            print("ℹ️  Table french_test_answers n'existe pas - création...")
            create_answer_table(db)
        else:
            print("✅ Table french_test_answers trouvée")
        
        # Table french_learning_profiles
        result = db.execute(text("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='french_learning_profiles'
        """))
        
        if not result.fetchone():
            print("ℹ️  Table french_learning_profiles n'existe pas - création...")
            create_profile_table(db)
        else:
            print("✅ Table french_learning_profiles trouvée")
        
        # Table assessment_questions
        result = db.execute(text("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='assessment_questions'
        """))
        
        if not result.fetchone():
            print("ℹ️  Table assessment_questions n'existe pas - création...")
            create_assessment_questions_table(db)
        else:
            print("✅ Table assessment_questions trouvée")
        
        print("\n" + "=" * 50)
        print("🎉 RÉPARATION TERMINÉE AVEC SUCCÈS !")
        print("✅ Toutes les tables sont maintenant correctement configurées")
        print("✅ Le système d'évaluation peut maintenant fonctionner")
        
        return True
        
    except Exception as e:
        print(f"\n❌ ERREUR LORS DE LA RÉPARATION: {e}")
        import traceback
        traceback.print_exc()
        return False
        
    finally:
        if 'db' in locals():
            db.close()

def create_french_tables(db):
    """Créer les tables françaises avec la bonne structure"""
    
    # Table des tests français
    db.execute(text("""
        CREATE TABLE french_adaptive_tests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            test_type VARCHAR NOT NULL,
            current_question_index INTEGER DEFAULT 1,
            total_questions INTEGER,
            current_difficulty VARCHAR NOT NULL,
            status VARCHAR DEFAULT 'in_progress',
            started_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            completed_at DATETIME,
            final_score FLOAT,
            difficulty_progression TEXT,
            level_progression VARCHAR DEFAULT 'A1',
            current_level VARCHAR DEFAULT 'A1',
            questions_sequence TEXT
        )
    """))
    
    print("✅ Table french_adaptive_tests créée")

def create_answer_table(db):
    """Créer la table des réponses"""
    
    db.execute(text("""
        CREATE TABLE french_test_answers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            test_id INTEGER NOT NULL,
            student_id INTEGER NOT NULL,
            question_id INTEGER NOT NULL,
            answer TEXT NOT NULL,
            is_correct BOOLEAN NOT NULL,
            score INTEGER NOT NULL,
            answered_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """))
    
    print("✅ Table french_test_answers créée")

def create_profile_table(db):
    """Créer la table des profils"""
    
    db.execute(text("""
        CREATE TABLE french_learning_profiles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL UNIQUE,
            french_level VARCHAR,
            learning_style VARCHAR,
            preferred_pace VARCHAR,
            strengths TEXT,
            weaknesses TEXT,
            cognitive_profile TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """))
    
    print("✅ Table french_learning_profiles créée")

def create_assessment_questions_table(db):
    """Créer la table des questions d'évaluation"""
    
    db.execute(text("""
        CREATE TABLE assessment_questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            test_id INTEGER NOT NULL,
            question_id INTEGER NOT NULL,
            question_order INTEGER NOT NULL,
            difficulty VARCHAR NOT NULL,
            question_text TEXT NOT NULL,
            options TEXT NOT NULL,
            correct_answer TEXT NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """))
    
    print("✅ Table assessment_questions créée")

if __name__ == "__main__":
    print("🔧 SCRIPT DE RÉPARATION DE LA BASE DE DONNÉES")
    print("=" * 50)
    
    success = fix_database()
    
    if success:
        print("\n🚀 PROCHAINES ÉTAPES:")
        print("   1. ✅ Base de données réparée")
        print("   2. 🧪 Tester le système: python quick_test.py")
        print("   3. 🚀 Démarrer le serveur: python start_assessment_system.py")
        print("   4. 📱 Tester le frontend: http://localhost:3001/dashboard/student/assessment")
    else:
        print("\n❌ LA RÉPARATION A ÉCHOUÉ")
        print("   Vérifiez les erreurs ci-dessus et relancez le script")
    
    print("\n" + "=" * 50)





