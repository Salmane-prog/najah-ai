import { FrenchQuestion, generateUniqueQuestions } from '../data/frenchQuestionsBank';

export interface AIQuestionRequest {
  subject: string;
  level: string;
  questionCount: number;
  topics: string[];
  learningObjectives: string[];
}

export interface AIQuestionResponse {
  success: boolean;
  questions: FrenchQuestion[];
  generatedBy: string;
  fallbackUsed: boolean;
}

class FrenchAIService {
  private apiBaseUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
  private isAIAvailable = false;

  constructor() {
    this.checkAIAvailability();
  }

  private async checkAIAvailability() {
    try {
      const response = await fetch(`${this.apiBaseUrl}/api/v1/ai/status`);
      this.isAIAvailable = response.ok;
    } catch (error) {
      this.isAIAvailable = false;
      console.log('🔄 Service IA non disponible, utilisation du fallback local');
    }
  }

  async generateQuestions(request: AIQuestionRequest): Promise<AIQuestionResponse> {
    try {
      // Essayer d'abord avec l'IA
      if (this.isAIAvailable) {
        const aiQuestions = await this.generateWithAI(request);
        if (aiQuestions.success && aiQuestions.questions.length >= request.questionCount) {
          return {
            success: true,
            questions: aiQuestions.questions.slice(0, request.questionCount),
            generatedBy: 'OpenAI GPT-3.5',
            fallbackUsed: false
          };
        }
      }

      // Fallback vers la banque locale
      console.log('🔄 Utilisation de la banque de questions locale');
      const localQuestions = this.generateWithLocalBank(request);
      
      return {
        success: true,
        questions: localQuestions,
        generatedBy: 'Banque locale étendue',
        fallbackUsed: true
      };

    } catch (error) {
      console.error('❌ Erreur lors de la génération:', error);
      
      // Fallback final
      const fallbackQuestions = this.generateWithLocalBank(request);
      return {
        success: true,
        questions: fallbackQuestions,
        generatedBy: 'Fallback local',
        fallbackUsed: true
      };
    }
  }

  private async generateWithAI(request: AIQuestionRequest): Promise<AIQuestionResponse> {
    try {
      const prompt = this.buildAIPrompt(request);
      
      const response = await fetch(`${this.apiBaseUrl}/api/v1/ai/generate-questions`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('najah_token') || sessionStorage.getItem('najah_token')}`
        },
        body: JSON.stringify({
          prompt,
          subject: request.subject,
          level: request.level,
          questionCount: request.questionCount,
          topics: request.topics,
          learningObjectives: request.learningObjectives
        })
      });

      if (response.ok) {
        const data = await response.json();
        return {
          success: true,
          questions: this.parseAIResponse(data.questions, request),
          generatedBy: 'OpenAI GPT-3.5',
          fallbackUsed: false
        };
      }

      throw new Error(`Erreur API: ${response.status}`);

    } catch (error) {
      console.error('❌ Erreur génération IA:', error);
      throw error;
    }
  }

  private buildAIPrompt(request: AIQuestionRequest): string {
    const topicsText = request.topics.join(', ');
    const objectivesText = request.learningObjectives.join('\n');

    return `
    Génère ${request.questionCount} questions de français de niveau ${request.level} sur les thèmes suivants : ${topicsText}
    
    Objectifs d'apprentissage :
    ${objectivesText}
    
    Format requis pour chaque question :
    {
      "question": "Question claire et précise",
      "options": ["Option A", "Option B", "Option C", "Option D"],
      "correctAnswer": 0,
      "explanation": "Explication pédagogique détaillée",
      "difficulty": ${this.getDifficultyFromLevel(request.level)},
      "topic": "Thème principal",
      "learningObjective": "Objectif spécifique"
    }
    
    Les questions doivent être variées, progressives en difficulté, et couvrir différents aspects de la langue française.
    `;
  }

  private getDifficultyFromLevel(level: string): number {
    const levelMap: { [key: string]: number } = {
      "Débutant (1-3)": 2,
      "Intermédiaire (4-6)": 5,
      "Avancé (7-9)": 8,
      "Expert (10-12)": 10
    };
    return levelMap[level] || 5;
  }

  private parseAIResponse(aiQuestions: any[], request: AIQuestionRequest): FrenchQuestion[] {
    try {
      return aiQuestions.map((q, index) => ({
        id: Date.now() + index,
        question: q.question || `Question ${index + 1}`,
        options: q.options || ['Option A', 'Option B', 'Option C', 'Option D'],
        correctAnswer: q.correctAnswer || 0,
        explanation: q.explanation || 'Explication générée par IA',
        difficulty: q.difficulty || this.getDifficultyFromLevel(request.level),
        topic: q.topic || request.topics[0] || 'Général',
        learningObjective: q.learningObjective || request.learningObjectives[0] || 'Objectif d\'apprentissage'
      }));
    } catch (error) {
      console.error('❌ Erreur parsing réponse IA:', error);
      throw error;
    }
  }

  private generateWithLocalBank(request: AIQuestionRequest): FrenchQuestion[] {
    // Utiliser la banque locale étendue avec système anti-répétition
    const questions = generateUniqueQuestions(request.level, request.questionCount);
    
    // Adapter les questions selon les thèmes et objectifs
    const adaptedQuestions = this.adaptQuestionsToTopics(questions, request.topics, request.learningObjectives);
    
    return adaptedQuestions.slice(0, request.questionCount);
  }

  private adaptQuestionsToTopics(questions: FrenchQuestion[], topics: string[], learningObjectives: string[]): FrenchQuestion[] {
    // Prioriser les questions qui correspondent aux thèmes sélectionnés
    const prioritizedQuestions = questions.sort((a, b) => {
      const aTopicMatch = topics.includes(a.topic) ? 1 : 0;
      const bTopicMatch = topics.includes(b.topic) ? 1 : 0;
      return bTopicMatch - aTopicMatch;
    });

    // Adapter les objectifs d'apprentissage
    return prioritizedQuestions.map((q, index) => ({
      ...q,
      learningObjective: learningObjectives[index % learningObjectives.length] || q.learningObjective
    }));
  }

  // Méthode pour générer des variantes intelligentes
  generateIntelligentVariants(baseQuestion: FrenchQuestion, count: number): FrenchQuestion[] {
    const variants: FrenchQuestion[] = [];
    
    for (let i = 0; i < count; i++) {
      const variant = this.createIntelligentVariant(baseQuestion, i);
      variants.push(variant);
    }
    
    return variants;
  }

  private createIntelligentVariant(baseQuestion: FrenchQuestion, index: number): FrenchQuestion {
    const variantStrategies = [
      // Variante par synonyme
      () => ({
        ...baseQuestion,
        id: baseQuestion.id + 1000 + index,
        question: baseQuestion.question.replace(/grand/g, 'important'),
        options: baseQuestion.options.map(opt => opt.replace(/grand/g, 'important')),
        explanation: baseQuestion.explanation.replace(/grand/g, 'important')
      }),
      
      // Variante par contexte
      () => ({
        ...baseQuestion,
        id: baseQuestion.id + 2000 + index,
        question: baseQuestion.question.replace(/chat/g, 'chien'),
        options: baseQuestion.options.map(opt => opt.replace(/chat/g, 'chien')),
        explanation: baseQuestion.explanation.replace(/chat/g, 'chien')
      }),
      
      // Variante par structure
      () => ({
        ...baseQuestion,
        id: baseQuestion.id + 3000 + index,
        question: baseQuestion.question.replace(/Quel est/g, 'Quelle est la'),
        options: baseQuestion.options,
        explanation: baseQuestion.explanation
      })
    ];
    
    const strategy = variantStrategies[index % variantStrategies.length];
    return strategy();
  }

  // Validation de l'unicité des questions
  validateQuestionUniqueness(questions: FrenchQuestion[]): { isValid: boolean; duplicates: string[] } {
    const seenQuestions = new Set<string>();
    const duplicates: string[] = [];
    
    for (const question of questions) {
      const questionKey = `${question.question}-${question.topic}`;
      if (seenQuestions.has(questionKey)) {
        duplicates.push(questionKey);
      } else {
        seenQuestions.add(questionKey);
      }
    }
    
    return {
      isValid: duplicates.length === 0,
      duplicates
    };
  }

  // Optimisation de la distribution des difficultés
  optimizeDifficultyDistribution(questions: FrenchQuestion[], targetCount: number): FrenchQuestion[] {
    // Déduire la plage de difficultés à partir de l'échantillon (ou fallback sur 1-12)
    const presentDifficulties = Array.from(new Set(questions.map(q => q.difficulty))).sort((a, b) => a - b);
    const difficultyLevels = presentDifficulties.length > 0 ? presentDifficulties : [1,2,3,4,5,6,7,8,9,10,11,12];

    // Nombre cible par difficulté disponible
    const questionsPerDifficulty = Math.max(1, Math.ceil(targetCount / difficultyLevels.length));

    const optimizedQuestions: FrenchQuestion[] = [];
    const questionsByDifficulty = new Map<number, FrenchQuestion[]>();

    // Grouper les questions par difficulté
    for (const question of questions) {
      const difficulty = question.difficulty;
      if (!questionsByDifficulty.has(difficulty)) {
        questionsByDifficulty.set(difficulty, []);
      }
      questionsByDifficulty.get(difficulty)!.push(question);
    }

    // Première passe: prendre jusqu'à questionsPerDifficulty pour chaque difficulté présente
    for (const difficulty of difficultyLevels) {
      const availableQuestions = (questionsByDifficulty.get(difficulty) || []).slice();
      const selected = availableQuestions.slice(0, questionsPerDifficulty);
      optimizedQuestions.push(...selected);
      // Mettre à jour le pool restant
      questionsByDifficulty.set(difficulty, availableQuestions.slice(selected.length));
      if (optimizedQuestions.length >= targetCount) break;
    }

    // Deuxième passe: remplir avec le reste de toutes difficultés jusqu'à atteindre targetCount
    if (optimizedQuestions.length < targetCount) {
      const leftovers: FrenchQuestion[] = [];
      for (const list of questionsByDifficulty.values()) {
        leftovers.push(...list);
      }
      // Ajouter aléatoirement le reste
      leftovers.sort(() => Math.random() - 0.5);
      optimizedQuestions.push(...leftovers.slice(0, Math.max(0, targetCount - optimizedQuestions.length)));
    }

    // Mélanger pour éviter la monotonie et couper à la taille demandée
    return optimizedQuestions.sort(() => Math.random() - 0.5).slice(0, targetCount);
  }
}

export const frenchAIService = new FrenchAIService();
