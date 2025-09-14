import { apiClient } from '../utils/api';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// ============================================================================
// INTERFACES POUR LE CALENDRIER
// ============================================================================

export interface CalendarEvent {
  id: number;
  title: string;
  description: string;
  event_type: string;
  start_time: string;
  end_time: string;
  location: string;
  subject: string;
  color: string;
  icon: string;
  created_by: number;
  is_all_day: boolean;
  recurrence: string;
  attendees: number[];
}

export interface ScheduleEvent {
  id: number;
  title: string;
  description: string;
  event_type: string;
  start_time: string;
  end_time: string;
  location: string;
  subject: string;
  color: string;
  icon: string;
  class_id?: number;
  teacher_id?: number;
  student_id?: number;
}

export interface CalendarStats {
  total_events: number;
  upcoming_events: number;
  today_events: number;
  week_events: number;
}

export interface EventFilter {
  start_date?: string;
  end_date?: string;
  event_type?: string;
  subject?: string;
  user_id?: number;
  class_id?: number;
}

// ============================================================================
// FONCTIONS PRINCIPALES
// ============================================================================

export async function getUserCalendarEvents(token: string, userId: number, filter?: EventFilter): Promise<CalendarEvent[]> {
  try {
    console.log('🔄 Récupération des événements du calendrier...');
    
    let url = `${API_BASE_URL}/api/v1/calendar/user/${userId}`;
    if (filter) {
      const params = new URLSearchParams();
      Object.entries(filter).forEach(([key, value]) => {
        if (value) params.append(key, value);
      });
      if (params.toString()) {
        url += `?${params.toString()}`;
      }
    }
    
    const response = await fetch(url, {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });

    if (!response.ok) {
      throw new Error(`Erreur HTTP: ${response.status}`);
    }

    const data = await response.json();
    console.log('✅ Événements du calendrier récupérés:', data);
    return data;

  } catch (error) {
    console.error('❌ Erreur lors de la récupération des événements:', error);
    throw error;
  }
}

export async function getTeacherScheduleEvents(token: string, teacherId: number): Promise<ScheduleEvent[]> {
  try {
    console.log('🔄 Récupération des événements de l\'emploi du temps...');
    
    const response = await fetch(`${API_BASE_URL}/api/v1/schedule/teacher/${teacherId}`, {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });

    if (!response.ok) {
      throw new Error(`Erreur HTTP: ${response.status}`);
    }

    const data = await response.json();
    console.log('✅ Événements de l\'emploi du temps récupérés:', data);
    return data;

  } catch (error) {
    console.error('❌ Erreur lors de la récupération de l\'emploi du temps:', error);
    throw error;
  }
}

export async function getStudentScheduleEvents(token: string, studentId: number): Promise<ScheduleEvent[]> {
  try {
    console.log('🔄 Récupération des événements de l\'emploi du temps étudiant...');
    
    const response = await fetch(`${API_BASE_URL}/api/v1/schedule/student/${studentId}`, {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });

    if (!response.ok) {
      throw new Error(`Erreur HTTP: ${response.status}`);
    }

    const data = await response.json();
    console.log('✅ Événements de l\'emploi du temps étudiant récupérés:', data);
    return data;

  } catch (error) {
    console.error('❌ Erreur lors de la récupération de l\'emploi du temps étudiant:', error);
    throw error;
  }
}

export async function getClassScheduleEvents(token: string, classId: number): Promise<ScheduleEvent[]> {
  try {
    console.log('🔄 Récupération des événements de l\'emploi du temps de la classe...');
    
    const response = await fetch(`${API_BASE_URL}/api/v1/schedule/class/${classId}`, {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });

    if (!response.ok) {
      throw new Error(`Erreur HTTP: ${response.status}`);
    }

    const data = await response.json();
    console.log('✅ Événements de l\'emploi du temps de la classe récupérés:', data);
    return data;

  } catch (error) {
    console.error('❌ Erreur lors de la récupération de l\'emploi du temps de la classe:', error);
    throw error;
  }
}

export async function getCalendarStats(token: string, userId: number): Promise<CalendarStats> {
  try {
    console.log('🔄 Récupération des statistiques du calendrier...');
    
    const response = await fetch(`${API_BASE_URL}/api/v1/calendar/stats/${userId}`, {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });

    if (!response.ok) {
      throw new Error(`Erreur HTTP: ${response.status}`);
    }

    const data = await response.json();
    console.log('✅ Statistiques du calendrier récupérées:', data);
    return data;

  } catch (error) {
    console.error('❌ Erreur lors de la récupération des statistiques:', error);
    throw error;
  }
}

export async function createCalendarEvent(token: string, eventData: any): Promise<CalendarEvent> {
  try {
    console.log('🔄 Création d\'un événement...');
    
    const response = await fetch(`${API_BASE_URL}/api/v1/calendar/`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(eventData)
    });

    if (!response.ok) {
      throw new Error(`Erreur HTTP: ${response.status}`);
    }

    const data = await response.json();
    console.log('✅ Événement créé avec succès:', data);
    return data;

  } catch (error) {
    console.error('❌ Erreur lors de la création de l\'événement:', error);
    throw error;
  }
}

export async function updateCalendarEvent(token: string, eventId: number, eventData: any): Promise<CalendarEvent> {
  try {
    console.log('🔄 Mise à jour de l\'événement...');
    
    const response = await fetch(`${API_BASE_URL}/api/v1/calendar/${eventId}`, {
      method: 'PUT',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(eventData)
    });

    if (!response.ok) {
      throw new Error(`Erreur HTTP: ${response.status}`);
    }

    const data = await response.json();
    console.log('✅ Événement mis à jour avec succès:', data);
    return data;

  } catch (error) {
    console.error('❌ Erreur lors de la mise à jour de l\'événement:', error);
    throw error;
  }
}

export async function deleteCalendarEvent(token: string, eventId: number): Promise<void> {
  try {
    console.log('🔄 Suppression de l\'événement...');
    
    const response = await fetch(`${API_BASE_URL}/api/v1/calendar/${eventId}`, {
      method: 'DELETE',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });

    if (!response.ok) {
      throw new Error(`Erreur HTTP: ${response.status}`);
    }

    console.log('✅ Événement supprimé avec succès');

  } catch (error) {
    console.error('❌ Erreur lors de la suppression de l\'événement:', error);
    throw error;
  }
}

// ============================================================================
// FONCTIONS DE FALLBACK (DONNÉES MOCKÉES EN CAS D'ERREUR)
// ============================================================================

export function getMockCalendarEvents(): CalendarEvent[] {
  return [
    {
      id: 1,
      title: "Cours de Mathématiques",
      description: "Cours sur les fractions et décimaux",
      event_type: "course",
      start_time: new Date(Date.now() + 3600000).toISOString(),
      end_time: new Date(Date.now() + 7200000).toISOString(),
      location: "Salle 101",
      subject: "Mathématiques",
      color: "#3B82F6",
      icon: "book",
      created_by: 1,
      is_all_day: false,
      recurrence: "weekly",
      attendees: [1, 2, 3, 4, 5]
    },
    {
      id: 2,
      title: "Réunion des professeurs",
      description: "Réunion hebdomadaire de l'équipe pédagogique",
      event_type: "meeting",
      start_time: new Date(Date.now() + 86400000).toISOString(),
      end_time: new Date(Date.now() + 90000000).toISOString(),
      location: "Salle des professeurs",
      subject: "Général",
      color: "#10B981",
      icon: "users",
      created_by: 1,
      is_all_day: false,
      recurrence: "weekly",
      attendees: [1, 6, 7, 8]
    }
  ];
}

export function getMockScheduleEvents(): ScheduleEvent[] {
  return [
    {
      id: 1,
      title: "Mathématiques 6ème A",
      description: "Cours sur les fractions",
      event_type: "course",
      start_time: "08:00:00",
      end_time: "09:00:00",
      location: "Salle 101",
      subject: "Mathématiques",
      color: "#3B82F6",
      icon: "book",
      class_id: 1,
      teacher_id: 1
    },
    {
      id: 2,
      title: "Français 6ème A",
      description: "Cours de grammaire",
      event_type: "course",
      start_time: "09:00:00",
      end_time: "10:00:00",
      location: "Salle 102",
      subject: "Français",
      color: "#EF4444",
      icon: "book",
      class_id: 1,
      teacher_id: 2
    }
  ];
}

export function getMockCalendarStats(): CalendarStats {
  return {
    total_events: 15,
    upcoming_events: 8,
    today_events: 3,
    week_events: 12
  };
}

// ============================================================================
// FONCTIONS AVEC FALLBACK
// ============================================================================

export async function getUserCalendarEventsWithFallback(token: string, userId: number, filter?: EventFilter): Promise<CalendarEvent[]> {
  try {
    return await getUserCalendarEvents(token, userId, filter);
  } catch (error) {
    console.warn('⚠️ Utilisation des données de fallback pour le calendrier:', error);
    return getMockCalendarEvents();
  }
}

export async function getTeacherScheduleEventsWithFallback(token: string, teacherId: number): Promise<ScheduleEvent[]> {
  try {
    return await getTeacherScheduleEvents(token, teacherId);
  } catch (error) {
    console.warn('⚠️ Utilisation des données de fallback pour l\'emploi du temps:', error);
    return getMockScheduleEvents();
  }
}

export async function getStudentScheduleEventsWithFallback(token: string, studentId: number): Promise<ScheduleEvent[]> {
  try {
    return await getStudentScheduleEvents(token, studentId);
  } catch (error) {
    console.warn('⚠️ Utilisation des données de fallback pour l\'emploi du temps étudiant:', error);
    return getMockScheduleEvents();
  }
}

export async function getCalendarStatsWithFallback(token: string, userId: number): Promise<CalendarStats> {
  try {
    return await getCalendarStats(token, userId);
  } catch (error) {
    console.warn('⚠️ Utilisation des données de fallback pour les statistiques:', error);
    return getMockCalendarStats();
  }
}
