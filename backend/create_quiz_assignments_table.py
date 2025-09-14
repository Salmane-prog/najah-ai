#!/usr/bin/env python3
"""
Script pour créer la table quiz_assignments
"""

import sqlite3
import os
from pathlib import Path

def create_quiz_assignments_table():
    """Créer la table quiz_assignments"""
    
    # Chemin vers la base de données
    db_path = Path(__file__).parent.parent / "data" / "app.db"
    
    if not db_path.exists():
        print(f"❌ Base de données non trouvée: {db_path}")
        return False
    
    try:
        # Connexion à la base de données
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print(f"🔗 Connexion à la base de données: {db_path}")
        
        # Vérifier si la table existe déjà
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='quiz_assignments'")
        if cursor.fetchone():
            print("✅ La table 'quiz_assignments' existe déjà")
            return True
        
        print("🔧 Création de la table 'quiz_assignments'...")
        
        # Créer la table quiz_assignments
        cursor.execute("""
            CREATE TABLE quiz_assignments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                quiz_id INTEGER NOT NULL,
                student_id INTEGER NOT NULL,
                assigned_by INTEGER NOT NULL,
                assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                due_date TIMESTAMP,
                status TEXT DEFAULT 'assigned',
                score INTEGER,
                completed_at TIMESTAMP,
                feedback TEXT,
                FOREIGN KEY (quiz_id) REFERENCES quizzes (id),
                FOREIGN KEY (student_id) REFERENCES users (id),
                FOREIGN KEY (assigned_by) REFERENCES users (id)
            )
        """)
        
        # Créer des index pour améliorer les performances
        cursor.execute("CREATE INDEX idx_quiz_assignments_quiz_id ON quiz_assignments(quiz_id)")
        cursor.execute("CREATE INDEX idx_quiz_assignments_student_id ON quiz_assignments(student_id)")
        cursor.execute("CREATE INDEX idx_quiz_assignments_assigned_by ON quiz_assignments(assigned_by)")
        
        # Valider les changements
        conn.commit()
        
        print("✅ Table 'quiz_assignments' créée avec succès!")
        print("✅ Index créés pour optimiser les performances")
        
        # Vérifier la structure de la table
        cursor.execute("PRAGMA table_info(quiz_assignments)")
        columns = cursor.fetchall()
        
        print("\n📋 Structure de la table quiz_assignments:")
        for col in columns:
            print(f"  - {col[1]} ({col[2]})")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la création de la table: {str(e)}")
        if 'conn' in locals():
            conn.rollback()
        return False
    
    finally:
        if 'conn' in locals():
            conn.close()
            print("🔌 Connexion fermée")

if __name__ == "__main__":
    print("🚀 Script de création de la table quiz_assignments")
    print("=" * 60)
    
    success = create_quiz_assignments_table()
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 Script exécuté avec succès!")
        print("✅ La table quiz_assignments est maintenant disponible")
    else:
        print("💥 Échec de l'exécution du script")
        print("❌ Vérifiez les erreurs ci-dessus")
