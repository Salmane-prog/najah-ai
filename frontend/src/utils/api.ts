const API_BASE_URL = 'http://localhost:8000';

interface ApiResponse<T = any> {
  data: T;
  error?: string;
  status: number;
}

class ApiError extends Error {
  constructor(public status: number, message: string) {
    super(message);
    this.name = 'ApiError';
  }
}

export const apiClient = {
  async request<T = any>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<ApiResponse<T>> {
    try {
      // Récupérer le token depuis localStorage
      const token = localStorage.getItem('najah_token');
      
      if (!token) {
        throw new ApiError(401, 'Token d\'authentification manquant');
      }

      const url = endpoint.startsWith('http') ? endpoint : `${API_BASE_URL}${endpoint}`;
      
      const response = await fetch(url, {
        ...options,
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
          ...options.headers,
        },
      });

      if (!response.ok) {
        // Si 401, essayer de rafraîchir le token ou déconnecter
        if (response.status === 401) {
          console.warn('[API] Token expiré, déconnexion automatique');
          localStorage.removeItem('najah_token');
          localStorage.removeItem('najah_user');
          window.location.href = '/login';
          throw new ApiError(401, 'Session expirée, veuillez vous reconnecter');
        }
        
        const errorData = await response.json().catch(() => ({}));
        throw new ApiError(response.status, errorData.detail || response.statusText);
      }

      const data = await response.json();
      return { data, status: response.status };
    } catch (error) {
      if (error instanceof ApiError) {
        throw error;
      }
      console.error('[API] Erreur de requête:', error);
      throw new ApiError(500, 'Erreur de connexion au serveur');
    }
  },

  // Méthodes utilitaires
  async get<T = any>(endpoint: string): Promise<ApiResponse<T>> {
    return this.request<T>(endpoint, { method: 'GET' });
  },

  async post<T = any>(endpoint: string, data?: any): Promise<ApiResponse<T>> {
    return this.request<T>(endpoint, {
      method: 'POST',
      body: data ? JSON.stringify(data) : undefined,
    });
  },

  async put<T = any>(endpoint: string, data?: any): Promise<ApiResponse<T>> {
    return this.request<T>(endpoint, {
      method: 'PUT',
      body: data ? JSON.stringify(data) : undefined,
    });
  },

  async delete<T = any>(endpoint: string): Promise<ApiResponse<T>> {
    return this.request<T>(endpoint, { method: 'DELETE' });
  },
};

// Hook personnalisé pour les requêtes API
export const useApi = () => {
  const makeRequest = async <T = any>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> => {
    const response = await apiClient.request<T>(endpoint, options);
    return response.data;
  };

  return {
    get: <T = any>(endpoint: string) => makeRequest<T>(endpoint, { method: 'GET' }),
    post: <T = any>(endpoint: string, data?: any) => 
      makeRequest<T>(endpoint, { method: 'POST', body: JSON.stringify(data) }),
    put: <T = any>(endpoint: string, data?: any) => 
      makeRequest<T>(endpoint, { method: 'PUT', body: JSON.stringify(data) }),
    delete: <T = any>(endpoint: string) => makeRequest<T>(endpoint, { method: 'DELETE' }),
  };
}; 