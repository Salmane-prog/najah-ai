from sqlalchemy.orm import Session
from core.database import SessionLocal
from models.badge import Badge

def init_badges():
    db = SessionLocal()
    try:
        # Vérifier si des badges existent déjà
        existing_badges = db.query(Badge).count()
        if existing_badges > 0:
            print(f"✅ {existing_badges} badges existent déjà dans la base de données")
            return

        # Créer des badges de test
        badges_data = [
            {
                "name": "Premier Quiz",
                "description": "A complété son premier quiz avec succès",
                "criteria": "quiz_completed >= 1",
                "image_url": "/badges/first-quiz.png",
                "secret": False
            },
            {
                "name": "Élève Assidu",
                "description": "A participé à 10 sessions d'apprentissage",
                "criteria": "learning_sessions >= 10",
                "image_url": "/badges/dedicated-student.png",
                "secret": False
            },
            {
                "name": "Maître des Sciences",
                "description": "A obtenu 100% dans un quiz de sciences",
                "criteria": "science_quiz_score = 100",
                "image_url": "/badges/science-master.png",
                "secret": False
            },
            {
                "name": "Littéraire Confirmé",
                "description": "A complété 5 quiz de littérature",
                "criteria": "literature_quizzes >= 5",
                "image_url": "/badges/literature-expert.png",
                "secret": False
            },
            {
                "name": "Badge Secret",
                "description": "Un badge mystérieux à découvrir",
                "criteria": "secret_achievement",
                "image_url": None,
                "secret": True
            }
        ]

        for badge_data in badges_data:
            badge = Badge(**badge_data)
            db.add(badge)

        db.commit()
        print(f"✅ {len(badges_data)} badges ont été créés avec succès")
        
        # Afficher les badges créés
        badges = db.query(Badge).all()
        print("\n📋 Badges disponibles :")
        for badge in badges:
            print(f"  - {badge.name}: {badge.description}")

    except Exception as e:
        print(f"❌ Erreur lors de l'initialisation des badges: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_badges() 