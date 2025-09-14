import React from 'react';
import { Activity, Clock, TrendingUp, BookOpen, Target, Award } from 'lucide-react';

interface ActivityWidgetProps {
  activityData?: any;
  className?: string;
}

export const ActivityWidget: React.FC<ActivityWidgetProps> = ({ 
  activityData,
  className = '' 
}) => {
  const recentActivities = activityData?.recent?.activities || [];
  const activityStats = activityData?.stats;

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

  return (
    <div className={`space-y-6 ${className}`}>
      <div className="flex items-center gap-2 mb-4">
        <Activity className="text-blue-500" size={24} />
        <h3 className="text-xl font-bold text-gray-800">Activité Récente</h3>
      </div>

      {/* Statistiques d'activité */}
      {activityStats && (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
          <div className="bg-white border border-gray-200 rounded-lg p-4">
            <div className="flex items-center gap-2 mb-2">
              <Target className="text-blue-500" size={16} />
              <span className="text-sm font-medium">Quiz Complétés</span>
            </div>
            <div className="text-2xl font-bold text-blue-600">
              {activityStats.quiz_stats?.total_quizzes || 0}
            </div>
            <div className="text-xs text-gray-500">
              Moyenne: {activityStats.quiz_stats?.average_score?.toFixed(1) || 0}%
            </div>
          </div>

          <div className="bg-white border border-gray-200 rounded-lg p-4">
            <div className="flex items-center gap-2 mb-2">
              <BookOpen className="text-green-500" size={16} />
              <span className="text-sm font-medium">Sessions d'Étude</span>
            </div>
            <div className="text-2xl font-bold text-green-600">
              {activityStats.learning_stats?.total_sessions || 0}
            </div>
            <div className="text-xs text-gray-500">
              {Math.floor((activityStats.learning_stats?.total_study_time || 0) / 60)} min
            </div>
          </div>

          <div className="bg-white border border-gray-200 rounded-lg p-4">
            <div className="flex items-center gap-2 mb-2">
              <TrendingUp className="text-purple-500" size={16} />
              <span className="text-sm font-medium">Activités Aujourd'hui</span>
            </div>
            <div className="text-2xl font-bold text-purple-600">
              {activityStats.daily_activities?.[0]?.count || 0}
            </div>
            <div className="text-xs text-gray-500">
              Cette semaine
            </div>
          </div>
        </div>
      )}

      {/* Activités récentes */}
      <div className="space-y-3 max-h-96 overflow-y-auto">
        {recentActivities.length > 0 ? (
          recentActivities.map((activity: any, index: number) => (
            <div key={activity.id || index} className="bg-white border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
              <div className="flex items-start gap-3">
                <div className={`w-8 h-8 rounded-full flex items-center justify-center ${getActivityColor(activity.type)}`}>
                  {getActivityIcon(activity.type)}
                </div>
                <div className="flex-1 min-w-0">
                  <div className="flex items-center justify-between mb-1">
                    <p className="text-sm font-medium text-gray-800 truncate">
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
          ))
        ) : (
          <div className="text-center py-8 text-gray-500">
            <Activity className="mx-auto mb-2 text-gray-400" size={32} />
            <p>Aucune activité récente</p>
            <p className="text-sm">Commencez à étudier pour voir vos activités ici</p>
          </div>
        )}
      </div>

      {/* Graphique d'activité hebdomadaire */}
      {activityStats?.daily_activities && activityStats.daily_activities.length > 0 && (
        <div className="bg-white border border-gray-200 rounded-lg p-4">
          <h4 className="font-semibold text-gray-800 mb-3">Activité de la Semaine</h4>
          <div className="flex items-end justify-between h-20 gap-1">
            {activityStats.daily_activities.slice(-7).map((day: any, index: number) => {
              const maxCount = Math.max(...activityStats.daily_activities.map((d: any) => d.count));
              const height = maxCount > 0 ? (day.count / maxCount) * 100 : 0;
              
              return (
                <div key={index} className="flex-1 flex flex-col items-center">
                  <div 
                    className="w-full bg-blue-500 rounded-t transition-all duration-300 hover:bg-blue-600"
                    style={{ height: `${height}%` }}
                  ></div>
                  <div className="text-xs text-gray-500 mt-1">
                    {new Date(day.date).toLocaleDateString('fr-FR', { weekday: 'short' })}
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}
    </div>
  );
}; 