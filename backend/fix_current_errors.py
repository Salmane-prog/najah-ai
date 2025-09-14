#!/usr/bin/env python3
"""
Script pour corriger les erreurs actuelles identifiées dans les logs.
"""

import sqlite3
import os

def fix_current_errors():
    """Corriger les erreurs actuelles."""
    
    # Chemin vers la base de données
    db_path = "../data/app.db"
    
    if not os.path.exists(db_path):
        print(f"❌ Base de données introuvable: {db_path}")
        return
    
    print(f"🔧 Correction des erreurs dans {db_path}")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # 1. Ajouter la colonne updated_at à la table quizzes si elle n'existe pas
        cursor.execute("PRAGMA table_info(quizzes)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'updated_at' not in columns:
            print("✓ Ajout de la colonne 'updated_at' à la table 'quizzes'...")
            cursor.execute("ALTER TABLE quizzes ADD COLUMN updated_at TIMESTAMP")
            print("✓ Colonne 'updated_at' ajoutée")
        else:
            print("✓ Colonne 'updated_at' déjà présente")
        
        # 2. Ajouter la colonne objectives à la table learning_paths si elle n'existe pas
        cursor.execute("PRAGMA table_info(learning_paths)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'objectives' not in columns:
            print("✓ Ajout de la colonne 'objectives' à la table 'learning_paths'...")
            cursor.execute("ALTER TABLE learning_paths ADD COLUMN objectives TEXT")
            print("✓ Colonne 'objectives' ajoutée")
        else:
            print("✓ Colonne 'objectives' déjà présente")
        
        # 3. Vérifier et corriger les tables de gamification
        tables_to_check = [
            'user_levels', 'challenges', 'user_challenges', 
            'leaderboards', 'leaderboard_entries', 'achievements', 'user_achievements'
        ]
        
        for table in tables_to_check:
            cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table}'")
            if not cursor.fetchone():
                print(f"⚠️  Table '{table}' manquante - création nécessaire")
            else:
                print(f"✓ Table '{table}' présente")
        
        # 4. Vérifier les données de test pour les leaderboards
        cursor.execute("SELECT COUNT(*) FROM leaderboards")
        leaderboard_count = cursor.fetchone()[0]
        
        if leaderboard_count == 0:
            print("✓ Ajout de données de test pour les leaderboards...")
            cursor.execute("""
                INSERT INTO leaderboards (title, description, leaderboard_type, subject, is_active)
                VALUES 
                ('Classement Global', 'Classement général des étudiants', 'global', NULL, 1),
                ('Classement Classe 1', 'Classement de la classe 1', 'class', NULL, 1)
            """)
            print("✓ Données de test ajoutées")
        else:
            print(f"✓ {leaderboard_count} leaderboards présents")
        
        # 5. Vérifier les données de test pour les achievements
        cursor.execute("SELECT COUNT(*) FROM achievements")
        achievement_count = cursor.fetchone()[0]
        
        if achievement_count == 0:
            print("✓ Ajout de données de test pour les achievements...")
            cursor.execute("""
                INSERT INTO achievements (title, description, icon, achievement_type, requirements, xp_reward, is_hidden)
                VALUES 
                ('Premier Quiz', 'Complétez votre premier quiz', '🎯', 'quiz', '{"quiz_count": 1}', 10, 0),
                ('Quiz Régulier', 'Complétez 10 quiz', '📚', 'quiz', '{"quiz_count": 10}', 50, 0),
                ('Perfectionniste', 'Obtenez 5 scores parfaits', '⭐', 'quiz', '{"perfect_scores": 5}', 100, 0)
            """)
            print("✓ Données de test ajoutées")
        else:
            print(f"✓ {achievement_count} achievements présents")
        
        # 6. Vérifier les données de test pour les challenges
        cursor.execute("SELECT COUNT(*) FROM challenges")
        challenge_count = cursor.fetchone()[0]
        
        if challenge_count == 0:
            print("✓ Ajout de données de test pour les challenges...")
            cursor.execute("""
                INSERT INTO challenges (title, description, challenge_type, xp_reward, requirements, is_active)
                VALUES 
                ('Défi Quotidien', 'Complétez un quiz aujourd''hui', 'daily', 20, '{"daily_quiz": 1}', 1),
                ('Défi Hebdomadaire', 'Complétez 5 quiz cette semaine', 'weekly', 100, '{"weekly_quiz": 5}', 1),
                ('Défi Mensuel', 'Complétez 20 quiz ce mois', 'monthly', 500, '{"monthly_quiz": 20}', 1)
            """)
            print("✓ Données de test ajoutées")
        else:
            print(f"✓ {challenge_count} challenges présents")
        
        conn.commit()
        print("\n✅ Corrections terminées avec succès")
        
    except Exception as e:
        print(f"❌ Erreur lors des corrections: {str(e)}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    fix_current_errors() 