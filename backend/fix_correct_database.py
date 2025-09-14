#!/usr/bin/env python3
"""
Script pour corriger la contrainte NOT NULL sur total_questions
dans la VRAIE base de données utilisée par le backend
"""

import sqlite3
import os

def fix_correct_database():
    """Corrige la contrainte NOT NULL sur total_questions dans la vraie base"""
    
    # Chemin EXACT utilisé par le backend
    db_path = "F:/IMT/stage/Yancode/Najah__AI/data/app.db"
    
    print(f"🔧 Correction de la VRAIE base de données: {db_path}")
    
    try:
        # Connexion à la base de données
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Vérifier la structure actuelle de la table
        cursor.execute("PRAGMA table_info(french_adaptive_tests)")
        columns = cursor.fetchall()
        
        print("📋 Structure actuelle de la table french_adaptive_tests:")
        for col in columns:
            print(f"  - {col[1]} ({col[2]}) - nullable: {col[3]}")
        
        # Vérifier si total_questions a la bonne contrainte
        total_questions_col = None
        for col in columns:
            if col[1] == 'total_questions':
                total_questions_col = col
                break
        
        if total_questions_col and total_questions_col[3] == 0:  # NOT NULL
            print("❌ Problème détecté: total_questions est NOT NULL")
            
            # Créer une table temporaire avec la bonne structure
            print("🔧 Création d'une table temporaire...")
            
            # Créer la nouvelle table avec la bonne structure
            cursor.execute("""
                CREATE TABLE french_adaptive_tests_new (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    student_id INTEGER NOT NULL,
                    test_type VARCHAR NOT NULL,
                    current_question_index INTEGER DEFAULT 0,
                    total_questions INTEGER,  -- NULLABLE
                    current_difficulty VARCHAR NOT NULL,
                    status VARCHAR DEFAULT 'in_progress',
                    started_at DATETIME,
                    completed_at DATETIME,
                    final_score INTEGER,
                    difficulty_progression TEXT
                )
            """)
            
            # Copier les données existantes
            print("📋 Copie des données existantes...")
            cursor.execute("""
                INSERT INTO french_adaptive_tests_new 
                SELECT id, student_id, test_type, current_question_index, 
                       total_questions, current_difficulty, status, 
                       started_at, completed_at, final_score, difficulty_progression
                FROM french_adaptive_tests
            """)
            
            # Supprimer l'ancienne table
            print("🗑️ Suppression de l'ancienne table...")
            cursor.execute("DROP TABLE french_adaptive_tests")
            
            # Renommer la nouvelle table
            print("🔄 Renommage de la nouvelle table...")
            cursor.execute("ALTER TABLE french_adaptive_tests_new RENAME TO french_adaptive_tests")
            
            # Valider les changements
            conn.commit()
            
            print("✅ Table french_adaptive_tests corrigée avec succès!")
            
            # Vérifier la nouvelle structure
            cursor.execute("PRAGMA table_info(french_adaptive_tests)")
            new_columns = cursor.fetchall()
            
            print("📋 Nouvelle structure de la table french_adaptive_tests:")
            for col in new_columns:
                print(f"  - {col[1]} ({col[2]}) - nullable: {col[3]}")
                
        else:
            print("✅ La table french_adaptive_tests est déjà correcte")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Erreur lors de la correction: {e}")
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    fix_correct_database()











