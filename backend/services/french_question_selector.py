#!/usr/bin/env python3
"""
Service de sélection de questions françaises optimisé
Garantit exactement 20 questions avec répartition équilibrée
"""

from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
import json
import random

class FrenchQuestionSelector:
    """Sélecteur de questions françaises optimisé pour 20 questions exactes"""
    
    def __init__(self, db: Session):
        self.db = db
        self.question_pool = self._load_question_pool()
    
    def _load_question_pool(self) -> Dict[str, List[Dict[str, Any]]]:
        """Charger la banque de questions françaises"""
        return {
            "easy": [
                {
                    "id": 1,
                    "question": "Quel est l'article correct ? '___ chat'",
                    "options": ["Le", "La", "Les", "L'"],
                    "correct": "Le",
                    "explanation": "Le mot 'chat' est masculin singulier, donc on utilise 'Le'",
                    "difficulty": "easy",
                    "topic": "Articles"
                },
                {
                    "id": 2,
                    "question": "Conjuguez le verbe 'être' à la 1ère personne du singulier au présent",
                    "options": ["Je suis", "Je es", "Je être", "Je suis être"],
                    "correct": "Je suis",
                    "explanation": "Le verbe 'être' se conjugue 'je suis' à la 1ère personne du singulier au présent",
                    "difficulty": "easy",
                    "topic": "Conjugaison"
                },
                {
                    "id": 3,
                    "question": "Quel est le genre du mot 'maison' ?",
                    "options": ["Masculin", "Féminin", "Neutre", "Variable"],
                    "correct": "Féminin",
                    "explanation": "Le mot 'maison' est un nom féminin",
                    "difficulty": "easy",
                    "topic": "Genre des noms"
                },
                {
                    "id": 4,
                    "question": "Quel est le pluriel de 'cheval' ?",
                    "options": ["Chevals", "Chevaux", "Chevales", "Cheval"],
                    "correct": "Chevaux",
                    "explanation": "Le pluriel de 'cheval' est 'chevaux' (pluriel irrégulier)",
                    "difficulty": "easy",
                    "topic": "Pluriels"
                },
                {
                    "id": 5,
                    "question": "Quel est l'antonyme de 'grand' ?",
                    "options": ["Petit", "Gros", "Long", "Large"],
                    "correct": "Petit",
                    "explanation": "L'antonyme de 'grand' est 'petit'",
                    "difficulty": "easy",
                    "topic": "Vocabulaire"
                },
                {
                    "id": 6,
                    "question": "Complétez : 'Je ___ un étudiant'",
                    "options": ["suis", "es", "est", "sont"],
                    "correct": "suis",
                    "explanation": "Avec le sujet 'Je', le verbe 'être' se conjugue 'suis'",
                    "difficulty": "easy",
                    "topic": "Conjugaison"
                },
                {
                    "id": 7,
                    "question": "Quel est le féminin de 'professeur' ?",
                    "options": ["Professeur", "Professeure", "Professeuse", "Professeure"],
                    "correct": "Professeure",
                    "explanation": "Le féminin de 'professeur' est 'professeure'",
                    "difficulty": "easy",
                    "topic": "Formation du féminin"
                }
            ],
            "medium": [
                {
                    "id": 8,
                    "question": "Complétez : 'Les enfants ___ dans le jardin.'",
                    "options": ["joue", "jouent", "joues", "jouer"],
                    "correct": "jouent",
                    "explanation": "Avec le sujet 'Les enfants' (pluriel), le verbe 'jouer' prend la terminaison '-ent'",
                    "difficulty": "medium",
                    "topic": "Accords"
                },
                {
                    "id": 9,
                    "question": "Quel temps verbal dans 'J'ai mangé' ?",
                    "options": ["Présent", "Imparfait", "Passé composé", "Futur"],
                    "correct": "Passé composé",
                    "explanation": "'J'ai mangé' est au passé composé (avoir + participe passé)",
                    "difficulty": "medium",
                    "topic": "Temps verbaux"
                },
                {
                    "id": 10,
                    "question": "Quel est le féminin de 'acteur' ?",
                    "options": ["Acteur", "Actrice", "Acteuse", "Acteure"],
                    "correct": "Actrice",
                    "explanation": "Le féminin de 'acteur' est 'actrice'",
                    "difficulty": "medium",
                    "topic": "Formation du féminin"
                },
                {
                    "id": 11,
                    "question": "Combien de syllabes dans 'ordinateur' ?",
                    "options": ["3", "4", "5", "6"],
                    "correct": "4",
                    "explanation": "'ordinateur' se divise en 4 syllabes : or-di-na-teur",
                    "difficulty": "medium",
                    "topic": "Phonétique"
                },
                {
                    "id": 12,
                    "question": "Quel est le sens de 'rapidement' ?",
                    "options": ["Lentement", "Vite", "Doucement", "Fortement"],
                    "correct": "Vite",
                    "explanation": "'Rapidement' signifie 'vite' ou 'avec rapidité'",
                    "difficulty": "medium",
                    "topic": "Adverbes"
                },
                {
                    "id": 13,
                    "question": "Identifiez la fonction de 'très' dans 'Il est très intelligent'",
                    "options": ["Adjectif", "Adverbe", "Nom", "Verbe"],
                    "correct": "Adverbe",
                    "explanation": "'Très' est un adverbe qui modifie l'adjectif 'intelligent'",
                    "difficulty": "medium",
                    "topic": "Classes grammaticales"
                }
            ],
            "hard": [
                {
                    "id": 14,
                    "question": "Quel est le mode du verbe dans 'Veuillez patienter' ?",
                    "options": ["Indicatif", "Subjonctif", "Impératif", "Conditionnel"],
                    "correct": "Impératif",
                    "explanation": "'Veuillez' est à l'impératif, forme de politesse",
                    "difficulty": "hard",
                    "topic": "Modes verbaux"
                },
                {
                    "id": 15,
                    "question": "Quel est le type de phrase 'Quelle belle journée !' ?",
                    "options": ["Déclarative", "Interrogative", "Exclamative", "Impérative"],
                    "correct": "Exclamative",
                    "explanation": "Cette phrase exprime une exclamation, c'est une phrase exclamative",
                    "difficulty": "hard",
                    "topic": "Types de phrases"
                },
                {
                    "id": 16,
                    "question": "Quel est le registre de langue de 'bagnole' ?",
                    "options": ["Soutenu", "Courant", "Familier", "Argotique"],
                    "correct": "Familier",
                    "explanation": "'Bagnole' est un terme familier pour désigner une voiture",
                    "difficulty": "hard",
                    "topic": "Registres de langue"
                },
                {
                    "id": 17,
                    "question": "Quel est le sens figuré de 'avoir le cafard' ?",
                    "options": ["Être malade", "Être triste", "Être fatigué", "Être en colère"],
                    "correct": "Être triste",
                    "explanation": "'Avoir le cafard' signifie être triste ou déprimé (expression figurée)",
                    "difficulty": "hard",
                    "topic": "Expressions idiomatiques"
                },
                {
                    "id": 18,
                    "question": "Quel est le type de complément dans 'Il mange une pomme' ?",
                    "options": ["Complément d'objet direct", "Complément d'objet indirect", "Complément circonstanciel", "Attribut"],
                    "correct": "Complément d'objet direct",
                    "explanation": "'Une pomme' est le complément d'objet direct du verbe 'mange'",
                    "difficulty": "hard",
                    "topic": "Fonctions grammaticales"
                },
                {
                    "id": 19,
                    "question": "Quel est le degré de l'adjectif dans 'C'est le plus beau jour' ?",
                    "options": ["Positif", "Comparatif", "Superlatif", "Absolu"],
                    "correct": "Superlatif",
                    "explanation": "'Le plus beau' est au superlatif de supériorité",
                    "difficulty": "hard",
                    "topic": "Degrés de l'adjectif"
                },
                {
                    "id": 20,
                    "question": "Quel est le type de proposition dans 'Je pense qu'il viendra' ?",
                    "options": ["Principale", "Subordonnée relative", "Subordonnée complétive", "Subordonnée circonstancielle"],
                    "correct": "Subordonnée complétive",
                    "explanation": "'Qu'il viendra' est une proposition subordonnée complétive qui complète le verbe 'pense'",
                    "difficulty": "hard",
                    "topic": "Types de propositions"
                }
            ]
        }
    
    def select_questions_for_assessment(self, student_id: int) -> List[Dict[str, Any]]:
        """
        Sélectionner exactement 20 questions pour l'évaluation initiale
        Répartition : 7 facile + 6 moyen + 7 difficile
        """
        print(f"🎯 Sélection de 20 questions pour l'étudiant {student_id}")
        
        # Vérifier l'historique des questions de l'étudiant
        student_history = self._get_student_question_history(student_id)
        
        # Sélectionner les questions en évitant la répétition
        selected_questions = []
        
        # 7 questions faciles
        easy_questions = self._select_questions_by_difficulty("easy", 7, student_history)
        selected_questions.extend(easy_questions)
        
        # 6 questions moyennes
        medium_questions = self._select_questions_by_difficulty("medium", 6, student_history)
        selected_questions.extend(medium_questions)
        
        # 7 questions difficiles
        hard_questions = self._select_questions_by_difficulty("hard", 7, student_history)
        selected_questions.extend(hard_questions)
        
        # Mélanger l'ordre des questions
        random.shuffle(selected_questions)
        
        # Assigner un ordre séquentiel
        for i, question in enumerate(selected_questions):
            question["order"] = i + 1
        
        print(f"✅ {len(selected_questions)} questions sélectionnées et ordonnées")
        return selected_questions
    
    def _select_questions_by_difficulty(self, difficulty: str, count: int, student_history: List[int]) -> List[Dict[str, Any]]:
        """Sélectionner des questions d'une difficulté spécifique en évitant la répétition"""
        available_questions = self.question_pool[difficulty].copy()
        
        # Filtrer les questions déjà posées à l'étudiant
        if student_history:
            available_questions = [q for q in available_questions if q["id"] not in student_history]
        
        # Si pas assez de questions uniques, réutiliser certaines questions
        if len(available_questions) < count:
            print(f"⚠️ Seulement {len(available_questions)} questions uniques disponibles pour {difficulty}, réutilisation autorisée")
            available_questions = self.question_pool[difficulty].copy()
        
        # Sélectionner aléatoirement
        selected = random.sample(available_questions, min(count, len(available_questions)))
        return selected
    
    def _get_student_question_history(self, student_id: int) -> List[int]:
        """Récupérer l'historique des questions déjà posées à l'étudiant"""
        try:
            # Vérifier si la table question_history existe
            result = self.db.execute("""
                SELECT name FROM sqlite_master 
                WHERE type='table' AND name='question_history'
            """)
            
            if not result.fetchone():
                print("ℹ️ Table question_history n'existe pas encore")
                return []
            
            # Récupérer l'historique
            result = self.db.execute("""
                SELECT question_id FROM question_history 
                WHERE student_id = :student_id
            """, {"student_id": student_id})
            
            question_ids = [row[0] for row in result.fetchall()]
            print(f"📚 Historique de {len(question_ids)} questions pour l'étudiant {student_id}")
            return question_ids
            
        except Exception as e:
            print(f"⚠️ Erreur lors de la récupération de l'historique: {e}")
            return []
    
    def get_question_by_order(self, questions: List[Dict[str, Any]], order: int) -> Optional[Dict[str, Any]]:
        """Récupérer une question par son ordre"""
        for question in questions:
            if question.get("order") == order:
                return question
        return None
    
    def get_total_questions(self) -> int:
        """Retourner le nombre total de questions disponibles"""
        total = 0
        for difficulty in self.question_pool:
            total += len(self.question_pool[difficulty])
        return total
