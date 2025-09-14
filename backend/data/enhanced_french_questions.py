#!/usr/bin/env python3
"""
Banque de questions françaises étendue avec templates dynamiques
"""

import random
from typing import List, Dict, Any

# ============================================================================
# TEMPLATES DYNAMIQUES POUR QUESTIONS
# ============================================================================

# Templates pour les articles
ARTICLE_TEMPLATES = {
    "easy": [
        {
            "template": "Quel est l'article correct ? '___ {noun}'",
            "nouns": [
                {"word": "chat", "article": "Le", "gender": "masculin", "explanation": "Le mot 'chat' est masculin singulier"},
                {"word": "maison", "article": "La", "gender": "féminin", "explanation": "Le mot 'maison' est féminin singulier"},
                {"word": "oiseau", "article": "L'", "gender": "masculin", "explanation": "Le mot 'oiseau' commence par une voyelle, on utilise 'L''"},
                {"word": "école", "article": "L'", "gender": "féminin", "explanation": "Le mot 'école' commence par une voyelle, on utilise 'L''"},
                {"word": "livre", "article": "Le", "gender": "masculin", "explanation": "Le mot 'livre' est masculin singulier"}
            ]
        }
    ],
    "medium": [
        {
            "template": "Complétez avec l'article correct : '___ {noun} {adjective}'",
            "nouns": [
                {"word": "homme", "article": "L'", "gender": "masculin", "explanation": "Devant une voyelle, on utilise 'L''"},
                {"word": "enfant", "article": "L'", "gender": "masculin", "explanation": "Devant une voyelle, on utilise 'L''"},
                {"word": "étudiant", "article": "L'", "gender": "masculin", "explanation": "Devant une voyelle, on utilise 'L''"}
            ],
            "adjectives": ["intelligent", "amusant", "curieux"]
        }
    ]
}

# Templates pour la conjugaison
CONJUGATION_TEMPLATES = {
    "easy": [
        {
            "template": "Conjuguez le verbe '{verb}' à la {person} personne du {number} au présent",
            "verbs": [
                {"verb": "être", "conjugations": {"1s": "suis", "2s": "es", "3s": "est", "1p": "sommes", "2p": "êtes", "3p": "sont"}},
                {"verb": "avoir", "conjugations": {"1s": "ai", "2s": "as", "3s": "a", "1p": "avons", "2p": "avez", "3p": "ont"}},
                {"verb": "aller", "conjugations": {"1s": "vais", "2s": "vas", "3s": "va", "1p": "allons", "2p": "allez", "3p": "vont"}}
            ],
            "persons": ["1ère", "2ème", "3ème"],
            "numbers": ["singulier", "pluriel"]
        }
    ],
    "medium": [
        {
            "template": "Quel est le temps du verbe dans '{sentence}' ?",
            "sentences": [
                {"sentence": "J'ai mangé une pomme", "tense": "Passé composé", "explanation": "'J'ai mangé' est au passé composé (avoir + participe passé)"},
                {"sentence": "Je mangeais une pomme", "tense": "Imparfait", "explanation": "'Je mangeais' est à l'imparfait"},
                {"sentence": "Je mangerai une pomme", "tense": "Futur simple", "explanation": "'Je mangerai' est au futur simple"}
            ]
        }
    ]
}

# Templates pour le vocabulaire
VOCABULARY_TEMPLATES = {
    "easy": [
        {
            "template": "Quel est l'antonyme de '{word}' ?",
            "words": [
                {"word": "grand", "antonym": "petit", "explanation": "L'antonyme de 'grand' est 'petit'"},
                {"word": "chaud", "antonym": "froid", "explanation": "L'antonyme de 'chaud' est 'froid'"},
                {"word": "rapide", "antonym": "lent", "explanation": "L'antonyme de 'rapide' est 'lent'"},
                {"word": "facile", "antonym": "difficile", "explanation": "L'antonyme de 'facile' est 'difficile'"},
                {"word": "nouveau", "antonym": "ancien", "explanation": "L'antonyme de 'nouveau' est 'ancien'"}
            ]
        }
    ],
    "medium": [
        {
            "template": "Quel est le sens de l'expression '{expression}' ?",
            "expressions": [
                {"expression": "avoir le cafard", "meaning": "Être triste", "explanation": "'Avoir le cafard' signifie être triste ou déprimé"},
                {"expression": "casser les pieds", "meaning": "Ennuyer", "explanation": "'Casser les pieds' signifie ennuyer quelqu'un"},
                {"expression": "avoir la pêche", "meaning": "Être en forme", "explanation": "'Avoir la pêche' signifie être en forme et énergique"}
            ]
        }
    ]
}

# ============================================================================
# QUESTIONS STATIQUES ÉTENDUES
# ============================================================================

ENHANCED_FRENCH_QUESTIONS = {
    "easy": [
        # Articles et genre (ID 1-10)
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
            "question": "Quel est le genre du mot 'maison' ?",
            "options": ["Masculin", "Féminin", "Neutre", "Variable"],
            "correct": "Féminin",
            "explanation": "Le mot 'maison' est un nom féminin",
            "difficulty": "easy",
            "topic": "Genre des noms"
        },
        {
            "id": 3,
            "question": "Quel est le pluriel de 'cheval' ?",
            "options": ["Chevals", "Chevaux", "Chevales", "Cheval"],
            "correct": "Chevaux",
            "explanation": "Le pluriel de 'cheval' est 'chevaux' (pluriel irrégulier)",
            "difficulty": "easy",
            "topic": "Pluriels"
        },
        {
            "id": 4,
            "question": "Quel est l'article correct ? '___ école'",
            "options": ["Le", "La", "Les", "L'"],
            "correct": "L'",
            "explanation": "Le mot 'école' commence par une voyelle, on utilise 'L''",
            "difficulty": "easy",
            "topic": "Articles"
        },
        {
            "id": 5,
            "question": "Quel est le genre du mot 'livre' ?",
            "options": ["Masculin", "Féminin", "Neutre", "Variable"],
            "correct": "Masculin",
            "explanation": "Le mot 'livre' est un nom masculin",
            "difficulty": "easy",
            "topic": "Genre des noms"
        },
        {
            "id": 6,
            "question": "Quel est le pluriel de 'journal' ?",
            "options": ["Journals", "Journaux", "Journales", "Journal"],
            "correct": "Journaux",
            "explanation": "Le pluriel de 'journal' est 'journaux' (pluriel en -aux)",
            "difficulty": "easy",
            "topic": "Pluriels"
        },
        {
            "id": 7,
            "question": "Quel est l'article correct ? '___ arbre'",
            "options": ["Le", "La", "Les", "L'"],
            "correct": "L'",
            "explanation": "Le mot 'arbre' commence par une voyelle, on utilise 'L''",
            "difficulty": "easy",
            "topic": "Articles"
        },
        {
            "id": 8,
            "question": "Quel est le genre du mot 'table' ?",
            "options": ["Masculin", "Féminin", "Neutre", "Variable"],
            "correct": "Féminin",
            "explanation": "Le mot 'table' est un nom féminin",
            "difficulty": "easy",
            "topic": "Genre des noms"
        },
        {
            "id": 9,
            "question": "Quel est le pluriel de 'oiseau' ?",
            "options": ["Oiseaus", "Oiseaux", "Oiseaues", "Oiseau"],
            "correct": "Oiseaux",
            "explanation": "Le pluriel de 'oiseau' est 'oiseaux' (pluriel en -eaux)",
            "difficulty": "easy",
            "topic": "Pluriels"
        },
        {
            "id": 10,
            "question": "Quel est l'article correct ? '___ voiture'",
            "options": ["Le", "La", "Les", "L'"],
            "correct": "La",
            "explanation": "Le mot 'voiture' est féminin singulier, donc on utilise 'La'",
            "difficulty": "easy",
            "topic": "Articles"
        }
    ],
    "medium": [
        # Conjugaison et accords (ID 11-25)
        {
            "id": 11,
            "question": "Complétez : 'Les enfants ___ dans le jardin.'",
            "options": ["joue", "jouent", "joues", "jouer"],
            "correct": "jouent",
            "explanation": "Avec le sujet 'Les enfants' (pluriel), le verbe 'jouer' prend la terminaison '-ent'",
            "difficulty": "medium",
            "topic": "Accords"
        },
        {
            "id": 12,
            "question": "Quel temps verbal dans 'J'ai mangé une pomme' ?",
            "options": ["Présent", "Imparfait", "Passé composé", "Futur"],
            "correct": "Passé composé",
            "explanation": "'J'ai mangé' est au passé composé (avoir + participe passé)",
            "difficulty": "medium",
            "topic": "Temps verbaux"
        },
        {
            "id": 13,
            "question": "Quel est le féminin de 'acteur' ?",
            "options": ["Acteur", "Actrice", "Acteuse", "Acteure"],
            "correct": "Actrice",
            "explanation": "Le féminin de 'acteur' est 'actrice'",
            "difficulty": "medium",
            "topic": "Formation du féminin"
        },
        {
            "id": 14,
            "question": "Combien de syllabes dans 'ordinateur' ?",
            "options": ["3", "4", "5", "6"],
            "correct": "4",
            "explanation": "'ordinateur' se divise en 4 syllabes : or-di-na-teur",
            "difficulty": "medium",
            "topic": "Phonétique"
        },
        {
            "id": 15,
            "question": "Quel est le sens de 'rapidement' ?",
            "options": ["Lentement", "Vite", "Doucement", "Fortement"],
            "correct": "Vite",
            "explanation": "'Rapidement' signifie 'vite' ou 'avec rapidité'",
            "difficulty": "medium",
            "topic": "Adverbes"
        },
        {
            "id": 16,
            "question": "Complétez : 'La fille ___ une robe rouge.'",
            "options": ["porte", "portes", "portent", "porter"],
            "correct": "porte",
            "explanation": "Avec le sujet 'La fille' (singulier), le verbe 'porter' prend la terminaison '-e'",
            "difficulty": "medium",
            "topic": "Accords"
        },
        {
            "id": 17,
            "question": "Quel temps verbal dans 'Je mangeais une pomme' ?",
            "options": ["Présent", "Imparfait", "Passé composé", "Futur"],
            "correct": "Imparfait",
            "explanation": "'Je mangeais' est à l'imparfait",
            "difficulty": "medium",
            "topic": "Temps verbaux"
        },
        {
            "id": 18,
            "question": "Quel est le féminin de 'chanteur' ?",
            "options": ["Chanteur", "Chanteuse", "Chantrice", "Chanteure"],
            "correct": "Chanteuse",
            "explanation": "Le féminin de 'chanteur' est 'chanteuse'",
            "difficulty": "medium",
            "topic": "Formation du féminin"
        },
        {
            "id": 19,
            "question": "Combien de syllabes dans 'téléphone' ?",
            "options": ["3", "4", "5", "6"],
            "correct": "4",
            "explanation": "'téléphone' se divise en 4 syllabes : té-lé-pho-ne",
            "difficulty": "medium",
            "topic": "Phonétique"
        },
        {
            "id": 20,
            "question": "Quel est le sens de 'lentement' ?",
            "options": ["Vite", "Lentement", "Doucement", "Fortement"],
            "correct": "Lentement",
            "explanation": "'Lentement' signifie 'avec lenteur'",
            "difficulty": "medium",
            "topic": "Adverbes"
        },
        {
            "id": 21,
            "question": "Complétez : 'Les garçons ___ au football.'",
            "options": ["joue", "jouent", "joues", "jouer"],
            "correct": "jouent",
            "explanation": "Avec le sujet 'Les garçons' (pluriel), le verbe 'jouer' prend la terminaison '-ent'",
            "difficulty": "medium",
            "topic": "Accords"
        },
        {
            "id": 22,
            "question": "Quel temps verbal dans 'Je mangerai une pomme' ?",
            "options": ["Présent", "Imparfait", "Passé composé", "Futur"],
            "correct": "Futur",
            "explanation": "'Je mangerai' est au futur simple",
            "difficulty": "medium",
            "topic": "Temps verbaux"
        },
        {
            "id": 23,
            "question": "Quel est le féminin de 'professeur' ?",
            "options": ["Professeur", "Professeure", "Professeuse", "Professrice"],
            "correct": "Professeure",
            "explanation": "Le féminin de 'professeur' est 'professeure'",
            "difficulty": "medium",
            "topic": "Formation du féminin"
        },
        {
            "id": 24,
            "question": "Combien de syllabes dans 'université' ?",
            "options": ["4", "5", "6", "7"],
            "correct": "5",
            "explanation": "'université' se divise en 5 syllabes : u-ni-ver-si-té",
            "difficulty": "medium",
            "topic": "Phonétique"
        },
        {
            "id": 25,
            "question": "Quel est le sens de 'doucement' ?",
            "options": ["Vite", "Lentement", "Doucement", "Fortement"],
            "correct": "Doucement",
            "explanation": "'Doucement' signifie 'avec douceur'",
            "difficulty": "medium",
            "topic": "Adverbes"
        }
    ],
    "hard": [
        # Grammaire avancée et analyse (ID 26-40)
        {
            "id": 26,
            "question": "Quel est le mode du verbe dans 'Veuillez patienter' ?",
            "options": ["Indicatif", "Subjonctif", "Impératif", "Conditionnel"],
            "correct": "Impératif",
            "explanation": "'Veuillez' est à l'impératif, forme de politesse",
            "difficulty": "hard",
            "topic": "Modes verbaux"
        },
        {
            "id": 27,
            "question": "Quel est le type de phrase 'Quelle belle journée !' ?",
            "options": ["Déclarative", "Interrogative", "Exclamative", "Impérative"],
            "correct": "Exclamative",
            "explanation": "Cette phrase exprime une exclamation, c'est une phrase exclamative",
            "difficulty": "hard",
            "topic": "Types de phrases"
        },
        {
            "id": 28,
            "question": "Quel est le registre de langue de 'bagnole' ?",
            "options": ["Soutenu", "Courant", "Familier", "Argotique"],
            "correct": "Familier",
            "explanation": "'Bagnole' est un terme familier pour désigner une voiture",
            "difficulty": "hard",
            "topic": "Registres de langue"
        },
        {
            "id": 29,
            "question": "Quel est le sens figuré de 'avoir le cafard' ?",
            "options": ["Être malade", "Être triste", "Être fatigué", "Être en colère"],
            "correct": "Être triste",
            "explanation": "'Avoir le cafard' signifie être triste ou déprimé (expression figurée)",
            "difficulty": "hard",
            "topic": "Expressions idiomatiques"
        },
        {
            "id": 30,
            "question": "Quel est le type de complément dans 'Il mange une pomme' ?",
            "options": ["Complément d'objet direct", "Complément d'objet indirect", "Complément circonstanciel", "Attribut"],
            "correct": "Complément d'objet direct",
            "explanation": "'Une pomme' est le complément d'objet direct du verbe 'mange'",
            "difficulty": "hard",
            "topic": "Analyse grammaticale"
        },
        {
            "id": 31,
            "question": "Quel est le mode du verbe dans 'Il faut que tu viennes' ?",
            "options": ["Indicatif", "Subjonctif", "Impératif", "Conditionnel"],
            "correct": "Subjonctif",
            "explanation": "'Il faut que' exige l'emploi du subjonctif",
            "difficulty": "hard",
            "topic": "Modes verbaux"
        },
        {
            "id": 32,
            "question": "Quel est le type de phrase 'Où vas-tu ?' ?",
            "options": ["Déclarative", "Interrogative", "Exclamative", "Impérative"],
            "correct": "Interrogative",
            "explanation": "Cette phrase pose une question, c'est une phrase interrogative",
            "difficulty": "hard",
            "topic": "Types de phrases"
        },
        {
            "id": 33,
            "question": "Quel est le registre de langue de 'véhicule' ?",
            "options": ["Soutenu", "Courant", "Familier", "Argotique"],
            "correct": "Soutenu",
            "explanation": "'Véhicule' est un terme soutenu pour désigner un moyen de transport",
            "difficulty": "hard",
            "topic": "Registres de langue"
        },
        {
            "id": 34,
            "question": "Quel est le sens figuré de 'casser les pieds' ?",
            "options": ["Blesser", "Ennuyer", "Fatiguer", "Aider"],
            "correct": "Ennuyer",
            "explanation": "'Casser les pieds' signifie ennuyer quelqu'un (expression figurée)",
            "difficulty": "hard",
            "topic": "Expressions idiomatiques"
        },
        {
            "id": 35,
            "question": "Quel est le type de complément dans 'Il parle à son ami' ?",
            "options": ["Complément d'objet direct", "Complément d'objet indirect", "Complément circonstanciel", "Attribut"],
            "correct": "Complément d'objet indirect",
            "explanation": "'À son ami' est le complément d'objet indirect du verbe 'parle'",
            "difficulty": "hard",
            "topic": "Analyse grammaticale"
        },
        {
            "id": 36,
            "question": "Quel est le mode du verbe dans 'Si j'étais riche, je voyagerais' ?",
            "options": ["Indicatif", "Subjonctif", "Impératif", "Conditionnel"],
            "correct": "Conditionnel",
            "explanation": "'Je voyagerais' est au conditionnel présent",
            "difficulty": "hard",
            "topic": "Modes verbaux"
        },
        {
            "id": 37,
            "question": "Quel est le type de phrase 'Fermez la porte !' ?",
            "options": ["Déclarative", "Interrogative", "Exclamative", "Impérative"],
            "correct": "Impérative",
            "explanation": "Cette phrase donne un ordre, c'est une phrase impérative",
            "difficulty": "hard",
            "topic": "Types de phrases"
        },
        {
            "id": 38,
            "question": "Quel est le registre de langue de 'auto' ?",
            "options": ["Soutenu", "Courant", "Familier", "Argotique"],
            "correct": "Courant",
            "explanation": "'Auto' est un terme courant pour désigner une voiture",
            "difficulty": "hard",
            "topic": "Registres de langue"
        },
        {
            "id": 39,
            "question": "Quel est le sens figuré de 'avoir la pêche' ?",
            "options": ["Être malade", "Être triste", "Être en forme", "Être fatigué"],
            "correct": "Être en forme",
            "explanation": "'Avoir la pêche' signifie être en forme et énergique (expression figurée)",
            "difficulty": "hard",
            "topic": "Expressions idiomatiques"
        },
        {
            "id": 40,
            "question": "Quel est le type de complément dans 'Il est devenu professeur' ?",
            "options": ["Complément d'objet direct", "Complément d'objet indirect", "Complément circonstanciel", "Attribut"],
            "correct": "Attribut",
            "explanation": "'Professeur' est l'attribut du sujet 'Il'",
            "difficulty": "hard",
            "topic": "Analyse grammaticale"
        }
    ]
}

# ============================================================================
# FONCTIONS UTILITAIRES
# ============================================================================

def generate_dynamic_question(template_type: str, difficulty: str) -> Dict[str, Any]:
    """Génère une question dynamique basée sur un template"""
    
    if template_type == "articles" and difficulty in ARTICLE_TEMPLATES:
        template = random.choice(ARTICLE_TEMPLATES[difficulty])
        noun_data = random.choice(template["nouns"])
        
        question = template["template"].format(noun=noun_data["word"])
        
        return {
            "id": random.randint(1000, 9999),  # ID unique pour questions dynamiques
            "question": question,
            "options": ["Le", "La", "Les", "L'"],
            "correct": noun_data["article"],
            "explanation": noun_data["explanation"],
            "difficulty": difficulty,
            "topic": "Articles",
            "is_dynamic": True
        }
    
    elif template_type == "conjugation" and difficulty in CONJUGATION_TEMPLATES:
        template = random.choice(CONJUGATION_TEMPLATES[difficulty])
        
        # Vérifier si le template a la structure attendue
        if "verbs" in template:
            # Template de conjugaison avec verbes
            verb_data = random.choice(template["verbs"])
            person = random.choice(template["persons"])
            number = random.choice(template["numbers"])
            
            question = template["template"].format(
                verb=verb_data["verb"],
                person=person,
                number=number
            )
            
            # Déterminer la bonne réponse
            if person == "1ère" and number == "singulier":
                correct = verb_data["conjugations"]["1s"]
            elif person == "2ème" and number == "singulier":
                correct = verb_data["conjugations"]["2s"]
            elif person == "3ème" and number == "singulier":
                correct = verb_data["conjugations"]["3s"]
            elif person == "1ère" and number == "pluriel":
                correct = verb_data["conjugations"]["1p"]
            elif person == "2ème" and number == "pluriel":
                correct = verb_data["conjugations"]["2p"]
            else:
                correct = verb_data["conjugations"]["3p"]
            
            return {
                "id": random.randint(1000, 9999),
                "question": question,
                "options": list(verb_data["conjugations"].values()),
                "correct": correct,
                "explanation": f"Conjugaison du verbe '{verb_data['verb']}' à la {person} personne du {number}",
                "difficulty": difficulty,
                "topic": "Conjugaison",
                "is_dynamic": True
            }
        
        elif "sentences" in template:
            # Template de temps verbaux
            sentence_data = random.choice(template["sentences"])
            
            question = template["template"].format(sentence=sentence_data["sentence"])
            
            return {
                "id": random.randint(1000, 9999),
                "question": question,
                "options": ["Présent", "Imparfait", "Passé composé", "Futur simple"],
                "correct": sentence_data["tense"],
                "explanation": sentence_data["explanation"],
                "difficulty": difficulty,
                "topic": "Temps verbaux",
                "is_dynamic": True
            }
    
    # Fallback vers questions statiques
    return random.choice(ENHANCED_FRENCH_QUESTIONS[difficulty])

def get_question_pool(difficulty: str, include_dynamic: bool = True) -> List[Dict[str, Any]]:
    """Récupère le pool de questions pour une difficulté donnée"""
    
    questions = ENHANCED_FRENCH_QUESTIONS[difficulty].copy()
    
    if include_dynamic:
        # Ajouter quelques questions dynamiques
        dynamic_questions = []
        
        if difficulty == "easy":
            dynamic_questions.append(generate_dynamic_question("articles", difficulty))
        elif difficulty == "medium":
            dynamic_questions.append(generate_dynamic_question("conjugation", difficulty))
        
        questions.extend(dynamic_questions)
    
    return questions

def get_total_questions_count() -> Dict[str, int]:
    """Retourne le nombre total de questions par niveau"""
    return {
        "easy": len(ENHANCED_FRENCH_QUESTIONS["easy"]),
        "medium": len(ENHANCED_FRENCH_QUESTIONS["medium"]),
        "hard": len(ENHANCED_FRENCH_QUESTIONS["hard"]),
        "total": sum(len(questions) for questions in ENHANCED_FRENCH_QUESTIONS.values())
    }
