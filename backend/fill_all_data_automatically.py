#!/usr/bin/env python3
"""
Script complet pour remplir AUTOMATIQUEMENT toutes les données nécessaires
pour l'évaluation initiale et les parcours d'apprentissage.
"""

import sys
import os
import sqlite3
import json
from datetime import datetime, timedelta
import random

# Ajouter le répertoire parent au path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def get_db_connection():
    """Créer une connexion à la base de données"""
    db_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'app.db')
    
    if not os.path.exists(db_path):
        print(f"❌ Base de données non trouvée: {db_path}")
        print("   Créez d'abord la base avec: python init_complete_db.py")
        return None
    
    return sqlite3.connect(db_path)

def create_assessment_questions():
    """Créer des questions d'évaluation initiale complètes"""
    print("📝 Création des questions d'évaluation initiale...")
    
    conn = get_db_connection()
    if not conn:
        return False
    
    cursor = conn.cursor()
    
    try:
        # Questions par matière et niveau
        questions_data = [
            # FRANÇAIS - Niveau Débutant
            {
                "question_text": "Quel est le genre du mot 'livre' dans 'un livre intéressant' ?",
                "question_type": "multiple_choice",
                "subject": "Français",
                "difficulty": "beginner",
                "options": json.dumps(["Masculin", "Féminin", "Neutre", "Variable"]),
                "correct_answer": "Masculin",
                "points": 1.0,
                "order": 1
            },
            {
                "question_text": "Conjuguez le verbe 'être' à la 1ère personne du singulier au présent :",
                "question_type": "multiple_choice",
                "subject": "Français",
                "difficulty": "beginner",
                "options": json.dumps(["Je suis", "Je es", "Je être", "Je suis être"]),
                "correct_answer": "Je suis",
                "points": 1.0,
                "order": 2
            },
            {
                "question_text": "Quel est le pluriel de 'cheval' ?",
                "question_type": "multiple_choice",
                "subject": "Français",
                "difficulty": "beginner",
                "options": json.dumps(["Chevals", "Chevaux", "Chevales", "Cheval"]),
                "correct_answer": "Chevaux",
                "points": 1.0,
                "order": 3
            },
            
            # FRANÇAIS - Niveau Intermédiaire
            {
                "question_text": "Identifiez la figure de style dans 'Le soleil souriait ce matin' :",
                "question_type": "multiple_choice",
                "subject": "Français",
                "difficulty": "intermediate",
                "options": json.dumps(["Métaphore", "Personnification", "Comparaison", "Hyperbole"]),
                "correct_answer": "Personnification",
                "points": 1.5,
                "order": 4
            },
            {
                "question_text": "Quel est le temps du verbe dans 'Il aurait aimé partir' ?",
                "question_type": "multiple_choice",
                "subject": "Français",
                "difficulty": "intermediate",
                "options": json.dumps(["Conditionnel présent", "Conditionnel passé", "Plus-que-parfait", "Futur antérieur"]),
                "correct_answer": "Conditionnel passé",
                "points": 1.5,
                "order": 5
            },
            
            # MATHÉMATIQUES - Niveau Débutant
            {
                "question_text": "Quel est le résultat de 15 + 27 ?",
                "question_type": "multiple_choice",
                "subject": "Mathématiques",
                "difficulty": "beginner",
                "options": json.dumps(["40", "42", "41", "43"]),
                "correct_answer": "42",
                "points": 1.0,
                "order": 6
            },
            {
                "question_text": "Combien font 8 × 7 ?",
                "question_type": "multiple_choice",
                "subject": "Mathématiques",
                "difficulty": "beginner",
                "options": json.dumps(["54", "56", "58", "60"]),
                "correct_answer": "56",
                "points": 1.0,
                "order": 7
            },
            {
                "question_text": "Quel est le double de 13 ?",
                "question_type": "multiple_choice",
                "subject": "Mathématiques",
                "difficulty": "beginner",
                "options": json.dumps(["25", "26", "27", "28"]),
                "correct_answer": "26",
                "points": 1.0,
                "order": 8
            },
            
            # MATHÉMATIQUES - Niveau Intermédiaire
            {
                "question_text": "Résolvez l'équation : 2x + 5 = 13",
                "question_type": "multiple_choice",
                "subject": "Mathématiques",
                "difficulty": "intermediate",
                "options": json.dumps(["x = 3", "x = 4", "x = 5", "x = 6"]),
                "correct_answer": "x = 4",
                "points": 1.5,
                "order": 9
            },
            {
                "question_text": "Quel est l'aire d'un carré de côté 6 cm ?",
                "question_type": "multiple_choice",
                "subject": "Mathématiques",
                "difficulty": "intermediate",
                "options": json.dumps(["24 cm²", "30 cm²", "36 cm²", "42 cm²"]),
                "correct_answer": "36 cm²",
                "points": 1.5,
                "order": 10
            },
            
            # SCIENCES - Niveau Débutant
            {
                "question_text": "Quel est l'état de l'eau à 100°C ?",
                "question_type": "multiple_choice",
                "subject": "Sciences",
                "difficulty": "beginner",
                "options": json.dumps(["Solide", "Liquide", "Gaz", "Plasma"]),
                "correct_answer": "Gaz",
                "points": 1.0,
                "order": 11
            },
            {
                "question_text": "Quel organe pompe le sang dans le corps ?",
                "question_type": "multiple_choice",
                "subject": "Sciences",
                "difficulty": "beginner",
                "options": json.dumps(["Le cerveau", "Le cœur", "Les poumons", "Le foie"]),
                "correct_answer": "Le cœur",
                "points": 1.0,
                "order": 12
            },
            
            # SCIENCES - Niveau Intermédiaire
            {
                "question_text": "Quel est le symbole chimique de l'or ?",
                "question_type": "multiple_choice",
                "subject": "Sciences",
                "difficulty": "intermediate",
                "options": json.dumps(["Ag", "Au", "Fe", "Cu"]),
                "correct_answer": "Au",
                "points": 1.5,
                "order": 13
            },
            {
                "question_text": "Quelle est la formule de l'énergie cinétique ?",
                "question_type": "multiple_choice",
                "subject": "Sciences",
                "difficulty": "intermediate",
                "options": json.dumps(["E = mgh", "E = ½mv²", "E = mc²", "E = Fd"]),
                "correct_answer": "E = ½mv²",
                "points": 1.5,
                "order": 14
            },
            
            # HISTOIRE - Niveau Débutant
            {
                "question_text": "En quelle année a eu lieu la Révolution française ?",
                "question_type": "multiple_choice",
                "subject": "Histoire",
                "difficulty": "beginner",
                "options": json.dumps(["1789", "1799", "1769", "1779"]),
                "correct_answer": "1789",
                "points": 1.0,
                "order": 15
            },
            {
                "question_text": "Qui était Napoléon Bonaparte ?",
                "question_type": "multiple_choice",
                "subject": "Histoire",
                "difficulty": "beginner",
                "options": json.dumps(["Un peintre", "Un écrivain", "Un empereur", "Un scientifique"]),
                "correct_answer": "Un empereur",
                "points": 1.0,
                "order": 16
            },
            
            # GÉOGRAPHIE - Niveau Débutant
            {
                "question_text": "Quelle est la capitale de la France ?",
                "question_type": "multiple_choice",
                "subject": "Géographie",
                "difficulty": "beginner",
                "options": json.dumps(["Lyon", "Marseille", "Paris", "Toulouse"]),
                "correct_answer": "Paris",
                "points": 1.0,
                "order": 17
            },
            {
                "question_text": "Quel fleuve traverse Paris ?",
                "question_type": "multiple_choice",
                "subject": "Géographie",
                "difficulty": "beginner",
                "options": json.dumps(["La Loire", "La Seine", "Le Rhône", "La Garonne"]),
                "correct_answer": "La Seine",
                "points": 1.0,
                "order": 18
            }
        ]
        
        # Insérer les questions
        for question in questions_data:
            cursor.execute("""
                INSERT OR IGNORE INTO assessment_questions 
                (question_text, question_type, subject, difficulty, options, correct_answer, points, "order")
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                question["question_text"],
                question["question_type"],
                question["subject"],
                question["difficulty"],
                question["options"],
                question["correct_answer"],
                question["points"],
                question["order"]
            ))
        
        conn.commit()
        print(f"✅ {len(questions_data)} questions d'évaluation créées")
        return True
        
    except Exception as e:
        print(f"❌ Erreur création questions: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()

def create_learning_paths():
    """Créer des parcours d'apprentissage complets"""
    print("🛤️ Création des parcours d'apprentissage...")
    
    conn = get_db_connection()
    if not conn:
        return False
    
    cursor = conn.cursor()
    
    try:
        # Parcours d'apprentissage par matière - ADAPTÉ À LA STRUCTURE RÉELLE
        learning_paths_data = [
            {
                "title": "Parcours Français Débutant",
                "description": "Apprentissage progressif du français pour débutants",
                "objectives": "Maîtriser les bases de la langue française",
                "subject": "Français",
                "level": "beginner",
                "difficulty": "easy",
                "estimated_duration": 30,
                "is_adaptive": True,
                "created_by": 1
            },
            {
                "title": "Parcours Français Intermédiaire",
                "description": "Perfectionnement en français pour niveau intermédiaire",
                "objectives": "Améliorer l'expression et la compréhension",
                "subject": "Français",
                "level": "intermediate",
                "difficulty": "medium",
                "estimated_duration": 45,
                "is_adaptive": True,
                "created_by": 1
            },
            {
                "title": "Parcours Mathématiques Débutant",
                "description": "Fondamentaux des mathématiques",
                "objectives": "Acquérir les bases du calcul et de la géométrie",
                "subject": "Mathématiques",
                "level": "beginner",
                "difficulty": "easy",
                "estimated_duration": 40,
                "is_adaptive": True,
                "created_by": 1
            },
            {
                "title": "Parcours Mathématiques Intermédiaire",
                "description": "Algèbre et géométrie avancées",
                "objectives": "Maîtriser l'algèbre et la géométrie avancée",
                "subject": "Mathématiques",
                "level": "intermediate",
                "difficulty": "medium",
                "estimated_duration": 50,
                "is_adaptive": True,
                "created_by": 1
            },
            {
                "title": "Parcours Sciences Débutant",
                "description": "Découverte des sciences naturelles",
                "objectives": "Comprendre les phénomènes naturels de base",
                "subject": "Sciences",
                "level": "beginner",
                "difficulty": "easy",
                "estimated_duration": 35,
                "is_adaptive": True,
                "created_by": 1
            },
            {
                "title": "Parcours Histoire-Géographie",
                "description": "Histoire de France et géographie mondiale",
                "objectives": "Découvrir l'histoire et la géographie",
                "subject": "Histoire-Géographie",
                "level": "beginner",
                "difficulty": "easy",
                "estimated_duration": 25,
                "is_adaptive": True,
                "created_by": 1
            }
        ]
        
        # Insérer les parcours - ADAPTÉ À LA STRUCTURE RÉELLE
        for path in learning_paths_data:
            cursor.execute("""
                INSERT OR IGNORE INTO learning_paths 
                (title, description, objectives, subject, level, difficulty, estimated_duration, is_adaptive, created_by)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                path["title"],
                path["description"],
                path["objectives"],
                path["subject"],
                path["level"],
                path["difficulty"],
                path["estimated_duration"],
                path["is_adaptive"],
                path["created_by"]
            ))
        
        conn.commit()
        print(f"✅ {len(learning_paths_data)} parcours d'apprentissage créés")
        return True
        
    except Exception as e:
        print(f"❌ Erreur création parcours: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()

def create_learning_path_steps():
    """Créer les étapes des parcours d'apprentissage"""
    print("📚 Création des étapes des parcours...")
    
    conn = get_db_connection()
    if not conn:
        return False
    
    cursor = conn.cursor()
    
    try:
        # Récupérer les IDs des parcours créés
        cursor.execute("SELECT id, subject, level FROM learning_paths")
        paths = cursor.fetchall()
        
        steps_data = []
        
        for path_id, subject, level in paths:
            if subject == "Français" and level == "beginner":
                steps_data.extend([
                    (path_id, 1, "Alphabet et sons", "Apprendre l'alphabet français et les sons de base", "lesson", None, 15, True, True),
                    (path_id, 2, "Vocabulaire de base", "Mots essentiels du quotidien", "quiz", None, 20, True, True),
                    (path_id, 3, "Grammaire simple", "Articles et pronoms personnels", "lesson", None, 25, True, True),
                    (path_id, 4, "Conjugaison présent", "Verbes être et avoir au présent", "quiz", None, 20, True, True),
                    (path_id, 5, "Évaluation finale", "Test de validation du niveau débutant", "assessment", None, 30, True, True)
                ])
            elif subject == "Mathématiques" and level == "beginner":
                steps_data.extend([
                    (path_id, 1, "Nombres de 1 à 100", "Compter et écrire les nombres", "lesson", None, 20, True, True),
                    (path_id, 2, "Addition et soustraction", "Opérations de base", "quiz", None, 25, True, True),
                    (path_id, 3, "Tables de multiplication", "Multiplications jusqu'à 10", "lesson", None, 30, True, True),
                    (path_id, 4, "Géométrie de base", "Formes et figures simples", "quiz", None, 25, True, True),
                    (path_id, 5, "Évaluation finale", "Test de validation du niveau débutant", "assessment", None, 35, True, True)
                ])
            elif subject == "Sciences" and level == "beginner":
                steps_data.extend([
                    (path_id, 1, "Les 5 sens", "Découverte des sens humains", "lesson", None, 20, True, True),
                    (path_id, 2, "Le cycle de l'eau", "Évaporation, condensation, précipitation", "quiz", None, 25, True, True),
                    (path_id, 3, "Les animaux", "Classification simple des animaux", "lesson", None, 30, True, True),
                    (path_id, 4, "Les plantes", "Parties d'une plante et photosynthèse", "quiz", None, 25, True, True),
                    (path_id, 5, "Évaluation finale", "Test de validation du niveau débutant", "assessment", None, 30, True, True)
                ])
        
        # Insérer les étapes - ADAPTÉ À LA STRUCTURE RÉELLE
        for step in steps_data:
            cursor.execute("""
                INSERT OR IGNORE INTO learning_path_steps 
                (learning_path_id, step_number, title, description, content_type, content_id, estimated_duration, is_required, is_active)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, step)
        
        conn.commit()
        print(f"✅ {len(steps_data)} étapes de parcours créées")
        return True
        
    except Exception as e:
        print(f"❌ Erreur création étapes: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()

def create_sample_assessments():
    """Créer des évaluations d'exemple pour les étudiants existants"""
    print("📋 Création d'évaluations d'exemple...")
    
    conn = get_db_connection()
    if not conn:
        return False
    
    cursor = conn.cursor()
    
    try:
        # Récupérer les étudiants existants
        cursor.execute("SELECT id FROM users WHERE role = 'student' LIMIT 5")
        students = cursor.fetchall()
        
        if not students:
            print("⚠️ Aucun étudiant trouvé pour créer des évaluations")
            return False
        
        # Créer des évaluations pour chaque étudiant
        for student_id, in students:
            # Évaluation initiale
            cursor.execute("""
                INSERT OR IGNORE INTO assessments 
                (student_id, assessment_type, title, description, status, started_at)
                VALUES (?, 'initial', 'Évaluation Initiale Complète', 'Test de positionnement dans toutes les matières', 'not_started', datetime('now'))
            """, (student_id,))
            
            # Évaluation continue
            cursor.execute("""
                INSERT OR IGNORE INTO assessments 
                (student_id, assessment_type, title, description, status, started_at)
                VALUES (?, 'continuous', 'Évaluation Continue - Mathématiques', 'Test des compétences en mathématiques', 'not_started', datetime('now'))
            """, (student_id,))
        
        conn.commit()
        print(f"✅ Évaluations créées pour {len(students)} étudiants")
        return True
        
    except Exception as e:
        print(f"❌ Erreur création évaluations: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()

def verify_data_creation():
    """Vérifier que toutes les données ont été créées"""
    print("\n🔍 Vérification de la création des données...")
    
    conn = get_db_connection()
    if not conn:
        return False
    
    cursor = conn.cursor()
    
    try:
        # Compter les éléments créés
        counts = {}
        
        cursor.execute("SELECT COUNT(*) FROM assessment_questions")
        counts["questions"] = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM learning_paths")
        counts["paths"] = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM learning_path_steps")
        counts["steps"] = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM assessments")
        counts["assessments"] = cursor.fetchone()[0]
        
        print("📊 Résumé des données créées:")
        print(f"   📝 Questions d'évaluation: {counts['questions']}")
        print(f"   🛤️ Parcours d'apprentissage: {counts['paths']}")
        print(f"   📚 Étapes de parcours: {counts['steps']}")
        print(f"   📋 Évaluations: {counts['assessments']}")
        
        # Vérifier que les tables ne sont plus vides
        success = all(count > 0 for count in counts.values())
        
        if success:
            print("✅ Toutes les données ont été créées avec succès!")
        else:
            print("⚠️ Certaines données n'ont pas été créées")
        
        return success
        
    except Exception as e:
        print(f"❌ Erreur vérification: {e}")
        return False
    finally:
        conn.close()

def main():
    """Fonction principale"""
    print("🚀 REMPLISSAGE AUTOMATIQUE COMPLET DE LA BASE DE DONNÉES")
    print("=" * 70)
    print("Ce script va créer AUTOMATIQUEMENT toutes les données nécessaires")
    print("pour que l'évaluation initiale et les parcours d'apprentissage")
    print("soient entièrement fonctionnels.")
    print("=" * 70)
    
    # Étape 1: Questions d'évaluation
    if not create_assessment_questions():
        print("❌ Échec de la création des questions")
        return False
    
    # Étape 2: Parcours d'apprentissage
    if not create_learning_paths():
        print("❌ Échec de la création des parcours")
        return False
    
    # Étape 3: Étapes des parcours
    if not create_learning_path_steps():
        print("❌ Échec de la création des étapes")
        return False
    
    # Étape 4: Évaluations d'exemple
    if not create_sample_assessments():
        print("❌ Échec de la création des évaluations")
        return False
    
    # Étape 5: Vérification
    if not verify_data_creation():
        print("❌ Vérification échouée")
        return False
    
    print("\n" + "=" * 70)
    print("🎉 REMPLISSAGE AUTOMATIQUE TERMINÉ AVEC SUCCÈS!")
    print("=" * 70)
    print("\n📋 VOTRE PLATEFORME EST MAINTENANT PRÊTE!")
    print("\n🚀 Prochaines étapes:")
    print("1. Démarrez le backend: python app.py")
    print("2. Démarrez le frontend: cd frontend && npm run dev")
    print("3. Testez l'évaluation initiale")
    print("4. Testez les parcours d'apprentissage")
    print("\n💡 Toutes les données sont maintenant réelles et fonctionnelles!")
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        if success:
            print("\n✅ Script terminé avec succès!")
            sys.exit(0)
        else:
            print("\n❌ Script échoué")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n⏹️ Script interrompu par l'utilisateur")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Erreur critique: {e}")
        sys.exit(1)
