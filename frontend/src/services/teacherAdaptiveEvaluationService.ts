import { apiClient } from '../utils/api';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// ============================================================================
// INTERFACES POUR L'ÉVALUATION ADAPTATIVE DES ENSEIGNANTS
// ============================================================================

export interface AdaptiveTestCreate {
  title: string;
  subject: string;
  description?: string;
  difficulty_range?: { min: number; max: number };
  question_pool_size?: number;
  adaptation_algorithm?: 'irt' | 'ml' | 'expert';
  is_active?: boolean;
  questions?: AdaptiveQuestionCreate[];
}

export interface AdaptiveQuestionCreate {
  question_text: string;
  question_type: 'multiple_choice' | 'true_false' | 'fill_blank' | 'essay';
  options?: any;
  correct_answer: string;
  explanation?: string;
  difficulty_level: number;
  subject?: string;
  topic?: string;
  tags?: string[];
}

export interface TestAssignment {
  test_id: number;
  class_ids?: number[];
  student_ids?: number[];
  due_date?: string;
}

export interface TeacherTest {
  id: number;
  title: string;
  subject: string;
  description: string;
  difficulty_range: { min: number; max: number };
  estimated_duration: number;
  is_active: boolean;
  created_at: string;
  statistics: {
    assignments: {
      total: number;
      classes: number;
      individuals: number;
    };
    performance: {
      total_students: number;
      completed_students: number;
      in_progress_students: number;
      average_score: number;
    };
  };
}

export interface TestResults {
  test: {
    id: number;
    title: string;
    subject: string;
  };
  statistics: {
    total_students: number;
    completed_students: number;
    in_progress_students: number;
    not_started_students: number;
    average_score: number;
    avg_response_time: number;
    avg_difficulty_adjustments: number;
  };
  student_performances: Array<{
    student_id: number;
    student_name: string;
    email: string;
    class_name?: string;
    status: string;
    final_score: number;
    questions_answered: number;
    correct_answers: number;
    completion_time?: string;
    difficulty_adjustments: number;
    start_time?: string;
  }>;
  question_analysis: Array<{
    question_text: string;
    difficulty_level: number;
    times_answered: number;
    success_rate: number;
    avg_response_time: number;
  }>;
}

export interface ClassAnalytics {
  class: {
    id: number;
    name: string;
  };
  statistics: {
    total_students: number;
    total_tests: number;
    class_average_score: number;
    avg_response_time: number;
    total_difficulty_adjustments: number;
  };
  subject_performance: Array<{
    subject: string;
    students_count: number;
    average_score: number;
    tests_count: number;
  }>;
  student_progress: Array<{
    student_name: string;
    email: string;
    tests_completed: number;
    average_score: number;
    avg_response_time: number;
    total_adjustments: number;
    last_activity?: string;
  }>;
}

export interface TeacherDashboardOverview {
  overview: {
    total_tests: number;
    total_assignments: number;
    total_students: number;
    overall_average_score: number;
  };
  recent_tests: Array<{
    id: number;
    title: string;
    subject: string;
    created_at: string;
    assignments_count: number;
    students_count: number;
  }>;
  subject_performance: Array<{
    subject: string;
    tests_count: number;
    students_count: number;
    average_score: number;
  }>;
}

// ============================================================================
// SERVICE D'ÉVALUATION ADAPTATIVE POUR ENSEIGNANTS
// ============================================================================

class TeacherAdaptiveEvaluationService {
  private async makeAuthenticatedRequest(endpoint: string, method: string = 'GET', data?: any): Promise<any> {
    try {
      const token = localStorage.getItem('najah_token');
      if (!token) {
        throw new Error('Token d\'authentification non trouvé');
      }

      const response = await fetch(`${API_BASE_URL}${endpoint}`, {
        method,
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        body: data ? JSON.stringify(data) : undefined,
      });

      if (!response.ok) {
        if (response.status === 401) {
          throw new Error('Token expiré ou invalide');
        }
        throw new Error(`Erreur HTTP: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Erreur lors de la requête:', error);
      throw error;
    }
  }

  // ============================================================================
  // CRÉATION ET GESTION DES TESTS
  // ============================================================================

  /**
   * Créer un nouveau test adaptatif
   */
  async createAdaptiveTest(testData: AdaptiveTestCreate): Promise<any> {
    try {
      console.log('🔄 Création d\'un test adaptatif...');
      const result = await this.makeAuthenticatedRequest('/api/v1/teacher-adaptive-evaluation/tests/create', 'POST', testData);
      console.log('✅ Test adaptatif créé:', result);
      return result;
    } catch (error) {
      console.error('❌ Erreur lors de la création du test:', error);
      throw error;
    }
  }

  /**
   * Assigner un test à des classes ou étudiants
   */
  async assignTestToTargets(testId: number, assignmentData: TestAssignment): Promise<any> {
    try {
      console.log(`🔄 Assignation du test ${testId}...`);
      const result = await this.makeAuthenticatedRequest(`/api/v1/teacher-adaptive-evaluation/tests/${testId}/assign`, 'POST', assignmentData);
      console.log('✅ Test assigné:', result);
      return result;
    } catch (error) {
      console.error('❌ Erreur lors de l\'assignation:', error);
      throw error;
    }
  }

  /**
   * Récupérer tous les tests d'un enseignant
   */
  async getTeacherTests(teacherId: number): Promise<{ success: boolean; tests: TeacherTest[]; total_tests: number }> {
    try {
      console.log(`🔄 Récupération des tests de l'enseignant ${teacherId}...`);
      
      // Utiliser l'endpoint correct
      const result = await this.makeAuthenticatedRequest(`/api/v1/teacher-adaptive-evaluation/tests/teacher/${teacherId}`);
      console.log('✅ Tests récupérés (brut):', result);
      console.log('🔍 Service: Réponse complète de l\'API:', JSON.stringify(result, null, 2));
      console.log('🔍 Service: Type de result:', typeof result);
      console.log('🔍 Service: Clés de result:', Object.keys(result || {}));
      console.log('🔍 Service: result.tests:', result.tests);
      console.log('🔍 Service: Type de result.tests:', typeof result.tests);
      console.log('🔍 Service: Longueur de result.tests:', result.tests?.length);
      
      // Valider et nettoyer les données reçues
      if (result && result.success && result.tests) {
        console.log('🔍 Service: Validation des tests...');
        
        // Vérifier si les tests sont des tuples (arrays) au lieu d'objets
        if (Array.isArray(result.tests) && result.tests.length > 0) {
          const firstTest = result.tests[0];
          console.log('🔍 Service: Premier test:', firstTest);
          console.log('🔍 Service: Type du premier test:', typeof firstTest);
          console.log('🔍 Service: Est-ce un array?', Array.isArray(firstTest));
          
          if (Array.isArray(firstTest)) {
            console.warn('⚠️ Service: Les tests sont des tuples (arrays) au lieu d\'objets !');
            console.warn('⚠️ Service: Structure attendue: {id: 1, title: "..."}');
            console.warn('⚠️ Service: Structure reçue:', firstTest);
          }
        }
        
        result.tests = result.tests.map(test => this.validateTestData(test));
        console.log('🔍 Service: Tests après validation:', result.tests);
      } else {
        console.warn('⚠️ Service: Pas de tests à valider');
      }
      
      return result;
    } catch (error) {
      console.error('❌ Erreur lors de la récupération des tests:', error);
      throw error;
    }
  }

  /**
   * Valider et nettoyer les données d'un test
   */
  private validateTestData(test: any): TeacherTest {
    console.log('🔍 Service: Validation du test brut:', test);
    console.log('🔍 Service: Type du test:', typeof test);
    console.log('🔍 Service: Clés du test:', Object.keys(test || {}));
    
    const validatedTest = {
      id: test.id || 0,
      title: test.title || 'Sans titre',
      subject: test.subject || 'Matière non spécifiée',
      description: test.description || 'Aucune description',
      difficulty_range: {
        min: test.difficulty_range?.min || test.difficulty_range_min || 1,
        max: test.difficulty_range?.max || test.difficulty_range_max || 10
      },
      estimated_duration: test.estimated_duration || 30,
      is_active: test.is_active !== undefined ? test.is_active : true,
      created_at: test.created_at || new Date().toISOString(),
      statistics: {
        assignments: {
          total: test.statistics?.assignments?.total || 0,
          classes: test.statistics?.assignments?.classes || 0,
          individuals: test.statistics?.assignments?.individuals || 0
        },
        performance: {
          total_students: test.statistics?.performance?.total_students || 0,
          completed_students: test.statistics?.performance?.completed_students || 0,
          in_progress_students: test.statistics?.performance?.in_progress_students || 0,
          average_score: test.statistics?.performance?.average_score || 0
        }
      }
    };
    
    console.log('🔍 Service: Test validé:', validatedTest);
    return validatedTest;
  }

  // ============================================================================
  // RÉSULTATS ET ANALYTICS
  // ============================================================================

  /**
   * Récupérer les résultats détaillés d'un test
   */
  async getTestResults(testId: number): Promise<TestResults> {
    try {
      console.log(`🔄 Récupération des résultats du test ${testId}...`);
      const result = await this.makeAuthenticatedRequest(`/api/v1/teacher-adaptive-evaluation/tests/${testId}/results`);
      console.log('✅ Résultats récupérés:', result);
      return result;
    } catch (error) {
      console.error('❌ Erreur lors de la récupération des résultats:', error);
      throw error;
    }
  }

  /**
   * Récupérer les analytics d'une classe
   */
  async getClassAnalytics(classId: number): Promise<ClassAnalytics> {
    try {
      console.log(`🔄 Récupération des analytics de la classe ${classId}...`);
      const result = await this.makeAuthenticatedRequest(`/api/v1/teacher-adaptive-evaluation/analytics/class/${classId}`);
      console.log('✅ Analytics de classe récupérés:', result);
      return result;
    } catch (error) {
      console.error('❌ Erreur lors de la récupération des analytics:', error);
      throw error;
    }
  }

  /**
   * Récupérer la vue d'ensemble du dashboard enseignant
   */
  async getTeacherDashboardOverview(): Promise<TeacherDashboardOverview> {
    try {
      console.log('🔄 Récupération du dashboard enseignant...');
      const result = await this.makeAuthenticatedRequest('/api/v1/teacher-adaptive-evaluation/dashboard/overview');
      console.log('✅ Dashboard récupéré:', result);
      return result;
    } catch (error) {
      console.error('❌ Erreur lors de la récupération du dashboard:', error);
      throw error;
    }
  }

  /**
   * Récupérer les classes de l'enseignant
   */
  async getTeacherClasses(teacherId: number): Promise<Array<{
    id: number;
    name: string;
    student_count: number;
  }>> {
    try {
      console.log(`🔄 Récupération des classes de l'enseignant ${teacherId}...`);
      const result = await this.makeAuthenticatedRequest(`/api/v1/teacher/classes/`);
      console.log('✅ Classes récupérées:', result);
      
      if (Array.isArray(result)) {
        return result.map((cls: any) => ({
          id: cls.id,
          name: cls.name,
          student_count: cls.student_count || 0
        }));
      }
      
      return [];
    } catch (error) {
      console.error('❌ Erreur lors de la récupération des classes:', error);
      return [];
    }
  }

  /**
   * Récupérer les étudiants de l'enseignant
   */
  async getTeacherStudents(teacherId: number): Promise<Array<{
    id: number;
    first_name: string;
    last_name: string;
    email: string;
    class_name: string;
  }>> {
    try {
      console.log(`🔄 Récupération des étudiants de l'enseignant ${teacherId}...`);
      const result = await this.makeAuthenticatedRequest(`/api/v1/assignments/teacher/targets`);
      console.log('✅ Étudiants récupérés:', result);
      
      if (Array.isArray(result)) {
        return result.map((student: any) => ({
          id: student.id,
          first_name: student.name.split(' ')[0] || '',
          last_name: student.name.split(' ').slice(1).join(' ') || '',
          email: student.email || '',
          class_name: student.class_name || 'Classe non spécifiée'
        }));
      }
      
      return [];
    } catch (error) {
      console.error('❌ Erreur lors de la récupération des étudiants:', error);
      return [];
    }
  }

  // ============================================================================
  // UTILITAIRES
  // ============================================================================

  /**
   * Générer des questions d'exemple pour un test
   */
  generateSampleQuestions(subject: string, count: number = 5): AdaptiveQuestionCreate[] {
    const questions: AdaptiveQuestionCreate[] = [];
    
    const questionTemplates = {
      'Mathématiques': [
        {
          question_text: 'Quelle est la solution de l\'équation 2x + 5 = 13 ?',
          question_type: 'multiple_choice' as const,
          options: ['x = 4', 'x = 5', 'x = 6', 'x = 7'],
          correct_answer: 'x = 4',
          explanation: '2x + 5 = 13 → 2x = 8 → x = 4',
          difficulty_level: 3
        },
        {
          question_text: 'Calculer l\'aire d\'un rectangle de longueur 8 et largeur 6',
          question_type: 'fill_blank' as const,
          correct_answer: '48',
          explanation: 'Aire = longueur × largeur = 8 × 6 = 48',
          difficulty_level: 2
        }
      ],
      'Français': [
        {
          question_text: 'Quel est le genre du mot "table" ?',
          question_type: 'multiple_choice' as const,
          options: ['Masculin', 'Féminin', 'Les deux', 'Aucun'],
          correct_answer: 'Féminin',
          explanation: 'Le mot "table" est un nom féminin',
          difficulty_level: 1
        },
        {
          question_text: 'Conjuguez le verbe "être" à la première personne du singulier au présent',
          question_type: 'fill_blank' as const,
          correct_answer: 'suis',
          explanation: 'Je suis, tu es, il/elle est...',
          difficulty_level: 2
        }
      ],
      'Histoire': [
        {
          question_text: 'En quelle année a eu lieu la Révolution française ?',
          question_type: 'multiple_choice' as const,
          options: ['1789', '1799', '1809', '1819'],
          correct_answer: '1789',
          explanation: 'La Révolution française a commencé en 1789',
          difficulty_level: 3
        }
      ]
    };

    const templates = questionTemplates[subject as keyof typeof questionTemplates] || questionTemplates['Mathématiques'];
    
    for (let i = 0; i < count; i++) {
      const template = templates[i % templates.length];
      questions.push({
        ...template,
        question_text: `${template.question_text} (Question ${i + 1})`,
        difficulty_level: Math.min(10, Math.max(1, template.difficulty_level + (i % 3)))
      });
    }

    return questions;
  }

  /**
   * Valider les données de création de test
   */
  validateTestData(testData: AdaptiveTestCreate): { isValid: boolean; errors: string[] } {
    const errors: string[] = [];

    if (!testData.title || testData.title.trim().length < 3) {
      errors.push('Le titre doit contenir au moins 3 caractères');
    }

    if (!testData.subject || testData.subject.trim().length === 0) {
      errors.push('La matière est obligatoire');
    }

    if (testData.questions && testData.questions.length > 0) {
      testData.questions.forEach((question, index) => {
        if (!question.question_text || question.question_text.trim().length < 10) {
          errors.push(`Question ${index + 1}: Le texte de la question doit contenir au moins 10 caractères`);
        }
        if (!question.correct_answer || question.correct_answer.trim().length === 0) {
          errors.push(`Question ${index + 1}: La réponse correcte est obligatoire`);
        }
        if (question.difficulty_level < 1 || question.difficulty_level > 10) {
          errors.push(`Question ${index + 1}: Le niveau de difficulté doit être entre 1 et 10`);
        }
      });
    }

    return {
      isValid: errors.length === 0,
      errors
    };
  }
}

export const teacherAdaptiveEvaluationService = new TeacherAdaptiveEvaluationService();
export default teacherAdaptiveEvaluationService;



