// Configuration de l'API
export const API_BASE_URL = 'http://localhost:8000/api/v1';

// Configuration des timeouts
export const API_TIMEOUT = 10000; // 10 secondes

// Configuration des headers par défaut
export const DEFAULT_HEADERS = {
  'Content-Type': 'application/json',
};

// Fonction pour obtenir le token d'authentification
export const getAuthToken = (): string | null => {
  if (typeof window !== 'undefined') {
    return localStorage.getItem('token');
  }
  return null;
};

// Fonction pour créer les headers avec authentification
export const createAuthHeaders = (): Record<string, string> => {
  const token = getAuthToken();
  return {
    ...DEFAULT_HEADERS,
    ...(token && { 'Authorization': `Bearer ${token}` })
  };
};

// Gestionnaire d'erreurs API
export const handleApiError = (error: any): string => {
  if (error.response) {
    // Erreur de réponse du serveur
    const { status, data } = error.response;
    switch (status) {
      case 401:
        return 'Session expirée. Veuillez vous reconnecter.';
      case 403:
        return 'Accès refusé. Vous n\'avez pas les permissions nécessaires.';
      case 404:
        return 'Ressource non trouvée.';
      case 422:
        return data?.detail || 'Données invalides.';
      case 500:
        return 'Erreur serveur. Veuillez réessayer plus tard.';
      default:
        return data?.detail || `Erreur ${status}: ${data?.message || 'Erreur inconnue'}`;
    }
  } else if (error.request) {
    // Erreur de réseau
    return 'Erreur de connexion. Vérifiez votre connexion internet.';
  } else {
    // Autre erreur
    return error.message || 'Une erreur inattendue s\'est produite.';
  }
}; 