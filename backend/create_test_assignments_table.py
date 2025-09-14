#!/usr/bin/env python3
"""
Script pour créer la table test_assignments manquante
"""

import sqlite3

def create_test_assignments_table():
    try:
        conn = sqlite3.connect('../data/app.db')
        cursor = conn.cursor()
        
        print("🔧 Création de la table test_assignments...")
        
        # Créer la table test_assignments
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS test_assignments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                test_id INTEGER NOT NULL,
                assignment_type TEXT NOT NULL CHECK (assignment_type IN ('class', 'student')),
                target_id INTEGER NOT NULL,
                assigned_by INTEGER NOT NULL,
                assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                due_date TIMESTAMP,
                status TEXT DEFAULT 'active' CHECK (status IN ('active', 'inactive', 'completed')),
                FOREIGN KEY (test_id) REFERENCES adaptive_tests (id) ON DELETE CASCADE,
                FOREIGN KEY (assigned_by) REFERENCES users (id) ON DELETE CASCADE
            )
        """)
        
        # Créer des index pour améliorer les performances
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_test_assignments_test_id ON test_assignments (test_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_test_assignments_target_id ON test_assignments (target_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_test_assignments_assigned_by ON test_assignments (assigned_by)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_test_assignments_status ON test_assignments (status)")
        
        conn.commit()
        print("✅ Table test_assignments créée avec succès")
        
        # Vérifier la structure
        cursor.execute("PRAGMA table_info(test_assignments)")
        columns = cursor.fetchall()
        print("📋 Structure de la table test_assignments:")
        for col in columns:
            print(f"  - {col[1]} ({col[2]})")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Erreur lors de la création: {e}")

if __name__ == "__main__":
    create_test_assignments_table()
