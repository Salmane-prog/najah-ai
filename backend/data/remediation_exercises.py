#!/usr/bin/env python3
"""
Banque d'exercices de remédiation diversifiée
Évite la redondance et propose une variété d'activités d'apprentissage
"""

from typing import List, Dict, Any
import random

# ============================================================================
# EXERCICES DE GRAMMAIRE FRANÇAISE
# ============================================================================

GRAMMAR_EXERCISES = {
    "articles": [
        {
            "id": "gram_art_001",
            "type": "quiz",
            "question": "Choisissez l'article correct : ___ élève est intelligent.",
            "options": ["Le", "La", "L'", "Les"],
            "correct": "L'",
            "explanation": "Devant une voyelle, on utilise 'L'' au lieu de 'Le' ou 'La'.",
            "difficulty": "facile",
            "topic": "Articles",
            "estimated_time": 2
        },
        {
            "id": "gram_art_002",
            "type": "quiz",
            "question": "Complétez : ___ enfants jouent dans ___ parc.",
            "options": ["Les / le", "Les / la", "Le / le", "La / le"],
            "correct": "Les / le",
            "explanation": "'Enfants' est masculin pluriel → 'Les', 'parc' est masculin singulier → 'le'.",
            "difficulty": "intermédiaire",
            "topic": "Articles",
            "estimated_time": 3
        }
    ],
    
    "adjectifs": [
        {
            "id": "gram_adj_001",
            "type": "quiz",
            "question": "Accordez l'adjectif : Les filles sont ___ (beau).",
            "options": ["beau", "beaux", "belle", "belles"],
            "correct": "belles",
            "explanation": "'Filles' est féminin pluriel, donc 'beau' devient 'belles'.",
            "difficulty": "intermédiaire",
            "topic": "Accord des adjectifs",
            "estimated_time": 3
        },
        {
            "id": "gram_adj_002",
            "type": "practice",
            "question": "Transformez en accordant : 'Un petit garçon et une petite fille'",
            "hint": "Pensez au genre et au nombre",
            "solution": "Des petits garçons et des petites filles",
            "explanation": "Au pluriel : 'petit' → 'petits' (masculin), 'petite' → 'petites' (féminin)",
            "difficulty": "avancé",
            "topic": "Accord des adjectifs",
            "estimated_time": 5
        }
    ],
    
    "pronoms": [
        {
            "id": "gram_pro_001",
            "type": "quiz",
            "question": "Remplacez par un pronom : 'Je vois Marie' → 'Je ___ vois'",
            "options": ["la", "le", "lui", "elle"],
            "correct": "la",
            "explanation": "'Marie' est un COD féminin singulier, on le remplace par 'la'.",
            "difficulty": "intermédiaire",
            "topic": "Pronoms COD",
            "estimated_time": 3
        }
    ]
}

# ============================================================================
# EXERCICES DE CONJUGAISON
# ============================================================================

CONJUGATION_EXERCISES = {
    "present": [
        {
            "id": "conj_pre_001",
            "type": "quiz",
            "question": "Conjuguez 'être' à la 1ère personne du singulier au présent :",
            "options": ["Je suis", "Je es", "Je être", "Je suis être"],
            "correct": "Je suis",
            "explanation": "Le verbe 'être' au présent : je suis, tu es, il/elle est...",
            "difficulty": "facile",
            "topic": "Présent du verbe être",
            "estimated_time": 2
        },
        {
            "id": "conj_pre_002",
            "type": "quiz",
            "question": "Conjuguez 'finir' à la 3ème personne du pluriel au présent :",
            "options": ["Ils finissent", "Ils finissent", "Ils finissent", "Ils finissent"],
            "correct": "Ils finissent",
            "explanation": "Les verbes en -ir au présent : ils finissent, ils choisissent...",
            "difficulty": "facile",
            "topic": "Présent des verbes en -ir",
            "estimated_time": 2
        }
    ],
    
    "futur": [
        {
            "id": "conj_fut_001",
            "type": "quiz",
            "question": "Conjuguez 'aller' à la 2ème personne du singulier au futur :",
            "options": ["Tu iras", "Tu vas", "Tu alleras", "Tu alleras"],
            "correct": "Tu iras",
            "explanation": "Le futur simple : radical 'ir-' + terminaison '-as' pour 'tu'.",
            "difficulty": "intermédiaire",
            "topic": "Futur simple",
            "estimated_time": 3
        },
        {
            "id": "conj_fut_002",
            "type": "practice",
            "question": "Conjuguez 'venir' au futur simple pour toutes les personnes",
            "hint": "Radical 'viendr-' + terminaisons du futur",
            "solution": "Je viendrai, tu viendras, il/elle viendra, nous viendrons, vous viendrez, ils/elles viendront",
            "explanation": "Le futur de 'venir' : radical 'viendr-' + terminaisons -ai, -as, -a, -ons, -ez, -ont",
            "difficulty": "avancé",
            "topic": "Futur simple",
            "estimated_time": 8
        }
    ],
    
    "imparfait": [
        {
            "id": "conj_imp_001",
            "type": "quiz",
            "question": "Conjuguez 'avoir' à la 1ère personne du pluriel à l'imparfait :",
            "options": ["Nous avions", "Nous avons", "Nous avions", "Nous avions"],
            "correct": "Nous avions",
            "explanation": "L'imparfait de 'avoir' : nous avions, vous aviez, ils/elles avaient.",
            "difficulty": "intermédiaire",
            "topic": "Imparfait",
            "estimated_time": 3
        }
    ]
}

# ============================================================================
# EXERCICES DE VOCABULAIRE
# ============================================================================

VOCABULARY_EXERCISES = {
    "famille": [
        {
            "id": "voc_fam_001",
            "type": "matching",
            "question": "Associez les mots de famille avec leurs définitions :",
            "pairs": [
                ("père", "Parent masculin"),
                ("mère", "Parent féminin"),
                ("frère", "Enfant masculin de mêmes parents"),
                ("sœur", "Enfant féminin de mêmes parents")
            ],
            "explanation": "La famille nucléaire comprend les parents et leurs enfants.",
            "difficulty": "facile",
            "topic": "Vocabulaire de la famille",
            "estimated_time": 4
        }
    ],
    
    "maison": [
        {
            "id": "voc_mais_001",
            "type": "quiz",
            "question": "Qu'est-ce qu'une 'cuisine' ?",
            "options": ["Une pièce pour dormir", "Une pièce pour cuisiner", "Une pièce pour se laver", "Une pièce pour travailler"],
            "correct": "Une pièce pour cuisiner",
            "explanation": "La cuisine est l'endroit où on prépare les repas.",
            "difficulty": "facile",
            "topic": "Pièces de la maison",
            "estimated_time": 2
        }
    ],
    
    "nourriture": [
        {
            "id": "voc_nour_001",
            "type": "categorization",
            "question": "Classez ces aliments par catégorie :",
            "items": ["pomme", "poulet", "carotte", "poisson", "banane", "lait"],
            "categories": ["Fruits", "Légumes", "Viandes", "Produits laitiers"],
            "solutions": {
                "Fruits": ["pomme", "banane"],
                "Légumes": ["carotte"],
                "Viandes": ["poulet", "poisson"],
                "Produits laitiers": ["lait"]
            },
            "explanation": "Une alimentation équilibrée comprend tous ces groupes d'aliments.",
            "difficulty": "intermédiaire",
            "topic": "Vocabulaire alimentaire",
            "estimated_time": 5
        }
    ]
}

# ============================================================================
# EXERCICES DE COMPRÉHENSION
# ============================================================================

COMPREHENSION_EXERCISES = {
    "lecture": [
        {
            "id": "comp_lec_001",
            "type": "reading",
            "title": "Le Petit Déjeuner Français",
            "text": "En France, le petit déjeuner traditionnel comprend souvent une baguette avec du beurre et de la confiture, accompagnée d'un café ou d'un chocolat chaud. Certains préfèrent des céréales ou des yaourts.",
            "questions": [
                {
                    "question": "Que contient un petit déjeuner français traditionnel ?",
                    "options": ["Du pain et du café", "Des œufs et du bacon", "Du riz et du thé", "Des fruits seulement"],
                    "correct": "Du pain et du café",
                    "explanation": "Le texte mentionne 'baguette avec du beurre et de la confiture, accompagnée d'un café'."
                }
            ],
            "difficulty": "facile",
            "topic": "Compréhension de lecture",
            "estimated_time": 6
        }
    ],
    
    "audio": [
        {
            "id": "comp_aud_001",
            "type": "listening",
            "title": "Les Saisons",
            "audio_file": "seasons_fr.mp3",
            "transcript": "Il y a quatre saisons en France : le printemps, l'été, l'automne et l'hiver. Chaque saison a ses caractéristiques.",
            "questions": [
                {
                    "question": "Combien y a-t-il de saisons en France ?",
                    "options": ["3", "4", "5", "6"],
                    "correct": "4",
                    "explanation": "Le transcript mentionne 'quatre saisons'."
                }
            ],
            "difficulty": "facile",
            "topic": "Compréhension orale",
            "estimated_time": 5
        }
    ]
}

# ============================================================================
# EXERCICES INTERACTIFS
# ============================================================================

INTERACTIVE_EXERCISES = {
    "drag_drop": [
        {
            "id": "int_drag_001",
            "type": "drag_drop",
            "question": "Reconstituez la phrase en glissant les mots :",
            "sentence_parts": ["Je", "mange", "une", "pomme"],
            "correct_order": ["Je", "mange", "une", "pomme"],
            "explanation": "L'ordre correct est : sujet + verbe + article + nom.",
            "difficulty": "facile",
            "topic": "Construction de phrases",
            "estimated_time": 4
        }
    ],
    
    "fill_blank": [
        {
            "id": "int_fill_001",
            "type": "fill_blank",
            "question": "Complétez : 'Je ___ français et j'___ étudiant.'",
            "blanks": ["suis", "suis"],
            "hints": ["Verbe 'être' à la 1ère personne", "Même verbe pour la deuxième partie"],
            "explanation": "Le verbe 'être' se conjugue 'suis' à la 1ère personne du singulier.",
            "difficulty": "intermédiaire",
            "topic": "Conjugaison du verbe être",
            "estimated_time": 4
        }
    ]
}

# ============================================================================
# FONCTIONS DE SÉLECTION INTELLIGENTE
# ============================================================================

class RemediationExerciseBank:
    """Banque d'exercices de remédiation avec sélection intelligente"""
    
    def __init__(self):
        self.all_exercises = {
            "grammar": GRAMMAR_EXERCISES,
            "conjugation": CONJUGATION_EXERCISES,
            "vocabulary": VOCABULARY_EXERCISES,
            "comprehension": COMPREHENSION_EXERCISES,
            "interactive": INTERACTIVE_EXERCISES
        }
        
        # Historique des exercices déjà proposés (pour éviter la redondance)
        self.exercise_history = {}
    
    def get_diverse_exercises(self, topic: str, difficulty: str, count: int = 3, 
                            student_id: int = None, avoid_repetition: bool = True) -> List[Dict[str, Any]]:
        """
        Sélectionne des exercices diversifiés en évitant la redondance
        """
        # Récupérer tous les exercices du topic demandé
        available_exercises = []
        
        # Correspondance directe par nom de catégorie
        if topic.lower() in self.all_exercises:
            category_exercises = self.all_exercises[topic.lower()]
            for subcategory, exercise_list in category_exercises.items():
                available_exercises.extend(exercise_list)
        
        # Si aucune correspondance directe, essayer une correspondance partielle
        if not available_exercises:
            for category, exercises in self.all_exercises.items():
                if topic.lower() in category.lower():
                    for subcategory, exercise_list in exercises.items():
                        available_exercises.extend(exercise_list)
        
        # Log pour debug
        print(f"🔍 [EXERCISE_BANK] Topic demandé: {topic}")
        print(f"🔍 [EXERCISE_BANK] Catégories disponibles: {list(self.all_exercises.keys())}")
        print(f"🔍 [EXERCISE_BANK] Exercices trouvés: {len(available_exercises)}")
        
        # Filtrer par difficulté si spécifiée
        if difficulty:
            before_filter = len(available_exercises)
            available_exercises = [ex for ex in available_exercises if ex["difficulty"] == difficulty]
            after_filter = len(available_exercises)
            print(f"🔍 [EXERCISE_BANK] Filtrage par difficulté '{difficulty}': {before_filter} → {after_filter} exercices")
            
            # Si aucun exercice trouvé avec la difficulté demandée, essayer d'autres difficultés
            if after_filter == 0:
                print(f"⚠️ [EXERCISE_BANK] Aucun exercice trouvé avec difficulté '{difficulty}', recherche de difficultés alternatives...")
                # Récupérer tous les exercices du topic sans filtrage de difficulté
                all_topic_exercises = []
                if topic.lower() in self.all_exercises:
                    category_exercises = self.all_exercises[topic.lower()]
                    for subcategory, exercise_list in category_exercises.items():
                        all_topic_exercises.extend(exercise_list)
                
                if all_topic_exercises:
                    # Prendre les exercices de la difficulté la plus proche
                    difficulty_order = ["facile", "intermédiaire", "avancé"]
                    target_index = difficulty_order.index(difficulty) if difficulty in difficulty_order else 1
                    
                    # Essayer d'abord la difficulté demandée, puis les plus proches
                    for diff in [difficulty] + difficulty_order:
                        if diff in difficulty_order:
                            diff_exercises = [ex for ex in all_topic_exercises if ex["difficulty"] == diff]
                            if diff_exercises:
                                available_exercises = diff_exercises
                                print(f"✅ [EXERCISE_BANK] Utilisation de difficulté alternative '{diff}': {len(available_exercises)} exercices")
                                break
        
        # Éviter la redondance si demandé
        if avoid_repetition and student_id:
            if student_id not in self.exercise_history:
                self.exercise_history[student_id] = set()
            
            # Filtrer les exercices déjà proposés
            available_exercises = [ex for ex in available_exercises 
                                 if ex["id"] not in self.exercise_history[student_id]]
        
        # Mélanger pour plus de variété
        random.shuffle(available_exercises)
        
        # Sélectionner le nombre demandé
        selected_exercises = available_exercises[:count]
        
        # Mettre à jour l'historique
        if student_id:
            for exercise in selected_exercises:
                self.exercise_history[student_id].add(exercise["id"])
        
        return selected_exercises
    
    def get_exercise_by_id(self, exercise_id: str) -> Dict[str, Any]:
        """Récupère un exercice spécifique par son ID"""
        for category in self.all_exercises.values():
            for subcategory in category.values():
                for exercise in subcategory:
                    if exercise["id"] == exercise_id:
                        return exercise
        return None
    
    def get_random_exercise(self, topic: str = None, difficulty: str = None) -> Dict[str, Any]:
        """Récupère un exercice aléatoire"""
        exercises = self.get_diverse_exercises(topic or "all", difficulty or "all", 1)
        return exercises[0] if exercises else None
    
    def get_progressive_exercises(self, topic: str, student_level: str, count: int = 3) -> List[Dict[str, Any]]:
        """Récupère des exercices progressifs selon le niveau de l'étudiant"""
        difficulty_order = ["facile", "intermédiaire", "avancé"]
        
        if student_level == "débutant":
            target_difficulties = ["facile"]
        elif student_level == "intermédiaire":
            target_difficulties = ["facile", "intermédiaire"]
        else:
            target_difficulties = ["intermédiaire", "avancé"]
        
        progressive_exercises = []
        for difficulty in target_difficulties:
            exercises = self.get_diverse_exercises(topic, difficulty, count // len(target_difficulties))
            progressive_exercises.extend(exercises)
        
        return progressive_exercises[:count]

# Instance globale de la banque d'exercices
exercise_bank = RemediationExerciseBank()

# ============================================================================
# FONCTIONS UTILITAIRES
# ============================================================================

def get_exercises_for_remediation_plan(student_id: int, subject: str, topics: List[str], 
                                     difficulty: str = "intermédiaire") -> List[Dict[str, Any]]:
    """
    Génère une liste d'exercices diversifiés pour un plan de remédiation
    """
    exercises = []
    
    for topic in topics:
        topic_exercises = exercise_bank.get_diverse_exercises(
            topic=topic,
            difficulty=difficulty,
            count=2,  # 2 exercices par topic pour la variété
            student_id=student_id,
            avoid_repetition=True
        )
        exercises.extend(topic_exercises)
    
    # Mélanger pour plus de variété
    random.shuffle(exercises)
    
    return exercises

def get_exercise_statistics() -> Dict[str, Any]:
    """Retourne des statistiques sur la banque d'exercices"""
    total_exercises = 0
    by_category = {}
    by_difficulty = {}
    
    for category_name, category in exercise_bank.all_exercises.items():
        category_count = 0
        for subcategory in category.values():
            for exercise in subcategory:
                total_exercises += 1
                category_count += 1
                
                # Compter par difficulté
                difficulty = exercise["difficulty"]
                by_difficulty[difficulty] = by_difficulty.get(difficulty, 0) + 1
        
        by_category[category_name] = category_count
    
    return {
        "total_exercises": total_exercises,
        "by_category": by_category,
        "by_difficulty": by_difficulty,
        "categories": list(by_category.keys()),
        "difficulties": list(by_difficulty.keys())
    }

if __name__ == "__main__":
    # Test de la banque d'exercices
    print("📚 BANQUE D'EXERCICES DE REMÉDIATION DIVERSIFIÉE")
    print("=" * 60)
    
    stats = get_exercise_statistics()
    print(f"📊 Total d'exercices : {stats['total_exercises']}")
    print(f"🏷️  Catégories : {', '.join(stats['categories'])}")
    print(f"⭐ Difficultés : {', '.join(stats['difficulties'])}")
    
    print("\n🎯 Test de sélection diversifiée :")
    diverse_exercises = exercise_bank.get_diverse_exercises("conjugaison", "facile", 3)
    for i, ex in enumerate(diverse_exercises, 1):
        print(f"  {i}. {ex['question'][:50]}... ({ex['difficulty']})")
    
    print("\n✅ Banque d'exercices prête à l'emploi !")
