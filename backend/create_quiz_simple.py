#!/usr/bin/env python3
"""
Script simplifié pour créer un quiz avec 10 questions
"""
import sqlite3
import os
from datetime import datetime

def create_quiz_simple():
    # Chemin vers la base de données
    db_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'app.db')
    
    if not os.path.exists(db_path):
        print(f"❌ Base de données non trouvée: {db_path}")
        return False
    
    print(f"🔍 Création d'un quiz dans: {db_path}")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # 1. Trouver un professeur
        cursor.execute("SELECT id FROM users WHERE role = 'teacher' LIMIT 1")
        teacher = cursor.fetchone()
        if not teacher:
            print("❌ Aucun professeur trouvé")
            return False
        
        teacher_id = teacher[0]
        print(f"✅ Professeur trouvé: ID {teacher_id}")
        
        # 2. Créer le quiz
        quiz_data = {
            'title': 'Quiz Antigone - 10 Questions',
            'description': 'Quiz sur Antigone avec 10 questions',
            'subject': 'Antigone',
            'level': 'medium',
            'created_by': teacher_id,
            'time_limit': 20,
            'total_points': 20,
            'created_at': datetime.now().isoformat(),
            'is_active': 1
        }
        
        cursor.execute("""
            INSERT INTO quizzes (title, description, subject, level, created_by, time_limit, total_points, created_at, is_active)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            quiz_data['title'], quiz_data['description'], quiz_data['subject'], 
            quiz_data['level'], quiz_data['created_by'], quiz_data['time_limit'],
            quiz_data['total_points'], quiz_data['created_at'], quiz_data['is_active']
        ))
        
        quiz_id = cursor.lastrowid
        print(f"✅ Quiz créé: ID {quiz_id}")
        
        # 3. Créer les 10 questions
        questions_data = [
            ("Qui est le personnage principal d'Antigone ?", "mcq", 2, 0, ["Antigone", "Créon", "Ismène", "Hémon"]),
            ("Quel est le conflit principal dans Antigone ?", "mcq", 2, 1, ["Amour vs Haine", "Loi divine vs Loi humaine", "Pouvoir vs Liberté", "Vie vs Mort"]),
            ("Qui a interdit l'enterrement de Polynice ?", "mcq", 2, 1, ["Antigone", "Créon", "Ismène", "Hémon"]),
            ("Quelle est la punition d'Antigone ?", "mcq", 2, 2, ["Exil", "Mort par lapidation", "Emprisonnement", "Mort par pendaison"]),
            ("Qui est le fils de Créon ?", "mcq", 2, 2, ["Polynice", "Étéocle", "Hémon", "Thésée"]),
            ("Quelle est la relation entre Antigone et Ismène ?", "mcq", 2, 1, ["Cousines", "Sœurs", "Mère et fille", "Amiés"]),
            ("Quel est le thème principal d'Antigone ?", "mcq", 2, 2, ["L'amour", "La justice", "La désobéissance", "La famille"]),
            ("Qui meurt en premier dans la pièce ?", "mcq", 2, 0, ["Antigone", "Hémon", "Eurydice", "Créon"]),
            ("Quel est le rôle de Tirésias dans la pièce ?", "mcq", 2, 1, ["Roi", "Prophète", "Garde", "Prêtre"]),
            ("Comment se termine la pièce ?", "mcq", 2, 2, ["Créon devient roi", "Antigone survit", "Créon se suicide", "Tout le monde meurt"])
        ]
        
        for i, (question_text, question_type, points, correct_answer, options) in enumerate(questions_data):
            cursor.execute("""
                INSERT INTO questions (quiz_id, question_text, question_type, points, "order", options, correct_answer)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (quiz_id, question_text, question_type, points, i+1, str(options), correct_answer))
        
        conn.commit()
        
        print(f"✅ 10 questions créées pour le quiz {quiz_id}")
        print(f"📊 Quiz '{quiz_data['title']}' créé avec succès!")
        print(f"   - ID: {quiz_id}")
        print(f"   - Sujet: {quiz_data['subject']}")
        print(f"   - Niveau: {quiz_data['level']}")
        print(f"   - Temps: {quiz_data['time_limit']} min")
        print(f"   - Questions: 10")
        print(f"   - Points totaux: {quiz_data['total_points']}")
        
        return quiz_id
        
    except Exception as e:
        print(f"❌ Erreur lors de la création du quiz: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()

if __name__ == "__main__":
    print("🎯 Création d'un nouveau quiz avec 10 questions...")
    quiz_id = create_quiz_simple()
    if quiz_id:
        print(f"\n✅ Quiz créé avec succès! ID: {quiz_id}")
        print(f"   Tu peux maintenant l'assigner depuis le dashboard prof.")
    else:
        print(f"\n❌ Échec de la création du quiz.") 