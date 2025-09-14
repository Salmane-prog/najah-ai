'use client';

import React, { useState, useEffect } from 'react';
import { Lightbulb, Target, TrendingUp, BookOpen, Clock, Star, AlertCircle, CheckCircle, ArrowRight, Brain, RefreshCw } from 'lucide-react';
import { useAuth } from '../../hooks/useAuth';

interface AIRecommendation {
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
}

interface LearningAnalytics {
  study_time_recommendation: number;
  break_recommendation: number;
  recommended_break_duration: number;
  focus_areas: string[];
}

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export default function AIRecommendationsWidget({ className = '' }: { className?: string }) {
  const [recommendations, setRecommendations] = useState<AIRecommendation[]>([]);
  const [subjectAnalysis, setSubjectAnalysis] = useState<SubjectAnalysis[]>([]);
  const [learningAnalytics, setLearningAnalytics] = useState<LearningAnalytics | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedRecommendation, setSelectedRecommendation] = useState<AIRecommendation | null>(null);
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

      console.log('[AIRecommendationsWidget] 🔐 Chargement des recommandations IA pour l\'utilisateur:', user?.id);

      // Appels parallèles pour récupérer toutes les données
      const [recommendationsRes, analyticsRes] = await Promise.all([
        fetch(`${API_BASE_URL}/api/v1/ai-recommendations/student/${user?.id}`, {
          headers: { 'Authorization': `Bearer ${token}` }
        }),
        fetch(`${API_BASE_URL}/api/v1/learning-analytics/student/${user?.id}`, {
          headers: { 'Authorization': `Bearer ${token}` }
        })
      ]);

      console.log('[AIRecommendationsWidget] 📊 Réponses API:', { 
        recommendationsStatus: recommendationsRes.status,
        analyticsStatus: analyticsRes.status
      });

      if (recommendationsRes.ok) {
        const recommendationsData = await recommendationsRes.json();
        console.log('[AIRecommendationsWidget] ✅ Recommandations récupérées:', recommendationsData);
        setRecommendations(recommendationsData.recommendations || recommendationsData || []);
      } else {
        console.log('[AIRecommendationsWidget] ❌ Erreur recommandations:', recommendationsRes.status, recommendationsRes.statusText);
        // En cas d'erreur, utiliser des données simulées pour le développement
        setRecommendations(generateMockRecommendations());
      }

      if (analyticsRes.ok) {
        const analyticsData = await analyticsRes.json();
        console.log('[AIRecommendationsWidget] ✅ Analytics récupérées:', analyticsData);
        setLearningAnalytics(analyticsData);
        setSubjectAnalysis(analyticsData.subject_analysis || []);
      } else {
        console.log('[AIRecommendationsWidget] ❌ Erreur analytics:', analyticsRes.status, analyticsRes.statusText);
        // En cas d'erreur, utiliser des données simulées
        setLearningAnalytics(generateMockAnalytics());
        setSubjectAnalysis(generateMockSubjectAnalysis());
      }
    } catch (err) {
      console.error('[AIRecommendationsWidget] 💥 Erreur lors du chargement:', err);
      setError('Erreur lors du chargement des recommandations IA');
      // Utiliser des données simulées en cas d'erreur
      setRecommendations(generateMockRecommendations());
      setLearningAnalytics(generateMockAnalytics());
      setSubjectAnalysis(generateMockSubjectAnalysis());
    } finally {
      setLoading(false);
    }
  };

  // Fonction de rechargement forcé
  const forceRefresh = () => {
    console.log('[AIRecommendationsWidget] 🔄 Rechargement forcé des recommandations IA');
    setError(null);
    loadRecommendations();
  };

  // Génération de données simulées pour le développement
  const generateMockRecommendations = (): AIRecommendation[] => [
    {
      id: 1,
      type: 'practice',
      title: 'Quiz de consolidation en Mathématiques',
      description: 'Renforcez vos compétences en algèbre avec des exercices ciblés',
      priority: 'high',
      subject: 'Mathématiques',
      estimated_time_minutes: 30,
      difficulty: 'medium',
      reason: 'Basé sur vos performances récentes',
      impact_score: 85,
      created_at: new Date().toISOString(),
      is_completed: false
    },
    {
      id: 2,
      type: 'review',
      title: 'Révision des concepts de Français',
      description: 'Revisitez les règles de grammaire pour améliorer votre score',
      priority: 'medium',
      subject: 'Français',
      estimated_time_minutes: 45,
      difficulty: 'easy',
      reason: 'Identifié comme zone d\'amélioration',
      impact_score: 72,
      created_at: new Date().toISOString(),
      is_completed: false
    },
    {
      id: 3,
      type: 'challenge',
      title: 'Défi avancé en Sciences',
      description: 'Testez vos connaissances avec des problèmes complexes',
      priority: 'low',
      subject: 'Sciences',
      estimated_time_minutes: 60,
      difficulty: 'hard',
      reason: 'Pour développer votre pensée critique',
      impact_score: 95,
      created_at: new Date().toISOString(),
      is_completed: false
    }
  ];

  const generateMockAnalytics = (): LearningAnalytics => ({
    study_time_recommendation: 120,
    break_recommendation: 15,
    recommended_break_duration: 5,
    focus_areas: ['Mathématiques', 'Français', 'Sciences']
  });

  const generateMockSubjectAnalysis = (): SubjectAnalysis[] => [
    {
      subject: 'Mathématiques',
      current_level: 'Intermédiaire',
      target_level: 'Avancé',
      progress_percentage: 65,
      weak_areas: ['Algèbre', 'Géométrie'],
      strong_areas: ['Arithmétique', 'Statistiques']
    },
    {
      subject: 'Français',
      current_level: 'Débutant',
      target_level: 'Intermédiaire',
      progress_percentage: 45,
      weak_areas: ['Grammaire', 'Conjugaison'],
      strong_areas: ['Compréhension', 'Vocabulaire']
    }
  ];

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'high':
        return 'bg-red-100 text-red-800 border-red-200';
      case 'medium':
        return 'bg-yellow-100 text-yellow-800 border-yellow-200';
      case 'low':
        return 'bg-green-100 text-green-800 border-green-200';
      default:
        return 'bg-gray-100 text-gray-800 border-gray-200';
    }
  };

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

  const getTypeIcon = (type: string) => {
    switch (type) {
      case 'study':
        return <BookOpen className="w-4 h-4" />;
      case 'practice':
        return <Target className="w-4 h-4" />;
      case 'review':
        return <RefreshCw className="w-4 h-4" />;
      case 'challenge':
        return <Star className="w-4 h-4" />;
      case 'consolidation':
        return <TrendingUp className="w-4 h-4" />;
      default:
        return <Lightbulb className="w-4 h-4" />;
    }
  };

  const getTypeLabel = (type: string) => {
    switch (type) {
      case 'study':
        return 'Étude';
      case 'practice':
        return 'Pratique';
      case 'review':
        return 'Révision';
      case 'challenge':
        return 'Défi';
      case 'consolidation':
        return 'Consolidation';
      default:
        return 'Recommandation';
    }
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('fr-FR', {
      day: 'numeric',
      month: 'short',
      year: 'numeric'
    });
  };

  const handleAcceptRecommendation = async (recommendation: AIRecommendation) => {
    try {
      console.log('[AIRecommendationsWidget] ✅ Acceptation de la recommandation:', recommendation.id);
      
      // Marquer comme acceptée localement
      setRecommendations(prev => 
        prev.map(rec => 
          rec.id === recommendation.id 
            ? { ...rec, is_completed: true, completed_at: new Date().toISOString() }
            : rec
        )
      );

      // Appel API pour marquer comme acceptée
      const response = await fetch(`${API_BASE_URL}/api/v1/ai-recommendations/${recommendation.id}/accept`, {
        method: 'POST',
        headers: { 
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });

      if (response.ok) {
        console.log('[AIRecommendationsWidget] ✅ Recommandation acceptée avec succès');
      } else {
        console.log('[AIRecommendationsWidget] ❌ Erreur lors de l\'acceptation:', response.status);
      }
    } catch (err) {
      console.error('[AIRecommendationsWidget] 💥 Erreur lors de l\'acceptation:', err);
    }
  };

  const handleViewAnalytics = () => {
    // Rediriger vers la page Analytics Avancées
    window.location.href = '/dashboard/student/advanced-analytics';
  };

  if (loading) {
    return (
      <div className={`card-unified ${className}`}>
        <div className="card-unified-header">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 bg-gradient-to-br from-purple-500 to-blue-600 rounded-lg flex items-center justify-center">
              <Brain className="w-5 h-5 text-white" />
            </div>
            <h3 className="text-lg font-semibold">Recommandations IA</h3>
          </div>
        </div>
        <div className="card-unified-body">
          <div className="flex items-center justify-center py-8">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-purple-600"></div>
            <span className="ml-3 text-muted">Chargement des recommandations...</span>
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className={`card-unified ${className}`}>
        <div className="card-unified-header">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 bg-gradient-to-br from-purple-500 to-blue-600 rounded-lg flex items-center justify-center">
              <Brain className="w-5 h-5 text-white" />
            </div>
            <h3 className="text-lg font-semibold">Recommandations IA</h3>
          </div>
        </div>
        <div className="card-unified-body">
          <div className="flex items-center justify-center py-8 text-danger">
            <AlertCircle className="w-5 h-5 mr-2" />
            {error}
          </div>
          <div className="flex justify-center mt-4">
            <button
              onClick={forceRefresh}
              className="btn-unified btn-unified-primary flex items-center gap-2"
            >
              <RefreshCw className="w-4 h-4" />
              Réessayer
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className={`space-y-6 ${className}`}>
      {/* En-tête du widget */}
      <div className="card-unified">
        <div className="card-unified-header">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="w-8 h-8 bg-gradient-to-br from-purple-500 to-blue-600 rounded-lg flex items-center justify-center">
                <Brain className="w-5 h-5 text-white" />
              </div>
              <h3 className="text-lg font-semibold">Recommandations IA</h3>
            </div>
            <div className="flex items-center gap-2">
              <button
                onClick={handleViewAnalytics}
                className="btn-unified btn-unified-secondary flex items-center gap-2"
                title="Voir les analytics avancées"
              >
                <TrendingUp className="w-4 h-4" />
                Analytics
              </button>
              <button
                onClick={forceRefresh}
                className="btn-unified btn-unified-secondary flex items-center gap-2"
                title="Actualiser les recommandations"
              >
                <RefreshCw className="w-4 h-4" />
                Actualiser
              </button>
            </div>
          </div>
        </div>

        <div className="card-unified-body max-h-96 overflow-hidden">
          {/* Statistiques rapides */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
            <div className="text-center p-4 bg-purple-50 rounded-lg border border-purple-200">
              <div className="text-2xl font-bold text-purple-600">
                {recommendations.filter(r => !r.is_completed).length}
              </div>
              <div className="text-sm text-purple-600">Actives</div>
            </div>
            <div className="text-center p-4 bg-blue-50 rounded-lg border border-blue-200">
              <div className="text-2xl font-bold text-blue-600">
                {recommendations.filter(r => r.is_completed).length}
              </div>
              <div className="text-sm text-blue-600">Terminées</div>
            </div>
            <div className="text-center p-4 bg-green-50 rounded-lg border border-green-200">
              <div className="text-2xl font-bold text-green-600">
                {learningAnalytics?.study_time_recommendation || 0} min
              </div>
              <div className="text-sm text-green-600">Temps recommandé</div>
            </div>
          </div>

          {/* Liste des recommandations */}
          {recommendations.length > 0 ? (
            <div className="space-y-4 max-h-64 overflow-y-auto pr-2">
              {recommendations
                .filter(rec => !rec.is_completed)
                .slice(0, 5)
                .map((recommendation) => (
                  <div
                    key={recommendation.id}
                    className="p-4 bg-gradient-to-r from-blue-50 to-purple-50 rounded-lg border border-blue-200 hover:shadow-md transition-all duration-300"
                  >
                    <div className="flex items-start justify-between mb-3">
                      <div className="flex items-center gap-3">
                        <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-purple-600 rounded-lg flex items-center justify-center">
                          {getTypeIcon(recommendation.type)}
                        </div>
                        <div>
                          <h4 className="font-semibold text-gray-800">{recommendation.title}</h4>
                          <p className="text-sm text-gray-600">{recommendation.description}</p>
                        </div>
                      </div>
                      <div className="flex items-center gap-2">
                        <span className={`px-2 py-1 rounded-full text-xs font-medium border ${getPriorityColor(recommendation.priority)}`}>
                          {recommendation.priority === 'high' ? 'Élevée' : recommendation.priority === 'medium' ? 'Moyenne' : 'Faible'}
                        </span>
                        <span className={`px-2 py-1 rounded-full text-xs font-medium ${getDifficultyColor(recommendation.difficulty)}`}>
                          {recommendation.difficulty === 'easy' ? 'Facile' : recommendation.difficulty === 'medium' ? 'Moyen' : 'Difficile'}
                        </span>
                      </div>
                    </div>

                    <div className="flex items-center justify-between text-sm text-gray-600 mb-3">
                      <div className="flex items-center gap-4">
                        <span className="flex items-center gap-1">
                          <BookOpen className="w-4 h-4" />
                          {recommendation.subject}
                        </span>
                        <span className="flex items-center gap-1">
                          <Clock className="w-4 h-4" />
                          {recommendation.estimated_time_minutes} min
                        </span>
                        <span className="flex items-center gap-1">
                          <Star className="w-4 h-4" />
                          Impact: {recommendation.impact_score}%
                        </span>
                      </div>
                      <span className="text-xs text-gray-500">
                        {formatDate(recommendation.created_at)}
                      </span>
                    </div>

                    <div className="flex items-center justify-between">
                      <p className="text-xs text-gray-600 italic">
                        Raison: {recommendation.reason}
                      </p>
                      <button
                        onClick={() => handleAcceptRecommendation(recommendation)}
                        className="btn-unified btn-unified-primary flex items-center gap-2"
                      >
                        <CheckCircle className="w-4 h-4" />
                        Accepter
                      </button>
                    </div>
                  </div>
                ))}
            </div>
          ) : (
            <div className="text-center py-8">
              <Lightbulb className="w-16 h-16 text-gray-300 mx-auto mb-4" />
              <p className="text-lg font-semibold text-gray-600 mb-2">Aucune recommandation disponible</p>
              <p className="text-base text-gray-400">L'IA analysera vos performances et vous proposera des recommandations personnalisées.</p>
            </div>
          )}

          {/* Lien vers Analytics Avancées */}
          {recommendations.length > 0 && (
            <div className="mt-6 text-center">
              <button
                onClick={handleViewAnalytics}
                className="btn-unified btn-unified-secondary flex items-center gap-2 mx-auto"
              >
                <TrendingUp className="w-4 h-4" />
                Voir toutes les recommandations et analytics
                <ArrowRight className="w-4 h-4" />
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
