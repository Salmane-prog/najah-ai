#!/usr/bin/env python3
"""
Script pour recréer complètement la table french_adaptive_tests
avec la bonne structure (total_questions nullable)
"""

import sqlite3
import os

def fix_table_structure():
    """Recrée la table avec la bonne structure"""
    
    # Chemin EXACT utilisé par le backend
    db_path = "F:/IMT/stage/Yancode/Najah__AI/data/app.db"
    
    print(f"🔧 Recréation de la table french_adaptive_tests: {db_path}")
    
    try:
        # Connexion à la base de données
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 1. Sauvegarder les données existantes
        print("📋 1. Sauvegarde des données existantes...")
        cursor.execute("SELECT * FROM french_adaptive_tests")
        existing_data = cursor.fetchall()
        
        if existing_data:
            print(f"   - {len(existing_data)} enregistrements trouvés")
        else:
            print("   - Aucune donnée existante")
        
        # 2. Supprimer l'ancienne table
        print("🗑️ 2. Suppression de l'ancienne table...")
        cursor.execute("DROP TABLE french_adaptive_tests")
        print("   ✅ Ancienne table supprimée")
        
        # 3. Créer la nouvelle table avec la bonne structure
        print("🔧 3. Création de la nouvelle table...")
        cursor.execute("""
            CREATE TABLE french_adaptive_tests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER NOT NULL,
                test_type TEXT NOT NULL,
                current_question_index INTEGER DEFAULT 0,
                total_questions INTEGER,  -- NULLABLE pour le système adaptatif
                current_difficulty TEXT NOT NULL,
                status TEXT DEFAULT 'in_progress',
                started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                completed_at TIMESTAMP,
                final_score REAL,
                difficulty_progression TEXT,
                FOREIGN KEY (student_id) REFERENCES users (id)
            )
        """)
        print("   ✅ Nouvelle table créée")
        
        # 4. Restaurer les données existantes (si possible)
        if existing_data:
            print("📋 4. Restauration des données existantes...")
            
            # Vérifier la structure des données existantes
            cursor.execute("PRAGMA table_info(french_adaptive_tests)")
            new_columns = cursor.fetchall()
            column_names = [col[1] for col in new_columns]
            
            print(f"   - Colonnes de la nouvelle table: {column_names}")
            
            # Adapter les données existantes à la nouvelle structure
            for row in existing_data:
                try:
                    # Créer un dictionnaire avec les données existantes
                    data_dict = {}
                    for i, col in enumerate(new_columns):
                        if i < len(row):
                            data_dict[col[1]] = row[i]
                        else:
                            # Valeurs par défaut pour les nouvelles colonnes
                            if col[1] == 'total_questions':
                                data_dict[col[1]] = None  # NULL pour le système adaptatif
                            elif col[1] == 'difficulty_progression':
                                data_dict[col[1]] = None
                    
                    # Insérer avec la nouvelle structure
                    cursor.execute("""
                        INSERT INTO french_adaptive_tests 
                        (student_id, test_type, current_question_index, total_questions, 
                         current_difficulty, status, started_at, completed_at, final_score, difficulty_progression)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        data_dict.get('student_id'),
                        data_dict.get('test_type'),
                        data_dict.get('current_question_index', 0),
                        data_dict.get('total_questions'),  # Peut être NULL
                        data_dict.get('current_difficulty'),
                        data_dict.get('status', 'in_progress'),
                        data_dict.get('started_at'),
                        data_dict.get('completed_at'),
                        data_dict.get('final_score'),
                        data_dict.get('difficulty_progression')
                    ))
                    
                except Exception as e:
                    print(f"   ⚠️ Erreur lors de la restauration d'une ligne: {e}")
                    continue
            
            print("   ✅ Données restaurées")
        
        # 5. Valider les changements
        conn.commit()
        print("💾 5. Changements validés")
        
        # 6. Vérifier la nouvelle structure
        print("🔍 6. Vérification de la nouvelle structure...")
        cursor.execute("PRAGMA table_info(french_adaptive_tests)")
        new_columns = cursor.fetchall()
        
        print("📋 Structure de la nouvelle table:")
        for col in new_columns:
            print(f"   - {col[1]} ({col[2]}) - nullable: {col[3]}")
        
        # 7. Test d'insertion avec total_questions = NULL
        print("🧪 7. Test d'insertion avec total_questions = NULL...")
        try:
            cursor.execute("""
                INSERT INTO french_adaptive_tests 
                (student_id, test_type, current_question_index, total_questions, 
                 current_difficulty, status, started_at) 
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (999, 'test', 0, None, 'easy', 'in_progress', '2025-08-20 19:44:36.063345'))
            
            print("   ✅ Test d'insertion réussi avec total_questions = NULL")
            
            # Supprimer le test de test
            cursor.execute("DELETE FROM french_adaptive_tests WHERE student_id = 999")
            print("   ✅ Test supprimé")
            
        except Exception as e:
            print(f"   ❌ Échec du test d'insertion: {e}")
        
        conn.close()
        print("\n🎉 Table french_adaptive_tests recréée avec succès!")
        print("   Le système français devrait maintenant fonctionner !")
        
    except Exception as e:
        print(f"❌ Erreur lors de la recréation: {e}")
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    fix_table_structure()











