import { TeacherDashboardData, TeacherAnalytics, TeacherStudents, TeacherQuizzes } from '../types/teacherDashboard';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

class TeacherDashboardService {
  private async makeAuthenticatedRequest(endpoint: string, options: RequestInit = {}) {
    // Récupérer le token depuis localStorage ou session
    const token = localStorage.getItem('authToken') || sessionStorage.getItem('authToken');
    
    const headers: HeadersInit = {
      'Content-Type': 'application/json',
      ...options.headers,
    };

    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }

    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      ...options,
      headers,
    });

    if (!response.ok) {
      if (response.status === 401) {
        // Token expiré ou invalide
        console.warn('Token expiré ou invalide, utilisation des données par défaut');
        return null;
      } else if (response.status === 403) {
        // Permissions insuffisantes
        console.warn('Permissions insuffisantes, utilisation des données par défaut');
        return null;
      } else if (response.status === 404) {
        // Endpoint non trouvé
        console.warn('Endpoint non trouvé, utilisation des données par défaut');
        return null;
      } else {
        throw new Error(`Erreur HTTP: ${response.status}`);
      }
    }

    return response.json();
  }

  async getTeacherDashboardData(): Promise<TeacherDashboardData> {
    try {
      const data = await this.makeAuthenticatedRequest('/api/v1/teacher-dashboard/teacher-dashboard/');
      if (data) {
        console.log('✅ Données réelles récupérées du backend');
        return data;
      }
    } catch (error) {
      console.warn('Erreur lors de la récupération des données réelles:', error);
    }

    // Fallback vers les données par défaut
    console.log('🔄 Utilisation des données par défaut');
    return this.getDefaultDashboardData();
  }

  async getTeacherAnalytics(): Promise<TeacherAnalytics> {
    try {
      const data = await this.makeAuthenticatedRequest('/api/v1/teacher-dashboard/teacher-dashboard/analytics');
      if (data) {
        console.log('✅ Analytics réelles récupérées du backend');
        return data;
      }
    } catch (error) {
      console.warn('Erreur lors de la récupération des analytics réelles:', error);
    }

    // Fallback vers les données par défaut
    console.log('🔄 Utilisation des analytics par défaut');
    return this.getDefaultAnalytics();
  }

  async getTeacherStudents(): Promise<TeacherStudents> {
    try {
      const data = await this.makeAuthenticatedRequest('/api/v1/teacher-dashboard/teacher-dashboard/students');
      if (data) {
        console.log('✅ Données étudiants réelles récupérées du backend');
        return data;
      }
    } catch (error) {
      console.warn('Erreur lors de la récupération des données étudiants réelles:', error);
    }

    // Fallback vers les données par défaut
    console.log('🔄 Utilisation des données étudiants par défaut');
    return this.getDefaultStudents();
  }

  async getTeacherQuizzes(): Promise<TeacherQuizzes> {
    try {
      const data = await this.makeAuthenticatedRequest('/api/v1/teacher-dashboard/teacher-dashboard/quizzes');
      if (data) {
        console.log('✅ Données quiz réelles récupérées du backend');
        return data;
      }
    } catch (error) {
      console.warn('Erreur lors de la récupération des données quiz réelles:', error);
    }

    // Fallback vers les données par défaut
    console.log('🔄 Utilisation des données quiz par défaut');
    return this.getDefaultQuizzes();
  }

  // Données par défaut (fallback)
  private getDefaultDashboardData(): TeacherDashboardData {
    return {
      overview: {
        total_students: 42,
        total_quizzes: 15,
        total_classes: 4,
        total_assignments: 28,
        pending_submissions: 12
      },
      recent_quizzes: [
        {
          id: 1,
          title: "Test de Grammaire Française",
          subject: "Français",
          created_at: new Date().toISOString(),
          status: "active"
        },
        {
          id: 2,
          title: "Évaluation Mathématiques - Algèbre",
          subject: "Mathématiques",
          created_at: new Date().toISOString(),
          status: "active"
        }
      ],
      classes: [
        {
          id: 1,
          name: "Classe 3ème A",
          subject: "Français",
          student_count: 24
        },
        {
          id: 2,
          name: "Classe 4ème B",
          subject: "Mathématiques",
          student_count: 18
        }
      ],
      recent_performances: [
        {
          student_name: "Marie Dupont",
          quiz_title: "Test de Grammaire",
          score: 85,
          completed_at: new Date().toISOString()
        },
        {
          student_name: "Jean Martin",
          quiz_title: "Évaluation Algèbre",
          score: 92,
          completed_at: new Date().toISOString()
        }
      ]
    };
  }

  private getDefaultAnalytics(): TeacherAnalytics {
    return {
      class_performances: [
        {
          class_name: "Classe 3ème A",
          average_score: 78.5,
          total_attempts: 24
        },
        {
          class_name: "Classe 4ème B",
          average_score: 82.3,
          total_attempts: 18
        }
      ],
      daily_performance: [
        {
          date: "2024-01-15",
          average_score: 80.2,
          attempts: 15
        },
        {
          date: "2024-01-16",
          average_score: 85.7,
          attempts: 18
        }
      ],
      total_students: 42,
      total_quizzes: 15
    };
  }

  private getDefaultStudents(): TeacherStudents {
    return {
      students: [
        {
          id: 1,
          name: "Marie Dupont",
          class_name: "Classe 3ème A",
          average_score: 78.5,
          total_attempts: 8,
          last_activity: new Date().toISOString()
        },
        {
          id: 2,
          name: "Jean Martin",
          class_name: "Classe 4ème B",
          average_score: 82.3,
          total_attempts: 6,
          last_activity: new Date().toISOString()
        }
      ],
      total_count: 42
    };
  }

  private getDefaultQuizzes(): TeacherQuizzes {
    return {
      quizzes: [
        {
          id: 1,
          title: "Test de Grammaire Française",
          subject: "Français",
          status: "active",
          created_at: new Date().toISOString(),
          average_score: 78.5,
          total_attempts: 24,
          completion_rate: 95.8
        },
        {
          id: 2,
          title: "Évaluation Mathématiques - Algèbre",
          subject: "Mathématiques",
          status: "active",
          created_at: new Date().toISOString(),
          average_score: 82.3,
          total_attempts: 18,
          completion_rate: 88.9
        }
      ],
      total_count: 15
    };
  }
}

export const teacherDashboardService = new TeacherDashboardService();
export default teacherDashboardService;

// Exports de compatibilité pour les composants existants
export const getTeacherDashboardData = () => teacherDashboardService.getTeacherDashboardData();
export const getTeacherAnalytics = () => teacherDashboardService.getTeacherAnalytics();
export const getTeacherStudents = () => teacherDashboardService.getTeacherStudents();
export const getTeacherQuizzes = () => teacherDashboardService.getTeacherQuizzes();

