'use client';

import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import DashboardLayout from './DashboardLayout';

interface DashboardStats {
  totalStudents: number;
  totalAssessments: number;
  totalQuestions: number;
  averageScore: number;
  cognitiveProfiles: number;
  irtModels: number;
}

interface RecentActivity {
  id: string;
  type: 'assessment' | 'question' | 'analysis' | 'irt';
  title: string;
  description: string;
  timestamp: string;
  status: 'completed' | 'in_progress' | 'pending';
}

export default function TeacherDashboard() {
  const router = useRouter();
  const [stats, setStats] = useState<DashboardStats>({
    totalStudents: 0,
    totalAssessments: 0,
    totalQuestions: 0,
    averageScore: 0,
    cognitiveProfiles: 0,
    irtModels: 0
  });

  const [recentActivity, setRecentActivity] = useState<RecentActivity[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Simuler le chargement des données
    setTimeout(() => {
      setStats({
        totalStudents: 156,
        totalAssessments: 23,
        totalQuestions: 847,
        averageScore: 78.5,
        cognitiveProfiles: 142,
        irtModels: 8
      });

      setRecentActivity([
        {
          id: '1',
          type: 'assessment',
          title: 'Évaluation Mathématiques - Chapitre 3',
          description: 'Test sur les équations du second degré',
          timestamp: 'Il y a 2 heures',
          status: 'completed'
        },
        {
          id: '2',
          type: 'analysis',
          title: 'Analyse Cognitive - Classe 2A',
          description: 'Profil d\'apprentissage de 28 étudiants',
          timestamp: 'Il y a 1 jour',
          status: 'completed'
        },
        {
          id: '3',
          type: 'irt',
          title: 'Modèle IRT - Physique Quantique',
          description: 'Calibration des paramètres de difficulté',
          timestamp: 'Il y a 3 jours',
          status: 'in_progress'
        },
        {
          id: '4',
          type: 'question',
          title: 'Ajout de 15 questions',
          description: 'Nouvelles questions sur la mécanique',
          timestamp: 'Il y a 1 semaine',
          status: 'completed'
        }
      ]);

      setLoading(false);
    }, 1000);
  }, []);

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed':
        return 'bg-green-100 text-green-800';
      case 'in_progress':
        return 'bg-blue-100 text-blue-800';
      case 'pending':
        return 'bg-yellow-100 text-yellow-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const getStatusText = (status: string) => {
    switch (status) {
      case 'completed':
        return 'Terminé';
      case 'in_progress':
        return 'En cours';
      case 'pending':
        return 'En attente';
      default:
        return 'Inconnu';
    }
  };

  const getTypeIcon = (type: string) => {
    switch (type) {
      case 'assessment':
        return '📝';
      case 'question':
        return '❓';
      case 'analysis':
        return '🧠';
      case 'irt':
        return '📈';
      default:
        return '📋';
    }
  };

  const quickActions = [
    {
      title: 'Analytics Avancés',
      description: 'Analyse cognitive et IRT',
      icon: '🧠',
      path: '/dashboard/teacher/analytics/advanced',
      color: 'from-blue-500 to-indigo-600'
    },
    {
      title: 'Banque de Questions',
      description: 'Gérer et organiser',
      icon: '🗃️',
      path: '/dashboard/teacher/questions',
      color: 'from-green-500 to-emerald-600'
    },
    {
      title: 'Profils Cognitifs',
      description: 'Analyser les styles d\'apprentissage',
      icon: '👥',
      path: '/dashboard/teacher/cognitive-profiles',
      color: 'from-purple-500 to-pink-600'
    },
    {
      title: 'Dashboard IRT',
      description: 'Moteur d\'adaptation',
      icon: '📊',
      path: '/dashboard/teacher/irt',
      color: 'from-orange-500 to-red-600'
    }
  ];

  if (loading) {
    return (
      <DashboardLayout userType="teacher" title="Tableau de Bord" subtitle="Chargement...">
        <div className="flex items-center justify-center h-64">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
        </div>
      </DashboardLayout>
    );
  }

  return (
    <DashboardLayout 
      userType="teacher" 
      title="Tableau de Bord Enseignant" 
      subtitle="Gestion des évaluations et analytics avancés"
    >
      {/* En-tête avec métriques principales */}
      <div className="mb-8">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <div className="bg-white rounded-lg shadow p-6 border-l-4 border-blue-500">
            <div className="flex items-center">
              <div className="p-3 rounded-full bg-blue-100 text-blue-600">
                <span className="text-2xl">👥</span>
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Étudiants</p>
                <p className="text-2xl font-semibold text-gray-900">{stats.totalStudents}</p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6 border-l-4 border-green-500">
            <div className="flex items-center">
              <div className="p-3 rounded-full bg-green-100 text-green-600">
                <span className="text-2xl">📝</span>
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Évaluations</p>
                <p className="text-2xl font-semibold text-gray-900">{stats.totalAssessments}</p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6 border-l-4 border-purple-500">
            <div className="flex items-center">
              <div className="p-3 rounded-full bg-purple-100 text-purple-600">
                <span className="text-2xl">🧠</span>
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Profils Cognitifs</p>
                <p className="text-2xl font-semibold text-gray-900">{stats.cognitiveProfiles}</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Actions rapides */}
      <div className="mb-8">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">Actions Rapides</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {quickActions.map((action, index) => (
            <button
              key={index}
              onClick={() => router.push(action.path)}
              className={`bg-gradient-to-r ${action.color} text-white p-6 rounded-lg shadow-lg hover:shadow-xl transition-all duration-200 transform hover:-translate-y-1`}
            >
              <div className="text-center">
                <span className="text-3xl block mb-2">{action.icon}</span>
                <h3 className="font-semibold text-lg mb-1">{action.title}</h3>
                <p className="text-sm opacity-90">{action.description}</p>
              </div>
            </button>
          ))}
        </div>
      </div>

      {/* Statistiques détaillées */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
        {/* Métriques supplémentaires */}
        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Métriques Clés</h3>
          <div className="space-y-4">
            <div className="flex justify-between items-center">
              <span className="text-gray-600">Questions dans la banque</span>
              <span className="font-semibold text-gray-900">{stats.totalQuestions}</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-gray-600">Score moyen</span>
              <span className="font-semibold text-gray-900">{stats.averageScore}%</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-gray-600">Modèles IRT actifs</span>
              <span className="font-semibold text-gray-900">{stats.irtModels}</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-gray-600">Taux de complétion</span>
              <span className="font-semibold text-gray-900">94%</span>
            </div>
          </div>
        </div>

        {/* Activité récente */}
        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Activité Récente</h3>
          <div className="space-y-3">
            {recentActivity.slice(0, 4).map((activity) => (
              <div key={activity.id} className="flex items-start space-x-3 p-3 rounded-lg hover:bg-gray-50">
                <span className="text-xl">{getTypeIcon(activity.type)}</span>
                <div className="flex-1 min-w-0">
                  <p className="text-sm font-medium text-gray-900 truncate">{activity.title}</p>
                  <p className="text-xs text-gray-500">{activity.description}</p>
                  <p className="text-xs text-gray-400 mt-1">{activity.timestamp}</p>
                </div>
                <span className={`px-2 py-1 text-xs font-medium rounded-full ${getStatusColor(activity.status)}`}>
                  {getStatusText(activity.status)}
                </span>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Graphiques et visualisations */}
      <div className="bg-white rounded-lg shadow p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Vue d'Ensemble des Performances</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="text-center">
            <div className="w-24 h-24 mx-auto mb-3 relative">
              <svg className="w-24 h-24 transform -rotate-90" viewBox="0 0 36 36">
                <path
                  className="text-gray-200"
                  strokeWidth="3"
                  fill="none"
                  d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                />
                <path
                  className="text-blue-500"
                  strokeWidth="3"
                  strokeDasharray="75, 100"
                  strokeLinecap="round"
                  fill="none"
                  d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                />
              </svg>
              <div className="absolute inset-0 flex items-center justify-center">
                <span className="text-lg font-semibold text-gray-900">75%</span>
              </div>
            </div>
            <p className="text-sm text-gray-600">Satisfaction Étudiants</p>
          </div>

          <div className="text-center">
            <div className="w-24 h-24 mx-auto mb-3 relative">
              <svg className="w-24 h-24 transform -rotate-90" viewBox="0 0 36 36">
                <path
                  className="text-gray-200"
                  strokeWidth="3"
                  fill="none"
                  d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                />
                <path
                  className="text-green-500"
                  strokeWidth="3"
                  strokeDasharray="82, 100"
                  strokeLinecap="round"
                  fill="none"
                  d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                />
              </svg>
              <div className="absolute inset-0 flex items-center justify-center">
                <span className="text-lg font-semibold text-gray-900">82%</span>
              </div>
            </div>
            <p className="text-sm text-gray-600">Taux de Réussite</p>
          </div>

          <div className="text-center">
            <div className="w-24 h-24 mx-auto mb-3 relative">
              <svg className="w-24 h-24 transform -rotate-90" viewBox="0 0 36 36">
                <path
                  className="text-gray-200"
                  strokeWidth="3"
                  fill="none"
                  d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                />
                <path
                  className="text-purple-500"
                  strokeWidth="3"
                  strokeDasharray="68, 100"
                  strokeLinecap="round"
                  fill="none"
                  d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                />
              </svg>
              <div className="absolute inset-0 flex items-center justify-center">
                <span className="text-lg font-semibold text-gray-900">68%</span>
              </div>
            </div>
            <p className="text-sm text-gray-600">Engagement IRT</p>
          </div>
        </div>
      </div>
    </DashboardLayout>
  );
}












