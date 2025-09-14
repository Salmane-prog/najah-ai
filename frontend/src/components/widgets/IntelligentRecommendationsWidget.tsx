'use client';

import React, { useState, useEffect } from 'react';
import { Lightbulb, Target, TrendingUp, BookOpen, Clock, Star, AlertCircle, CheckCircle, ArrowRight } from 'lucide-react';
import { useAuth  } from '../../hooks/useAuth';

interface Recommendation {
  id: number;
  type: 'study' | 'practice' | 'review' | 'challenge' | 'consolidation';
  title: string;
  description: string;
  priority: 'low' | 'medium' | 'high';
  subject: string;
  estimated_time_minutes: number;
  difficulty: 'easy' | 'medium' | 'hard';
  reason: string;
  impact_score: number;
  created_at: string;
  is_completed?: boolean;
  completed_at?: string;
}

interface SubjectAnalysis {
  subject: string;
  current_level: string;
  target_level: string;
  progress_percentage: number;
  weak_areas: string[];
  strong_areas: string[];
  recommended_focus: string;
  estimated_improvement_time: number;
}

interface LearningAnalytics {
  study_time_trend: 'increasing' | 'decreasing' | 'stable';
  performance_trend: 'improving' | 'declining' | 'stable';
  consistency_score: number;
  best_study_time: string;
  recommended_break_duration: number;
  focus_areas: string[];
}

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export default function IntelligentRecommendationsWidget({ className = '' }: { className?: string }) {
  const [recommendations, setRecommendations] = useState<Recommendation[]>([]);
  const [subjectAnalysis, setSubjectAnalysis] = useState<SubjectAnalysis[]>([]);
  const [learningAnalytics, setLearningAnalytics] = useState<LearningAnalytics | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedRecommendation, setSelectedRecommendation] = useState<Recommendation | null>(null);
  const [showSubjectDetails, setShowSubjectDetails] = useState<string | null>(null);

  const { user, token } = useAuth();

  useEffect(() => {
    if (user?.id && token) {
      loadRecommendations();
    }
  }, [user?.id, token]);

  const loadRecommendations = async () => {
    try {
      setLoading(true);
      setError(null);

      const [reportsRes, subjectsRes] = await Promise.all([
        fetch(`${API_BASE_URL}/api/v1/analytics/student/${user?.id}/reports`, {
          headers: { 'Authorization': `Bearer ${token}` }
        }),
        fetch(`${API_BASE_URL}/api/v1/analytics/student/${user?.id}/subjects`, {
          headers: { 'Authorization': `Bearer ${token}` }
        })
      ]);

      if (reportsRes.ok) {
        const reportsData = await reportsRes.json();
        // Extraire les recommandations des rapports
        const extractedRecommendations = reportsData.recommendations || [];
        setRecommendations(extractedRecommendations);
      }

      if (subjectsRes.ok) {
        const subjectsData = await subjectsRes.json();
        setSubjectAnalysis(subjectsData.subjects || []);
      }

      // Simuler les analytics d'apprentissage (à remplacer par l'endpoint réel)
      setLearningAnalytics({
        study_time_trend: 'increasing',
        performance_trend: 'improving',
        consistency_score: 85,
        best_study_time: '14:00-16:00',
        recommended_break_duration: 15,
        focus_areas: ['Mathématiques', 'Français', 'Sciences']
      });

    } catch (err) {
      console.error('Erreur lors du chargement des recommandations:', err);
      setError('Erreur lors du chargement des recommandations');
    } finally {
      setLoading(false);
    }
  };

  const markRecommendationCompleted = async (recommendationId: number) => {
    try {
      setError(null);

      // Mettre à jour l'état local
      setRecommendations(prev => 
        prev.map(rec => 
          rec.id === recommendationId 
            ? { ...rec, is_completed: true, completed_at: new Date().toISOString() }
            : rec
        )
      );

      // Ici, vous pourriez appeler un endpoint pour marquer la recommandation comme terminée
      // await fetch(`${API_BASE_URL}/api/v1/recommendations/${recommendationId}/complete`, {
      //   method: 'POST',
      //   headers: { 'Authorization': `Bearer ${token}` }
      // });

    } catch (err) {
      console.error('Erreur lors de la mise à jour:', err);
      setError('Erreur lors de la mise à jour');
    }
  };

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'high': return 'text-red-600 bg-red-100 border-red-200';
      case 'medium': return 'text-yellow-600 bg-yellow-100 border-yellow-200';
      case 'low': return 'text-green-600 bg-green-100 border-green-200';
      default: return 'text-gray-600 bg-gray-100 border-gray-200';
    }
  };

  const getTypeIcon = (type: string) => {
    switch (type) {
      case 'study': return '📚';
      case 'practice': return '✏️';
      case 'review': return '🔄';
      case 'challenge': return '🚀';
      case 'consolidation': return '🎯';
      default: return '💡';
    }
  };

  const getDifficultyColor = (difficulty: string) => {
    switch (difficulty) {
      case 'easy': return 'text-green-600 bg-green-100';
      case 'medium': return 'text-yellow-600 bg-yellow-100';
      case 'hard': return 'text-red-600 bg-red-100';
      default: return 'text-gray-600 bg-gray-100';
    }
  };

  const getTrendIcon = (trend: string) => {
    switch (trend) {
      case 'increasing':
      case 'improving':
        return <TrendingUp className="w-4 h-4 text-green-600" />;
      case 'decreasing':
      case 'declining':
        return <TrendingUp className="w-4 h-4 text-red-600 transform rotate-180" />;
      default:
        return <TrendingUp className="w-4 h-4 text-gray-600" />;
    }
  };

  if (loading) {
    return (
      <div className={`bg-white rounded-lg shadow-md p-6 ${className}`}>
        <div className="animate-pulse">
          <div className="h-6 bg-gray-200 rounded w-1/3 mb-4"></div>
          <div className="h-4 bg-gray-200 rounded w-1/2 mb-2"></div>
          <div className="h-4 bg-gray-200 rounded w-3/4"></div>
        </div>
      </div>
    );
  }

  return (
    <div className={`bg-white rounded-lg shadow-md p-6 ${className}`}>
      <div className="flex items-center justify-between mb-6">
        <div>
          <h2 className="text-xl font-semibold text-gray-800 flex items-center">
            <Lightbulb className="w-6 h-6 mr-2 text-yellow-500" />
            Recommandations Intelligentes
          </h2>
          <p className="text-gray-600 mt-1">
            Conseils personnalisés basés sur vos performances et objectifs
          </p>
        </div>
        <div className="text-right">
          <div className="text-2xl font-bold text-yellow-600">
            {recommendations.filter(r => !r.is_completed).length}
          </div>
          <div className="text-sm text-gray-600">Recommandations actives</div>
        </div>
      </div>

      {error && (
        <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg">
          <div className="flex items-center text-red-800">
            <AlertCircle className="w-5 h-5 mr-2" />
            {error}
          </div>
        </div>
      )}

      {/* Analytics d'apprentissage */}
      {learningAnalytics && (
        <div className="mb-6 p-4 bg-gradient-to-r from-blue-50 to-purple-50 rounded-lg border border-blue-200">
          <h3 className="text-lg font-semibold text-gray-800 mb-3 flex items-center">
            <TrendingUp className="w-5 h-5 mr-2 text-blue-600" />
            Analyse de vos habitudes d'apprentissage
          </h3>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="text-center">
              <div className="text-2xl font-bold text-blue-600 mb-1">
                {learningAnalytics.consistency_score}%
              </div>
              <div className="text-sm text-gray-600">Score de cohérence</div>
            </div>
            
            <div className="text-center">
              <div className="flex items-center justify-center mb-1">
                {getTrendIcon(learningAnalytics.study_time_trend)}
              </div>
              <div className="text-sm text-gray-600">Temps d'étude</div>
            </div>
            
            <div className="text-center">
              <div className="flex items-center justify-center mb-1">
                {getTrendIcon(learningAnalytics.performance_trend)}
              </div>
              <div className="text-sm text-gray-600">Performance</div>
            </div>
          </div>
          
          <div className="mt-3 text-sm text-gray-600">
            <div className="flex items-center justify-between">
              <span>Meilleur moment pour étudier : <strong>{learningAnalytics.best_study_time}</strong></span>
              <span>Pause recommandée : <strong>{learningAnalytics.recommended_break_duration} min</strong></span>
            </div>
          </div>
        </div>
      )}

      {/* Analyse par matière */}
      {subjectAnalysis.length > 0 && (
        <div className="mb-6">
          <h3 className="text-lg font-semibold text-gray-800 mb-3 flex items-center">
            <BookOpen className="w-5 h-5 mr-2 text-green-600" />
            Analyse par matière
          </h3>
          
          <div className="space-y-3">
            {subjectAnalysis.slice(0, 3).map((subject, index) => (
              <div key={index} className="border border-gray-200 rounded-lg p-4 hover:bg-gray-50">
                <div className="flex items-center justify-between">
                  <div className="flex-1">
                    <h4 className="font-medium text-gray-800">{subject.subject}</h4>
                    <div className="flex items-center space-x-4 mt-2 text-sm text-gray-500">
                      <span>Niveau actuel : <strong>{subject.current_level}</strong></span>
                      <span>Objectif : <strong>{subject.target_level}</strong></span>
                      <span className="flex items-center">
                        <TrendingUp className="w-4 h-4 mr-1" />
                        {subject.progress_percentage}%
                      </span>
                    </div>
                    
                    {subject.weak_areas.length > 0 && (
                      <div className="mt-2">
                        <span className="text-xs text-red-600 font-medium">Points à améliorer : </span>
                        <span className="text-xs text-gray-600">{subject.weak_areas.join(', ')}</span>
                      </div>
                    )}
                  </div>
                  
                  <button
                    onClick={() => setShowSubjectDetails(showSubjectDetails === subject.subject ? null : subject.subject)}
                    className="text-blue-600 hover:text-blue-800 text-sm"
                  >
                    {showSubjectDetails === subject.subject ? 'Masquer' : 'Détails'}
                  </button>
                </div>
                
                {showSubjectDetails === subject.subject && (
                  <div className="mt-3 pt-3 border-t border-gray-200">
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
                      <div>
                        <h5 className="font-medium text-gray-700 mb-2">Points forts :</h5>
                        <div className="space-y-1">
                          {subject.strong_areas.map((area, idx) => (
                            <div key={idx} className="flex items-center text-green-600">
                              <CheckCircle className="w-4 h-4 mr-2" />
                              {area}
                            </div>
                          ))}
                        </div>
                      </div>
                      
                      <div>
                        <h5 className="font-medium text-gray-700 mb-2">Focus recommandé :</h5>
                        <p className="text-gray-600">{subject.recommended_focus}</p>
                        <p className="text-gray-500 text-xs mt-1">
                          Temps estimé : {subject.estimated_improvement_time} heures
                        </p>
                      </div>
                    </div>
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Recommandations */}
      {recommendations.length > 0 && (
        <div>
          <h3 className="text-lg font-semibold text-gray-800 mb-3 flex items-center">
            <Target className="w-5 h-5 mr-2 text-orange-500" />
            Recommandations personnalisées
          </h3>
          
          <div className="space-y-3">
            {recommendations
              .filter(rec => !rec.is_completed)
              .sort((a, b) => {
                const priorityOrder = { high: 3, medium: 2, low: 1 };
                return priorityOrder[b.priority] - priorityOrder[a.priority];
              })
              .slice(0, 5)
              .map((recommendation) => (
                <div key={recommendation.id} className="border border-gray-200 rounded-lg p-4 hover:bg-gray-50">
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <div className="flex items-center space-x-3 mb-2">
                        <span className="text-2xl">{getTypeIcon(recommendation.type)}</span>
                        <div>
                          <h4 className="font-medium text-gray-800">{recommendation.title}</h4>
                          <p className="text-sm text-gray-600">{recommendation.description}</p>
                        </div>
                      </div>
                      
                      <div className="flex items-center space-x-4 text-sm text-gray-500 mb-2">
                        <span className={`px-2 py-1 rounded-full text-xs font-medium ${getPriorityColor(recommendation.priority)}`}>
                          {recommendation.priority}
                        </span>
                        <span className="flex items-center">
                          <BookOpen className="w-4 h-4 mr-1" />
                          {recommendation.subject}
                        </span>
                        <span className="flex items-center">
                          <Clock className="w-4 h-4 mr-1" />
                          {recommendation.estimated_time_minutes} min
                        </span>
                        <span className={`px-2 py-1 rounded-full text-xs font-medium ${getDifficultyColor(recommendation.difficulty)}`}>
                          {recommendation.difficulty}
                        </span>
                      </div>
                      
                      <div className="text-sm text-gray-600">
                        <strong>Pourquoi :</strong> {recommendation.reason}
                      </div>
                      
                      <div className="mt-2 flex items-center space-x-2">
                        <span className="text-xs text-gray-500">Impact estimé :</span>
                        <div className="flex items-center space-x-1">
                          {[...Array(5)].map((_, i) => (
                            <Star 
                              key={i} 
                              className={`w-3 h-3 ${
                                i < recommendation.impact_score 
                                  ? 'text-yellow-500 fill-current' 
                                  : 'text-gray-300'
                              }`} 
                            />
                          ))}
                        </div>
                      </div>
                    </div>
                    
                    <div className="flex items-center space-x-2 ml-4">
                      <button
                        onClick={() => markRecommendationCompleted(recommendation.id)}
                        className="px-3 py-1 bg-green-600 text-white text-sm rounded-lg hover:bg-green-700 flex items-center"
                      >
                        <CheckCircle className="w-4 h-4 mr-1" />
                        Terminer
                      </button>
                    </div>
                  </div>
                </div>
              ))}
          </div>
          
          {recommendations.filter(r => !r.is_completed).length > 5 && (
            <div className="text-center mt-4">
              <button className="text-blue-600 hover:text-blue-800 text-sm font-medium">
                Voir toutes les recommandations ({recommendations.filter(r => !r.is_completed).length})
              </button>
            </div>
          )}
        </div>
      )}

      {recommendations.length === 0 && subjectAnalysis.length === 0 && (
        <div className="text-center py-8">
          <Lightbulb className="w-16 h-16 text-gray-300 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-gray-600 mb-2">
            Aucune recommandation disponible
          </h3>
          <p className="text-gray-500">
            Complétez des évaluations pour recevoir des recommandations personnalisées
          </p>
        </div>
      )}
    </div>
  );
}







