import { apiClient } from '../apiClient';

export interface Homework {
  id: number;
  title: string;
  description?: string;
  subject: string;
  class_id?: number;
  due_date: string;
  priority: 'low' | 'medium' | 'high';
  estimated_time?: number;
  max_score: number;
  instructions?: string;
  attachments?: string[];
  created_by: number;
  created_at: string;
  submissions_count?: number;
}

export interface HomeworkSubmission {
  id: number;
  homework_id: number;
  student_id: number;
  submitted_at: string;
  content?: string;
  attachments?: string[];
  score?: number;
  max_score?: number;
  feedback?: string;
  status: 'submitted' | 'graded' | 'late';
}

export interface CreateHomeworkData {
  title: string;
  description?: string;
  subject: string;
  class_id?: number;
  due_date: string;
  priority?: 'low' | 'medium' | 'high';
  estimated_time?: number;
  max_score?: number;
  instructions?: string;
  attachments?: string[];
}

export interface UpdateHomeworkData {
  title?: string;
  description?: string;
  subject?: string;
  due_date?: string;
  priority?: 'low' | 'medium' | 'high';
  estimated_time?: number;
  max_score?: number;
  instructions?: string;
  attachments?: string[];
}

export interface SubmitHomeworkData {
  content?: string;
  attachments?: string[];
}

export interface GradeSubmissionData {
  score?: number;
  feedback?: string;
  status?: 'submitted' | 'graded' | 'late';
}

class HomeworkAPI {
  // Récupérer tous les devoirs
  async getHomeworks(subject?: string, class_id?: number, status?: string): Promise<Homework[]> {
    const params = new URLSearchParams();
    if (subject) params.append('subject', subject);
    if (class_id) params.append('class_id', class_id.toString());
    if (status) params.append('status', status);
    
    return this.request(`/api/v1/homework?${params.toString()}`);
  }

  // Récupérer un devoir spécifique
  async getHomework(homeworkId: number): Promise<Homework> {
    return this.request(`/api/v1/homework/${homeworkId}`);
  }

  // Créer un nouveau devoir (professeur uniquement)
  async createHomework(data: CreateHomeworkData): Promise<Homework> {
    return this.request('/api/v1/homework', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  // Mettre à jour un devoir
  async updateHomework(homeworkId: number, data: UpdateHomeworkData): Promise<Homework> {
    return this.request(`/api/v1/homework/${homeworkId}`, {
      method: 'PUT',
      body: JSON.stringify(data),
    });
  }

  // Supprimer un devoir
  async deleteHomework(homeworkId: number): Promise<void> {
    return this.request(`/api/v1/homework/${homeworkId}`, {
      method: 'DELETE',
    });
  }

  // Soumettre un devoir
  async submitHomework(homeworkId: number, data: SubmitHomeworkData): Promise<HomeworkSubmission> {
    return this.request(`/api/v1/homework/${homeworkId}/submit`, {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  // Récupérer les soumissions d'un devoir
  async getHomeworkSubmissions(homeworkId: number): Promise<HomeworkSubmission[]> {
    return this.request(`/api/v1/homework/${homeworkId}/submissions`);
  }

  // Noter une soumission
  async gradeSubmission(submissionId: number, data: GradeSubmissionData): Promise<HomeworkSubmission> {
    return this.request(`/api/v1/homework/submissions/${submissionId}/grade`, {
      method: 'PUT',
      body: JSON.stringify(data),
    });
  }

  private async request<T>(endpoint: string, options?: RequestInit): Promise<T> {
    const response = await apiClient.request<T>(endpoint, options);
    return response.data;
  }
}

export const homeworkAPI = new HomeworkAPI();