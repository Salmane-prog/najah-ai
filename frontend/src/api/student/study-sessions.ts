// API pour les sessions d'étude des étudiants

export interface StudySession {
  id: number;
  student_id: number;
  subject: string;
  duration: number; // en minutes
  start_time: string;
  end_time: string;
  notes: string;
  efficiency_rating: number; // 1-5
  created_at: string;
}

export const studySessionAPI = {
  // Récupérer toutes les sessions d'étude d'un étudiant
  async getStudySessions(studentId: number): Promise<StudySession[]> {
    try {
      const token = localStorage.getItem('najah_token');
      if (!token) {
        console.warn('Aucun token disponible pour les sessions d\'étude');
        return [];
      }
      
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/v1/students/${studentId}/study-sessions`, {
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        }
      });
      
      if (!response.ok) {
        if (response.status === 401) {
          console.warn('Token expiré pour les sessions d\'étude');
          return [];
        }
        throw new Error(`Erreur ${response.status}: Erreur lors de la récupération des sessions`);
      }
      
      return await response.json();
    } catch (error) {
      console.error('Erreur API study sessions:', error);
      return [];
    }
  },

  // Créer une nouvelle session d'étude
  async createStudySession(sessionData: Partial<StudySession>): Promise<StudySession | null> {
    try {
      const response = await fetch('/api/v1/study-sessions', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(sessionData),
      });
      if (!response.ok) throw new Error('Erreur lors de la création de la session');
      return await response.json();
    } catch (error) {
      console.error('Erreur API création session:', error);
      return null;
    }
  },

  // Mettre à jour une session d'étude
  async updateStudySession(sessionId: number, sessionData: Partial<StudySession>): Promise<StudySession | null> {
    try {
      const response = await fetch(`/api/v1/study-sessions/${sessionId}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(sessionData),
      });
      if (!response.ok) throw new Error('Erreur lors de la mise à jour de la session');
      return await response.json();
    } catch (error) {
      console.error('Erreur API mise à jour session:', error);
      return null;
    }
  },

  // Supprimer une session d'étude
  async deleteStudySession(sessionId: number): Promise<boolean> {
    try {
      const response = await fetch(`/api/v1/study-sessions/${sessionId}`, {
        method: 'DELETE',
      });
      return response.ok;
    } catch (error) {
      console.error('Erreur API suppression session:', error);
      return false;
    }
  },

  // Récupérer les statistiques des sessions d'étude
  async getStudyStats(studentId: number): Promise<{
    total_sessions: number;
    total_duration: number;
    average_efficiency: number;
    subjects: { [key: string]: number };
  }> {
    try {
      const response = await fetch(`/api/v1/students/${studentId}/study-stats`);
      if (!response.ok) throw new Error('Erreur lors de la récupération des statistiques');
      return await response.json();
    } catch (error) {
      console.error('Erreur API statistiques sessions:', error);
      return {
        total_sessions: 0,
        total_duration: 0,
        average_efficiency: 0,
        subjects: {},
      };
    }
  },
};
