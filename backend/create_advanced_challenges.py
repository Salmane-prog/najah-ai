#!/usr/bin/env python3
"""
Script pour créer des défis et badges avancés
"""

import sqlite3
import json
from datetime import datetime, timedelta

def create_advanced_challenges():
    db_path = "../data/app.db"
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("🏆 Création des défis avancés...")
        
        # Défis pour les étudiants
        challenges = [
            {
                "title": "Défi Quiz Master",
                "description": "Complétez 10 quiz avec un score moyen de 80% ou plus",
                "challenge_type": "quiz",
                "difficulty": "medium",
                "points_reward": 150,
                "requirements": {"quiz_count": 10, "min_average_score": 80},
                "start_date": datetime.utcnow(),
                "end_date": datetime.utcnow() + timedelta(days=30),
                "is_active": 1
            },
            {
                "title": "Streak de 7 jours",
                "description": "Connectez-vous et complétez une activité pendant 7 jours consécutifs",
                "challenge_type": "streak",
                "difficulty": "easy",
                "points_reward": 100,
                "requirements": {"streak_days": 7},
                "start_date": datetime.utcnow(),
                "end_date": datetime.utcnow() + timedelta(days=60),
                "is_active": 1
            },
            {
                "title": "Explorateur de Contenu",
                "description": "Consultez 20 contenus différents",
                "challenge_type": "content",
                "difficulty": "medium",
                "points_reward": 120,
                "requirements": {"content_views": 20},
                "start_date": datetime.utcnow(),
                "end_date": datetime.utcnow() + timedelta(days=45),
                "is_active": 1
            },
            {
                "title": "Perfectionniste",
                "description": "Obtenez un score parfait (100%) sur 5 quiz différents",
                "challenge_type": "quiz",
                "difficulty": "hard",
                "points_reward": 300,
                "requirements": {"perfect_scores": 5},
                "start_date": datetime.utcnow(),
                "end_date": datetime.utcnow() + timedelta(days=90),
                "is_active": 1
            },
            {
                "title": "Aide aux Autres",
                "description": "Envoyez 10 messages d'aide à d'autres étudiants",
                "challenge_type": "social",
                "difficulty": "medium",
                "points_reward": 80,
                "requirements": {"help_messages": 10},
                "start_date": datetime.utcnow(),
                "end_date": datetime.utcnow() + timedelta(days=40),
                "is_active": 1
            },
            {
                "title": "Marathon d'Apprentissage",
                "description": "Passez 5 heures à apprendre en une semaine",
                "challenge_type": "time",
                "difficulty": "hard",
                "points_reward": 250,
                "requirements": {"learning_hours": 5, "timeframe": "week"},
                "start_date": datetime.utcnow(),
                "end_date": datetime.utcnow() + timedelta(days=7),
                "is_active": 1
            },
            {
                "title": "Défi Multimatière",
                "description": "Complétez des quiz dans 5 matières différentes",
                "challenge_type": "diversity",
                "difficulty": "medium",
                "points_reward": 180,
                "requirements": {"subjects_count": 5},
                "start_date": datetime.utcnow(),
                "end_date": datetime.utcnow() + timedelta(days=50),
                "is_active": 1
            },
            {
                "title": "Progression Constante",
                "description": "Améliorez votre score moyen de 10% en 2 semaines",
                "challenge_type": "improvement",
                "difficulty": "hard",
                "points_reward": 200,
                "requirements": {"score_improvement": 10, "timeframe": "weeks", "duration": 2},
                "start_date": datetime.utcnow(),
                "end_date": datetime.utcnow() + timedelta(days=14),
                "is_active": 1
            }
        ]
        
        for challenge in challenges:
            cursor.execute("""
                INSERT INTO challenges (title, description, challenge_type, difficulty, 
                                     points_reward, requirements, start_date, end_date, 
                                     is_active, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                challenge["title"],
                challenge["description"],
                challenge["challenge_type"],
                challenge["difficulty"],
                challenge["points_reward"],
                json.dumps(challenge["requirements"]),
                challenge["start_date"],
                challenge["end_date"],
                challenge["is_active"],
                datetime.utcnow()
            ))
        
        print("✅ Défis créés avec succès!")
        
        # Créer des badges avancés
        print("🏅 Création des badges avancés...")
        
        badges = [
            {
                "name": "Quiz Master",
                "description": "Complétez 50 quiz avec succès",
                "icon": "🎯",
                "category": "achievement",
                "points_reward": 100
            },
            {
                "name": "Perfectionniste",
                "description": "Obtenez 10 scores parfaits",
                "icon": "⭐",
                "category": "achievement",
                "points_reward": 200
            },
            {
                "name": "Streak Master",
                "description": "Maintenez une série de 30 jours",
                "icon": "🔥",
                "category": "streak",
                "points_reward": 300
            },
            {
                "name": "Explorateur",
                "description": "Consultez 100 contenus différents",
                "icon": "🗺️",
                "category": "exploration",
                "points_reward": 150
            },
            {
                "name": "Aide aux Autres",
                "description": "Aidez 50 autres étudiants",
                "icon": "🤝",
                "category": "social",
                "points_reward": 120
            },
            {
                "name": "Multimatière",
                "description": "Excellez dans 8 matières différentes",
                "icon": "📚",
                "category": "diversity",
                "points_reward": 250
            },
            {
                "name": "Progression Rapide",
                "description": "Améliorez votre score de 50% en un mois",
                "icon": "📈",
                "category": "improvement",
                "points_reward": 400
            },
            {
                "name": "Marathon d'Apprentissage",
                "description": "Passez 50 heures à apprendre",
                "icon": "⏰",
                "category": "time",
                "points_reward": 500
            },
            {
                "name": "Premier de Classe",
                "description": "Soyez le meilleur de votre classe pendant 3 mois",
                "icon": "👑",
                "category": "leadership",
                "points_reward": 1000
            },
            {
                "name": "Innovateur",
                "description": "Créez 10 contenus originaux",
                "icon": "💡",
                "category": "creation",
                "points_reward": 300
            }
        ]
        
        for badge in badges:
            cursor.execute("""
                INSERT INTO badges (name, description, icon, category, points_reward, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                badge["name"],
                badge["description"],
                badge["icon"],
                badge["category"],
                badge["points_reward"],
                datetime.utcnow()
            ))
        
        print("✅ Badges créés avec succès!")
        
        # Créer des classements dynamiques
        print("🏆 Création des classements dynamiques...")
        
        leaderboards = [
            {
                "name": "Classement Hebdomadaire",
                "description": "Top des étudiants de la semaine",
                "leaderboard_type": "weekly",
                "period": "weekly",
                "is_active": 1
            },
            {
                "name": "Classement Mensuel",
                "description": "Top des étudiants du mois",
                "leaderboard_type": "monthly",
                "period": "monthly",
                "is_active": 1
            },
            {
                "name": "Classement par Matière",
                "description": "Meilleurs par matière",
                "leaderboard_type": "subject",
                "period": "monthly",
                "is_active": 1
            },
            {
                "name": "Classement Progression",
                "description": "Plus grande amélioration",
                "leaderboard_type": "improvement",
                "period": "monthly",
                "is_active": 1
            }
        ]
        
        for leaderboard in leaderboards:
            cursor.execute("""
                INSERT INTO leaderboards (name, description, leaderboard_type, period, is_active, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                leaderboard["name"],
                leaderboard["description"],
                leaderboard["leaderboard_type"],
                leaderboard["period"],
                leaderboard["is_active"],
                datetime.utcnow()
            ))
        
        print("✅ Classements créés avec succès!")
        
        conn.commit()
        conn.close()
        
        print("🎉 Toutes les fonctionnalités avancées ont été créées!")
        
    except Exception as e:
        print(f"❌ Erreur lors de la création: {str(e)}")

if __name__ == "__main__":
    create_advanced_challenges() 