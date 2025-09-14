'use client';

import React, { useState, useEffect } from 'react';
import { 
  BarChart3, 
  Clock, 
  Target, 
  CheckCircle, 
  AlertCircle, 
  TrendingUp,
  BookOpen,
  Calendar
} from 'lucide-react';
import { organizationAPI } from '../api/student/organization';

interface OrganizationStats {
  total_homeworks: number;
  total_study_sessions: number;
  completed_sessions: number;
  total_goals: number;
  completed_goals: number;
  active_reminders: number;
  total_calendar_events: number;
  upcoming_events: number;
}

interface StudyTimeStats {
  total_time: number;
  average_per_session: float;
  sessions_count: number;
  subject_breakdown: Array<{ subject: string; time: number }>;
}

export default function OrganizationStats() {
  const [stats, setStats] = useState<OrganizationStats | null>(null);
  const [studyTimeStats, setStudyTimeStats] = useState<StudyTimeStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [period, setPeriod] = useState<'week' | 'month' | 'year'>('week');

  useEffect(() => {
    const loadStats = async () => {
      try {
        setLoading(true);
        
        // Charger les statistiques d'organisation
        const organizationStats = await organizationAPI.getOrganizationStats();
        setStats(organizationStats);
        
        // Charger les statistiques de temps d'étude
        const timeStats = await organizationAPI.getStudyTimeStats(period);
        setStudyTimeStats(timeStats);
        
      } catch (error) {
        console.error('Erreur lors du chargement des statistiques:', error);
      } finally {
        setLoading(false);
      }
    };

    loadStats();
  }, [period]);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (!stats || !studyTimeStats) {
    return (
      <div className="text-center text-gray-500 py-8">
        Impossible de charger les statistiques
      </div>
    );
  }

  // Calculer les pourcentages
  const sessionCompletionRate = stats.total_study_sessions > 0 
    ? Math.round((stats.completed_sessions / stats.total_study_sessions) * 100) 
    : 0;
  
  const goalCompletionRate = stats.total_goals > 0 
    ? Math.round((stats.completed_goals / stats.total_goals) * 100) 
    : 0;

  // Formater le temps d'étude
  const formatStudyTime = (minutes: number) => {
    const hours = Math.floor(minutes / 60);
    const mins = minutes % 60;
    return hours > 0 ? `${hours}h ${mins}min` : `${mins}min`;
  };

  return (
    <div className="space-y-6">
      {/* Statistiques principales */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {/* Devoirs */}
        <div className="bg-white rounded-lg shadow-md p-6 border-l-4 border-blue-500">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Devoirs</p>
              <p className="text-2xl font-bold text-gray-900">{stats.total_homeworks}</p>
            </div>
            <BookOpen className="h-8 w-8 text-blue-500" />
          </div>
        </div>

        {/* Sessions d'étude */}
        <div className="bg-white rounded-lg shadow-md p-6 border-l-4 border-green-500">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Sessions d'étude</p>
              <p className="text-2xl font-bold text-gray-900">{stats.total_study_sessions}</p>
              <p className="text-sm text-green-600">{sessionCompletionRate}% terminées</p>
            </div>
            <Clock className="h-8 w-8 text-green-500" />
          </div>
        </div>

        {/* Objectifs */}
        <div className="bg-white rounded-lg shadow-md p-6 border-l-4 border-purple-500">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Objectifs</p>
              <p className="text-2xl font-bold text-gray-900">{stats.total_goals}</p>
              <p className="text-sm text-purple-600">{goalCompletionRate}% atteints</p>
            </div>
            <Target className="h-8 w-8 text-purple-500" />
          </div>
        </div>

        {/* Rappels actifs */}
        <div className="bg-white rounded-lg shadow-md p-6 border-l-4 border-yellow-500">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Rappels actifs</p>
              <p className="text-2xl font-bold text-gray-900">{stats.active_reminders}</p>
            </div>
            <AlertCircle className="h-8 w-8 text-yellow-500" />
          </div>
        </div>
      </div>

      {/* Statistiques de temps d'étude */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <div className="flex items-center justify-between mb-6">
          <h3 className="text-lg font-semibold text-gray-900">Temps d'étude</h3>
          
          {/* Sélecteur de période */}
          <div className="flex space-x-2">
            {(['week', 'month', 'year'] as const).map((p) => (
              <button
                key={p}
                onClick={() => setPeriod(p)}
                className={`
                  px-3 py-1 text-sm font-medium rounded-lg transition-colors
                  ${period === p 
                    ? 'bg-blue-600 text-white' 
                    : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                  }
                `}
              >
                {p === 'week' ? 'Semaine' : p === 'month' ? 'Mois' : 'Année'}
              </button>
            ))}
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {/* Temps total */}
          <div className="text-center">
            <div className="text-3xl font-bold text-blue-600 mb-2">
              {formatStudyTime(studyTimeStats.total_time)}
            </div>
            <p className="text-sm text-gray-600">Temps total d'étude</p>
          </div>

          {/* Moyenne par session */}
          <div className="text-center">
            <div className="text-3xl font-bold text-green-600 mb-2">
              {formatStudyTime(Math.round(studyTimeStats.average_per_session))}
            </div>
            <p className="text-sm text-gray-600">Moyenne par session</p>
          </div>

          {/* Nombre de sessions */}
          <div className="text-center">
            <div className="text-3xl font-bold text-purple-600 mb-2">
              {studyTimeStats.sessions_count}
            </div>
            <p className="text-sm text-gray-600">Sessions effectuées</p>
          </div>
        </div>

        {/* Répartition par matière */}
        {studyTimeStats.subject_breakdown.length > 0 && (
          <div className="mt-6">
            <h4 className="text-md font-medium text-gray-900 mb-4">Répartition par matière</h4>
            <div className="space-y-3">
              {studyTimeStats.subject_breakdown.map((subject, index) => (
                <div key={index} className="flex items-center justify-between">
                  <span className="text-sm font-medium text-gray-700">{subject.subject}</span>
                  <div className="flex items-center space-x-3">
                    <div className="w-32 bg-gray-200 rounded-full h-2">
                      <div 
                        className="bg-blue-600 h-2 rounded-full"
                        style={{ 
                          width: `${(subject.time / studyTimeStats.total_time) * 100}%` 
                        }}
                      ></div>
                    </div>
                    <span className="text-sm text-gray-600 w-20 text-right">
                      {formatStudyTime(subject.time)}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Statistiques du calendrier */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <div className="flex items-center space-x-3 mb-4">
          <Calendar className="h-6 w-6 text-indigo-600" />
          <h3 className="text-lg font-semibold text-gray-900">Calendrier</h3>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="text-center p-4 bg-indigo-50 rounded-lg">
            <div className="text-2xl font-bold text-indigo-600 mb-2">
              {stats.total_calendar_events}
            </div>
            <p className="text-sm text-indigo-700">Événements total</p>
          </div>
          
          <div className="text-center p-4 bg-green-50 rounded-lg">
            <div className="text-2xl font-bold text-green-600 mb-2">
              {stats.upcoming_events}
            </div>
            <p className="text-sm text-green-700">Événements à venir</p>
          </div>
        </div>
      </div>
    </div>
  );
}
