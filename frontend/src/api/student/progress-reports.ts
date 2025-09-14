import { API_BASE_URL } from '../config';

export interface ProgressReport {
  student_id: number;
  student_name: string;
  period: {
    start_date: string;
    end_date: string;
    duration_days: number;
  };
  summary: {
    total_homework: number;
    completed_homework: number;
    overdue_homework: number;
    homework_completion_rate: number;
    study_sessions_count: number;
    total_study_time_hours: number;
    study_consistency: number;
    total_goals: number;
    completed_goals: number;
    active_goals: number;
    goal_achievement_rate: number;
    average_progress: number;
  };
  details: {
    subjects_progress: Record<string, any>;
    study_sessions: any[];
    goals: any[];
  };
  recommendations: string[];
  performance_score: number;
}

export interface ClassProgressReport {
  class_id: number;
  class_name: string;
  period: string;
  start_date: string;
  end_date: string;
  class_summary: {
    total_students: number;
    avg_homework_completion: number;
    avg_study_time: number;
    avg_goal_achievement: number;
    avg_performance_score: number;
  };
  students_progress: ProgressReport[];
}

export interface WeeklyProgress {
  week_start: string;
  week_end: string;
  summary: any;
  performance_score: number;
}

export interface SubjectProgress {
  student_id: number;
  subjects_progress: Record<string, {
    goals_count: number;
    completed_goals: number;
    total_progress: number;
    avg_progress: number;
    study_time_hours: number;
    homework_completion_rate: number;
  }>;
}

export interface PersonalizedRecommendation {
  type: string;
  priority: string;
  title: string;
  description: string;
  action: string;
}

export interface RecommendationsResponse {
  student_id: number;
  recommendations: PersonalizedRecommendation[];
  performance_summary: any;
}

class ProgressReportsAPI {
  private baseURL = `${API_BASE_URL}/progress-reports`;

  private async request<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
    const token = localStorage.getItem('token');
    
    const config: RequestInit = {
      headers: {
        'Content-Type': 'application/json',
        ...(token && { 'Authorization': `Bearer ${token}` }),
        ...options.headers,
      },
      ...options,
    };

    const response = await fetch(`${this.baseURL}${endpoint}`, config);
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return await response.json();
  }

  // =====================================================
  // RAPPORTS DE PROGRESSION
  // =====================================================

  async getStudentProgress(
    studentId: number,
    period: 'weekly' | 'monthly' | 'semester' = 'monthly'
  ): Promise<ProgressReport> {
    return this.request<ProgressReport>(`/student/${studentId}/progress?period=${period}`);
  }

  async getClassProgress(
    classId: number,
    period: 'weekly' | 'monthly' | 'semester' = 'monthly'
  ): Promise<ClassProgressReport> {
    return this.request<ClassProgressReport>(`/class/${classId}/progress?period=${period}`);
  }

  // =====================================================
  // PROGRESSION HEBDOMADAIRE
  // =====================================================

  async getWeeklyProgress(): Promise<{
    student_id: number;
    student_name: string;
    weekly_progress: WeeklyProgress[];
  }> {
    return this.request<{
      student_id: number;
      student_name: string;
      weekly_progress: WeeklyProgress[];
    }>('/weekly-progress');
  }

  // =====================================================
  // PROGRESSION PAR MATIÈRE
  // =====================================================

  async getSubjectProgress(): Promise<SubjectProgress> {
    return this.request<SubjectProgress>('/subject-progress');
  }

  // =====================================================
  // RECOMMANDATIONS PERSONNALISÉES
  // =====================================================

  async getPersonalizedRecommendations(): Promise<RecommendationsResponse> {
    return this.request<RecommendationsResponse>('/recommendations');
  }
}

export const progressReportsAPI = new ProgressReportsAPI(); 