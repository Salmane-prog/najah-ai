import { apiClient } from '../utils/api';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// ============================================================================
// INTERFACES POUR LES CLASSES ET ÉTUDIANTS
// ============================================================================

export interface ClassGroup {
  id: number;
  name: string;
  description: string;
  teacher_id: number;
  level: string;
  subject: string;
  max_students: number;
  is_active: boolean;
  created_at: string;
  student_count: number;
}

export interface ClassStudent {
  id: number;
  class_id: number;
  student_id: number;
  student_name: string;
  student_email: string;
  joined_at: string;
}

export interface StudentPerformance {
  student_id: number;
  student_name: string;
  total_quizzes: number;
  average_score: number;
  overall_percentage: number;
  recent_activity_count: number;
  last_activity: string;
}

export interface ClassPerformance {
  class_id: number;
  class_name: string;
  students_count: number;
  class_average: number;
  class_max: number;
  class_min: number;
  students: StudentPerformance[];
}

export interface TeacherClassData {
  classes: ClassGroup[];
  total_students: number;
  active_classes: number;
}

// ============================================================================
// FONCTIONS PRINCIPALES
// ============================================================================

export async function getTeacherClasses(token: string, teacherId: number): Promise<TeacherClassData> {
  try {
    console.log('🔄 Récupération des classes du professeur...');
    
    const response = await fetch(`${API_BASE_URL}/api/v1/teacher/classes/${teacherId}`, {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });

    if (!response.ok) {
      throw new Error(`Erreur HTTP: ${response.status}`);
    }

    const data = await response.json();
    console.log('✅ Classes du professeur récupérées:', data);
    return data;

  } catch (error) {
    console.error('❌ Erreur lors de la récupération des classes:', error);
    throw error;
  }
}

export async function getClassStudents(token: string, classId: number): Promise<ClassStudent[]> {
  try {
    console.log('🔄 Récupération des étudiants de la classe...');
    
    const response = await fetch(`${API_BASE_URL}/api/v1/class_groups/${classId}/students`, {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });

    if (!response.ok) {
      throw new Error(`Erreur HTTP: ${response.status}`);
    }

    const data = await response.json();
    console.log('✅ Étudiants de la classe récupérés:', data);
    return data.students || [];

  } catch (error) {
    console.error('❌ Erreur lors de la récupération des étudiants:', error);
    throw error;
  }
}

export async function getClassPerformance(token: string, classId: number): Promise<ClassPerformance> {
  try {
    console.log('🔄 Récupération de la performance de la classe...');
    
    const response = await fetch(`${API_BASE_URL}/api/v1/student_performance/class/${classId}/students-performance`, {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });

    if (!response.ok) {
      throw new Error(`Erreur HTTP: ${response.status}`);
    }

    const data = await response.json();
    console.log('✅ Performance de la classe récupérée:', data);
    return data;

  } catch (error) {
    console.error('❌ Erreur lors de la récupération de la performance:', error);
    throw error;
  }
}

export async function getAllStudentsAnalytics(token: string): Promise<any> {
  try {
    console.log('🔄 Récupération des analytics de tous les étudiants...');
    
    const response = await fetch(`${API_BASE_URL}/api/v1/student_analytics/students/analytics`, {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });

    if (!response.ok) {
      throw new Error(`Erreur HTTP: ${response.status}`);
    }

    const data = await response.json();
    console.log('✅ Analytics de tous les étudiants récupérées:', data);
    return data;

  } catch (error) {
    console.error('❌ Erreur lors de la récupération des analytics:', error);
    throw error;
  }
}

// ============================================================================
// FONCTIONS DE FALLBACK (DONNÉES MOCKÉES EN CAS D'ERREUR)
// ============================================================================

export function getMockTeacherClasses(): TeacherClassData {
  return {
    classes: [
      {
        id: 1,
        name: "6ème A",
        description: "Classe de 6ème année",
        teacher_id: 1,
        level: "6ème",
        subject: "Mathématiques",
        max_students: 30,
        is_active: true,
        created_at: new Date().toISOString(),
        student_count: 25
      },
      {
        id: 2,
        name: "6ème B",
        description: "Classe de 6ème année",
        teacher_id: 1,
        level: "6ème",
        subject: "Mathématiques",
        max_students: 30,
        is_active: true,
        created_at: new Date().toISOString(),
        student_count: 28
      }
    ],
    total_students: 53,
    active_classes: 2
  };
}

export function getMockClassStudents(): ClassStudent[] {
  return [
    {
      id: 1,
      class_id: 1,
      student_id: 1,
      student_name: "Étudiant 1",
      student_email: "etudiant1@example.com",
      joined_at: new Date().toISOString()
    },
    {
      id: 2,
      class_id: 1,
      student_id: 2,
      student_name: "Étudiant 2",
      student_email: "etudiant2@example.com",
      joined_at: new Date().toISOString()
    }
  ];
}

export function getMockClassPerformance(): ClassPerformance {
  return {
    class_id: 1,
    class_name: "6ème A",
    students_count: 25,
    class_average: 78.5,
    class_max: 95,
    class_min: 62,
    students: [
      {
        student_id: 1,
        student_name: "Étudiant 1",
        total_quizzes: 8,
        average_score: 85,
        overall_percentage: 85,
        recent_activity_count: 3,
        last_activity: new Date().toISOString()
      },
      {
        student_id: 2,
        student_name: "Étudiant 2",
        total_quizzes: 7,
        average_score: 72,
        overall_percentage: 72,
        recent_activity_count: 2,
        last_activity: new Date().toISOString()
      }
    ]
  };
}

// ============================================================================
// FONCTIONS AVEC FALLBACK
// ============================================================================

export async function getTeacherClassesWithFallback(token: string, teacherId: number): Promise<TeacherClassData> {
  try {
    return await getTeacherClasses(token, teacherId);
  } catch (error) {
    console.warn('⚠️ Utilisation des données de fallback pour les classes:', error);
    return getMockTeacherClasses();
  }
}

export async function getClassStudentsWithFallback(token: string, classId: number): Promise<ClassStudent[]> {
  try {
    return await getClassStudents(token, classId);
  } catch (error) {
    console.warn('⚠️ Utilisation des données de fallback pour les étudiants:', error);
    return getMockClassStudents();
  }
}

export async function getClassPerformanceWithFallback(token: string, classId: number): Promise<ClassPerformance> {
  try {
    return await getClassPerformance(token, classId);
  } catch (error) {
    console.warn('⚠️ Utilisation des données de fallback pour la performance:', error);
    return getMockClassPerformance();
  }
}
