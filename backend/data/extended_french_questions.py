#!/usr/bin/env python3
"""
Banque étendue de questions françaises (100+ questions)
Niveaux A0-C2 avec sélection intelligente
"""

import random
from typing import List, Dict, Any, Optional

# Banque de questions étendue par niveau
EXTENDED_FRENCH_QUESTIONS = {
    "A0": [
        # Questions ultra-basiques (débutant absolu)
        {"id": "A0_1", "question": "Comment dit-on 'bonjour' en français ?", "options": ["Hello", "Bonjour", "Salut", "Bonsoir"], "correct": "Bonjour", "explanation": "Bonjour est la salutation standard en français", "difficulty": "A0", "topic": "Salutations"},
        {"id": "A0_2", "question": "Quel est le mot pour 'oui' ?", "options": ["Oui", "Non", "Peut-être", "Sûrement"], "correct": "Oui", "explanation": "Oui signifie 'yes' en anglais", "difficulty": "A0", "topic": "Vocabulaire de base"},
        {"id": "A0_3", "question": "Comment dit-on 'merci' ?", "options": ["Merci", "S'il vous plaît", "De rien", "Pardon"], "correct": "Merci", "explanation": "Merci signifie 'thank you' en anglais", "difficulty": "A0", "topic": "Politesse"},
        {"id": "A0_4", "question": "Quel est le mot pour 'eau' ?", "options": ["Eau", "Pain", "Lait", "Vin"], "correct": "Eau", "explanation": "Eau signifie 'water' en anglais", "difficulty": "A0", "topic": "Nourriture et boissons"},
        {"id": "A0_5", "question": "Comment dit-on 'au revoir' ?", "options": ["Au revoir", "Bonjour", "Merci", "S'il vous plaît"], "correct": "Au revoir", "explanation": "Au revoir signifie 'goodbye' en anglais", "difficulty": "A0", "topic": "Salutations"},
    ],
    
    "A1": [
        # Questions de base (débutant)
        {"id": "A1_1", "question": "Quel est l'article correct ? '___ chat'", "options": ["Le", "La", "Les", "L'"], "correct": "Le", "explanation": "Chat est masculin singulier", "difficulty": "A1", "topic": "Articles"},
        {"id": "A1_2", "question": "Conjuguez 'être' à la 1ère personne : 'Je ___'", "options": ["suis", "es", "est", "sont"], "correct": "suis", "explanation": "Je suis = I am", "difficulty": "A1", "topic": "Conjugaison"},
        {"id": "A1_3", "question": "Quel est le genre de 'maison' ?", "options": ["Masculin", "Féminin", "Neutre", "Variable"], "correct": "Féminin", "explanation": "La maison = the house", "difficulty": "A1", "topic": "Genre des noms"},
        {"id": "A1_4", "question": "Pluriel de 'cheval' ?", "options": ["Chevals", "Chevaux", "Chevales", "Cheval"], "correct": "Chevaux", "explanation": "Pluriel irrégulier", "difficulty": "A1", "topic": "Pluriels"},
        {"id": "A1_5", "question": "Antonyme de 'grand' ?", "options": ["Petit", "Gros", "Long", "Large"], "correct": "Petit", "explanation": "Grand = big, Petit = small", "difficulty": "A1", "topic": "Vocabulaire"},
        {"id": "A1_6", "question": "Complétez : 'Les enfants ___ dans le jardin'", "options": ["joue", "jouent", "joues", "jouer"], "correct": "jouent", "explanation": "Accord avec sujet pluriel", "difficulty": "A1", "topic": "Accords"},
        {"id": "A1_7", "question": "Temps verbal dans 'J'ai mangé' ?", "options": ["Présent", "Imparfait", "Passé composé", "Futur"], "correct": "Passé composé", "explanation": "Avoir + participe passé", "difficulty": "A1", "topic": "Temps verbaux"},
        {"id": "A1_8", "question": "Comment dit-on 'je voudrais' ?", "options": ["Je voudrais", "Je veux", "Je vais", "Je peux"], "correct": "Je voudrais", "explanation": "Forme polie de vouloir", "difficulty": "A1", "topic": "Politesse"},
        {"id": "A1_9", "question": "Quel est le mot pour 'travail' ?", "options": ["Travail", "Maison", "École", "Magasin"], "correct": "Travail", "explanation": "Travail = work", "difficulty": "A1", "topic": "Vocabulaire"},
        {"id": "A1_10", "question": "Comment dit-on 'je ne comprends pas' ?", "options": ["Je ne comprends pas", "Je comprends", "Je vais comprendre", "Je peux comprendre"], "correct": "Je ne comprends pas", "explanation": "Forme négative", "difficulty": "A1", "topic": "Négation"},
    ],
    
    "A2": [
        # Questions intermédiaires (débutant avancé)
        {"id": "A2_1", "question": "Conjuguez 'aller' au futur : 'Je ___'", "options": ["vais", "irai", "allais", "suis allé"], "correct": "irai", "explanation": "Futur simple d'aller", "difficulty": "A2", "topic": "Futur"},
        {"id": "A2_2", "question": "Quel est l'accord correct ? 'Les filles ___ contentes'", "options": ["est", "sont", "sont", "sont"], "correct": "sont", "explanation": "Accord avec sujet pluriel féminin", "difficulty": "A2", "topic": "Accords"},
        {"id": "A2_3", "question": "Préposition : 'Je vais ___ Paris'", "options": ["à", "de", "en", "dans"], "correct": "à", "explanation": "Aller à + ville", "difficulty": "A2", "topic": "Prépositions"},
        {"id": "A2_4", "question": "Conjuguez 'faire' à l'imparfait : 'Tu ___'", "options": ["fais", "faisais", "feras", "as fait"], "correct": "faisais", "explanation": "Imparfait de faire", "difficulty": "A2", "topic": "Imparfait"},
        {"id": "A2_5", "question": "Quel est le mot pour 'déjà' ?", "options": ["Déjà", "Encore", "Toujours", "Jamais"], "correct": "Déjà", "explanation": "Déjà = already", "difficulty": "A2", "topic": "Adverbes"},
        {"id": "A2_6", "question": "Complétez : 'Si j'___ riche, je voyagerais'", "options": ["étais", "serais", "avais été", "aurais été"], "correct": "étais", "explanation": "Si + imparfait, conditionnel", "difficulty": "A2", "topic": "Conditionnel"},
        {"id": "A2_7", "question": "Quel est le genre de 'temps' (weather) ?", "options": ["Masculin", "Féminin", "Neutre", "Variable"], "correct": "Masculin", "explanation": "Le temps = the weather", "difficulty": "A2", "topic": "Genre"},
        {"id": "A2_8", "question": "Conjuguez 'voir' au présent : 'Nous ___'", "options": ["vois", "vois", "voyons", "voient"], "correct": "voyons", "explanation": "Nous voyons = we see", "difficulty": "A2", "topic": "Conjugaison"},
        {"id": "A2_9", "question": "Quel est l'antonyme de 'facile' ?", "options": ["Difficile", "Simple", "Compliqué", "Dur"], "correct": "Difficile", "explanation": "Facile = easy, Difficile = difficult", "difficulty": "A2", "topic": "Antonymes"},
        {"id": "A2_10", "question": "Comment dit-on 'je vais essayer' ?", "options": ["Je vais essayer", "J'essaie", "J'essayerai", "J'ai essayé"], "correct": "Je vais essayer", "explanation": "Futur proche", "difficulty": "A2", "topic": "Futur proche"},
    ],
    
    "B1": [
        # Questions avancées (intermédiaire)
        {"id": "B1_1", "question": "Conjuguez 'prendre' au subjonctif : 'que je ___'", "options": ["prends", "prenne", "prendrai", "prenais"], "correct": "prenne", "explanation": "Subjonctif présent de prendre", "difficulty": "B1", "topic": "Subjonctif"},
        {"id": "B1_2", "question": "Quel est l'accord correct ? 'La plupart des gens ___ contents'", "options": ["est", "sont", "sont", "sont"], "correct": "sont", "explanation": "La plupart + nom pluriel = verbe au pluriel", "difficulty": "B1", "topic": "Accords complexes"},
        {"id": "B1_3", "question": "Préposition : 'Je suis fier ___ toi'", "options": ["de", "à", "en", "dans"], "correct": "de", "explanation": "Être fier de + nom/pronom", "difficulty": "B1", "topic": "Prépositions avec adjectifs"},
        {"id": "B1_4", "question": "Conjuguez 'venir' au plus-que-parfait : 'j'___'", "options": ["viens", "viendrai", "étais venu", "étais venu"], "correct": "étais venu", "explanation": "Plus-que-parfait de venir", "difficulty": "B1", "topic": "Plus-que-parfait"},
        {"id": "B1_5", "question": "Quel est le mot pour 'néanmoins' ?", "options": ["Néanmoins", "Cependant", "Pourtant", "Toutefois"], "correct": "Néanmoins", "explanation": "Néanmoins = nevertheless", "difficulty": "B1", "topic": "Conjonctions"},
        {"id": "B1_6", "question": "Complétez : 'Bien que je ___ fatigué, je vais travailler'", "options": ["suis", "sois", "serais", "étais"], "correct": "sois", "explanation": "Bien que + subjonctif", "difficulty": "B1", "topic": "Subjonctif après conjonctions"},
        {"id": "B1_7", "question": "Quel est le genre de 'amour' ?", "options": ["Masculin", "Féminin", "Neutre", "Variable"], "correct": "Masculin", "explanation": "L'amour = love (masculin)", "difficulty": "B1", "topic": "Genre des noms abstraits"},
        {"id": "B1_8", "question": "Conjuguez 'pouvoir' au conditionnel : 'je ___'", "options": ["peux", "pourrais", "pouvais", "ai pu"], "correct": "pourrais", "explanation": "Conditionnel présent de pouvoir", "difficulty": "B1", "topic": "Conditionnel"},
        {"id": "B1_9", "question": "Quel est l'antonyme de 'rapidement' ?", "options": ["Lentement", "Vite", "Bientôt", "Tôt"], "correct": "Lentement", "explanation": "Rapidement = quickly, Lentement = slowly", "difficulty": "B1", "topic": "Adverbes"},
        {"id": "B1_10", "question": "Comment dit-on 'je voudrais bien' ?", "options": ["Je voudrais bien", "Je veux bien", "Je vais bien", "Je peux bien"], "correct": "Je voudrais bien", "explanation": "Forme polie et insistante", "difficulty": "B1", "topic": "Politesse avancée"},
    ],
    
    "B2": [
        # Questions très avancées (intermédiaire avancé)
        {"id": "B2_1", "question": "Conjuguez 's'asseoir' au passé simple : 'je ___'", "options": ["m'assieds", "m'assis", "m'asseyais", "me suis assis"], "correct": "m'assis", "explanation": "Passé simple de s'asseoir", "difficulty": "B2", "topic": "Passé simple"},
        {"id": "B2_2", "question": "Quel est l'accord correct ? 'L'un et l'autre ___ venus'", "options": ["est", "sont", "sont", "sont"], "correct": "sont", "explanation": "L'un et l'autre = verbe au pluriel", "difficulty": "B2", "topic": "Accords complexes"},
        {"id": "B2_3", "question": "Préposition : 'Il s'agit ___ résoudre ce problème'", "options": ["de", "à", "en", "dans"], "correct": "de", "explanation": "Il s'agit de + infinitif", "difficulty": "B2", "topic": "Expressions avec prépositions"},
        {"id": "B2_4", "question": "Conjuguez 'naître' au subjonctif imparfait : 'que je ___'", "options": ["naisse", "naquisse", "naissais", "sois né"], "correct": "naquisse", "explanation": "Subjonctif imparfait de naître", "difficulty": "B2", "topic": "Subjonctif imparfait"},
        {"id": "B2_5", "question": "Quel est le mot pour 'par conséquent' ?", "options": ["Par conséquent", "Donc", "Alors", "Ainsi"], "correct": "Par conséquent", "explanation": "Par conséquent = consequently", "difficulty": "B2", "topic": "Conjonctions logiques"},
        {"id": "B2_6", "question": "Complétez : 'À peine ___ -il parti qu'il pleuvait'", "options": ["est", "était", "fut", "soit"], "correct": "était", "explanation": "À peine + plus-que-parfait", "difficulty": "B2", "topic": "Temps avec conjonctions"},
        {"id": "B2_7", "question": "Quel est le genre de 'délai' ?", "options": ["Masculin", "Féminin", "Neutre", "Variable"], "correct": "Masculin", "explanation": "Le délai = delay (masculin)", "difficulty": "B2", "topic": "Genre des noms"},
        {"id": "B2_8", "question": "Conjuguez 'valoir' au futur antérieur : 'j'___'", "options": ["vaux", "vaudrai", "aurai valu", "avais valu"], "correct": "aurai valu", "explanation": "Futur antérieur de valoir", "difficulty": "B2", "topic": "Futur antérieur"},
        {"id": "B2_9", "question": "Quel est l'antonyme de 'évidemment' ?", "options": ["Évidemment", "Certainement", "Probablement", "Peut-être"], "correct": "Peut-être", "explanation": "Évidemment = obviously, Peut-être = maybe", "difficulty": "B2", "topic": "Adverbes de certitude"},
        {"id": "B2_10", "question": "Comment dit-on 'je tiens à préciser' ?", "options": ["Je tiens à préciser", "Je veux préciser", "Je vais préciser", "Je peux préciser"], "correct": "Je tiens à préciser", "explanation": "Forme soutenue et insistante", "difficulty": "B2", "topic": "Langage soutenu"},
    ],
    
    "C1": [
        # Questions expertes (avancé)
        {"id": "C1_1", "question": "Conjuguez 'malfaire' au subjonctif plus-que-parfait : 'que j'___'", "options": ["malfasse", "malfaisais", "malfasse", "malfasse"], "correct": "malfasse", "explanation": "Subjonctif plus-que-parfait de malfaire", "difficulty": "C1", "topic": "Subjonctif plus-que-parfait"},
        {"id": "C1_2", "question": "Quel est l'accord correct ? 'Tel père, tel fils, ___ dit-on'", "options": ["dit", "disent", "disent", "disent"], "correct": "disent", "explanation": "On = verbe au pluriel", "difficulty": "C1", "topic": "Accords avec on"},
        {"id": "C1_3", "question": "Préposition : 'Il n'y a pas lieu ___ s'inquiéter'", "options": ["de", "à", "en", "dans"], "correct": "de", "explanation": "Il n'y a pas lieu de + infinitif", "difficulty": "C1", "topic": "Expressions soutenues"},
        {"id": "C1_4", "question": "Conjuguez 'surseoir' au passé antérieur : 'j'___'", "options": ["sursois", "surseoirai", "eus sursis", "avais sursis"], "correct": "eus sursis", "explanation": "Passé antérieur de surseoir", "difficulty": "C1", "topic": "Passé antérieur"},
        {"id": "C1_5", "question": "Quel est le mot pour 'en dépit de' ?", "options": ["En dépit de", "Malgré", "Bien que", "Quoique"], "correct": "En dépit de", "explanation": "En dépit de = despite", "difficulty": "C1", "topic": "Conjonctions soutenues"},
        {"id": "C1_6", "question": "Complétez : 'N'eût été sa présence, tout ___ échoué'", "options": ["aurait", "avait", "eût", "soit"], "correct": "aurait", "explanation": "N'eût été + conditionnel passé", "difficulty": "C1", "topic": "Conditionnel avec inversion"},
        {"id": "C1_7", "question": "Quel est le genre de 'échéance' ?", "options": ["Masculin", "Féminin", "Neutre", "Variable"], "correct": "Féminin", "explanation": "L'échéance = deadline (féminin)", "difficulty": "C1", "topic": "Genre des noms abstraits"},
        {"id": "C1_8", "question": "Conjuguez 'choir' au subjonctif présent : 'que je ___'", "options": ["chois", "choie", "choie", "choie"], "correct": "choie", "explanation": "Subjonctif présent de choir", "difficulty": "C1", "topic": "Verbes irréguliers"},
        {"id": "C1_9", "question": "Quel est l'antonyme de 'incontestablement' ?", "options": ["Incontestablement", "Certainement", "Probablement", "Discutablement"], "correct": "Discutablement", "explanation": "Incontestablement = unquestionably, Discutablement = debatably", "difficulty": "C1", "topic": "Adverbes de certitude"},
        {"id": "C1_10", "question": "Comment dit-on 'je me permets de souligner' ?", "options": ["Je me permets de souligner", "Je veux souligner", "Je vais souligner", "Je peux souligner"], "correct": "Je me permets de souligner", "explanation": "Forme très soutenue et polie", "difficulty": "C1", "topic": "Langage très soutenu"},
    ],
    
    "C2": [
        # Questions maîtrise (expert)
        {"id": "C2_1", "question": "Conjuguez 'clore' au subjonctif imparfait : 'que je ___'", "options": ["close", "closais", "closisse", "eusse clos"], "correct": "closisse", "explanation": "Subjonctif imparfait de clore", "difficulty": "C2", "topic": "Subjonctif imparfait"},
        {"id": "C2_2", "question": "Quel est l'accord correct ? 'C'est moi qui ___ responsable'", "options": ["suis", "est", "suis", "suis"], "correct": "suis", "explanation": "C'est moi qui + verbe à la 1ère personne", "difficulty": "C2", "topic": "Accords avec qui"},
        {"id": "C2_3", "question": "Préposition : 'Il n'est pas question ___ céder'", "options": ["de", "à", "en", "dans"], "correct": "de", "explanation": "Il n'est pas question de + infinitif", "difficulty": "C2", "topic": "Expressions très soutenues"},
        {"id": "C2_4", "question": "Conjuguez 'traire' au plus-que-parfait du subjonctif : 'que j'___'", "options": ["traie", "trairais", "traisisse", "eusse trait"], "correct": "eusse trait", "explanation": "Plus-que-parfait du subjonctif de traire", "difficulty": "C2", "topic": "Plus-que-parfait du subjonctif"},
        {"id": "C2_5", "question": "Quel est le mot pour 'en dépit du fait que' ?", "options": ["En dépit du fait que", "Bien que", "Quoique", "Malgré que"], "correct": "En dépit du fait que", "explanation": "En dépit du fait que = despite the fact that", "difficulty": "C2", "topic": "Conjonctions très soutenues"},
        {"id": "C2_6", "question": "Complétez : 'Fût-il roi, il ___ respecté les lois'", "options": ["aurait", "avait", "eût", "soit"], "correct": "aurait", "explanation": "Fût-il + conditionnel", "difficulty": "C2", "topic": "Conditionnel avec inversion soutenue"},
        {"id": "C2_7", "question": "Quel est le genre de 'échéance' ?", "options": ["Masculin", "Féminin", "Neutre", "Variable"], "correct": "Féminin", "explanation": "L'échéance = deadline (féminin)", "difficulty": "C2", "topic": "Genre des noms très abstraits"},
        {"id": "C2_8", "question": "Conjuguez 'clore' au subjonctif présent : 'que je ___'", "options": ["close", "clos", "clos", "clos"], "correct": "close", "explanation": "Subjonctif présent de clore", "difficulty": "C2", "topic": "Verbes très irréguliers"},
        {"id": "C2_9", "question": "Quel est l'antonyme de 'indubitablement' ?", "options": ["Indubitablement", "Certainement", "Probablement", "Douteusement"], "correct": "Douteusement", "explanation": "Indubitablement = undoubtedly, Douteusement = doubtfully", "difficulty": "C2", "topic": "Adverbes de certitude très soutenus"},
        {"id": "C2_10", "question": "Comment dit-on 'je me permets de vous faire observer' ?", "options": ["Je me permets de vous faire observer", "Je veux vous faire observer", "Je vais vous faire observer", "Je peux vous faire observer"], "correct": "Je me permets de vous faire observer", "explanation": "Forme ultra-soutenue et très polie", "difficulty": "C2", "topic": "Langage ultra-soutenu"},
    ]
}

def get_question_pool(difficulty: str = None, include_dynamic: bool = True) -> List[Dict[str, Any]]:
    """Récupère le pool de questions pour une difficulté donnée"""
    if difficulty:
        return EXTENDED_FRENCH_QUESTIONS.get(difficulty, [])
    
    # Retourner toutes les questions si aucune difficulté spécifiée
    all_questions = []
    for level_questions in EXTENDED_FRENCH_QUESTIONS.values():
        all_questions.extend(level_questions)
    return all_questions

def get_total_questions_count() -> Dict[str, int]:
    """Retourne le nombre total de questions par niveau"""
    counts = {}
    total = 0
    
    for level, questions in EXTENDED_FRENCH_QUESTIONS.items():
        count = len(questions)
        counts[level] = count
        total += count
    
    counts["total"] = total
    return counts

def select_questions_for_level_assessment(level: str, count: int = 10) -> List[Dict[str, Any]]:
    """Sélectionne des questions spécifiques pour évaluer un niveau"""
    questions = EXTENDED_FRENCH_QUESTIONS.get(level, [])
    if len(questions) <= count:
        return questions
    
    # Sélection intelligente : mélanger et prendre les premières
    selected = questions.copy()
    random.shuffle(selected)
    return selected[:count]

def get_questions_by_topic(topic: str, difficulty: str = None) -> List[Dict[str, Any]]:
    """Récupère les questions par topic et difficulté"""
    questions = []
    
    if difficulty:
        level_questions = EXTENDED_FRENCH_QUESTIONS.get(difficulty, [])
        questions = [q for q in level_questions if topic.lower() in q.get("topic", "").lower()]
    else:
        for level_questions in EXTENDED_FRENCH_QUESTIONS.values():
            topic_questions = [q for q in level_questions if topic.lower() in q.get("topic", "").lower()]
            questions.extend(topic_questions)
    
    return questions

def get_random_question(difficulty: str = None, exclude_ids: List[str] = None) -> Dict[str, Any]:
    """Récupère une question aléatoire en excluant certaines IDs"""
    if exclude_ids is None:
        exclude_ids = []
    
    if difficulty:
        questions = EXTENDED_FRENCH_QUESTIONS.get(difficulty, [])
    else:
        questions = get_question_pool()
    
    # Filtrer les questions exclues
    available_questions = [q for q in questions if q["id"] not in exclude_ids]
    
    if not available_questions:
        return {}
    
    return random.choice(available_questions)

if __name__ == "__main__":
    # Test de la banque de questions
    print("📚 Banque de questions françaises étendue")
    print(f"Total: {get_total_questions_count()['total']} questions")
    
    for level, count in get_total_questions_count().items():
        if level != "total":
            print(f"  {level}: {count} questions")
    
    # Test de sélection
    print("\n🧪 Test de sélection:")
    easy_questions = select_questions_for_level_assessment("A1", 3)
    for q in easy_questions:
        print(f"  - {q['question'][:50]}...")











