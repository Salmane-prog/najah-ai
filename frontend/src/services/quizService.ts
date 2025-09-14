import { apiClient } from '../utils/api';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// ============================================================================
// INTERFACES POUR LES QUIZ ET ÉVALUATIONS
// ============================================================================

export interface Quiz {
  id: number;
  title: string;
  description: string;
  subject: string;
  level: string;
  difficulty: string;
  time_limit: number;
  max_score: number;
  is_active: boolean;
  created_by: number;
  created_at: string;
  updated_at: string;
  questions_count: number;
}

export interface QuizQuestion {
  id: number;
  quiz_id: number;
  question_text: string;
  question_type: string;
  options: string[];
  correct_answer: string;
  points: number;
  order: number;
}

export interface QuizResult {
  id: number;
  user_id: number;
  student_id: number;
  quiz_id: number;
  score: number;
  max_score: number;
  percentage: number;
  is_completed: boolean;
  completed_at: string;
  sujet: string;
  answers: string;
  time_spent: number;
  created_at: string;
}

export interface QuizAssignment {
  id: number;
  quiz_id: number;
  student_id: number;
  assigned_by: number;
  assigned_at: string;
  due_date: string;
  status: string;
  score?: number;
  completed_at?: string;
  feedback?: string;
  quiz_title: string;
  quiz_subject: string;
  student_name: string;
  student_email: string;
}

export interface TeacherQuizData {
  quizzes: Quiz[];
  total_quizzes: number;
  active_quizzes: number;
  total_assignments: number;
  completed_assignments: number;
}

export interface StudentQuizData {
  assigned_quizzes: QuizAssignment[];
  completed_quizzes: QuizResult[];
  total_quizzes: number;
  average_score: number;
}

// ============================================================================
// FONCTIONS PRINCIPALES
// ============================================================================

export async function getTeacherQuizzes(token: string, teacherId: number): Promise<TeacherQuizData> {
  try {
    console.log('🔄 Récupération des quiz du professeur...');
    
    const response = await fetch(`${API_BASE_URL}/api/v1/quizzes/teacher/${teacherId}`, {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });

    if (!response.ok) {
      throw new Error(`Erreur HTTP: ${response.status}`);
    }

    const data = await response.json();
    console.log('✅ Quiz du professeur récupérés:', data);
    return data;

  } catch (error) {
    console.error('❌ Erreur lors de la récupération des quiz:', error);
    throw error;
  }
}

export async function getQuizDetails(token: string, quizId: number): Promise<Quiz & { questions: QuizQuestion[] }> {
  try {
    console.log('🔄 Récupération des détails du quiz...');
    
    const response = await fetch(`${API_BASE_URL}/api/v1/quizzes/${quizId}/with-questions`, {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });

    if (!response.ok) {
      throw new Error(`Erreur HTTP: ${response.status}`);
    }

    const data = await response.json();
    console.log('✅ Détails du quiz récupérés:', data);
    return data;

  } catch (error) {
    console.error('❌ Erreur lors de la récupération des détails du quiz:', error);
    throw error;
  }
}

export async function getQuizResults(token: string, quizId: number): Promise<QuizResult[]> {
  try {
    console.log('🔄 Récupération des résultats du quiz...');
    
    const response = await fetch(`${API_BASE_URL}/api/v1/quiz_results/enriched/`, {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });

    if (!response.ok) {
      throw new Error(`Erreur HTTP: ${response.status}`);
    }

    const data = await response.json();
    // Filtrer par quiz_id si nécessaire
    const filteredResults = data.filter((result: any) => result.quiz_id === quizId);
    console.log('✅ Résultats du quiz récupérés:', filteredResults);
    return filteredResults;

  } catch (error) {
    console.error('❌ Erreur lors de la récupération des résultats:', error);
    throw error;
  }
}

export async function getStudentQuizzes(token: string, studentId: number): Promise<StudentQuizData> {
  try {
    console.log('🔄 Récupération des quiz de l\'étudiant...');
    
    // Récupérer les quiz assignés
    const assignedResponse = await fetch(`${API_BASE_URL}/api/v1/quiz_assignments/student/${studentId}`, {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });

    if (!assignedResponse.ok) {
      throw new Error(`Erreur HTTP: ${assignedResponse.status}`);
    }

    const assignedQuizzes = await assignedResponse.json();

    // Récupérer les quiz complétés
    const completedResponse = await fetch(`${API_BASE_URL}/api/v1/quiz_results/user/${studentId}`, {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });

    if (!completedResponse.ok) {
      throw new Error(`Erreur HTTP: ${completedResponse.status}`);
    }

    const completedQuizzes = await completedResponse.json();

    // Calculer les statistiques
    const totalQuizzes = assignedQuizzes.length;
    const averageScore = completedQuizzes.length > 0 
      ? completedQuizzes.reduce((sum: number, quiz: QuizResult) => sum + quiz.score, 0) / completedQuizzes.length
      : 0;

    const studentData: StudentQuizData = {
      assigned_quizzes: assignedQuizzes,
      completed_quizzes: completedQuizzes,
      total_quizzes: totalQuizzes,
      average_score: Math.round(averageScore)
    };

    console.log('✅ Quiz de l\'étudiant récupérés:', studentData);
    return studentData;

  } catch (error) {
    console.error('❌ Erreur lors de la récupération des quiz de l\'étudiant:', error);
    throw error;
  }
}

export async function getQuizAssignments(token: string, teacherId: number): Promise<QuizAssignment[]> {
  try {
    console.log('🔄 Récupération des assignations de quiz...');
    
    const response = await fetch(`${API_BASE_URL}/api/v1/quiz_assignments/teacher/${teacherId}`, {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });

    if (!response.ok) {
      throw new Error(`Erreur HTTP: ${response.status}`);
    }

    const data = await response.json();
    console.log('✅ Assignations de quiz récupérées:', data);
    return data;

  } catch (error) {
    console.error('❌ Erreur lors de la récupération des assignations:', error);
    throw error;
  }
}

// ============================================================================
// FONCTIONS DE CRÉATION ET MODIFICATION
// ============================================================================

export async function createQuiz(token: string, quizData: any): Promise<Quiz> {
  try {
    console.log('🔄 Création d\'un nouveau quiz...');
    
    const response = await fetch(`${API_BASE_URL}/api/v1/quizzes/`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(quizData)
    });

    if (!response.ok) {
      throw new Error(`Erreur HTTP: ${response.status}`);
    }

    const data = await response.json();
    console.log('✅ Quiz créé avec succès:', data);
    return data;

  } catch (error) {
    console.error('❌ Erreur lors de la création du quiz:', error);
    throw error;
  }
}

export async function assignQuizToStudent(token: string, assignmentData: any): Promise<QuizAssignment> {
  try {
    console.log('🔄 Assignation d\'un quiz à un étudiant...');
    
    const response = await fetch(`${API_BASE_URL}/api/v1/quiz_assignments/`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(assignmentData)
    });

    if (!response.ok) {
      throw new Error(`Erreur HTTP: ${response.status}`);
    }

    const data = await response.json();
    console.log('✅ Quiz assigné avec succès:', data);
    return data;

  } catch (error) {
    console.error('❌ Erreur lors de l\'assignation du quiz:', error);
    throw error;
  }
}

// ============================================================================
// FONCTIONS DE FALLBACK (DONNÉES MOCKÉES EN CAS D'ERREUR)
// ============================================================================

export function getMockTeacherQuizzes(): TeacherQuizData {
  return {
    quizzes: [
      {
        id: 1,
        title: "Quiz Mathématiques 6ème",
        description: "Quiz sur les fractions et décimaux",
        subject: "Mathématiques",
        level: "6ème",
        difficulty: "medium",
        time_limit: 30,
        max_score: 100,
        is_active: true,
        created_by: 1,
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString(),
        questions_count: 10
      },
      {
        id: 2,
        title: "Quiz Français Grammaire",
        description: "Quiz sur la conjugaison",
        subject: "Français",
        level: "6ème",
        difficulty: "easy",
        time_limit: 20,
        max_score: 100,
        is_active: true,
        created_by: 1,
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString(),
        questions_count: 8
      }
    ],
    total_quizzes: 2,
    active_quizzes: 2,
    total_assignments: 15,
    completed_assignments: 12
  };
}

export function getMockStudentQuizzes(): StudentQuizData {
  return {
    assigned_quizzes: [
      {
        id: 1,
        quiz_id: 1,
        student_id: 1,
        assigned_by: 1,
        assigned_at: new Date().toISOString(),
        due_date: new Date(Date.now() + 86400000).toISOString(),
        status: "pending",
        quiz_title: "Quiz Mathématiques 6ème",
        quiz_subject: "Mathématiques",
        student_name: "Étudiant 1",
        student_email: "etudiant1@example.com"
      }
    ],
    completed_quizzes: [
      {
        id: 1,
        user_id: 1,
        student_id: 1,
        quiz_id: 1,
        score: 85,
        max_score: 100,
        percentage: 85,
        is_completed: true,
        completed_at: new Date().toISOString(),
        sujet: "Mathématiques",
        answers: "{}",
        time_spent: 1800,
        created_at: new Date().toISOString()
      }
    ],
    total_quizzes: 1,
    average_score: 85
  };
}

// ============================================================================
// FONCTIONS AVEC FALLBACK
// ============================================================================

export async function getTeacherQuizzesWithFallback(token: string, teacherId: number): Promise<TeacherQuizData> {
  try {
    return await getTeacherQuizzes(token, teacherId);
  } catch (error) {
    console.warn('⚠️ Utilisation des données de fallback pour les quiz:', error);
    return getMockTeacherQuizzes();
  }
}

export async function getStudentQuizzesWithFallback(token: string, studentId: number): Promise<StudentQuizData> {
  try {
    return await getStudentQuizzes(token, studentId);
  } catch (error) {
    console.warn('⚠️ Utilisation des données de fallback pour les quiz étudiant:', error);
    return getMockStudentQuizzes();
  }
}
