'use client';

import React, { useState, useEffect } from 'react';
import { 
  BookOpen, 
  Map, 
  Lightbulb, 
  BarChart3, 
  Calendar, 
  Target, 
  TrendingUp, 
  Award,
  Clock,
  CheckCircle,
  AlertCircle
} from 'lucide-react';
import { useAuth  } from '../../hooks/useAuth';
import InitialAssessmentWidget from './InitialAssessmentWidget';
import LearningPathWidget from './LearningPathWidget';
import IntelligentRecommendationsWidget from './IntelligentRecommendationsWidget';
import EnhancedChartsWidget from './EnhancedChartsWidget';
import ModernCalendarWidget from './ModernCalendarWidget';
import UnifiedStatsWidget from './UnifiedStatsWidget';

interface DashboardStats {
  totalAssessments: number;
  completedAssessments: number;
  activeLearningPaths: number;
  completedLearningPaths: number;
  totalQuizzes: number;
  completedQuizzes: number;
  totalHomework: number;
  completedHomework: number;
  overallProgress: number;
  studyStreak: number;
  averageScore: number;
}

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export default function IntelligentStudentDashboard({ className = '' }: { className?: string }) {
  const [stats, setStats] = useState<DashboardStats>({
    totalAssessments: 0,
    completedAssessments: 0,
    activeLearningPaths: 0,
    completedLearningPaths: 0,
    totalQuizzes: 0,
    completedQuizzes: 0,
    totalHomework: 0,
    completedHomework: 0,
    overallProgress: 0,
    studyStreak: 0,
    averageScore: 0
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState<'overview' | 'assessments' | 'learning' | 'analytics'>('overview');

  const { user, token } = useAuth();

  useEffect(() => {
    if (user?.id && token) {
      loadDashboardStats();
    }
  }, [user?.id, token]);

  const loadDashboardStats = async () => {
    try {
      setLoading(true);
      setError(null);

      const [
        assessmentsRes,
        learningPathsRes,
        quizzesRes,
        homeworksRes,
        progressRes
      ] = await Promise.all([
        fetch(`${API_BASE_URL}/api/v1/assessments/student/${user?.id}/pending`, {
          headers: { 'Authorization': `Bearer ${token}` }
        }).catch(() => ({ ok: false, json: () => [] })),
        
        fetch(`${API_BASE_URL}/api/v1/assessments/student/${user?.id}/completed`, {
          headers: { 'Authorization': `Bearer ${token}` }
        }).catch(() => ({ ok: false, json: () => [] })),
        
        fetch(`${API_BASE_URL}/api/v1/learning_paths/student/${user?.id}/active`, {
          headers: { 'Authorization': `Bearer ${token}` }
        }).catch(() => ({ ok: false, json: () => [] })),
        
        fetch(`${API_BASE_URL}/api/v1/learning_paths/student/${user?.id}/completed`, {
          headers: { 'Authorization': `Bearer ${token}` }
        }).catch(() => ({ ok: false, json: () => [] })),
        
        fetch(`${API_BASE_URL}/api/v1/quizzes/assigned/${user?.id}`, {
          headers: { 'Authorization': `Bearer ${token}` }
        }).catch(() => ({ ok: false, json: () => [] })),
        
        fetch(`${API_BASE_URL}/api/v1/assignments/student/${user?.id}/assigned`, {
          headers: { 'Authorization': `Bearer ${token}` }
        }).catch(() => ({ ok: false, json: () => [] })),
        
        fetch(`${API_BASE_URL}/api/v1/analytics/student/${user?.id}/progress`, {
          headers: { 'Authorization': `Bearer ${token}` }
        }).catch(() => ({ ok: false, json: () => ({ overall_progress: 0, study_streak: 0, average_score: 0 }) }))
      ]);

      const pendingAssessments = assessmentsRes.ok ? await assessmentsRes.json() : [];
      const completedAssessments = learningPathsRes.ok ? await learningPathsRes.json() : [];
      const activePaths = quizzesRes.ok ? await quizzesRes.json() : [];
      const completedPaths = homeworksRes.ok ? await homeworksRes.json() : [];
      const progress = progressRes.ok ? await progressRes.json() : { overall_progress: 0, study_streak: 0, average_score: 0 };

      setStats({
        totalAssessments: pendingAssessments.length + completedAssessments.length,
        completedAssessments: completedAssessments.length,
        activeLearningPaths: activePaths.length,
        completedLearningPaths: completedPaths.length,
        totalQuizzes: 0, // À remplacer par l'endpoint réel
        completedQuizzes: 0,
        totalHomework: 0, // À remplacer par l'endpoint réel
        completedHomework: 0,
        overallProgress: progress.overall_progress || 0,
        studyStreak: progress.study_streak || 0,
        averageScore: progress.average_score || 0
      });

    } catch (err) {
      console.error('Erreur lors du chargement des statistiques:', err);
      setError('Erreur lors du chargement des statistiques');
    } finally {
      setLoading(false);
    }
  };

  const getProgressColor = (progress: number) => {
    if (progress >= 80) return 'text-green-600';
    if (progress >= 60) return 'text-yellow-600';
    return 'text-red-600';
  };

  const getProgressBgColor = (progress: number) => {
    if (progress >= 80) return 'bg-green-100';
    if (progress >= 60) return 'bg-yellow-100';
    return 'bg-red-100';
  };

  if (loading) {
    return (
      <div className={`bg-white rounded-lg shadow-md p-6 ${className}`}>
        <div className="animate-pulse">
          <div className="h-8 bg-gray-200 rounded w-1/3 mb-6"></div>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
            {[...Array(4)].map((_, i) => (
              <div key={i} className="h-24 bg-gray-200 rounded"></div>
            ))}
          </div>
          <div className="h-64 bg-gray-200 rounded"></div>
        </div>
      </div>
    );
  }

  return (
    <div className={`bg-white rounded-lg shadow-md ${className}`}>
      {/* Header du dashboard */}
      <div className="p-6 border-b border-gray-200">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-gray-800">
              Tableau de Bord Intelligent
            </h1>
            <p className="text-gray-600 mt-1">
              Bienvenue, {user?.first_name || 'Étudiant'} ! Suivez votre progression et recevez des recommandations personnalisées.
            </p>
          </div>
          
          <div className="text-right">
            <div className="text-3xl font-bold text-blue-600">
              {stats.overallProgress}%
            </div>
            <div className="text-sm text-gray-600">Progression globale</div>
          </div>
        </div>

        {/* Navigation par onglets */}
        <div className="flex space-x-1 mt-6">
          {[
            { id: 'overview', label: 'Vue d\'ensemble', icon: BarChart3 },
            { id: 'assessments', label: 'Évaluations', icon: BookOpen },
            { id: 'learning', label: 'Parcours', icon: Map },
            { id: 'analytics', label: 'Analytics', icon: TrendingUp }
          ].map((tab) => {
            const Icon = tab.icon;
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id as any)}
                className={`flex items-center space-x-2 px-4 py-2 rounded-lg font-medium transition-colors ${
                  activeTab === tab.id
                    ? 'bg-blue-100 text-blue-700 border border-blue-200'
                    : 'text-gray-600 hover:text-gray-800 hover:bg-gray-100'
                }`}
              >
                <Icon className="w-4 h-4" />
                <span>{tab.label}</span>
              </button>
            );
          })}
        </div>
      </div>

      {/* Contenu principal */}
      <div className="p-6">
        {error && (
          <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg">
            <div className="flex items-center text-red-800">
              <AlertCircle className="w-5 h-5 mr-2" />
              {error}
            </div>
          </div>
        )}

        {/* Vue d'ensemble */}
        {activeTab === 'overview' && (
          <div className="space-y-6">
            {/* Statistiques principales */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
              <div className="bg-gradient-to-br from-blue-50 to-blue-100 p-4 rounded-lg border border-blue-200">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium text-blue-600">Évaluations</p>
                    <p className="text-2xl font-bold text-blue-800">
                      {stats.completedAssessments}/{stats.totalAssessments}
                    </p>
                  </div>
                  <BookOpen className="w-8 h-8 text-blue-600" />
                </div>
                <div className="mt-2">
                  <div className="w-full bg-blue-200 rounded-full h-2">
                    <div 
                      className="bg-blue-600 h-2 rounded-full transition-all duration-300"
                      style={{ width: `${stats.totalAssessments > 0 ? (stats.completedAssessments / stats.totalAssessments) * 100 : 0}%` }}
                    ></div>
                  </div>
                </div>
              </div>

              <div className="bg-gradient-to-br from-green-50 to-green-100 p-4 rounded-lg border border-green-200">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium text-green-600">Parcours</p>
                    <p className="text-2xl font-bold text-green-800">
                      {stats.activeLearningPaths} actifs
                    </p>
                  </div>
                  <Map className="w-8 h-8 text-green-600" />
                </div>
                <div className="mt-2 text-sm text-green-600">
                  {stats.completedLearningPaths} terminés
                </div>
              </div>

              <div className="bg-gradient-to-br from-purple-50 to-purple-100 p-4 rounded-lg border border-purple-200">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium text-purple-600">Score Moyen</p>
                    <p className="text-2xl font-bold text-purple-800">
                      {stats.averageScore}%
                    </p>
                  </div>
                  <Award className="w-8 h-8 text-purple-600" />
                </div>
                <div className="mt-2 text-sm text-purple-600">
                  Basé sur {stats.completedAssessments} évaluations
                </div>
              </div>

              <div className="bg-gradient-to-br from-orange-50 to-orange-100 p-4 rounded-lg border border-orange-200">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium text-orange-600">Série d'étude</p>
                    <p className="text-2xl font-bold text-orange-800">
                      {stats.studyStreak} jours
                    </p>
                  </div>
                  <TrendingUp className="w-8 h-8 text-orange-600" />
                </div>
                <div className="mt-2 text-sm text-orange-600">
                  Continuez votre série !
                </div>
              </div>
            </div>

            {/* Widgets principaux */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <InitialAssessmentWidget />
              <LearningPathWidget />
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <IntelligentRecommendationsWidget />
              <EnhancedChartsWidget />
            </div>

            <div className="grid grid-cols-1 gap-6">
              <ModernCalendarWidget />
            </div>
          </div>
        )}

        {/* Onglet Évaluations */}
        {activeTab === 'assessments' && (
          <div className="space-y-6">
            <InitialAssessmentWidget />
          </div>
        )}

        {/* Onglet Parcours */}
        {activeTab === 'learning' && (
          <div className="space-y-6">
            <LearningPathWidget />
          </div>
        )}

        {/* Onglet Analytics */}
        {activeTab === 'analytics' && (
          <div className="space-y-6">
            <EnhancedChartsWidget />
            <UnifiedStatsWidget />
            <IntelligentRecommendationsWidget />
          </div>
        )}
      </div>
    </div>
  );
}




