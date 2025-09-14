#!/usr/bin/env python3
"""
Script pour corriger la table achievements existante
"""

import sqlite3
import os

def fix_achievements_table():
    """Corriger la table achievements"""
    
    print("🔧 Correction de la table achievements...")
    
    # Chemin vers la base de données
    db_path = "../data/app.db"
    
    if not os.path.exists(db_path):
        print(f"❌ Base de données non trouvée : {db_path}")
        return
    
    try:
        # Connexion à la base de données
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Vérifier la structure de la table achievements
        print("📋 Vérification de la structure achievements...")
        cursor.execute("PRAGMA table_info(achievements)")
        columns = [row[1] for row in cursor.fetchall()]
        print(f"Colonnes existantes : {columns}")
        
        # Supprimer la table si elle existe avec une mauvaise structure
        if 'name' not in columns:
            print("🗑️ Suppression de la table achievements existante...")
            cursor.execute("DROP TABLE IF EXISTS achievements")
        
        # Recréer la table achievements
        print("📋 Recréation de la table achievements...")
        cursor.execute("""
            CREATE TABLE achievements (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(100) NOT NULL,
                description TEXT,
                points INTEGER DEFAULT 0,
                icon VARCHAR(50),
                category VARCHAR(50),
                criteria TEXT,
                is_hidden BOOLEAN DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Insérer des données de test pour les achievements
        print("📝 Insertion des achievements de test...")
        achievements_data = [
            ("Premier Pas", "Complétez votre premier quiz", 50, "🎯", "quiz", '{"type": "first_quiz"}', 0),
            ("Série de 7", "Complétez des quiz 7 jours de suite", 200, "🔥", "streak", '{"type": "streak", "days": 7}', 0),
            ("Perfectionniste", "Obtenez 100% sur un quiz", 300, "⭐", "score", '{"type": "perfect_score"}', 0),
            ("Rapide comme l'éclair", "Complétez 5 quiz en moins de 30 minutes", 150, "⚡", "speed", '{"type": "speed_quiz", "count": 5, "time": 1800}', 0),
            ("Maître du Sujet", "Obtenez une moyenne de 90%+ sur 10 quiz d'un même sujet", 500, "👑", "mastery", '{"type": "subject_mastery", "score": 0.9, "count": 10}', 0),
            ("Lève-tôt", "Complétez un quiz avant 8h du matin", 100, "🌅", "time", '{"type": "early_bird", "hour": 8}', 0)
        ]
        
        for achievement in achievements_data:
            cursor.execute("""
                INSERT INTO achievements (name, description, points, icon, category, criteria, is_hidden)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, achievement)
        
        # Vérifier la structure de la table challenges
        print("📋 Vérification de la structure challenges...")
        cursor.execute("PRAGMA table_info(challenges)")
        challenge_columns = [row[1] for row in cursor.fetchall()]
        print(f"Colonnes existantes : {challenge_columns}")
        
        # Supprimer la table si elle existe avec une mauvaise structure
        if 'name' not in challenge_columns:
            print("🗑️ Suppression de la table challenges existante...")
            cursor.execute("DROP TABLE IF EXISTS challenges")
        
        # Recréer la table challenges
        print("📋 Recréation de la table challenges...")
        cursor.execute("""
            CREATE TABLE challenges (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(100) NOT NULL,
                description TEXT,
                points INTEGER DEFAULT 0,
                icon VARCHAR(50),
                category VARCHAR(50),
                criteria TEXT,
                is_active BOOLEAN DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Insérer des données de test pour les challenges
        print("📝 Insertion des challenges de test...")
        challenges_data = [
            ("Quiz Master", "Complétez 10 quiz", 100, "📚", "quiz", '{"type": "quiz_count", "target": 10}', 1),
            ("Streak Master", "Complétez des quiz 5 jours de suite", 150, "🔥", "streak", '{"type": "streak", "days": 5}', 1),
            ("Score Hunter", "Obtenez une moyenne de 80% sur 5 quiz", 200, "🎯", "score", '{"type": "average_score", "target": 0.8, "count": 5}', 1)
        ]
        
        for challenge in challenges_data:
            cursor.execute("""
                INSERT INTO challenges (name, description, points, icon, category, criteria, is_active)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, challenge)
        
        # Valider les changements
        conn.commit()
        
        print("✅ Tables achievements et challenges corrigées avec succès !")
        
    except Exception as e:
        print(f"❌ Erreur lors de la correction : {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    fix_achievements_table() 