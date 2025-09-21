'use client';

import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import DashboardLayout from './DashboardLayout';

interface StudentStats {
  totalAssessments: number;
  completedAssessments: number;
  averageScore: number;
  currentStreak: number;
  cognitiveProfile: string;
  learningStyle: string;
  adaptiveTestsTaken: number;
}

interface UpcomingAssessment {
  id: string;
  title: string;
  subject: string;
  type: 'standard' | 'adaptive';
  dueDate: string;
  estimatedDuration: string;
  difficulty: 'easy' | 'medium' | 'hard';
}

interface RecentResult {
  id: string;
  title: string;
  score: number;
  maxScore: number;
  type: 'standard' | 'adaptive';
  date: string;
  feedback: string;
}

export default function StudentDashboard() {
  const router = useRouter();
  const [stats, setStats] = useState<StudentStats>({
    totalAssessments: 0,
    completedAssessments: 0,
    averageScore: 0,
    currentStreak: 0,
    cognitiveProfile: '',
    learningStyle: '',
    adaptiveTestsTaken: 0
  });

  const [upcomingAssessments, setUpcomingAssessments] = useState<UpcomingAssessment[]>([]);
  const [recentResults, setRecentResults] = useState<RecentResult[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Simuler le chargement des données
    setTimeout(() => {
      setStats({
        totalAssessments: 15,
        completedAssessments: 12,
        averageScore: 82.5,
        currentStreak: 7,
        cognitiveProfile: 'Analytique',
        learningStyle: 'Visuel + Kinesthésique',
        adaptiveTestsTaken: 5
      });

      setUpcomingAssessments([
        {
          id: '1',
          title: 'Évaluation Mathématiques - Algèbre',
          subject: 'Mathématiques',
          type: 'adaptive',
          dueDate: 'Dans 2 jours',
          estimatedDuration: '45 min',
          difficulty: 'medium'
        },
        {
          id: '2',
          title: 'Test Physique - Mécanique',
          subject: 'Physique',
          type: 'standard',
          dueDate: 'Dans 1 semaine',
          estimatedDuration: '60 min',
          difficulty: 'hard'
        },
        {
          id: '3',
          title: 'Quiz Histoire - Révolution',
          subject: 'Histoire',
          type: 'adaptive',
          dueDate: 'Dans 3 jours',
          estimatedDuration: '30 min',
          difficulty: 'easy'
        }
      ]);

      setRecentResults([
        {
          id: '1',
          title: 'Évaluation Mathématiques - Géométrie',
          score: 85,
          maxScore: 100,
          type: 'adaptive',
          date: 'Il y a 2 jours',
          feedback: 'Excellent travail sur les théorèmes ! Continuez ainsi.'
        },
        {
          id: '2',
          title: 'Test Physique - Thermodynamique',
          score: 78,
          maxScore: 100,
          type: 'standard',
          date: 'Il y a 1 semaine',
          feedback: 'Bonnes bases, révisez les formules de pression.'
        },
        {
          id: '3',
          title: 'Quiz Chimie - Réactions',
          score: 92,
          maxScore: 100,
          type: 'adaptive',
          date: 'Il y a 2 semaines',
          feedback: 'Parfait ! Vous maîtrisez bien les équilibres.'
        }
      ]);

      setLoading(false);
    }, 1000);
  }, []);

  const getDifficultyColor = (difficulty: string) => {
    switch (difficulty) {
      case 'easy':
        return 'bg-green-100 text-green-800';
      case 'medium':
        return 'bg-yellow-100 text-yellow-800';
      case 'hard':
        return 'bg-red-100 text-red-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const getDifficultyText = (difficulty: string) => {
    switch (difficulty) {
      case 'easy':
        return 'Facile';
      case 'medium':
        return 'Moyen';
      case 'hard':
        return 'Difficile';
      default:
        return 'Inconnu';
    }
  };

  const getTypeIcon = (type: string) => {
    return type === 'adaptive' ? '🔄' : '📝';
  };

  const getTypeText = (type: string) => {
    return type === 'adaptive' ? 'Adaptatif' : 'Standard';
  };

  const quickActions = [
    {
      title: 'Évaluation Adaptative',
      description: 'Test intelligent personnalisé',
      icon: '🔄',
      path: '/assessment/adaptive',
      color: 'from-purple-500 to-pink-600'
    },
    {
      title: 'Mon Profil Cognitif',
      description: 'Découvrir mon style d\'apprentissage',
      icon: '🧠',
      path: '/dashboard/student/cognitive-profile',
      color: 'from-blue-500 to-indigo-600'
    },
    {
      title: 'Mes Résultats',
      description: 'Voir tous mes scores',
      icon: '📊',
      path: '/assessment/results',
      color: 'from-green-500 to-emerald-600'
    },
    {
      title: 'Progression',
      description: 'Suivre mes améliorations',
      icon: '📈',
      path: '/dashboard/student/progress',
      color: 'from-orange-500 to-red-600'
    }
  ];

  if (loading) {
    return (
      <DashboardLayout userType="student" title="Tableau de Bord" subtitle="Chargement...">
        <div className="flex items-center justify-center h-64">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
        </div>
      </DashboardLayout>
    );
  }

  return (
    <DashboardLayout 
      userType="student" 
      title="Tableau de Bord Étudiant" 
      subtitle="Apprentissage adaptatif et suivi des progrès"
    >
      {/* En-tête avec métriques principales */}
      <div className="mb-8">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <div className="bg-white rounded-lg shadow p-6 border-l-4 border-blue-500">
            <div className="flex items-center">
              <div className="p-3 rounded-full bg-blue-100 text-blue-600">
                <span className="text-2xl">📝</span>
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Évaluations</p>
                <p className="text-2xl font-semibold text-gray-900">{stats.completedAssessments}/{stats.totalAssessments}</p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6 border-l-4 border-green-500">
            <div className="flex items-center">
              <div className="p-3 rounded-full bg-green-100 text-green-600">
                <span className="text-2xl">📊</span>
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Score Moyen</p>
                <p className="text-2xl font-semibold text-gray-900">{stats.averageScore}%</p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6 border-l-4 border-purple-500">
            <div className="flex items-center">
              <div className="p-3 rounded-full bg-purple-100 text-purple-600">
                <span className="text-2xl">🔥</span>
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Série Actuelle</p>
                <p className="text-2xl font-semibold text-gray-900">{stats.currentStreak} jours</p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6 border-l-4 border-orange-500">
            <div className="flex items-center">
              <div className="p-3 rounded-full bg-orange-100 text-orange-600">
                <span className="text-2xl">🔄</span>
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Tests Adaptatifs</p>
                <p className="text-2xl font-semibold text-gray-900">{stats.adaptiveTestsTaken}</p>
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

      {/* Profil cognitif et évaluations à venir */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
        {/* Profil cognitif */}
        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Mon Profil Cognitif</h3>
          <div className="space-y-4">
            <div className="flex justify-between items-center">
              <span className="text-gray-600">Style d'apprentissage</span>
              <span className="font-semibold text-gray-900">{stats.learningStyle}</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-gray-600">Profil cognitif</span>
              <span className="font-semibold text-gray-900">{stats.cognitiveProfile}</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-gray-600">Tests adaptatifs</span>
              <span className="font-semibold text-gray-900">{stats.adaptiveTestsTaken}</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-gray-600">Série actuelle</span>
              <span className="font-semibold text-gray-900">{stats.currentStreak} jours</span>
            </div>
          </div>
          
          <button
            onClick={() => router.push('/dashboard/student/cognitive-profile')}
            className="w-full mt-4 bg-gradient-to-r from-blue-500 to-indigo-600 text-white py-2 px-4 rounded-lg hover:from-blue-600 hover:to-indigo-700 transition-all duration-200"
          >
            Voir mon profil complet
          </button>
        </div>

        {/* Évaluations à venir */}
        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Évaluations à Venir</h3>
          <div className="space-y-3">
            {upcomingAssessments.slice(0, 3).map((assessment) => (
              <div key={assessment.id} className="p-3 rounded-lg border border-gray-200 hover:border-blue-300 transition-colors">
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <div className="flex items-center space-x-2 mb-1">
                      <span className="text-lg">{getTypeIcon(assessment.type)}</span>
                      <span className="text-xs px-2 py-1 rounded-full bg-gray-100 text-gray-600">
                        {getTypeText(assessment.type)}
                      </span>
                      <span className={`px-2 py-1 text-xs font-medium rounded-full ${getDifficultyColor(assessment.difficulty)}`}>
                        {getDifficultyText(assessment.difficulty)}
                      </span>
                    </div>
                    <h4 className="font-medium text-gray-900 text-sm">{assessment.title}</h4>
                    <p className="text-xs text-gray-500">{assessment.subject}</p>
                    <div className="flex items-center space-x-4 mt-2 text-xs text-gray-500">
                      <span>📅 {assessment.dueDate}</span>
                      <span>⏱️ {assessment.estimatedDuration}</span>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
          
          <button
            onClick={() => router.push('/assessment')}
            className="w-full mt-4 bg-gradient-to-r from-green-500 to-emerald-600 text-white py-2 px-4 rounded-lg hover:from-green-600 hover:to-emerald-700 transition-all duration-200"
          >
            Voir toutes les évaluations
          </button>
        </div>
      </div>

      {/* Résultats récents */}
      <div className="bg-white rounded-lg shadow p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Résultats Récents</h3>
        <div className="space-y-4">
          {recentResults.map((result) => (
            <div key={result.id} className="flex items-center space-x-4 p-4 rounded-lg border border-gray-200 hover:border-blue-300 transition-colors">
              <div className="flex-shrink-0">
                <div className="w-16 h-16 rounded-full bg-gradient-to-r from-blue-500 to-indigo-600 flex items-center justify-center text-white font-bold text-lg">
                  {Math.round((result.score / result.maxScore) * 100)}%
                </div>
              </div>
              
              <div className="flex-1 min-w-0">
                <div className="flex items-center space-x-2 mb-1">
                  <h4 className="font-medium text-gray-900">{result.title}</h4>
                  <span className="text-xs px-2 py-1 rounded-full bg-gray-100 text-gray-600">
                    {getTypeText(result.type)}
                  </span>
                </div>
                <p className="text-sm text-gray-600 mb-2">{result.feedback}</p>
                <div className="flex items-center space-x-4 text-xs text-gray-500">
                  <span>📊 {result.score}/{result.maxScore} points</span>
                  <span>📅 {result.date}</span>
                </div>
              </div>
            </div>
          ))}
        </div>
        
        <button
          onClick={() => router.push('/assessment/results')}
          className="w-full mt-4 bg-gradient-to-r from-purple-500 to-pink-600 text-white py-2 px-4 rounded-lg hover:from-purple-600 hover:to-pink-700 transition-all duration-200"
        >
          Voir tous mes résultats
        </button>
      </div>

      {/* Graphique de progression */}
      <div className="bg-white rounded-lg shadow p-6 mt-8">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Ma Progression</h3>
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
                  strokeDasharray="82.5, 100"
                  strokeLinecap="round"
                  fill="none"
                  d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                />
              </svg>
              <div className="absolute inset-0 flex items-center justify-center">
                <span className="text-lg font-semibold text-gray-900">{stats.averageScore}%</span>
              </div>
            </div>
            <p className="text-sm text-gray-600">Score Moyen</p>
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
                  strokeDasharray="80, 100"
                  strokeLinecap="round"
                  fill="none"
                  d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                />
              </svg>
              <div className="absolute inset-0 flex items-center justify-center">
                <span className="text-lg font-semibold text-gray-900">80%</span>
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
            <p className="text-sm text-gray-600">Engagement</p>
          </div>
        </div>
      </div>
    </DashboardLayout>
  );
}















