// Types pour le dashboard du professeur

export interface TeacherDashboardData {
  overview: {
    total_students: number;
    total_quizzes: number;
    total_classes: number;
    total_assignments: number;
    pending_submissions: number;
  };
  recent_quizzes: Array<{
    id: number;
    title: string;
    subject: string;
    created_at: string;
    status: string;
  }>;
  classes: Array<{
    id: number;
    name: string;
    subject: string;
    student_count: number;
  }>;
  recent_performances: Array<{
    student_name: string;
    quiz_title: string;
    score: number;
    completed_at: string;
  }>;
}

export interface TeacherAnalytics {
  class_performances: Array<{
    class_name: string;
    average_score: number;
    total_attempts: number;
  }>;
  daily_performance: Array<{
    date: string;
    average_score: number;
    attempts: number;
  }>;
  total_students: number;
  total_quizzes: number;
}

export interface TeacherStudents {
  students: Array<{
    id: number;
    name: string;
    class_name: string;
    average_score: number;
    total_attempts: number;
    last_activity: string;
  }>;
  total_count: number;
}

export interface TeacherQuizzes {
  quizzes: Array<{
    id: number;
    title: string;
    subject: string;
    status: string;
    created_at: string;
    average_score: number;
    total_attempts: number;
    completion_rate: number;
  }>;
  total_count: number;
}























