from sqlalchemy.orm import Session
from core.database import SessionLocal
from models.badge import Badge
from models.user import User, UserRole
from models.class_group import ClassGroup
from models.content import Content
from models.learning_path import LearningPath
from models.category import Category
from models.quiz import Quiz
from core.security import get_password_hash
from datetime import datetime

def init_test_data():
    db = SessionLocal()
    try:
        print("🚀 Initialisation des données de test...")
        
        # 1. Initialiser les badges
        init_badges(db)
        
        # 2. Initialiser les catégories
        init_categories(db)
        
        # 3. Initialiser les contenus
        init_contents(db)
        
        # 4. Initialiser les quiz
        init_quizzes(db)
        
        # 5. Initialiser les parcours d'apprentissage
        init_learning_paths(db)
        
        # 6. Initialiser les classes
        init_classes(db)
        
        print("✅ Toutes les données de test ont été initialisées avec succès !")
        
    except Exception as e:
        print(f"❌ Erreur lors de l'initialisation: {e}")
        db.rollback()
    finally:
        db.close()

def init_badges(db: Session):
    existing_badges = db.query(Badge).count()
    if existing_badges > 0:
        print(f"✅ {existing_badges} badges existent déjà")
        return

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
        }
    ]

    for badge_data in badges_data:
        badge = Badge(**badge_data)
        db.add(badge)

    db.commit()
    print(f"✅ {len(badges_data)} badges créés")

def init_categories(db: Session):
    existing_categories = db.query(Category).count()
    if existing_categories > 0:
        print(f"✅ {existing_categories} catégories existent déjà")
        return

    categories_data = [
        {"name": "Littérature", "description": "Cours de littérature française"},
        {"name": "Mathématiques", "description": "Cours de mathématiques"},
        {"name": "Sciences", "description": "Cours de sciences naturelles"},
        {"name": "Histoire", "description": "Cours d'histoire"},
        {"name": "Géographie", "description": "Cours de géographie"}
    ]

    for cat_data in categories_data:
        category = Category(**cat_data)
        db.add(category)

    db.commit()
    print(f"✅ {len(categories_data)} catégories créées")

def init_contents(db: Session):
    existing_contents = db.query(Content).count()
    if existing_contents > 0:
        print(f"✅ {existing_contents} contenus existent déjà")
        return

    # Récupérer les catégories
    literature_cat = db.query(Category).filter(Category.name == "Littérature").first()
    sciences_cat = db.query(Category).filter(Category.name == "Sciences").first()

    contents_data = [
        {
            "title": "Antigone - Acte 1",
            "description": "QCM sur Antigone",
            "content_type": "quiz",
            "subject": "Littérature",
            "difficulty": "medium",
            "category_id": literature_cat.id if literature_cat else 1
        },
        {
            "title": "Figures de Style",
            "description": "QCM sur les figures de style",
            "content_type": "quiz",
            "subject": "Littérature",
            "difficulty": "easy",
            "category_id": literature_cat.id if literature_cat else 1
        },
        {
            "title": "QCM Sciences",
            "description": "QCM sur les bases des sciences",
            "content_type": "quiz",
            "subject": "Sciences",
            "difficulty": "easy",
            "category_id": sciences_cat.id if sciences_cat else 3
        }
    ]

    for content_data in contents_data:
        content = Content(**content_data)
        db.add(content)

    db.commit()
    print(f"✅ {len(contents_data)} contenus créés")

def init_quizzes(db: Session):
    existing_quizzes = db.query(Quiz).count()
    if existing_quizzes > 0:
        print(f"✅ {existing_quizzes} quiz existent déjà")
        return

    quizzes_data = [
        {
            "title": "Quiz Littérature - Poésie",
            "description": "Test sur la poésie française",
            "subject": "Littérature",
            "difficulty": "medium",
            "questions_count": 10
        },
        {
            "title": "Quiz Mathématiques - Fractions",
            "description": "Test sur les fractions",
            "subject": "Mathématiques",
            "difficulty": "easy",
            "questions_count": 8
        },
        {
            "title": "Quiz Histoire - Révolution",
            "description": "Test sur la Révolution française",
            "subject": "Histoire",
            "difficulty": "hard",
            "questions_count": 12
        }
    ]

    for quiz_data in quizzes_data:
        quiz = Quiz(**quiz_data)
        db.add(quiz)

    db.commit()
    print(f"✅ {len(quizzes_data)} quiz créés")

def init_learning_paths(db: Session):
    existing_paths = db.query(LearningPath).count()
    if existing_paths > 0:
        print(f"✅ {existing_paths} parcours existent déjà")
        return

    paths_data = [
        {
            "title": "Parcours Littérature",
            "description": "Découverte de la littérature",
            "subject": "Littérature",
            "difficulty": "medium",
            "estimated_duration": 120
        },
        {
            "title": "Parcours Sciences",
            "description": "Initiation aux sciences",
            "subject": "Sciences",
            "difficulty": "easy",
            "estimated_duration": 90
        },
        {
            "title": "Parcours Mathématiques",
            "description": "Fondamentaux des mathématiques",
            "subject": "Mathématiques",
            "difficulty": "medium",
            "estimated_duration": 150
        }
    ]

    for path_data in paths_data:
        path = LearningPath(**path_data)
        db.add(path)

    db.commit()
    print(f"✅ {len(paths_data)} parcours d'apprentissage créés")

def init_classes(db: Session):
    existing_classes = db.query(ClassGroup).count()
    if existing_classes > 0:
        print(f"✅ {existing_classes} classes existent déjà")
        return

    classes_data = [
        {
            "name": "Seconde A",
            "description": "Classe de seconde générale",
            "level": "Seconde",
            "capacity": 30
        },
        {
            "name": "Première S",
            "description": "Classe de première scientifique",
            "level": "Première",
            "capacity": 25
        },
        {
            "name": "Terminale L",
            "description": "Classe de terminale littéraire",
            "level": "Terminale",
            "capacity": 20
        }
    ]

    for class_data in classes_data:
        class_group = ClassGroup(**class_data)
        db.add(class_group)

    db.commit()
    print(f"✅ {len(classes_data)} classes créées")

if __name__ == "__main__":
    init_test_data() 