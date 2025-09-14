import { 
  AdaptiveTest, 
  CreateTestData, 
  AssignmentData, 
  TestResponse,
  Class,
  User,
  TestAttempt,
  CompetencyAnalysis,
  AIAnalysisResult,
  StudentActivity,
  TestPerformance
} from '../types/adaptiveEvaluation';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

class AdaptiveEvaluationService {
  private async request<T>(
    endpoint: string, 
    options: RequestInit = {}
  ): Promise<T> {
    const token = localStorage.getItem('najah_token');
    
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
        ...options.headers,
      },
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({}));
      throw new Error(error.detail || `HTTP error! status: ${response.status}`);
    }

    return response.json();
  }

  // ============================================================================
  // TESTS ADAPTATIFS
  // ============================================================================

  async createTest(testData: CreateTestData): Promise<{ success: boolean; test: AdaptiveTest }> {
    return this.request('/api/v1/adaptive-evaluation/tests/', {
      method: 'POST',
      body: JSON.stringify(testData),
    });
  }

  async getAllTests(): Promise<{ success: boolean; tests: AdaptiveTest[] }> {
    return this.request('/api/v1/adaptive-evaluation/tests/');
  }

  // Nouvelle méthode simple
  async getAllTestsSimple(): Promise<{ tests: any[]; count: number }> {
    return this.request('/api/v1/adaptive-evaluation/tests/simple/');
  }

  async getTestDetails(testId: number): Promise<{ success: boolean; test: AdaptiveTest }> {
    return this.request(`/api/v1/adaptive-evaluation/tests/${testId}`);
  }

  // Récupérer tous les tests (actifs et inactifs)
  async getAllTestsIncludingInactive(): Promise<ApiResponse<AdaptiveTest[]>> {
    try {
      const response = await this.request('/api/v1/adaptive-evaluation/tests/all/');
      return response;
    } catch (error) {
      console.error('Erreur lors de la récupération de tous les tests:', error);
      return { success: false, error: 'Erreur lors de la récupération des tests' };
    }
  }

  // Activer un test
  async activateTest(testId: number): Promise<ApiResponse<{ message: string }>> {
    try {
      const response = await this.request(`/api/v1/adaptive-evaluation/tests/${testId}/activate/`, {
        method: 'PATCH',
        body: JSON.stringify({ is_active: true })
      });
      return response;
    } catch (error) {
      console.error('Erreur lors de l\'activation du test:', error);
      return { success: false, error: 'Erreur lors de l\'activation du test' };
    }
  }

  // Désactiver un test
  async deactivateTest(testId: number): Promise<ApiResponse<{ message: string }>> {
    try {
      const response = await this.request(`/api/v1/adaptive-evaluation/tests/${testId}/deactivate/`, {
        method: 'PATCH',
        body: JSON.stringify({ is_active: false })
      });
      return response;
    } catch (error) {
      console.error('Erreur lors de la désactivation du test:', error);
      return { success: false, error: 'Erreur lors de la désactivation du test' };
    }
  }

  // ============================================================================
  // ASSIGNATIONS
  // ============================================================================

  async assignTest(testId: number, assignmentData: AssignmentData): Promise<{
    success: boolean;
    message: string;
    assignments: any[];
  }> {
    return this.request(`/api/v1/adaptive-evaluation/tests/${testId}/assign`, {
      method: 'POST',
      body: JSON.stringify(assignmentData),
    });
  }

  // ============================================================================
  // ÉTUDIANTS
  // ============================================================================

  async getStudentAssignedTests(studentId: number): Promise<{ success: boolean; tests: AdaptiveTest[] }> {
    return this.request(`/api/v1/adaptive-evaluation/student/${studentId}/assigned`);
  }

  // ============================================================================
  // TENTATIVES DE TEST
  // ============================================================================

  async startTest(testId: number): Promise<{ success: boolean; attempt_id: number; message: string }> {
    return this.request(`/api/v1/adaptive-evaluation/tests/${testId}/start`, {
      method: 'POST',
    });
  }

  async submitTestAttempt(attemptId: number, responses: TestResponse[]): Promise<{
    success: boolean;
    message: string;
    score: number;
    max_score: number;
    percentage: number;
  }> {
    return this.request(`/api/v1/adaptive-evaluation/attempts/${attemptId}/submit`, {
      method: 'POST',
      body: JSON.stringify(responses),
    });
  }

  // ============================================================================
  // ANALYSE DES COMPÉTENCES
  // ============================================================================

  async getCompetencyAnalysis(attemptId: number): Promise<{
    success: boolean;
    attempt_id: number;
    competencies: CompetencyAnalysis[];
  }> {
    return this.request(`/api/v1/adaptive-evaluation/attempts/${attemptId}/analysis`);
  }

  // ============================================================================
  // ANALYSE IA DES COMPÉTENCES
  // ============================================================================

  async analyzeCompetenciesWithAI(attemptId: number): Promise<AIAnalysisResult> {
    // Simulation de l'analyse IA - à remplacer par un vrai appel API
    return new Promise((resolve) => {
      setTimeout(() => {
        resolve({
          competencies: [
            {
              id: 1,
              attempt_id: attemptId,
              student_id: 1,
              test_id: 1,
              competency_name: "Grammaire",
              competency_level: 75,
              confidence_score: 85,
              ai_recommendations: "L'étudiant maîtrise bien la grammaire de base. Recommandation : pratiquer les temps composés.",
              analyzed_at: new Date().toISOString()
            },
            {
              id: 2,
              attempt_id: attemptId,
              student_id: 1,
              test_id: 1,
              competency_name: "Conjugaison",
              competency_level: 60,
              confidence_score: 70,
              ai_recommendations: "Niveau intermédiaire en conjugaison. Recommandation : réviser les verbes irréguliers.",
              analyzed_at: new Date().toISOString()
            }
          ],
          learning_recommendations: [
            "Pratiquer les exercices de conjugaison des verbes irréguliers",
            "Revoir les règles d'accord sujet-verbe",
            "S'entraîner sur les temps composés"
          ],
          difficulty_adjustment: 2,
          next_question_suggestion: 3
        });
      }, 1000);
    });
  }

  // ============================================================================
  // GESTION DES CLASSES ET ÉTUDIANTS
  // ============================================================================

  async getTeacherClasses(teacherId: number): Promise<Class[]> {
    try {
      // Appel API réel pour récupérer les classes du professeur
      const response = await this.request(`/api/v1/teacher/classes/`);
      return response || [];
    } catch (error) {
      console.error('Erreur lors de la récupération des classes:', error);
      // Fallback avec des données vides en cas d'erreur
      return [];
    }
  }

  async getTeacherStudents(teacherId: number): Promise<User[]> {
    try {
      // Appel API réel pour récupérer les étudiants du professeur
      const response = await this.request(`/api/v1/teacher/classes/students/all`);
      return response || [];
    } catch (error) {
      console.error('Erreur lors de la récupération des étudiants:', error);
      // Fallback avec des données vides en cas d'erreur
      return [];
    }
  }

  // ============================================================================
  // STATISTIQUES ET ANALYTICS
  // ============================================================================

  async getTestStatistics(testId: number): Promise<{
    success: boolean;
    statistics: any;
  }> {
    // Simulation - à remplacer par un vrai appel API
    return new Promise((resolve) => {
      setTimeout(() => {
        resolve({
          success: true,
          statistics: {
            assignments: {
              total: 24,
              classes: 2,
              individuals: 0
            },
            performance: {
              total_students: 24,
              completed_students: 20,
              in_progress_students: 4,
              average_score: 78
            },
            competencies: {
              total_analyzed: 20,
              average_level: 72,
              strengths: ["Grammaire", "Vocabulaire"],
              weaknesses: ["Conjugaison", "Syntaxe"]
            }
          }
        });
      }, 300);
    });
  }

  // ============================================================================
  // MONITORING EN TEMPS RÉEL
  // ============================================================================

  async getStudentActivity(teacherId: number): Promise<StudentActivity[]> {
    try {
      // Utiliser des données simulées en attendant que les routes de monitoring soient disponibles
      console.log('📊 Utilisation de données simulées pour l\'activité des étudiants');
      
      // Simuler des données d'activité des étudiants
      const mockActivities: StudentActivity[] = [
        {
          id: 1,
          name: "Ahmed Benali",
          testId: 101,
          testTitle: "Évaluation Mathématiques - Algèbre",
          currentQuestion: 3,
          totalQuestions: 10,
          difficulty: 0.7,
          confidence: 0.8,
          timeSpent: 450,
          status: 'active',
          lastActivity: new Date().toISOString()
        },
        {
          id: 2,
          name: "Fatima Zahra",
          testId: 102,
          testTitle: "Évaluation Français - Grammaire",
          currentQuestion: 7,
          totalQuestions: 15,
          difficulty: 0.6,
          confidence: 0.9,
          timeSpent: 320,
          status: 'active',
          lastActivity: new Date().toISOString()
        },
        {
          id: 3,
          name: "Omar Khelil",
          testId: 103,
          testTitle: "Évaluation Sciences - Physique",
          currentQuestion: 5,
          totalQuestions: 12,
          difficulty: 0.8,
          confidence: 0.6,
          timeSpent: 280,
          status: 'completed',
          lastActivity: new Date(Date.now() - 5 * 60 * 1000).toISOString()
        }
      ];
      
      return mockActivities;
    } catch (error) {
      console.error('Erreur lors de la récupération de l\'activité des étudiants:', error);
      return [];
    }
  }

  async getTestPerformance(teacherId: number): Promise<TestPerformance[]> {
    try {
      // Utiliser des données simulées en attendant que les routes de monitoring soient disponibles
      console.log('📊 Utilisation de données simulées pour les performances des tests');
      
      // Simuler des données de performance des tests
      const mockPerformances: TestPerformance[] = [
        {
          testId: 101,
          title: "Évaluation Mathématiques - Algèbre",
          activeStudents: 12,
          averageDifficulty: 0.7,
          averageConfidence: 0.8,
          completionRate: 0.85,
          averageTime: 450
        },
        {
          testId: 102,
          title: "Évaluation Français - Grammaire",
          activeStudents: 8,
          averageDifficulty: 0.6,
          averageConfidence: 0.9,
          completionRate: 0.92,
          averageTime: 320
        },
        {
          testId: 103,
          title: "Évaluation Sciences - Physique",
          activeStudents: 15,
          averageDifficulty: 0.8,
          averageConfidence: 0.6,
          completionRate: 0.78,
          averageTime: 280
        }
      ];
      
      return mockPerformances;
    } catch (error) {
      console.error('Erreur lors de la récupération des performances des tests:', error);
      return [];
    }
  }

  async getRealTimeMonitoring(teacherId: number): Promise<{
    activities: StudentActivity[];
    performances: TestPerformance[];
  }> {
    try {
      const [activities, performances] = await Promise.all([
        this.getStudentActivity(teacherId),
        this.getTestPerformance(teacherId)
      ]);

      return {
        activities,
        performances
      };
    } catch (error) {
      console.error('Erreur lors de la récupération du monitoring en temps réel:', error);
      return {
        activities: [],
        performances: []
      };
    }
  }
}

export const adaptiveEvaluationService = new AdaptiveEvaluationService();
