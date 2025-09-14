import { apiClient } from '../utils/api';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// ============================================================================
// INTERFACES POUR LES MESSAGES ET NOTIFICATIONS
// ============================================================================

export interface Message {
  id: number;
  sender_id: number;
  recipient_id: number;
  subject: string;
  content: string;
  is_read: boolean;
  created_at: string;
  updated_at: string;
  sender_name: string;
  sender_email: string;
  recipient_name: string;
  recipient_email: string;
}

export interface Notification {
  id: number;
  user_id: number;
  type: string;
  title: string;
  message: string;
  is_read: boolean;
  created_at: string;
  data: any;
  action_url?: string;
}

export interface Conversation {
  id: number;
  participants: number[];
  last_message: Message;
  unread_count: number;
  participant_names: string[];
}

export interface MessagingStats {
  total_messages: number;
  unread_messages: number;
  total_notifications: number;
  unread_notifications: number;
}

// ============================================================================
// FONCTIONS PRINCIPALES
// ============================================================================

export async function getUserMessages(token: string, userId: number): Promise<Message[]> {
  try {
    console.log('🔄 Récupération des messages de l\'utilisateur...');
    
    const response = await fetch(`${API_BASE_URL}/api/v1/messages/user/${userId}`, {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });

    if (!response.ok) {
      throw new Error(`Erreur HTTP: ${response.status}`);
    }

    const data = await response.json();
    console.log('✅ Messages récupérés:', data);
    return data;

  } catch (error) {
    console.error('❌ Erreur lors de la récupération des messages:', error);
    throw error;
  }
}

export async function getUserNotifications(token: string, userId: number): Promise<Notification[]> {
  try {
    console.log('🔄 Récupération des notifications de l\'utilisateur...');
    
    const response = await fetch(`${API_BASE_URL}/api/v1/notifications/user/${userId}`, {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });

    if (!response.ok) {
      throw new Error(`Erreur HTTP: ${response.status}`);
    }

    const data = await response.json();
    console.log('✅ Notifications récupérées:', data);
    return data;

  } catch (error) {
    console.error('❌ Erreur lors de la récupération des notifications:', error);
    throw error;
  }
}

export async function getConversations(token: string, userId: number): Promise<Conversation[]> {
  try {
    console.log('🔄 Récupération des conversations de l\'utilisateur...');
    
    const response = await fetch(`${API_BASE_URL}/api/v1/messages/conversations/${userId}`, {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });

    if (!response.ok) {
      throw new Error(`Erreur HTTP: ${response.status}`);
    }

    const data = await response.json();
    console.log('✅ Conversations récupérées:', data);
    return data;

  } catch (error) {
    console.error('❌ Erreur lors de la récupération des conversations:', error);
    throw error;
  }
}

export async function getMessagingStats(token: string, userId: number): Promise<MessagingStats> {
  try {
    console.log('🔄 Récupération des statistiques de messagerie...');
    
    const response = await fetch(`${API_BASE_URL}/api/v1/messages/stats/${userId}`, {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });

    if (!response.ok) {
      throw new Error(`Erreur HTTP: ${response.status}`);
    }

    const data = await response.json();
    console.log('✅ Statistiques de messagerie récupérées:', data);
    return data;

  } catch (error) {
    console.error('❌ Erreur lors de la récupération des statistiques:', error);
    throw error;
  }
}

export async function sendMessage(token: string, messageData: any): Promise<Message> {
  try {
    console.log('🔄 Envoi d\'un message...');
    
    const response = await fetch(`${API_BASE_URL}/api/v1/messages/`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(messageData)
    });

    if (!response.ok) {
      throw new Error(`Erreur HTTP: ${response.status}`);
    }

    const data = await response.json();
    console.log('✅ Message envoyé avec succès:', data);
    return data;

  } catch (error) {
    console.error('❌ Erreur lors de l\'envoi du message:', error);
    throw error;
  }
}

export async function markMessageAsRead(token: string, messageId: number): Promise<void> {
  try {
    console.log('🔄 Marquage du message comme lu...');
    
    const response = await fetch(`${API_BASE_URL}/api/v1/messages/${messageId}/read`, {
      method: 'PUT',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });

    if (!response.ok) {
      throw new Error(`Erreur HTTP: ${response.status}`);
    }

    console.log('✅ Message marqué comme lu');

  } catch (error) {
    console.error('❌ Erreur lors du marquage du message:', error);
    throw error;
  }
}

export async function markNotificationAsRead(token: string, notificationId: number): Promise<void> {
  try {
    console.log('🔄 Marquage de la notification comme lue...');
    
    const response = await fetch(`${API_BASE_URL}/api/v1/notifications/${notificationId}/read`, {
      method: 'PUT',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });

    if (!response.ok) {
      throw new Error(`Erreur HTTP: ${response.status}`);
    }

    console.log('✅ Notification marquée comme lue');

  } catch (error) {
    console.error('❌ Erreur lors du marquage de la notification:', error);
    throw error;
  }
}

// ============================================================================
// FONCTIONS DE FALLBACK (DONNÉES MOCKÉES EN CAS D'ERREUR)
// ============================================================================

export function getMockMessages(): Message[] {
  return [
    {
      id: 1,
      sender_id: 1,
      recipient_id: 2,
      subject: "Question sur le quiz",
      content: "Bonjour, j'ai une question sur le quiz de mathématiques...",
      is_read: false,
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
      sender_name: "Prof. Martin",
      sender_email: "prof.martin@example.com",
      recipient_name: "Étudiant 1",
      recipient_email: "etudiant1@example.com"
    },
    {
      id: 2,
      sender_id: 2,
      recipient_id: 1,
      subject: "Réponse à votre question",
      content: "Merci pour votre question. Voici la réponse...",
      is_read: true,
      created_at: new Date(Date.now() - 3600000).toISOString(),
      updated_at: new Date(Date.now() - 3600000).toISOString(),
      sender_name: "Étudiant 1",
      sender_email: "etudiant1@example.com",
      recipient_name: "Prof. Martin",
      recipient_email: "prof.martin@example.com"
    }
  ];
}

export function getMockNotifications(): Notification[] {
  return [
    {
      id: 1,
      user_id: 1,
      type: "quiz_assignment",
      title: "Nouveau quiz assigné",
      message: "Un nouveau quiz de mathématiques vous a été assigné",
      is_read: false,
      created_at: new Date().toISOString(),
      data: { quiz_id: 1, subject: "Mathématiques" },
      action_url: "/dashboard/student/quiz/1"
    },
    {
      id: 2,
      user_id: 1,
      type: "badge_earned",
      title: "Badge obtenu !",
      message: "Félicitations ! Vous avez obtenu le badge 'Quiz Master'",
      is_read: true,
      created_at: new Date(Date.now() - 7200000).toISOString(),
      data: { badge_id: 1, badge_name: "Quiz Master" },
      action_url: "/dashboard/student/badges"
    }
  ];
}

export function getMockConversations(): Conversation[] {
  return [
    {
      id: 1,
      participants: [1, 2],
      last_message: {
        id: 2,
        sender_id: 2,
        recipient_id: 1,
        subject: "Réponse à votre question",
        content: "Merci pour votre question. Voici la réponse...",
        is_read: true,
        created_at: new Date(Date.now() - 3600000).toISOString(),
        updated_at: new Date(Date.now() - 3600000).toISOString(),
        sender_name: "Étudiant 1",
        sender_email: "etudiant1@example.com",
        recipient_name: "Prof. Martin",
        recipient_email: "prof.martin@example.com"
      },
      unread_count: 0,
      participant_names: ["Prof. Martin", "Étudiant 1"]
    }
  ];
}

export function getMockMessagingStats(): MessagingStats {
  return {
    total_messages: 15,
    unread_messages: 3,
    total_notifications: 8,
    unread_notifications: 2
  };
}

// ============================================================================
// FONCTIONS AVEC FALLBACK
// ============================================================================

export async function getUserMessagesWithFallback(token: string, userId: number): Promise<Message[]> {
  try {
    return await getUserMessages(token, userId);
  } catch (error) {
    console.warn('⚠️ Utilisation des données de fallback pour les messages:', error);
    return getMockMessages();
  }
}

export async function getUserNotificationsWithFallback(token: string, userId: number): Promise<Notification[]> {
  try {
    return await getUserNotifications(token, userId);
  } catch (error) {
    console.warn('⚠️ Utilisation des données de fallback pour les notifications:', error);
    return getMockNotifications();
  }
}

export async function getConversationsWithFallback(token: string, userId: number): Promise<Conversation[]> {
  try {
    return await getConversations(token, userId);
  } catch (error) {
    console.warn('⚠️ Utilisation des données de fallback pour les conversations:', error);
    return getMockConversations();
  }
}

export async function getMessagingStatsWithFallback(token: string, userId: number): Promise<MessagingStats> {
  try {
    return await getMessagingStats(token, userId);
  } catch (error) {
    console.warn('⚠️ Utilisation des données de fallback pour les statistiques:', error);
    return getMockMessagingStats();
  }
}
