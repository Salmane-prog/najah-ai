#!/usr/bin/env python3
"""
Script pour corriger les tables de quiz
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.database import SessionLocal, engine
from sqlalchemy import text

def fix_quiz_tables():
    """Corrige les tables de quiz en ajoutant les colonnes manquantes."""
    db = SessionLocal()
    
    try:
        print("🔧 Correction des tables de quiz...")
        
        # Vérifier et corriger la table quiz_results
        try:
            # Vérifier si la colonne quiz_id existe
            result = db.execute(text("PRAGMA table_info(quiz_results)"))
            columns = [row[1] for row in result.fetchall()]
            
            if 'quiz_id' not in columns:
                print("  ➕ Ajout de la colonne quiz_id à quiz_results...")
                db.execute(text("ALTER TABLE quiz_results ADD COLUMN quiz_id INTEGER"))
            
            if 'student_id' not in columns:
                print("  ➕ Ajout de la colonne student_id à quiz_results...")
                db.execute(text("ALTER TABLE quiz_results ADD COLUMN student_id INTEGER"))
            
            if 'score' not in columns:
                print("  ➕ Ajout de la colonne score à quiz_results...")
                db.execute(text("ALTER TABLE quiz_results ADD COLUMN score REAL DEFAULT 0"))
            
            if 'max_score' not in columns:
                print("  ➕ Ajout de la colonne max_score à quiz_results...")
                db.execute(text("ALTER TABLE quiz_results ADD COLUMN max_score REAL DEFAULT 0"))
            
            if 'percentage' not in columns:
                print("  ➕ Ajout de la colonne percentage à quiz_results...")
                db.execute(text("ALTER TABLE quiz_results ADD COLUMN percentage REAL DEFAULT 0"))
            
            if 'started_at' not in columns:
                print("  ➕ Ajout de la colonne started_at à quiz_results...")
                db.execute(text("ALTER TABLE quiz_results ADD COLUMN started_at DATETIME"))
            
            if 'completed_at' not in columns:
                print("  ➕ Ajout de la colonne completed_at à quiz_results...")
                db.execute(text("ALTER TABLE quiz_results ADD COLUMN completed_at DATETIME"))
            
            if 'is_completed' not in columns:
                print("  ➕ Ajout de la colonne is_completed à quiz_results...")
                db.execute(text("ALTER TABLE quiz_results ADD COLUMN is_completed BOOLEAN DEFAULT 0"))
            
        except Exception as e:
            print(f"  ⚠️ Erreur lors de la correction de quiz_results: {e}")
        
        # Vérifier et corriger la table quiz_answers
        try:
            result = db.execute(text("PRAGMA table_info(quiz_answers)"))
            columns = [row[1] for row in result.fetchall()]
            
            if 'result_id' not in columns:
                print("  ➕ Ajout de la colonne result_id à quiz_answers...")
                db.execute(text("ALTER TABLE quiz_answers ADD COLUMN result_id INTEGER"))
            
            if 'question_id' not in columns:
                print("  ➕ Ajout de la colonne question_id à quiz_answers...")
                db.execute(text("ALTER TABLE quiz_answers ADD COLUMN question_id INTEGER"))
            
            if 'student_answer' not in columns:
                print("  ➕ Ajout de la colonne student_answer à quiz_answers...")
                db.execute(text("ALTER TABLE quiz_answers ADD COLUMN student_answer TEXT"))
            
            if 'is_correct' not in columns:
                print("  ➕ Ajout de la colonne is_correct à quiz_answers...")
                db.execute(text("ALTER TABLE quiz_answers ADD COLUMN is_correct BOOLEAN"))
            
            if 'points_earned' not in columns:
                print("  ➕ Ajout de la colonne points_earned à quiz_answers...")
                db.execute(text("ALTER TABLE quiz_answers ADD COLUMN points_earned REAL DEFAULT 0"))
            
        except Exception as e:
            print(f"  ⚠️ Erreur lors de la correction de quiz_answers: {e}")
        
        db.commit()
        print("✅ Tables de quiz corrigées avec succès !")
        
    except Exception as e:
        print(f"❌ Erreur lors de la correction: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    fix_quiz_tables() 