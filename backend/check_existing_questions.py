#!/usr/bin/env python3
"""
Script pour examiner la banque de questions existante
"""

from core.database import engine
from sqlalchemy import text
import json

def check_existing_questions():
    """Vérifier la banque de questions existante"""
    
    try:
        with engine.connect() as conn:
            print("🔍 Analyse de la banque de questions existante...")
            
            # 1. Compter le total des questions
            result = conn.execute(text("SELECT COUNT(*) as count FROM questions"))
            total_questions = result.fetchone()[0]
            print(f"📊 Total des questions: {total_questions}")
            
            # 2. Vérifier la structure des questions
            print("\n📋 Structure des questions existantes:")
            result = conn.execute(text("SELECT * FROM questions LIMIT 3"))
            sample_questions = result.fetchall()
            
            for i, question in enumerate(sample_questions, 1):
                print(f"\n  Question {i}:")
                print(f"    ID: {question[0]}")
                print(f"    Quiz ID: {question[1]}")
                print(f"    Texte: {question[2][:100]}...")
                print(f"    Type: {question[3]}")
                print(f"    Options: {question[4]}")
                print(f"    Réponse correcte: {question[5]}")
                print(f"    Points: {question[6]}")
                print(f"    Ordre: {question[7]}")
            
            # 3. Vérifier les types de questions
            print("\n🎯 Types de questions disponibles:")
            result = conn.execute(text("SELECT DISTINCT question_type, COUNT(*) as count FROM questions GROUP BY question_type"))
            question_types = result.fetchall()
            
            for qtype, count in question_types:
                print(f"  {qtype}: {count} questions")
            
            # 4. Vérifier les quiz disponibles
            print("\n📚 Quiz disponibles:")
            result = conn.execute(text("SELECT DISTINCT quiz_id, COUNT(*) as count FROM questions GROUP BY quiz_id"))
            quiz_counts = result.fetchall()
            
            for quiz_id, count in quiz_counts:
                print(f"  Quiz {quiz_id}: {count} questions")
            
            # 5. Vérifier s'il y a des questions françaises
            print("\n🇫🇷 Recherche de questions françaises:")
            result = conn.execute(text("SELECT COUNT(*) FROM questions WHERE question_text LIKE '%français%' OR question_text LIKE '%France%' OR question_text LIKE '%être%' OR question_text LIKE '%avoir%'"))
            french_questions = result.fetchone()[0]
            print(f"  Questions potentiellement françaises: {french_questions}")
            
            # 6. Vérifier la table question_history
            print("\n📖 Historique des questions:")
            result = conn.execute(text("SELECT COUNT(*) FROM question_history"))
            history_count = result.fetchone()[0]
            print(f"  Questions dans l'historique: {history_count}")
            
            if history_count > 0:
                result = conn.execute(text("SELECT * FROM question_history LIMIT 2"))
                history_samples = result.fetchall()
                for i, hist in enumerate(history_samples, 1):
                    print(f"\n  Historique {i}:")
                    print(f"    Question: {hist[3][:80]}...")
                    print(f"    Difficulté: {hist[4]}")
                    print(f"    Sujet: {hist[5]}")
            
            # 7. Vérifier les tables d'évaluation adaptative
            print("\n🧠 Tables d'évaluation adaptative:")
            tables_to_check = ['adaptive_questions', 'french_adaptive_tests']
            
            for table in tables_to_check:
                try:
                    result = conn.execute(text(f"SELECT COUNT(*) FROM {table}"))
                    count = result.fetchone()[0]
                    print(f"  {table}: {count} entrées")
                except:
                    print(f"  {table}: Table non accessible")
            
    except Exception as e:
        print(f"❌ Erreur lors de l'analyse: {e}")
        raise

def check_question_content():
    """Vérifier le contenu des questions pour identifier les questions françaises"""
    
    try:
        with engine.connect() as conn:
            print("\n🔍 Analyse du contenu des questions...")
            
            # Rechercher des mots-clés français
            french_keywords = [
                "être", "avoir", "faire", "aller", "venir", "voir", "savoir",
                "pouvoir", "vouloir", "devoir", "prendre", "mettre", "dire",
                "donner", "parler", "écouter", "lire", "écrire", "apprendre",
                "comprendre", "expliquer", "traduire", "conjuguer", "grammaire",
                "vocabulaire", "prononciation", "accent", "article", "nom",
                "verbe", "adjectif", "adverbe", "préposition", "conjonction"
            ]
            
            french_questions_found = []
            
            for keyword in french_keywords:
                result = conn.execute(text("""
                    SELECT id, question_text, question_type 
                    FROM questions 
                    WHERE question_text LIKE :keyword 
                    LIMIT 5
                """), {"keyword": f"%{keyword}%"})
                
                questions = result.fetchall()
                if questions:
                    french_questions_found.extend(questions)
            
            if french_questions_found:
                print(f"\n🇫🇷 Questions françaises trouvées: {len(french_questions_found)}")
                for i, (qid, text, qtype) in enumerate(french_questions_found[:10], 1):
                    print(f"  {i}. ID {qid} - {text[:80]}...")
            else:
                print("\n❌ Aucune question française trouvée dans la banque existante")
            
    except Exception as e:
        print(f"❌ Erreur lors de l'analyse du contenu: {e}")

if __name__ == "__main__":
    print("🚀 Analyse de la banque de questions existante...")
    check_existing_questions()
    check_question_content()
    print("\n✅ Analyse terminée !")














