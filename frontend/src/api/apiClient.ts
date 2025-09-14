const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

interface ApiResponse<T = any> {
  data: T;
  status: number;
  ok: boolean;
}

class ApiClient {
  private baseURL: string;

  constructor(baseURL: string = API_BASE_URL) {
    this.baseURL = baseURL;
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<ApiResponse<T>> {
    const url = `${this.baseURL}${endpoint}`;
    
    // Get token from localStorage if available
    const token = typeof window !== 'undefined' ? localStorage.getItem('najah_token') : null;
    
    const defaultHeaders: HeadersInit = {
      'Content-Type': 'application/json',
    };

    if (token) {
      defaultHeaders['Authorization'] = `Bearer ${token}`;
    }

    const config: RequestInit = {
      ...options,
      headers: {
        ...defaultHeaders,
        ...options.headers,
      },
    };

    // Créer un AbortController pour le timeout
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 10000); // 10 secondes de timeout

    try {
      const response = await fetch(url, {
        ...config,
        signal: controller.signal,
      });
      
      clearTimeout(timeoutId);
      
      // Vérifier si la réponse est ok avant de traiter
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      let data: T;
      const contentType = response.headers.get('content-type');
      
      if (contentType && contentType.includes('application/json')) {
        data = await response.json();
      } else {
        data = await response.text() as T;
      }

      return {
        data,
        status: response.status,
        ok: response.ok,
      };
    } catch (error) {
      clearTimeout(timeoutId);
      console.error('API request failed:', error);
      
      // Gestion spécifique des erreurs de réseau
      if (error instanceof TypeError && error.message.includes('Failed to fetch')) {
        throw new Error('Erreur de connexion au serveur. Vérifiez que le backend est en cours d\'exécution.');
      }
      
      // Gestion des erreurs de timeout
      if (error.name === 'AbortError') {
        throw new Error('La requête a pris trop de temps. Vérifiez votre connexion internet.');
      }
      
      throw new Error(`API request failed: ${error instanceof Error ? error.message : 'Unknown error'}`);
    }
  }

  async get<T = any>(endpoint: string): Promise<ApiResponse<T>> {
    return this.request<T>(endpoint, { method: 'GET' });
  }

  async post<T = any>(endpoint: string, data?: any): Promise<ApiResponse<T>> {
    return this.request<T>(endpoint, {
      method: 'POST',
      body: data ? JSON.stringify(data) : undefined,
    });
  }

  async put<T = any>(endpoint: string, data?: any): Promise<ApiResponse<T>> {
    return this.request<T>(endpoint, {
      method: 'PUT',
      body: data ? JSON.stringify(data) : undefined,
    });
  }

  async patch<T = any>(endpoint: string, data?: any): Promise<ApiResponse<T>> {
    return this.request<T>(endpoint, {
      method: 'PATCH',
      body: data ? JSON.stringify(data) : undefined,
    });
  }

  async delete<T = any>(endpoint: string): Promise<ApiResponse<T>> {
    return this.request<T>(endpoint, { method: 'DELETE' });
  }
}

// Export the apiClient instance
export const apiClient = new ApiClient();

// Also export the class for testing purposes
export { ApiClient }; 