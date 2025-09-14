#!/usr/bin/env python3
"""
Script pour ajouter les colonnes manquantes dans les tables existantes
"""

import sqlite3
import os
from pathlib import Path

def fix_missing_columns():
    """Ajoute les colonnes manquantes dans les tables existantes"""
    
    db_path = Path("F:/IMT/stage/Yancode/Najah__AI/data/app.db")
    
    if not db_path.exists():
        print("❌ Base de données non trouvée")
        return
    
    print(f"🔧 Correction des colonnes manquantes dans: {db_path.absolute()}")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Vérifier les tables existantes
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        existing_tables = [row[0] for row in cursor.fetchall()]
        
        print(f"📊 Tables existantes: {existing_tables}")
        
        # 1. Ajouter class_id à calendar_events si elle n'existe pas
        if 'calendar_events' in existing_tables:
            cursor.execute("PRAGMA table_info(calendar_events)")
            columns = [row[1] for row in cursor.fetchall()]
            
            if 'class_id' not in columns:
                cursor.execute("ALTER TABLE calendar_events ADD COLUMN class_id INTEGER")
                print("✅ Colonne class_id ajoutée à calendar_events")
            else:
                print("✅ Colonne class_id existe déjà dans calendar_events")
        
        # 2. Ajouter d'autres colonnes manquantes si nécessaire
        if 'learning_history' in existing_tables:
            cursor.execute("PRAGMA table_info(learning_history)")
            columns = [row[1] for row in cursor.fetchall()]
            
            missing_columns = []
            if 'progress' not in columns:
                missing_columns.append("progress REAL DEFAULT 0.0")
            if 'time_spent' not in columns:
                missing_columns.append("time_spent INTEGER DEFAULT 0")
            if 'created_at' not in columns:
                missing_columns.append("created_at TEXT DEFAULT CURRENT_TIMESTAMP")
            
            for column_def in missing_columns:
                column_name = column_def.split()[0]
                cursor.execute(f"ALTER TABLE learning_history ADD COLUMN {column_def}")
                print(f"✅ Colonne {column_name} ajoutée à learning_history")
        
        # 3. Vérifier et corriger d'autres tables
        tables_to_check = {
            'calendar_study_sessions': ['class_id', 'created_by'],
            'ai_recommendations': ['content_id', 'quiz_id', 'learning_path_id'],
            'ai_tutoring_sessions': ['subject', 'topic', 'session_type'],
            'difficulty_detections': ['subject', 'topic', 'difficulty_level']
        }
        
        for table_name, required_columns in tables_to_check.items():
            if table_name in existing_tables:
                cursor.execute(f"PRAGMA table_info({table_name})")
                existing_columns = [row[1] for row in cursor.fetchall()]
                
                for column in required_columns:
                    if column not in existing_columns:
                        # Déterminer le type de colonne
                        if column in ['class_id', 'created_by', 'content_id', 'quiz_id', 'learning_path_id']:
                            column_type = "INTEGER"
                        elif column in ['subject', 'topic', 'session_type', 'difficulty_level']:
                            column_type = "TEXT"
                        else:
                            column_type = "TEXT"
                        
                        cursor.execute(f"ALTER TABLE {table_name} ADD COLUMN {column} {column_type}")
                        print(f"✅ Colonne {column} ajoutée à {table_name}")
        
        # Valider les changements
        conn.commit()
        
        print("\n🎉 Correction des colonnes terminée avec succès!")
        
        # Vérifier le résultat final
        print("\n📋 RÉSUMÉ DES CORRECTIONS:")
        for table_name in ['calendar_events', 'learning_history', 'ai_recommendations', 'ai_tutoring_sessions']:
            if table_name in existing_tables:
                cursor.execute(f"PRAGMA table_info({table_name})")
                columns = [row[1] for row in cursor.fetchall()]
                print(f"   {table_name}: {len(columns)} colonnes - {', '.join(columns)}")
        
    except Exception as e:
        print(f"❌ Erreur lors de la correction: {e}")
        conn.rollback()
    finally:
        conn.close()

def insert_sample_calendar_data():
    """Insère des données d'exemple pour le calendrier"""
    
    db_path = Path("F:/IMT/stage/Yancode/Najah__AI/data/app.db")
    if not db_path.exists():
        print("❌ Base de données non trouvée")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        print("\n📅 Insertion des données d'exemple pour le calendrier...")
        
        # Vérifier si la table calendar_events a des données
        cursor.execute("SELECT COUNT(*) FROM calendar_events")
        count = cursor.fetchone()[0]
        
        if count == 0:
            # Insérer des événements d'exemple
            cursor.execute("""
                INSERT INTO calendar_events 
                (title, description, event_type, start_time, end_time, subject, color, class_id, created_by)
                VALUES 
                ('Cours de Mathematiques', 'Algebre lineaire', 'course', '2025-08-12 09:00:00', '2025-08-12 10:30:00', 'Mathematiques', '#3B82F6', 1, 1),
                ('Examen de Physique', 'Mecanique classique', 'exam', '2025-08-14 14:00:00', '2025-08-14 16:00:00', 'Physique', '#EF4444', 2, 1),
                ('Devoir de Chimie', 'Stoechiometrie', 'homework', '2025-08-16 10:00:00', '2025-08-16 11:00:00', 'Chimie', '#10B981', 3, 1)
            """)
            
            print("✅ 3 événements d'exemple ajoutés au calendrier")
        else:
            print(f"✅ Table calendar_events contient déjà {count} événements")
        
        conn.commit()
        
    except Exception as e:
        print(f"❌ Erreur lors de l'insertion des données: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    print("🔧 CORRECTION DES COLONNES MANQUANTES")
    print("=" * 50)
    
    fix_missing_columns()
    insert_sample_calendar_data()
    
    print("\n" + "=" * 50)
    print("✅ CORRECTION TERMINÉE!")
    print("💡 IMPORTANT: Redémarrez le serveur backend maintenant!")
    print("🚀 Les erreurs 500 et 'Failed to fetch' devraient disparaître")
    print("📅 Le calendrier devrait maintenant afficher des événements")
