import { API_BASE_URL } from '../config';

export interface Resource {
  id: number;
  title: string;
  description: string;
  type: 'video' | 'document' | 'image' | 'audio' | 'link' | 'interactive';
  subject: string;
  level: string;
  tags: string[];
  author: string;
  created_at: string;
  duration?: number; // en minutes pour les vidéos
  file_size?: string;
  views: number;
  rating: number;
  is_favorite: boolean;
  is_in_collection: boolean;
  collections: string[];
  url: string;
  thumbnail?: string;
}

export interface Collection {
  id: number;
  name: string;
  description: string;
  resource_count: number;
  is_public: boolean;
  created_at: string;
  color: string;
}

export interface Subject {
  id: number;
  name: string;
  color: string;
  resource_count: number;
}

export interface Level {
  id: number;
  name: string;
  color: string;
  resource_count: number;
}

export interface CreateCollectionRequest {
  name: string;
  description: string;
  is_public: boolean;
  color?: string;
}

export interface UpdateCollectionRequest {
  name?: string;
  description?: string;
  is_public?: boolean;
  color?: string;
}

export interface AddToCollectionRequest {
  resource_id: number;
  collection_id: number;
}

export interface RateResourceRequest {
  resource_id: number;
  rating: number; // 1-5
  comment?: string;
}

class LibraryAPI {
  private baseURL = `${API_BASE_URL}/library`;

  // ===== RESSOURCES =====

  // Récupérer toutes les ressources
  async getResources(
    subject?: string,
    level?: string,
    type?: string,
    searchTerm?: string,
    sortBy?: 'recent' | 'popular' | 'rating' | 'title',
    sortOrder?: 'asc' | 'desc'
  ): Promise<Resource[]> {
    try {
      const params = new URLSearchParams();
      if (subject) params.append('subject', subject);
      if (level) params.append('level', level);
      if (type) params.append('type', type);
      if (searchTerm) params.append('search', searchTerm);
      if (sortBy) params.append('sort_by', sortBy);
      if (sortOrder) params.append('sort_order', sortOrder);

      const response = await fetch(`${this.baseURL}/resources?${params}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error fetching resources:', error);
      throw error;
    }
  }

  // Récupérer une ressource spécifique
  async getResource(resourceId: number): Promise<Resource> {
    try {
      const response = await fetch(`${this.baseURL}/resources/${resourceId}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error fetching resource:', error);
      throw error;
    }
  }

  // Marquer une ressource comme vue
  async markAsViewed(resourceId: number): Promise<void> {
    try {
      const response = await fetch(`${this.baseURL}/resources/${resourceId}/view`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
    } catch (error) {
      console.error('Error marking resource as viewed:', error);
      throw error;
    }
  }

  // ===== FAVORIS =====

  // Récupérer les ressources favorites
  async getFavoriteResources(): Promise<Resource[]> {
    try {
      const response = await fetch(`${this.baseURL}/favorites`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error fetching favorite resources:', error);
      throw error;
    }
  }

  // Marquer/démarquer une ressource comme favorite
  async toggleFavorite(resourceId: number): Promise<void> {
    try {
      const response = await fetch(`${this.baseURL}/resources/${resourceId}/favorite`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
    } catch (error) {
      console.error('Error toggling resource favorite:', error);
      throw error;
    }
  }

  // Ajouter/retirer une ressource d'une collection
  async toggleCollection(resourceId: number): Promise<void> {
    try {
      const response = await fetch(`${this.baseURL}/resources/${resourceId}/collection`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
    } catch (error) {
      console.error('Error toggling resource collection:', error);
      throw error;
    }
  }

  // ===== COLLECTIONS =====

  // Récupérer toutes les collections
  async getCollections(): Promise<Collection[]> {
    try {
      const response = await fetch(`${this.baseURL}/collections`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error fetching collections:', error);
      throw error;
    }
  }

  // Créer une nouvelle collection
  async createCollection(data: CreateCollectionRequest): Promise<Collection> {
    try {
      const response = await fetch(`${this.baseURL}/collections`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        },
        body: JSON.stringify(data)
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error creating collection:', error);
      throw error;
    }
  }

  // Mettre à jour une collection
  async updateCollection(collectionId: number, data: UpdateCollectionRequest): Promise<Collection> {
    try {
      const response = await fetch(`${this.baseURL}/collections/${collectionId}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        },
        body: JSON.stringify(data)
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error updating collection:', error);
      throw error;
    }
  }

  // Supprimer une collection
  async deleteCollection(collectionId: number): Promise<void> {
    try {
      const response = await fetch(`${this.baseURL}/collections/${collectionId}`, {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
    } catch (error) {
      console.error('Error deleting collection:', error);
      throw error;
    }
  }

  // Récupérer les ressources d'une collection
  async getCollectionResources(collectionId: number): Promise<Resource[]> {
    try {
      const response = await fetch(`${this.baseURL}/collections/${collectionId}/resources`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error fetching collection resources:', error);
      throw error;
    }
  }

  // Ajouter une ressource à une collection
  async addToCollection(data: AddToCollectionRequest): Promise<void> {
    try {
      const response = await fetch(`${this.baseURL}/collections/${data.collection_id}/resources`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        },
        body: JSON.stringify({ resource_id: data.resource_id })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
    } catch (error) {
      console.error('Error adding resource to collection:', error);
      throw error;
    }
  }

  // Retirer une ressource d'une collection
  async removeFromCollection(collectionId: number, resourceId: number): Promise<void> {
    try {
      const response = await fetch(`${this.baseURL}/collections/${collectionId}/resources/${resourceId}`, {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
    } catch (error) {
      console.error('Error removing resource from collection:', error);
      throw error;
    }
  }

  // ===== MATIÈRES ET NIVEAUX =====

  // Récupérer toutes les matières
  async getSubjects(): Promise<Subject[]> {
    try {
      const response = await fetch(`${this.baseURL}/subjects`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error fetching subjects:', error);
      throw error;
    }
  }

  // Récupérer tous les niveaux
  async getLevels(): Promise<Level[]> {
    try {
      const response = await fetch(`${this.baseURL}/levels`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error fetching levels:', error);
      throw error;
    }
  }

  // ===== ÉVALUATIONS =====

  // Évaluer une ressource
  async rateResource(data: RateResourceRequest): Promise<void> {
    try {
      const response = await fetch(`${this.baseURL}/resources/${data.resource_id}/rate`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        },
        body: JSON.stringify({
          rating: data.rating,
          comment: data.comment
        })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
    } catch (error) {
      console.error('Error rating resource:', error);
      throw error;
    }
  }

  // Récupérer les évaluations d'une ressource
  async getResourceRatings(resourceId: number): Promise<{
    average_rating: number;
    total_ratings: number;
    ratings: Array<{
      user_id: number;
      rating: number;
      comment?: string;
      created_at: string;
    }>;
  }> {
    try {
      const response = await fetch(`${this.baseURL}/resources/${resourceId}/ratings`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error fetching resource ratings:', error);
      throw error;
    }
  }

  // ===== RECHERCHE ET FILTRES =====

  // Recherche avancée
  async searchResources(query: string, filters?: {
    subject?: string;
    level?: string;
    type?: string;
    min_rating?: number;
    max_duration?: number;
  }): Promise<Resource[]> {
    try {
      const params = new URLSearchParams();
      params.append('query', query);
      
      if (filters) {
        Object.entries(filters).forEach(([key, value]) => {
          if (value !== undefined) {
            params.append(key, value.toString());
          }
        });
      }

      const response = await fetch(`${this.baseURL}/search?${params}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error searching resources:', error);
      throw error;
    }
  }

  // Récupérer les ressources recommandées
  async getRecommendedResources(limit: number = 10): Promise<Resource[]> {
    try {
      const response = await fetch(`${this.baseURL}/recommendations?limit=${limit}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error fetching recommended resources:', error);
      throw error;
    }
  }

  // ===== STATISTIQUES =====

  // Récupérer les statistiques de la bibliothèque
  async getLibraryStats(): Promise<{
    total_resources: number;
    total_views: number;
    total_favorites: number;
    total_collections: number;
    most_viewed_subject: string;
    most_rated_resource: string;
  }> {
    try {
      const response = await fetch(`${this.baseURL}/stats`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error fetching library stats:', error);
      throw error;
    }
  }

  // Récupérer l'historique de consultation
  async getViewHistory(limit: number = 20): Promise<Array<{
    resource: Resource;
    viewed_at: string;
  }>> {
    try {
      const response = await fetch(`${this.baseURL}/history?limit=${limit}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error fetching view history:', error);
      throw error;
    }
  }
}

export const libraryAPI = new LibraryAPI(); 