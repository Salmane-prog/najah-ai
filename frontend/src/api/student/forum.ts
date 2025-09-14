import { API_BASE_URL } from '../config';

export interface ForumCategory {
  id: number;
  name: string;
  description: string;
  thread_count: number;
  color: string;
}

export interface ForumThread {
  id: number;
  title: string;
  content: string;
  author: {
    id: number;
    name: string;
    avatar?: string;
  };
  category: string;
  tags: string[];
  created_at: string;
  replies_count: number;
  views_count: number;
  is_pinned: boolean;
  is_locked: boolean;
  votes: {
    up: number;
    down: number;
  };
}

export interface ForumMessage {
  id: number;
  content: string;
  author: {
    id: number;
    name: string;
    avatar?: string;
  };
  created_at: string;
  votes: {
    up: number;
    down: number;
  };
  is_solution: boolean;
}

export interface CreateThreadRequest {
  title: string;
  content: string;
  category_id: number;
  tags: string[];
}

export interface CreateMessageRequest {
  content: string;
  thread_id: number;
}

export interface VoteRequest {
  message_id: number;
  vote_type: 'up' | 'down';
}

export interface ReportRequest {
  thread_id?: number;
  message_id?: number;
  reason: string;
}

class ForumAPI {
  // CORRECTION: Utiliser le bon préfixe d'API
  private baseURL = `${API_BASE_URL}/forum`;

  // Récupérer toutes les catégories
  async getCategories(): Promise<ForumCategory[]> {
    try {
      const response = await fetch(`${this.baseURL}/categories`, {
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
      console.error('Error fetching forum categories:', error);
      throw error;
    }
  }

  // Récupérer tous les threads
  async getThreads(categoryId?: number, searchTerm?: string, limit: number = 20, offset: number = 0): Promise<ForumThread[]> {
    try {
      const params = new URLSearchParams();
      
      if (categoryId) params.append('category_id', categoryId.toString());
      if (searchTerm) params.append('search', searchTerm);
      if (limit) params.append('limit', limit.toString());
      if (offset) params.append('offset', offset.toString());

      const response = await fetch(`${this.baseURL}/threads?${params.toString()}`, {
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
      console.error('Error fetching forum threads:', error);
      throw error;
    }
  }

  // Créer un nouveau thread
  async createThread(threadData: any): Promise<ForumThread> {
    try {
      const response = await fetch(`${this.baseURL}/threads`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('najah_token')}`
        },
        body: JSON.stringify(threadData)
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error creating forum thread:', error);
      throw error;
    }
  }

  // Créer une réponse à un thread
  async createReply(threadId: number, replyData: { content: string }): Promise<ForumMessage> {
    try {
      const response = await fetch(`${this.baseURL}/threads/${threadId}/replies`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('najah_token')}`
        },
        body: JSON.stringify(replyData)
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error creating forum reply:', error);
      throw error;
    }
  }

  // Récupérer un thread spécifique avec ses réponses
  async getThread(threadId: number): Promise<ForumThread> {
    try {
      const response = await fetch(`${this.baseURL}/threads/${threadId}`, {
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
      console.error('Error fetching forum thread:', error);
      throw error;
    }
  }

  // Voter sur un thread
  async voteThread(threadId: number, voteType: 'up' | 'down'): Promise<void> {
    try {
      const response = await fetch(`${this.baseURL}/threads/${threadId}/vote`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('najah_token')}`
        },
        body: JSON.stringify({ vote_type: voteType })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
    } catch (error) {
      console.error('Error voting on forum thread:', error);
      throw error;
    }
  }

  // Voter sur un message
  async voteMessage(messageId: number, voteType: 'up' | 'down'): Promise<void> {
    try {
      const response = await fetch(`${this.baseURL}/messages/${messageId}/vote`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('najah_token')}`
        },
        body: JSON.stringify({ vote_type: voteType })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
    } catch (error) {
      console.error('Error voting on forum message:', error);
      throw error;
    }
  }

  // Signaler un thread ou un message
  async report(data: ReportRequest): Promise<void> {
    try {
      const response = await fetch(`${this.baseURL}/reports`, {
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
    } catch (error) {
      console.error('Error reporting forum content:', error);
      throw error;
    }
  }

  // Marquer un message comme solution
  async markAsSolution(messageId: number): Promise<void> {
    try {
      const response = await fetch(`${this.baseURL}/messages/${messageId}/solution`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('najah_token')}`
        }
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
    } catch (error) {
      console.error('Error marking message as solution:', error);
      throw error;
    }
  }

  // Épingler/désépingler un thread
  async togglePin(threadId: number): Promise<void> {
    try {
      const response = await fetch(`${this.baseURL}/threads/${threadId}/pin`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('najah_token')}`
        }
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
    } catch (error) {
      console.error('Error toggling thread pin:', error);
      throw error;
    }
  }

  // Verrouiller/déverrouiller un thread
  async toggleLock(threadId: number): Promise<void> {
    try {
      const response = await fetch(`${this.baseURL}/threads/${threadId}/lock`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('najah_token')}`
        }
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
    } catch (error) {
      console.error('Error toggling thread lock:', error);
      throw error;
    }
  }
}

export const forumAPI = new ForumAPI();
