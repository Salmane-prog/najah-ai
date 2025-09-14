// API pour les assignations des enseignants

import { apiClient } from '../apiClient';

export interface Assignment {
  id: number;
  title: string;
  description: string;
  subject: string;
  assignment_type: 'class' | 'student';
  target_ids: number[];
  due_date?: string;
  priority: 'low' | 'medium' | 'high';
  estimated_time?: number; // en minutes
  status: string;
  created_at: string;
  created_by: number;
  teacher_name: string;
  target_names: string[];
  attachment?: {
    name: string;
    size: number;
    url: string;
    type: string;
    filename?: string; // Nom du fichier sur le serveur
  } | null;
}

export interface AssignmentCreate {
  title: string;
  description: string;
  subject: string;
  assignment_type: 'class' | 'student';
  target_ids: number[];
  due_date?: string;
  priority: 'low' | 'medium' | 'high';
  estimated_time?: number;
}

export interface TeacherTarget {
  id: number;
  name: string;
  type: 'class' | 'student';
  student_count?: number;
  email?: string;
  class_name?: string;
}

export interface TeacherTargetsResponse {
  classes: TeacherTarget[];
  students: TeacherTarget[];
  total_students: number;
}

export const assignmentsAPI = {
  // Récupérer les cibles disponibles pour l'enseignant (classes et étudiants)
  async getTeacherTargets(): Promise<TeacherTargetsResponse> {
    try {
      const response = await apiClient.get('/api/v1/assignments/teacher/targets');
      return response.data;
    } catch (error) {
      console.error('Erreur API teacher targets:', error);
      return {
        classes: [],
        students: [],
        total_students: 0
      };
    }
  },

  // Créer une nouvelle assignation
  async createAssignment(assignmentData: AssignmentCreate): Promise<Assignment | null> {
    try {
      const response = await apiClient.post('/api/v1/assignments/', assignmentData);
      return response.data;
    } catch (error) {
      console.error('Erreur API création assignation:', error);
      return null;
    }
  },

  // Récupérer toutes les assignations d'un enseignant
  async getTeacherAssignments(): Promise<Assignment[]> {
    try {
      const response = await apiClient.get('/api/v1/assignments/teacher/assignments');
      return response.data;
    } catch (error) {
      console.error('Erreur API récupération assignations:', error);
      return [];
    }
  },

  // Mettre à jour une assignation
  async updateAssignment(assignmentId: number, assignmentData: Partial<AssignmentCreate>): Promise<Assignment | null> {
    try {
      const response = await apiClient.put(`/api/v1/assignments/${assignmentId}`, assignmentData);
      return response.data;
    } catch (error) {
      console.error('Erreur API mise à jour assignation:', error);
      return null;
    }
  },

  // Supprimer une assignation
  async deleteAssignment(assignmentId: number): Promise<boolean> {
    try {
      const response = await apiClient.delete(`/api/v1/assignments/${assignmentId}`);
      return response.ok;
    } catch (error) {
      console.error('Erreur API suppression assignation:', error);
      return false;
    }
  },
};
