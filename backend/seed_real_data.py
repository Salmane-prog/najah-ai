#!/usr/bin/env python3
"""
Script pour remplir la base de données avec du vrai contenu pédagogique
"""

import sys
import os
import json
from datetime import datetime
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.database import get_db
from models.quiz import Quiz, Question
from models.category import Category
from models.user import User, UserRole

def seed_real_data():
    print("=== REMPLISSAGE BASE DE DONNÉES ===")
    
    db = next(get_db())
    
    # 1. Créer les catégories par matière et niveau
    categories_data = [
        # Primaire
        {"name": "Mathématiques Primaire", "description": "Arithmétique et géométrie de base", "level": "primaire", "subject": "mathématiques"},
        {"name": "Français Primaire", "description": "Lecture, écriture et grammaire", "level": "primaire", "subject": "français"},
        {"name": "Anglais Primaire", "description": "Vocabulaire et expressions de base", "level": "primaire", "subject": "anglais"},
        
        # Collège
        {"name": "Mathématiques Collège", "description": "Algèbre et géométrie", "level": "collège", "subject": "mathématiques"},
        {"name": "Français Collège", "description": "Grammaire et littérature", "level": "collège", "subject": "français"},
        {"name": "Anglais Collège", "description": "Grammaire et communication", "level": "collège", "subject": "anglais"},
        {"name": "Histoire Collège", "description": "Histoire de France et du monde", "level": "collège", "subject": "histoire"},
        {"name": "Géographie Collège", "description": "Géographie physique et humaine", "level": "collège", "subject": "géographie"},
        {"name": "Sciences Collège", "description": "Physique, chimie et biologie", "level": "collège", "subject": "sciences"},
        
        # Lycée
        {"name": "Mathématiques Lycée", "description": "Analyse et géométrie avancée", "level": "lycée", "subject": "mathématiques"},
        {"name": "Français Lycée", "description": "Littérature et analyse de textes", "level": "lycée", "subject": "français"},
        {"name": "Anglais Lycée", "description": "Littérature anglaise et civilisation", "level": "lycée", "subject": "anglais"},
        {"name": "Histoire Lycée", "description": "Histoire moderne et contemporaine", "level": "lycée", "subject": "histoire"},
        {"name": "Géographie Lycée", "description": "Géographie économique et politique", "level": "lycée", "subject": "géographie"},
        {"name": "Physique Lycée", "description": "Mécanique, électricité et optique", "level": "lycée", "subject": "physique"},
        {"name": "Chimie Lycée", "description": "Chimie générale et organique", "level": "lycée", "subject": "chimie"},
        {"name": "Biologie Lycée", "description": "Biologie cellulaire et génétique", "level": "lycée", "subject": "biologie"},
    ]
    
    print("📚 Création des catégories...")
    categories = {}
    for cat_data in categories_data:
        category = Category(
            name=cat_data["name"],
            description=cat_data["description"]
        )
        db.add(category)
        db.flush()  # Pour obtenir l'ID
        categories[f"{cat_data['subject']}_{cat_data['level']}"] = category.id
        print(f"  ✅ {cat_data['name']}")
    
    # 2. Créer les quizzes par matière et niveau
    quizzes_data = [
        # Mathématiques Primaire
        {"title": "Addition et Soustraction", "description": "Opérations de base", "subject": "mathématiques", "level": "primaire", "difficulty": "débutant"},
        {"title": "Multiplication et Division", "description": "Tables de multiplication", "subject": "mathématiques", "level": "primaire", "difficulty": "intermédiaire"},
        {"title": "Géométrie de Base", "description": "Formes et mesures", "subject": "mathématiques", "level": "primaire", "difficulty": "débutant"},
        
        # Français Primaire
        {"title": "Lecture et Compréhension", "description": "Compréhension de textes simples", "subject": "français", "level": "primaire", "difficulty": "débutant"},
        {"title": "Grammaire de Base", "description": "Conjugaison et accords", "subject": "français", "level": "primaire", "difficulty": "intermédiaire"},
        {"title": "Vocabulaire", "description": "Enrichissement du vocabulaire", "subject": "français", "level": "primaire", "difficulty": "débutant"},
        
        # Anglais Primaire
        {"title": "Vocabulaire de Base", "description": "Mots du quotidien", "subject": "anglais", "level": "primaire", "difficulty": "débutant"},
        {"title": "Expressions Simples", "description": "Phrases courantes", "subject": "anglais", "level": "primaire", "difficulty": "intermédiaire"},
        
        # Mathématiques Collège
        {"title": "Algèbre de Base", "description": "Équations du premier degré", "subject": "mathématiques", "level": "collège", "difficulty": "débutant"},
        {"title": "Géométrie", "description": "Théorèmes et calculs", "subject": "mathématiques", "level": "collège", "difficulty": "intermédiaire"},
        {"title": "Statistiques", "description": "Moyennes et graphiques", "subject": "mathématiques", "level": "collège", "difficulty": "avancé"},
        
        # Français Collège
        {"title": "Grammaire Avancée", "description": "Analyse grammaticale", "subject": "français", "level": "collège", "difficulty": "intermédiaire"},
        {"title": "Littérature", "description": "Analyse de textes", "subject": "français", "level": "collège", "difficulty": "avancé"},
        
        # Sciences Collège
        {"title": "Physique de Base", "description": "Mécanique et énergie", "subject": "sciences", "level": "collège", "difficulty": "débutant"},
        {"title": "Chimie de Base", "description": "Atomes et molécules", "subject": "sciences", "level": "collège", "difficulty": "intermédiaire"},
        {"title": "Biologie", "description": "Le vivant et son évolution", "subject": "sciences", "level": "collège", "difficulty": "intermédiaire"},
    ]
    
    print("\n📝 Création des quizzes...")
    quizzes = {}
    for quiz_data in quizzes_data:
        quiz = Quiz(
            title=quiz_data["title"],
            description=quiz_data["description"],
            subject=quiz_data["subject"],
            level=quiz_data["level"],
            is_active=True
        )
        db.add(quiz)
        db.flush()
        quizzes[f"{quiz_data['subject']}_{quiz_data['level']}_{quiz_data['title']}"] = quiz.id
        print(f"  ✅ {quiz_data['title']}")
    
    # 3. Créer les questions par quiz
    questions_data = [
        # Mathématiques Primaire - Addition et Soustraction
        {
            "quiz_key": "mathématiques_primaire_Addition et Soustraction",
            "questions": [
                {
                    "question_text": "Combien font 5 + 3 ?",
                    "options": ["7", "8", "9", "10"],
                    "correct_answer": "8",
                    "points": 1,
                    "difficulty": "débutant"
                },
                {
                    "question_text": "Combien font 12 - 4 ?",
                    "options": ["6", "7", "8", "9"],
                    "correct_answer": "8",
                    "points": 1,
                    "difficulty": "débutant"
                },
                {
                    "question_text": "Quel est le résultat de 15 + 7 ?",
                    "options": ["20", "21", "22", "23"],
                    "correct_answer": "22",
                    "points": 2,
                    "difficulty": "intermédiaire"
                }
            ]
        },
        
        # Français Primaire - Lecture et Compréhension
        {
            "quiz_key": "français_primaire_Lecture et Compréhension",
            "questions": [
                {
                    "question_text": "Dans la phrase 'Le chat dort sur le canapé', quel est le sujet ?",
                    "options": ["Le chat", "dort", "sur", "le canapé"],
                    "correct_answer": "Le chat",
                    "points": 1,
                    "difficulty": "débutant"
                },
                {
                    "question_text": "Quel est le verbe dans la phrase 'Les enfants jouent dans le jardin' ?",
                    "options": ["Les enfants", "jouent", "dans", "le jardin"],
                    "correct_answer": "jouent",
                    "points": 1,
                    "difficulty": "débutant"
                },
                {
                    "question_text": "Complétez : 'Le petit garçon ___ dans la rue.'",
                    "options": ["marcher", "marche", "marché", "marchait"],
                    "correct_answer": "marche",
                    "points": 2,
                    "difficulty": "intermédiaire"
                }
            ]
        },
        
        # Anglais Primaire - Vocabulaire de Base
        {
            "quiz_key": "anglais_primaire_Vocabulaire de Base",
            "questions": [
                {
                    "question_text": "Comment dit-on 'bonjour' en anglais ?",
                    "options": ["Goodbye", "Hello", "Thank you", "Please"],
                    "correct_answer": "Hello",
                    "points": 1,
                    "difficulty": "débutant"
                },
                {
                    "question_text": "Quel est le mot anglais pour 'chat' ?",
                    "options": ["Dog", "Cat", "Bird", "Fish"],
                    "correct_answer": "Cat",
                    "points": 1,
                    "difficulty": "débutant"
                },
                {
                    "question_text": "Comment dit-on 'merci' en anglais ?",
                    "options": ["Please", "Thank you", "Sorry", "Excuse me"],
                    "correct_answer": "Thank you",
                    "points": 1,
                    "difficulty": "débutant"
                }
            ]
        },
        
        # Mathématiques Collège - Algèbre de Base
        {
            "quiz_key": "mathématiques_collège_Algèbre de Base",
            "questions": [
                {
                    "question_text": "Résolvez l'équation : x + 5 = 12",
                    "options": ["x = 5", "x = 7", "x = 12", "x = 17"],
                    "correct_answer": "x = 7",
                    "points": 2,
                    "difficulty": "intermédiaire"
                },
                {
                    "question_text": "Quelle est la valeur de x dans l'équation 2x = 10 ?",
                    "options": ["x = 3", "x = 5", "x = 8", "x = 10"],
                    "correct_answer": "x = 5",
                    "points": 2,
                    "difficulty": "intermédiaire"
                },
                {
                    "question_text": "Résolvez : 3x - 6 = 9",
                    "options": ["x = 3", "x = 5", "x = 7", "x = 9"],
                    "correct_answer": "x = 5",
                    "points": 3,
                    "difficulty": "avancé"
                }
            ]
        },
        
        # Sciences Collège - Physique de Base
        {
            "quiz_key": "sciences_collège_Physique de Base",
            "questions": [
                {
                    "question_text": "Quelle est l'unité de mesure de la force ?",
                    "options": ["Le mètre", "Le newton", "Le joule", "Le watt"],
                    "correct_answer": "Le newton",
                    "points": 2,
                    "difficulty": "intermédiaire"
                },
                {
                    "question_text": "Qu'est-ce que l'énergie cinétique ?",
                    "options": ["L'énergie de mouvement", "L'énergie de position", "L'énergie thermique", "L'énergie électrique"],
                    "correct_answer": "L'énergie de mouvement",
                    "points": 2,
                    "difficulty": "intermédiaire"
                },
                {
                    "question_text": "Quelle est la formule de l'énergie cinétique ?",
                    "options": ["E = mgh", "E = ½mv²", "E = mc²", "E = Fd"],
                    "correct_answer": "E = ½mv²",
                    "points": 3,
                    "difficulty": "avancé"
                }
            ]
        }
    ]
    
    print("\n❓ Création des questions...")
    for quiz_questions in questions_data:
        quiz_id = quizzes.get(quiz_questions["quiz_key"])
        if quiz_id:
            for q_data in quiz_questions["questions"]:
                question = Question(
                    quiz_id=quiz_id,
                    question_text=q_data["question_text"],
                    options=json.dumps(q_data["options"]),
                    correct_answer=q_data["correct_answer"],
                    points=q_data["points"],
                    difficulty=q_data["difficulty"]
                )
                db.add(question)
                print(f"  ✅ Question: {q_data['question_text'][:50]}...")
    
    db.commit()
    print(f"\n🎉 Base de données remplie avec succès!")
    print(f"  📚 {len(categories_data)} catégories créées")
    print(f"  📝 {len(quizzes_data)} quizzes créés")
    print(f"  ❓ {sum(len(q['questions']) for q in questions_data)} questions créées")
    
    db.close()

if __name__ == "__main__":
    seed_real_data() 