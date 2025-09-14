import { apiClient } from '../api/config';

export interface CognitiveProfile {
  student_id: number;
  learning_style: {
    primary_style: string;
    secondary_style?: string;
    confidence_score: number;
    evidence: string[];
  };
  cognitive_abilities: {
    memory_strength: number;
    attention_span: number;
    problem_solving: number;
    visual_processing: number;
    auditory_processing: number;
  };
  learning_preferences: {
    preferred_content_types: string[];
    preferred_difficulty: string;
    preferred_pace: string;
    preferred_environment: string;
  };
  strengths: string[];
  areas_for_improvement: string[];
  recommendations: string[];
  last_updated: string;
}

export interface AdaptiveQuiz {
  quiz_id: number;
  title: string;
  subject: string;
  difficulty: string;
  question_count: number;
  estimated_duration: number;
  adaptation_reason: string;
  questions: QuizQuestion[];
}

export interface QuizQuestion {
  id: number;
  question_text: string;
  question_type: 'multiple_choice' | 'true_false' | 'fill_blank' | 'matching';
  options?: string[];
  correct_answer: string | string[];
  explanation?: string;
  difficulty: 'easy' | 'medium' | 'hard';
  subject: string;
  topic: string;
}

export interface GapAnalysis {
  student_id: number;
  subject: string;
  analysis_date: string;
  identified_gaps: LearningGap[];
  remediation_plan: RemediationStep[];
  estimated_completion_time: number;
  priority_level: 'high' | 'medium' | 'low';
  overall_gap_score?: number;
  recommendations?: string[];
}

export interface LearningGap {
  topic: string;
  current_level: string;
  target_level: string;
  gap_size: 'small' | 'medium' | 'large';
  impact_score: number;
  evidence: string[];
  recommended_resources: string[];
  estimated_time_to_close?: string;
}

export interface RemediationStep {
  step_number: number;
  topic: string;
  learning_objective: string;
  content_type: 'video' | 'reading' | 'exercise' | 'quiz' | 'exercices' | 'vocabulaire' | 'conjugaison';
  estimated_duration: number;
  prerequisites: string[];
  resources: string[];
}

export interface RemediationPlan {
  student_id: number;
  subject: string;
  created_date: string;
  steps: RemediationStep[];
  total_duration: number;
  progress: number;
  current_step: number;
}

export class CognitiveDiagnosticService {
  private static API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

  /**
   * Récupère le profil cognitif complet d'un étudiant
   */
  static async getCognitiveProfile(studentId: number, token: string): Promise<CognitiveProfile> {
    try {
      const response = await fetch(`${this.API_BASE_URL}/api/v1/cognitive_diagnostic/student/${studentId}/cognitive-profile`, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });

      if (!response.ok) {
        throw new Error(`Erreur lors de la récupération du profil cognitif: ${response.status}`);
      }

      const data = await response.json();
      return data;
    } catch (error) {
      console.error('Erreur getCognitiveProfile:', error);
      throw error;
    }
  }

  /**
   * Retourne un profil cognitif par défaut
   */
  private static getDefaultCognitiveProfile(studentId: number): CognitiveProfile {
    return {
      student_id: studentId,
      learning_style: {
        primary_style: 'Auditif',
        confidence_score: 0.8,
        evidence: ['Tests de style d\'apprentissage', 'Analyse des performances']
      },
      cognitive_abilities: {
        memory_strength: 0.7,
        attention_span: 0.6,
        problem_solving: 0.8,
        visual_processing: 0.5,
        auditory_processing: 0.9
      },
      learning_preferences: {
        preferred_content_types: ['audio', 'vidéo', 'interactif'],
        preferred_difficulty: 'facile',
        preferred_pace: 'modéré',
        preferred_environment: 'calme'
      },
      strengths: ['Compréhension orale', 'Mémorisation des sons', 'Résolution de problèmes'],
      areas_for_improvement: ['Grammaire', 'Conjugaison', 'Vocabulaire', 'Expression écrite'],
      recommendations: ['Pratiquer la grammaire avec des exercices audio', 'Utiliser des flashcards pour le vocabulaire'],
      last_updated: new Date().toISOString()
    };
  }

  /**
   * Génère un quiz adaptatif basé sur le profil de l'étudiant
   */
  static async generateAdaptiveQuiz(
    studentId: number,
    subject: string,
    questionCount: number = 10,
    difficultyPreference: string = 'auto',
    token: string
  ): Promise<AdaptiveQuiz> {
    try {
      const response = await fetch(`${this.API_BASE_URL}/api/v1/adaptive_quizzes/generate-test/${studentId}?subject=${subject}&question_count=${questionCount}&difficulty_preference=${difficultyPreference}`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });

      if (!response.ok) {
        throw new Error(`Erreur lors de la génération du quiz: ${response.status}`);
      }

      const data = await response.json();
      return data;
    } catch (error) {
      console.error('Erreur generateAdaptiveQuiz:', error);
      throw error;
    }
  }

  /**
   * Analyse les lacunes d'apprentissage d'un étudiant
   */
  static async analyzeLearningGaps(
    studentId: number,
    subject: string,
    token: string
  ): Promise<GapAnalysis> {
    try {
      const response = await fetch(`${this.API_BASE_URL}/api/v1/gap_analysis/student/${studentId}/analyze`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          subject: subject,
          analysis_depth: 'comprehensive'
        })
      });

      if (!response.ok) {
        throw new Error(`Erreur lors de l'analyse des lacunes: ${response.status}`);
      }

      const data = await response.json();
      return data;
    } catch (error) {
      console.error('Erreur analyzeLearningGaps:', error);
      throw error;
    }
  }

  /**
   * Génère un plan de remédiation personnalisé
   */
  static async generateRemediationPlan(
    studentId: number,
    subject: string,
    token: string
  ): Promise<RemediationPlan> {
    try {
      const response = await fetch(`${this.API_BASE_URL}/api/v1/remediation/student/${studentId}/plan`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          subject: subject,
          include_exercises: true,
          include_assessments: true
        })
      });

      if (!response.ok) {
        throw new Error(`Erreur lors de la génération du plan de remédiation: ${response.status}`);
      }

      const data = await response.json();
      return data;
    } catch (error) {
      console.error('Erreur generateRemediationPlan:', error);
      throw error;
    }
  }

  /**
   * Soumet les résultats d'un quiz pour analyse adaptative
   */
  static async submitQuizResults(
    quizId: number,
    studentId: number,
    answers: Record<number, string | string[]>,
    timeSpent: number,
    token: string
  ): Promise<{
    score: number;
    feedback: string;
    recommendations: string[];
    next_difficulty: string;
  }> {
    try {
      const response = await fetch(`${this.API_BASE_URL}/api/v1/adaptive_quizzes/${quizId}/submit`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          student_id: studentId,
          answers: answers,
          time_spent: timeSpent,
          submission_timestamp: new Date().toISOString()
        })
      });

      if (!response.ok) {
        throw new Error(`Erreur lors de la soumission des résultats: ${response.status}`);
      }

      const data = await response.json();
      return data;
    } catch (error) {
      console.error('Erreur submitQuizResults:', error);
      throw error;
    }
  }

  /**
   * Met à jour le profil cognitif basé sur les nouvelles données
   */
  static async updateCognitiveProfile(
    studentId: number,
    newData: Partial<CognitiveProfile>,
    token: string
  ): Promise<CognitiveProfile> {
    try {
      const response = await fetch(`${this.API_BASE_URL}/api/v1/cognitive_diagnostic/student/${studentId}/update`, {
        method: 'PUT',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(newData)
      });

      if (!response.ok) {
        throw new Error(`Erreur lors de la mise à jour du profil: ${response.status}`);
      }

      const data = await response.json();
      return data;
    } catch (error) {
      console.error('Erreur updateCognitiveProfile:', error);
      throw error;
    }
  }

  /**
   * Récupère l'historique des quiz adaptatifs d'un étudiant
   */
  static async getQuizHistory(
    studentId: number,
    subject?: string,
    limit: number = 20,
    token: string
  ): Promise<{
    quizzes: Array<{
      id: number;
      title: string;
      subject: string;
      difficulty: string;
      score: number;
      completed_at: string;
      adaptation_level: string;
    }>;
    performance_trend: Array<{
      date: string;
      average_score: number;
      difficulty_level: string;
    }>;
  }> {
    try {
      const url = new URL(`${this.API_BASE_URL}/api/v1/adaptive_quizzes/student/${studentId}/history`);
      if (subject) url.searchParams.append('subject', subject);
      url.searchParams.append('limit', limit.toString());

      const response = await fetch(url.toString(), {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });

      if (!response.ok) {
        throw new Error(`Erreur lors de la récupération de l'historique: ${response.status}`);
      }

      const data = await response.json();
      return data;
    } catch (error) {
      console.error('Erreur getQuizHistory:', error);
      throw error;
    }
  }

  /**
   * Retourne une analyse des lacunes par défaut
   */
  private static getDefaultGapAnalysis(studentId: number, subject: string): GapAnalysis {
    return {
      student_id: studentId,
      subject: subject,
      analysis_date: new Date().toISOString(),
      priority_level: 'medium',
      overall_gap_score: 0.6,
      estimated_completion_time: 45,
      identified_gaps: [
        {
          topic: 'Grammaire de base',
          current_level: 'A1',
          target_level: 'A2',
          gap_size: 'medium',
          impact_score: 7,
          evidence: ['Tests de grammaire', 'Exercices de conjugaison'],
          recommended_resources: ['Cours vidéo', 'Exercices interactifs', 'Quiz de pratique'],
          estimated_time_to_close: '2-3 semaines'
        },
        {
          topic: 'Vocabulaire quotidien',
          current_level: 'A1',
          target_level: 'A2',
          gap_size: 'large',
          impact_score: 8,
          evidence: ['Tests de vocabulaire', 'Compréhension écrite'],
          recommended_resources: ['Listes de mots', 'Flashcards', 'Lectures guidées'],
          estimated_time_to_close: '3-4 semaines'
        },
        {
          topic: 'Conjugaison des verbes',
          current_level: 'A1',
          target_level: 'A2',
          gap_size: 'medium',
          impact_score: 6,
          evidence: ['Tests de conjugaison', 'Exercices pratiques'],
          recommended_resources: ['Tableaux de conjugaison', 'Exercices interactifs', 'Tests de validation'],
          estimated_time_to_close: '2-3 semaines'
        }
      ],
      remediation_plan: [],
      recommendations: [
        'Pratiquer la grammaire avec des exercices quotidiens',
        'Utiliser des flashcards pour enrichir le vocabulaire',
        'S\'entraîner à la conjugaison avec des exercices interactifs'
      ]
    };
  }

  /**
   * Retourne un plan de remédiation par défaut
   */
  private static getDefaultRemediationPlan(studentId: number, subject: string): RemediationPlan {
    return {
      student_id: studentId,
      subject: subject,
      created_date: new Date().toISOString(),
      current_step: 1,
      progress: 0,
      total_duration: 115, // 30 + 45 + 40
      steps: [
        {
          step_number: 1,
          topic: 'Grammaire de base',
          learning_objective: 'Maîtriser les articles et la conjugaison du présent',
          content_type: 'exercices',
          estimated_duration: 30,
          prerequisites: [],
          resources: ['Exercices de grammaire', 'Vidéos explicatives', 'Quiz de validation']
        },
        {
          step_number: 2,
          topic: 'Vocabulaire quotidien',
          learning_objective: 'Enrichir le vocabulaire de base (famille, travail, loisirs)',
          content_type: 'vocabulaire',
          estimated_duration: 45,
          prerequisites: ['Grammaire de base'],
          resources: ['Listes de mots thématiques', 'Flashcards interactives', 'Exercices de mémorisation']
        },
        {
          step_number: 3,
          topic: 'Conjugaison des verbes',
          learning_objective: 'Maîtriser la conjugaison des verbes du 1er groupe au présent',
          content_type: 'conjugaison',
          estimated_duration: 40,
          prerequisites: ['Grammaire de base'],
          resources: ['Tableaux de conjugaison', 'Exercices pratiques', 'Tests de validation']
        }
      ]
    };
  }
}
