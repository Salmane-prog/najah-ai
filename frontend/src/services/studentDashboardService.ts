import { apiClient } from '../utils/api';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// ============================================================================
// INTERFACES POUR LES DONNÉES ÉTUDIANT
// ============================================================================

export interface StudentOverview {
  id: number;
  name: string;
  email: string;
  role: string;
  overall_progress: number;
  quizzes_completed: number;
  average_score: number;
  classes_count: number;
  badges_count: number;
  last_activity: string;
}

export interface StudentClass {
  id: number;
  name: string;
  subject: string;
  progress: number;
}

export interface StudentBadge {
  id: number;
  name: string;
  description: string;
  icon: string;
  awarded_at: string;
}

export interface StudentQuiz {
  id: number;
  title: string;
  subject: string;
  score: number;
  max_score: number;
  completed_at: string;
  feedback?: string;
}

export interface AssignedQuiz {
  id: number;
  quiz_id: number;
  quiz_title: string;
  quiz_subject: string;
  assigned_by: number;
  assigned_at: string;
  due_date: string;
  status: string;
  score?: number;
  completed_at?: string;
  feedback?: string;
}

export interface StudentActivity {
  id: number;
  type: string;
  description: string;
  timestamp: string;
}

export interface StudentAnalytics {
  student: StudentOverview;
  analytics: {
    overall_progress: number;
    quizzes_completed: number;
    average_score: number;
    classes_count: number;
    badges_count: number;
    last_activity: string;
  };
  classes: StudentClass[];
  badges: StudentBadge[];
  recent_activity: StudentActivity[];
}

export interface StudentDashboardData {
  overview: StudentOverview;
  classes: StudentClass[];
  badges: StudentBadge[];
  recent_quizzes: StudentQuiz[];
  assigned_quizzes: AssignedQuiz[];
  recent_activity: StudentActivity[];
  analytics: StudentAnalytics;
}

// ============================================================================
// FONCTIONS PRINCIPALES
// ============================================================================

export async function getStudentDashboardData(token: string, studentId: number): Promise<StudentDashboardData> {
  try {
    console.log('🔄 Récupération des données du dashboard étudiant...');
    
    // Récupérer toutes les données en parallèle
    const [analytics, assignedQuizzes, recentQuizzes] = await Promise.all([
      getStudentAnalytics(token, studentId),
      getStudentAssignedQuizzes(token, studentId),
      getStudentRecentQuizzes(token, studentId)
    ]);

    // Construire le dashboard complet
    const dashboardData: StudentDashboardData = {
      overview: analytics.student,
      classes: analytics.classes,
      badges: analytics.badges,
      recent_quizzes: recentQuizzes,
      assigned_quizzes: assignedQuizzes,
      recent_activity: analytics.recent_activity,
      analytics: analytics
    };

    console.log('✅ Dashboard étudiant récupéré avec succès:', dashboardData);
    return dashboardData;

  } catch (error) {
    console.error('❌ Erreur lors de la récupération du dashboard étudiant:', error);
    throw error;
  }
}

// ============================================================================
// FONCTIONS SPÉCIFIQUES
// ============================================================================

export async function getStudentAnalytics(token: string, studentId: number): Promise<StudentAnalytics> {
  try {
    const response = await fetch(`${API_BASE_URL}/api/v1/student_analytics/student/${studentId}`, {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });

    if (!response.ok) {
      throw new Error(`Erreur HTTP: ${response.status}`);
    }

    const data = await response.json();
    console.log('✅ Analytics étudiant récupérées:', data);
    return data;

  } catch (error) {
    console.error('❌ Erreur lors de la récupération des analytics étudiant:', error);
    throw error;
  }
}

export async function getStudentAssignedQuizzes(token: string, studentId: number): Promise<AssignedQuiz[]> {
  try {
    const response = await fetch(`${API_BASE_URL}/api/v1/quiz_assignments/student/${studentId}`, {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });

    if (!response.ok) {
      throw new Error(`Erreur HTTP: ${response.status}`);
    }

    const data = await response.json();
    console.log('✅ Quiz assignés récupérés:', data);
    return data;

  } catch (error) {
    console.error('❌ Erreur lors de la récupération des quiz assignés:', error);
    throw error;
  }
}

export async function getStudentRecentQuizzes(token: string, studentId: number): Promise<StudentQuiz[]> {
  try {
    const response = await fetch(`${API_BASE_URL}/api/v1/quiz_results/user/${studentId}`, {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });

    if (!response.ok) {
      throw new Error(`Erreur HTTP: ${response.status}`);
    }

    const data = await response.json();
    console.log('✅ Quiz récents récupérés:', data);
    return data;

  } catch (error) {
    console.error('❌ Erreur lors de la récupération des quiz récents:', error);
    throw error;
  }
}

export async function getStudentClasses(token: string, studentId: number): Promise<StudentClass[]> {
  try {
    const response = await fetch(`${API_BASE_URL}/api/v1/student_learning_paths/student/${studentId}`, {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });

    if (!response.ok) {
      throw new Error(`Erreur HTTP: ${response.status}`);
    }

    const data = await response.json();
    console.log('✅ Classes étudiant récupérées:', data);
    return data.learning_paths || [];

  } catch (error) {
    console.error('❌ Erreur lors de la récupération des classes étudiant:', error);
    throw error;
  }
}

export async function getStudentBadges(token: string, studentId: number): Promise<StudentBadge[]> {
  try {
    const response = await fetch(`${API_BASE_URL}/api/v1/gamification/student/${studentId}/badges`, {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });

    if (!response.ok) {
      throw new Error(`Erreur HTTP: ${response.status}`);
    }

    const data = await response.json();
    console.log('✅ Badges étudiant récupérés:', data);
    return data.badges || [];

  } catch (error) {
    console.error('❌ Erreur lors de la récupération des badges étudiant:', error);
    throw error;
  }
}

// ============================================================================
// FONCTIONS DE FALLBACK (DONNÉES MOCKÉES EN CAS D'ERREUR)
// ============================================================================

export function getMockStudentDashboardData(): StudentDashboardData {
  return {
    overview: {
      id: 1,
      name: "Étudiant",
      email: "etudiant@example.com",
      role: "student",
      overall_progress: 75,
      quizzes_completed: 12,
      average_score: 82,
      classes_count: 3,
      badges_count: 5,
      last_activity: new Date().toISOString()
    },
    classes: [
      { id: 1, name: "Mathématiques", subject: "Math", progress: 80 },
      { id: 2, name: "Français", subject: "Langue", progress: 70 },
      { id: 3, name: "Sciences", subject: "Science", progress: 75 }
    ],
    badges: [
      { id: 1, name: "Quiz Master", description: "Complété 10 quiz", icon: "award", awarded_at: new Date().toISOString() },
      { id: 2, name: "Excellent Score", description: "Score moyen de 80%", icon: "star", awarded_at: new Date().toISOString() }
    ],
    recent_quizzes: [
      { id: 1, title: "Quiz Math Avancé", subject: "Math", score: 85, max_score: 100, completed_at: new Date().toISOString() },
      { id: 2, title: "Quiz Français", subject: "Langue", score: 78, max_score: 100, completed_at: new Date().toISOString() }
    ],
    assigned_quizzes: [
      { id: 1, quiz_id: 1, quiz_title: "Quiz Math", quiz_subject: "Math", assigned_by: 1, assigned_at: new Date().toISOString(), due_date: new Date(Date.now() + 86400000).toISOString(), status: "pending" }
    ],
    recent_activity: [
      { id: 1, type: "quiz", description: "Quiz Math complété avec 85%", timestamp: new Date().toISOString() },
      { id: 2, type: "badge", description: "Badge Quiz Master obtenu", timestamp: new Date().toISOString() }
    ],
    analytics: {
      student: {
        id: 1,
        name: "Étudiant",
        email: "etudiant@example.com",
        role: "student",
        overall_progress: 75,
        quizzes_completed: 12,
        average_score: 82,
        classes_count: 3,
        badges_count: 5,
        last_activity: new Date().toISOString()
      },
      analytics: {
        overall_progress: 75,
        quizzes_completed: 12,
        average_score: 82,
        classes_count: 3,
        badges_count: 5,
        last_activity: new Date().toISOString()
      },
      classes: [
        { id: 1, name: "Mathématiques", subject: "Math", progress: 80 },
        { id: 2, name: "Français", subject: "Langue", progress: 70 },
        { id: 3, name: "Sciences", subject: "Science", progress: 75 }
      ],
      badges: [
        { id: 1, name: "Quiz Master", description: "Complété 10 quiz", icon: "award", awarded_at: new Date().toISOString() },
        { id: 2, name: "Excellent Score", description: "Score moyen de 80%", icon: "star", awarded_at: new Date().toISOString() }
      ],
      recent_activity: [
        { id: 1, type: "quiz", description: "Quiz Math complété avec 85%", timestamp: new Date().toISOString() },
        { id: 2, type: "badge", description: "Badge Quiz Master obtenu", timestamp: new Date().toISOString() }
      ]
    }
  };
}

export async function getStudentDashboardDataWithFallback(token: string, studentId: number): Promise<StudentDashboardData> {
  try {
    return await getStudentDashboardData(token, studentId);
  } catch (error) {
    console.warn('⚠️ Utilisation des données de fallback pour le dashboard étudiant:', error);
    return getMockStudentDashboardData();
  }
}
