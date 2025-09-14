import { API_BASE_URL } from '../config';

export interface Homework {
  id: number;
  title: string;
  description: string;
  subject: string;
  due_date: string;
  priority: 'high' | 'medium' | 'low';
  status: 'pending' | 'in_progress' | 'completed';
  estimated_time: number; // en minutes
  actual_time?: number;
  tags: string[];
  attachments?: string[];
}

export interface StudySession {
  id: number;
  title: string;
  subject: string;
  start_time: string;
  end_time: string;
  duration: number; // en minutes
  goals: string[];
  completed: boolean;
  notes?: string;
}

export interface Reminder {
  id: number;
  title: string;
  message: string;
  due_date: string;
  priority: 'high' | 'medium' | 'low';
  is_active: boolean;
  repeat: 'none' | 'daily' | 'weekly' | 'monthly';
}

export interface LearningGoal {
  id: number;
  title: string;
  description: string;
  subject: string;
  target_date: string;
  progress: number; // 0-100
  status: 'not_started' | 'in_progress' | 'completed';
  milestones: Milestone[];
}

export interface Milestone {
  id: number;
  title: string;
  completed: boolean;
  due_date: string;
}

export interface CalendarEvent {
  id: number;
  title: string;
  type: 'homework' | 'study_session' | 'reminder' | 'goal';
  date: string;
  time?: string;
  color: string;
  priority?: 'high' | 'medium' | 'low';
}

export interface CreateHomeworkRequest {
  title: string;
  description: string;
  subject: string;
  due_date: string;
  priority: 'high' | 'medium' | 'low';
  estimated_time: number;
  tags: string[];
}

export interface CreateStudySessionRequest {
  title: string;
  subject: string;
  start_time: string;
  end_time: string;
  goals: string[];
}

export interface CreateReminderRequest {
  title: string;
  message: string;
  due_date: string;
  priority: 'high' | 'medium' | 'low';
  repeat: 'none' | 'daily' | 'weekly' | 'monthly';
}

export interface CreateLearningGoalRequest {
  title: string;
  description: string;
  subject: string;
  target_date: string;
  milestones: Omit<Milestone, 'id'>[];
}

class OrganizationAPI {
  private baseURL: string;

  constructor() {
    this.baseURL = API_BASE_URL;
  }

  // ===== DEVOIRS =====

  // Récupérer tous les devoirs
  async getHomeworks(subject?: string, status?: string): Promise<Homework[]> {
    try {
      // Récupérer l'ID de l'utilisateur connecté
      const user = localStorage.getItem('najah_user');
      if (!user) {
        throw new Error('Utilisateur non connecté');
      }
      
      const userData = JSON.parse(user);
      const studentId = userData.id;
      
      const params = new URLSearchParams();
      if (subject) params.append('subject', subject);
      if (status) params.append('status', status);
      
      // Utiliser l'endpoint des devoirs assignés
      const response = await fetch(`${this.baseURL}/assignments/homework/assigned/${studentId}?${params.toString()}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('najah_token')}`
        }
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const assignments = await response.json();
      
      // Transformer les assignments en format Homework
      return assignments.map((assignment: any) => ({
        id: assignment.id,
        title: assignment.title,
        description: assignment.description,
        subject: assignment.subject,
        due_date: assignment.due_date,
        priority: assignment.priority,
        status: assignment.status,
        estimated_time: assignment.estimated_time || 0,
        tags: [],
        attachments: assignment.attachment ? [assignment.attachment.name] : []
      }));
    } catch (error) {
      console.error('Error fetching homeworks:', error);
      throw error;
    }
  }

  // Créer un nouveau devoir
  async createHomework(data: CreateHomeworkRequest): Promise<Homework> {
    try {
      const response = await fetch(`${this.baseURL}/organization/homework`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('najah_token')}`
        },
        body: JSON.stringify(data)
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error creating homework:', error);
      throw error;
    }
  }

  // Mettre à jour un devoir
  async updateHomework(homeworkId: number, data: Partial<Homework>): Promise<Homework> {
    try {
      const response = await fetch(`${this.baseURL}/organization/homework`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('najah_token')}`
        },
        body: JSON.stringify(data)
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error updating homework:', error);
      throw error;
    }
  }

  // Supprimer un devoir
  async deleteHomework(homeworkId: number): Promise<void> {
    try {
      const response = await fetch(`${this.baseURL}/organization/homework/${homeworkId}`, {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('najah_token')}`
        }
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
    } catch (error) {
      console.error('Error deleting homework:', error);
      throw error;
    }
  }

  // ===== SESSIONS D'ÉTUDE =====

  // Récupérer toutes les sessions d'étude
  async getStudySessions(subject?: string): Promise<StudySession[]> {
    try {
      const params = new URLSearchParams();
      if (subject) params.append('subject', subject);

      const response = await fetch(`${this.baseURL}/organization/study-sessions?${params}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('najah_token')}`
        }
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error fetching study sessions:', error);
      throw error;
    }
  }

  // Créer une nouvelle session d'étude
  async createStudySession(data: any): Promise<StudySession> {
    try {
      const response = await fetch(`${this.baseURL}/organization/study-sessions`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('najah_token')}`
        },
        body: JSON.stringify(data)
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error creating study session:', error);
      throw error;
    }
  }

  // Marquer une session comme terminée
  async completeStudySession(sessionId: number): Promise<void> {
    try {
      const response = await fetch(`${this.baseURL}/organization/study-sessions/${sessionId}/complete`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('najah_token')}`
        }
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
    } catch (error) {
      console.error('Error completing study session:', error);
      throw error;
    }
  }

  // ===== RAPPELS =====

  // Récupérer tous les rappels
  async getReminders(): Promise<Reminder[]> {
    try {
      const response = await fetch(`${this.baseURL}/organization/reminders`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('najah_token')}`
        }
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error fetching reminders:', error);
      throw error;
    }
  }

  // Créer un nouveau rappel
  async createReminder(data: CreateReminderRequest): Promise<Reminder> {
    try {
      const response = await fetch(`${this.baseURL}/organization/reminders`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('najah_token')}`
        },
        body: JSON.stringify(data)
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error creating reminder:', error);
      throw error;
    }
  }

  // Activer/désactiver un rappel
  async toggleReminder(reminderId: number): Promise<void> {
    try {
      const response = await fetch(`${this.baseURL}/organization/reminders/${reminderId}/toggle`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('najah_token')}`
        }
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
    } catch (error) {
      console.error('Error toggling reminder:', error);
      throw error;
    }
  }

  // ===== OBJECTIFS D'APPRENTISSAGE =====

  // Récupérer tous les objectifs
  async getLearningGoals(subject?: string): Promise<LearningGoal[]> {
    try {
      const params = new URLSearchParams();
      if (subject) params.append('subject', subject);

      const response = await fetch(`${this.baseURL}/organization/learning-goals?${params}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('najah_token')}`
        }
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error fetching learning goals:', error);
      throw error;
    }
  }

  // Créer un nouvel objectif
  async createLearningGoal(data: CreateLearningGoalRequest): Promise<LearningGoal> {
    try {
      const response = await fetch(`${this.baseURL}/organization/learning-goals`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('najah_token')}`
        },
        body: JSON.stringify(data)
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error creating learning goal:', error);
      throw error;
    }
  }

  // Marquer une étape comme terminée
  async completeMilestone(goalId: number, milestoneId: number): Promise<void> {
    try {
      const response = await fetch(`${this.baseURL}/organization/learning-goals/${goalId}/milestones/${milestoneId}/complete`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('najah_token')}`
        }
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
    } catch (error) {
      console.error('Error completing milestone:', error);
      throw error;
    }
  }

  // ===== CALENDRIER =====

  // Récupérer les événements du calendrier
  async getCalendarEvents(startDate?: string, endDate?: string): Promise<CalendarEvent[]> {
    try {
      const params = new URLSearchParams();
      if (startDate) params.append('start_date', startDate);
      if (endDate) params.append('end_date', endDate);

      const response = await fetch(`${this.baseURL}/organization/calendar?${params}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('najah_token')}`
        }
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error fetching calendar events:', error);
      throw error;
    }
  }

  // Créer un événement du calendrier
  async createCalendarEvent(eventData: {
    title: string;
    description?: string;
    event_type: string;
    start_date: string;
    end_date?: string;
    location?: string;
    color?: string;
    priority?: string;
    all_day?: boolean;
  }): Promise<CalendarEvent> {
    try {
      const response = await fetch(`${this.baseURL}/organization/calendar`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('najah_token')}`
        },
        body: JSON.stringify(eventData)
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error creating calendar event:', error);
      throw error;
    }
  }

  // ===== STATISTIQUES =====

  // Récupérer les statistiques d'organisation
  async getOrganizationStats(): Promise<{
    total_homeworks: number;
    total_study_sessions: number;
    completed_sessions: number;
    total_goals: number;
    completed_goals: number;
    active_reminders: number;
  }> {
    try {
      const response = await fetch(`${this.baseURL}/organization/stats`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('najah_token')}`
        }
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error fetching organization stats:', error);
      throw error;
    }
  }

  // Récupérer les statistiques de temps d'étude
  async getStudyTimeStats(period: 'week' | 'month' | 'year' = 'week'): Promise<{
    total_time: number;
    average_per_session: number;
    sessions_count: number;
    subject_breakdown: { subject: string; time: number }[];
  }> {
    try {
      const response = await fetch(`${this.baseURL}/organization/study-time-stats?period=${period}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('najah_token')}`
        }
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error fetching study time stats:', error);
      throw error;
    }
  }
}

export const organizationAPI = new OrganizationAPI(); 