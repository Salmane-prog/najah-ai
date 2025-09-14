import { API_BASE_URL } from '../config';

export interface Note {
  id: number;
  title: string;
  content: string;
  subject_id: number;  // Changé de subject (string) à subject_id (number)
  chapter_id: number;  // Changé de chapter (string) à chapter_id (number)
  tags: string[];
  created_at: string;
  updated_at: string;
  is_favorite: boolean;
  is_shared: boolean;
  shared_with: string[];
  version: number;
  color: string;
  attachments: Attachment[];
}

export interface Attachment {
  id: number;
  name: string;
  type: 'image' | 'document' | 'link';
  url: string;
  size?: string;
}

export interface Subject {
  id: number;
  name: string;
  color: string;
  note_count: number;
}

export interface Chapter {
  id: number;
  name: string;
  subject_id: number;
  note_count: number;
}

export interface CreateNoteRequest {
  title: string;
  content: string;
  subject_id: number;  // Changé de subject (string) à subject_id (number)
  chapter_id: number;  // Changé de chapter (string) à chapter_id (number)
  tags: string[];
  color?: string;
}

export interface UpdateNoteRequest {
  title?: string;
  content?: string;
  subject_id?: number;  // Changé de subject (string) à subject_id (number)
  chapter_id?: number;  // Changé de chapter (string) à chapter_id (number)
  tags?: string[];
  color?: string;
}

export interface ShareNoteRequest {
  note_id: number;
  user_ids: number[];
  permissions: 'read' | 'write' | 'admin';
}

class NotesAPI {
  private baseURL = `${API_BASE_URL}/notes-advanced`;

  // Récupérer toutes les notes
  async getNotes(subject?: string, chapter?: string, search?: string): Promise<Note[]> {
    try {
      const params = new URLSearchParams();
      if (subject) params.append('subject', subject);
      if (chapter) params.append('chapter', chapter);
      if (search) params.append('search', search);

      const response = await fetch(`${this.baseURL}/?${params}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('najah_token')}`
        }
      });

      if (!response.ok) {
        const errorText = await response.text();
        console.error('API: Erreur de réponse:', errorText);
        throw new Error(`HTTP error! status: ${response.status}, message: ${errorText}`);
      }

      const data = await response.json();
      console.log('API: Données reçues:', data);
      
      // L'API retourne {notes: [...], total: ..., limit: ..., offset: ...}
      // On extrait le champ "notes"
      if (data && data.notes && Array.isArray(data.notes)) {
        return data.notes;
      } else {
        console.warn('API: Format de réponse inattendu:', data);
        return [];
      }
    } catch (error) {
      console.error('Error fetching notes:', error);
      throw error;
    }
  }

  // Récupérer une note spécifique
  async getNote(noteId: number): Promise<Note> {
    try {
      const response = await fetch(`${this.baseURL}/${noteId}`, {
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
      console.error('Error fetching note:', error);
      throw error;
    }
  }

  // Créer une nouvelle note
  async createNote(data: CreateNoteRequest): Promise<Note> {
    try {
      console.log('API: Envoi de la requête de création de note');
      console.log('API: URL:', `${this.baseURL}`);
      console.log('API: Données:', data);
      
      const response = await fetch(`${this.baseURL}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('najah_token')}`
        },
        body: JSON.stringify({
          title: data.title,
          content: data.content,
          subject_id: data.subject_id,
          chapter_id: data.chapter_id,
          tags: data.tags || [],  // Envoyer directement la liste, pas JSON.stringify
          color: data.color || "#3B82F6"  // Utiliser un code couleur hexadécimal
        })
      });

      console.log('API: Status de la réponse:', response.status);
      console.log('API: Headers de la réponse:', Object.fromEntries(response.headers.entries()));

      if (!response.ok) {
        const errorText = await response.text();
        console.error('API: Erreur de réponse:', errorText);
        throw new Error(`HTTP error! status: ${response.status}, message: ${errorText}`);
      }

      const result = await response.json();
      console.log('API: Réponse reçue:', result);
      return result;
    } catch (error) {
      console.error('API: Erreur lors de la création de note:', error);
      throw error;
    }
  }

  // Mettre à jour une note
  async updateNote(noteId: number, data: UpdateNoteRequest): Promise<Note> {
    try {
      const updateData: any = {};
      if (data.title !== undefined) updateData.title = data.title;
      if (data.content !== undefined) updateData.content = data.content;
      if (data.subject_id !== undefined) updateData.subject_id = data.subject_id;
      if (data.chapter_id !== undefined) updateData.chapter_id = data.chapter_id;
      if (data.tags !== undefined) updateData.tags = JSON.stringify(data.tags);
      if (data.color !== undefined) updateData.color = data.color;

      const response = await fetch(`${this.baseURL}/${noteId}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('najah_token')}`
        },
        body: JSON.stringify(updateData)
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error updating note:', error);
      throw error;
    }
  }

  // Supprimer une note
  async deleteNote(noteId: number): Promise<void> {
    try {
      const response = await fetch(`${this.baseURL}/${noteId}`, {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('najah_token')}`
        }
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
    } catch (error) {
      console.error('Error deleting note:', error);
      throw error;
    }
  }

  // Récupérer toutes les matières
  async getSubjects(): Promise<Subject[]> {
    try {
      const response = await fetch(`${this.baseURL}/subjects`, {
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
      console.error('Error fetching subjects:', error);
      throw error;
    }
  }

  // Récupérer les chapitres d'une matière
  async getChapters(subjectId?: number): Promise<Chapter[]> {
    try {
      const params = new URLSearchParams();
      if (subjectId) params.append('subject_id', subjectId.toString());

      const response = await fetch(`${this.baseURL}/chapters?${params}`, {
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
      console.error('Error fetching chapters:', error);
      throw error;
    }
  }

  // Ajouter/retirer une note des favoris
  async toggleFavorite(noteId: number): Promise<void> {
    try {
      const response = await fetch(`${this.baseURL}/notes/${noteId}/favorite`, {
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
      console.error('Error toggling favorite:', error);
      throw error;
    }
  }

  // Partager une note
  async shareNote(data: ShareNoteRequest): Promise<void> {
    try {
      const response = await fetch(`${this.baseURL}/notes/${data.note_id}/share`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('najah_token')}`
        },
        body: JSON.stringify({
          user_ids: data.user_ids,
          permissions: data.permissions
        })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
    } catch (error) {
      console.error('Error sharing note:', error);
      throw error;
    }
  }

  // Récupérer les versions d'une note
  async getNoteVersions(noteId: number): Promise<Note[]> {
    try {
      const response = await fetch(`${this.baseURL}/notes/${noteId}/versions`, {
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
      console.error('Error fetching note versions:', error);
      throw error;
    }
  }

  // Restaurer une version d'une note
  async restoreVersion(noteId: number, versionId: number): Promise<Note> {
    try {
      const response = await fetch(`${this.baseURL}/notes/${noteId}/versions/${versionId}/restore`, {
        method: 'POST',
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
      console.error('Error restoring version:', error);
      throw error;
    }
  }

  // Ajouter une pièce jointe à une note
  async addAttachment(noteId: number, file: File): Promise<Attachment> {
    try {
      const formData = new FormData();
      formData.append('file', file);

      const response = await fetch(`${this.baseURL}/notes/${noteId}/attachments`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('najah_token')}`
        },
        body: formData
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error adding attachment:', error);
      throw error;
    }
  }

  // Supprimer une pièce jointe d'une note
  async deleteAttachment(noteId: number, attachmentId: number): Promise<void> {
    try {
      const response = await fetch(`${this.baseURL}/notes/${noteId}/attachments/${attachmentId}`, {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('najah_token')}`
        }
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
    } catch (error) {
      console.error('Error deleting attachment:', error);
      throw error;
    }
  }

  // Récupérer les notes partagées
  async getSharedNotes(): Promise<Note[]> {
    try {
      const response = await fetch(`${this.baseURL}/shared`, {
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
      console.error('Error fetching shared notes:', error);
      throw error;
    }
  }

  // Récupérer les notes favorites
  async getFavoriteNotes(): Promise<Note[]> {
    try {
      const response = await fetch(`${this.baseURL}/favorites`, {
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
      console.error('Error fetching favorite notes:', error);
      throw error;
    }
  }
}

export const notesAPI = new NotesAPI(); 