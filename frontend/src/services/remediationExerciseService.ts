/**
 * Service pour interagir avec la banque d'exercices de remédiation diversifiée
 */

export interface DiverseExercise {
  id: string;
  type: 'quiz' | 'practice' | 'matching' | 'categorization' | 'reading' | 'listening' | 'drag_drop' | 'fill_blank';
  question: string;
  options?: string[];
  correct?: string;
  explanation: string;
  difficulty: 'facile' | 'intermédiaire' | 'avancé';
  topic: string;
  estimated_time: number;
  pairs?: [string, string][];
  items?: string[];
  categories?: string[];
  solutions?: Record<string, string[]>;
  blanks?: string[];
  hints?: string[];
  title?: string;
  text?: string;
  audio_file?: string;
  transcript?: string;
  sentence_parts?: string[];
  correct_order?: string[];
}

export interface ExerciseStatistics {
  total_exercises: number;
  by_category: Record<string, number>;
  by_difficulty: Record<string, number>;
  categories: string[];
  difficulties: string[];
}

export interface DiverseExerciseResponse {
  success: boolean;
  exercises: DiverseExercise[];
  total_found: number;
  topic: string;
  difficulty: string;
  avoided_repetition: boolean;
}

export class RemediationExerciseService {
  private static baseUrl = '/api/v1/remediation';

  /**
   * Récupère des exercices diversifiés pour éviter la redondance
   */
  static async getDiverseExercises(
    topic: string,
    difficulty: string,
    count: number = 3,
    token: string // Ajout du paramètre token
  ): Promise<DiverseExerciseResponse> {
    try {
      if (!token) {
        console.warn('⚠️ Aucun token JWT fourni, utilisation des données simulées');
        return this.getMockDiverseExercises(topic, difficulty, count);
      }

      console.log(`🔑 [SERVICE] Token fourni pour ${topic}/${difficulty}: ${token ? 'PRÉSENT' : 'ABSENT'}`);

      const response = await fetch(
        `${this.baseUrl}/exercises/diverse?topic=${encodeURIComponent(topic)}&difficulty=${encodeURIComponent(difficulty)}&count=${count}`,
        {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        }
      );

      if (!response.ok) {
        console.warn(`⚠️ [SERVICE] Réponse HTTP non-OK: ${response.status} ${response.statusText}`);
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      console.log(`✅ [SERVICE] Données récupérées pour ${topic}/${difficulty}:`, data);
      
      // Vérifier la structure des données
      if (!data || typeof data !== 'object') {
        console.warn('⚠️ [SERVICE] Données invalides reçues, utilisation des données simulées');
        return this.getMockDiverseExercises(topic, difficulty, count);
      }

      // Normaliser la structure des exercices
      if (data.exercises && Array.isArray(data.exercises)) {
        const normalizedExercises = data.exercises.map(ex => this.normalizeExercise(ex, topic, difficulty));
        data.exercises = normalizedExercises;
      }

      return data;
    } catch (error) {
      console.error('❌ Erreur lors de la récupération d\'exercices diversifiés:', error);
      
      // Retourner des exercices simulés en cas d'erreur
      return this.getMockDiverseExercises(topic, difficulty, count);
    }
  }

  /**
   * Normalise la structure d'un exercice
   */
  private static normalizeExercise(exercise: any, topic: string, difficulty: string): DiverseExercise {
    return {
      id: exercise.id || `exercise_${Date.now()}_${Math.random()}`,
      type: exercise.type || 'quiz',
      question: exercise.question || exercise.title || `Exercice de ${topic}`,
      options: exercise.options || [],
      correct: exercise.correct || '',
      explanation: exercise.explanation || exercise.description || `Explication pour l'exercice de ${topic}`,
      difficulty: exercise.difficulty || difficulty,
      topic: exercise.topic || topic,
      estimated_time: exercise.estimated_time || 5,
      pairs: exercise.pairs || [],
      items: exercise.items || [],
      categories: exercise.categories || [],
      solutions: exercise.solutions || {},
      blanks: exercise.blanks || [],
      hints: exercise.hints || [],
      title: exercise.title || exercise.question || `Exercice ${topic}`,
      text: exercise.text || '',
      audio_file: exercise.audio_file || '',
      transcript: exercise.transcript || '',
      sentence_parts: exercise.sentence_parts || [],
      correct_order: exercise.correct_order || []
    };
  }

  /**
   * Récupère des exercices par type
   */
  static async getExercisesByType(
    exerciseType: string,
    token: string, // Ajout du paramètre token
    topic?: string,
    difficulty?: string,
    count: number = 5
  ): Promise<{
    success: boolean;
    exercise_type: string;
    exercises: DiverseExercise[];
    total_found: number;
    filters_applied: { topic?: string; difficulty?: string };
  }> {
    try {
      if (!token) {
        console.warn('⚠️ Aucun token JWT fourni, utilisation des données simulées');
        return {
          success: false,
          exercise_type: exerciseType,
          exercises: this.getMockExercisesByType(exerciseType, count),
          total_found: count,
          filters_applied: { topic, difficulty }
        };
      }

      let url = `${this.baseUrl}/exercises/by-type/${exerciseType}?count=${count}`;
      if (topic) url += `&topic=${encodeURIComponent(topic)}`;
      if (difficulty) url += `&difficulty=${encodeURIComponent(difficulty)}`;

      const response = await fetch(url, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      
      // Normaliser les exercices reçus
      if (data.exercises && Array.isArray(data.exercises)) {
        data.exercises = data.exercises.map(ex => this.normalizeExercise(ex, topic || 'general', difficulty || 'intermédiaire'));
      }
      
      return data;
    } catch (error) {
      console.error('❌ Erreur lors de la récupération d\'exercices par type:', error);
      
      // Retourner des exercices simulés en cas d'erreur
      return {
        success: false,
        exercise_type: exerciseType,
        exercises: this.getMockExercisesByType(exerciseType, count),
        total_found: count,
        filters_applied: { topic, difficulty }
      };
    }
  }

  /**
   * Récupère les statistiques de la banque d'exercices
   */
  static async getExerciseStatistics(token: string): Promise<ExerciseStatistics> {
    try {
      if (!token) {
        console.warn('⚠️ Aucun token JWT fourni, utilisation des données simulées');
        return this.getMockExerciseStatistics();
      }

      const response = await fetch(`${this.baseUrl}/exercises/statistics`, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      return data.statistics;
    } catch (error) {
      console.error('❌ Erreur lors de la récupération des statistiques:', error);
      
      // Retourner des statistiques simulées en cas d'erreur
      return this.getMockExerciseStatistics();
    }
  }

  /**
   * Récupère un exercice spécifique par son ID
   */
  static async getExerciseById(exerciseId: string): Promise<DiverseExercise | null> {
    try {
      // Pour l'instant, on simule la récupération par ID
      // Plus tard, on pourra ajouter un endpoint backend pour cela
      const allExercises = await this.getAllExercises();
      return allExercises.find(ex => ex.id === exerciseId) || null;
    } catch (error) {
      console.error('❌ Erreur lors de la récupération de l\'exercice:', error);
      return null;
    }
  }

  /**
   * Récupère tous les exercices disponibles
   */
  static async getAllExercises(): Promise<DiverseExercise[]> {
    try {
      // Récupérer des exercices de chaque type
      const quizExercises = await this.getExercisesByType('quiz', undefined, undefined, undefined, 10);
      const practiceExercises = await this.getExercisesByType('practice', undefined, undefined, undefined, 10);
      const matchingExercises = await this.getExercisesByType('matching', undefined, undefined, undefined, 10);

      return [
        ...quizExercises.exercises,
        ...practiceExercises.exercises,
        ...matchingExercises.exercises
      ];
    } catch (error) {
      console.error('❌ Erreur lors de la récupération de tous les exercices:', error);
      return this.getMockAllExercises();
    }
  }

  // ============================================================================
  // MÉTHODES DE FALLBACK (MOCK DATA)
  // ============================================================================

  private static getMockDiverseExercises(
    topic: string,
    difficulty: string,
    count: number
  ): DiverseExerciseResponse {
    const mockExercises: DiverseExercise[] = [
      {
        id: 'mock_gram_001',
        type: 'quiz',
        question: 'Choisissez l\'article correct : ___ élève est intelligent.',
        options: ['Le', 'La', 'L\'', 'Les'],
        correct: 'L\'',
        explanation: 'Devant une voyelle, on utilise \'L\'\' au lieu de \'Le\' ou \'La\'.',
        difficulty: 'facile',
        topic: 'Articles',
        estimated_time: 2
      },
      {
        id: 'mock_conj_001',
        type: 'quiz',
        question: 'Conjuguez \'être\' à la 1ère personne du singulier au présent :',
        options: ['Je suis', 'Je es', 'Je être', 'Je suis être'],
        correct: 'Je suis',
        explanation: 'Le verbe \'être\' au présent : je suis, tu es, il/elle est...',
        difficulty: 'facile',
        topic: 'Présent du verbe être',
        estimated_time: 2
      },
      {
        id: 'mock_voc_001',
        type: 'matching',
        question: 'Associez les mots de famille avec leurs définitions :',
        pairs: [
          ['père', 'Parent masculin'],
          ['mère', 'Parent féminin'],
          ['frère', 'Enfant masculin de mêmes parents'],
          ['sœur', 'Enfant féminin de mêmes parents']
        ],
        explanation: 'La famille nucléaire comprend les parents et leurs enfants.',
        difficulty: 'facile',
        topic: 'Vocabulaire de la famille',
        estimated_time: 4
      },
      {
        id: 'mock_comp_001',
        type: 'reading',
        question: 'Lisez le texte et répondez aux questions de compréhension.',
        text: 'La France est un pays d\'Europe de l\'Ouest...',
        explanation: 'Compréhension de texte sur la géographie française.',
        difficulty: 'intermédiaire',
        topic: 'Compréhension écrite',
        estimated_time: 8
      },
      {
        id: 'mock_prac_001',
        type: 'practice',
        question: 'Transformez les phrases en utilisant la voix passive.',
        explanation: 'Pratique de la transformation active-passive.',
        difficulty: 'avancé',
        topic: 'Voix passive',
        estimated_time: 6
      }
    ];

    // Filtrer par difficulté si spécifiée
    let filteredExercises = mockExercises;
    if (difficulty && difficulty !== 'tous') {
      filteredExercises = mockExercises.filter(ex => ex.difficulty === difficulty);
    }

    // Limiter le nombre d'exercices
    const limitedExercises = filteredExercises.slice(0, count);

    return {
      success: true,
      exercises: limitedExercises,
      total_found: limitedExercises.length,
      topic,
      difficulty,
      avoided_repetition: true
    };
  }

  private static getMockExercisesByType(type: string, count: number): DiverseExercise[] {
    const mockExercises: Record<string, DiverseExercise[]> = {
      quiz: [
        {
          id: 'mock_quiz_001',
          type: 'quiz',
          question: 'Quelle est la forme correcte du verbe \'aller\' au présent ?',
          options: ['Je vais', 'Je va', 'Je aller', 'Je allons'],
          correct: 'Je vais',
          explanation: 'Le verbe \'aller\' au présent : je vais, tu vas, il/elle va...',
          difficulty: 'facile',
          topic: 'Conjugaison',
          estimated_time: 2
        },
        {
          id: 'mock_quiz_002',
          type: 'quiz',
          question: 'Choisissez la bonne forme de l\'adjectif : Les ___ (beau) maisons.',
          options: ['beau', 'beaux', 'belle', 'belles'],
          correct: 'belles',
          explanation: 'Maisons est féminin pluriel, donc l\'adjectif s\'accorde en genre et en nombre.',
          difficulty: 'intermédiaire',
          topic: 'Accord des adjectifs',
          estimated_time: 3
        }
      ],
      practice: [
        {
          id: 'mock_practice_001',
          type: 'practice',
          question: 'Transformez en accordant : \'Un petit garçon et une petite fille\'',
          explanation: 'Au pluriel : \'petit\' → \'petits\' (masculin), \'petite\' → \'petites\' (féminin)',
          difficulty: 'avancé',
          topic: 'Accord des adjectifs',
          estimated_time: 5
        },
        {
          id: 'mock_practice_002',
          type: 'practice',
          question: 'Conjuguez le verbe \'finir\' au présent de l\'indicatif.',
          explanation: 'Le verbe finir appartient au 2ème groupe, il se conjugue avec -is, -is, -it...',
          difficulty: 'intermédiaire',
          topic: 'Conjugaison',
          estimated_time: 4
        }
      ],
      matching: [
        {
          id: 'mock_matching_001',
          type: 'matching',
          question: 'Associez les verbes avec leurs temps :',
          pairs: [
            ['Je vais', 'Présent'],
            ['J\'irai', 'Futur'],
            ['J\'allais', 'Imparfait']
          ],
          explanation: 'Les temps verbaux expriment le moment de l\'action.',
          difficulty: 'intermédiaire',
          topic: 'Temps verbaux',
          estimated_time: 4
        },
        {
          id: 'mock_matching_002',
          type: 'matching',
          question: 'Associez les mots avec leurs synonymes :',
          pairs: [
            ['grand', 'immense'],
            ['petit', 'minuscule'],
            ['rapide', 'vite']
          ],
          explanation: 'Les synonymes sont des mots de sens proche.',
          difficulty: 'facile',
          topic: 'Vocabulaire',
          estimated_time: 3
        }
      ],
      reading: [
        {
          id: 'mock_reading_001',
          type: 'reading',
          question: 'Lisez le texte et répondez aux questions.',
          text: 'Paris est la capitale de la France. Cette ville magnifique est connue dans le monde entier...',
          explanation: 'Compréhension de texte sur Paris.',
          difficulty: 'facile',
          topic: 'Compréhension écrite',
          estimated_time: 7
        }
      ]
    };

    const exercises = mockExercises[type] || [];
    return exercises.slice(0, count);
  }

  private static getMockExerciseStatistics(): ExerciseStatistics {
    return {
      total_exercises: 25,
      by_category: {
        grammar: 8,
        conjugation: 7,
        vocabulary: 5,
        comprehension: 3,
        interactive: 2
      },
      by_difficulty: {
        facile: 12,
        intermédiaire: 8,
        avancé: 5
      },
      categories: ['grammar', 'conjugation', 'vocabulary', 'comprehension', 'interactive'],
      difficulties: ['facile', 'intermédiaire', 'avancé']
    };
  }

  private static getMockAllExercises(): DiverseExercise[] {
    return [
      ...this.getMockExercisesByType('quiz', 8),
      ...this.getMockExercisesByType('practice', 6),
      ...this.getMockExercisesByType('matching', 5),
      ...this.getMockExercisesByType('reading', 3)
    ];
  }
}
