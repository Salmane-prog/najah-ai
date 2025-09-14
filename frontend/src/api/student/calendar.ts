import { apiClient } from '../apiClient';

export interface CalendarEvent {
  id: number;
  title: string;
  description?: string;
  event_type: 'course' | 'exam' | 'homework' | 'study_session' | 'reminder';
  start_time: string;
  end_time?: string;
  location?: string;
  subject?: string;
  color: string;
  is_recurring: boolean;
  recurrence_pattern?: any;
  class_id?: number;
  created_by: number;
  created_at: string;
}

export interface StudySession {
  id: number;
  title: string;
  description?: string;
  subject?: string;
  start_time: string;
  end_time?: string;
  duration?: number;
  goals?: string[];
  completed: boolean;
  notes?: string;
  student_id: number;
  created_at: string;
}

export interface EventReminder {
  id: number;
  event_id: number;
  user_id: number;
  reminder_time: string;
  reminder_type: 'notification' | 'email' | 'sms';
  is_sent: boolean;
  sent_at?: string;
  created_at: string;
}

export interface CreateCalendarEventData {
  title: string;
  description?: string;
  event_type: 'course' | 'exam' | 'homework' | 'study_session' | 'reminder';
  start_time: string;
  end_time?: string;
  location?: string;
  subject?: string;
  color?: string;
  is_recurring?: boolean;
  recurrence_pattern?: any;
  class_id?: number;
}

export interface CreateStudySessionData {
  title: string;
  description?: string;
  subject?: string;
  start_time: string;
  end_time?: string;
  duration?: number;
  goals?: string[];
  notes?: string;
}

export interface CreateReminderData {
  event_id: number;
  reminder_time: string;
  reminder_type?: 'notification' | 'email' | 'sms';
}

class CalendarAPI {
  // Récupérer tous les événements
  async getCalendarEvents(
    start_date?: string,
    end_date?: string,
    event_type?: string,
    subject?: string,
    class_id?: number
  ): Promise<CalendarEvent[]> {
    const params = new URLSearchParams();
    if (start_date) params.append('start_date', start_date);
    if (end_date) params.append('end_date', end_date);
    if (event_type) params.append('event_type', event_type);
    if (subject) params.append('subject', subject);
    if (class_id) params.append('class_id', class_id.toString());
    
    return this.request(`/api/v1/calendar/events?${params.toString()}`);
  }

  // Récupérer un événement spécifique
  async getCalendarEvent(eventId: number): Promise<CalendarEvent> {
    return this.request(`/api/v1/calendar/events/${eventId}`);
  }

  // Créer un nouvel événement
  async createCalendarEvent(data: CreateCalendarEventData): Promise<CalendarEvent> {
    return this.request('/api/v1/calendar/events', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  // Mettre à jour un événement
  async updateCalendarEvent(eventId: number, data: Partial<CreateCalendarEventData>): Promise<CalendarEvent> {
    return this.request(`/api/v1/calendar/events/${eventId}`, {
      method: 'PUT',
      body: JSON.stringify(data),
    });
  }

  // Supprimer un événement
  async deleteCalendarEvent(eventId: number): Promise<void> {
    return this.request(`/api/v1/calendar/events/${eventId}`, {
      method: 'DELETE',
    });
  }

  // Récupérer toutes les sessions d'étude
  async getStudySessions(
    start_date?: string,
    end_date?: string,
    subject?: string,
    completed?: boolean
  ): Promise<StudySession[]> {
    const params = new URLSearchParams();
    if (start_date) params.append('start_date', start_date);
    if (end_date) params.append('end_date', end_date);
    if (subject) params.append('subject', subject);
    if (completed !== undefined) params.append('completed', completed.toString());
    
    return this.request(`/api/v1/calendar/study-sessions?${params.toString()}`);
  }

  // Créer une nouvelle session d'étude
  async createStudySession(data: CreateStudySessionData): Promise<StudySession> {
    return this.request('/api/v1/calendar/study-sessions', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  // Marquer une session d'étude comme terminée
  async completeStudySession(sessionId: number): Promise<StudySession> {
    return this.request(`/api/v1/calendar/study-sessions/${sessionId}/complete`, {
      method: 'PUT',
    });
  }

  // Créer un rappel pour un événement
  async createEventReminder(data: CreateReminderData): Promise<EventReminder> {
    return this.request(`/api/v1/calendar/events/${data.event_id}/reminders`, {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  private async request<T>(endpoint: string, options?: RequestInit): Promise<T> {
    const response = await apiClient.request<T>(endpoint, options);
    return response.data;
  }
}

export const calendarAPI = new CalendarAPI();
