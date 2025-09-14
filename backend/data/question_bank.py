"""
Banque de questions pour les tests adaptatifs
Organisée par matière et niveau de difficulté
"""

QUESTION_BANK = {
    "français": {
        "débutant": [
            {
                "id": "fr_deb_1",
                "question": "Quel est le genre du mot 'table' ?",
                "options": ["Masculin", "Féminin", "Neutre", "Variable"],
                "correct_answer": 1,
                "explication": "Le mot 'table' est féminin. On dit 'une table'."
            },
            {
                "id": "fr_deb_2",
                "question": "Conjuguez le verbe 'être' au présent de l'indicatif à la 1ère personne :",
                "options": ["Je suis", "Je serai", "J'étais", "Je serais"],
                "correct_answer": 0,
                "explication": "À la 1ère personne du présent, on dit 'je suis'."
            },
            {
                "id": "fr_deb_3",
                "question": "Identifiez la fonction du mot 'rapidement' dans la phrase : 'Il court rapidement'",
                "options": ["Sujet", "Verbe", "Complément", "Adverbe"],
                "correct_answer": 3,
                "explication": "'Rapidement' modifie le verbe 'court', c'est donc un adverbe."
            },
            {
                "id": "fr_deb_4",
                "question": "Quel est le pluriel de 'cheval' ?",
                "options": ["Chevals", "Chevaux", "Chevales", "Chevaux"],
                "correct_answer": 1,
                "explication": "Le pluriel de 'cheval' est 'chevaux'."
            },
            {
                "id": "fr_deb_5",
                "question": "Dans la phrase 'Le chat dort', quel est le sujet ?",
                "options": ["Le", "chat", "dort", "Le chat"],
                "correct_answer": 3,
                "explication": "Le sujet de la phrase est 'Le chat'."
            }
        ],
        "intermédiaire": [
            {
                "id": "fr_int_1",
                "question": "Conjuguez le verbe 'prendre' au passé composé à la 3ème personne du pluriel :",
                "options": ["Ils ont pris", "Ils ont prit", "Ils ont prendu", "Ils ont prend"],
                "correct_answer": 0,
                "explication": "Le participe passé de 'prendre' est 'pris'."
            },
            {
                "id": "fr_int_2",
                "question": "Identifiez la nature du mot 'bien' dans 'Il travaille bien' :",
                "options": ["Nom", "Adjectif", "Adverbe", "Conjonction"],
                "correct_answer": 2,
                "explication": "'Bien' modifie le verbe 'travaille', c'est un adverbe."
            },
            {
                "id": "fr_int_3",
                "question": "Quel est l'antonyme de 'rapide' ?",
                "options": ["Lent", "Vite", "Prompt", "Accéléré"],
                "correct_answer": 0,
                "explication": "L'antonyme de 'rapide' est 'lent'."
            },
            {
                "id": "fr_int_4",
                "question": "Dans 'La belle voiture rouge', quel est l'adjectif qualificatif ?",
                "options": ["La", "belle", "voiture", "rouge"],
                "correct_answer": 1,
                "explication": "'Belle' est l'adjectif qualificatif qui qualifie 'voiture'."
            },
            {
                "id": "fr_int_5",
                "question": "Conjuguez 'aller' au futur simple à la 2ème personne du singulier :",
                "options": ["Tu vas", "Tu iras", "Tu alleras", "Tu alleras"],
                "correct_answer": 1,
                "explication": "Le futur de 'aller' est 'iras' à la 2ème personne."
            }
        ],
        "avancé": [
            {
                "id": "fr_adv_1",
                "question": "Identifiez la figure de style dans 'Le soleil se couche dans un lit de nuages' :",
                "options": ["Métaphore", "Comparaison", "Hyperbole", "Personnification"],
                "correct_answer": 0,
                "explication": "C'est une métaphore : les nuages sont comparés à un lit."
            },
            {
                "id": "fr_adv_2",
                "question": "Analysez la fonction de 'que' dans 'Je pense qu'il viendra' :",
                "options": ["Pronom relatif", "Conjonction de subordination", "Adverbe", "Préposition"],
                "correct_answer": 1,
                "explication": "'Que' introduit une proposition subordonnée, c'est une conjonction."
            },
            {
                "id": "fr_adv_3",
                "question": "Quel est le registre de langue de 'bagnole' ?",
                "options": ["Soutenu", "Courant", "Familier", "Argotique"],
                "correct_answer": 2,
                "explication": "'Bagnole' appartient au registre familier."
            },
            {
                "id": "fr_adv_4",
                "question": "Identifiez le champ lexical dans 'mer, océan, vague, bateau' :",
                "options": ["Marine", "Transport", "Eau", "Navigation"],
                "correct_answer": 0,
                "explication": "Ces mots appartiennent au champ lexical de la marine."
            },
            {
                "id": "fr_adv_5",
                "question": "Conjuguez 'savoir' au subjonctif présent à la 1ère personne du pluriel :",
                "options": ["Nous savons", "Nous sachions", "Nous savions", "Nous sachons"],
                "correct_answer": 3,
                "explication": "Au subjonctif présent, on dit 'nous sachons'."
            }
        ]
    },
    
    "mathématiques": {
        "débutant": [
            {
                "id": "math_deb_1",
                "question": "Résolvez l'équation : 2x + 5 = 13",
                "options": ["x = 3", "x = 4", "x = 5", "x = 6"],
                "correct_answer": 1,
                "explication": "2x + 5 = 13 → 2x = 8 → x = 4"
            },
            {
                "id": "math_deb_2",
                "question": "Calculez l'aire d'un rectangle de longueur 8 cm et largeur 5 cm",
                "options": ["13 cm²", "26 cm²", "40 cm²", "45 cm²"],
                "correct_answer": 2,
                "explication": "Aire = longueur × largeur = 8 × 5 = 40 cm²"
            },
            {
                "id": "math_deb_3",
                "question": "Simplifiez l'expression : 3x + 2x - x",
                "options": ["4x", "5x", "6x", "7x"],
                "correct_answer": 0,
                "explication": "3x + 2x - x = (3+2-1)x = 4x"
            },
            {
                "id": "math_deb_4",
                "question": "Quel est le périmètre d'un carré de côté 6 cm ?",
                "options": ["12 cm", "18 cm", "24 cm", "36 cm"],
                "correct_answer": 2,
                "explication": "Périmètre = 4 × côté = 4 × 6 = 24 cm"
            },
            {
                "id": "math_deb_5",
                "question": "Calculez : 15 ÷ 3 + 4 × 2",
                "options": ["13", "14", "15", "16"],
                "correct_answer": 0,
                "explication": "15 ÷ 3 + 4 × 2 = 5 + 8 = 13"
            }
        ],
        "intermédiaire": [
            {
                "id": "math_int_1",
                "question": "Résolvez l'équation : 3x² - 12 = 0",
                "options": ["x = ±2", "x = ±4", "x = ±6", "x = ±8"],
                "correct_answer": 0,
                "explication": "3x² = 12 → x² = 4 → x = ±2"
            },
            {
                "id": "math_int_2",
                "question": "Calculez l'aire d'un cercle de rayon 5 cm",
                "options": ["25π cm²", "50π cm²", "75π cm²", "100π cm²"],
                "correct_answer": 0,
                "explication": "Aire = πr² = π × 5² = 25π cm²"
            },
            {
                "id": "math_int_3",
                "question": "Factorisez : x² - 9",
                "options": ["(x-3)(x+3)", "(x-9)(x+9)", "(x-3)²", "(x+3)²"],
                "correct_answer": 0,
                "explication": "x² - 9 = x² - 3² = (x-3)(x+3)"
            },
            {
                "id": "math_int_4",
                "question": "Résolvez le système : x + y = 5 et 2x - y = 1",
                "options": ["x=2, y=3", "x=3, y=2", "x=1, y=4", "x=4, y=1"],
                "correct_answer": 0,
                "explication": "En additionnant : 3x = 6 → x = 2, puis y = 3"
            },
            {
                "id": "math_int_5",
                "question": "Calculez la dérivée de f(x) = 3x² + 2x",
                "options": ["6x + 2", "6x + 1", "3x + 2", "3x + 1"],
                "correct_answer": 0,
                "explication": "f'(x) = 2×3x + 2 = 6x + 2"
            }
        ],
        "avancé": [
            {
                "id": "math_adv_1",
                "question": "Résolvez l'équation : e^x = 8",
                "options": ["x = ln(8)", "x = log(8)", "x = 8", "x = e^8"],
                "correct_answer": 0,
                "explication": "e^x = 8 → x = ln(8)"
            },
            {
                "id": "math_adv_2",
                "question": "Calculez l'intégrale de x² dx",
                "options": ["x³/3 + C", "x³/2 + C", "2x + C", "x² + C"],
                "correct_answer": 0,
                "explication": "∫x² dx = x³/3 + C"
            },
            {
                "id": "math_adv_3",
                "question": "Quelle est la limite de (x²-1)/(x-1) quand x tend vers 1 ?",
                "options": ["0", "1", "2", "∞"],
                "correct_answer": 2,
                "explication": "Factorisation : (x-1)(x+1)/(x-1) = x+1 → limite = 2"
            },
            {
                "id": "math_adv_4",
                "question": "Résolvez l'équation différentielle : y' = 2y",
                "options": ["y = Ce^(2x)", "y = Ce^(-2x)", "y = Cx²", "y = C/x"],
                "correct_answer": 0,
                "explication": "La solution est y = Ce^(2x)"
            },
            {
                "id": "math_adv_5",
                "question": "Calculez le déterminant de la matrice [[2,1],[3,4]]",
                "options": ["5", "6", "7", "8"],
                "correct_answer": 0,
                "explication": "det = 2×4 - 1×3 = 8 - 3 = 5"
            }
        ]
    },
    
    "histoire": {
        "débutant": [
            {
                "id": "hist_deb_1",
                "question": "En quelle année a eu lieu la Révolution française ?",
                "options": ["1789", "1799", "1809", "1819"],
                "correct_answer": 0,
                "explication": "La Révolution française a commencé en 1789."
            },
            {
                "id": "hist_deb_2",
                "question": "Qui était Napoléon Bonaparte ?",
                "options": ["Un roi", "Un empereur", "Un président", "Un général"],
                "correct_answer": 1,
                "explication": "Napoléon Bonaparte était empereur des Français."
            },
            {
                "id": "hist_deb_3",
                "question": "Quel événement marque le début de la Révolution française ?",
                "options": ["La prise de la Bastille", "Le serment du Jeu de Paume", "La Déclaration des Droits de l'Homme", "L'exécution de Louis XVI"],
                "correct_answer": 0,
                "explication": "La prise de la Bastille le 14 juillet 1789 marque le début."
            },
            {
                "id": "hist_deb_4",
                "question": "Quel roi régnait en France avant la Révolution ?",
                "options": ["Louis XIV", "Louis XV", "Louis XVI", "Louis XVII"],
                "correct_answer": 2,
                "explication": "Louis XVI régnait avant la Révolution française."
            },
            {
                "id": "hist_deb_5",
                "question": "Quelle était la devise de la Révolution française ?",
                "options": ["Liberté, Égalité, Fraternité", "Paix, Amour, Harmonie", "Justice, Vérité, Honneur", "Gloire, Honneur, Patrie"],
                "correct_answer": 0,
                "explication": "La devise était 'Liberté, Égalité, Fraternité'."
            }
        ],
        "intermédiaire": [
            {
                "id": "hist_int_1",
                "question": "Quel traité met fin à la Première Guerre mondiale ?",
                "options": ["Traité de Versailles", "Traité de Trianon", "Traité de Saint-Germain", "Traité de Sèvres"],
                "correct_answer": 0,
                "explication": "Le Traité de Versailles (1919) met fin à la guerre."
            },
            {
                "id": "hist_int_2",
                "question": "Qui était Charles de Gaulle ?",
                "options": ["Un roi", "Un président", "Un général", "Un ministre"],
                "correct_answer": 2,
                "explication": "Charles de Gaulle était général et chef de la Résistance."
            },
            {
                "id": "hist_int_3",
                "question": "En quelle année a eu lieu la chute du mur de Berlin ?",
                "options": ["1987", "1988", "1989", "1990"],
                "correct_answer": 2,
                "explication": "Le mur de Berlin est tombé le 9 novembre 1989."
            },
            {
                "id": "hist_int_4",
                "question": "Quel événement marque le début de la Seconde Guerre mondiale ?",
                "options": ["L'invasion de la Pologne", "L'attaque de Pearl Harbor", "La bataille de Stalingrad", "Le débarquement de Normandie"],
                "correct_answer": 0,
                "explication": "L'invasion de la Pologne par l'Allemagne en 1939."
            },
            {
                "id": "hist_int_5",
                "question": "Qui était Jeanne d'Arc ?",
                "options": ["Une reine", "Une sainte", "Une héroïne", "Une artiste"],
                "correct_answer": 2,
                "explication": "Jeanne d'Arc était une héroïne de la guerre de Cent Ans."
            }
        ],
        "avancé": [
            {
                "id": "hist_adv_1",
                "question": "Quel philosophe a écrit 'Le Contrat social' ?",
                "options": ["Voltaire", "Rousseau", "Montesquieu", "Diderot"],
                "correct_answer": 1,
                "explication": "Jean-Jacques Rousseau a écrit 'Le Contrat social'."
            },
            {
                "id": "hist_adv_2",
                "question": "Quel était le nom de la première République française ?",
                "options": ["République française", "République démocratique", "République populaire", "République sociale"],
                "correct_answer": 0,
                "explication": "La première République française (1792-1804)."
            },
            {
                "id": "hist_adv_3",
                "question": "Quel traité met fin à la guerre de Cent Ans ?",
                "options": ["Traité de Troyes", "Traité de Brétigny", "Traité de Calais", "Traité de Paris"],
                "correct_answer": 1,
                "explication": "Le Traité de Brétigny (1360) met fin à la guerre."
            },
            {
                "id": "hist_adv_4",
                "question": "Qui était Richelieu ?",
                "options": ["Un roi", "Un cardinal", "Un général", "Un ministre"],
                "correct_answer": 1,
                "explication": "Richelieu était cardinal et ministre de Louis XIII."
            },
            {
                "id": "hist_adv_5",
                "question": "En quelle année a eu lieu la bataille de Waterloo ?",
                "options": ["1813", "1814", "1815", "1816"],
                "correct_answer": 2,
                "explication": "La bataille de Waterloo a eu lieu le 18 juin 1815."
            }
        ]
    },
    
    "sciences": {
        "débutant": [
            {
                "id": "sci_deb_1",
                "question": "Quel est le symbole chimique de l'oxygène ?",
                "options": ["O", "Ox", "Oxy", "O2"],
                "correct_answer": 0,
                "explication": "Le symbole chimique de l'oxygène est O."
            },
            {
                "id": "sci_deb_2",
                "question": "Quelle est la formule de l'eau ?",
                "options": ["H2O", "CO2", "O2", "H2"],
                "correct_answer": 0,
                "explication": "La formule de l'eau est H2O."
            },
            {
                "id": "sci_deb_3",
                "question": "Quel organe pompe le sang dans le corps ?",
                "options": ["Le cerveau", "Le cœur", "Les poumons", "Le foie"],
                "correct_answer": 1,
                "explication": "Le cœur pompe le sang dans tout le corps."
            },
            {
                "id": "sci_deb_4",
                "question": "Quelle est la planète la plus proche du Soleil ?",
                "options": ["Vénus", "Mercure", "Mars", "Terre"],
                "correct_answer": 1,
                "explication": "Mercure est la planète la plus proche du Soleil."
            },
            {
                "id": "sci_deb_5",
                "question": "Quel est l'état de l'eau à 100°C ?",
                "options": ["Solide", "Liquide", "Gazeux", "Plasma"],
                "correct_answer": 2,
                "explication": "À 100°C, l'eau passe à l'état gazeux (vapeur)."
            }
        ],
        "intermédiaire": [
            {
                "id": "sci_int_1",
                "question": "Quel est le pH d'une solution neutre ?",
                "options": ["0", "7", "14", "10"],
                "correct_answer": 1,
                "explication": "Une solution neutre a un pH de 7."
            },
            {
                "id": "sci_int_2",
                "question": "Quelle est la formule de la photosynthèse ?",
                "options": ["6CO2 + 6H2O → C6H12O6 + 6O2", "C6H12O6 + 6O2 → 6CO2 + 6H2O", "2H2 + O2 → 2H2O", "NaCl + H2O → Na+ + Cl-"],
                "correct_answer": 0,
                "explication": "6CO2 + 6H2O + lumière → C6H12O6 + 6O2"
            },
            {
                "id": "sci_int_3",
                "question": "Quel est le nom de la force qui attire les objets vers la Terre ?",
                "options": ["Force magnétique", "Force gravitationnelle", "Force électrique", "Force nucléaire"],
                "correct_answer": 1,
                "explication": "La force gravitationnelle attire les objets vers la Terre."
            },
            {
                "id": "sci_int_4",
                "question": "Quel est le nom de la cellule reproductrice mâle ?",
                "options": ["Ovule", "Spermatozoïde", "Zygote", "Gamète"],
                "correct_answer": 1,
                "explication": "Le spermatozoïde est la cellule reproductrice mâle."
            },
            {
                "id": "sci_int_5",
                "question": "Quel est le nom de l'énergie stockée dans les aliments ?",
                "options": ["Énergie cinétique", "Énergie potentielle", "Énergie chimique", "Énergie thermique"],
                "correct_answer": 2,
                "explication": "L'énergie chimique est stockée dans les aliments."
            }
        ],
        "avancé": [
            {
                "id": "sci_adv_1",
                "question": "Quel est le nom de la théorie qui explique l'évolution des espèces ?",
                "options": ["Théorie de la gravitation", "Théorie de l'évolution", "Théorie de la relativité", "Théorie quantique"],
                "correct_answer": 1,
                "explication": "La théorie de l'évolution explique l'évolution des espèces."
            },
            {
                "id": "sci_adv_2",
                "question": "Quel est le nom de la particule élémentaire de charge positive ?",
                "options": ["Électron", "Proton", "Neutron", "Photon"],
                "correct_answer": 1,
                "explication": "Le proton est la particule élémentaire de charge positive."
            },
            {
                "id": "sci_adv_3",
                "question": "Quel est le nom de la réaction qui libère de l'énergie ?",
                "options": ["Réaction endothermique", "Réaction exothermique", "Réaction catalytique", "Réaction enzymatique"],
                "correct_answer": 1,
                "explication": "Une réaction exothermique libère de l'énergie."
            },
            {
                "id": "sci_adv_4",
                "question": "Quel est le nom de la structure qui contient l'ADN ?",
                "options": ["Noyau", "Cytoplasme", "Mitochondrie", "Ribosome"],
                "correct_answer": 0,
                "explication": "L'ADN est contenu dans le noyau de la cellule."
            },
            {
                "id": "sci_adv_5",
                "question": "Quel est le nom de la vitesse de la lumière ?",
                "options": ["300 000 km/s", "200 000 km/s", "400 000 km/s", "500 000 km/s"],
                "correct_answer": 0,
                "explication": "La vitesse de la lumière est d'environ 300 000 km/s."
            }
        ]
    }
}

def get_questions_by_subject_and_level(subject: str, level: str, count: int = 5) -> list:
    """Récupérer des questions par matière et niveau."""
    subject_lower = subject.lower()
    
    if subject_lower not in QUESTION_BANK:
        return []
    
    if level.lower() not in QUESTION_BANK[subject_lower]:
        return []
    
    questions = QUESTION_BANK[subject_lower][level.lower()]
    return questions[:count]

def get_available_subjects() -> list:
    """Récupérer la liste des matières disponibles."""
    return list(QUESTION_BANK.keys())

def get_available_levels(subject: str) -> list:
    """Récupérer la liste des niveaux disponibles pour une matière."""
    subject_lower = subject.lower()
    if subject_lower not in QUESTION_BANK:
        return []
    return list(QUESTION_BANK[subject_lower].keys()) 