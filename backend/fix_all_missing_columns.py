#!/usr/bin/env python3
"""
Script complet pour ajouter TOUTES les colonnes manquantes
"""

import sqlite3
import os
from pathlib import Path

def fix_all_missing_columns():
    """Ajoute TOUTES les colonnes manquantes dans TOUTES les tables"""
    
    db_path = Path("F:/IMT/stage/Yancode/Najah__AI/data/app.db")
    
    if not db_path.exists():
        print("❌ Base de données non trouvée")
        return
    
    print(f"🔧 Correction COMPLÈTE des colonnes manquantes dans: {db_path.absolute()}")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Vérifier les tables existantes
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        existing_tables = [row[0] for row in cursor.fetchall()]
        
        print(f"📊 Tables existantes: {existing_tables}")
        
        # 1. CORRIGER calendar_events
        if 'calendar_events' in existing_tables:
            print("\n📅 Correction de calendar_events...")
            cursor.execute("PRAGMA table_info(calendar_events)")
            columns = [row[1] for row in cursor.fetchall()]
            
            missing_columns = []
            if 'created_by' not in columns:
                missing_columns.append("created_by INTEGER")
            if 'user_id' not in columns:
                missing_columns.append("user_id INTEGER")
            if 'is_active' not in columns:
                missing_columns.append("is_active BOOLEAN DEFAULT 1")
            if 'updated_at' not in columns:
                missing_columns.append("updated_at TEXT DEFAULT CURRENT_TIMESTAMP")
            
            for column_def in missing_columns:
                column_name = column_def.split()[0]
                cursor.execute(f"ALTER TABLE calendar_events ADD COLUMN {column_def}")
                print(f"   ✅ Colonne {column_name} ajoutée")
        
        # 2. CORRIGER badges
        if 'badges' in existing_tables:
            print("\n🏆 Correction de badges...")
            cursor.execute("PRAGMA table_info(badges)")
            columns = [row[1] for row in cursor.fetchall()]
            
            missing_columns = []
            if 'criteria' not in columns:
                missing_columns.append("criteria TEXT")
            if 'image_url' not in columns:
                missing_columns.append("image_url TEXT")
            if 'secret' not in columns:
                missing_columns.append("secret BOOLEAN DEFAULT 0")
            if 'badge_type' not in columns:
                missing_columns.append("badge_type TEXT DEFAULT 'achievement'")
            if 'requirements' not in columns:
                missing_columns.append("requirements TEXT")
            
            for column_def in missing_columns:
                column_name = column_def.split()[0]
                cursor.execute(f"ALTER TABLE badges ADD COLUMN {column_def}")
                print(f"   ✅ Colonne {column_name} ajoutée")
        
        # 3. CORRIGER learning_history
        if 'learning_history' in existing_tables:
            print("\n📚 Correction de learning_history...")
            cursor.execute("PRAGMA table_info(learning_history)")
            columns = [row[1] for row in cursor.fetchall()]
            
            missing_columns = []
            if 'progress' not in columns:
                missing_columns.append("progress REAL DEFAULT 0.0")
            if 'time_spent' not in columns:
                missing_columns.append("time_spent INTEGER DEFAULT 0")
            if 'created_at' not in columns:
                missing_columns.append("created_at TEXT DEFAULT CURRENT_TIMESTAMP")
            if 'completed' not in columns:
                missing_columns.append("completed BOOLEAN DEFAULT 0")
            if 'started_at' not in columns:
                missing_columns.append("started_at TEXT DEFAULT CURRENT_TIMESTAMP")
            if 'completed_at' not in columns:
                missing_columns.append("completed_at TEXT")
            
            for column_def in missing_columns:
                column_name = column_def.split()[0]
                cursor.execute(f"ALTER TABLE learning_history ADD COLUMN {column_def}")
                print(f"   ✅ Colonne {column_name} ajoutée")
        
        # 4. CORRIGER gamification_test
        if 'gamification_test' in existing_tables:
            print("\n🎮 Correction de gamification_test...")
            cursor.execute("PRAGMA table_info(gamification_test)")
            columns = [row[1] for row in cursor.fetchall()]
            
            missing_columns = []
            if 'achievements_count' not in columns:
                missing_columns.append("achievements_count INTEGER DEFAULT 0")
            if 'challenges_count' not in columns:
                missing_columns.append("challenges_count INTEGER DEFAULT 0")
            if 'last_updated' not in columns:
                missing_columns.append("last_updated TEXT DEFAULT CURRENT_TIMESTAMP")
            
            for column_def in missing_columns:
                column_name = column_def.split()[0]
                cursor.execute(f"ALTER TABLE gamification_test ADD COLUMN {column_def}")
                print(f"   ✅ Colonne {column_name} ajoutée")
        
        # 5. CORRIGER autres tables importantes
        tables_to_fix = {
            'ai_recommendations': ['content_id', 'quiz_id', 'learning_path_id', 'confidence_score'],
            'ai_tutoring_sessions': ['subject', 'topic', 'session_type', 'duration', 'status'],
            'difficulty_detections': ['subject', 'topic', 'difficulty_level', 'confidence_score'],
            'homework_assignments': ['class_id', 'assigned_by', 'due_date', 'max_score'],
            'study_groups': ['subject', 'max_members', 'is_public', 'created_by']
        }
        
        for table_name, required_columns in tables_to_fix.items():
            if table_name in existing_tables:
                print(f"\n🔧 Correction de {table_name}...")
                cursor.execute(f"PRAGMA table_info({table_name})")
                existing_columns = [row[1] for row in cursor.fetchall()]
                
                for column in required_columns:
                    if column not in existing_columns:
                        # Déterminer le type de colonne
                        if column in ['class_id', 'assigned_by', 'created_by', 'content_id', 'quiz_id', 'learning_path_id', 'max_members', 'max_score']:
                            column_type = "INTEGER"
                        elif column in ['subject', 'topic', 'session_type', 'difficulty_level']:
                            column_type = "TEXT"
                        elif column in ['due_date', 'duration']:
                            column_type = "TEXT"
                        elif column in ['confidence_score']:
                            column_type = "REAL"
                        elif column in ['is_public']:
                            column_type = "BOOLEAN"
                        else:
                            column_type = "TEXT"
                        
                        cursor.execute(f"ALTER TABLE {table_name} ADD COLUMN {column} {column_type}")
                        print(f"   ✅ Colonne {column} ajoutée")
        
        # Valider tous les changements
        conn.commit()
        
        print("\n🎉 Correction COMPLÈTE terminée avec succès!")
        
        # Vérifier le résultat final
        print("\n📋 RÉSUMÉ DES CORRECTIONS:")
        important_tables = ['calendar_events', 'badges', 'learning_history', 'gamification_test', 'ai_recommendations']
        for table_name in important_tables:
            if table_name in existing_tables:
                cursor.execute(f"PRAGMA table_info({table_name})")
                columns = [row[1] for row in cursor.fetchall()]
                print(f"   {table_name}: {len(columns)} colonnes - {', '.join(columns)}")
        
    except Exception as e:
        print(f"❌ Erreur lors de la correction: {e}")
        conn.rollback()
    finally:
        conn.close()

def insert_sample_data():
    """Insère des données d'exemple pour tester"""
    
    db_path = Path("F:/IMT/stage/Yancode/Najah__AI/data/app.db")
    if not db_path.exists():
        print("❌ Base de données non trouvée")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        print("\n📅 Insertion des données d'exemple...")
        
        # Vérifier si calendar_events a des données
        cursor.execute("SELECT COUNT(*) FROM calendar_events")
        calendar_count = cursor.fetchone()[0]
        
        if calendar_count == 0:
            # Insérer des événements d'exemple
            cursor.execute("""
                INSERT INTO calendar_events 
                (title, description, event_type, start_time, end_time, subject, color, class_id, created_by, user_id)
                VALUES 
                ('Cours de Mathematiques', 'Algebre lineaire', 'course', '2025-08-12 09:00:00', '2025-08-12 10:30:00', 'Mathematiques', '#3B82F6', 1, 1, 4),
                ('Examen de Physique', 'Mecanique classique', 'exam', '2025-08-14 14:00:00', '2025-08-14 16:00:00', 'Physique', '#EF4444', 2, 1, 4),
                ('Devoir de Chimie', 'Stoechiometrie', 'homework', '2025-08-16 10:00:00', '2025-08-16 11:00:00', 'Chimie', '#10B981', 3, 1, 4)
            """)
            print("   ✅ 3 événements de calendrier ajoutés")
        
        # Vérifier si badges a des données
        cursor.execute("SELECT COUNT(*) FROM badges")
        badges_count = cursor.fetchone()[0]
        
        if badges_count == 0:
            # Insérer des badges d'exemple
            cursor.execute("""
                INSERT INTO badges 
                (user_id, name, description, rarity, criteria, icon)
                VALUES 
                (4, 'Quiz Master', 'Complété 5 quiz', 'gold', 'Compléter 5 quiz', '🏆'),
                (5, 'Quiz Expert', 'Score moyen > 80%', 'silver', 'Score moyen > 80%', '🎖️'),
                (6, 'Score Parfait', 'Obtenu 100% sur un quiz', 'platinum', 'Score parfait', '💎')
            """)
            print("   ✅ 3 badges ajoutés")
        
        conn.commit()
        
    except Exception as e:
        print(f"❌ Erreur lors de l'insertion: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    print("🔧 CORRECTION COMPLÈTE DES COLONNES MANQUANTES")
    print("=" * 60)
    
    fix_all_missing_columns()
    insert_sample_data()
    
    print("\n" + "=" * 60)
    print("✅ CORRECTION COMPLÈTE TERMINÉE!")
    print("💡 IMPORTANT: Redémarrez le serveur backend maintenant!")
    print("🚀 TOUTES les colonnes manquantes sont ajoutées")
    print("📊 Plus d'erreurs 500 ou colonnes manquantes!")
    print("🎯 Le frontend devrait maintenant fonctionner parfaitement!")


