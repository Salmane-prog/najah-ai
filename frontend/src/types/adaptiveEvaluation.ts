// Types pour le système d'évaluation adaptative

export interface AdaptiveTest {
  id: number;
  title: string;
  subject: string;
  description: string;
  difficulty_min: number;
  difficulty_max: number;
  estimated_duration: number;
  total_questions: number;
  adaptation_type: 'cognitive' | 'performance' | 'hybrid';
  learning_objectives: string;
  is_active: boolean;
  created_by: number;
  created_at: string;
  questions?: AdaptiveQuestion[];
  statistics?: TestStatistics;
}

export interface AdaptiveQuestion {
  id: number;
  test_id: number;
  question_text: string;
  question_type: 'multiple_choice' | 'open_ended' | 'true_false';
  difficulty_level: number;
  learning_objective: string;
  options: string[];
  correct_answer: string;
  explanation: string;
  order_index: number;
}

export interface TestAssignment {
  id: number;
  test_id: number;
  assignment_type: 'class' | 'student';
  target_id: number;
  assigned_by: number;
  assigned_at: string;
  due_date?: string;
  status: 'active' | 'inactive' | 'completed';
}

export interface TestAttempt {
  id: number;
  test_id: number;
  student_id: number;
  assignment_id?: number;
  started_at: string;
  completed_at?: string;
  status: 'in_progress' | 'completed' | 'abandoned';
  current_question_index: number;
  total_score: number;
  max_score: number;
}

export interface QuestionResponse {
  id: number;
  attempt_id: number;
  question_id: number;
  student_answer: string;
  is_correct: boolean;
  score: number;
  response_time: number;
  answered_at: string;
}

export interface CompetencyAnalysis {
  id: number;
  attempt_id: number;
  student_id: number;
  test_id: number;
  competency_name: string;
  competency_level: number; // 0-100
  confidence_score: number; // 0-100
  ai_recommendations: string;
  analyzed_at: string;
}

export interface Class {
  id: number;
  name: string;
  description: string;
  teacher_id: number;
  created_at: string;
  students?: ClassStudent[];
}

export interface ClassStudent {
  id: number;
  class_id: number;
  student_id: number;
  joined_at: string;
  student?: User;
}

export interface User {
  id: number;
  first_name: string;
  last_name: string;
  email: string;
  role: 'student' | 'teacher' | 'admin';
}

export interface TestStatistics {
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
  competencies: {
    total_analyzed: number;
    average_level: number;
    strengths: string[];
    weaknesses: string[];
  };
}

export interface CreateTestData {
  title: string;
  subject: string;
  description?: string;
  difficulty_min: number;
  difficulty_max: number;
  estimated_duration: number;
  total_questions: number;
  adaptation_type: 'cognitive' | 'performance' | 'hybrid';
  learning_objectives?: string;
  questions?: CreateQuestionData[];
}

export interface CreateQuestionData {
  question_text: string;
  question_type: 'multiple_choice' | 'open_ended' | 'true_false';
  difficulty_level: number;
  learning_objective?: string;
  options?: string[];
  correct_answer: string;
  explanation?: string;
}

export interface AssignmentData {
  class_ids: number[];
  student_ids: number[];
  due_date?: string;
}

export interface TestResponse {
  question_id: number;
  answer: string;
  response_time: number;
}

export interface AIAnalysisResult {
  competencies: CompetencyAnalysis[];
  learning_recommendations: string[];
  difficulty_adjustment: number;
  next_question_suggestion: number;
}

// Types pour le monitoring en temps réel
export interface StudentActivity {
  id: number;
  name: string;
  testId: number;
  testTitle: string;
  currentQuestion: number;
  totalQuestions: number;
  difficulty: number;
  confidence: number;
  timeSpent: number;
  status: 'active' | 'completed' | 'paused';
  lastActivity: string;
}

export interface TestPerformance {
  testId: number;
  title: string;
  activeStudents: number;
  averageDifficulty: number;
  averageConfidence: number;
  completionRate: number;
  averageTime: number;
}