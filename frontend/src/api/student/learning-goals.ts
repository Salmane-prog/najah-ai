// API pour les objectifs d'apprentissage des étudiants

export interface LearningGoal {
  id: number;
  student_id: number;
  title: string;
  description: string;
  subject: string;
  target_date: string;
  progress: number; // 0-100
  status: 'pending' | 'in_progress' | 'completed' | 'cancelled';
  priority: 'low' | 'medium' | 'high';
  created_at: string;
  updated_at: string;
}

export const learningGoalsAPI = {
  // Récupérer tous les objectifs d'apprentissage d'un étudiant
  async getLearningGoals(studentId: number): Promise<LearningGoal[]> {
    try {
      const token = localStorage.getItem('najah_token');
      if (!token) {
        console.warn('Aucun token disponible pour les objectifs d\'apprentissage');
        return [];
      }
      
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/v1/students/${studentId}/learning-goals`, {
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        }
      });
      
      if (!response.ok) {
        if (response.status === 401) {
          console.warn('Token expiré pour les objectifs d\'apprentissage');
          return [];
        }
        throw new Error(`Erreur ${response.status}: Erreur lors de la récupération des objectifs`);
      }
      
      return await response.json();
    } catch (error) {
      console.error('Erreur API learning goals:', error);
      return [];
    }
  },

  // Créer un nouvel objectif d'apprentissage
  async createLearningGoal(goalData: Partial<LearningGoal>): Promise<LearningGoal | null> {
    try {
      const response = await fetch('/api/v1/learning-goals', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(goalData),
      });
      if (!response.ok) throw new Error('Erreur lors de la création de l\'objectif');
      return await response.json();
    } catch (error) {
      console.error('Erreur API création objectif:', error);
      return null;
    }
  },

  // Mettre à jour un objectif d'apprentissage
  async updateLearningGoal(goalId: number, goalData: Partial<LearningGoal>): Promise<LearningGoal | null> {
    try {
      const response = await fetch(`/api/v1/learning-goals/${goalId}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(goalData),
      });
      if (!response.ok) throw new Error('Erreur lors de la mise à jour de l\'objectif');
      return await response.json();
    } catch (error) {
      console.error('Erreur API mise à jour objectif:', error);
      return null;
    }
  },

  // Supprimer un objectif d'apprentissage
  async deleteLearningGoal(goalId: number): Promise<boolean> {
    try {
      const response = await fetch(`/api/v1/learning-goals/${goalId}`, {
        method: 'DELETE',
      });
      return response.ok;
    } catch (error) {
      console.error('Erreur API suppression objectif:', error);
      return false;
    }
  },

  // Mettre à jour le progrès d'un objectif
  async updateGoalProgress(goalId: number, progress: number): Promise<LearningGoal | null> {
    try {
      const response = await fetch(`/api/v1/learning-goals/${goalId}/progress`, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ progress }),
      });
      if (!response.ok) throw new Error('Erreur lors de la mise à jour du progrès');
      return await response.json();
    } catch (error) {
      console.error('Erreur API mise à jour progrès:', error);
      return null;
    }
  },

  // Récupérer les statistiques des objectifs
  async getGoalsStats(studentId: number): Promise<{
    total_goals: number;
    completed_goals: number;
    in_progress_goals: number;
    pending_goals: number;
    average_progress: number;
  }> {
    try {
      const response = await fetch(`/api/v1/students/${studentId}/goals-stats`);
      if (!response.ok) throw new Error('Erreur lors de la récupération des statistiques');
      return await response.json();
    } catch (error) {
      console.error('Erreur API statistiques objectifs:', error);
      return {
        total_goals: 0,
        completed_goals: 0,
        in_progress_goals: 0,
        pending_goals: 0,
        average_progress: 0,
      };
    }
  },
};
