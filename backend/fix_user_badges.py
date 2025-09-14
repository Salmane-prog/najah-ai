#!/usr/bin/env python3
"""
Script pour corriger la table user_badge et copier les données
"""

import sqlite3
import os

def fix_user_badges():
    """Corriger la table user_badge et copier les données"""
    
    print("🔧 Correction de la table user_badge...")
    
    # Chemin vers la base de données
    db_path = "../data/app.db"
    
    if not os.path.exists(db_path):
        print(f"❌ Base de données non trouvée : {db_path}")
        return
    
    try:
        # Connexion à la base de données
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Vérifier la structure de user_badges
        print("📋 Vérification de la structure de user_badges...")
        cursor.execute("PRAGMA table_info(user_badges)")
        user_badges_columns = [row[1] for row in cursor.fetchall()]
        print(f"   Colonnes de user_badges : {user_badges_columns}")
        
        # Vérifier la structure de user_badge
        print("📋 Vérification de la structure de user_badge...")
        cursor.execute("PRAGMA table_info(user_badge)")
        user_badge_columns = [row[1] for row in cursor.fetchall()]
        print(f"   Colonnes de user_badge : {user_badge_columns}")
        
        # Supprimer la table user_badge existante et la recréer
        print("🔄 Recréation de la table user_badge...")
        cursor.execute("DROP TABLE IF EXISTS user_badge")
        
        # Créer la table user_badge avec la bonne structure
        cursor.execute("""
            CREATE TABLE user_badge (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                badge_id INTEGER NOT NULL,
                progression REAL DEFAULT 0.0,
                awarded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id),
                FOREIGN KEY (badge_id) REFERENCES badges (id)
            )
        """)
        print("   ✅ Table user_badge recréée")
        
        # Copier les données de user_badges vers user_badge
        print("📋 Copie des données...")
        
        # Vérifier quelles colonnes sont disponibles dans user_badges
        if 'awarded_at' in user_badges_columns:
            cursor.execute("""
                INSERT INTO user_badge (user_id, badge_id, progression, awarded_at)
                SELECT user_id, badge_id, progression, awarded_at FROM user_badges
            """)
        else:
            # Si awarded_at n'existe pas, utiliser la date actuelle
            cursor.execute("""
                INSERT INTO user_badge (user_id, badge_id, progression)
                SELECT user_id, badge_id, progression FROM user_badges
            """)
        
        # Vérifier le nombre de données copiées
        cursor.execute("SELECT COUNT(*) FROM user_badge")
        count = cursor.fetchone()[0]
        print(f"   ✅ {count} enregistrements copiés")
        
        # Afficher les données copiées
        cursor.execute("""
            SELECT ub.id, ub.user_id, u.username, ub.badge_id, b.name, ub.progression
            FROM user_badge ub
            JOIN users u ON ub.user_id = u.id
            JOIN badges b ON ub.badge_id = b.id
        """)
        
        print("📊 Données copiées :")
        for row in cursor.fetchall():
            print(f"   • {row[2]} -> {row[4]} (progression: {row[5]}%)")
        
        # Valider les changements
        conn.commit()
        
        print("\n🎉 Table user_badge corrigée avec succès !")
        
    except Exception as e:
        print(f"❌ Erreur lors de la correction : {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    fix_user_badges() 