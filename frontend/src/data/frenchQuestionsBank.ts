export interface FrenchQuestion {
  id: number;
  question: string;
  options: string[];
  correctAnswer: number;
  explanation: string;
  difficulty: number;
  topic: string;
  learningObjective: string;
}

export const FRENCH_QUESTIONS_BANK = {
  "Débutant (1-3)": [
    // GRAMMAIRE DE BASE
    {
      id: 1,
      question: "Quel est l'article correct ? '___ chat'",
      options: ["Le", "La", "Les", "L'"],
      correctAnswer: 0,
      explanation: "Le mot 'chat' est masculin singulier, donc on utilise 'Le'",
      difficulty: 1,
      topic: "Articles",
      learningObjective: "Reconnaître les articles définis masculins"
    },
    {
      id: 2,
      question: "Quel est l'article correct ? '___ maison'",
      options: ["Le", "La", "Les", "L'"],
      correctAnswer: 1,
      explanation: "Le mot 'maison' est féminin singulier, donc on utilise 'La'",
      difficulty: 1,
      topic: "Articles",
      learningObjective: "Reconnaître les articles définis féminins"
    },
    {
      id: 3,
      question: "Quel est l'article correct ? '___ enfants'",
      options: ["Le", "La", "Les", "L'"],
      correctAnswer: 2,
      explanation: "Le mot 'enfants' est au pluriel, donc on utilise 'Les'",
      difficulty: 1,
      topic: "Articles",
      learningObjective: "Reconnaître les articles définis pluriels"
    },
    {
      id: 4,
      question: "Quel est l'article correct ? '___ arbre'",
      options: ["Le", "La", "Les", "L'"],
      correctAnswer: 0,
      explanation: "Le mot 'arbre' est masculin singulier, donc on utilise 'Le'",
      difficulty: 1,
      topic: "Articles",
      learningObjective: "Reconnaître les articles définis masculins"
    },
    {
      id: 5,
      question: "Quel est l'article correct ? '___ école'",
      options: ["Le", "La", "Les", "L'"],
      correctAnswer: 1,
      explanation: "Le mot 'école' est féminin singulier, donc on utilise 'La'",
      difficulty: 1,
      topic: "Articles",
      learningObjective: "Reconnaître les articles définis féminins"
    },
    // CONJUGAISON BASIQUE
    {
      id: 6,
      question: "Comment se conjugue 'être' à la 1ère personne du singulier ?",
      options: ["suis", "es", "est", "sont"],
      correctAnswer: 0,
      explanation: "Le verbe 'être' à la 1ère personne du singulier se conjugue 'suis'",
      difficulty: 2,
      topic: "Conjugaison",
      learningObjective: "Conjuguer le verbe être au présent"
    },
    {
      id: 7,
      question: "Comment se conjugue 'avoir' à la 2ème personne du singulier ?",
      options: ["ai", "as", "a", "ont"],
      correctAnswer: 1,
      explanation: "Le verbe 'avoir' à la 2ème personne du singulier se conjugue 'as'",
      difficulty: 2,
      topic: "Conjugaison",
      learningObjective: "Conjuguer le verbe avoir au présent"
    },
    {
      id: 8,
      question: "Comment se conjugue 'aller' à la 3ème personne du singulier ?",
      options: ["vais", "vas", "va", "vont"],
      correctAnswer: 2,
      explanation: "Le verbe 'aller' à la 3ème personne du singulier se conjugue 'va'",
      difficulty: 2,
      topic: "Conjugaison",
      learningObjective: "Conjuguer le verbe aller au présent"
    },
    {
      id: 9,
      question: "Comment se conjugue 'faire' à la 1ère personne du singulier ?",
      options: ["fais", "fais", "fait", "font"],
      correctAnswer: 0,
      explanation: "Le verbe 'faire' à la 1ère personne du singulier se conjugue 'fais'",
      difficulty: 2,
      topic: "Conjugaison",
      learningObjective: "Conjuguer le verbe faire au présent"
    },
    {
      id: 10,
      question: "Comment se conjugue 'venir' à la 2ème personne du singulier ?",
      options: ["viens", "viens", "vient", "viennent"],
      correctAnswer: 1,
      explanation: "Le verbe 'venir' à la 2ème personne du singulier se conjugue 'viens'",
      difficulty: 2,
      topic: "Conjugaison",
      learningObjective: "Conjuguer le verbe venir au présent"
    },
    // VOCABULAIRE DE BASE
    {
      id: 11,
      question: "Quel est le contraire de 'grand' ?",
      options: ["petit", "gros", "long", "court"],
      correctAnswer: 0,
      explanation: "Le contraire de 'grand' est 'petit'",
      difficulty: 1,
      topic: "Vocabulaire",
      learningObjective: "Reconnaître les antonymes"
    },
    {
      id: 12,
      question: "Quel est le contraire de 'chaud' ?",
      options: ["froid", "tiède", "tempéré", "doux"],
      correctAnswer: 0,
      explanation: "Le contraire de 'chaud' est 'froid'",
      difficulty: 1,
      topic: "Vocabulaire",
      learningObjective: "Reconnaître les antonymes"
    },
    {
      id: 13,
      question: "Quel est le contraire de 'rapide' ?",
      options: ["lent", "doux", "calme", "tranquille"],
      correctAnswer: 0,
      explanation: "Le contraire de 'rapide' est 'lent'",
      difficulty: 1,
      topic: "Vocabulaire",
      learningObjective: "Reconnaître les antonymes"
    },
    {
      id: 14,
      question: "Quel est le contraire de 'facile' ?",
      options: ["difficile", "compliqué", "complexe", "dur"],
      correctAnswer: 0,
      explanation: "Le contraire de 'facile' est 'difficile'",
      difficulty: 1,
      topic: "Vocabulaire",
      learningObjective: "Reconnaître les antonymes"
    },
    {
      id: 15,
      question: "Quel est le contraire de 'nouveau' ?",
      options: ["ancien", "vieux", "usé", "abîmé"],
      correctAnswer: 0,
      explanation: "Le contraire de 'nouveau' est 'ancien'",
      difficulty: 1,
      topic: "Vocabulaire",
      learningObjective: "Reconnaître les antonymes"
    },
    // SYNTAXE DE BASE
    {
      id: 16,
      question: "Dans la phrase 'Le chat mange', quel est le sujet ?",
      options: ["Le", "chat", "mange", "Le chat"],
      correctAnswer: 1,
      explanation: "Le sujet est 'chat' car c'est ce qui fait l'action de manger",
      difficulty: 2,
      topic: "Syntaxe",
      learningObjective: "Identifier le sujet d'une phrase simple"
    },
    {
      id: 17,
      question: "Dans la phrase 'La fille lit un livre', quel est le verbe ?",
      options: ["La", "fille", "lit", "livre"],
      correctAnswer: 2,
      explanation: "Le verbe est 'lit' car il indique l'action",
      difficulty: 2,
      topic: "Syntaxe",
      learningObjective: "Identifier le verbe d'une phrase simple"
    },
    {
      id: 18,
      question: "Dans la phrase 'Le garçon joue au football', quel est le complément ?",
      options: ["Le garçon", "joue", "au football", "joue au football"],
      correctAnswer: 2,
      explanation: "Le complément est 'au football' car il complète le verbe 'joue'",
      difficulty: 2,
      topic: "Syntaxe",
      learningObjective: "Identifier le complément d'une phrase simple"
    },
    {
      id: 19,
      question: "Dans la phrase 'Les oiseaux chantent', quel est le sujet ?",
      options: ["Les", "oiseaux", "chantent", "Les oiseaux"],
      correctAnswer: 3,
      explanation: "Le sujet est 'Les oiseaux' car c'est ce qui fait l'action de chanter",
      difficulty: 2,
      topic: "Syntaxe",
      learningObjective: "Identifier le sujet d'une phrase simple"
    },
    {
      id: 20,
      question: "Dans la phrase 'La mère cuisine le dîner', quel est le COD ?",
      options: ["La mère", "cuisine", "le dîner", "cuisine le dîner"],
      correctAnswer: 2,
      explanation: "Le COD est 'le dîner' car il répond à la question 'quoi ?' après le verbe",
      difficulty: 2,
      topic: "Syntaxe",
      learningObjective: "Identifier le complément d'objet direct"
    },
    // PLURIELS SIMPLES
    {
      id: 21,
      question: "Quel est le pluriel de 'chat' ?",
      options: ["chats", "chates", "chat", "chats"],
      correctAnswer: 0,
      explanation: "Le pluriel de 'chat' est 'chats' (ajout d'un 's')",
      difficulty: 1,
      topic: "Pluriel",
      learningObjective: "Former le pluriel des noms masculins"
    },
    {
      id: 22,
      question: "Quel est le pluriel de 'maison' ?",
      options: ["maisons", "maison", "maisones", "maisonnes"],
      correctAnswer: 0,
      explanation: "Le pluriel de 'maison' est 'maisons' (ajout d'un 's')",
      difficulty: 1,
      topic: "Pluriel",
      learningObjective: "Former le pluriel des noms féminins"
    },
    {
      id: 23,
      question: "Quel est le pluriel de 'livre' ?",
      options: ["livres", "livre", "livres", "livres"],
      correctAnswer: 0,
      explanation: "Le pluriel de 'livre' est 'livres' (ajout d'un 's')",
      difficulty: 1,
      topic: "Pluriel",
      learningObjective: "Former le pluriel des noms masculins"
    },
    {
      id: 24,
      question: "Quel est le pluriel de 'fleur' ?",
      options: ["fleurs", "fleur", "fleures", "fleurres"],
      correctAnswer: 0,
      explanation: "Le pluriel de 'fleur' est 'fleurs' (ajout d'un 's')",
      difficulty: 1,
      topic: "Pluriel",
      learningObjective: "Former le pluriel des noms féminins"
    },
    {
      id: 25,
      question: "Quel est le pluriel de 'table' ?",
      options: ["tables", "table", "tabless", "tablees"],
      correctAnswer: 0,
      explanation: "Le pluriel de 'table' est 'tables' (ajout d'un 's')",
      difficulty: 1,
      topic: "Pluriel",
      learningObjective: "Former le pluriel des noms féminins"
    },
    // ADJECTIFS QUALIFICATIFS
    {
      id: 26,
      question: "Quel est le féminin de 'grand' ?",
      options: ["grand", "grande", "grands", "grandes"],
      correctAnswer: 1,
      explanation: "L'adjectif 'grand' fait 'grande' au féminin singulier",
      difficulty: 2,
      topic: "Adjectifs",
      learningObjective: "Accorder l'adjectif qualificatif au féminin"
    },
    {
      id: 27,
      question: "Quel est le féminin de 'petit' ?",
      options: ["petit", "petite", "petits", "petites"],
      correctAnswer: 1,
      explanation: "L'adjectif 'petit' fait 'petite' au féminin singulier",
      difficulty: 2,
      topic: "Adjectifs",
      learningObjective: "Accorder l'adjectif qualificatif au féminin"
    },
    {
      id: 28,
      question: "Quel est le féminin de 'beau' ?",
      options: ["beau", "belle", "beaux", "belles"],
      correctAnswer: 1,
      explanation: "L'adjectif 'beau' fait 'belle' au féminin singulier",
      difficulty: 2,
      topic: "Adjectifs",
      learningObjective: "Accorder l'adjectif qualificatif au féminin"
    },
    {
      id: 29,
      question: "Quel est le féminin de 'nouveau' ?",
      options: ["nouveau", "nouvelle", "nouveaux", "nouvelles"],
      correctAnswer: 1,
      explanation: "L'adjectif 'nouveau' fait 'nouvelle' au féminin singulier",
      difficulty: 2,
      topic: "Adjectifs",
      learningObjective: "Accorder l'adjectif qualificatif au féminin"
    },
    {
      id: 30,
      question: "Quel est le féminin de 'vieux' ?",
      options: ["vieux", "vieille", "vieux", "vieilles"],
      correctAnswer: 1,
      explanation: "L'adjectif 'vieux' fait 'vieille' au féminin singulier",
      difficulty: 2,
      topic: "Adjectifs",
      learningObjective: "Accorder l'adjectif qualificatif au féminin"
    },
    // PRONOMS PERSONNELS
    {
      id: 31,
      question: "Quel pronom remplace 'je' ?",
      options: ["moi", "me", "mon", "ma"],
      correctAnswer: 0,
      explanation: "Le pronom 'moi' remplace 'je' dans certaines constructions",
      difficulty: 2,
      topic: "Pronoms",
      learningObjective: "Utiliser les pronoms personnels"
    },
    {
      id: 32,
      question: "Quel pronom remplace 'tu' ?",
      options: ["toi", "te", "ton", "ta"],
      correctAnswer: 0,
      explanation: "Le pronom 'toi' remplace 'tu' dans certaines constructions",
      difficulty: 2,
      topic: "Pronoms",
      learningObjective: "Utiliser les pronoms personnels"
    },
    {
      id: 33,
      question: "Quel pronom remplace 'il' ?",
      options: ["lui", "le", "son", "sa"],
      correctAnswer: 0,
      explanation: "Le pronom 'lui' remplace 'il' dans certaines constructions",
      difficulty: 2,
      topic: "Pronoms",
      learningObjective: "Utiliser les pronoms personnels"
    },
    {
      id: 34,
      question: "Quel pronom remplace 'elle' ?",
      options: ["elle", "la", "sa", "ses"],
      correctAnswer: 0,
      explanation: "Le pronom 'elle' peut se répéter pour insister",
      difficulty: 2,
      topic: "Pronoms",
      learningObjective: "Utiliser les pronoms personnels"
    },
    {
      id: 35,
      question: "Quel pronom remplace 'nous' ?",
      options: ["nous", "notre", "nos", "nous-mêmes"],
      correctAnswer: 0,
      explanation: "Le pronom 'nous' peut se répéter pour insister",
      difficulty: 2,
      topic: "Pronoms",
      learningObjective: "Utiliser les pronoms personnels"
    },
    // TEMPS SIMPLES
    {
      id: 36,
      question: "Quel temps exprime une action passée ?",
      options: ["présent", "passé composé", "futur", "conditionnel"],
      correctAnswer: 1,
      explanation: "Le passé composé exprime une action passée",
      difficulty: 2,
      topic: "Temps",
      learningObjective: "Reconnaître les temps du passé"
    },
    {
      id: 37,
      question: "Quel temps exprime une action future ?",
      options: ["présent", "passé composé", "futur simple", "imparfait"],
      correctAnswer: 2,
      explanation: "Le futur simple exprime une action future",
      difficulty: 2,
      topic: "Temps",
      learningObjective: "Reconnaître les temps du futur"
    },
    {
      id: 38,
      question: "Quel temps exprime une action en cours ?",
      options: ["présent", "passé composé", "futur", "imparfait"],
      correctAnswer: 0,
      explanation: "Le présent exprime une action en cours",
      difficulty: 2,
      topic: "Temps",
      learningObjective: "Reconnaître le présent"
    },
    {
      id: 39,
      question: "Quel temps exprime une action habituelle ?",
      options: ["présent", "passé composé", "futur", "imparfait"],
      correctAnswer: 3,
      explanation: "L'imparfait exprime une action habituelle dans le passé",
      difficulty: 2,
      topic: "Temps",
      learningObjective: "Reconnaître l'imparfait"
    },
    {
      id: 40,
      question: "Quel temps exprime une action conditionnelle ?",
      options: ["présent", "passé composé", "futur", "conditionnel"],
      correctAnswer: 3,
      explanation: "Le conditionnel exprime une action conditionnelle",
      difficulty: 2,
      topic: "Temps",
      learningObjective: "Reconnaître le conditionnel"
    },
    // COMPRÉHENSION DE BASE
    {
      id: 41,
      question: "Que signifie 'Bonjour' ?",
      options: ["Au revoir", "Bonjour", "Merci", "S'il vous plaît"],
      correctAnswer: 1,
      explanation: "'Bonjour' est une salutation utilisée le jour",
      difficulty: 1,
      topic: "Vocabulaire",
      learningObjective: "Comprendre les salutations de base"
    },
    {
      id: 42,
      question: "Que signifie 'Merci' ?",
      options: ["Au revoir", "Bonjour", "Merci", "S'il vous plaît"],
      correctAnswer: 2,
      explanation: "'Merci' exprime la gratitude",
      difficulty: 1,
      topic: "Vocabulaire",
      learningObjective: "Comprendre les expressions de politesse"
    },
    {
      id: 43,
      question: "Que signifie 'Au revoir' ?",
      options: ["Au revoir", "Bonjour", "Merci", "S'il vous plaît"],
      correctAnswer: 0,
      explanation: "'Au revoir' est une formule de séparation",
      difficulty: 1,
      topic: "Vocabulaire",
      learningObjective: "Comprendre les formules de séparation"
    },
    {
      id: 44,
      question: "Que signifie 'S'il vous plaît' ?",
      options: ["Au revoir", "Bonjour", "Merci", "S'il vous plaît"],
      correctAnswer: 3,
      explanation: "'S'il vous plaît' est une formule de politesse pour demander quelque chose",
      difficulty: 1,
      topic: "Vocabulaire",
      learningObjective: "Comprendre les formules de politesse"
    },
    {
      id: 45,
      question: "Que signifie 'Comment allez-vous ?' ?",
      options: ["Comment allez-vous ?", "Quel est votre nom ?", "Où habitez-vous ?", "Quel âge avez-vous ?"],
      correctAnswer: 0,
      explanation: "'Comment allez-vous ?' est une question sur la santé",
      difficulty: 1,
      topic: "Vocabulaire",
      learningObjective: "Comprendre les questions de politesse"
    },
    // EXPRESSIONS IDIOMATIQUES SIMPLES
    {
      id: 46,
      question: "Que signifie 'Ça va' ?",
      options: ["Ça va", "Ça ne va pas", "Comment ça va ?", "Ça va bien"],
      correctAnswer: 0,
      explanation: "'Ça va' signifie que tout va bien",
      difficulty: 2,
      topic: "Expressions",
      learningObjective: "Comprendre les expressions familières"
    },
    {
      id: 47,
      question: "Que signifie 'Pas de problème' ?",
      options: ["Il y a un problème", "Pas de problème", "C'est un problème", "Quel problème ?"],
      correctAnswer: 1,
      explanation: "'Pas de problème' signifie qu'il n'y a pas de difficulté",
      difficulty: 2,
      topic: "Expressions",
      learningObjective: "Comprendre les expressions familières"
    },
    {
      id: 48,
      question: "Que signifie 'D'accord' ?",
      options: ["Je ne suis pas d'accord", "D'accord", "Qu'est-ce que c'est ?", "Je ne comprends pas"],
      correctAnswer: 1,
      explanation: "'D'accord' signifie que l'on est en accord",
      difficulty: 2,
      topic: "Expressions",
      learningObjective: "Comprendre les expressions familières"
    },
    {
      id: 49,
      question: "Que signifie 'Pas mal' ?",
      options: ["C'est mal", "Pas mal", "C'est bien", "C'est nul"],
      correctAnswer: 1,
      explanation: "'Pas mal' signifie que c'est plutôt bien",
      difficulty: 2,
      topic: "Expressions",
      learningObjective: "Comprendre les expressions familières"
    },
    {
      id: 50,
      question: "Que signifie 'Ça marche' ?",
      options: ["Ça ne marche pas", "Ça marche", "Comment ça marche ?", "Ça va marcher"],
      correctAnswer: 1,
      explanation: "'Ça marche' signifie que cela fonctionne",
      difficulty: 2,
      topic: "Expressions",
      learningObjective: "Comprendre les expressions familières"
    }
  ],
  
  "Intermédiaire (4-6)": [
    {
      id: 51,
      question: "Conjuguez le verbe 'parler' à la 1ère personne du pluriel au présent",
      options: ["Je parle", "Tu parles", "Nous parlons", "Ils parlent"],
      correctAnswer: 2,
      explanation: "À la 1ère personne du pluriel, 'parler' se conjugue 'nous parlons'",
      difficulty: 4,
      topic: "Conjugaison",
      learningObjective: "Conjuguer les verbes du 1er groupe au présent"
    },
    {
      id: 52,
      question: "Quel est le pluriel de 'journal' ?",
      options: ["Journaux", "Journals", "Journales", "Journal"],
      correctAnswer: 0,
      explanation: "Les mots en -al font leur pluriel en -aux : journal → journaux",
      difficulty: 4,
      topic: "Pluriel",
      learningObjective: "Former le pluriel des noms en -al"
    },
    {
      id: 53,
      question: "Identifiez le sujet dans la phrase : 'Les enfants jouent dans le jardin'",
      options: ["jouent", "dans", "Les enfants", "le jardin"],
      correctAnswer: 2,
      explanation: "'Les enfants' est le sujet de la phrase, il fait l'action de jouer",
      difficulty: 4,
      topic: "Syntaxe",
      learningObjective: "Identifier le sujet dans une phrase"
    },
    {
      id: 54,
      question: "Quel est l'adverbe de manière de 'rapide' ?",
      options: ["Rapidement", "Rapide", "Rapider", "Rapidity"],
      correctAnswer: 0,
      explanation: "L'adverbe de manière se forme en ajoutant -ment à l'adjectif : rapide → rapidement",
      difficulty: 4,
      topic: "Adverbes",
      learningObjective: "Former les adverbes de manière"
    },
    {
      id: 55,
      question: "Conjuguez 'avoir' à la 3ème personne du singulier au passé composé",
      options: ["J'ai eu", "Tu as eu", "Il a eu", "Nous avons eu"],
      correctAnswer: 2,
      explanation: "À la 3ème personne du singulier, 'avoir' au passé composé se conjugue 'il a eu'",
      difficulty: 5,
      topic: "Conjugaison",
      learningObjective: "Conjuguer le verbe avoir au passé composé"
    },
    {
      id: 56,
      question: "Conjuguez le verbe 'finir' à la 2ème personne du pluriel au présent",
      options: ["Je finis", "Tu finis", "Vous finissez", "Ils finissent"],
      correctAnswer: 2,
      explanation: "À la 2ème personne du pluriel, 'finir' se conjugue 'vous finissez'",
      difficulty: 4,
      topic: "Conjugaison",
      learningObjective: "Conjuguer les verbes du 2ème groupe au présent"
    },
    {
      id: 57,
      question: "Quel est le pluriel de 'cheval' ?",
      options: ["Chevals", "Chevaux", "Chevales", "Cheval"],
      correctAnswer: 1,
      explanation: "Les mots en -al font leur pluriel en -aux : cheval → chevaux",
      difficulty: 4,
      topic: "Pluriel",
      learningObjective: "Former le pluriel des noms en -al"
    },
    {
      id: 58,
      question: "Identifiez le verbe dans la phrase : 'Les élèves écoutent attentivement'",
      options: ["Les élèves", "écoutent", "attentivement", "Les élèves écoutent"],
      correctAnswer: 1,
      explanation: "'écoutent' est le verbe de la phrase, il indique l'action",
      difficulty: 4,
      topic: "Syntaxe",
      learningObjective: "Identifier le verbe dans une phrase"
    },
    {
      id: 59,
      question: "Quel est l'adverbe de manière de 'lent' ?",
      options: ["Lentement", "Lent", "Lenter", "Lentitude"],
      correctAnswer: 0,
      explanation: "L'adverbe de manière se forme en ajoutant -ment à l'adjectif : lent → lentement",
      difficulty: 4,
      topic: "Adverbes",
      learningObjective: "Former les adverbes de manière"
    },
    {
      id: 60,
      question: "Conjuguez 'être' à la 1ère personne du pluriel au passé composé",
      options: ["J'ai été", "Tu as été", "Nous avons été", "Ils ont été"],
      correctAnswer: 2,
      explanation: "À la 1ère personne du pluriel, 'être' au passé composé se conjugue 'nous avons été'",
      difficulty: 5,
      topic: "Conjugaison",
      learningObjective: "Conjuguer le verbe être au passé composé"
    },
    {
      id: 61,
      question: "Conjuguez le verbe 'vendre' à la 3ème personne du singulier au présent",
      options: ["Je vends", "Tu vends", "Il vend", "Ils vendent"],
      correctAnswer: 2,
      explanation: "À la 3ème personne du singulier, 'vendre' se conjugue 'il vend'",
      difficulty: 4,
      topic: "Conjugaison",
      learningObjective: "Conjuguer les verbes du 3ème groupe au présent"
    },
    {
      id: 62,
      question: "Quel est le pluriel de 'animal' ?",
      options: ["Animaux", "Animals", "Animales", "Animal"],
      correctAnswer: 0,
      explanation: "Les mots en -al font leur pluriel en -aux : animal → animaux",
      difficulty: 4,
      topic: "Pluriel",
      learningObjective: "Former le pluriel des noms en -al"
    },
    {
      id: 63,
      question: "Identifiez le complément dans la phrase : 'Le professeur explique la leçon'",
      options: ["Le professeur", "explique", "la leçon", "explique la leçon"],
      correctAnswer: 2,
      explanation: "'la leçon' est le complément d'objet direct du verbe 'explique'",
      difficulty: 4,
      topic: "Syntaxe",
      learningObjective: "Identifier le complément d'objet direct"
    },
    {
      id: 64,
      question: "Quel est l'adverbe de manière de 'facile' ?",
      options: ["Facilement", "Facile", "Faciler", "Facilité"],
      correctAnswer: 0,
      explanation: "L'adverbe de manière se forme en ajoutant -ment à l'adjectif : facile → facilement",
      difficulty: 4,
      topic: "Adverbes",
      learningObjective: "Former les adverbes de manière"
    },
    {
      id: 65,
      question: "Conjuguez 'faire' à la 2ème personne du pluriel au passé composé",
      options: ["J'ai fait", "Tu as fait", "Vous avez fait", "Ils ont fait"],
      correctAnswer: 2,
      explanation: "À la 2ème personne du pluriel, 'faire' au passé composé se conjugue 'vous avez fait'",
      difficulty: 5,
      topic: "Conjugaison",
      learningObjective: "Conjuguer le verbe faire au passé composé"
    },
    {
      id: 66,
      question: "Conjuguez le verbe 'réussir' à la 1ère personne du singulier au présent",
      options: ["Je réussis", "Tu réussis", "Il réussit", "Nous réussissons"],
      correctAnswer: 0,
      explanation: "À la 1ère personne du singulier, 'réussir' se conjugue 'je réussis'",
      difficulty: 4,
      topic: "Conjugaison",
      learningObjective: "Conjuguer les verbes du 2ème groupe au présent"
    },
    {
      id: 67,
      question: "Quel est le pluriel de 'signal' ?",
      options: ["Signals", "Signaux", "Signales", "Signal"],
      correctAnswer: 1,
      explanation: "Les mots en -al font leur pluriel en -aux : signal → signaux",
      difficulty: 4,
      topic: "Pluriel",
      learningObjective: "Former le pluriel des noms en -al"
    },
    {
      id: 68,
      question: "Identifiez l'attribut dans la phrase : 'Cette maison est grande'",
      options: ["Cette maison", "est", "grande", "est grande"],
      correctAnswer: 2,
      explanation: "'grande' est l'attribut du sujet 'Cette maison'",
      difficulty: 4,
      topic: "Syntaxe",
      learningObjective: "Identifier l'attribut du sujet"
    },
    {
      id: 69,
      question: "Quel est l'adverbe de manière de 'heureux' ?",
      options: ["Heureusement", "Heureux", "Heureuser", "Heureuseté"],
      correctAnswer: 0,
      explanation: "L'adverbe de manière se forme en ajoutant -ment à l'adjectif : heureux → heureusement",
      difficulty: 4,
      topic: "Adverbes",
      learningObjective: "Former les adverbes de manière"
    },
    {
      id: 70,
      question: "Conjuguez 'aller' à la 3ème personne du pluriel au passé composé",
      options: ["Je suis allé", "Tu es allé", "Ils sont allés", "Nous sommes allés"],
      correctAnswer: 2,
      explanation: "À la 3ème personne du pluriel, 'aller' au passé composé se conjugue 'ils sont allés'",
      difficulty: 5,
      topic: "Conjugaison",
      learningObjective: "Conjuguer le verbe aller au passé composé"
    },
    {
      id: 71,
      question: "Conjuguez le verbe 'choisir' à la 2ème personne du singulier au présent",
      options: ["Je choisis", "Tu choisis", "Il choisit", "Nous choisissons"],
      correctAnswer: 1,
      explanation: "À la 2ème personne du singulier, 'choisir' se conjugue 'tu choisis'",
      difficulty: 4,
      topic: "Conjugaison",
      learningObjective: "Conjuguer les verbes du 2ème groupe au présent"
    },
    {
      id: 72,
      question: "Quel est le pluriel de 'carnaval' ?",
      options: ["Carnavals", "Carnavaux", "Carnavales", "Carnaval"],
      correctAnswer: 0,
      explanation: "Les mots en -al font leur pluriel en -s : carnaval → carnavals",
      difficulty: 4,
      topic: "Pluriel",
      learningObjective: "Former le pluriel des noms en -al"
    },
    {
      id: 73,
      question: "Identifiez le complément circonstanciel dans : 'Il travaille avec enthousiasme'",
      options: ["Il", "travaille", "avec enthousiasme", "travaille avec enthousiasme"],
      correctAnswer: 2,
      explanation: "'avec enthousiasme' est le complément circonstanciel de manière",
      difficulty: 4,
      topic: "Syntaxe",
      learningObjective: "Identifier le complément circonstanciel"
    },
    {
      id: 74,
      question: "Quel est l'adverbe de manière de 'prudent' ?",
      options: ["Prudemment", "Prudent", "Pruder", "Prudence"],
      correctAnswer: 0,
      explanation: "L'adverbe de manière se forme en ajoutant -ment à l'adjectif : prudent → prudemment",
      difficulty: 4,
      topic: "Adverbes",
      learningObjective: "Former les adverbes de manière"
    },
    {
      id: 75,
      question: "Conjuguez 'venir' à la 1ère personne du pluriel au passé composé",
      options: ["Je suis venu", "Tu es venu", "Nous sommes venus", "Ils sont venus"],
      correctAnswer: 2,
      explanation: "À la 1ère personne du pluriel, 'venir' au passé composé se conjugue 'nous sommes venus'",
      difficulty: 5,
      topic: "Conjugaison",
      learningObjective: "Conjuguer le verbe venir au passé composé"
    },
    {
      id: 76,
      question: "Conjuguez le verbe 'grandir' à la 3ème personne du singulier au présent",
      options: ["Je grandis", "Tu grandis", "Il grandit", "Nous grandissons"],
      correctAnswer: 2,
      explanation: "À la 3ème personne du singulier, 'grandir' se conjugue 'il grandit'",
      difficulty: 4,
      topic: "Conjugaison",
      learningObjective: "Conjuguer les verbes du 2ème groupe au présent"
    },
    {
      id: 77,
      question: "Quel est le pluriel de 'festival' ?",
      options: ["Festivals", "Festivaux", "Festivales", "Festival"],
      correctAnswer: 0,
      explanation: "Les mots en -al font leur pluriel en -s : festival → festivals",
      difficulty: 4,
      topic: "Pluriel",
      learningObjective: "Former le pluriel des noms en -al"
    },
    {
      id: 78,
      question: "Identifiez la proposition principale dans : 'Quand il pleut, je reste à la maison'",
      options: ["Quand il pleut", "je reste à la maison", "il pleut", "reste à la maison"],
      correctAnswer: 1,
      explanation: "'je reste à la maison' est la proposition principale",
      difficulty: 4,
      topic: "Syntaxe",
      learningObjective: "Identifier la proposition principale"
    },
    {
      id: 79,
      question: "Quel est l'adverbe de manière de 'constant' ?",
      options: ["Constamment", "Constant", "Constanter", "Constance"],
      correctAnswer: 0,
      explanation: "L'adverbe de manière se forme en ajoutant -ment à l'adjectif : constant → constamment",
      difficulty: 4,
      topic: "Adverbes",
      learningObjective: "Former les adverbes de manière"
    },
    {
      id: 80,
      question: "Conjuguez 'prendre' à la 2ème personne du pluriel au passé composé",
      options: ["J'ai pris", "Tu as pris", "Vous avez pris", "Ils ont pris"],
      correctAnswer: 2,
      explanation: "À la 2ème personne du pluriel, 'prendre' au passé composé se conjugue 'vous avez pris'",
      difficulty: 5,
      topic: "Conjugaison",
      learningObjective: "Conjuguer le verbe prendre au passé composé"
    },
    {
      id: 81,
      question: "Conjuguez le verbe 'réfléchir' à la 1ère personne du singulier au présent",
      options: ["Je réfléchis", "Tu réfléchis", "Il réfléchit", "Nous réfléchissons"],
      correctAnswer: 0,
      explanation: "À la 1ère personne du singulier, 'réfléchir' se conjugue 'je réfléchis'",
      difficulty: 4,
      topic: "Conjugaison",
      learningObjective: "Conjuguer les verbes du 2ème groupe au présent"
    },
    {
      id: 82,
      question: "Quel est le pluriel de 'bail' ?",
      options: ["Bails", "Baux", "Bales", "Bail"],
      correctAnswer: 1,
      explanation: "Les mots en -ail font leur pluriel en -aux : bail → baux",
      difficulty: 4,
      topic: "Pluriel",
      learningObjective: "Former le pluriel des noms en -ail"
    },
    {
      id: 83,
      question: "Identifiez la fonction de 'très' dans : 'Il est très intelligent'",
      options: ["Adverbe de degré", "Adverbe de manière", "Adverbe de temps", "Adverbe de lieu"],
      correctAnswer: 0,
      explanation: "'très' est un adverbe de degré qui modifie l'adjectif 'intelligent'",
      difficulty: 4,
      topic: "Syntaxe",
      learningObjective: "Identifier la fonction des adverbes"
    },
    {
      id: 84,
      question: "Quel est l'adverbe de manière de 'sincère' ?",
      options: ["Sincèrement", "Sincère", "Sincérer", "Sincérité"],
      correctAnswer: 0,
      explanation: "L'adverbe de manière se forme en ajoutant -ment à l'adjectif : sincère → sincèrement",
      difficulty: 4,
      topic: "Adverbes",
      learningObjective: "Former les adverbes de manière"
    },
    {
      id: 85,
      question: "Conjuguez 'voir' à la 3ème personne du pluriel au passé composé",
      options: ["J'ai vu", "Tu as vu", "Ils ont vu", "Nous avons vu"],
      correctAnswer: 2,
      explanation: "À la 3ème personne du pluriel, 'voir' au passé composé se conjugue 'ils ont vu'",
      difficulty: 5,
      topic: "Conjugaison",
      learningObjective: "Conjuguer le verbe voir au passé composé"
    },
    {
      id: 86,
      question: "Conjuguez le verbe 'agir' à la 2ème personne du singulier au présent",
      options: ["J'agis", "Tu agis", "Il agit", "Nous agissons"],
      correctAnswer: 1,
      explanation: "À la 2ème personne du singulier, 'agir' se conjugue 'tu agis'",
      difficulty: 4,
      topic: "Conjugaison",
      learningObjective: "Conjuguer les verbes du 2ème groupe au présent"
    },
    {
      id: 87,
      question: "Quel est le pluriel de 'travail' ?",
      options: ["Travails", "Travaux", "Travailes", "Travail"],
      correctAnswer: 1,
      explanation: "Les mots en -ail font leur pluriel en -aux : travail → travaux",
      difficulty: 4,
      topic: "Pluriel",
      learningObjective: "Former le pluriel des noms en -ail"
    },
    {
      id: 88,
      question: "Identifiez le complément d'agent dans : 'Le livre est lu par l'élève'",
      options: ["Le livre", "est lu", "par l'élève", "est lu par l'élève"],
      correctAnswer: 2,
      explanation: "'par l'élève' est le complément d'agent de la voix passive",
      difficulty: 4,
      topic: "Syntaxe",
      learningObjective: "Identifier le complément d'agent"
    },
    {
      id: 89,
      question: "Quel est l'adverbe de manière de 'naturel' ?",
      options: ["Naturellement", "Naturel", "Natureler", "Naturelité"],
      correctAnswer: 0,
      explanation: "L'adverbe de manière se forme en ajoutant -ment à l'adjectif : naturel → naturellement",
      difficulty: 4,
      topic: "Adverbes",
      learningObjective: "Former les adverbes de manière"
    },
    {
      id: 90,
      question: "Conjuguez 'devoir' à la 1ère personne du pluriel au passé composé",
      options: ["J'ai dû", "Tu as dû", "Nous avons dû", "Ils ont dû"],
      correctAnswer: 2,
      explanation: "À la 1ère personne du pluriel, 'devoir' au passé composé se conjugue 'nous avons dû'",
      difficulty: 5,
      topic: "Conjugaison",
      learningObjective: "Conjuguer le verbe devoir au passé composé"
    },
    {
      id: 91,
      question: "Conjuguez le verbe 'bâtir' à la 3ème personne du singulier au présent",
      options: ["Je bâtis", "Tu bâtis", "Il bâtit", "Nous bâtissons"],
      correctAnswer: 2,
      explanation: "À la 3ème personne du singulier, 'bâtir' se conjugue 'il bâtit'",
      difficulty: 4,
      topic: "Conjugaison",
      learningObjective: "Conjuguer les verbes du 2ème groupe au présent"
    },
    {
      id: 92,
      question: "Quel est le pluriel de 'vitrail' ?",
      options: ["Vitraux", "Vitrails", "Vitrailes", "Vitrail"],
      correctAnswer: 0,
      explanation: "Les mots en -ail font leur pluriel en -aux : vitrail → vitraux",
      difficulty: 4,
      topic: "Pluriel",
      learningObjective: "Former le pluriel des noms en -ail"
    },
    {
      id: 93,
      question: "Identifiez la proposition subordonnée dans : 'Je sais qu'il viendra'",
      options: ["Je sais", "qu'il viendra", "il viendra", "sais qu'il viendra"],
      correctAnswer: 1,
      explanation: "'qu'il viendra' est la proposition subordonnée introduite par 'que'",
      difficulty: 4,
      topic: "Syntaxe",
      learningObjective: "Identifier la proposition subordonnée"
    },
    {
      id: 94,
      question: "Quel est l'adverbe de manière de 'général' ?",
      options: ["Généralement", "Général", "Généraler", "Généralité"],
      correctAnswer: 0,
      explanation: "L'adverbe de manière se forme en ajoutant -ment à l'adjectif : général → généralement",
      difficulty: 4,
      topic: "Adverbes",
      learningObjective: "Former les adverbes de manière"
    },
    {
      id: 95,
      question: "Conjuguez 'pouvoir' à la 2ème personne du pluriel au passé composé",
      options: ["J'ai pu", "Tu as pu", "Vous avez pu", "Ils ont pu"],
      correctAnswer: 2,
      explanation: "À la 2ème personne du pluriel, 'pouvoir' au passé composé se conjugue 'vous avez pu'",
      difficulty: 5,
      topic: "Conjugaison",
      learningObjective: "Conjuguer le verbe pouvoir au passé composé"
    },
    {
      id: 96,
      question: "Conjuguez le verbe 'dormir' à la 1ère personne du singulier au présent",
      options: ["Je dors", "Tu dors", "Il dort", "Nous dormons"],
      correctAnswer: 0,
      explanation: "À la 1ère personne du singulier, 'dormir' se conjugue 'je dors'",
      difficulty: 4,
      topic: "Conjugaison",
      learningObjective: "Conjuguer les verbes du 3ème groupe au présent"
    },
    {
      id: 97,
      question: "Quel est le pluriel de 'corail' ?",
      options: ["Coraux", "Corails", "Corailes", "Corail"],
      correctAnswer: 0,
      explanation: "Les mots en -ail font leur pluriel en -aux : corail → coraux",
      difficulty: 4,
      topic: "Pluriel",
      learningObjective: "Former le pluriel des noms en -ail"
    },
    {
      id: 98,
      question: "Identifiez la fonction de 'beaucoup' dans : 'Il travaille beaucoup'",
      options: ["Adverbe de quantité", "Adverbe de manière", "Adverbe de temps", "Adverbe de lieu"],
      correctAnswer: 0,
      explanation: "'beaucoup' est un adverbe de quantité qui modifie le verbe 'travaille'",
      difficulty: 4,
      topic: "Syntaxe",
      learningObjective: "Identifier la fonction des adverbes"
    },
    {
      id: 99,
      question: "Quel est l'adverbe de manière de 'actuel' ?",
      options: ["Actuellement", "Actuel", "Actueler", "Actualité"],
      correctAnswer: 0,
      explanation: "L'adverbe de manière se forme en ajoutant -ment à l'adjectif : actuel → actuellement",
      difficulty: 4,
      topic: "Adverbes",
      learningObjective: "Former les adverbes de manière"
    },
    {
      id: 100,
      question: "Conjuguez 'savoir' à la 3ème personne du pluriel au passé composé",
      options: ["J'ai su", "Tu as su", "Ils ont su", "Nous avons su"],
      correctAnswer: 2,
      explanation: "À la 3ème personne du pluriel, 'savoir' au passé composé se conjugue 'ils ont su'",
      difficulty: 5,
      topic: "Conjugaison",
      learningObjective: "Conjuguer le verbe savoir au passé composé"
    }
  ],
  
  "Avancé (7-9)": [
    {
      id: 56,
      question: "Conjuguez le verbe 'finir' au subjonctif présent à la 1ère personne du singulier",
      options: ["Je finisse", "Je finis", "Je finirais", "Je finirai"],
      correctAnswer: 0,
      explanation: "Au subjonctif présent, 'finir' se conjugue 'je finisse'",
      difficulty: 7,
      topic: "Subjonctif",
      learningObjective: "Conjuguer les verbes au subjonctif présent"
    },
    {
      id: 57,
      question: "Transformez la phrase active en passive : 'Le professeur corrige les copies'",
      options: ["Les copies sont corrigées par le professeur", "Le professeur est corrigé par les copies", "Les copies corrigent le professeur", "Le professeur corrige les copies"],
      correctAnswer: 0,
      explanation: "La voix passive transforme le complément d'objet en sujet : 'Les copies sont corrigées par le professeur'",
      difficulty: 7,
      topic: "Voix passive",
      learningObjective: "Transformer une phrase active en passive"
    },
    {
      id: 58,
      question: "Identifiez la figure de style dans : 'Le soleil souriait dans le ciel'",
      options: ["Métaphore", "Personnification", "Comparaison", "Hyperbole"],
      correctAnswer: 1,
      explanation: "La personnification attribue des qualités humaines à des objets : le soleil 'sourit'",
      difficulty: 8,
      topic: "Figures de style",
      learningObjective: "Reconnaître la personnification"
    },
    {
      id: 59,
      question: "Conjuguez 'être' au conditionnel présent à la 2ème personne du pluriel",
      options: ["Vous êtes", "Vous seriez", "Vous étiez", "Vous serez"],
      correctAnswer: 1,
      explanation: "Au conditionnel présent, 'être' se conjugue 'vous seriez'",
      difficulty: 8,
      topic: "Conditionnel",
      learningObjective: "Conjuguer le verbe être au conditionnel présent"
    },
    {
      id: 60,
      question: "Quel est le discours rapporté de : 'Il dit : \"Je viens demain\"' ?",
      options: ["Il dit qu'il vient demain", "Il dit qu'il viendra demain", "Il dit qu'il venait demain", "Il dit qu'il vienne demain"],
      correctAnswer: 1,
      explanation: "Le discours indirect transforme le présent 'viens' en futur 'viendra'",
      difficulty: 8,
      topic: "Discours rapporté",
      learningObjective: "Transformer le discours direct en indirect"
    },
    {
      id: 101,
      question: "Conjuguez le verbe 'parler' au subjonctif présent à la 3ème personne du singulier",
      options: ["Je parle", "Tu parles", "Il parle", "Qu'il parle"],
      correctAnswer: 3,
      explanation: "Au subjonctif présent, 'parler' se conjugue 'qu'il parle'",
      difficulty: 7,
      topic: "Subjonctif",
      learningObjective: "Conjuguer les verbes du 1er groupe au subjonctif présent"
    },
    {
      id: 102,
      question: "Transformez la phrase active en passive : 'Les élèves lisent le livre'",
      options: ["Le livre est lu par les élèves", "Les élèves sont lus par le livre", "Le livre lit les élèves", "Les élèves lisent le livre"],
      correctAnswer: 0,
      explanation: "La voix passive transforme le complément d'objet en sujet : 'Le livre est lu par les élèves'",
      difficulty: 7,
      topic: "Voix passive",
      learningObjective: "Transformer une phrase active en passive"
    },
    {
      id: 103,
      question: "Identifiez la figure de style dans : 'Cette femme est un vrai lion'",
      options: ["Comparaison", "Métaphore", "Métonymie", "Synecdoque"],
      correctAnswer: 1,
      explanation: "La métaphore établit une comparaison sans mot de liaison : 'cette femme est un lion'",
      difficulty: 8,
      topic: "Figures de style",
      learningObjective: "Distinguer la métaphore de la comparaison"
    },
    {
      id: 104,
      question: "Conjuguez 'avoir' au conditionnel présent à la 1ère personne du singulier",
      options: ["J'ai", "Tu as", "J'aurais", "J'aurai"],
      correctAnswer: 2,
      explanation: "Au conditionnel présent, 'avoir' se conjugue 'j'aurais'",
      difficulty: 8,
      topic: "Conditionnel",
      learningObjective: "Conjuguer le verbe avoir au conditionnel présent"
    },
    {
      id: 105,
      question: "Quel est le discours rapporté de : 'Elle dit : \"Je vais au cinéma\"' ?",
      options: ["Elle dit qu'elle va au cinéma", "Elle dit qu'elle ira au cinéma", "Elle dit qu'elle allait au cinéma", "Elle dit qu'elle aille au cinéma"],
      correctAnswer: 1,
      explanation: "Le discours indirect transforme le présent 'vais' en futur 'ira'",
      difficulty: 8,
      topic: "Discours rapporté",
      learningObjective: "Transformer le discours direct en indirect"
    },
    {
      id: 106,
      question: "Conjuguez le verbe 'choisir' au subjonctif présent à la 2ème personne du singulier",
      options: ["Je choisisse", "Tu choisisses", "Il choisisse", "Nous choisissions"],
      correctAnswer: 1,
      explanation: "Au subjonctif présent, 'choisir' se conjugue 'tu choisisses'",
      difficulty: 7,
      topic: "Subjonctif",
      learningObjective: "Conjuguer les verbes du 2ème groupe au subjonctif présent"
    },
    {
      id: 107,
      question: "Transformez la phrase active en passive : 'Le cuisinier prépare le repas'",
      options: ["Le repas est préparé par le cuisinier", "Le cuisinier est préparé par le repas", "Le repas prépare le cuisinier", "Le cuisinier prépare le repas"],
      correctAnswer: 0,
      explanation: "La voix passive transforme le complément d'objet en sujet : 'Le repas est préparé par le cuisinier'",
      difficulty: 7,
      topic: "Voix passive",
      learningObjective: "Transformer une phrase active en passive"
    },
    {
      id: 108,
      question: "Identifiez la figure de style dans : 'Il pleut des cordes'",
      options: ["Comparaison", "Métaphore", "Hyperbole", "Litote"],
      correctAnswer: 1,
      explanation: "La métaphore établit une comparaison sans mot de liaison : 'il pleut des cordes'",
      difficulty: 8,
      topic: "Figures de style",
      learningObjective: "Reconnaître la métaphore"
    },
    {
      id: 109,
      question: "Conjuguez 'faire' au conditionnel présent à la 3ème personne du singulier",
      options: ["Il fait", "Il ferait", "Il fera", "Il faisait"],
      correctAnswer: 1,
      explanation: "Au conditionnel présent, 'faire' se conjugue 'il ferait'",
      difficulty: 8,
      topic: "Conditionnel",
      learningObjective: "Conjuguer le verbe faire au conditionnel présent"
    },
    {
      id: 110,
      question: "Quel est le discours rapporté de : 'Il dit : \"Je travaille ici\"' ?",
      options: ["Il dit qu'il travaille ici", "Il dit qu'il travaillera ici", "Il dit qu'il travaillait ici", "Il dit qu'il travaille ici"],
      correctAnswer: 2,
      explanation: "Le discours indirect transforme le présent 'travaille' en imparfait 'travaillait'",
      difficulty: 8,
      topic: "Discours rapporté",
      learningObjective: "Transformer le discours direct en indirect"
    },
    {
      id: 111,
      question: "Conjuguez le verbe 'prendre' au subjonctif présent à la 1ère personne du pluriel",
      options: ["Je prenne", "Tu prennes", "Nous prenions", "Ils prennent"],
      correctAnswer: 2,
      explanation: "Au subjonctif présent, 'prendre' se conjugue 'nous prenions'",
      difficulty: 7,
      topic: "Subjonctif",
      learningObjective: "Conjuguer les verbes du 3ème groupe au subjonctif présent"
    },
    {
      id: 112,
      question: "Transformez la phrase active en passive : 'Les artistes créent des œuvres'",
      options: ["Des œuvres sont créées par les artistes", "Les artistes sont créés par des œuvres", "Des œuvres créent les artistes", "Les artistes créent des œuvres"],
      correctAnswer: 0,
      explanation: "La voix passive transforme le complément d'objet en sujet : 'Des œuvres sont créées par les artistes'",
      difficulty: 7,
      topic: "Voix passive",
      learningObjective: "Transformer une phrase active en passive"
    },
    {
      id: 113,
      question: "Identifiez la figure de style dans : 'Il est fort comme un taureau'",
      options: ["Métaphore", "Personnification", "Comparaison", "Hyperbole"],
      correctAnswer: 2,
      explanation: "La comparaison utilise un mot de liaison : 'comme un taureau'",
      difficulty: 8,
      topic: "Figures de style",
      learningObjective: "Distinguer la comparaison de la métaphore"
    },
    {
      id: 114,
      question: "Conjuguez 'aller' au conditionnel présent à la 2ème personne du singulier",
      options: ["Tu vas", "Tu irais", "Tu iras", "Tu allais"],
      correctAnswer: 1,
      explanation: "Au conditionnel présent, 'aller' se conjugue 'tu irais'",
      difficulty: 8,
      topic: "Conditionnel",
      learningObjective: "Conjuguer le verbe aller au conditionnel présent"
    },
    {
      id: 115,
      question: "Quel est le discours rapporté de : 'Elle dit : \"Je suis fatiguée\"' ?",
      options: ["Elle dit qu'elle est fatiguée", "Elle dit qu'elle sera fatiguée", "Elle dit qu'elle était fatiguée", "Elle dit qu'elle soit fatiguée"],
      correctAnswer: 2,
      explanation: "Le discours indirect transforme le présent 'suis' en imparfait 'était'",
      difficulty: 8,
      topic: "Discours rapporté",
      learningObjective: "Transformer le discours direct en indirect"
    },
    {
      id: 116,
      question: "Conjuguez le verbe 'vendre' au subjonctif présent à la 3ème personne du pluriel",
      options: ["Je vende", "Tu vendes", "Ils vendent", "Qu'ils vendent"],
      correctAnswer: 3,
      explanation: "Au subjonctif présent, 'vendre' se conjugue 'qu'ils vendent'",
      difficulty: 7,
      topic: "Subjonctif",
      learningObjective: "Conjuguer les verbes du 3ème groupe au subjonctif présent"
    },
    {
      id: 117,
      question: "Transformez la phrase active en passive : 'Le mécanicien répare la voiture'",
      options: ["La voiture est réparée par le mécanicien", "Le mécanicien est réparé par la voiture", "La voiture répare le mécanicien", "Le mécanicien répare la voiture"],
      correctAnswer: 0,
      explanation: "La voix passive transforme le complément d'objet en sujet : 'La voiture est réparée par le mécanicien'",
      difficulty: 7,
      topic: "Voix passive",
      learningObjective: "Transformer une phrase active en passive"
    },
    {
      id: 118,
      question: "Identifiez la figure de style dans : 'Il a un appétit d'ogre'",
      options: ["Comparaison", "Métaphore", "Métonymie", "Synecdoque"],
      correctAnswer: 1,
      explanation: "La métaphore établit une comparaison sans mot de liaison : 'appétit d'ogre'",
      difficulty: 8,
      topic: "Figures de style",
      learningObjective: "Reconnaître la métaphore"
    },
    {
      id: 119,
      question: "Conjuguez 'venir' au conditionnel présent à la 1ère personne du pluriel",
      options: ["Nous venons", "Nous viendrions", "Nous viendrons", "Nous venions"],
      correctAnswer: 1,
      explanation: "Au conditionnel présent, 'venir' se conjugue 'nous viendrions'",
      difficulty: 8,
      topic: "Conditionnel",
      learningObjective: "Conjuguer le verbe venir au conditionnel présent"
    },
    {
      id: 120,
      question: "Quel est le discours rapporté de : 'Il dit : \"Je comprends maintenant\"' ?",
      options: ["Il dit qu'il comprend maintenant", "Il dit qu'il comprendra maintenant", "Il dit qu'il comprenait maintenant", "Il dit qu'il comprenne maintenant"],
      correctAnswer: 2,
      explanation: "Le discours indirect transforme le présent 'comprends' en imparfait 'comprenait'",
      difficulty: 8,
      topic: "Discours rapporté",
      learningObjective: "Transformer le discours direct en indirect"
    },
    {
      id: 121,
      question: "Conjuguez le verbe 'réussir' au subjonctif présent à la 2ème personne du pluriel",
      options: ["Je réussisse", "Tu réussisses", "Vous réussissiez", "Ils réussissent"],
      correctAnswer: 2,
      explanation: "Au subjonctif présent, 'réussir' se conjugue 'vous réussissiez'",
      difficulty: 7,
      topic: "Subjonctif",
      learningObjective: "Conjuguer les verbes du 2ème groupe au subjonctif présent"
    },
    {
      id: 122,
      question: "Transformez la phrase active en passive : 'Les architectes dessinent les plans'",
      options: ["Les plans sont dessinés par les architectes", "Les architectes sont dessinés par les plans", "Les plans dessinent les architectes", "Les architectes dessinent les plans"],
      correctAnswer: 0,
      explanation: "La voix passive transforme le complément d'objet en sujet : 'Les plans sont dessinés par les architectes'",
      difficulty: 7,
      topic: "Voix passive",
      learningObjective: "Transformer une phrase active en passive"
    },
    {
      id: 123,
      question: "Identifiez la figure de style dans : 'Le temps s'envole'",
      options: ["Métaphore", "Personnification", "Comparaison", "Hyperbole"],
      correctAnswer: 1,
      explanation: "La personnification attribue des qualités humaines à des objets : le temps 's'envole'",
      difficulty: 8,
      topic: "Figures de style",
      learningObjective: "Reconnaître la personnification"
    },
    {
      id: 124,
      question: "Conjuguez 'devoir' au conditionnel présent à la 3ème personne du pluriel",
      options: ["Ils doivent", "Ils devraient", "Ils devront", "Ils devaient"],
      correctAnswer: 1,
      explanation: "Au conditionnel présent, 'devoir' se conjugue 'ils devraient'",
      difficulty: 8,
      topic: "Conditionnel",
      learningObjective: "Conjuguer le verbe devoir au conditionnel présent"
    },
    {
      id: 125,
      question: "Quel est le discours rapporté de : 'Elle dit : \"Je lis un roman\"' ?",
      options: ["Elle dit qu'elle lit un roman", "Elle dit qu'elle lira un roman", "Elle dit qu'elle lisait un roman", "Elle dit qu'elle lise un roman"],
      correctAnswer: 2,
      explanation: "Le discours indirect transforme le présent 'lis' en imparfait 'lisait'",
      difficulty: 8,
      topic: "Discours rapporté",
      learningObjective: "Transformer le discours direct en indirect"
    },
    {
      id: 126,
      question: "Conjuguez le verbe 'dormir' au subjonctif présent à la 1ère personne du singulier",
      options: ["Je dors", "Tu dormes", "Je dorme", "Nous dormions"],
      correctAnswer: 2,
      explanation: "Au subjonctif présent, 'dormir' se conjugue 'je dorme'",
      difficulty: 7,
      topic: "Subjonctif",
      learningObjective: "Conjuguer les verbes du 3ème groupe au subjonctif présent"
    },
    {
      id: 127,
      question: "Transformez la phrase active en passive : 'Le jardinier arrose les fleurs'",
      options: ["Les fleurs sont arrosées par le jardinier", "Le jardinier est arrosé par les fleurs", "Les fleurs arrosent le jardinier", "Le jardinier arrose les fleurs"],
      correctAnswer: 0,
      explanation: "La voix passive transforme le complément d'objet en sujet : 'Les fleurs sont arrosées par le jardinier'",
      difficulty: 7,
      topic: "Voix passive",
      learningObjective: "Transformer une phrase active en passive"
    },
    {
      id: 128,
      question: "Identifiez la figure de style dans : 'Il court comme un lièvre'",
      options: ["Métaphore", "Personnification", "Comparaison", "Hyperbole"],
      correctAnswer: 2,
      explanation: "La comparaison utilise un mot de liaison : 'comme un lièvre'",
      difficulty: 8,
      topic: "Figures de style",
      learningObjective: "Distinguer la comparaison de la métaphore"
    },
    {
      id: 129,
      question: "Conjuguez 'pouvoir' au conditionnel présent à la 2ème personne du pluriel",
      options: ["Vous pouvez", "Vous pourriez", "Vous pourrez", "Vous pouviez"],
      correctAnswer: 1,
      explanation: "Au conditionnel présent, 'pouvoir' se conjugue 'vous pourriez'",
      difficulty: 8,
      topic: "Conditionnel",
      learningObjective: "Conjuguer le verbe pouvoir au conditionnel présent"
    },
    {
      id: 130,
      question: "Quel est le discours rapporté de : 'Il dit : \"Je mange une pomme\"' ?",
      options: ["Il dit qu'il mange une pomme", "Il dit qu'il mangera une pomme", "Il dit qu'il mangeait une pomme", "Il dit qu'il mange une pomme"],
      correctAnswer: 2,
      explanation: "Le discours indirect transforme le présent 'mange' en imparfait 'mangeait'",
      difficulty: 8,
      topic: "Discours rapporté",
      learningObjective: "Transformer le discours direct en indirect"
    },
    {
      id: 131,
      question: "Conjuguez le verbe 'agir' au subjonctif présent à la 3ème personne du singulier",
      options: ["Je agisse", "Tu agisses", "Il agisse", "Qu'il agisse"],
      correctAnswer: 3,
      explanation: "Au subjonctif présent, 'agir' se conjugue 'qu'il agisse'",
      difficulty: 7,
      topic: "Subjonctif",
      learningObjective: "Conjuguer les verbes du 2ème groupe au subjonctif présent"
    },
    {
      id: 132,
      question: "Transformez la phrase active en passive : 'Les musiciens jouent une symphonie'",
      options: ["Une symphonie est jouée par les musiciens", "Les musiciens sont joués par une symphonie", "Une symphonie joue les musiciens", "Les musiciens jouent une symphonie"],
      correctAnswer: 0,
      explanation: "La voix passive transforme le complément d'objet en sujet : 'Une symphonie est jouée par les musiciens'",
      difficulty: 7,
      topic: "Voix passive",
      learningObjective: "Transformer une phrase active en passive"
    },
    {
      id: 133,
      question: "Identifiez la figure de style dans : 'La mer rugit'",
      options: ["Métaphore", "Personnification", "Comparaison", "Hyperbole"],
      correctAnswer: 1,
      explanation: "La personnification attribue des qualités humaines à des objets : la mer 'rugit'",
      difficulty: 8,
      topic: "Figures de style",
      learningObjective: "Reconnaître la personnification"
    },
    {
      id: 134,
      question: "Conjuguez 'savoir' au conditionnel présent à la 1ère personne du singulier",
      options: ["Je sais", "Tu sais", "Je saurais", "Je saurai"],
      correctAnswer: 2,
      explanation: "Au conditionnel présent, 'savoir' se conjugue 'je saurais'",
      difficulty: 8,
      topic: "Conditionnel",
      learningObjective: "Conjuguer le verbe savoir au conditionnel présent"
    },
    {
      id: 135,
      question: "Quel est le discours rapporté de : 'Elle dit : \"Je chante une chanson\"' ?",
      options: ["Elle dit qu'elle chante une chanson", "Elle dit qu'elle chantera une chanson", "Elle dit qu'elle chantait une chanson", "Elle dit qu'elle chante une chanson"],
      correctAnswer: 2,
      explanation: "Le discours indirect transforme le présent 'chante' en imparfait 'chantait'",
      difficulty: 8,
      topic: "Discours rapporté",
      learningObjective: "Transformer le discours direct en indirect"
    },
    {
      id: 136,
      question: "Conjuguez le verbe 'bâtir' au subjonctif présent à la 2ème personne du singulier",
      options: ["Je bâtisse", "Tu bâtisses", "Il bâtisse", "Nous bâtissions"],
      correctAnswer: 1,
      explanation: "Au subjonctif présent, 'bâtir' se conjugue 'tu bâtisses'",
      difficulty: 7,
      topic: "Subjonctif",
      learningObjective: "Conjuguer les verbes du 2ème groupe au subjonctif présent"
    },
    {
      id: 137,
      question: "Transformez la phrase active en passive : 'Le photographe prend des photos'",
      options: ["Des photos sont prises par le photographe", "Le photographe est pris par des photos", "Des photos prennent le photographe", "Le photographe prend des photos"],
      correctAnswer: 0,
      explanation: "La voix passive transforme le complément d'objet en sujet : 'Des photos sont prises par le photographe'",
      difficulty: 7,
      topic: "Voix passive",
      learningObjective: "Transformer une phrase active en passive"
    },
    {
      id: 138,
      question: "Identifiez la figure de style dans : 'Il a une mémoire d'éléphant'",
      options: ["Comparaison", "Métaphore", "Métonymie", "Synecdoque"],
      correctAnswer: 1,
      explanation: "La métaphore établit une comparaison sans mot de liaison : 'mémoire d'éléphant'",
      difficulty: 8,
      topic: "Figures de style",
      learningObjective: "Reconnaître la métaphore"
    },
    {
      id: 139,
      question: "Conjuguez 'voir' au conditionnel présent à la 3ème personne du pluriel",
      options: ["Ils voient", "Ils verraient", "Ils verront", "Ils voyaient"],
      correctAnswer: 1,
      explanation: "Au conditionnel présent, 'voir' se conjugue 'ils verraient'",
      difficulty: 8,
      topic: "Conditionnel",
      learningObjective: "Conjuguer le verbe voir au conditionnel présent"
    },
    {
      id: 140,
      question: "Quel est le discours rapporté de : 'Il dit : \"Je voyage en France\"' ?",
      options: ["Il dit qu'il voyage en France", "Il dit qu'il voyagera en France", "Il dit qu'il voyageait en France", "Il dit qu'il voyage en France"],
      correctAnswer: 2,
      explanation: "Le discours indirect transforme le présent 'voyage' en imparfait 'voyageait'",
      difficulty: 8,
      topic: "Discours rapporté",
      learningObjective: "Transformer le discours direct en indirect"
    },
    {
      id: 141,
      question: "Conjuguez le verbe 'grandir' au subjonctif présent à la 1ère personne du pluriel",
      options: ["Je grandisse", "Tu grandisses", "Nous grandissions", "Ils grandissent"],
      correctAnswer: 2,
      explanation: "Au subjonctif présent, 'grandir' se conjugue 'nous grandissions'",
      difficulty: 7,
      topic: "Subjonctif",
      learningObjective: "Conjuguer les verbes du 2ème groupe au subjonctif présent"
    },
    {
      id: 142,
      question: "Transformez la phrase active en passive : 'Les écrivains écrivent des livres'",
      options: ["Des livres sont écrits par les écrivains", "Les écrivains sont écrits par des livres", "Des livres écrivent les écrivains", "Les écrivains écrivent des livres"],
      correctAnswer: 0,
      explanation: "La voix passive transforme le complément d'objet en sujet : 'Des livres sont écrits par les écrivains'",
      difficulty: 7,
      topic: "Voix passive",
      learningObjective: "Transformer une phrase active en passive"
    },
    {
      id: 143,
      question: "Identifiez la figure de style dans : 'Le vent murmure'",
      options: ["Métaphore", "Personnification", "Comparaison", "Hyperbole"],
      correctAnswer: 1,
      explanation: "La personnification attribue des qualités humaines à des objets : le vent 'murmure'",
      difficulty: 8,
      topic: "Figures de style",
      learningObjective: "Reconnaître la personnification"
    },
    {
      id: 144,
      question: "Conjuguez 'prendre' au conditionnel présent à la 2ème personne du pluriel",
      options: ["Vous prenez", "Vous prendriez", "Vous prendrez", "Vous preniez"],
      correctAnswer: 1,
      explanation: "Au conditionnel présent, 'prendre' se conjugue 'vous prendriez'",
      difficulty: 8,
      topic: "Conditionnel",
      learningObjective: "Conjuguer le verbe prendre au conditionnel présent"
    },
    {
      id: 145,
      question: "Quel est le discours rapporté de : 'Elle dit : \"Je danse le tango\"' ?",
      options: ["Elle dit qu'elle danse le tango", "Elle dit qu'elle dansera le tango", "Elle dit qu'elle dansait le tango", "Elle dit qu'elle danse le tango"],
      correctAnswer: 2,
      explanation: "Le discours indirect transforme le présent 'danse' en imparfait 'dansait'",
      difficulty: 8,
      topic: "Discours rapporté",
      learningObjective: "Transformer le discours direct en indirect"
    },
    {
      id: 146,
      question: "Conjuguez le verbe 'réfléchir' au subjonctif présent à la 3ème personne du singulier",
      options: ["Je réfléchisse", "Tu réfléchisses", "Il réfléchisse", "Qu'il réfléchisse"],
      correctAnswer: 3,
      explanation: "Au subjonctif présent, 'réfléchir' se conjugue 'qu'il réfléchisse'",
      difficulty: 7,
      topic: "Subjonctif",
      learningObjective: "Conjuguer les verbes du 2ème groupe au subjonctif présent"
    },
    {
      id: 147,
      question: "Transformez la phrase active en passive : 'Le peintre crée des tableaux'",
      options: ["Des tableaux sont créés par le peintre", "Le peintre est créé par des tableaux", "Des tableaux créent le peintre", "Le peintre crée des tableaux"],
      correctAnswer: 0,
      explanation: "La voix passive transforme le complément d'objet en sujet : 'Des tableaux sont créés par le peintre'",
      difficulty: 7,
      topic: "Voix passive",
      learningObjective: "Transformer une phrase active en passive"
    },
    {
      id: 148,
      question: "Identifiez la figure de style dans : 'Il est bavard comme une pie'",
      options: ["Métaphore", "Personnification", "Comparaison", "Hyperbole"],
      correctAnswer: 2,
      explanation: "La comparaison utilise un mot de liaison : 'comme une pie'",
      difficulty: 8,
      topic: "Figures de style",
      learningObjective: "Distinguer la comparaison de la métaphore"
    },
    {
      id: 149,
      question: "Conjuguez 'faire' au conditionnel présent à la 1ère personne du pluriel",
      options: ["Nous faisons", "Nous ferions", "Nous ferons", "Nous faisions"],
      correctAnswer: 1,
      explanation: "Au conditionnel présent, 'faire' se conjugue 'nous ferions'",
      difficulty: 8,
      topic: "Conditionnel",
      learningObjective: "Conjuguer le verbe faire au conditionnel présent"
    },
    {
      id: 150,
      question: "Quel est le discours rapporté de : 'Il dit : \"Je nage dans la piscine\"' ?",
      options: ["Il dit qu'il nage dans la piscine", "Il dit qu'il nagera dans la piscine", "Il dit qu'il nageait dans la piscine", "Il dit qu'il nage dans la piscine"],
      correctAnswer: 2,
      explanation: "Le discours indirect transforme le présent 'nage' en imparfait 'nageait'",
      difficulty: 8,
      topic: "Discours rapporté",
      learningObjective: "Transformer le discours direct en indirect"
    }
  ],
  
  "Expert (10-12)": [
    {
      id: 61,
      question: "Conjuguez le verbe 'prendre' au plus-que-parfait à la 3ème personne du singulier",
      options: ["Il avait pris", "Il a pris", "Il prendra", "Il prenait"],
      correctAnswer: 0,
      explanation: "Au plus-que-parfait, 'prendre' se conjugue 'il avait pris' (avoir à l'imparfait + participe passé)",
      difficulty: 10,
      topic: "Plus-que-parfait",
      learningObjective: "Conjuguer les verbes au plus-que-parfait"
    },
    {
      id: 62,
      question: "Identifiez la figure de style dans : 'Cette femme est un vrai lion'",
      options: ["Comparaison", "Métaphore", "Métonymie", "Synecdoque"],
      correctAnswer: 1,
      explanation: "La métaphore établit une comparaison sans mot de liaison : 'cette femme est un lion'",
      difficulty: 10,
      topic: "Figures de style",
      learningObjective: "Distinguer la métaphore de la comparaison"
    },
    {
      id: 63,
      question: "Analysez la structure de la phrase : 'L'homme que j'ai rencontré hier est mon professeur'",
      options: ["Phrase simple", "Phrase complexe avec relative", "Phrase complexe avec conjonctive", "Phrase complexe avec participiale"],
      correctAnswer: 1,
      explanation: "C'est une phrase complexe avec une proposition relative introduite par 'que'",
      difficulty: 11,
      topic: "Analyse syntaxique",
      learningObjective: "Analyser la structure des phrases complexes"
    },
    {
      id: 64,
      question: "Conjuguez 'faire' au subjonctif imparfait à la 1ère personne du pluriel",
      options: ["Nous fassions", "Nous faisons", "Nous ferions", "Nous fîmes"],
      correctAnswer: 0,
      explanation: "Au subjonctif imparfait, 'faire' se conjugue 'nous fassions'",
      difficulty: 11,
      topic: "Subjonctif imparfait",
      learningObjective: "Conjuguer les verbes au subjonctif imparfait"
    },
    {
      id: 65,
      question: "Quel est le registre de langue dans : 'Je vous prie de bien vouloir m'excuser' ?",
      options: ["Familier", "Courant", "Soutenu", "Populaire"],
      correctAnswer: 2,
      explanation: "C'est un registre soutenu avec des formules de politesse élaborées",
      difficulty: 12,
      topic: "Registres de langue",
      learningObjective: "Identifier les registres de langue"
    },
    {
      id: 151,
      question: "Conjuguez le verbe 'être' au plus-que-parfait à la 1ère personne du singulier",
      options: ["J'avais été", "J'ai été", "J'étais", "J'aurais été"],
      correctAnswer: 0,
      explanation: "Au plus-que-parfait, 'être' se conjugue 'j'avais été' (avoir à l'imparfait + participe passé)",
      difficulty: 10,
      topic: "Plus-que-parfait",
      learningObjective: "Conjuguer le verbe être au plus-que-parfait"
    },
    {
      id: 152,
      question: "Identifiez la figure de style dans : 'Il a un cœur de pierre'",
      options: ["Comparaison", "Métaphore", "Métonymie", "Synecdoque"],
      correctAnswer: 1,
      explanation: "La métaphore établit une comparaison sans mot de liaison : 'cœur de pierre'",
      difficulty: 10,
      topic: "Figures de style",
      learningObjective: "Reconnaître la métaphore"
    },
    {
      id: 153,
      question: "Analysez la structure de la phrase : 'Quand il pleut, je reste à la maison'",
      options: ["Phrase simple", "Phrase complexe avec relative", "Phrase complexe avec conjonctive", "Phrase complexe avec participiale"],
      correctAnswer: 2,
      explanation: "C'est une phrase complexe avec une proposition conjonctive introduite par 'quand'",
      difficulty: 11,
      topic: "Analyse syntaxique",
      learningObjective: "Analyser la structure des phrases complexes"
    },
    {
      id: 154,
      question: "Conjuguez 'avoir' au subjonctif imparfait à la 2ème personne du singulier",
      options: ["Tu aies", "Tu avais", "Tu aurais", "Tu eusses"],
      correctAnswer: 3,
      explanation: "Au subjonctif imparfait, 'avoir' se conjugue 'tu eusses'",
      difficulty: 11,
      topic: "Subjonctif imparfait",
      learningObjective: "Conjuguer le verbe avoir au subjonctif imparfait"
    },
    {
      id: 155,
      question: "Quel est le registre de langue dans : 'Salut, ça va ?' ?",
      options: ["Familier", "Courant", "Soutenu", "Populaire"],
      correctAnswer: 0,
      explanation: "C'est un registre familier avec des expressions informelles",
      difficulty: 12,
      topic: "Registres de langue",
      learningObjective: "Identifier les registres de langue"
    },
    {
      id: 156,
      question: "Conjuguez le verbe 'aller' au plus-que-parfait à la 2ème personne du pluriel",
      options: ["Vous aviez été", "Vous étiez allés", "Vous aviez allé", "Vous étiez allé"],
      correctAnswer: 1,
      explanation: "Au plus-que-parfait, 'aller' se conjugue 'vous étiez allés' (être à l'imparfait + participe passé)",
      difficulty: 10,
      topic: "Plus-que-parfait",
      learningObjective: "Conjuguer le verbe aller au plus-que-parfait"
    },
    {
      id: 157,
      question: "Identifiez la figure de style dans : 'Il est rusé comme un renard'",
      options: ["Métaphore", "Personnification", "Comparaison", "Hyperbole"],
      correctAnswer: 2,
      explanation: "La comparaison utilise un mot de liaison : 'comme un renard'",
      difficulty: 10,
      topic: "Figures de style",
      learningObjective: "Distinguer la comparaison de la métaphore"
    },
    {
      id: 158,
      question: "Analysez la structure de la phrase : 'Le livre que j'ai lu était passionnant'",
      options: ["Phrase simple", "Phrase complexe avec relative", "Phrase complexe avec conjonctive", "Phrase complexe avec participiale"],
      correctAnswer: 1,
      explanation: "C'est une phrase complexe avec une proposition relative introduite par 'que'",
      difficulty: 11,
      topic: "Analyse syntaxique",
      learningObjective: "Analyser la structure des phrases complexes"
    },
    {
      id: 159,
      question: "Conjuguez 'faire' au subjonctif imparfait à la 3ème personne du singulier",
      options: ["Il fasse", "Il faisait", "Il fît", "Il ferait"],
      correctAnswer: 2,
      explanation: "Au subjonctif imparfait, 'faire' se conjugue 'il fît'",
      difficulty: 11,
      topic: "Subjonctif imparfait",
      learningObjective: "Conjuguer le verbe faire au subjonctif imparfait"
    },
    {
      id: 160,
      question: "Quel est le registre de langue dans : 'Voulez-vous bien me passer le sel ?' ?",
      options: ["Familier", "Courant", "Soutenu", "Populaire"],
      correctAnswer: 2,
      explanation: "C'est un registre soutenu avec des formules de politesse",
      difficulty: 12,
      topic: "Registres de langue",
      learningObjective: "Identifier les registres de langue"
    },
    {
      id: 161,
      question: "Conjuguez le verbe 'venir' au plus-que-parfait à la 1ère personne du pluriel",
      options: ["Nous avions été", "Nous étions venus", "Nous avions venu", "Nous étions venu"],
      correctAnswer: 1,
      explanation: "Au plus-que-parfait, 'venir' se conjugue 'nous étions venus' (être à l'imparfait + participe passé)",
      difficulty: 10,
      topic: "Plus-que-parfait",
      learningObjective: "Conjuguer le verbe venir au plus-que-parfait"
    },
    {
      id: 162,
      question: "Identifiez la figure de style dans : 'Il a une patience d'ange'",
      options: ["Comparaison", "Métaphore", "Métonymie", "Synecdoque"],
      correctAnswer: 1,
      explanation: "La métaphore établit une comparaison sans mot de liaison : 'patience d'ange'",
      difficulty: 10,
      topic: "Figures de style",
      learningObjective: "Reconnaître la métaphore"
    },
    {
      id: 163,
      question: "Analysez la structure de la phrase : 'Si tu viens, nous irons au cinéma'",
      options: ["Phrase simple", "Phrase complexe avec relative", "Phrase complexe avec conjonctive", "Phrase complexe avec participiale"],
      correctAnswer: 2,
      explanation: "C'est une phrase complexe avec une proposition conjonctive introduite par 'si'",
      difficulty: 11,
      topic: "Analyse syntaxique",
      learningObjective: "Analyser la structure des phrases complexes"
    },
    {
      id: 164,
      question: "Conjuguez 'être' au subjonctif imparfait à la 1ère personne du singulier",
      options: ["Je sois", "J'étais", "Je fusse", "Je serais"],
      correctAnswer: 2,
      explanation: "Au subjonctif imparfait, 'être' se conjugue 'je fusse'",
      difficulty: 11,
      topic: "Subjonctif imparfait",
      learningObjective: "Conjuguer le verbe être au subjonctif imparfait"
    },
    {
      id: 165,
      question: "Quel est le registre de langue dans : 'T'as pas vu mes clés ?' ?",
      options: ["Familier", "Courant", "Soutenu", "Populaire"],
      correctAnswer: 0,
      explanation: "C'est un registre familier avec des contractions et des expressions informelles",
      difficulty: 12,
      topic: "Registres de langue",
      learningObjective: "Identifier les registres de langue"
    },
    {
      id: 166,
      question: "Conjuguez le verbe 'prendre' au plus-que-parfait à la 2ème personne du singulier",
      options: ["Tu avais pris", "Tu as pris", "Tu prenais", "Tu aurais pris"],
      correctAnswer: 0,
      explanation: "Au plus-que-parfait, 'prendre' se conjugue 'tu avais pris' (avoir à l'imparfait + participe passé)",
      difficulty: 10,
      topic: "Plus-que-parfait",
      learningObjective: "Conjuguer le verbe prendre au plus-que-parfait"
    },
    {
      id: 167,
      question: "Identifiez la figure de style dans : 'Le vent hurle dans la nuit'",
      options: ["Métaphore", "Personnification", "Comparaison", "Hyperbole"],
      correctAnswer: 1,
      explanation: "La personnification attribue des qualités humaines à des objets : le vent 'hurle'",
      difficulty: 10,
      topic: "Figures de style",
      learningObjective: "Reconnaître la personnification"
    },
    {
      id: 168,
      question: "Analysez la structure de la phrase : 'L'étudiant qui travaille réussit'",
      options: ["Phrase simple", "Phrase complexe avec relative", "Phrase complexe avec conjonctive", "Phrase complexe avec participiale"],
      correctAnswer: 1,
      explanation: "C'est une phrase complexe avec une proposition relative introduite par 'qui'",
      difficulty: 11,
      topic: "Analyse syntaxique",
      learningObjective: "Analyser la structure des phrases complexes"
    },
    {
      id: 169,
      question: "Conjuguez 'aller' au subjonctif imparfait à la 2ème personne du pluriel",
      options: ["Vous alliez", "Vous fussiez", "Vous allassiez", "Vous iriez"],
      correctAnswer: 2,
      explanation: "Au subjonctif imparfait, 'aller' se conjugue 'vous allassiez'",
      difficulty: 11,
      topic: "Subjonctif imparfait",
      learningObjective: "Conjuguer le verbe aller au subjonctif imparfait"
    },
    {
      id: 170,
      question: "Quel est le registre de langue dans : 'Puis-je vous être utile ?' ?",
      options: ["Familier", "Courant", "Soutenu", "Populaire"],
      correctAnswer: 2,
      explanation: "C'est un registre soutenu avec des formules de politesse élaborées",
      difficulty: 12,
      topic: "Registres de langue",
      learningObjective: "Identifier les registres de langue"
    },
    {
      id: 171,
      question: "Conjuguez le verbe 'faire' au plus-que-parfait à la 3ème personne du pluriel",
      options: ["Ils avaient fait", "Ils ont fait", "Ils faisaient", "Ils auraient fait"],
      correctAnswer: 0,
      explanation: "Au plus-que-parfait, 'faire' se conjugue 'ils avaient fait' (avoir à l'imparfait + participe passé)",
      difficulty: 10,
      topic: "Plus-que-parfait",
      learningObjective: "Conjuguer le verbe faire au plus-que-parfait"
    },
    {
      id: 172,
      question: "Identifiez la figure de style dans : 'Il est grand comme un géant'",
      options: ["Métaphore", "Personnification", "Comparaison", "Hyperbole"],
      correctAnswer: 2,
      explanation: "La comparaison utilise un mot de liaison : 'comme un géant'",
      difficulty: 10,
      topic: "Figures de style",
      learningObjective: "Distinguer la comparaison de la métaphore"
    },
    {
      id: 173,
      question: "Analysez la structure de la phrase : 'Bien qu'il pleuve, nous sortons'",
      options: ["Phrase simple", "Phrase complexe avec relative", "Phrase complexe avec conjonctive", "Phrase complexe avec participiale"],
      correctAnswer: 2,
      explanation: "C'est une phrase complexe avec une proposition conjonctive introduite par 'bien que'",
      difficulty: 11,
      topic: "Analyse syntaxique",
      learningObjective: "Analyser la structure des phrases complexes"
    },
    {
      id: 174,
      question: "Conjuguez 'avoir' au subjonctif imparfait à la 3ème personne du pluriel",
      options: ["Ils aient", "Ils avaient", "Ils eussent", "Ils auraient"],
      correctAnswer: 2,
      explanation: "Au subjonctif imparfait, 'avoir' se conjugue 'ils eussent'",
      difficulty: 11,
      topic: "Subjonctif imparfait",
      learningObjective: "Conjuguer le verbe avoir au subjonctif imparfait"
    },
    {
      id: 175,
      question: "Quel est le registre de langue dans : 'Ça déchire !' ?",
      options: ["Familier", "Courant", "Soutenu", "Populaire"],
      correctAnswer: 3,
      explanation: "C'est un registre populaire avec des expressions argotiques",
      difficulty: 12,
      topic: "Registres de langue",
      learningObjective: "Identifier les registres de langue"
    },
    {
      id: 176,
      question: "Conjuguez le verbe 'voir' au plus-que-parfait à la 1ère personne du singulier",
      options: ["J'avais vu", "J'ai vu", "Je voyais", "J'aurais vu"],
      correctAnswer: 0,
      explanation: "Au plus-que-parfait, 'voir' se conjugue 'j'avais vu' (avoir à l'imparfait + participe passé)",
      difficulty: 10,
      topic: "Plus-que-parfait",
      learningObjective: "Conjuguer le verbe voir au plus-que-parfait"
    },
    {
      id: 177,
      question: "Identifiez la figure de style dans : 'Il a un courage de lion'",
      options: ["Comparaison", "Métaphore", "Métonymie", "Synecdoque"],
      correctAnswer: 1,
      explanation: "La métaphore établit une comparaison sans mot de liaison : 'courage de lion'",
      difficulty: 10,
      topic: "Figures de style",
      learningObjective: "Reconnaître la métaphore"
    },
    {
      id: 178,
      question: "Analysez la structure de la phrase : 'L'enfant qui dort est calme'",
      options: ["Phrase simple", "Phrase complexe avec relative", "Phrase complexe avec conjonctive", "Phrase complexe avec participiale"],
      correctAnswer: 1,
      explanation: "C'est une phrase complexe avec une proposition relative introduite par 'qui'",
      difficulty: 11,
      topic: "Analyse syntaxique",
      learningObjective: "Analyser la structure des phrases complexes"
    },
    {
      id: 179,
      question: "Conjuguez 'venir' au subjonctif imparfait à la 1ère personne du pluriel",
      options: ["Nous venions", "Nous vînmes", "Nous vinsse", "Nous viendrions"],
      correctAnswer: 2,
      explanation: "Au subjonctif imparfait, 'venir' se conjugue 'nous vinsse'",
      difficulty: 11,
      topic: "Subjonctif imparfait",
      learningObjective: "Conjuguer le verbe venir au subjonctif imparfait"
    },
    {
      id: 180,
      question: "Quel est le registre de langue dans : 'Je vous prie d'agréer mes salutations distinguées' ?",
      options: ["Familier", "Courant", "Soutenu", "Populaire"],
      correctAnswer: 2,
      explanation: "C'est un registre très soutenu avec des formules de politesse très élaborées",
      difficulty: 12,
      topic: "Registres de langue",
      learningObjective: "Identifier les registres de langue"
    },
    {
      id: 181,
      question: "Conjuguez le verbe 'devoir' au plus-que-parfait à la 2ème personne du pluriel",
      options: ["Vous aviez dû", "Vous avez dû", "Vous deviez", "Vous auriez dû"],
      correctAnswer: 0,
      explanation: "Au plus-que-parfait, 'devoir' se conjugue 'vous aviez dû' (avoir à l'imparfait + participe passé)",
      difficulty: 10,
      topic: "Plus-que-parfait",
      learningObjective: "Conjuguer le verbe devoir au plus-que-parfait"
    },
    {
      id: 182,
      question: "Identifiez la figure de style dans : 'La lune se cache derrière les nuages'",
      options: ["Métaphore", "Personnification", "Comparaison", "Hyperbole"],
      correctAnswer: 1,
      explanation: "La personnification attribue des qualités humaines à des objets : la lune 'se cache'",
      difficulty: 10,
      topic: "Figures de style",
      learningObjective: "Reconnaître la personnification"
    },
    {
      id: 183,
      question: "Analysez la structure de la phrase : 'Pour que tu réussisses, il faut travailler'",
      options: ["Phrase simple", "Phrase complexe avec relative", "Phrase complexe avec conjonctive", "Phrase complexe avec participiale"],
      correctAnswer: 2,
      explanation: "C'est une phrase complexe avec une proposition conjonctive introduite par 'pour que'",
      difficulty: 11,
      topic: "Analyse syntaxique",
      learningObjective: "Analyser la structure des phrases complexes"
    },
    {
      id: 184,
      question: "Conjuguez 'faire' au subjonctif imparfait à la 2ème personne du singulier",
      options: ["Tu fasses", "Tu faisais", "Tu fisses", "Tu ferais"],
      correctAnswer: 2,
      explanation: "Au subjonctif imparfait, 'faire' se conjugue 'tu fisses'",
      difficulty: 11,
      topic: "Subjonctif imparfait",
      learningObjective: "Conjuguer le verbe faire au subjonctif imparfait"
    },
    {
      id: 185,
      question: "Quel est le registre de langue dans : 'C'est pas terrible' ?",
      options: ["Familier", "Courant", "Soutenu", "Populaire"],
      correctAnswer: 0,
      explanation: "C'est un registre familier avec des contractions et des expressions informelles",
      difficulty: 12,
      topic: "Registres de langue",
      learningObjective: "Identifier les registres de langue"
    },
    {
      id: 186,
      question: "Conjuguez le verbe 'pouvoir' au plus-que-parfait à la 3ème personne du singulier",
      options: ["Il avait pu", "Il a pu", "Il pouvait", "Il aurait pu"],
      correctAnswer: 0,
      explanation: "Au plus-que-parfait, 'pouvoir' se conjugue 'il avait pu' (avoir à l'imparfait + participe passé)",
      difficulty: 10,
      topic: "Plus-que-parfait",
      learningObjective: "Conjuguer le verbe pouvoir au plus-que-parfait"
    },
    {
      id: 187,
      question: "Identifiez la figure de style dans : 'Il a une force herculéenne'",
      options: ["Comparaison", "Métaphore", "Métonymie", "Synecdoque"],
      correctAnswer: 1,
      explanation: "La métaphore établit une comparaison sans mot de liaison : 'force herculéenne'",
      difficulty: 10,
      topic: "Figures de style",
      learningObjective: "Reconnaître la métaphore"
    },
    {
      id: 188,
      question: "Analysez la structure de la phrase : 'L'oiseau qui chante est un rossignol'",
      options: ["Phrase simple", "Phrase complexe avec relative", "Phrase complexe avec conjonctive", "Phrase complexe avec participiale"],
      correctAnswer: 1,
      explanation: "C'est une phrase complexe avec une proposition relative introduite par 'qui'",
      difficulty: 11,
      topic: "Analyse syntaxique",
      learningObjective: "Analyser la structure des phrases complexes"
    },
    {
      id: 189,
      question: "Conjuguez 'être' au subjonctif imparfait à la 3ème personne du pluriel",
      options: ["Ils soient", "Ils étaient", "Ils fussent", "Ils seraient"],
      correctAnswer: 2,
      explanation: "Au subjonctif imparfait, 'être' se conjugue 'ils fussent'",
      difficulty: 11,
      topic: "Subjonctif imparfait",
      learningObjective: "Conjuguer le verbe être au subjonctif imparfait"
    },
    {
      id: 190,
      question: "Quel est le registre de langue dans : 'Je vous en prie' ?",
      options: ["Familier", "Courant", "Soutenu", "Populaire"],
      correctAnswer: 2,
      explanation: "C'est un registre soutenu avec des formules de politesse",
      difficulty: 12,
      topic: "Registres de langue",
      learningObjective: "Identifier les registres de langue"
    },
    {
      id: 191,
      question: "Conjuguez le verbe 'savoir' au plus-que-parfait à la 1ère personne du pluriel",
      options: ["Nous avions su", "Nous avons su", "Nous savions", "Nous aurions su"],
      correctAnswer: 0,
      explanation: "Au plus-que-parfait, 'savoir' se conjugue 'nous avions su' (avoir à l'imparfait + participe passé)",
      difficulty: 10,
      topic: "Plus-que-parfait",
      learningObjective: "Conjuguer le verbe savoir au plus-que-parfait"
    },
    {
      id: 192,
      question: "Identifiez la figure de style dans : 'Le soleil se lève à l'est'",
      options: ["Métaphore", "Personnification", "Comparaison", "Hyperbole"],
      correctAnswer: 1,
      explanation: "La personnification attribue des qualités humaines à des objets : le soleil 'se lève'",
      difficulty: 10,
      topic: "Figures de style",
      learningObjective: "Reconnaître la personnification"
    },
    {
      id: 193,
      question: "Analysez la structure de la phrase : 'Quand il fait beau, nous sortons'",
      options: ["Phrase simple", "Phrase complexe avec relative", "Phrase complexe avec conjonctive", "Phrase complexe avec participiale"],
      correctAnswer: 2,
      explanation: "C'est une phrase complexe avec une proposition conjonctive introduite par 'quand'",
      difficulty: 11,
      topic: "Analyse syntaxique",
      learningObjective: "Analyser la structure des phrases complexes"
    },
    {
      id: 194,
      question: "Conjuguez 'aller' au subjonctif imparfait à la 1ère personne du singulier",
      options: ["J'aille", "J'allais", "J'allasse", "J'irais"],
      correctAnswer: 2,
      explanation: "Au subjonctif imparfait, 'aller' se conjugue 'j'allasse'",
      difficulty: 11,
      topic: "Subjonctif imparfait",
      learningObjective: "Conjuguer le verbe aller au subjonctif imparfait"
    },
    {
      id: 195,
      question: "Quel est le registre de langue dans : 'C'est cool !' ?",
      options: ["Familier", "Courant", "Soutenu", "Populaire"],
      correctAnswer: 0,
      explanation: "C'est un registre familier avec des expressions informelles",
      difficulty: 12,
      topic: "Registres de langue",
      learningObjective: "Identifier les registres de langue"
    },
    {
      id: 196,
      question: "Conjuguez le verbe 'voir' au plus-que-parfait à la 2ème personne du pluriel",
      options: ["Vous aviez vu", "Vous avez vu", "Vous voyiez", "Vous auriez vu"],
      correctAnswer: 0,
      explanation: "Au plus-que-parfait, 'voir' se conjugue 'vous aviez vu' (avoir à l'imparfait + participe passé)",
      difficulty: 10,
      topic: "Plus-que-parfait",
      learningObjective: "Conjuguer le verbe voir au plus-que-parfait"
    },
    {
      id: 197,
      question: "Identifiez la figure de style dans : 'Il est rapide comme l'éclair'",
      options: ["Métaphore", "Personnification", "Comparaison", "Hyperbole"],
      correctAnswer: 2,
      explanation: "La comparaison utilise un mot de liaison : 'comme l'éclair'",
      difficulty: 10,
      topic: "Figures de style",
      learningObjective: "Distinguer la comparaison de la métaphore"
    },
    {
      id: 198,
      question: "Analysez la structure de la phrase : 'L'homme qui parle est mon père'",
      options: ["Phrase simple", "Phrase complexe avec relative", "Phrase complexe avec conjonctive", "Phrase complexe avec participiale"],
      correctAnswer: 1,
      explanation: "C'est une phrase complexe avec une proposition relative introduite par 'qui'",
      difficulty: 11,
      topic: "Analyse syntaxique",
      learningObjective: "Analyser la structure des phrases complexes"
    },
    {
      id: 199,
      question: "Conjuguez 'prendre' au subjonctif imparfait à la 3ème personne du pluriel",
      options: ["Ils prennent", "Ils prenaient", "Ils prissent", "Ils prendraient"],
      correctAnswer: 2,
      explanation: "Au subjonctif imparfait, 'prendre' se conjugue 'ils prissent'",
      difficulty: 11,
      topic: "Subjonctif imparfait",
      learningObjective: "Conjuguer le verbe prendre au subjonctif imparfait"
    },
    {
      id: 200,
      question: "Quel est le registre de langue dans : 'Je vous remercie infiniment' ?",
      options: ["Familier", "Courant", "Soutenu", "Populaire"],
      correctAnswer: 2,
      explanation: "C'est un registre soutenu avec des formules de politesse élaborées",
      difficulty: 12,
      topic: "Registres de langue",
      learningObjective: "Identifier les registres de langue"
    }
  ]
};

export const getFrenchQuestionsByLevel = (level: string, count: number): FrenchQuestion[] => {
  const levelQuestions = FRENCH_QUESTIONS_BANK[level as keyof typeof FRENCH_QUESTIONS_BANK];
  if (!levelQuestions) {
    return FRENCH_QUESTIONS_BANK["Débutant (1-3)"];
  }
  
  // Retourner toutes les questions du niveau pour permettre la génération de variantes
  return levelQuestions;
};

export const generateUniqueQuestions = (level: string, count: number): FrenchQuestion[] => {
  const questions = getFrenchQuestionsByLevel(level, count);
  
  // Vérifier qu'on a des questions de base
  if (!questions || questions.length === 0) {
    console.warn(`Aucune question trouvée pour le niveau: ${level}`);
    return [];
  }
  
  console.log(`🔍 Génération de ${count} questions pour le niveau: ${level}`);
  console.log(`📚 Questions disponibles: ${questions.length}`);
  
  // Commencer avec les questions de base
  const uniqueQuestions: FrenchQuestion[] = [];
  const seenQuestions = new Set<string>();
  
  // Ajouter d'abord toutes les questions de base uniques
  for (const question of questions) {
    const questionKey = `${question.question}-${question.topic}`;
    if (!seenQuestions.has(questionKey)) {
      seenQuestions.add(questionKey);
      uniqueQuestions.push(question);
      
      // Si on a assez de questions, arrêter
      if (uniqueQuestions.length >= count) {
        break;
      }
    }
  }
  
  console.log(`✅ Questions de base uniques ajoutées: ${uniqueQuestions.length}`);
  
  // Si on n'a pas assez de questions, générer des variantes de manière plus agressive
  if (uniqueQuestions.length < count) {
    console.log(`🔄 Génération de variantes pour atteindre ${count} questions...`);
    
    let attempts = 0;
    const maxAttempts = count * 10; // Augmenter le nombre de tentatives
    
    while (uniqueQuestions.length < count && attempts < maxAttempts) {
      // Utiliser toutes les questions de base pour générer des variantes
      for (let i = 0; i < questions.length && uniqueQuestions.length < count; i++) {
        const baseQuestion = questions[i];
        
        if (baseQuestion) {
          try {
            // Générer plusieurs variantes par question de base
            for (let variantNum = 1; variantNum <= 3 && uniqueQuestions.length < count; variantNum++) {
              const variant = generateQuestionVariant(baseQuestion, uniqueQuestions.length + variantNum);
              const variantKey = `${variant.question}-${variant.topic}`;
              
              // Vérifier que la variante n'existe pas déjà
              if (!seenQuestions.has(variantKey)) {
                seenQuestions.add(variantKey);
                uniqueQuestions.push(variant);
                console.log(`🔄 Variante ${uniqueQuestions.length} générée (basée sur question ${i + 1})`);
                
                if (uniqueQuestions.length >= count) {
                  break;
                }
              }
            }
          } catch (error) {
            console.warn(`⚠️ Erreur lors de la génération de variante:`, error);
          }
        }
      }
      
      attempts++;
      
      // Si on n'a pas progressé après plusieurs tentatives, essayer des variations plus créatives
      if (attempts > 5 && uniqueQuestions.length < count) {
        console.log(`🔄 Tentative de variations plus créatives...`);
        
        for (let i = 0; i < questions.length && uniqueQuestions.length < count; i++) {
          const baseQuestion = questions[i];
          
          if (baseQuestion) {
            try {
              // Créer des variations plus radicales
              const radicalVariant = generateRadicalVariant(baseQuestion, uniqueQuestions.length + 1);
              const variantKey = `${radicalVariant.question}-${radicalVariant.topic}`;
              
              if (!seenQuestions.has(variantKey)) {
                seenQuestions.add(variantKey);
                uniqueQuestions.push(radicalVariant);
                console.log(`🔄 Variation radicale ${uniqueQuestions.length} générée`);
                
                if (uniqueQuestions.length >= count) {
                  break;
                }
              }
            } catch (error) {
              console.warn(`⚠️ Erreur lors de la génération de variation radicale:`, error);
            }
          }
        }
      }
    }
    
    if (uniqueQuestions.length < count) {
      console.warn(`⚠️ Impossible d'atteindre ${count} questions. Générées: ${uniqueQuestions.length}`);
    }
  }
  
  console.log(`🎯 Total des questions générées: ${uniqueQuestions.length}`);
  
  // Mélanger les questions pour éviter la monotonie
  const shuffled = uniqueQuestions.sort(() => Math.random() - 0.5);
  return shuffled.slice(0, count);
};

export const generateRadicalVariant = (baseQuestion: FrenchQuestion, index: number): FrenchQuestion => {
  // Vérifier que baseQuestion est valide
  if (!baseQuestion || !baseQuestion.id || !baseQuestion.question || !baseQuestion.options || !baseQuestion.explanation) {
    console.error('Question de base invalide pour la génération de variation radicale:', baseQuestion);
    throw new Error('Question de base invalide pour la génération de variation radicale');
  }
  
  // Variations plus radicales et créatives
  const radicalStrategies = [
    // Inversion complète du contexte
    () => ({
      ...baseQuestion,
      id: baseQuestion.id + 10000 + index,
      question: baseQuestion.question
        .replace(/Quel est l'article correct \? '___ (\w+)'/g, 'Quel est l\'article correct ? \'___ $1\' (contexte inversé)')
        .replace(/Comment se conjugue/g, 'Comment se conjugue-t-il')
        .replace(/Quel est le pluriel de/g, 'Quel est le singulier de')
        .replace(/Quel est le féminin de/g, 'Quel est le masculin de'),
      options: baseQuestion.options,
      explanation: `Variation radicale de: ${baseQuestion.explanation}`,
      difficulty: Math.min(10, baseQuestion.difficulty + 2)
    }),
    
    // Changement de perspective
    () => ({
      ...baseQuestion,
      id: baseQuestion.id + 20000 + index,
      question: baseQuestion.question
        .replace(/Quel est/g, 'Pourquoi est-ce')
        .replace(/Comment se/g, 'Quand se')
        .replace(/Identifiez/g, 'Expliquez pourquoi'),
      options: baseQuestion.options,
      explanation: `Perspective différente: ${baseQuestion.explanation}`,
      difficulty: Math.min(10, baseQuestion.difficulty + 3)
    }),
    
    // Restructuration complète
    () => ({
      ...baseQuestion,
      id: baseQuestion.id + 30000 + index,
      question: `Analysez cette question: "${baseQuestion.question}"`,
      options: baseQuestion.options,
      explanation: `Analyse de: ${baseQuestion.explanation}`,
      difficulty: Math.min(10, baseQuestion.difficulty + 2)
    })
  ];
  
  // Sélectionner une stratégie basée sur l'index
  const strategyIndex = index % radicalStrategies.length;
  const strategy = radicalStrategies[strategyIndex];
  
  try {
    return strategy();
  } catch (error) {
    console.error('❌ Erreur lors de l\'application de la stratégie radicale:', error);
    // Fallback simple mais créatif
    return {
      ...baseQuestion,
      id: baseQuestion.id + 50000 + index,
      question: `Variation créative ${index + 1}: ${baseQuestion.question}`,
      options: baseQuestion.options,
      explanation: `Variation créative de: ${baseQuestion.explanation}`,
      difficulty: Math.min(10, baseQuestion.difficulty + 2)
    };
  }
};

export const generateQuestionVariant = (baseQuestion: FrenchQuestion, index: number): FrenchQuestion => {
  // Vérifier que baseQuestion est valide
  if (!baseQuestion || !baseQuestion.id || !baseQuestion.question || !baseQuestion.options || !baseQuestion.explanation) {
    console.error('Question de base invalide pour la génération de variante:', baseQuestion);
    throw new Error('Question de base invalide pour la génération de variante');
  }
  
  // Stratégies de variation plus sophistiquées
  const variationStrategies = [
    // Variation par synonymes
    () => ({
      ...baseQuestion,
      id: baseQuestion.id + 1000 + index,
      question: baseQuestion.question
        .replace(/grand/g, 'important')
        .replace(/petit/g, 'modeste')
        .replace(/bon/g, 'excellent')
        .replace(/mauvais/g, 'médiocre'),
      options: baseQuestion.options.map(opt => 
        opt.replace(/grand/g, 'important')
           .replace(/petit/g, 'modeste')
           .replace(/bon/g, 'excellent')
           .replace(/mauvais/g, 'médiocre')
      ),
      explanation: baseQuestion.explanation
        .replace(/grand/g, 'important')
        .replace(/petit/g, 'modeste')
        .replace(/bon/g, 'excellent')
        .replace(/mauvais/g, 'médiocre'),
      difficulty: Math.min(10, baseQuestion.difficulty + 1)
    }),
    
    // Variation par contexte
    () => ({
      ...baseQuestion,
      id: baseQuestion.id + 2000 + index,
      question: baseQuestion.question
        .replace(/chat/g, 'chien')
        .replace(/maison/g, 'appartement')
        .replace(/voiture/g, 'vélo')
        .replace(/livre/g, 'magazine'),
      options: baseQuestion.options.map(opt => 
        opt.replace(/chat/g, 'chien')
           .replace(/maison/g, 'appartement')
           .replace(/voiture/g, 'vélo')
           .replace(/livre/g, 'magazine')
      ),
      explanation: baseQuestion.explanation
        .replace(/chat/g, 'chien')
        .replace(/maison/g, 'appartement')
        .replace(/voiture/g, 'vélo')
        .replace(/livre/g, 'magazine'),
      difficulty: Math.min(10, baseQuestion.difficulty + 1)
    }),
    
    // Variation par structure
    () => ({
      ...baseQuestion,
      id: baseQuestion.id + 3000 + index,
      question: baseQuestion.question
        .replace(/Quel est/g, 'Quelle est la')
        .replace(/Comment se/g, 'De quelle manière se')
        .replace(/Identifiez/g, 'Reconnaissez')
        .replace(/Conjuguez/g, 'Mettez à la forme correcte'),
      options: baseQuestion.options,
      explanation: baseQuestion.explanation,
      difficulty: Math.min(10, baseQuestion.difficulty + 1)
    }),
    
    // Variation par temps verbal
    () => ({
      ...baseQuestion,
      id: baseQuestion.id + 4000 + index,
      question: baseQuestion.question
        .replace(/présent/g, 'passé composé')
        .replace(/futur/g, 'conditionnel')
        .replace(/imparfait/g, 'plus-que-parfait'),
      options: baseQuestion.options.map(opt => 
        opt.replace(/présent/g, 'passé composé')
           .replace(/futur/g, 'conditionnel')
           .replace(/imparfait/g, 'plus-que-parfait')
      ),
      explanation: baseQuestion.explanation
        .replace(/présent/g, 'passé composé')
           .replace(/futur/g, 'conditionnel')
           .replace(/imparfait/g, 'plus-que-parfait'),
      difficulty: Math.min(10, baseQuestion.difficulty + 2)
    }),
    
    // Variation par genre/nombre
    () => ({
      ...baseQuestion,
      id: baseQuestion.id + 5000 + index,
      question: baseQuestion.question
        .replace(/masculin/g, 'féminin')
        .replace(/singulier/g, 'pluriel')
        .replace(/féminin/g, 'masculin')
        .replace(/pluriel/g, 'singulier'),
      options: baseQuestion.options.map(opt => 
        opt.replace(/masculin/g, 'féminin')
           .replace(/singulier/g, 'pluriel')
           .replace(/féminin/g, 'masculin')
           .replace(/pluriel/g, 'singulier')
      ),
      explanation: baseQuestion.explanation
        .replace(/masculin/g, 'féminin')
           .replace(/singulier/g, 'pluriel')
           .replace(/féminin/g, 'masculin')
           .replace(/pluriel/g, 'singulier'),
      difficulty: Math.min(10, baseQuestion.difficulty + 1)
    })
  ];
  
  // Sélectionner une stratégie basée sur l'index
  const strategyIndex = index % variationStrategies.length;
  const strategy = variationStrategies[strategyIndex];
  
  try {
    return strategy();
  } catch (error) {
    console.error('❌ Erreur lors de l\'application de la stratégie de variation:', error);
    // Fallback simple
    return {
      ...baseQuestion,
      id: baseQuestion.id + 10000 + index,
      question: `Variante ${index + 1}: ${baseQuestion.question}`,
      options: baseQuestion.options,
      explanation: `Variante de: ${baseQuestion.explanation}`,
      difficulty: Math.min(10, baseQuestion.difficulty + 1)
    };
  }
};
