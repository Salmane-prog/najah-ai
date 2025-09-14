#!/usr/bin/env python3
"""
Script pour créer les tables manquantes pour l'évaluation adaptative complète
"""

import sqlite3
import os
from datetime import datetime

def create_adaptive_evaluation_tables():
    """Créer les tables manquantes pour l'évaluation adaptative"""
    
    # Chemin vers la base de données
    db_path = "./data/app.db"
    
    if not os.path.exists(db_path):
        print(f"❌ Base de données non trouvée: {db_path}")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("🚀 Création des tables manquantes pour l'évaluation adaptative...")
        
        # =====================================================
        # TABLE TEST_ASSIGNMENTS - Assignation des tests
        # =====================================================
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS test_assignments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            test_id INTEGER NOT NULL REFERENCES adaptive_tests(id) ON DELETE CASCADE,
            assignment_type VARCHAR(20) NOT NULL CHECK (assignment_type IN ('class', 'student', 'individual')),
            target_id INTEGER NOT NULL, -- ID de la classe ou de l'étudiant
            assigned_by INTEGER NOT NULL REFERENCES users(id),
            assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            due_date TIMESTAMP,
            is_active BOOLEAN DEFAULT 1,
            notification_sent BOOLEAN DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        print("  ✅ Table test_assignments créée")
        
        # =====================================================
        # TABLE TEST_RESULTS_SUMMARY - Résultats agrégés
        # =====================================================
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS test_results_summary (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            test_id INTEGER NOT NULL REFERENCES adaptive_tests(id) ON DELETE CASCADE,
            class_id INTEGER REFERENCES class_groups(id),
            total_students INTEGER DEFAULT 0,
            started_students INTEGER DEFAULT 0,
            completed_students INTEGER DEFAULT 0,
            average_score REAL DEFAULT 0.0,
            average_completion_time REAL DEFAULT 0.0,
            difficulty_adjustments_count INTEGER DEFAULT 0,
            questions_answered_total INTEGER DEFAULT 0,
            correct_answers_total INTEGER DEFAULT 0,
            last_activity TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        print("  ✅ Table test_results_summary créée")
        
        # =====================================================
        # TABLE ADAPTIVE_TEST_PERFORMANCE - Métriques détaillées
        # =====================================================
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS adaptive_test_performance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            test_id INTEGER NOT NULL REFERENCES adaptive_tests(id) ON DELETE CASCADE,
            student_id INTEGER NOT NULL REFERENCES users(id),
            class_id INTEGER REFERENCES class_groups(id),
            start_time TIMESTAMP,
            completion_time TIMESTAMP,
            total_questions INTEGER DEFAULT 0,
            questions_answered INTEGER DEFAULT 0,
            correct_answers INTEGER DEFAULT 0,
            incorrect_answers INTEGER DEFAULT 0,
            skipped_questions INTEGER DEFAULT 0,
            final_score REAL DEFAULT 0.0,
            initial_difficulty_level REAL DEFAULT 5.0,
            final_difficulty_level REAL DEFAULT 5.0,
            difficulty_adjustments INTEGER DEFAULT 0,
            average_response_time REAL DEFAULT 0.0,
            confidence_levels_avg REAL DEFAULT 0.0,
            learning_patterns JSON, -- Patterns d'apprentissage détectés
            recommendations JSON, -- Recommandations générées
            status VARCHAR(20) DEFAULT 'not_started' CHECK (status IN ('not_started', 'in_progress', 'completed', 'abandoned')),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        print("  ✅ Table adaptive_test_performance créée")
        
        # =====================================================
        # TABLE ADAPTIVE_QUESTIONS_POOL - Banque de questions
        # =====================================================
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS adaptive_questions_pool (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            test_id INTEGER NOT NULL REFERENCES adaptive_tests(id) ON DELETE CASCADE,
            question_id INTEGER NOT NULL REFERENCES adaptive_questions(id) ON DELETE CASCADE,
            difficulty_level REAL NOT NULL CHECK (difficulty_level BETWEEN 1.0 AND 10.0),
            cognitive_level VARCHAR(20) CHECK (cognitive_level IN ('remember', 'understand', 'apply', 'analyze', 'evaluate', 'create')),
            topic VARCHAR(100),
            subject VARCHAR(100),
            estimated_time INTEGER DEFAULT 60, -- en secondes
            success_rate REAL DEFAULT 0.0, -- taux de réussite historique
            usage_count INTEGER DEFAULT 0, -- nombre d'utilisations
            last_used TIMESTAMP,
            is_active BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        print("  ✅ Table adaptive_questions_pool créée")
        
        # =====================================================
        # TABLE LEARNING_ANALYTICS - Analytics d'apprentissage
        # =====================================================
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS learning_analytics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL REFERENCES users(id),
            test_id INTEGER REFERENCES adaptive_tests(id),
            subject VARCHAR(100),
            topic VARCHAR(100),
            learning_objective VARCHAR(255),
            performance_metric VARCHAR(50), -- score, time, difficulty, etc.
            metric_value REAL,
            metric_unit VARCHAR(20), -- %, seconds, level, etc.
            context JSON, -- contexte de l'analyse
            analysis_type VARCHAR(50), -- real_time, batch, predictive
            confidence_level REAL DEFAULT 0.0,
            recommendations JSON,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        print("  ✅ Table learning_analytics créée")
        
        # =====================================================
        # TABLE AI_RECOMMENDATIONS - Recommandations IA
        # =====================================================
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS ai_recommendations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL REFERENCES users(id),
            test_id INTEGER REFERENCES adaptive_tests(id),
            recommendation_type VARCHAR(50) NOT NULL CHECK (recommendation_type IN ('content', 'difficulty', 'pace', 'strategy', 'remediation')),
            title VARCHAR(255) NOT NULL,
            description TEXT,
            priority INTEGER DEFAULT 1 CHECK (priority BETWEEN 1 AND 5),
            confidence_score REAL DEFAULT 0.0 CHECK (confidence_score BETWEEN 0.0 AND 1.0),
            implementation_status VARCHAR(20) DEFAULT 'pending' CHECK (implementation_status IN ('pending', 'implemented', 'ignored', 'completed')),
            target_date TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        print("  ✅ Table ai_recommendations créée")
        
        # =====================================================
        # INDEXES POUR OPTIMISER LES PERFORMANCES
        # =====================================================
        print("\n🔍 Création des index pour optimiser les performances...")
        
        # Index pour test_assignments
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_test_assignments_test_id ON test_assignments(test_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_test_assignments_target ON test_assignments(assignment_type, target_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_test_assignments_assigned_by ON test_assignments(assigned_by)')
        
        # Index pour test_results_summary
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_test_results_test_id ON test_results_summary(test_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_test_results_class_id ON test_results_summary(class_id)')
        
        # Index pour adaptive_test_performance
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_performance_test_student ON adaptive_test_performance(test_id, student_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_performance_class ON adaptive_test_performance(class_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_performance_status ON adaptive_test_performance(status)')
        
        # Index pour learning_analytics
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_analytics_student ON learning_analytics(student_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_analytics_subject ON learning_analytics(subject)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_analytics_created ON learning_analytics(created_at)')
        
        print("  ✅ Index créés avec succès")
        
        # =====================================================
        # DONNÉES DE DÉMONSTRATION
        # =====================================================
        print("\n📊 Insertion de données de démonstration...")
        
        # Insérer des assignations de test de démonstration
        cursor.execute('''
        INSERT OR IGNORE INTO test_assignments (test_id, assignment_type, target_id, assigned_by, due_date)
        VALUES 
        (1, 'class', 1, 1, datetime('now', '+7 days')),
        (2, 'class', 1, 1, datetime('now', '+5 days')),
        (3, 'individual', 4, 1, datetime('now', '+3 days'))
        ''')
        
        # Insérer des résultats de démonstration
        cursor.execute('''
        INSERT OR IGNORE INTO test_results_summary (test_id, class_id, total_students, started_students, completed_students, average_score)
        VALUES 
        (1, 1, 24, 20, 18, 78.5),
        (2, 1, 18, 15, 12, 82.3),
        (3, NULL, 15, 8, 0, 0.0)
        ''')
        
        print("  ✅ Données de démonstration insérées")
        
        # Valider les changements
        conn.commit()
        print("\n🎉 Toutes les tables ont été créées avec succès !")
        
        # Afficher un résumé
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE '%adaptive%' OR name LIKE '%test%' OR name LIKE '%learning%' OR name LIKE '%ai%'")
        tables = cursor.fetchall()
        
        print(f"\n📋 Tables créées ({len(tables)}):")
        for table in tables:
            print(f"  - {table[0]}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la création des tables: {e}")
        conn.rollback()
        return False
        
    finally:
        conn.close()

if __name__ == "__main__":
    create_adaptive_evaluation_tables()
