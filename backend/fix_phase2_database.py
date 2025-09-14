#!/usr/bin/env python3
"""
Script pour corriger la base de données Phase 2
"""
import sqlite3
import os
from datetime import datetime

def fix_phase2_database():
    """Corriger la base de données pour la Phase 2"""
    db_path = "F:/IMT/stage/Yancode/Najah__AI/data/app.db"
    
    if not os.path.exists(db_path):
        print(f"❌ Base de données non trouvée: {db_path}")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print("🔧 Correction de la base de données Phase 2...")
    print("=" * 50)
    
    try:
        # 1. Créer la table notifications
        print("➕ Création de la table notifications...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS notifications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                title VARCHAR(255) NOT NULL,
                message TEXT NOT NULL,
                type VARCHAR(50) DEFAULT 'info',
                is_read BOOLEAN DEFAULT FALSE,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)
        print("✅ Table notifications créée")
        
        # 2. Créer la table reports
        print("\n➕ Création de la table reports...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS reports (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title VARCHAR(255) NOT NULL,
                description TEXT,
                report_type VARCHAR(50) NOT NULL,
                generated_by INTEGER NOT NULL,
                file_path VARCHAR(500),
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (generated_by) REFERENCES users(id)
            )
        """)
        print("✅ Table reports créée")
        
        # 3. Créer la table resource_ratings
        print("\n➕ Création de la table resource_ratings...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS resource_ratings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                resource_type VARCHAR(50) NOT NULL,
                resource_id INTEGER NOT NULL,
                rating INTEGER NOT NULL CHECK (rating >= 1 AND rating <= 5),
                comment TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)
        print("✅ Table resource_ratings créée")
        
        # 4. Créer la table remediation_plans
        print("\n➕ Création de la table remediation_plans...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS remediation_plans (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER NOT NULL,
                teacher_id INTEGER NOT NULL,
                title VARCHAR(255) NOT NULL,
                description TEXT,
                status VARCHAR(50) DEFAULT 'active',
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (student_id) REFERENCES users(id),
                FOREIGN KEY (teacher_id) REFERENCES users(id)
            )
        """)
        print("✅ Table remediation_plans créée")
        
        # 5. Créer la table remediation_activities
        print("\n➕ Création de la table remediation_activities...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS remediation_activities (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                plan_id INTEGER NOT NULL,
                activity_type VARCHAR(50) NOT NULL,
                title VARCHAR(255) NOT NULL,
                description TEXT,
                content_id INTEGER,
                quiz_id INTEGER,
                order_index INTEGER DEFAULT 0,
                is_completed BOOLEAN DEFAULT FALSE,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (plan_id) REFERENCES remediation_plans(id),
                FOREIGN KEY (content_id) REFERENCES contents(id),
                FOREIGN KEY (quiz_id) REFERENCES quizzes(id)
            )
        """)
        print("✅ Table remediation_activities créée")
        
        # 6. Ajouter des données de test pour learning_history (avec la bonne structure)
        print("\n➕ Ajout de données de test pour learning_history...")
        cursor.execute("SELECT COUNT(*) FROM learning_history")
        count = cursor.fetchone()[0]
        
        if count == 0:
            # Ajouter quelques entrées d'historique d'apprentissage avec la structure réelle
            test_data = [
                (4, 1, 1, 50.0, 300, 1, datetime.now(), datetime.now(), 1, 'quiz_completion', 85.0, 50.0, 'Quiz terminé avec succès', datetime.now()),
                (5, 2, 1, 75.0, 450, 1, datetime.now(), datetime.now(), 1, 'content_view', 92.0, 75.0, 'Contenu visualisé', datetime.now()),
                (6, 3, 1, 30.0, 180, 0, datetime.now(), None, 1, 'quiz_start', 78.0, 30.0, 'Quiz commencé', datetime.now()),
                (7, 1, 2, 90.0, 600, 1, datetime.now(), datetime.now(), 2, 'quiz_completion', 95.0, 90.0, 'Quiz terminé avec excellence', datetime.now()),
                (8, 2, 2, 60.0, 400, 1, datetime.now(), datetime.now(), 2, 'content_view', 88.0, 60.0, 'Contenu étudié', datetime.now())
            ]
            
            cursor.executemany("""
                INSERT INTO learning_history 
                (student_id, content_id, learning_path_id, progress, time_spent, completed, 
                 started_at, completed_at, path_id, action, score, progression, details, timestamp)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, test_data)
            print("✅ 5 entrées d'historique d'apprentissage ajoutées")
        else:
            print(f"✅ {count} entrées d'historique existantes")
        
        # 7. Ajouter des notifications de test
        print("\n➕ Ajout de notifications de test...")
        notifications_data = [
            (1, 'Nouveau quiz disponible', 'Un nouveau quiz de mathématiques est disponible', 'info'),
            (1, 'Rappel évaluation', 'N\'oubliez pas l\'évaluation de fin de semaine', 'warning'),
            (2, 'Progression excellente', 'Félicitations pour votre progression !', 'success'),
            (3, 'Remédiation suggérée', 'Des exercices de remédiation vous sont proposés', 'info')
        ]
        
        cursor.executemany("""
            INSERT INTO notifications (user_id, title, message, type)
            VALUES (?, ?, ?, ?)
        """, notifications_data)
        print("✅ 4 notifications de test ajoutées")
        
        # 8. Ajouter des évaluations continues de test
        print("\n➕ Ajout d'évaluations continues de test...")
        cursor.execute("SELECT COUNT(*) FROM continuous_assessments")
        ca_count = cursor.fetchone()[0]
        
        if ca_count == 0:
            ca_data = [
                ('Évaluation Mathématiques', 'Évaluation continue en mathématiques', 'math', 'active'),
                ('Évaluation Physique', 'Évaluation continue en physique', 'physics', 'active'),
                ('Évaluation Chimie', 'Évaluation continue en chimie', 'chemistry', 'active')
            ]
            
            cursor.executemany("""
                INSERT INTO continuous_assessments (title, description, subject, status)
                VALUES (?, ?, ?, ?)
            """, ca_data)
            print("✅ 3 évaluations continues ajoutées")
        
        # 9. Ajouter des compétences de test
        print("\n➕ Ajout de compétences de test...")
        cursor.execute("SELECT COUNT(*) FROM competencies")
        comp_count = cursor.fetchone()[0]
        
        if comp_count == 0:
            competencies_data = [
                ('Résolution d\'équations', 'Capacité à résoudre des équations du premier degré', 'math', 'intermediate'),
                ('Analyse de données', 'Capacité à analyser et interpréter des données', 'science', 'advanced'),
                ('Communication écrite', 'Capacité à s\'exprimer clairement par écrit', 'language', 'basic'),
                ('Pensée critique', 'Capacité à analyser et évaluer des informations', 'general', 'intermediate')
            ]
            
            cursor.executemany("""
                INSERT INTO competencies (name, description, category, level)
                VALUES (?, ?, ?, ?)
            """, competencies_data)
            print("✅ 4 compétences ajoutées")
        
        conn.commit()
        print("\n✅ Base de données Phase 2 corrigée avec succès!")
        
        # Vérification finale
        print("\n📊 VÉRIFICATION FINALE:")
        cursor.execute("SELECT COUNT(*) FROM learning_history")
        lh_count = cursor.fetchone()[0]
        print(f"📚 Historique apprentissage: {lh_count} entrées")
        
        cursor.execute("SELECT COUNT(*) FROM notifications")
        notif_count = cursor.fetchone()[0]
        print(f"🔔 Notifications: {notif_count} entrées")
        
        cursor.execute("SELECT COUNT(*) FROM continuous_assessments")
        ca_final_count = cursor.fetchone()[0]
        print(f"📝 Évaluations continues: {ca_final_count} entrées")
        
        cursor.execute("SELECT COUNT(*) FROM competencies")
        comp_final_count = cursor.fetchone()[0]
        print(f"🎯 Compétences: {comp_final_count} entrées")
        
    except Exception as e:
        print(f"❌ Erreur lors de la correction: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    fix_phase2_database() 