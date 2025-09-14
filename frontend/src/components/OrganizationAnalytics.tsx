'use client';

import React, { useState, useEffect } from 'react';
import { 
  TrendingUp, 
  Clock, 
  Target, 
  Award, 
  AlertTriangle,
  Calendar,
  BarChart3,
  Lightbulb
} from 'lucide-react';
import { organizationAdvancedAPI, ProductivityAnalytics, PriorityTask, Achievement } from '../api/student/organization-advanced';

interface OrganizationAnalyticsProps {
  className?: string;
}

export default function OrganizationAnalytics({ className = '' }: OrganizationAnalyticsProps) {
  const [analytics, setAnalytics] = useState<ProductivityAnalytics | null>(null);
  const [recommendations, setRecommendations] = useState<PriorityTask[]>([]);
  const [achievements, setAchievements] = useState<Achievement[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadAnalytics();
  }, []);

  const loadAnalytics = async () => {
    try {
      setLoading(true);
      setError(null);

      // Temporairement désactivé - endpoints non disponibles
      console.log('[ANALYTICS] Endpoints temporairement désactivés');
      
      // Données mockées pour l'instant
      setAnalytics({
        study_time_hours: 12.5,
        avg_productivity: 8.2,
        homework_completion_rate: 85,
        sessions_count: 15
      });
      
      setRecommendations([]);
      setAchievements([]);

    } catch (err) {
      console.error('Erreur lors du chargement des analytics:', err);
      setError('Impossible de charger les données d\'analytics');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className={`grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 ${className}`}>
        {[...Array(6)].map((_, i) => (
          <div key={i} className="bg-white rounded-lg p-6 shadow-sm animate-pulse">
            <div className="h-4 bg-gray-200 rounded mb-4"></div>
            <div className="h-8 bg-gray-200 rounded mb-2"></div>
            <div className="h-3 bg-gray-200 rounded"></div>
          </div>
        ))}
      </div>
    );
  }

  if (error) {
    return (
      <div className={`bg-red-50 border border-red-200 rounded-lg p-4 ${className}`}>
        <div className="flex items-center text-red-800">
          <AlertTriangle className="w-5 h-5 mr-2" />
          <span>{error}</span>
        </div>
      </div>
    );
  }

  return (
    <div className={`space-y-6 ${className}`}>
      {/* Analytics Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="bg-white rounded-lg p-6 shadow-sm border">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Temps d'étude</p>
              <p className="text-2xl font-bold text-blue-600">
                {analytics?.study_time_hours.toFixed(1)}h
              </p>
            </div>
            <Clock className="w-8 h-8 text-blue-500" />
          </div>
        </div>

        <div className="bg-white rounded-lg p-6 shadow-sm border">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Productivité</p>
              <p className="text-2xl font-bold text-green-600">
                {analytics?.avg_productivity.toFixed(1)}/10
              </p>
            </div>
            <TrendingUp className="w-8 h-8 text-green-500" />
          </div>
        </div>

        <div className="bg-white rounded-lg p-6 shadow-sm border">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Devoirs terminés</p>
              <p className="text-2xl font-bold text-purple-600">
                {analytics?.homework_completion_rate.toFixed(0)}%
              </p>
            </div>
            <Target className="w-8 h-8 text-purple-500" />
          </div>
        </div>

        <div className="bg-white rounded-lg p-6 shadow-sm border">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Sessions</p>
              <p className="text-2xl font-bold text-orange-600">
                {analytics?.sessions_count}
              </p>
            </div>
            <BarChart3 className="w-8 h-8 text-orange-500" />
          </div>
        </div>
      </div>

      {/* Recommandations et Achievements */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Recommandations */}
        <div className="bg-white rounded-lg p-6 shadow-sm border">
          <div className="flex items-center mb-4">
            <Lightbulb className="w-5 h-5 text-yellow-500 mr-2" />
            <h3 className="text-lg font-semibold text-gray-900">Recommandations IA</h3>
          </div>
          
          {recommendations.length > 0 ? (
            <div className="space-y-3">
              {recommendations.slice(0, 3).map((task, index) => (
                <div key={index} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                  <div className="flex-1">
                    <p className="font-medium text-gray-900">{task.title}</p>
                    <p className="text-sm text-gray-600">
                      {task.days_left} jour(s) restant(s)
                    </p>
                  </div>
                  <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                    task.priority === 'critical' 
                      ? 'bg-red-100 text-red-800' 
                      : 'bg-yellow-100 text-yellow-800'
                  }`}>
                    {task.priority === 'critical' ? 'Urgent' : 'Important'}
                  </span>
                </div>
              ))}
            </div>
          ) : (
            <p className="text-gray-500 text-center py-4">
              Aucune tâche urgente pour le moment !
            </p>
          )}
        </div>

        {/* Achievements */}
        <div className="bg-white rounded-lg p-6 shadow-sm border">
          <div className="flex items-center mb-4">
            <Award className="w-5 h-5 text-yellow-500 mr-2" />
            <h3 className="text-lg font-semibold text-gray-900">Achievements</h3>
          </div>
          
          {achievements.length > 0 ? (
            <div className="space-y-3">
              {achievements.slice(0, 3).map((achievement, index) => (
                <div key={index} className="flex items-center p-3 bg-gray-50 rounded-lg">
                  <span className="text-2xl mr-3">{achievement.icon}</span>
                  <div className="flex-1">
                    <p className="font-medium text-gray-900">{achievement.title}</p>
                    <p className="text-sm text-gray-600">{achievement.description}</p>
                    {achievement.unlocked && (
                      <div className="mt-2">
                        <div className="w-full bg-gray-200 rounded-full h-2">
                          <div 
                            className="bg-green-500 h-2 rounded-full" 
                            style={{ width: `${achievement.progress}%` }}
                          ></div>
                        </div>
                        <p className="text-xs text-gray-500 mt-1">
                          {achievement.progress.toFixed(0)}% complété
                        </p>
                      </div>
                    )}
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <p className="text-gray-500 text-center py-4">
              Commencez à étudier pour débloquer des achievements !
            </p>
          )}
        </div>
      </div>
    </div>
  );
} 