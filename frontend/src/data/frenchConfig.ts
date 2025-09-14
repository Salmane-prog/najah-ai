export interface FrenchLevel {
  id: string;
  name: string;
  description: string;
  difficultyRange: [number, number];
  topics: string[];
  learningObjectives: string[];
}

export interface FrenchTopic {
  id: string;
  name: string;
  description: string;
  difficulty: number;
  subTopics: string[];
}

export const FRENCH_LEVELS: FrenchLevel[] = [
  {
    id: "debutant",
    name: "Débutant (1-3)",
    description: "Niveau débutant pour les élèves de 1ère à 3ème année",
    difficultyRange: [1, 3],
    topics: ["Articles", "Conjugaison", "Vocabulaire", "Syntaxe", "Pluriel", "Adjectifs"],
    learningObjectives: [
      "Reconnaître les articles définis et indéfinis",
      "Conjuguer les verbes être et avoir au présent",
      "Comprendre le vocabulaire de base",
      "Identifier le sujet et le verbe dans une phrase simple",
      "Former le pluriel des noms",
      "Accorder les adjectifs qualificatifs"
    ]
  },
  {
    id: "intermediaire",
    name: "Intermédiaire (4-6)",
    description: "Niveau intermédiaire pour les élèves de 4ème à 6ème année",
    difficultyRange: [4, 6],
    topics: ["Conjugaison", "Temps", "Pronoms", "Adverbes", "Conjonctions", "Compréhension"],
    learningObjectives: [
      "Conjuguer les verbes du 1er et 2ème groupe au présent",
      "Utiliser le passé composé et l'imparfait",
      "Employer les pronoms personnels et relatifs",
      "Reconnaître et utiliser les adverbes",
      "Comprendre les conjonctions de coordination",
      "Analyser des textes courts"
    ]
  },
  {
    id: "avance",
    name: "Avancé (7-9)",
    description: "Niveau avancé pour les élèves de 7ème à 9ème année",
    difficultyRange: [7, 9],
    topics: ["Subjonctif", "Conditionnel", "Passif", "Discours rapporté", "Figures de style", "Littérature"],
    learningObjectives: [
      "Maîtriser le subjonctif présent et passé",
      "Utiliser le conditionnel présent et passé",
      "Transformer des phrases actives en passives",
      "Rapporter des paroles au discours indirect",
      "Identifier et analyser les figures de style",
      "Étudier des œuvres littéraires classiques"
    ]
  },
  {
    id: "expert",
    name: "Expert (10-12)",
    description: "Niveau expert pour les élèves de 10ème à 12ème année",
    difficultyRange: [10, 12],
    topics: ["Plus-que-parfait", "Subjonctif imparfait", "Gérondif", "Participe présent", "Analyse littéraire", "Dissertation"],
    learningObjectives: [
      "Maîtriser tous les temps de l'indicatif et du subjonctif",
      "Utiliser le gérondif et le participe présent",
      "Analyser des textes complexes",
      "Rédiger des dissertations argumentées",
      "Étudier l'histoire littéraire",
      "Développer un esprit critique"
    ]
  }
];

export const FRENCH_TOPICS: FrenchTopic[] = [
  {
    id: "articles",
    name: "Articles",
    description: "Articles définis, indéfinis et partitifs",
    difficulty: 1,
    subTopics: ["Articles définis", "Articles indéfinis", "Articles partitifs", "Contractions"]
  },
  {
    id: "conjugaison",
    name: "Conjugaison",
    description: "Conjugaison des verbes aux différents temps",
    difficulty: 2,
    subTopics: ["Présent", "Passé composé", "Imparfait", "Futur", "Conditionnel", "Subjonctif"]
  },
  {
    id: "vocabulaire",
    name: "Vocabulaire",
    description: "Enrichissement du vocabulaire et expressions",
    difficulty: 1,
    subTopics: ["Synonymes", "Antonymes", "Familles de mots", "Expressions idiomatiques"]
  },
  {
    id: "syntaxe",
    name: "Syntaxe",
    description: "Structure des phrases et analyse grammaticale",
    difficulty: 3,
    subTopics: ["Sujet", "Verbe", "Compléments", "Propositions", "Ponctuation"]
  },
  {
    id: "pluriel",
    name: "Pluriel",
    description: "Formation du pluriel des noms et adjectifs",
    difficulty: 2,
    subTopics: ["Pluriel en -s", "Pluriel en -x", "Pluriel irrégulier", "Accord des adjectifs"]
  },
  {
    id: "adjectifs",
    name: "Adjectifs",
    description: "Accord et emploi des adjectifs qualificatifs",
    difficulty: 2,
    subTopics: ["Accord en genre", "Accord en nombre", "Place de l'adjectif", "Degrés de comparaison"]
  },
  {
    id: "pronoms",
    name: "Pronoms",
    description: "Différents types de pronoms et leur emploi",
    difficulty: 4,
    subTopics: ["Pronoms personnels", "Pronoms relatifs", "Pronoms démonstratifs", "Pronoms possessifs"]
  },
  {
    id: "temps",
    name: "Temps",
    description: "Utilisation des différents temps verbaux",
    difficulty: 3,
    subTopics: ["Temps du passé", "Temps du présent", "Temps du futur", "Temps composés"]
  },
  {
    id: "adverbes",
    name: "Adverbes",
    description: "Formation et emploi des adverbes",
    difficulty: 4,
    subTopics: ["Adverbes de manière", "Adverbes de temps", "Adverbes de lieu", "Adverbes de quantité"]
  },
  {
    id: "conjonctions",
    name: "Conjonctions",
    description: "Conjonctions de coordination et de subordination",
    difficulty: 4,
    subTopics: ["Coordination", "Subordination", "Conjonctions temporelles", "Conjonctions causales"]
  }
];

export const getFrenchLevelById = (id: string): FrenchLevel | undefined => {
  return FRENCH_LEVELS.find(level => level.id === id);
};

export const getFrenchTopicById = (id: string): FrenchTopic | undefined => {
  return FRENCH_TOPICS.find(topic => topic.id === id);
};

export const getTopicsByDifficulty = (minDifficulty: number, maxDifficulty: number): FrenchTopic[] => {
  return FRENCH_TOPICS.filter(topic => 
    topic.difficulty >= minDifficulty && topic.difficulty <= maxDifficulty
  );
};















