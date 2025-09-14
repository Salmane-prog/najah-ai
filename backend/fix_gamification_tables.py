#!/usr/bin/env python3
"""
Script pour ajouter les tables de gamification manquantes à la base de données.
"""

import sqlite3
import os

def fix_gamification_tables():
    """Ajouter les tables de gamification manquantes."""
    
    # Chemin vers la base de données
    db_path = "../data/app.db"
    
    if not os.path.exists(db_path):
        print(f"❌ Base de données introuvable: {db_path}")
        return
    
    print(f"🔧 Ajout des tables de gamification à {db_path}")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Vérifier et créer la table user_levels
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_levels (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL UNIQUE,
                level INTEGER DEFAULT 1,
                current_xp INTEGER DEFAULT 0,
                total_xp INTEGER DEFAULT 0,
                xp_to_next_level INTEGER DEFAULT 1000,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        """)
        print("✓ Table user_levels créée/vérifiée")
        
        # Vérifier et créer la table challenges
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS challenges (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                challenge_type TEXT NOT NULL,
                xp_reward INTEGER DEFAULT 0,
                badge_reward_id INTEGER,
                requirements TEXT,
                is_active BOOLEAN DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (badge_reward_id) REFERENCES badges (id)
            )
        """)
        print("✓ Table challenges créée/vérifiée")
        
        # Vérifier et créer la table user_challenges
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_challenges (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                challenge_id INTEGER NOT NULL,
                progress REAL DEFAULT 0.0,
                is_completed BOOLEAN DEFAULT 0,
                completed_at TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id),
                FOREIGN KEY (challenge_id) REFERENCES challenges (id)
            )
        """)
        print("✓ Table user_challenges créée/vérifiée")
        
        # Vérifier et créer la table leaderboards
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS leaderboards (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                leaderboard_type TEXT NOT NULL,
                subject TEXT,
                class_id INTEGER,
                start_date TIMESTAMP,
                end_date TIMESTAMP,
                is_active BOOLEAN DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (class_id) REFERENCES class_groups (id)
            )
        """)
        print("✓ Table leaderboards créée/vérifiée")
        
        # Vérifier et créer la table leaderboard_entries
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS leaderboard_entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                leaderboard_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                score INTEGER DEFAULT 0,
                rank INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (leaderboard_id) REFERENCES leaderboards (id),
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        """)
        print("✓ Table leaderboard_entries créée/vérifiée")
        
        # Vérifier et créer la table achievements
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS achievements (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                icon TEXT,
                achievement_type TEXT NOT NULL,
                requirements TEXT,
                xp_reward INTEGER DEFAULT 0,
                badge_reward_id INTEGER,
                is_hidden BOOLEAN DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (badge_reward_id) REFERENCES badges (id)
            )
        """)
        print("✓ Table achievements créée/vérifiée")
        
        # Vérifier et créer la table user_achievements
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_achievements (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                achievement_id INTEGER NOT NULL,
                unlocked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id),
                FOREIGN KEY (achievement_id) REFERENCES achievements (id)
            )
        """)
        print("✓ Table user_achievements créée/vérifiée")
        
        # Ajouter quelques données de test pour les challenges et achievements
        cursor.execute("SELECT COUNT(*) FROM challenges")
        if cursor.fetchone()[0] == 0:
            cursor.execute("""
                INSERT INTO challenges (title, description, challenge_type, xp_reward) VALUES
                ('Premier Quiz', 'Complétez votre premier quiz', 'achievement', 50),
                ('Quiz Master', 'Complétez 10 quiz', 'achievement', 200),
                ('Streak de 7 jours', 'Connectez-vous 7 jours de suite', 'achievement', 100)
            """)
            print("✓ Données de test ajoutées pour challenges")
        
        cursor.execute("SELECT COUNT(*) FROM achievements")
        if cursor.fetchone()[0] == 0:
            cursor.execute("""
                INSERT INTO achievements (title, description, achievement_type, xp_reward) VALUES
                ('Débutant', 'Complétez votre premier quiz', 'quiz', 50),
                ('Quiz Master', 'Complétez 10 quiz', 'quiz', 200),
                ('Niveau 5', 'Atteignez le niveau 5', 'level', 100)
            """)
            print("✓ Données de test ajoutées pour achievements")
        
        conn.commit()
        print("✅ Tables de gamification ajoutées avec succès !")
        
    except Exception as e:
        print(f"❌ Erreur lors de l'ajout des tables: {str(e)}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    fix_gamification_tables() 