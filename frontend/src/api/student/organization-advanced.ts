import { API_BASE_URL } from '../config';

export interface CalendarEvent {
  id: string;
  title: string;
  start: string;
  end: string;
  type: 'homework' | 'study_session' | 'reminder';
  priority?: string;
  color: string;
}

export interface ProductivityAnalytics {
  study_time_hours: number;
  avg_productivity: number;
  homework_completion_rate: number;
  sessions_count: number;
  homework_count: number;
}

export interface PriorityTask {
  type: string;
  title: string;
  priority: string;
  days_left: number;
  estimated_time?: number;
}

export interface Achievement {
  id: string;
  title: string;
  description: string;
  icon: string;
  unlocked: boolean;
  progress: number;
}

export class OrganizationAdvancedAPI {
  private baseURL = `http://localhost:8000/organization-advanced`;

  // =====================================================
  // CALENDRIER INTELLIGENT
  // =====================================================

  async getCalendarEvents(startDate: string, endDate: string): Promise<CalendarEvent[]> {
    try {
      const params = new URLSearchParams({
        start_date: startDate,
        end_date: endDate
      });

      const response = await fetch(`${this.baseURL}/calendar/events?${params}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json'
        }
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Erreur lors de la récupération des événements du calendrier:', error);
      throw error;
    }
  }

  // =====================================================
  // ANALYTICS DE PRODUCTIVITÉ
  // =====================================================

  async getProductivityAnalytics(days: number = 30): Promise<ProductivityAnalytics> {
    try {
      const params = new URLSearchParams({
        days: days.toString()
      });

      const response = await fetch(`${this.baseURL}/analytics/productivity?${params}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json'
        }
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Erreur lors de la récupération des analytics:', error);
      throw error;
    }
  }

  // =====================================================
  // RECOMMANDATIONS IA
  // =====================================================

  async getPriorityTaskRecommendations(): Promise<{
    recommendations: PriorityTask[];
    total_urgent: number;
  }> {
    try {
      const response = await fetch(`${this.baseURL}/recommendations/priority-tasks`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json'
        }
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Erreur lors de la récupération des recommandations:', error);
      throw error;
    }
  }

  // =====================================================
  // GAMIFICATION
  // =====================================================

  async getUserAchievements(): Promise<{
    achievements: Achievement[];
    total_unlocked: number;
    total_available: number;
  }> {
    try {
      const response = await fetch(`${this.baseURL}/gamification/achievements`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json'
        }
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Erreur lors de la récupération des achievements:', error);
      throw error;
    }
  }
}

// Instance singleton
export const organizationAdvancedAPI = new OrganizationAdvancedAPI(); 