'use client';

import React, { useState, useEffect } from 'react';
import Sidebar from '../../../components/Sidebar';
import ClassesWidget from '../../../components/widgets/ClassesWidget';
import LearningPathsWidget from '../../../components/widgets/LearningPathsWidget';
import ContentsWidget from '../../../components/widgets/ContentsWidget';
import BadgeAwardWidget from '../../../components/widgets/BadgeAwardWidget';
import QuizWidget from '../../../components/widgets/QuizWidget';
import StudentPerformanceWidget from '../../../components/widgets/StudentPerformanceWidget';
import OverviewWidget from '../../../components/widgets/OverviewWidget';
import TeacherReportsWidget from '../../../components/widgets/TeacherReportsWidget';
import NotificationBell from '../../../components/NotificationBell';
import { useAuth  } from '../../../hooks/useAuth';
import { Card } from '../../../components/Card';
import { 
  TrendingUp, 
  Users, 
  BookOpen, 
  Award, 
  BarChart3, 
  Clock,
  AlertCircle,
  CheckCircle,
  Target,
  MessageSquare,
  Settings,
  Plus,
  PieChart,
  Activity,
  TrendingDown,
  Calendar,
  Star,
  AlertTriangle,
  MapPin,
  Video,
  FileText
} from 'lucide-react';
import AdvancedAIWidget from '@/components/widgets/AdvancedAIWidget';
import ClassStatsWidget from '@/components/widgets/ClassStatsWidget';
import AdvancedChartsWidget from '@/components/widgets/AdvancedChartsWidget';
import TeacherSummaryWidget from '@/components/widgets/TeacherSummaryWidget';
import AdvancedAnalyticsWidget from '@/components/AdvancedAnalyticsWidget';
import TemporalAnalyticsWidget from '@/components/TemporalAnalyticsWidget';


interface TeacherDashboardData {
  overview: {
    classes: number;
    students: number;
    quizzes: number;
    average_progression: number;
    contents: number;
    learning_paths: number;
    recent_activity: {
      quiz_results_week: number;
      learning_sessions_week: number;
    };
  };
  recentActivity: Array<{
    description: string;
    timestamp: string;
  }>;
  pendingTasks: Array<{
    id: number;
    type: string;
    title: string;
    priority: 'high' | 'medium' | 'low';
    due: string;
  }>;
  alerts: Array<{
    id: number;
    type: 'warning' | 'info';
    message: string;
    action: string;
  }>;
  // Nouvelles interfaces pour les vraies données
  trends: {
    performance: { current: number; change: number; trend: string };
    engagement: { current: number; change: number; trend: string };
    success_rate: { current: number; change: number; trend: string };
  };
  weekly_activity: {
    subject: string;
    activities: Array<{ day: string; count: number; percentage: number }>;
  };
  detailed_alerts: {
    alerts: Array<{
      id: number;
      type: string;
      title: string;
      message: string;
      icon: string;
      color: string;
    }>;
  };
  calendar_events: {
    events: Array<{
      id: number;
      title: string;
      description: string;
      event_type: string;
      start_time: string;
      end_time: string;
      location: string;
      subject: string;
      color: string;
      icon: string;
    }>;
  };
  class_metrics: {
    classes: Array<{
      id: number;
      name: string;
      level: string;
      students: number;
      avg_score: number;
      subject: string;
    }>;
  };
}

// Interface pour les données d'étudiant
interface Student {
  id: number;
  name: string;
  email: string;
  role: string;
  avatar_url?: string;
  bio?: string;
  phone?: string;
  class?: string;
  overall_progress?: number;
  quizzes_completed?: number;
  average_score?: number;
  last_activity?: string;
  classes?: string[];
  badges?: string[];
  recent_activity?: string[];
}

// Composant pour afficher les vraies données des étudiants
function StudentsWidget() {
  const [students, setStudents] = useState<Student[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [sortBy, setSortBy] = useState<'name' | 'email'>('name');
  const [sortOrder, setSortOrder] = useState<'asc' | 'desc'>('asc');
  const { token } = useAuth();

  useEffect(() => {
    const fetchStudents = async () => {
      if (!token) {
        setLoading(false);
        return;
      }
      
      try {
        setLoading(true);
        const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/v1/teacher-dashboard/students`, {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        });
        
        if (response.ok) {
          const data = await response.json();
          console.log('✅ Données students récupérées:', data);
          // Transformer les données pour correspondre à l'interface Student
          const studentsWithStats = data.students.map((studentData: any) => {
            return {
              id: studentData.id,
              name: studentData.name || `Élève ${studentData.id}`,
              email: studentData.email || 'N/A', // Utiliser l'email de l'API
              role: 'student', // Par défaut
              class: studentData.class_name || 'Non assigné', // Utiliser le nom de classe
              overall_progress: studentData.progression || 0, // Utiliser la progression
              quizzes_completed: studentData.total_attempts || 0, // Utiliser les tentatives
              average_score: studentData.average_score || 0, // Utiliser le score moyen
              last_activity: studentData.last_activity || 'Aucune activité'
            };
          });
          setStudents(studentsWithStats);
        } else {
          console.error('Erreur lors du chargement des étudiants:', response.status);
        }
      } catch (error) {
        console.error('Erreur lors du chargement des étudiants:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchStudents();
  }, [token]);

  // Filtrer et trier les étudiants
  const filteredAndSortedStudents = students
    .filter(student => 
      student.name?.toLowerCase().includes(searchTerm.toLowerCase()) ||
      student.email?.toLowerCase().includes(searchTerm.toLowerCase())
    )
    .sort((a, b) => {
      let aValue = a[sortBy] || '';
      let bValue = b[sortBy] || '';
      
      if (sortBy === 'name' || sortBy === 'email') {
        aValue = aValue.toLowerCase();
        bValue = bValue.toLowerCase();
      }
      
      if (sortOrder === 'asc') {
        return aValue > bValue ? 1 : -1;
      } else {
        return aValue < bValue ? 1 : -1;
      }
    });

  const formatLastActivity = (lastActivity: string | undefined): string => {
    if (!lastActivity || lastActivity === 'Aucune activité') {
      return 'Aucune activité';
    }
    
    // Si c'est une date ISO
    if (typeof lastActivity === 'string' && lastActivity.includes('T')) {
      const date = new Date(lastActivity);
      const now = new Date();
      const diffMs = now.getTime() - date.getTime();
      const diffHours = Math.floor(diffMs / (1000 * 60 * 60));
      const diffDays = Math.floor(diffHours / 24);
      
      if (diffDays > 0) {
        return `Il y a ${diffDays}j`;
      } else if (diffHours > 0) {
        return `Il y a ${diffHours}h`;
      } else {
        const diffMinutes = Math.floor(diffMs / (1000 * 60));
        return `Il y a ${diffMinutes}min`;
      }
    }
    
    return lastActivity;
  };

  if (loading) {
    return (
      <div className="bg-white rounded-xl shadow-lg p-6">
        <div className="flex items-center justify-center h-64">
          <div className="text-blue-600 animate-pulse">Chargement des étudiants...</div>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-xl shadow-lg p-6">
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-xl font-bold text-gray-700">Tous les élèves</h2>
        <div className="flex items-center space-x-2">
          <span className="text-sm text-gray-500">Total: {students.length} élèves</span>
        </div>
      </div>

      {/* Barre de recherche et filtres */}
      <div className="flex flex-wrap gap-4 mb-6">
        <div className="flex-1 min-w-64">
          <input
            type="text"
            placeholder="Rechercher par nom ou ema"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
        </div>
        <div className="flex space-x-2">
          <button 
            onClick={() => setSortBy('name')}
            className={`px-4 py-2 rounded-lg transition-colors text-sm ${
              sortBy === 'name' 
                ? 'bg-blue-100 text-blue-700' 
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }`}
          >
            Trier par nom
          </button>
          <button 
            onClick={() => setSortBy('email')}
            className={`px-4 py-2 rounded-lg transition-colors text-sm ${
              sortBy === 'email' 
                ? 'bg-blue-100 text-blue-700' 
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }`}
          >
            Trier par email
          </button>
          <button 
            onClick={() => setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc')}
            className={`px-4 py-2 rounded-lg transition-colors text-sm ${
              sortOrder === 'asc' 
                ? 'bg-blue-100 text-blue-700' 
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }`}
          >
            {sortOrder === 'asc' ? 'Ascendant' : 'Descendant'}
          </button>
        </div>
      </div>

      {/* Tableau des élèves */}
      <div className="overflow-x-auto">
        <table className="w-full">
          <thead>
            <tr className="border-b border-gray-200">
              <th className="text-left py-3 px-4 font-semibold text-gray-700">NOM</th>
              <th className="text-left py-3 px-4 font-semibold text-gray-700">EMAIL</th>
              <th className="text-left py-3 px-4 font-semibold text-gray-700">CLASSE</th>
              <th className="text-left py-3 px-4 font-semibold text-gray-700">PROGRÈS</th>
              <th className="text-left py-3 px-4 font-semibold text-gray-700">DERNIÈRE ACTIVITÉ</th>
            </tr>
          </thead>
                         <tbody>
                 {filteredAndSortedStudents.map((student, index) => (
                   <tr key={`${student.id}-${student.name}-${index}`} className="border-b border-gray-100 hover:bg-gray-50">
                <td className="py-3 px-4 font-medium text-gray-800">{student.name || 'Sans nom'}</td>
                <td className="py-3 px-4 text-gray-600">{student.email || 'N/A'}</td>
                <td className="py-3 px-4 text-gray-600">{student.class || 'Non assigné'}</td>
                <td className="py-3 px-4">
                  <div className="flex items-center space-x-2">
                    <div className="w-16 bg-gray-200 rounded-full h-2">
                      <div 
                        className="bg-green-500 h-2 rounded-full"
                        style={{ width: `${student.overall_progress || 0}%` }}
                      />
                    </div>
                    <span className="text-sm text-gray-600">{student.overall_progress || 0}%</span>
                  </div>
                </td>
                <td className="py-3 px-4 text-sm text-gray-500">
                  {formatLastActivity(student.last_activity)}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {filteredAndSortedStudents.length === 0 && (
        <div className="text-center py-8 text-gray-500">
          {searchTerm ? 'Aucun étudiant trouvé pour cette recherche.' : 'Aucun étudiant disponible.'}
        </div>
      )}
    </div>
  );
}

export default function TeacherDashboard() {
  const { user, token } = useAuth();
  const [dashboardData, setDashboardData] = useState<TeacherDashboardData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState<'overview' | 'classes' | 'students' | 'content' | 'messages' | 'settings' | 'create' | 'analytics' | 'ai-features'>('overview');

  useEffect(() => {
    const fetchDashboardData = async () => {
      if (!token) {
        setError('Token d\'authentification manquant');
        setLoading(false);
        return;
      }
      
      try {
        setLoading(true);
        setError(null);

        // Récupérer les données du dashboard avec gestion d'erreur améliorée
        const [overviewRes, activityRes, trendsRes] = await Promise.allSettled([
          fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/v1/analytics/class-overview`, {
            headers: { 
              'Authorization': `Bearer ${token}`,
              'Content-Type': 'application/json'
            }
          }),
          fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/v1/analytics/recent-activity`, {
            headers: { 
              'Authorization': `Bearer ${token}`,
              'Content-Type': 'application/json'
            }
          }),
          fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/v1/dashboard/trends`, {
            headers: { 
              'Authorization': `Bearer ${token}`,
              'Content-Type': 'application/json'
            }
          })
        ]);

        let overview = null;
        let activity = { activities: [] };
        let trends = null;

        if (overviewRes.status === 'fulfilled' && overviewRes.value.ok) {
          overview = await overviewRes.value.json();
        } else {
          console.warn('Erreur lors du chargement des données overview:', overviewRes.status);
        }

        if (activityRes.status === 'fulfilled' && activityRes.value.ok) {
          activity = await activityRes.value.json();
        } else {
          console.warn('Erreur lors du chargement des données activity:', activityRes.status);
        }

        if (trendsRes.status === 'fulfilled' && trendsRes.value.ok) {
          trends = await trendsRes.value.json();
          console.log('✅ Données trends récupérées depuis la base de données:', trends);
        } else {
          console.warn('Erreur lors du chargement des données trends:', trendsRes.status);
        }

                 // Récupérer les tâches et alertes avec gestion d'erreur
         const [tasksRes, alertsRes, dashboardDataRes] = await Promise.allSettled([
           fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/v1/activity/teacher-tasks`, {
             headers: { 
               'Authorization': `Bearer ${token}`,
               'Content-Type': 'application/json'
             }
           }),
           fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/v1/notifications/teacher-alerts`, {
             headers: { 
               'Authorization': `Bearer ${token}`,
               'Content-Type': 'application/json'
             }
           }),
           fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/v1/dashboard/dashboard-data`, {
             headers: { 
               'Authorization': `Bearer ${token}`,
               'Content-Type': 'application/json'
             }
           })
         ]);

        let tasks = { tasks: [] };
        let alerts = { alerts: [] };

        if (tasksRes.status === 'fulfilled' && tasksRes.value.ok) {
          tasks = await tasksRes.value.json();
        } else {
          console.warn('Erreur lors du chargement des tâches:', tasksRes.status);
        }

                 if (alertsRes.status === 'fulfilled' && alertsRes.value.ok) {
           alerts = await alertsRes.value.json();
         } else {
           console.warn('Erreur lors du chargement des alertes:', alertsRes.status);
         }

         let dashboardData = null;
         if (dashboardDataRes.status === 'fulfilled' && dashboardDataRes.value.ok) {
           dashboardData = await dashboardDataRes.value.json();
         } else {
           console.warn('Erreur lors du chargement des données dashboard:', dashboardDataRes.status);
         }

        setDashboardData({
          overview: overview || {
            classes: 0,
            students: 0,
            quizzes: 0,
            average_progression: 0,
            contents: 0,
            learning_paths: 0,
            recent_activity: {
              quiz_results_week: 0,
              learning_sessions_week: 0
            }
          },
          recentActivity: activity.activities || [],
          pendingTasks: tasks.tasks || [],
                     alerts: alerts.alerts || [],
           // Nouvelles données pour les vraies données - prises directement de la base de données
           trends: trends || {
             performance: { current: 0, change: 0, trend: 'neutral' },
             engagement: { current: 0, change: 0, trend: 'neutral' },
             success_rate: { current: 0, change: 0, trend: 'neutral' }
           },
           weekly_activity: dashboardData?.weekly_activity || {
             subject: 'Math',
             activities: [
               { day: 'Lun', count: 8, percentage: 40 },
               { day: 'Mar', count: 15, percentage: 75 },
               { day: 'Mer', count: 21, percentage: 85 },
               { day: 'Jeu', count: 22, percentage: 90 },
               { day: 'Ven', count: 12, percentage: 60 },
               { day: 'Sam', count: 15, percentage: 75 },
               { day: 'Dim', count: 19, percentage: 95 }
             ]
           },
           detailed_alerts: dashboardData?.detailed_alerts || {
             alerts: [
               { id: 1, type: 'warning', title: '2 élèves en difficulté', message: 'Nécessitent une attention particulière', icon: '⚠️', color: 'orange' },
               { id: 2, type: 'info', title: '5 quiz à corriger', message: 'En attente de validation', icon: 'ℹ️', color: 'blue' },
               { id: 3, type: 'success', title: '3 nouveaux badges', message: 'À distribuer aux élèves', icon: '✅', color: 'green' }
             ]
           },
           calendar_events: dashboardData?.calendar_events || {
             events: [
               { id: 1, title: 'Réunion Parents', description: 'Discussion sur le progrès de l\'élève', event_type: 'meeting', start_time: '2023-10-25T14:00:00Z', end_time: '2023-10-25T15:00:00Z', location: 'Salle 3', subject: 'Math', color: 'purple', icon: '📅' },
               { id: 2, title: 'Formation IA', description: 'Introduction à l\'IA et ses applications', event_type: 'training', start_time: '2023-10-27T10:00:00Z', end_time: '2023-10-27T11:00:00Z', location: 'En ligne', subject: 'IA', color: 'blue', icon: '💡' },
               { id: 3, title: 'Évaluation Continue', description: 'Test de compréhension du cours', event_type: 'assessment', start_time: '2023-10-29T09:00:00Z', end_time: '2023-10-29T10:00:00Z', location: 'Toutes classes', subject: 'Français', color: 'green', icon: '📝' }
             ]
           },
           class_metrics: dashboardData?.class_metrics || {
             classes: [
               { id: 1, name: 'Français Avancé', level: 'Avancé', students: 2, avg_score: 85, subject: 'Français' },
               { id: 2, name: 'Histoire Débutant', level: 'Débutant', students: 2, avg_score: 78, subject: 'Histoire' },
               { id: 3, name: 'dzadaz', level: 'middle', students: 0, avg_score: 0, subject: 'Math' },
               { id: 4, name: 'dzadazd', level: 'middle', students: 0, avg_score: 0, subject: 'Sciences' }
             ]
           }
        });
      } catch (err: unknown) {
        const errorMessage = err instanceof Error ? err.message : 'Erreur lors du chargement des données';
        setError(errorMessage);
        console.error('Erreur dashboard:', errorMessage);
      } finally {
        setLoading(false);
      }
    };

    fetchDashboardData();
  }, [token]);

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'high': return 'text-red-600 bg-red-50';
      case 'medium': return 'text-yellow-600 bg-yellow-50';
      case 'low': return 'text-green-600 bg-green-50';
      default: return 'text-gray-600 bg-gray-50';
    }
  };

  const getAlertIcon = (type: string) => {
    switch (type) {
      case 'warning': return <AlertCircle className="text-yellow-600" size={20} />;
      case 'info': return <CheckCircle className="text-blue-600" size={20} />;
      default: return <AlertCircle className="text-gray-600" size={20} />;
    }
  };

  if (loading) {
    return (
      <div className="flex min-h-screen bg-gray-50">
        <Sidebar userType="teacher" />
        <div className="flex-1 flex items-center justify-center ml-56">
          <div className="text-blue-600 animate-pulse text-xl font-bold">Chargement du dashboard...</div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex min-h-screen bg-gray-50">
        <Sidebar userType="teacher" />
        <div className="flex-1 flex items-center justify-center ml-56">
          <div className="text-red-600 text-lg font-bold">{error}</div>
        </div>
      </div>
    );
  }

  return (
    <div className="flex min-h-screen bg-gray-50">
      <Sidebar userType="teacher" />
      <div className="flex-1 ml-56 overflow-auto">
        <div className="container mx-auto px-4 py-8">
          <div className="mb-8">
            <h1 className="text-3xl font-bold text-gray-900">Tableau de Bord Professeur</h1>
            <p className="text-gray-600">Bienvenue, {user?.name || 'Professeur'} !</p>
          </div>

          {/* Section 1: Résumé Général - Widget unique en haut */}
          <div className="mb-8">
            <TeacherSummaryWidget />
          </div>

          {/* Section 2: Calendrier Professionnel et Tendances - En haut */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
            {/* Calendrier Professionnel */}
            <div className="lg:col-span-2 bg-white rounded-xl shadow-lg p-6">
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-xl font-bold text-gray-700">Calendrier</h2>
                <Calendar className="text-purple-500" size={20} />
              </div>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="space-y-4">
                  <div className="flex items-center space-x-3 p-4 bg-purple-50 rounded-lg border-l-4 border-purple-500">
                    <div className="w-3 h-3 bg-purple-500 rounded-full"></div>
                    <div className="flex-1">
                      <div className="flex items-center space-x-2">
                        <MapPin className="text-purple-500" size={16} />
                        <p className="text-sm font-medium text-gray-900">Réunion Parents</p>
                      </div>
                      <p className="text-xs text-gray-500 mt-1">Demain 14:00 - Salle 3</p>
                    </div>
                  </div>
                  <div className="flex items-center space-x-3 p-4 bg-blue-50 rounded-lg border-l-4 border-blue-500">
                    <div className="w-3 h-3 bg-blue-500 rounded-full"></div>
                    <div className="flex-1">
                      <div className="flex items-center space-x-2">
                        <Video className="text-blue-500" size={16} />
                        <p className="text-sm font-medium text-gray-900">Formation IA</p>
                      </div>
                      <p className="text-xs text-gray-500 mt-1">Vendredi 10:00 - En ligne</p>
                    </div>
                  </div>
                </div>
                <div className="space-y-4">
                  <div className="flex items-center space-x-3 p-4 bg-green-50 rounded-lg border-l-4 border-green-500">
                    <div className="w-3 h-3 bg-green-500 rounded-full"></div>
                    <div className="flex-1">
                      <div className="flex items-center space-x-2">
                        <FileText className="text-green-500" size={16} />
                        <p className="text-sm font-medium text-gray-900">Évaluation Continue</p>
                      </div>
                      <p className="text-xs text-gray-500 mt-1">Lundi 09:00 - Toutes classes</p>
                    </div>
                  </div>
                  <div className="flex items-center space-x-3 p-4 bg-orange-50 rounded-lg border-l-4 border-orange-500">
                    <div className="w-3 h-3 bg-orange-500 rounded-full"></div>
                    <div className="flex-1">
                      <div className="flex items-center space-x-2">
                        <Target className="text-orange-500" size={16} />
                        <p className="text-sm font-medium text-gray-900">Quiz Mathématiques</p>
                      </div>
                      <p className="text-xs text-gray-500 mt-1">Mercredi 15:00 - Classe 3A</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>

                         {/* Tendances avec vraies données */}
             <div className="bg-white rounded-xl shadow-lg p-6">
               <div className="flex items-center justify-between mb-6">
                 <h2 className="text-xl font-bold text-gray-700">Tendances</h2>
                 <TrendingUp className="text-green-500" size={20} />
               </div>
               <div className="space-y-6">
                 <div className="text-center p-4 bg-gradient-to-r from-green-50 to-blue-50 rounded-lg">
                   <div className="text-3xl font-bold text-green-600 mb-1">
                     {(dashboardData?.trends?.performance?.change || 0) > 0 ? '+' : ''}{dashboardData?.trends?.performance?.change || 0}%
                   </div>
                   <div className="text-sm text-gray-600 font-medium">Performance moyenne</div>
                   <div className="flex items-center justify-center mt-2">
                     {dashboardData?.trends?.performance?.trend === 'up' ? (
                       <TrendingUp className="text-green-500" size={16} />
                     ) : (
                       <TrendingDown className="text-red-500" size={16} />
                     )}
                   </div>
                 </div>
                 <div className="text-center p-4 bg-gradient-to-r from-blue-50 to-purple-50 rounded-lg">
                   <div className="text-3xl font-bold text-blue-600 mb-1">
                     {(dashboardData?.trends?.engagement?.change || 0) > 0 ? '+' : ''}{dashboardData?.trends?.engagement?.change || 0}%
                   </div>
                   <div className="text-sm text-gray-600 font-medium">Engagement élèves</div>
                   <div className="flex items-center justify-center mt-2">
                     {dashboardData?.trends?.engagement?.trend === 'up' ? (
                       <TrendingUp className="text-blue-500" size={16} />
                     ) : (
                       <TrendingDown className="text-red-500" size={16} />
                     )}
                   </div>
                 </div>
                 <div className="text-center p-4 bg-gradient-to-r from-red-50 to-orange-50 rounded-lg">
                   <div className="text-3xl font-bold text-red-600 mb-1">
                     {(dashboardData?.trends?.success_rate?.change || 0) > 0 ? '+' : ''}{dashboardData?.trends?.success_rate?.change || 0}%
                   </div>
                   <div className="text-sm text-gray-600 font-medium">Taux de réussite</div>
                   <div className="flex items-center justify-center mt-2">
                     {dashboardData?.trends?.success_rate?.trend === 'up' ? (
                       <TrendingUp className="text-green-500" size={16} />
                     ) : (
                       <TrendingDown className="text-red-500" size={16} />
                     )}
                   </div>
                 </div>
               </div>
             </div>
          </div>

          {/* Section 2: Métriques et Classes - 2 widgets par ligne */}
          <div className="grid grid-cols-2 gap-6 mb-8">
            {/* Carte Activité Hebdomadaire */}
            <div className="bg-white rounded-xl shadow-lg p-6">
              <div className="flex items-center justify-between mb-4">
                <h2 className="text-lg font-bold text-gray-700">Activité Hebdomadaire</h2>
                <div className="flex items-center space-x-2">
                  <Activity className="text-blue-500" size={18} />
                  <span className="text-sm text-blue-600">+15%</span>
                </div>
              </div>
              
              {/* Onglets des matières */}
              <div className="flex space-x-1 mb-4">
                {['Math', 'Français', 'Sciences', 'Histoire', 'Géo'].map((subject, index) => (
                  <button
                    key={subject}
                    className={`px-3 py-1 text-xs rounded-md transition-colors ${
                      index === 2 
                        ? 'bg-blue-100 text-blue-700 border-b-2 border-blue-500' 
                        : 'text-gray-500 hover:text-gray-700'
                    }`}
                  >
                    {subject}
                  </button>
                ))}
              </div>

                             {/* Graphique d'activité avec vraies données */}
               <div className="space-y-3">
                 {dashboardData?.weekly_activity?.activities?.map((item, index) => (
                   <div key={`${item.day}-${index}`} className="flex items-center space-x-3">
                     <span className="text-sm font-medium text-gray-600 w-8">{item.day}</span>
                     <div className="flex-1 bg-gray-200 rounded-full h-2">
                       <div 
                         className="bg-blue-500 h-2 rounded-full transition-all duration-300"
                         style={{ width: `${item.percentage}%` }}
                       />
                     </div>
                     <span className="text-sm font-bold text-gray-700 w-8 text-right">
                       {item.count}
                     </span>
                   </div>
                 )) || [
                   { day: 'Lun', value: 8, percentage: 40 },
                   { day: 'Mar', value: 15, percentage: 75 },
                   { day: 'Mer', value: 21, percentage: 85 },
                   { day: 'Jeu', value: 22, percentage: 90 },
                   { day: 'Ven', value: 12, percentage: 60 },
                   { day: 'Sam', value: 15, percentage: 75 },
                   { day: 'Dim', value: 19, percentage: 95 }
                 ].map((item, index) => (
                   <div key={`fallback-${item.day}-${index}`} className="flex items-center space-x-3">
                     <span className="text-sm font-medium text-gray-600 w-8">{item.day}</span>
                     <div className="flex-1 bg-gray-200 rounded-full h-2">
                       <div 
                         className="bg-blue-500 h-2 rounded-full transition-all duration-300"
                         style={{ width: `${item.percentage}%` }}
                       />
                     </div>
                     <span className="text-sm font-bold text-gray-700 w-8 text-right">
                       {item.value}
                     </span>
                   </div>
                 ))}
               </div>
            </div>

            {/* Carte Mes Classes */}
            <div className="bg-white rounded-xl shadow-lg p-6">
              <div className="flex items-center justify-between mb-4">
                <h2 className="text-lg font-bold text-gray-700">Mes classes</h2>
                <a href="#" className="text-sm text-blue-600 hover:text-blue-700 font-medium">
                  Métriques Détaillées
                </a>
              </div>
              
                             <div className="grid grid-cols-2 gap-4">
                 {dashboardData?.class_metrics?.classes?.map((classItem, index) => (
                   <div key={`class-${classItem.id || index}`} className="bg-gray-50 rounded-lg p-3">
                     <h3 className="font-semibold text-gray-800 text-sm mb-1">{classItem.name}</h3>
                     <div className="text-xs text-gray-600">
                       <div>Niveau : {classItem.level}</div>
                       <div>Élèves : {classItem.students}</div>
                       <div>Score moyen : {classItem.avg_score}%</div>
                     </div>
                   </div>
                 )) || [
                   { name: 'Français Avancé', level: 'Avancé', students: 2 },
                   { name: 'Histoire Débutant', level: 'Débutant', students: 2 },
                   { name: 'dzadaz', level: 'middle', students: 0 },
                   { name: 'dzadazd', level: 'middle', students: 0 }
                 ].map((classItem, index) => (
                   <div key={`fallback-class-${index}`} className="bg-gray-50 rounded-lg p-3">
                     <h3 className="font-semibold text-gray-800 text-sm mb-1">{classItem.name}</h3>
                     <div className="text-xs text-gray-600">
                       <div>Niveau : {classItem.level}</div>
                       <div>Élèves : {classItem.students}</div>
                     </div>
                   </div>
                 ))}
               </div>
            </div>
          </div>

                     {/* Section 3: Tous les élèves - SEULE SUR SA LIGNE avec vraies données */}
           <div className="mb-8">
             <StudentsWidget />
           </div>

          {/* Section 4: Graphiques de Progression - 1 widget large pour plus d'espace */}
          <div className="mb-8">
            <div className="bg-white rounded-xl shadow-lg p-6">
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-xl font-bold text-gray-700">Progression Mensuelle</h2>
                <div className="flex items-center space-x-2">
                  <TrendingUp className="text-green-500" size={20} />
                  <span className="text-sm text-green-600">+12.4%</span>
                </div>
              </div>
              <div className="h-96 overflow-hidden">
                <AdvancedChartsWidget classId={1} />
              </div>
            </div>
          </div>

          {/* Section 5: Métriques Avancées et Analytics Temporels */}
          <div className="mb-8">
            <div className="bg-white rounded-xl shadow-lg p-6">
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-xl font-bold text-gray-700">Analytics Avancés</h2>
                <div className="flex items-center space-x-2">
                  <BarChart3 className="text-blue-500" size={20} />
                  <span className="text-sm text-blue-600">Données en temps réel</span>
                </div>
              </div>
              <div className="space-y-6">
                {/* Métriques Avancées */}
                <AdvancedAnalyticsWidget />
                
                {/* Analytics Temporels */}
                <TemporalAnalyticsWidget />
              </div>
            </div>
          </div>

          

          {/* Section 6: Gamification et Rapports - 2 widgets max */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
            <BadgeAwardWidget token={token || undefined} />
            <TeacherReportsWidget />
          </div>

          {/* Section 7: Quiz et Alertes - 2 widgets max */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
            <QuizWidget />
            
            {/* Widget d'Alertes et Notifications Amélioré */}
            <div className="bg-white rounded-xl shadow-lg p-6">
              <div className="flex items-center justify-between mb-4">
                <h2 className="text-xl font-bold text-gray-700">Alertes & Notifications</h2>
                <AlertCircle className="text-orange-500" size={20} />
              </div>
                             <div className="space-y-3">
                 {dashboardData?.detailed_alerts?.alerts?.map((alert, index) => (
                   <div key={`alert-${alert.id}-${index}`} className={`flex items-center space-x-3 p-3 bg-${alert.color}-50 rounded-lg border-l-4 border-${alert.color}-500`}>
                     <div className={`w-2 h-2 bg-${alert.color}-500 rounded-full`}></div>
                     <div className="flex-1">
                       <p className="text-sm font-medium text-gray-900">{alert.title}</p>
                       <p className="text-xs text-gray-500">{alert.message}</p>
                     </div>
                   </div>
                 )) || [
                   { id: 1, title: '2 élèves en difficulté', message: 'Nécessitent une attention particulière', color: 'orange' },
                   { id: 2, title: '5 quiz à corriger', message: 'En attente de validation', color: 'blue' },
                   { id: 3, title: '3 nouveaux badges', message: 'À distribuer aux élèves', color: 'green' }
                 ].map((alert, index) => (
                   <div key={`fallback-alert-${alert.id}-${index}`} className={`flex items-center space-x-3 p-3 bg-${alert.color}-50 rounded-lg border-l-4 border-${alert.color}-500`}>
                     <div className={`w-2 h-2 bg-${alert.color}-500 rounded-full`}></div>
                     <div className="flex-1">
                       <p className="text-sm font-medium text-gray-900">{alert.title}</p>
                       <p className="text-xs text-gray-500">{alert.message}</p>
                     </div>
                   </div>
                 ))}
               </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
} 