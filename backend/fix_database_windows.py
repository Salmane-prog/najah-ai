#!/usr/bin/env python3
"""
SCRIPT DE REPARATION DE LA BASE DE DONNEES - VERSION WINDOWS
Corrige les problemes de colonnes et de structure des tables
"""

import sys
import os
from pathlib import Path

# Ajouter le repertoire parent au path
sys.path.append(str(Path(__file__).parent))

from core.database import get_db, engine
from sqlalchemy import text

def fix_database():
    """Reparer la base de donnees"""
    
    print("REPARATION DE LA BASE DE DONNEES")
    print("=" * 50)
    
    try:
        db = next(get_db())
        
        print("\nVerification des tables existantes...")
        
        # Verifier si la table french_adaptive_tests existe
        result = db.execute(text("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='french_adaptive_tests'
        """))
        
        if result.fetchone():
            print("OK: Table french_adaptive_tests trouvee")
            
            # Verifier la structure de la table
            result = db.execute(text("PRAGMA table_info(french_adaptive_tests)"))
            columns = [row[1] for row in result.fetchall()]
            print(f"   Colonnes actuelles: {', '.join(columns)}")
            
            # Verifier si current_question_order existe
            if 'current_question_order' in columns:
                print("ATTENTION: Colonne 'current_question_order' trouvee - suppression en cours...")
                
                # Creer une nouvelle table avec la bonne structure
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
                
                # Copier les donnees existantes
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
                print("OK: Table french_adaptive_tests reparee")
                
            else:
                print("OK: Structure de la table correcte")
                
        else:
            print("INFO: Table french_adaptive_tests n'existe pas - creation...")
            create_french_tables(db)
        
        # Verifier les autres tables
        print("\nVerification des autres tables...")
        
        # Table french_test_answers
        result = db.execute(text("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='french_test_answers'
        """))
        
        if not result.fetchone():
            print("INFO: Table french_test_answers n'existe pas - creation...")
            create_answer_table(db)
        else:
            print("OK: Table french_test_answers trouvee")
        
        # Table french_learning_profiles
        result = db.execute(text("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='french_learning_profiles'
        """))
        
        if not result.fetchone():
            print("INFO: Table french_learning_profiles n'existe pas - creation...")
            create_profile_table(db)
        else:
            print("OK: Table french_learning_profiles trouvee")
        
        # Table assessment_questions
        result = db.execute(text("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='assessment_questions'
        """))
        
        if not result.fetchone():
            print("INFO: Table assessment_questions n'existe pas - creation...")
            create_assessment_questions_table(db)
        else:
            print("OK: Table assessment_questions trouvee")
        
        print("\n" + "=" * 50)
        print("REPARATION TERMINEE AVEC SUCCES !")
        print("OK: Toutes les tables sont maintenant correctement configurees")
        print("OK: Le systeme d'evaluation peut maintenant fonctionner")
        
        return True
        
    except Exception as e:
        print(f"\nERREUR LORS DE LA REPARATION: {e}")
        import traceback
        traceback.print_exc()
        return False
        
    finally:
        if 'db' in locals():
            db.close()

def create_french_tables(db):
    """Creer les tables francaises avec la bonne structure"""
    
    # Table des tests francais
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
    
    print("OK: Table french_adaptive_tests creee")

def create_answer_table(db):
    """Creer la table des reponses"""
    
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
    
    print("OK: Table french_test_answers creee")

def create_profile_table(db):
    """Creer la table des profils"""
    
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
    
    print("OK: Table french_learning_profiles creee")

def create_assessment_questions_table(db):
    """Creer la table des questions d'evaluation"""
    
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
    
    print("OK: Table assessment_questions creee")

if __name__ == "__main__":
    print("SCRIPT DE REPARATION DE LA BASE DE DONNEES - VERSION WINDOWS")
    print("=" * 50)
    
    success = fix_database()
    
    if success:
        print("\nPROCHAINES ETAPES:")
        print("   1. OK: Base de donnees reparee")
        print("   2. TEST: Tester le systeme: python quick_test.py")
        print("   3. DEMARRAGE: Demarrer le serveur: python start_assessment_system.py")
        print("   4. FRONTEND: Tester le frontend: http://localhost:3001/dashboard/student/assessment")
    else:
        print("\nLA REPARATION A ECHOUE")
        print("   Verifiez les erreurs ci-dessus et relancez le script")
    
    print("\n" + "=" * 50)





