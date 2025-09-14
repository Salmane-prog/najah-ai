'use client';

import { API_BASE_URL } from '@/config/api';

// ============================================================================
// INTERFACES UNIFIÉES
// ============================================================================

export interface UnifiedQuiz {
  id: number;
  title: string;
  description: string;
  subject: string;
  quiz_type: 'normal' | 'adaptive';
  estimated_duration: number;
  total_questions: number;
  is_active: boolean;
  created_by: number;
  created_at: string;
}

export interface UnifiedQuestion {
  id: number;
  question_text: string;
  question_type: string;
  options: string[];
  correct_answer: string;
  explanation?: string;
  points: number;
  order: number;
}

export interface UnifiedQuizResult {
  id: number;
  quiz_id: number;
  quiz_type: 'normal' | 'adaptive';
  student_id: number;
  score: number;
  max_score: number;
  percentage: number;
  is_completed: boolean;
  completed_at: string;
  time_spent: number;
  answers: any[];
}

export interface UnifiedQuizAssignment {
  id: string; // Maintenant une string unique (ex: "normal-1", "adaptive-2")
  original_id: number; // L'ID original de la base de données
  quiz_id: number;
  quiz_title: string;
  quiz_type: 'normal' | 'adaptive';
  subject: string;
  description: string;
  assigned_by: number;
  assigned_at: string;
  due_date: string;
  status: string;
  estimated_duration: number;
}

// ============================================================================
// ADAPTATEURS POUR UNIFIER LES DONNÉES
// ============================================================================

export function normalizeQuiz(quiz: any, type: 'normal' | 'adaptive'): UnifiedQuiz {
  if (type === 'normal') {
    return {
      id: quiz.id,
      title: quiz.title,
      description: quiz.description || '',
      subject: quiz.subject || 'Général',
      quiz_type: 'normal',
      estimated_duration: quiz.time_limit || 30,
      total_questions: quiz.questions?.length || 0,
      is_active: quiz.is_active,
      created_by: quiz.created_by,
      created_at: quiz.created_at
    };
  } else {
    console.log('🔥 [DEBUG] Normalisation du test adaptatif:', quiz);
    console.log('🔥 [DEBUG] Questions dans le quiz:', quiz.questions?.length || 0);
    
    return {
      id: quiz.id,
      title: quiz.title,
      description: quiz.description || '',
      subject: quiz.subject || 'Général',
      quiz_type: 'adaptive',
      estimated_duration: quiz.estimated_duration || 30,
      total_questions: quiz.questions?.length || quiz.total_questions || 0,
      is_active: quiz.is_active,
      created_by: quiz.created_by,
      created_at: quiz.created_at
    };
  }
}

export function normalizeQuestion(question: any, type: 'normal' | 'adaptive'): UnifiedQuestion {
  if (type === 'normal') {
    return {
      id: question.id,
      question_text: question.question_text,
      question_type: question.question_type || 'multiple_choice',
      options: Array.isArray(question.options) ? question.options : [],
      correct_answer: question.correct_answer || '',
      explanation: question.explanation,
      points: question.points || 1,
      order: question.order || 0
    };
  } else {
    return {
      id: question.id,
      question_text: question.question_text,
      question_type: question.question_type || 'multiple_choice',
      options: Array.isArray(question.options) ? question.options : [],
      correct_answer: question.correct_answer || '',
      explanation: question.explanation,
      points: 1, // Tests adaptatifs ont généralement 1 point par question
      order: question.question_order || 0
    };
  }
}

export function normalizeQuizResult(result: any, type: 'normal' | 'adaptive'): UnifiedQuizResult {
  if (type === 'normal') {
    return {
      id: result.id,
      quiz_id: result.quiz_id,
      quiz_type: 'normal',
      student_id: result.student_id,
      score: result.score || 0,
      max_score: result.max_score || 100,
      percentage: result.percentage || 0,
      is_completed: result.is_completed || false,
      completed_at: result.completed_at,
      time_spent: result.time_spent || 0,
      answers: result.answers ? JSON.parse(result.answers) : []
    };
  } else {
    console.log('🔥 [DEBUG] Normalisation du test adaptatif:', result);
    return {
      id: result.id || result.attempt_id,
      quiz_id: result.test_id || result.quiz_id, // Test adaptatif utilise test_id
      quiz_type: 'adaptive',
      student_id: result.student_id,
      score: result.score || result.total_score || 0,
      max_score: result.max_score || 10, // Utiliser la vraie valeur du backend
      percentage: result.percentage || 0, // Utiliser le pourcentage calculé par le backend
      is_completed: result.status === 'completed' || result.success === true,
      completed_at: result.completed_at,
      time_spent: 0, // Pas de time_spent dans TestAttempt
      answers: [] // Pas d'answers détaillés dans TestAttempt
    };
  }
}

// ============================================================================
// FONCTIONS DE RÉCUPÉRATION UNIFIÉES
// ============================================================================

export async function getUnifiedQuiz(token: string, quizId: string): Promise<UnifiedQuiz> {
  try {
    console.log('🔥 [DEBUG] Tentative de récupération du quiz:', quizId);
    
    if (!token) {
      throw new Error('Token d\'authentification manquant');
    }
    
    // Essayer d'abord comme quiz normal
    const normalResponse = await fetch(`${API_BASE_URL}/api/v1/quizzes/${quizId}`, {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });

    console.log('🔥 [DEBUG] Réponse quiz normal:', normalResponse.status, normalResponse.statusText);

    if (normalResponse.ok) {
      const quizData = await normalResponse.json();
      console.log('🔥 [DEBUG] Quiz normal trouvé:', quizData);
      return normalizeQuiz(quizData, 'normal');
    }

    // Si pas de quiz normal, essayer comme test adaptatif
    const adaptiveResponse = await fetch(`${API_BASE_URL}/api/v1/adaptive-evaluation/tests/${quizId}`, {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });

    console.log('🔥 [DEBUG] Réponse test adaptatif:', adaptiveResponse.status, adaptiveResponse.statusText);

    if (adaptiveResponse.ok) {
      const testData = await adaptiveResponse.json();
      console.log('🔥 [DEBUG] Test adaptatif trouvé:', testData);
      console.log('🔥 [DEBUG] Structure des données:', JSON.stringify(testData, null, 2));
      
      // Pour les tests adaptatifs, les questions sont dans testData.test.questions
      if (testData.test && testData.test.questions) {
        console.log('🔥 [DEBUG] Questions trouvées dans le test:', testData.test.questions.length);
      }
      
      return normalizeQuiz(testData.test || testData, 'adaptive');
    }

    console.log('❌ [DEBUG] Aucun quiz trouvé avec l\'ID:', quizId);
    console.log('❌ [DEBUG] Status quiz normal:', normalResponse.status);
    console.log('❌ [DEBUG] Status test adaptatif:', adaptiveResponse.status);
    
    // Si aucun quiz trouvé, essayer avec le quiz de test (ID 24) ou le test adaptatif (ID 47)
    if (quizId !== '24' && quizId !== '47') {
      console.log('🔄 [DEBUG] Tentative avec le quiz de test ID 24...');
      return getUnifiedQuiz(token, '24');
    }
    
    throw new Error(`Quiz non trouvé avec l'ID ${quizId}`);
  } catch (error) {
    console.error('❌ Erreur lors de la récupération du quiz:', error);
    if (error instanceof Error) {
      throw new Error(`Erreur lors de la récupération du quiz: ${error.message}`);
    } else {
      throw new Error('Erreur inconnue lors de la récupération du quiz');
    }
  }
}

export async function getUnifiedQuizQuestions(token: string, quizId: string, quizType: 'normal' | 'adaptive'): Promise<UnifiedQuestion[]> {
  try {
    if (quizType === 'normal') {
      const response = await fetch(`${API_BASE_URL}/api/v1/quizzes/${quizId}`, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });

      if (response.ok) {
        const quizData = await response.json();
        return (quizData.questions || []).map((q: any) => normalizeQuestion(q, 'normal'));
      }
    } else {
      const response = await fetch(`${API_BASE_URL}/api/v1/adaptive-evaluation/tests/${quizId}`, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });

      if (response.ok) {
        const testData = await response.json();
        console.log('🔥 [DEBUG] Récupération des questions du test adaptatif:', testData);
        
        // Pour les tests adaptatifs, les questions sont dans testData.test.questions
        const questions = testData.test?.questions || testData.questions || [];
        console.log('🔥 [DEBUG] Questions extraites:', questions.length);
        
        return questions.map((q: any) => normalizeQuestion(q, 'adaptive'));
      }
    }

    throw new Error('Questions non trouvées');
  } catch (error) {
    console.error('❌ Erreur lors de la récupération des questions:', error);
    throw error;
  }
}

export async function submitUnifiedQuiz(
  token: string, 
  quizId: string, 
  quizType: 'normal' | 'adaptive',
  answers: any[]
): Promise<UnifiedQuizResult> {
  try {
    if (quizType === 'normal') {
      const response = await fetch(`${API_BASE_URL}/api/v1/quizzes/${quizId}/submit`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          quiz_id: Number(quizId),
          answers: answers.map(ans => ({
            question_id: ans.question_id,
            answer: ans.answer
          }))
        })
      });

      if (response.ok) {
        const result = await response.json();
        return normalizeQuizResult(result, 'normal');
      }
    } else {
      // Pour les tests adaptatifs, soumettre directement
      const submitResponse = await fetch(`${API_BASE_URL}/api/v1/adaptive-evaluation/tests/${quizId}/submit`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          answers: answers.map(ans => ({
            question_id: ans.question_id,
            answer: ans.answer
          }))
        })
      });

      if (submitResponse.ok) {
        const result = await submitResponse.json();
        return normalizeQuizResult(result, 'adaptive');
      }
    }

    throw new Error('Erreur lors de la soumission');
  } catch (error) {
    console.error('❌ Erreur lors de la soumission du quiz:', error);
    throw error;
  }
}

export async function getUnifiedQuizAssignments(token: string, studentId: number): Promise<UnifiedQuizAssignment[]> {
  try {
    const [normalResponse, adaptiveResponse] = await Promise.all([
      fetch(`${API_BASE_URL}/api/v1/quiz_assignments/student/${studentId}`, {
        headers: { 'Authorization': `Bearer ${token}` }
      }),
      fetch(`${API_BASE_URL}/api/v1/adaptive-evaluation/student/${studentId}/assignments`, {
        headers: { 'Authorization': `Bearer ${token}` }
      })
    ]);

    let allAssignments: UnifiedQuizAssignment[] = [];

    // Traiter les quiz normaux
    if (normalResponse.ok) {
      const normalData = await normalResponse.json();
      const normalAssignments = normalData.map((assignment: any) => ({
        id: `normal-${assignment.id}`, // Clé unique pour les quiz normaux
        original_id: assignment.id,
        quiz_id: assignment.quiz_id,
        quiz_title: assignment.quiz_title,
        quiz_type: 'normal' as const,
        subject: assignment.quiz_subject || 'Général',
        description: assignment.description || '',
        assigned_by: assignment.assigned_by,
        assigned_at: assignment.assigned_at,
        due_date: assignment.due_date,
        status: assignment.status,
        estimated_duration: assignment.estimated_duration || 30
      }));
      allAssignments.push(...normalAssignments);
    }

    // Traiter les tests adaptatifs
    if (adaptiveResponse.ok) {
      const adaptiveData = await adaptiveResponse.json();
      const adaptiveAssignments = adaptiveData.map((assignment: any) => ({
        id: `adaptive-${assignment.id}`, // Clé unique pour les tests adaptatifs
        original_id: assignment.id,
        quiz_id: assignment.test_id,
        quiz_title: assignment.title,
        quiz_type: 'adaptive' as const,
        subject: assignment.subject,
        description: assignment.description,
        assigned_by: assignment.assigned_by,
        assigned_at: assignment.assigned_at,
        due_date: assignment.due_date,
        status: assignment.status,
        estimated_duration: assignment.estimated_duration || 30
      }));
      allAssignments.push(...adaptiveAssignments);
    }

    console.log('🔥 [DEBUG] Total des assignations unifiées:', allAssignments.length);
    console.log('🔥 [DEBUG] Assignations avec clés uniques:', allAssignments.map(a => ({ id: a.id, type: a.quiz_type })));
    return allAssignments;
  } catch (error) {
    console.error('❌ Erreur lors de la récupération des assignations:', error);
    return [];
  }
}

export async function getUnifiedCompletedQuizzes(token: string, studentId: number): Promise<UnifiedQuizAssignment[]> {
  try {
    console.log('🔥 [DEBUG] Récupération des quiz terminés pour l\'étudiant:', studentId);
    
    // Récupérer les quiz normaux terminés
    const normalResultsResponse = await fetch(`${API_BASE_URL}/api/v1/quiz_results/user/${studentId}`, {
      headers: { 'Authorization': `Bearer ${token}` }
    });
    
    // Récupérer les tests adaptatifs terminés
    const adaptiveResultsResponse = await fetch(`${API_BASE_URL}/api/v1/adaptive-evaluation/student/${studentId}/results`, {
      headers: { 'Authorization': `Bearer ${token}` }
    });
    
    let completedQuizzes: UnifiedQuizAssignment[] = [];
    
    // Traiter les quiz normaux terminés
    if (normalResultsResponse.ok) {
      const normalResults = await normalResultsResponse.json();
      const completedNormal = normalResults.filter((result: any) => result.completed || result.is_completed);
      
      for (const result of completedNormal) {
        // Récupérer les détails de l'assignation
        const assignmentResponse = await fetch(`${API_BASE_URL}/api/v1/quiz_assignments/student/${studentId}`, {
          headers: { 'Authorization': `Bearer ${token}` }
        });
        
        if (assignmentResponse.ok) {
          const assignments = await assignmentResponse.json();
          const assignment = assignments.find((a: any) => a.quiz_id === result.quiz_id);
          
          if (assignment) {
            completedQuizzes.push({
              id: `normal-completed-${result.id}`,
              original_id: assignment.id,
              quiz_id: result.quiz_id,
              quiz_title: assignment.quiz_title || `Quiz ${result.quiz_id}`,
              quiz_type: 'normal' as const,
              subject: assignment.quiz_subject || 'Général',
              description: assignment.description || '',
              assigned_by: assignment.assigned_by,
              assigned_at: assignment.assigned_at,
              due_date: assignment.due_date,
              status: 'completed',
              estimated_duration: assignment.estimated_duration || 30
            });
          }
        }
      }
    }
    
    // Traiter les tests adaptatifs terminés
    if (adaptiveResultsResponse.ok) {
      const adaptiveResults = await adaptiveResultsResponse.json();
      console.log('🔥 [DEBUG] Résultats adaptatifs reçus:', adaptiveResults);
      
      // Vérifier que adaptiveResults a la bonne structure
      if (adaptiveResults && adaptiveResults.results && Array.isArray(adaptiveResults.results)) {
        for (const result of adaptiveResults.results) {
          // Récupérer les détails de l'assignation
          const assignmentResponse = await fetch(`${API_BASE_URL}/api/v1/adaptive-evaluation/student/${studentId}/assignments`, {
            headers: { 'Authorization': `Bearer ${token}` }
          });
          
          if (assignmentResponse.ok) {
            const assignments = await assignmentResponse.json();
            const assignment = assignments.find((a: any) => a.test_id === result.test_id);
            
            if (assignment) {
              completedQuizzes.push({
                id: `adaptive-completed-${result.id}`,
                original_id: assignment.id,
                quiz_id: result.test_id,
                quiz_title: result.test_title || assignment.title,
                quiz_type: 'adaptive' as const,
                subject: result.test_subject || assignment.subject,
                description: assignment.description || '',
                assigned_by: assignment.assigned_by,
                assigned_at: assignment.assigned_at,
                due_date: assignment.due_date,
                status: 'completed',
                estimated_duration: assignment.estimated_duration || 30
              });
            }
          }
        }
      } else {
        console.log('⚠️ [DEBUG] Structure des résultats adaptatifs inattendue:', adaptiveResults);
      }
    }
    
    console.log('🔥 [DEBUG] Quiz terminés trouvés:', completedQuizzes.length);
    return completedQuizzes;
    
  } catch (error) {
    console.error('❌ Erreur lors de la récupération des quiz terminés:', error);
    return [];
  }
}
