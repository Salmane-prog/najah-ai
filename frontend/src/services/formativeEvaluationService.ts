// Service pour les évaluations formatives

export interface FormativeEvaluationRequest {
  title: string;
  subject: string;
  assessment_type: string;
  description: string;
  target_level: string;
  duration_minutes: number;
  max_students: number;
  learning_objectives: string[];
  custom_requirements?: string;
}

export interface AIGeneratedEvaluation {
  title: string;
  description: string;
  assessment_type: string;
  criteria: Array<{
    name: string;
    description: string;
    weight: number;
    max_points: number;
  }>;
  rubric: {
    excellent: { points: number; description: string };
    good: { points: number; description: string };
    satisfactory: { points: number; description: string };
    needs_improvement: { points: number; description: string };
  };
  questions: Array<{
    question: string;
    type: string;
    max_points: number;
  }>;
  instructions: string;
  estimated_duration: number;
  difficulty_level: string;
  success_indicators: string[];
}

export interface FormativeEvaluation {
  id: number;
  title: string;
  description: string;
  assessment_type: string;
  subject: string;
  target_level: string;
  duration_minutes: number;
  max_students: number;
  learning_objectives: string[];
  criteria: any[];
  rubric: any;
  questions: any[];
  instructions: string;
  is_active: boolean;
  created_at: string;
  teacher_id: number;
}

class FormativeEvaluationService {
  // Générer une évaluation avec l'IA
  async generateWithAI(request: FormativeEvaluationRequest): Promise<AIGeneratedEvaluation> {
    // FORCER l'utilisation du générateur local pour tester
    console.log('🧠 Utilisation forcée du générateur IA local...');
    return this.generateLocalAI(request);
    
    /* Code backend commenté temporairement
    try {
      console.log('🚀 Tentative de génération IA via backend...');
      
      // Essayer d'abord le backend
      const response = await this.request('/api/v1/ai-formative-evaluations/generate-evaluation/', {
        method: 'POST',
        body: JSON.stringify(request),
      });
      
      if (response.success) {
        console.log('✅ Génération IA backend réussie');
        return response.evaluation;
      } else {
        throw new Error('Erreur lors de la génération IA backend');
      }
    } catch (error) {
      console.log('⚠️ Backend IA indisponible, utilisation du générateur local...');
      
      // Fallback : génération locale intelligente
      return this.generateLocalAI(request);
    }
    */
  }

  // Générateur IA local avec contenu unique par type
  private generateLocalAI(request: FormativeEvaluationRequest): AIGeneratedEvaluation {
    console.log('🧠 Génération IA locale pour:', request.assessment_type, 'en', request.subject);
    
    const baseTitle = `${this.getTypeDisplayName(request.assessment_type)} - ${request.subject}`;
    const timestamp = Date.now();
    
    // Générer du contenu unique basé sur le type, la matière et le timestamp
    const uniqueContent = this.generateUniqueContent(request, timestamp);
    
    return {
      title: baseTitle,
      description: uniqueContent.description,
      assessment_type: request.assessment_type,
      criteria: uniqueContent.criteria,
      rubric: uniqueContent.rubric,
      questions: uniqueContent.questions,
      instructions: uniqueContent.instructions,
      estimated_duration: request.duration_minutes,
      difficulty_level: request.target_level,
      success_indicators: uniqueContent.success_indicators
    };
  }

  // Générer du contenu unique pour chaque type
  private generateUniqueContent(request: FormativeEvaluationRequest, timestamp: number) {
    const type = request.assessment_type;
    const subject = request.subject;
    const level = request.target_level;
    
    // Utiliser le timestamp ET la matière pour varier le contenu
    const variation = (timestamp + subject.length + type.length) % 5;
    const subjectVariation = subject.length % 3;
    
    console.log('🔍 Variations calculées:', { variation, subjectVariation, subject, type, timestamp });
    
    switch (type) {
      case 'project':
        return this.generateProjectContent(subject, level, variation, subjectVariation);
      case 'presentation':
        return this.generatePresentationContent(subject, level, variation, subjectVariation);
      case 'discussion':
        return this.generateDiscussionContent(subject, level, variation, subjectVariation);
      case 'portfolio':
        return this.generatePortfolioContent(subject, level, variation, subjectVariation);
      case 'observation':
        return this.generateObservationContent(subject, level, variation, subjectVariation);
      case 'self_evaluation':
        return this.generateSelfEvaluationContent(subject, level, variation, subjectVariation);
      default:
        return this.generateProjectContent(subject, level, variation, subjectVariation);
    }
  }

  // Contenu pour Projet de Recherche
  private generateProjectContent(subject: string, level: string, variation: number, subjectVariation: number) {
    console.log('🔬 Génération contenu Projet de Recherche:', { subject, level, variation, subjectVariation });
    
    // Descriptions variées selon la matière
    const descriptions = [
      `Évaluation formative pour un projet de recherche en ${subject} permettant aux étudiants de développer leurs compétences de recherche et d'analyse.`,
      `Projet de recherche approfondi en ${subject} visant à renforcer la méthodologie scientifique et l'esprit critique.`,
      `Travail de recherche en ${subject} favorisant l'autonomie et la rigueur méthodologique des étudiants.`,
      `Recherche appliquée en ${subject} encourageant l'innovation et la créativité dans l'approche méthodologique.`,
      `Projet d'investigation en ${subject} développant la pensée analytique et la résolution de problèmes.`
    ];

    // Critères adaptés selon la matière
    let criteria;
    if (subject.toLowerCase().includes('math') || subject.toLowerCase().includes('scien')) {
      criteria = [
        { name: "Rigueur mathématique", description: "Précision des calculs et démonstrations", weight: 30, max_points: 4 },
        { name: "Méthodologie", description: "Approche systématique et logique", weight: 25, max_points: 4 },
        { name: "Analyse critique", description: "Validation des hypothèses et résultats", weight: 25, max_points: 4 },
        { name: "Présentation", description: "Clarté des graphiques et formules", weight: 20, max_points: 4 }
      ];
    } else if (subject.toLowerCase().includes('fran') || subject.toLowerCase().includes('lang')) {
      criteria = [
        { name: "Analyse littéraire", description: "Profondeur de l'analyse des textes", weight: 30, max_points: 4 },
        { name: "Méthodologie", description: "Approche critique et comparative", weight: 25, max_points: 4 },
        { name: "Expression", description: "Qualité de l'écriture et du style", weight: 25, max_points: 4 },
        { name: "Sources", description: "Diversité et pertinence des références", weight: 20, max_points: 4 }
      ];
    } else if (subject.toLowerCase().includes('hist') || subject.toLowerCase().includes('geo')) {
      criteria = [
        { name: "Recherche documentaire", description: "Qualité et diversité des sources historiques", weight: 30, max_points: 4 },
        { name: "Méthodologie", description: "Approche chronologique et spatiale", weight: 25, max_points: 4 },
        { name: "Analyse critique", description: "Interprétation et contextualisation", weight: 25, max_points: 4 },
        { name: "Présentation", description: "Clarté de la narration et des cartes", weight: 20, max_points: 4 }
      ];
    } else {
      // Critères génériques avec variations
      criteria = [
        { name: "Qualité de la recherche", description: "Pertinence et diversité des sources consultées", weight: 25, max_points: 4 },
        { name: "Méthodologie", description: "Clarté et cohérence de l'approche méthodologique", weight: 25, max_points: 4 },
        { name: "Analyse critique", description: "Profondeur de l'analyse et qualité des arguments", weight: 30, max_points: 4 },
        { name: "Présentation", description: "Clarté de la présentation et qualité du support visuel", weight: 20, max_points: 4 }
      ];
    }

    // Questions adaptées selon la matière
    let questions;
    if (subject.toLowerCase().includes('math')) {
      questions = [
        { question: `Quelle est l'hypothèse mathématique principale de votre recherche en ${subject} ?`, type: "hypothesis", max_points: 5 },
        { question: "Comment avez-vous validé vos calculs et démonstrations ?", type: "validation", max_points: 5 },
        { question: "Quels outils mathématiques avez-vous utilisés pour votre analyse ?", type: "tools", max_points: 5 }
      ];
    } else if (subject.toLowerCase().includes('fran')) {
      questions = [
        { question: `Quel corpus de textes avez-vous sélectionné pour votre analyse en ${subject} ?`, type: "corpus", max_points: 5 },
        { question: "Comment avez-vous appliqué les méthodes d'analyse littéraire ?", type: "methodology", max_points: 5 },
        { question: "Quelles sont les spécificités stylistiques que vous avez identifiées ?", type: "style", max_points: 5 }
      ];
    } else {
      questions = [
        { question: `Quelle est la question de recherche principale de votre projet en ${subject} ?`, type: "reflection", max_points: 5 },
        { question: "Comment avez-vous sélectionné vos sources de recherche ?", type: "methodology", max_points: 5 },
        { question: "Quels sont les principaux défis que vous avez rencontrés ?", type: "reflection", max_points: 5 }
      ];
    }

    // Instructions adaptées selon la matière
    let instructions;
    if (subject.toLowerCase().includes('math')) {
      instructions = [
        "Définissez clairement votre hypothèse mathématique",
        "Utilisez des méthodes de démonstration rigoureuses",
        "Vérifiez tous vos calculs et résultats",
        "Présentez vos formules de manière claire",
        "Incluez des graphiques et visualisations pertinents",
        "Préparez une démonstration orale structurée"
      ];
    } else if (subject.toLowerCase().includes('fran')) {
      instructions = [
        "Sélectionnez un corpus de textes représentatif",
        "Appliquez les méthodes d'analyse littéraire appropriées",
        "Analysez les aspects stylistiques et thématiques",
        "Contextualisez vos analyses historiquement",
        "Incluez des citations pertinentes et commentées",
        "Préparez une présentation orale argumentée"
      ];
    } else {
      instructions = [
        "Choisissez un sujet spécifique et pertinent",
        "Effectuez une recherche documentaire approfondie",
        "Développez une méthodologie claire",
        "Présentez vos résultats de manière structurée",
        "Incluez une analyse critique de vos sources",
        "Préparez une présentation orale de 10-15 minutes"
      ];
    }

    return {
      description: descriptions[variation],
      criteria,
      rubric: this.generateRubric(level),
      questions,
      instructions: instructions.join('\n'),
      success_indicators: [
        "Sujet de recherche clairement défini",
        "Méthodologie bien structurée",
        "Présentation claire et engageante",
        "Sources variées et pertinentes consultées",
        "Analyse critique développée"
      ]
    };
  }

  // Contenu pour Présentation Orale
  private generatePresentationContent(subject: string, level: string, variation: number, subjectVariation: number) {
    console.log('🎤 Génération contenu Présentation Orale:', { subject, level, variation, subjectVariation });
    
    const descriptions = [
      `Évaluation formative pour une présentation orale en ${subject} développant les compétences de communication et d'expression.`,
      `Présentation orale structurée en ${subject} visant à améliorer la clarté du discours et la confiance en soi.`,
      `Exposé oral en ${subject} favorisant la maîtrise des techniques de présentation et l'engagement de l'audience.`,
      `Communication orale en ${subject} renforçant la capacité de persuasion et l'impact sur l'audience.`,
      `Présentation interactive en ${subject} encourageant l'échange et la participation active.`
    ];

    const criteria = [
      { name: "Contenu", description: "Qualité et pertinence du contenu présenté", weight: 30, max_points: 4 },
      { name: "Structure", description: "Organisation logique et clarté du plan", weight: 25, max_points: 4 },
      { name: "Expression", description: "Clarté du discours et qualité de l'élocution", weight: 25, max_points: 4 },
      { name: "Support visuel", description: "Qualité et pertinence des supports utilisés", weight: 20, max_points: 4 }
    ];

    const questions = [
      { question: "Quel est le message principal de votre présentation ?", type: "communication", max_points: 5 },
      { question: "Comment avez-vous structuré votre argumentation ?", type: "organization", max_points: 5 },
      { question: "Quelles techniques avez-vous utilisées pour capter l'attention ?", type: "engagement", max_points: 5 }
    ];

    const instructions = [
      "Préparez un plan clair et structuré",
      "Créez des supports visuels pertinents",
      "Entraînez-vous à la fluidité du discours",
      "Anticipez les questions de l'audience",
      "Respectez le temps imparti",
      "Maintenez un contact visuel avec l'audience"
    ];

    return {
      description: descriptions[variation],
      criteria,
      rubric: this.generateRubric(level),
      questions,
      instructions: instructions.join('\n'),
      success_indicators: [
        "Message principal clairement identifié",
        "Structure logique et cohérente",
        "Expression claire et engageante",
        "Supports visuels pertinents",
        "Gestion du temps respectée"
      ]
    };
  }

  // Contenu pour Discussion Critique
  private generateDiscussionContent(subject: string, level: string, variation: number, subjectVariation: number) {
    console.log('💬 Génération contenu Discussion Critique:', { subject, level, variation, subjectVariation });
    
    const descriptions = [
      `Évaluation formative pour une discussion critique en ${subject} développant l'esprit critique et le débat constructif.`,
      `Débat analytique en ${subject} visant à améliorer la capacité d'argumentation et d'écoute active.`,
      `Discussion critique structurée en ${subject} favorisant l'échange d'idées et la réflexion collective.`,
      `Dialogue constructif en ${subject} encourageant la diversité des points de vue et la réflexion collective.`,
      `Débat structuré en ${subject} développant la pensée critique et la capacité d'argumentation.`
    ];

    const criteria = [
      { name: "Participation", description: "Engagement actif dans la discussion", weight: 25, max_points: 4 },
      { name: "Argumentation", description: "Qualité et pertinence des arguments avancés", weight: 30, max_points: 4 },
      { name: "Écoute active", description: "Capacité à écouter et rebondir sur les propos", weight: 25, max_points: 4 },
      { name: "Respect", description: "Respect des règles de débat et des autres", weight: 20, max_points: 4 }
    ];

    const questions = [
      { question: "Quel est votre point de vue principal sur le sujet ?", type: "opinion", max_points: 5 },
      { question: "Comment avez-vous réagi aux arguments des autres ?", type: "interaction", max_points: 5 },
      { question: "Qu'avez-vous appris de cette discussion ?", type: "reflection", max_points: 5 }
    ];

    const instructions = [
      "Préparez vos arguments à l'avance",
      "Écoutez activement les autres participants",
      "Respectez le temps de parole de chacun",
      "Rebondissez sur les propos des autres",
      "Restez ouvert aux points de vue différents",
      "Concluez par une synthèse personnelle"
    ];

    return {
      description: descriptions[variation],
      criteria,
      rubric: this.generateRubric(level),
      questions,
      instructions: instructions.join('\n'),
      success_indicators: [
        "Participation active et constructive",
        "Arguments pertinents et bien structurés",
        "Écoute active et respectueuse",
        "Capacité de rebond et d'adaptation",
        "Synthèse personnelle pertinente"
      ]
    };
  }

  // Contenu pour Portfolio
  private generatePortfolioContent(subject: string, level: string, variation: number, subjectVariation: number) {
    console.log('📁 Génération contenu Portfolio:', { subject, level, variation, subjectVariation });
    
    const descriptions = [
      `Évaluation formative pour un portfolio en ${subject} permettant de documenter le parcours d'apprentissage.`,
      `Collection de travaux en ${subject} visant à démontrer l'évolution des compétences et la réflexion métacognitive.`,
      `Portfolio réflexif en ${subject} favorisant l'auto-évaluation et la prise de conscience des progrès.`,
      `Collection structurée en ${subject} illustrant la progression et la maîtrise des compétences.`,
      `Portfolio d'apprentissage en ${subject} documentant les réalisations et les réflexions personnelles.`
    ];

    const criteria = [
      { name: "Sélection", description: "Pertinence et diversité des travaux sélectionnés", weight: 25, max_points: 4 },
      { name: "Organisation", description: "Structure claire et logique du portfolio", weight: 25, max_points: 4 },
      { name: "Réflexion", description: "Qualité de l'analyse et de la réflexion personnelle", weight: 30, max_points: 4 },
      { name: "Présentation", description: "Qualité visuelle et clarté de la présentation", weight: 20, max_points: 4 }
    ];

    const questions = [
      { question: "Quels travaux illustrent le mieux vos progrès ?", type: "selection", max_points: 5 },
      { question: "Comment avez-vous organisé votre portfolio ?", type: "organization", max_points: 5 },
      { question: "Que révèle ce portfolio sur votre apprentissage ?", type: "reflection", max_points: 5 }
    ];

    const instructions = [
      "Sélectionnez vos meilleurs travaux",
      "Organisez-les de manière logique",
      "Ajoutez des commentaires réflexifs",
      "Incluez des exemples de progression",
      "Présentez clairement chaque section",
      "Concluez par une auto-évaluation globale"
    ];

    return {
      description: descriptions[variation],
      criteria,
      rubric: this.generateRubric(level),
      questions,
      instructions: instructions.join('\n'),
      success_indicators: [
        "Sélection pertinente des travaux",
        "Organisation claire et logique",
        "Réflexion personnelle approfondie",
        "Démonstration des progrès",
        "Présentation soignée et professionnelle"
      ]
    };
  }

  // Contenu pour Observation Participante
  private generateObservationContent(subject: string, level: string, variation: number, subjectVariation: number) {
    console.log('👁️ Génération contenu Observation Participante:', { subject, level, variation, subjectVariation });
    
    const descriptions = [
      `Évaluation formative pour une observation participante en ${subject} développant les compétences d'analyse et d'empathie.`,
      `Observation structurée en ${subject} visant à améliorer la capacité d'analyse et la prise de recul.`,
      `Immersion observationnelle en ${subject} favorisant la compréhension des dynamiques et des comportements.`,
      `Analyse observationnelle en ${subject} renforçant la capacité d'interprétation et de synthèse.`,
      `Observation méthodique en ${subject} développant l'esprit d'analyse et la rigueur scientifique.`
    ];

    const criteria = [
      { name: "Observation", description: "Qualité et précision des observations", weight: 30, max_points: 4 },
      { name: "Analyse", description: "Profondeur de l'analyse des données recueillies", weight: 30, max_points: 4 },
      { name: "Réflexion", description: "Qualité de la réflexion personnelle", weight: 25, max_points: 4 },
      { name: "Documentation", description: "Qualité de la documentation des observations", weight: 15, max_points: 4 }
    ];

    const questions = [
      { question: "Qu'avez-vous observé de plus surprenant ?", type: "observation", max_points: 5 },
      { question: "Comment avez-vous analysé vos observations ?", type: "analysis", max_points: 5 },
      { question: "Quelles conclusions en tirez-vous ?", type: "conclusion", max_points: 5 }
    ];

    const instructions = [
      "Définissez clairement votre objectif d'observation",
      "Prenez des notes détaillées et objectives",
      "Identifiez les patterns et les anomalies",
      "Analysez vos observations de manière critique",
      "Documentez vos réflexions personnelles",
      "Préparez un rapport d'observation structuré"
    ];

    return {
      description: descriptions[variation],
      criteria,
      rubric: this.generateRubric(level),
      questions,
      instructions: instructions.join('\n'),
      success_indicators: [
        "Observations précises et objectives",
        "Analyse approfondie des données",
        "Réflexion personnelle pertinente",
        "Documentation claire et structurée",
        "Conclusions bien argumentées"
      ]
    };
  }

  // Contenu pour Auto-évaluation
  private generateSelfEvaluationContent(subject: string, level: string, variation: number, subjectVariation: number) {
    console.log('🔍 Génération contenu Auto-évaluation:', { subject, level, variation, subjectVariation });
    
    const descriptions = [
      `Évaluation formative pour une auto-évaluation en ${subject} développant la conscience de ses propres compétences.`,
      `Réflexion personnelle en ${subject} visant à améliorer la capacité d'auto-analyse et de métacognition.`,
      `Auto-évaluation structurée en ${subject} favorisant la prise de conscience des forces et des axes d'amélioration.`,
      `Analyse réflexive en ${subject} encourageant la métacognition et l'auto-régulation.`,
      `Évaluation personnelle en ${subject} développant la conscience de soi et la responsabilité d'apprentissage.`
    ];

    const criteria = [
      { name: "Honnêteté", description: "Objectivité et honnêteté dans l'auto-évaluation", weight: 25, max_points: 4 },
      { name: "Analyse", description: "Profondeur de l'analyse de ses propres compétences", weight: 30, max_points: 4 },
      { name: "Objectifs", description: "Clarté et réalisme des objectifs fixés", weight: 25, max_points: 4 },
      { name: "Plan d'action", description: "Concrétude du plan d'amélioration", weight: 20, max_points: 4 }
    ];

    const questions = [
      { question: "Quelles sont vos forces principales dans cette matière ?", type: "strengths", max_points: 5 },
      { question: "Sur quoi aimeriez-vous progresser ?", type: "improvement", max_points: 5 },
      { question: "Comment comptez-vous y parvenir ?", type: "planning", max_points: 5 }
    ];

    const instructions = [
      "Évaluez honnêtement vos compétences actuelles",
      "Identifiez vos forces et vos faiblesses",
      "Fixez des objectifs réalistes et mesurables",
      "Définissez un plan d'action concret",
      "Prévoyez des indicateurs de progression",
      "Planifiez des moments de réévaluation"
    ];

    return {
      description: descriptions[variation],
      criteria,
      rubric: this.generateRubric(level),
      questions,
      instructions: instructions.join('\n'),
      success_indicators: [
        "Auto-évaluation honnête et objective",
        "Analyse approfondie des compétences",
        "Objectifs clairs et réalistes",
        "Plan d'action concret et réalisable",
        "Indicateurs de progression définis"
      ]
    };
  }

  // Générer une grille de notation adaptée au niveau
  private generateRubric(level: string) {
    const baseRubric = {
      excellent: { points: 4, description: "Travail exceptionnel démontrant une maîtrise approfondie du sujet" },
      good: { points: 3, description: "Travail de qualité avec une bonne compréhension du sujet" },
      satisfactory: { points: 2, description: "Travail acceptable avec une compréhension de base" },
      needs_improvement: { points: 1, description: "Travail nécessitant des améliorations significatives" }
    };

    // Adapter selon le niveau
    if (level === 'beginner') {
      baseRubric.excellent.description = "Travail remarquable pour un débutant, démontrant une compréhension solide des bases";
      baseRubric.good.description = "Bon travail de débutant avec une compréhension correcte des concepts fondamentaux";
    } else if (level === 'advanced') {
      baseRubric.excellent.description = "Travail d'expert démontrant une maîtrise exceptionnelle et une créativité remarquable";
      baseRubric.good.description = "Travail avancé avec une compréhension approfondie et une approche innovante";
    }

    return baseRubric;
  }

  // Obtenir le nom d'affichage du type
  private getTypeDisplayName(type: string): string {
    const typeNames: { [key: string]: string } = {
      'project': 'Projet de Recherche',
      'presentation': 'Présentation Orale',
      'discussion': 'Discussion Critique',
      'portfolio': 'Portfolio',
      'observation': 'Observation Participante',
      'self_evaluation': 'Auto-évaluation'
    };
    return typeNames[type] || 'Évaluation';
  }

  // Récupérer tous les types d'évaluations supportés
  async getAvailableTypes(): Promise<any[]> {
    try {
      const response = await this.request('/api/v1/ai-formative-evaluations/available-types/');
      return response.assessment_types || [];
    } catch (error) {
      console.error('Erreur lors de la récupération des types:', error);
      // Types par défaut si l'API échoue
      return [
        { type: 'project', name: 'Projet de Recherche', description: 'Travail de recherche individuel ou en groupe' },
        { type: 'presentation', name: 'Présentation Orale', description: 'Exposé oral devant la classe' },
        { type: 'discussion', name: 'Discussion Critique', description: 'Débat et analyse critique en groupe' },
        { type: 'portfolio', name: 'Portfolio', description: 'Collection de travaux et réflexions' },
        { type: 'observation', name: 'Observation Participante', description: 'Observation et analyse de situations' },
        { type: 'self_evaluation', name: 'Auto-évaluation', description: 'Évaluation de ses propres compétences' }
      ];
    }
  }

  // Créer une nouvelle évaluation formative
  async createEvaluation(evaluation: AIGeneratedEvaluation, formData: any): Promise<FormativeEvaluation> {
    try {
      console.log('💾 Tentative de sauvegarde backend...');
      
      // Structure simplifiée pour le backend
      const adaptedData = {
        title: evaluation.title,
        description: evaluation.description,
        assessment_type: evaluation.assessment_type,
        subject: formData.subject || "Mathématiques",
        target_level: formData.target_level || "intermediate",
        duration_minutes: formData.duration_minutes || 60,
        max_students: formData.max_students || 30,
        learning_objectives: ["Compétence 1", "Compétence 2"],
        criteria: evaluation.criteria.map(c => ({
          name: c.name,
          description: c.description,
          weight: c.weight,
          max_points: c.max_points
        })),
        rubric: {
          excellent: evaluation.rubric.excellent,
          good: evaluation.rubric.good,
          satisfactory: evaluation.rubric.satisfactory,
          needs_improvement: evaluation.rubric.needs_improvement
        },
        questions: evaluation.questions.map(q => ({
          question: q.question,
          type: q.type,
          max_points: q.max_points
        })),
        instructions: evaluation.instructions,
        success_indicators: evaluation.success_indicators
      };

      console.log('[FORMATIVE] Données adaptées envoyées:', adaptedData);
      console.log('[FORMATIVE] URL backend:', 'http://localhost:8000/api/v1/formative-evaluations/');

      // Appel direct au backend
      const response = await this.request('/api/v1/formative-evaluations/', {
        method: 'POST',
        body: JSON.stringify(adaptedData),
      });
      
      console.log('✅ Sauvegarde backend réussie:', response);
      return response;
      
    } catch (error) {
      console.error('❌ Erreur lors de la création:', error);
      throw error; // Remonter l'erreur pour la gérer dans l'UI
    }
  }



  // Récupérer toutes les évaluations formatives
  async getAllEvaluations(): Promise<FormativeEvaluation[]> {
    try {
      const response = await this.request('/api/v1/formative-evaluations/');
      return response || [];
    } catch (error) {
      console.error('Erreur lors de la récupération des évaluations formatives:', error);
      return [];
    }
  }

  // Mettre à jour une évaluation formative
  async updateEvaluation(evaluationId: number, updatedData: Partial<FormativeEvaluation>): Promise<FormativeEvaluation> {
    try {
      console.log('💾 Tentative de mise à jour backend...');
      
      // Structure simplifiée pour le backend
      const adaptedData = {
        title: updatedData.title,
        description: updatedData.description,
        assessment_type: updatedData.assessment_type,
        subject: updatedData.subject,
        target_level: updatedData.target_level,
        duration_minutes: updatedData.duration_minutes,
        max_students: updatedData.max_students,
        learning_objectives: updatedData.learning_objectives || ["Compétence 1", "Compétence 2"],
        criteria: updatedData.criteria?.map(c => ({
          name: c.name,
          description: c.description,
          weight: c.weight,
          max_points: c.max_points
        })) || [],
        rubric: updatedData.rubric || {
          excellent: { points: 4, description: "Travail exceptionnel" },
          good: { points: 3, description: "Travail de qualité" },
          satisfactory: { points: 2, description: "Travail acceptable" },
          needs_improvement: { points: 1, description: "Travail à améliorer" }
        },
        questions: updatedData.questions?.map(q => ({
          question: q.question,
          type: q.type,
          max_points: q.max_points
        })) || [],
        instructions: updatedData.instructions || '',
        success_indicators: updatedData.success_indicators || []
      };

      console.log('[FORMATIVE] Données de mise à jour envoyées:', adaptedData);

      // Appel au backend
      const response = await this.request(`/api/v1/formative-evaluations/${evaluationId}/`, {
        method: 'POST',
        body: JSON.stringify(adaptedData),
      });
      
      console.log('✅ Mise à jour backend réussie:', response);
      return response;
      
    } catch (error) {
      console.error('❌ Erreur lors de la mise à jour:', error);
      throw error;
    }
  }

  // Activer/Désactiver une évaluation
  async toggleEvaluationStatus(evaluationId: number, isActive: boolean): Promise<boolean> {
    try {
      const response = await this.request(`/api/v1/formative-evaluations/${evaluationId}/toggle-status/`, {
        method: 'PATCH',
        body: JSON.stringify({ is_active: isActive }),
      });
      return response.success;
    } catch (error) {
      console.error('Erreur lors du changement de statut:', error);
      return false;
    }
  }

  // Méthode privée pour les requêtes
  private async request(endpoint: string, options: RequestInit = {}): Promise<any> {
    const token = localStorage.getItem('najah_token');
    
    if (!token) {
      throw new Error('Token d\'authentification manquant. Veuillez vous reconnecter.');
    }
    
    const defaultOptions: RequestInit = {
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
      ...options,
    };

    const fullUrl = `http://localhost:8000${endpoint}`;
    console.log(`[FORMATIVE] Appel API: ${fullUrl}`);
    console.log(`[FORMATIVE] Token: ${token ? 'Présent' : 'Manquant'}`);
    console.log(`[FORMATIVE] Options:`, defaultOptions);
    console.log(`[FORMATIVE] Body:`, options.body);

    try {
      const response = await fetch(fullUrl, defaultOptions);
      
      console.log(`[FORMATIVE] Réponse reçue:`, {
        status: response.status,
        statusText: response.statusText,
        headers: Object.fromEntries(response.headers.entries())
      });
      
      if (!response.ok) {
        // Essayer de lire le corps de l'erreur
        let errorBody = '';
        try {
          errorBody = await response.text();
          console.error(`[FORMATIVE] Corps de l'erreur:`, errorBody);
        } catch (e) {
          console.error(`[FORMATIVE] Impossible de lire le corps de l'erreur:`, e);
        }
        
        if (response.status === 401) {
          throw new Error('Erreur d\'authentification. Veuillez vous reconnecter.');
        } else if (response.status === 500) {
          throw new Error(`Erreur serveur (500): ${errorBody || 'Problème interne du serveur'}`);
        } else {
          throw new Error(`Erreur HTTP ${response.status}: ${response.statusText} - ${errorBody}`);
        }
      }
      
      const responseData = await response.json();
      console.log(`[FORMATIVE] Données reçues:`, responseData);
      return responseData;
      
    } catch (fetchError) {
      console.error(`[FORMATIVE] Erreur fetch:`, fetchError);
      throw fetchError;
    }
  }
}

export const formativeEvaluationService = new FormativeEvaluationService();
