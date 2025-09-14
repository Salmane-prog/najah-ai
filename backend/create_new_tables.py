#!/usr/bin/env python3
"""
Script pour ajouter les nouvelles tables d'évaluation adaptative, analytics et IA
à la base de données existante Najah AI
"""

import sqlite3
import os
from pathlib import Path

def add_new_tables():
    """Ajouter les nouvelles tables à la base de données existante"""
    
    # Chemin vers la base de données
    db_path = Path("../data/app.db")
    
    # Vérifier si la base de données existe
    if not db_path.exists():
        print(f"❌ Base de données non trouvée: {db_path}")
        print("Exécutez d'abord create_database.py depuis le répertoire racine")
        return False
    
    print(f"🔍 Connexion à la base de données: {db_path}")
    
    # Connexion à la base de données
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print("🚀 Ajout des nouvelles tables...")
    
    try:
        # =====================================================
        # TABLES D'ÉVALUATION ADAPTATIVE
        # =====================================================
        
        print("📊 Création des tables d'évaluation adaptative...")
        
        # Table ADAPTIVE_TESTS
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS adaptive_tests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title VARCHAR(255) NOT NULL,
            subject VARCHAR(100) NOT NULL,
            description TEXT,
            difficulty_range_min INTEGER DEFAULT 1,
            difficulty_range_max INTEGER DEFAULT 10,
            estimated_duration INTEGER DEFAULT 30,
            is_active BOOLEAN DEFAULT 1,
            created_by INTEGER REFERENCES users(id),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        print("  ✅ Table adaptive_tests créée")
        
        # Table ADAPTIVE_QUESTIONS
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS adaptive_questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            test_id INTEGER REFERENCES adaptive_tests(id) ON DELETE CASCADE,
            question_text TEXT NOT NULL,
            question_type VARCHAR(50) NOT NULL CHECK (question_type IN ('multiple_choice', 'true_false', 'fill_blank', 'essay')),
            options TEXT, -- JSON string pour les choix multiples
            correct_answer TEXT NOT NULL,
            explanation TEXT,
            difficulty_level INTEGER NOT NULL CHECK (difficulty_level BETWEEN 1 AND 10),
            topic VARCHAR(100),
            cognitive_level VARCHAR(50) CHECK (cognitive_level IN ('remember', 'understand', 'apply', 'analyze', 'evaluate', 'create')),
            estimated_time INTEGER DEFAULT 60,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        print("  ✅ Table adaptive_questions créée")
        
        # Table STUDENT_ADAPTIVE_TESTS
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS student_adaptive_tests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
            test_id INTEGER REFERENCES adaptive_tests(id) ON DELETE CASCADE,
            started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            completed_at TIMESTAMP,
            current_question_index INTEGER DEFAULT 0,
            estimated_ability REAL DEFAULT 0.0,
            confidence_interval_lower REAL DEFAULT 0.0,
            confidence_interval_upper REAL DEFAULT 0.0,
            status VARCHAR(20) DEFAULT 'in_progress' CHECK (status IN ('not_started', 'in_progress', 'completed', 'abandoned')),
            total_score INTEGER DEFAULT 0,
            max_score INTEGER DEFAULT 0,
            UNIQUE(student_id, test_id)
        )
        ''')
        print("  ✅ Table student_adaptive_tests créée")
        
        # Table STUDENT_ANSWERS
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS student_answers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_test_id INTEGER REFERENCES student_adaptive_tests(id) ON DELETE CASCADE,
            question_id INTEGER REFERENCES adaptive_questions(id) ON DELETE CASCADE,
            selected_answer TEXT,
            is_correct BOOLEAN,
            time_spent INTEGER DEFAULT 0,
            difficulty_rating INTEGER CHECK (difficulty_rating BETWEEN 1 AND 5),
            confidence_rating INTEGER CHECK (confidence_rating BETWEEN 1 AND 5),
            answered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        print("  ✅ Table student_answers créée")
        
        # Table FORMATIVE_ASSESSMENTS
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS formative_assessments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title VARCHAR(255) NOT NULL,
            subject VARCHAR(100) NOT NULL,
            description TEXT,
            assessment_type VARCHAR(50) CHECK (assessment_type IN ('quiz', 'project', 'presentation', 'discussion', 'observation')),
            learning_objectives TEXT,
            criteria TEXT, -- JSON string pour les critères d'évaluation
            max_score INTEGER DEFAULT 100,
            weight REAL DEFAULT 1.0,
            due_date DATE,
            created_by INTEGER REFERENCES users(id),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        print("  ✅ Table formative_assessments créée")
        
        # Table STUDENT_FORMATIVE_ASSESSMENTS
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS student_formative_assessments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
            assessment_id INTEGER REFERENCES formative_assessments(id) ON DELETE CASCADE,
            submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            score REAL,
            feedback TEXT,
            status VARCHAR(20) DEFAULT 'submitted' CHECK (status IN ('not_started', 'in_progress', 'submitted', 'graded', 'returned')),
            graded_by INTEGER REFERENCES users(id),
            graded_at TIMESTAMP,
            UNIQUE(student_id, assessment_id)
        )
        ''')
        print("  ✅ Table student_formative_assessments créée")
        
        # Table SELF_ASSESSMENTS
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS self_assessments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
            title VARCHAR(255) NOT NULL,
            subject VARCHAR(100) NOT NULL,
            self_rating INTEGER CHECK (self_rating BETWEEN 1 AND 5),
            confidence_level INTEGER CHECK (confidence_level BETWEEN 1 AND 5),
            areas_of_strength TEXT,
            areas_for_improvement TEXT,
            learning_goals TEXT,
            reflection_notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        print("  ✅ Table self_assessments créée")
        
        # =====================================================
        # TABLES D'ANALYTICS ET REPORTING
        # =====================================================
        
        print("📈 Création des tables d'analytics et reporting...")
        
        # Table LEARNING_ANALYTICS
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS learning_analytics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
            date DATE NOT NULL,
            total_study_time INTEGER DEFAULT 0, -- en minutes
            subjects_studied TEXT, -- JSON string
            quizzes_taken INTEGER DEFAULT 0,
            quizzes_passed INTEGER DEFAULT 0,
            average_score REAL DEFAULT 0.0,
            learning_paths_completed INTEGER DEFAULT 0,
            badges_earned INTEGER DEFAULT 0,
            engagement_score REAL DEFAULT 0.0,
            focus_time INTEGER DEFAULT 0, -- temps de concentration
            break_time INTEGER DEFAULT 0, -- temps de pause
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        print("  ✅ Table learning_analytics créée")
        
        # Table PREDICTIVE_MODELS
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS predictive_models (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(255) NOT NULL,
            description TEXT,
            model_type VARCHAR(100) NOT NULL CHECK (model_type IN ('performance', 'engagement', 'completion', 'difficulty', 'custom')),
            algorithm VARCHAR(100),
            version VARCHAR(20) DEFAULT '1.0',
            accuracy REAL DEFAULT 0.0,
            precision REAL DEFAULT 0.0,
            recall REAL DEFAULT 0.0,
            f1_score REAL DEFAULT 0.0,
            training_data_size INTEGER DEFAULT 0,
            last_trained_at TIMESTAMP,
            is_active BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        print("  ✅ Table predictive_models créée")
        
        # Table STUDENT_PREDICTIONS
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS student_predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
            model_id INTEGER REFERENCES predictive_models(id) ON DELETE CASCADE,
            prediction_type VARCHAR(100) NOT NULL,
            predicted_value REAL NOT NULL,
            confidence REAL DEFAULT 0.0,
            prediction_date DATE NOT NULL,
            actual_value REAL,
            accuracy REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        print("  ✅ Table student_predictions créée")
        
        # Table LEARNING_PATTERNS
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS learning_patterns (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
            pattern_type VARCHAR(100) NOT NULL CHECK (pattern_type IN ('study_schedule', 'preferred_subjects', 'learning_style', 'performance_trend', 'engagement_pattern')),
            pattern_data TEXT, -- JSON string contenant les données du pattern
            confidence REAL DEFAULT 0.0,
            detected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            is_active BOOLEAN DEFAULT 1
        )
        ''')
        print("  ✅ Table learning_patterns créée")
        
        # Table BLOCKAGE_DETECTION
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS blockage_detection (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
            subject VARCHAR(100) NOT NULL,
            topic VARCHAR(100),
            blockage_type VARCHAR(100) CHECK (blockage_type IN ('conceptual', 'procedural', 'motivational', 'cognitive', 'metacognitive')),
            severity_level INTEGER CHECK (severity_level BETWEEN 1 AND 5),
            description TEXT,
            detected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            resolved_at TIMESTAMP,
            resolution_method TEXT,
            is_resolved BOOLEAN DEFAULT 0
        )
        ''')
        print("  ✅ Table blockage_detection créée")
        
        # Table TEACHER_DASHBOARDS
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS teacher_dashboards (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            teacher_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
            dashboard_name VARCHAR(255) NOT NULL,
            dashboard_type VARCHAR(100) CHECK (dashboard_type IN ('class_overview', 'student_progress', 'performance_analytics', 'content_effectiveness', 'custom')),
            configuration TEXT, -- JSON string pour la configuration du dashboard
            is_default BOOLEAN DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        print("  ✅ Table teacher_dashboards créée")
        
        # Table PARENT_DASHBOARDS
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS parent_dashboards (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            parent_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
            student_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
            dashboard_name VARCHAR(255) NOT NULL,
            dashboard_type VARCHAR(100) CHECK (dashboard_type IN ('academic_progress', 'behavior_tracking', 'communication_log', 'goal_setting', 'custom')),
            configuration TEXT, -- JSON string pour la configuration du dashboard
            is_default BOOLEAN DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        print("  ✅ Table parent_dashboards créée")
        
        # Table AUTOMATED_REPORTS
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS automated_reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title VARCHAR(255) NOT NULL,
            report_type VARCHAR(100) NOT NULL CHECK (report_type IN ('weekly', 'monthly', 'quarterly', 'semester', 'custom')),
            subject VARCHAR(100),
            class_id INTEGER REFERENCES class_groups(id),
            template_id VARCHAR(100),
            generation_schedule VARCHAR(100), -- cron expression ou description
            last_generated_at TIMESTAMP,
            next_generation_at TIMESTAMP,
            is_active BOOLEAN DEFAULT 1,
            created_by INTEGER REFERENCES users(id),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        print("  ✅ Table automated_reports créée")
        
        # Table REPORT_RECIPIENTS
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS report_recipients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            report_id INTEGER REFERENCES automated_reports(id) ON DELETE CASCADE,
            recipient_type VARCHAR(20) NOT NULL CHECK (recipient_type IN ('teacher', 'parent', 'student', 'admin')),
            recipient_id INTEGER REFERENCES users(id),
            delivery_method VARCHAR(50) CHECK (delivery_method IN ('email', 'dashboard', 'pdf', 'notification')),
            delivery_status VARCHAR(20) DEFAULT 'pending' CHECK (delivery_status IN ('pending', 'sent', 'delivered', 'failed')),
            sent_at TIMESTAMP,
            delivered_at TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        print("  ✅ Table report_recipients créée")
        
        # =====================================================
        # TABLES D'IA ET COLLECTE DE DONNÉES
        # =====================================================
        
        print("🤖 Création des tables d'IA et collecte de données...")
        
        # Table AI_MODELS
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS ai_models (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(255) NOT NULL,
            description TEXT,
            model_type VARCHAR(100) NOT NULL CHECK (model_type IN ('ml_algorithm', 'neural_network', 'expert_system', 'nlp_model', 'recommendation_engine')),
            technology VARCHAR(100),
            version VARCHAR(20) DEFAULT '1.0',
            performance_metrics TEXT, -- JSON string
            training_status VARCHAR(20) DEFAULT 'not_trained' CHECK (training_status IN ('not_trained', 'training', 'trained', 'deployed', 'archived')),
            deployment_status VARCHAR(20) DEFAULT 'not_deployed' CHECK (deployment_status IN ('not_deployed', 'testing', 'staging', 'production', 'maintenance')),
            created_by INTEGER REFERENCES users(id),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        print("  ✅ Table ai_models créée")
        
        # Table MODEL_TRAINING_SESSIONS
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS model_training_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            model_id INTEGER REFERENCES ai_models(id) ON DELETE CASCADE,
            session_name VARCHAR(255) NOT NULL,
            training_data_size INTEGER DEFAULT 0,
            training_parameters TEXT, -- JSON string
            start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            end_time TIMESTAMP,
            duration INTEGER, -- en secondes
            status VARCHAR(20) DEFAULT 'running' CHECK (status IN ('queued', 'running', 'completed', 'failed', 'cancelled')),
            accuracy REAL DEFAULT 0.0,
            loss REAL DEFAULT 0.0,
            validation_metrics TEXT, -- JSON string
            error_log TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        print("  ✅ Table model_training_sessions créée")
        
        # Table MODEL_PREDICTIONS
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS model_predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            model_id INTEGER REFERENCES ai_models(id) ON DELETE CASCADE,
            input_data TEXT, -- JSON string des données d'entrée
            prediction_result TEXT, -- JSON string du résultat
            confidence REAL DEFAULT 0.0,
            processing_time REAL DEFAULT 0.0, -- en millisecondes
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            user_id INTEGER REFERENCES users(id),
            session_id VARCHAR(100)
        )
        ''')
        print("  ✅ Table model_predictions créée")
        
        # Table MODEL_DEPLOYMENTS
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS model_deployments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            model_id INTEGER REFERENCES ai_models(id) ON DELETE CASCADE,
            environment VARCHAR(50) NOT NULL CHECK (environment IN ('development', 'staging', 'production')),
            deployment_url VARCHAR(255),
            api_key VARCHAR(255),
            status VARCHAR(20) DEFAULT 'deploying' CHECK (status IN ('deploying', 'active', 'inactive', 'failed', 'maintenance')),
            deployed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            deactivated_at TIMESTAMP,
            performance_metrics TEXT, -- JSON string
            error_log TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        print("  ✅ Table model_deployments créée")
        
        # Table DATA_COLLECTION
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS data_collection (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
            data_type VARCHAR(100) NOT NULL CHECK (data_type IN ('interaction', 'performance', 'behavior', 'preference', 'feedback')),
            data_source VARCHAR(100) NOT NULL,
            data_content TEXT NOT NULL, -- JSON string
            metadata TEXT, -- JSON string pour les métadonnées
            collection_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            is_anonymized BOOLEAN DEFAULT 1,
            consent_given BOOLEAN DEFAULT 1
        )
        ''')
        print("  ✅ Table data_collection créée")
        
        # Table LEARNING_PATTERN_ANALYSIS
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS learning_pattern_analysis (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
            analysis_type VARCHAR(100) NOT NULL CHECK (analysis_type IN ('study_habits', 'performance_trends', 'engagement_patterns', 'learning_preferences', 'difficulty_progression')),
            analysis_data TEXT NOT NULL, -- JSON string des résultats d'analyse
            insights TEXT,
            recommendations TEXT,
            confidence_score REAL DEFAULT 0.0,
            analysis_date DATE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        print("  ✅ Table learning_pattern_analysis créée")
        
        # Table CONTINUOUS_IMPROVEMENT
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS continuous_improvement (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            improvement_type VARCHAR(100) NOT NULL CHECK (improvement_type IN ('model_performance', 'user_experience', 'content_quality', 'system_efficiency', 'learning_outcomes')),
            description TEXT NOT NULL,
            current_metrics TEXT, -- JSON string
            target_metrics TEXT, -- JSON string
            improvement_strategy TEXT,
            implementation_status VARCHAR(20) DEFAULT 'planned' CHECK (implementation_status IN ('planned', 'in_progress', 'implemented', 'evaluated', 'abandoned')),
            priority INTEGER CHECK (priority BETWEEN 1 AND 5),
            estimated_impact VARCHAR(50) CHECK (estimated_impact IN ('low', 'medium', 'high', 'critical')),
            start_date DATE,
            completion_date DATE,
            results TEXT,
            created_by INTEGER REFERENCES users(id),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        print("  ✅ Table continuous_improvement créée")
        
        # =====================================================
        # CRÉATION DES INDEX
        # =====================================================
        
        print("🔍 Création des index pour les nouvelles tables...")
        
        # Index pour l'évaluation adaptative
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_adaptive_tests_subject ON adaptive_tests(subject)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_adaptive_questions_test_id ON adaptive_questions(test_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_student_adaptive_tests_student_id ON student_adaptive_tests(student_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_student_answers_student_test_id ON student_answers(student_test_id)')
        print("  ✅ Index pour l'évaluation adaptative créés")
        
        # Index pour l'analytics
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_learning_analytics_student_date ON learning_analytics(student_id, date)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_predictive_models_type ON predictive_models(model_type)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_student_predictions_student_model ON student_predictions(student_id, model_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_learning_patterns_student_type ON learning_patterns(student_id, pattern_type)')
        print("  ✅ Index pour l'analytics créés")
        
        # Index pour l'IA
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_ai_models_type ON ai_models(model_type)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_model_training_sessions_model_id ON model_training_sessions(model_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_model_predictions_model_id ON model_predictions(model_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_data_collection_student_type ON data_collection(student_id, data_type)')
        print("  ✅ Index pour l'IA créés")
        
        # Valider et fermer
        conn.commit()
        conn.close()
        
        print("✅ Nouvelles tables ajoutées avec succès !")
        print("📊 25 nouvelles tables créées")
        print("🔍 Index créés pour optimiser les performances")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la création des tables : {e}")
        conn.rollback()
        conn.close()
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    try:
        success = add_new_tables()
        if success:
            print("\n🎉 Nouvelles tables prêtes !")
            print("💡 Vous pouvez maintenant utiliser les nouvelles fonctionnalités")
        else:
            print("\n❌ Erreur lors de la création des tables")
    except Exception as e:
        print(f"❌ Erreur lors de la création des tables : {e}")
        import traceback
        traceback.print_exc() 