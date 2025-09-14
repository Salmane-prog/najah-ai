'use client';

import React, { useState, useEffect } from 'react';
import Sidebar from '../../../../components/Sidebar';
import { useAuth  } from '../../../../hooks/useAuth';
import NotificationBell from '../../../../components/NotificationBell';
import { 
  fetchRecentActivity, 
  fetchActivityStats, 
  fetchActivityTimeline,
  fetchActivityAchievements
} from '../../../../api/student/activity';
import { Activity, Clock, TrendingUp, BookOpen, Target, Award, Calendar, BarChart3, Filter } from 'lucide-react';

export default function ActivityPage() {
  const { user, token } = useAuth();
  const userId = user?.id;
  
  const [recentActivity, setRecentActivity] = useState<any>(null);
  const [activityStats, setActivityStats] = useState<any>(null);
  const [activityTimeline, setActivityTimeline] = useState<any>(null);
  const [activityAchievements, setActivityAchievements] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [selectedPeriod, setSelectedPeriod] = useState('week');
  const [selectedFilter, setSelectedFilter] = useState('all');

  useEffect(() => {
    if (!userId) return;
    
    const loadActivityData = async () => {
      try {
        const [recentRes, statsRes, timelineRes, achievementsRes] = await Promise.all([
          fetchRecentActivity(userId, 20),
          fetchActivityStats(userId, selectedPeriod),
          fetchActivityTimeline(userId, 7),
          fetchActivityAchievements(userId)
        ]);

        setRecentActivity(recentRes);
        setActivityStats(statsRes);
        setActivityTimeline(timelineRes);
        setActivityAchievements(achievementsRes);
        setLoading(false);
      } catch (error) {
        console.error('Erreur lors du chargement de l\'activité:', error);
        setLoading(false);
      }
    };

    loadActivityData();
  }, [userId, selectedPeriod]);

  const getActivityIcon = (type: string) => {
    switch (type) {
      case 'quiz_completed':
        return <Target className="text-blue-500" size={16} />;
      case 'achievement_unlocked':
        return <Award className="text-yellow-500" size={16} />;
      case 'study_session':
        return <BookOpen className="text-green-500" size={16} />;
      case 'level_up':
        return <TrendingUp className="text-purple-500" size={16} />;
      default:
        return <Activity className="text-gray-500" size={16} />;
    }
  };

  const getActivityColor = (type: string) => {
    switch (type) {
      case 'quiz_completed':
        return 'bg-blue-100';
      case 'achievement_unlocked':
        return 'bg-yellow-100';
      case 'study_session':
        return 'bg-green-100';
      case 'level_up':
        return 'bg-purple-100';
      default:
        return 'bg-gray-100';
    }
  };

  const formatTimeAgo = (dateString: string) => {
    const date = new Date(dateString);
    const now = new Date();
    const diffInMinutes = Math.floor((now.getTime() - date.getTime()) / (1000 * 60));
    
    if (diffInMinutes < 1) return 'À l\'instant';
    if (diffInMinutes < 60) return `Il y a ${diffInMinutes} min`;
    if (diffInMinutes < 1440) return `Il y a ${Math.floor(diffInMinutes / 60)}h`;
    return `Il y a ${Math.floor(diffInMinutes / 1440)}j`;
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('fr-FR', {
      weekday: 'long',
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
  };

  const filteredActivities = recentActivity?.activities?.filter((activity: any) => {
    if (selectedFilter === 'all') return true;
    return activity.type === selectedFilter;
  }) || [];

  if (!userId) {
    return (
      <div className="flex min-h-screen bg-gray-50">
        <Sidebar />
        <div className="flex-1 flex items-center justify-center">
          <div className="text-red-600 text-lg font-bold">Erreur : utilisateur non connecté.</div>
        </div>
      </div>
    );
  }

  if (loading) {
    return (
      <div className="flex min-h-screen bg-gray-50">
        <Sidebar />
        <div className="flex-1 flex items-center justify-center">
          <div className="text-blue-600 animate-pulse text-xl font-bold">Chargement de l'activité...</div>
        </div>
      </div>
    );
  }

  return (
    <div className="flex min-h-screen bg-gray-50">
      <Sidebar />
      <div className="flex-1 overflow-auto pl-0 md:pl-56">
        <div className="p-6">
          {/* Header */}
          <div className="mb-8 flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-gray-800 mb-2 flex items-center gap-3">
                <Activity className="text-blue-600" />
                Activité
              </h1>
              <p className="text-gray-600">Suivez votre progression et vos activités</p>
            </div>
            <div className="flex items-center gap-4">
              <NotificationBell />
            </div>
          </div>

          {/* Filtres */}
          <div className="mb-6 flex items-center gap-4">
            <div className="flex items-center gap-2">
              <Filter className="text-gray-500" size={16} />
              <span className="text-sm font-medium text-gray-700">Période:</span>
              <select
                value={selectedPeriod}
                onChange={(e) => setSelectedPeriod(e.target.value)}
                className="px-3 py-1 border border-gray-300 rounded-md text-sm focus:ring-2 focus:ring-blue-500"
              >
                <option value="week">Cette semaine</option>
                <option value="month">Ce mois</option>
                <option value="year">Cette année</option>
              </select>
            </div>
            
            <div className="flex items-center gap-2">
              <span className="text-sm font-medium text-gray-700">Filtrer:</span>
              <select
                value={selectedFilter}
                onChange={(e) => setSelectedFilter(e.target.value)}
                className="px-3 py-1 border border-gray-300 rounded-md text-sm focus:ring-2 focus:ring-blue-500"
              >
                <option value="all">Toutes les activités</option>
                <option value="quiz_completed">Quiz complétés</option>
                <option value="achievement_unlocked">Achievements débloqués</option>
                <option value="study_session">Sessions d'étude</option>
                <option value="level_up">Niveaux supérieurs</option>
              </select>
            </div>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Statistiques principales */}
            <div className="lg:col-span-1">
              <div className="bg-white rounded-lg shadow-sm p-6 mb-6">
                <h2 className="text-xl font-bold text-gray-800 mb-4 flex items-center gap-2">
                  <BarChart3 className="text-blue-500" />
                  Statistiques
                </h2>
                
                <div className="space-y-4">
                  <div className="bg-blue-50 rounded-lg p-4">
                    <div className="flex items-center gap-2 mb-2">
                      <Target className="text-blue-500" size={16} />
                      <span className="font-medium">Quiz Complétés</span>
                    </div>
                    <div className="text-2xl font-bold text-blue-600">
                      {activityStats?.quiz_stats?.total_quizzes || 0}
                    </div>
                    <div className="text-sm text-gray-600">
                      Moyenne: {activityStats?.quiz_stats?.average_score?.toFixed(1) || 0}%
                    </div>
                  </div>

                  <div className="bg-green-50 rounded-lg p-4">
                    <div className="flex items-center gap-2 mb-2">
                      <BookOpen className="text-green-500" size={16} />
                      <span className="font-medium">Sessions d'Étude</span>
                    </div>
                    <div className="text-2xl font-bold text-green-600">
                      {activityStats?.learning_stats?.total_sessions || 0}
                    </div>
                    <div className="text-sm text-gray-600">
                      {Math.floor((activityStats?.learning_stats?.total_study_time || 0) / 60)} minutes
                    </div>
                  </div>

                  <div className="bg-purple-50 rounded-lg p-4">
                    <div className="flex items-center gap-2 mb-2">
                      <TrendingUp className="text-purple-500" size={16} />
                      <span className="font-medium">Activités Aujourd'hui</span>
                    </div>
                    <div className="text-2xl font-bold text-purple-600">
                      {activityStats?.daily_activities?.[0]?.count || 0}
                    </div>
                    <div className="text-sm text-gray-600">
                      Cette semaine
                    </div>
                  </div>
                </div>
              </div>

              {/* Achievements basés sur l'activité */}
              {activityAchievements && (
                <div className="bg-white rounded-lg shadow-sm p-6">
                  <h2 className="text-xl font-bold text-gray-800 mb-4 flex items-center gap-2">
                    <Award className="text-yellow-500" />
                    Achievements d'Activité
                  </h2>
                  
                  <div className="space-y-3">
                    {activityAchievements.achievements?.map((achievement: any, index: number) => (
                      <div key={index} className={`p-3 rounded-lg border ${
                        achievement.achieved 
                          ? 'bg-yellow-50 border-yellow-200' 
                          : 'bg-gray-50 border-gray-200'
                      }`}>
                        <div className="flex items-center gap-3">
                          <div className={`w-8 h-8 rounded-full flex items-center justify-center ${
                            achievement.achieved ? 'bg-yellow-100' : 'bg-gray-100'
                          }`}>
                            {achievement.achieved ? (
                              <Award className="text-yellow-600" size={16} />
                            ) : (
                              <Target className="text-gray-400" size={16} />
                            )}
                          </div>
                          <div className="flex-1">
                            <p className={`font-medium ${
                              achievement.achieved ? 'text-yellow-800' : 'text-gray-600'
                            }`}>
                              {achievement.title}
                            </p>
                            <p className="text-xs text-gray-500">{achievement.description}</p>
                            {achievement.achieved && achievement.achieved_at && (
                              <p className="text-xs text-yellow-600">
                                Débloqué le {new Date(achievement.achieved_at).toLocaleDateString()}
                              </p>
                            )}
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>

            {/* Timeline d'activité */}
            <div className="lg:col-span-2">
              <div className="bg-white rounded-lg shadow-sm p-6">
                <h2 className="text-xl font-bold text-gray-800 mb-4 flex items-center gap-2">
                  <Calendar className="text-green-500" />
                  Timeline d'Activité
                </h2>
                
                <div className="space-y-6">
                  {activityTimeline?.timeline ? (
                    Object.entries(activityTimeline.timeline).map(([date, activities]: [string, any]) => (
                      <div key={date} className="border-l-2 border-blue-200 pl-4">
                        <div className="mb-3">
                          <h3 className="font-semibold text-gray-800">{formatDate(date)}</h3>
                        </div>
                        <div className="space-y-3">
                          {activities.map((activity: any, index: number) => (
                            <div key={activity.id || index} className="bg-gray-50 rounded-lg p-4">
                              <div className="flex items-start gap-3">
                                <div className={`w-8 h-8 rounded-full flex items-center justify-center ${getActivityColor(activity.type)}`}>
                                  {getActivityIcon(activity.type)}
                                </div>
                                <div className="flex-1 min-w-0">
                                  <div className="flex items-center justify-between mb-1">
                                    <p className="text-sm font-medium text-gray-800">
                                      {activity.description}
                                    </p>
                                    <div className="flex items-center gap-1 text-xs text-gray-500">
                                      <Clock size={12} />
                                      {formatTimeAgo(activity.created_at)}
                                    </div>
                                  </div>
                                  <p className="text-xs text-gray-600 mb-2">
                                    {activity.type === 'quiz_completed' ? 'Quiz terminé' : 
                                     activity.type === 'achievement_unlocked' ? 'Achievement débloqué' :
                                     activity.type === 'study_session' ? 'Session d\'étude' :
                                     activity.type === 'level_up' ? 'Niveau supérieur' : 'Activité'}
                                  </p>
                                  {activity.score && (
                                    <div className="flex items-center gap-2">
                                      <div className="text-xs font-medium text-green-600">
                                        Score: {activity.score}%
                                      </div>
                                      {activity.duration && (
                                        <div className="text-xs text-gray-500">
                                          Durée: {Math.floor(activity.duration / 60)}min
                                        </div>
                                      )}
                                    </div>
                                  )}
                                </div>
                              </div>
                            </div>
                          ))}
                        </div>
                      </div>
                    ))
                  ) : (
                    <div className="text-center py-8 text-gray-500">
                      <Activity className="mx-auto mb-2 text-gray-400" size={32} />
                      <p>Aucune activité récente</p>
                      <p className="text-sm">Commencez à étudier pour voir votre timeline</p>
                    </div>
                  )}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
} 