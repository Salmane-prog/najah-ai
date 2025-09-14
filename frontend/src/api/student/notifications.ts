import { API_BASE_URL } from '../config';

export interface Notification {
  id: number;
  user_id: number;
  title: string;
  message: string;
  type: string;
  priority: string;
  is_read: boolean;
  created_at: string;
  data?: any;
}

export interface NotificationStats {
  total_notifications: number;
  unread_notifications: number;
  read_rate: number;
  by_type: Record<string, number>;
  by_priority: Record<string, number>;
}

class NotificationsAPI {
  private baseURL = `${API_BASE_URL}/notifications-auto`;

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
  // NOTIFICATIONS
  // =====================================================

  async getNotifications(unreadOnly: boolean = false): Promise<Notification[]> {
    return this.request<Notification[]>(`/notifications?unread_only=${unreadOnly}`);
  }

  async markNotificationRead(notificationId: number): Promise<{ message: string }> {
    return this.request<{ message: string }>(`/notifications/${notificationId}/read`, {
      method: 'PUT'
    });
  }

  async markAllNotificationsRead(): Promise<{ message: string }> {
    return this.request<{ message: string }>('/notifications/read-all', {
      method: 'PUT'
    });
  }

  async getUnreadCount(): Promise<{ unread_count: number }> {
    return this.request<{ unread_count: number }>('/notifications/unread-count');
  }

  // =====================================================
  // STATISTIQUES
  // =====================================================

  async getNotificationStats(): Promise<NotificationStats> {
    return this.request<NotificationStats>('/notifications/stats');
  }

  // =====================================================
  // VÉRIFICATIONS AUTOMATIQUES (pour les professeurs)
  // =====================================================

  async triggerNotificationChecks(): Promise<{ message: string }> {
    return this.request<{ message: string }>('/trigger-checks', {
      method: 'POST'
    });
  }

  async sendCustomNotification(notificationData: {
    user_id: number;
    title: string;
    message: string;
    type: string;
    priority?: string;
    data?: any;
  }): Promise<{ message: string; notification_id: number }> {
    return this.request<{ message: string; notification_id: number }>('/send-custom-notification', {
      method: 'POST',
      body: JSON.stringify(notificationData)
    });
  }
}

export const notificationsAPI = new NotificationsAPI(); 