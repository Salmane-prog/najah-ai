#!/usr/bin/env python3
"""
Script pour ajouter des questions d'exemple aux tests adaptatifs
"""

import sqlite3
import os

def add_sample_questions():
    # Chemin vers la base de données
    db_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'app.db')
    print(f"🔧 Ajout de questions d'exemple aux tests adaptatifs")
    print(f"📁 Base de données: {db_path}")
    print("=" * 60)
    
    try:
        # Connexion à la base
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Vérifier si la table adaptive_questions existe
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='adaptive_questions'")
        if not cursor.fetchone():
            print("❌ Table 'adaptive_questions' n'existe pas!")
            return
        
        print("✅ Table 'adaptive_questions' existe")
        
        # Vérifier les tests existants
        cursor.execute("SELECT id, title FROM adaptive_tests WHERE is_active = 1")
        tests = cursor.fetchall()
        
        if not tests:
            print("❌ Aucun test actif trouvé!")
            return
        
        print(f"📊 Tests trouvés: {len(tests)}")
        for test in tests:
            print(f"  - ID: {test[0]}, Titre: {test[1]}")
        
        # Ajouter des questions pour chaque test
        for test_id, test_title in tests:
            print(f"\n🔧 Ajout de questions pour: {test_title}")
            
            # Compter les questions existantes
            cursor.execute("SELECT COUNT(*) FROM adaptive_questions WHERE test_id = ?", (test_id,))
            existing_count = cursor.fetchone()[0]
            
            if existing_count > 0:
                print(f"  ⚠️  {existing_count} questions existent déjà, passage au suivant")
                continue
            
            # Ajouter des questions selon le sujet
            if "Français" in test_title or "Grammaire" in test_title:
                questions = [
                    ("Conjuguez le verbe 'être' au présent de l'indicatif", "être", "conjugaison", 3, "Je suis, tu es, il est, nous sommes, vous êtes, ils sont"),
                    ("Quelle est la nature grammaticale du mot 'rapidement' ?", "adverbe", "grammaire", 4, "C'est un adverbe de manière qui modifie le verbe"),
                    ("Identifiez le sujet dans la phrase : 'Les enfants jouent dans le jardin'", "Les enfants", "analyse", 2, "Le sujet est 'Les enfants', groupe nominal"),
                    ("Conjuguez le verbe 'avoir' à l'imparfait", "avoir", "conjugaison", 3, "J'avais, tu avais, il avait, nous avions, vous aviez, ils avaient"),
                    ("Quelle est la fonction de 'très' dans 'très beau' ?", "adverbe d'intensité", "grammaire", 4, "'Très' est un adverbe d'intensité qui modifie l'adjectif 'beau'")
                ]
            elif "Mathématiques" in test_title or "Algèbre" in test_title:
                questions = [
                    ("Résolvez l'équation : 2x + 5 = 13", "x = 4", "équations", 4, "2x + 5 = 13 → 2x = 8 → x = 4"),
                    ("Calculez : 3(x + 2) - 2(x - 1)", "x + 8", "développement", 5, "3(x + 2) - 2(x - 1) = 3x + 6 - 2x + 2 = x + 8"),
                    ("Factorisez : x² - 4", "(x + 2)(x - 2)", "factorisation", 6, "x² - 4 = x² - 2² = (x + 2)(x - 2)"),
                    ("Résolvez : 5x - 3 = 2x + 9", "x = 4", "équations", 3, "5x - 3 = 2x + 9 → 3x = 12 → x = 4"),
                    ("Calculez : (2x + 1)²", "4x² + 4x + 1", "identités", 7, "(2x + 1)² = (2x)² + 2×2x×1 + 1² = 4x² + 4x + 1")
                ]
            elif "Histoire" in test_title:
                questions = [
                    ("En quelle année a eu lieu la prise de la Bastille ?", "1789", "chronologie", 3, "La prise de la Bastille a eu lieu le 14 juillet 1789"),
                    ("Qui était le roi de France en 1789 ?", "Louis XVI", "personnages", 2, "Louis XVI était roi de France de 1774 à 1792"),
                    ("Quel était le slogan de la Révolution française ?", "Liberté, Égalité, Fraternité", "concepts", 4, "Ce slogan est devenu la devise de la République française"),
                    ("Quelle assemblée a été créée en 1789 ?", "Assemblée nationale", "institutions", 3, "L'Assemblée nationale a été proclamée le 17 juin 1789"),
                    ("Quel événement marque le début de la Révolution ?", "États généraux", "événements", 5, "Les États généraux convoqués en mai 1789 marquent le début")
                ]
            else:
                # Questions génériques
                questions = [
                    ("Question de test 1", "réponse 1", "catégorie", 3, "explication 1"),
                    ("Question de test 2", "réponse 2", "catégorie", 4, "explication 2"),
                    ("Question de test 3", "réponse 3", "catégorie", 5, "explication 3")
                ]
            
            # Insérer les questions
            for i, (question_text, correct_answer, category, difficulty, explanation) in enumerate(questions, 1):
                cursor.execute("""
                    INSERT INTO adaptive_questions (
                        test_id, question_text, correct_answer, category, 
                        difficulty_level, explanation, question_order, is_active
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (test_id, question_text, correct_answer, category, difficulty, explanation, i, 1))
            
            print(f"  ✅ {len(questions)} questions ajoutées")
            
            # Mettre à jour le nombre total de questions dans le test
            cursor.execute("""
                UPDATE adaptive_tests 
                SET total_questions = ? 
                WHERE id = ?
            """, (len(questions), test_id))
            
            print(f"  ✅ total_questions mis à jour: {len(questions)}")
        
        # Valider les changements
        conn.commit()
        
        # Vérifier le résultat
        print(f"\n📊 Résumé final:")
        cursor.execute("""
            SELECT t.title, t.total_questions, COUNT(q.id) as questions_count
            FROM adaptive_tests t
            LEFT JOIN adaptive_questions q ON t.id = q.test_id
            WHERE t.is_active = 1
            GROUP BY t.id, t.title, t.total_questions
        """)
        
        results = cursor.fetchall()
        for title, total_questions, questions_count in results:
            print(f"  - {title}: {total_questions} questions déclarées, {questions_count} questions en base")
        
        conn.close()
        print("\n✅ Questions ajoutées avec succès!")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    add_sample_questions()
















