'use client';

import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Brain, Lightbulb, Target, TrendingUp, MessageSquare, AlertTriangle, Calendar, Clock, RefreshCw } from 'lucide-react';
import { aiAdvancedAPI, AIRecommendation, DifficultyDetection, AITutoringSession } from '@/api/student/ai-advanced';
import { useAuth  } from '@/hooks/useAuth';

interface AIAdvancedWidgetProps {
  className?: string;
}

export default function AIAdvancedWidget({ className }: AIAdvancedWidgetProps) {
  const { user } = useAuth();
  const [recommendations, setRecommendations] = useState<AIRecommendation[]>([]);
  const [difficulties, setDifficulties] = useState<DifficultyDetection[]>([]);
  const [tutoringSessions, setTutoringSessions] = useState<AITutoringSession[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedTab, setSelectedTab] = useState<'recommendations' | 'difficulties' | 'tutoring'>('recommendations');

  useEffect(() => {
    loadAIData();
  }, []);

  const loadAIData = async () => {
    try {
      setLoading(true);
      setError(null);
      
      const [recommendationsData, difficultiesData, sessionsData] = await Promise.all([
        aiAdvancedAPI.getAIRecommendations().catch(() => []),
        aiAdvancedAPI.getDifficultyDetections().catch(() => []),
        aiAdvancedAPI.getAITutoringSessions().catch(() => [])
      ]);

      // S'assurer que les données sont des tableaux
      setRecommendations(Array.isArray(recommendationsData) ? recommendationsData : []);
      setDifficulties(Array.isArray(difficultiesData) ? difficultiesData : []);
      setTutoringSessions(Array.isArray(sessionsData) ? sessionsData : []);
    } catch (err) {
      setError('Erreur lors du chargement des données IA');
      console.error('Erreur:', err);
      // Initialiser avec des tableaux vides en cas d'erreur
      setRecommendations([]);
      setDifficulties([]);
      setTutoringSessions([]);
    } finally {
      setLoading(false);
    }
  };

  const handleAcceptRecommendation = async (recommendationId: number) => {
    try {
      await aiAdvancedAPI.acceptAIRecommendation(recommendationId);
      await loadAIData(); // Recharger les données
    } catch (err) {
      console.error('Erreur lors de l\'acceptation de la recommandation:', err);
    }
  };

  const handleDismissRecommendation = async (recommendationId: number) => {
    try {
      await aiAdvancedAPI.dismissAIRecommendation(recommendationId);
      await loadAIData(); // Recharger les données
    } catch (err) {
      console.error('Erreur lors du rejet de la recommandation:', err);
    }
  };

  const handleResolveDifficulty = async (difficultyId: number) => {
    try {
      await aiAdvancedAPI.resolveDifficultyDetection(difficultyId);
      await loadAIData(); // Recharger les données
    } catch (err) {
      console.error('Erreur lors de la résolution de la difficulté:', err);
    }
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('fr-FR', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
    });
  };

  const getDifficultyColor = (level: string) => {
    switch (level) {
      case 'high':
        return 'bg-red-100 text-red-800';
      case 'medium':
        return 'bg-yellow-100 text-yellow-800';
      case 'low':
        return 'bg-green-100 text-green-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const getRecommendationTypeIcon = (type: string) => {
    switch (type) {
      case 'content':
        return <Target className="w-4 h-4" />;
      case 'quiz':
        return <Brain className="w-4 h-4" />;
      case 'study_session':
        return <MessageSquare className="w-4 h-4" />;
      default:
        return <Lightbulb className="w-4 h-4" />;
    }
  };

  if (loading) {
    return (
      <Card className={className}>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Brain className="w-5 h-5" />
            IA Avancée
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex items-center justify-center py-8">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
            <span className="ml-2 text-gray-600">Chargement...</span>
          </div>
        </CardContent>
      </Card>
    );
  }

  if (error) {
    return (
      <Card className={className}>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Brain className="w-5 h-5" />
            IA Avancée
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="text-center py-8">
            <AlertTriangle className="w-12 h-12 mx-auto mb-4 text-red-500" />
            <h3 className="text-lg font-semibold text-gray-900 mb-2">Erreur de chargement</h3>
            <p className="text-gray-600 mb-4">{error}</p>
            <Button onClick={loadAIData} variant="outline">
              <RefreshCw className="w-4 h-4 mr-2" />
              Réessayer
            </Button>
          </div>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card className={className}>
      <CardHeader>
        <div className="flex items-center justify-between">
          <CardTitle className="flex items-center gap-2">
            <Brain className="w-5 h-5" />
            IA Avancée
          </CardTitle>
          <div className="flex gap-2">
            <Button
              variant={selectedTab === 'recommendations' ? 'default' : 'outline'}
              size="sm"
              onClick={() => setSelectedTab('recommendations')}
            >
              Recommandations
            </Button>
            <Button
              variant={selectedTab === 'difficulties' ? 'default' : 'outline'}
              size="sm"
              onClick={() => setSelectedTab('difficulties')}
            >
              Difficultés
            </Button>
            <Button
              variant={selectedTab === 'tutoring' ? 'default' : 'outline'}
              size="sm"
              onClick={() => setSelectedTab('tutoring')}
            >
              Tutorat
            </Button>
          </div>
        </div>
      </CardHeader>
      <CardContent>
        <div className="space-y-4 max-h-96 overflow-y-auto">
          {selectedTab === 'recommendations' && (
            <>
              {!Array.isArray(recommendations) || recommendations.length === 0 ? (
                <div className="text-center text-gray-500 py-8">
                  <Lightbulb className="w-12 h-12 mx-auto mb-2 opacity-50" />
                  <p>Aucune recommandation IA disponible</p>
                </div>
              ) : (
                recommendations.map((recommendation) => (
                  <div key={recommendation.id} className="border rounded-lg p-4 hover:shadow-md transition-shadow">
                    <div className="flex items-start justify-between">
                      <div className="flex-1">
                        <div className="flex items-center gap-2 mb-2">
                          {getRecommendationTypeIcon(recommendation.recommendation_type)}
                          <h3 className="font-semibold text-gray-900">{recommendation.title}</h3>
                          <Badge className="bg-blue-100 text-blue-800">
                            {recommendation.recommendation_type}
                          </Badge>
                        </div>
                        <p className="text-sm text-gray-600 mb-2">{recommendation.description}</p>
                        <div className="flex items-center gap-4 text-sm text-gray-500">
                          <div className="flex items-center gap-1">
                            <TrendingUp className="w-4 h-4" />
                            <span>Confiance: {Math.round(recommendation.confidence_score * 100)}%</span>
                          </div>
                          <div className="flex items-center gap-1">
                            <Calendar className="w-4 h-4" />
                            <span>{formatDate(recommendation.created_at)}</span>
                          </div>
                        </div>
                      </div>
                      <div className="flex flex-col gap-2 ml-4">
                        {!recommendation.is_accepted && !recommendation.is_dismissed && (
                          <>
                            <Button
                              size="sm"
                              onClick={() => handleAcceptRecommendation(recommendation.id)}
                            >
                              Accepter
                            </Button>
                            <Button
                              size="sm"
                              variant="outline"
                              onClick={() => handleDismissRecommendation(recommendation.id)}
                            >
                              Rejeter
                            </Button>
                          </>
                        )}
                        {recommendation.is_accepted && (
                          <Badge className="bg-green-100 text-green-800">
                            Acceptée
                          </Badge>
                        )}
                        {recommendation.is_dismissed && (
                          <Badge className="bg-gray-100 text-gray-800">
                            Rejetée
                          </Badge>
                        )}
                      </div>
                    </div>
                  </div>
                ))
              )}
            </>
          )}

          {selectedTab === 'difficulties' && (
            <>
              {!Array.isArray(difficulties) || difficulties.length === 0 ? (
                <div className="text-center text-gray-500 py-8">
                  <Target className="w-12 h-12 mx-auto mb-2 opacity-50" />
                  <p>Aucune difficulté détectée</p>
                </div>
              ) : (
                difficulties.map((difficulty) => (
                  <div key={difficulty.id} className="border rounded-lg p-4 hover:shadow-md transition-shadow">
                    <div className="flex items-start justify-between">
                      <div className="flex-1">
                        <div className="flex items-center gap-2 mb-2">
                          <AlertTriangle className="w-4 h-4 text-yellow-500" />
                          <h3 className="font-semibold text-gray-900">{difficulty.topic}</h3>
                          <Badge className={getDifficultyColor(difficulty.difficulty_level)}>
                            {difficulty.difficulty_level}
                          </Badge>
                        </div>
                        <p className="text-sm text-gray-600 mb-2">
                          Matière: {difficulty.subject}
                        </p>
                        <div className="flex items-center gap-4 text-sm text-gray-500">
                          <div className="flex items-center gap-1">
                            <TrendingUp className="w-4 h-4" />
                            <span>Confiance: {Math.round(difficulty.confidence_score * 100)}%</span>
                          </div>
                          <div className="flex items-center gap-1">
                            <Calendar className="w-4 h-4" />
                            <span>{formatDate(difficulty.detected_at)}</span>
                          </div>
                        </div>
                      </div>
                      {!difficulty.is_resolved && (
                        <Button
                          size="sm"
                          onClick={() => handleResolveDifficulty(difficulty.id)}
                          className="ml-4"
                        >
                          Résoudre
                        </Button>
                      )}
                      {difficulty.is_resolved && (
                        <Badge className="bg-green-100 text-green-800 ml-4">
                          Résolue
                        </Badge>
                      )}
                    </div>
                  </div>
                ))
              )}
            </>
          )}

          {selectedTab === 'tutoring' && (
            <>
              {!Array.isArray(tutoringSessions) || tutoringSessions.length === 0 ? (
                <div className="text-center text-gray-500 py-8">
                  <MessageSquare className="w-12 h-12 mx-auto mb-2 opacity-50" />
                  <p>Aucune session de tutorat IA</p>
                </div>
              ) : (
                tutoringSessions.map((session) => (
                  <div key={session.id} className="border rounded-lg p-4 hover:shadow-md transition-shadow">
                    <div className="flex items-start justify-between">
                      <div className="flex-1">
                        <div className="flex items-center gap-2 mb-2">
                          <MessageSquare className="w-4 h-4 text-blue-500" />
                          <h3 className="font-semibold text-gray-900">
                            Session de tutorat {session.session_type}
                          </h3>
                          <Badge className="bg-blue-100 text-blue-800">
                            {session.status}
                          </Badge>
                        </div>
                        <p className="text-sm text-gray-600 mb-2">
                          {session.subject && `Matière: ${session.subject}`}
                          {session.topic && ` | Sujet: ${session.topic}`}
                        </p>
                        <div className="flex items-center gap-4 text-sm text-gray-500">
                          <div className="flex items-center gap-1">
                            <Calendar className="w-4 h-4" />
                            <span>{formatDate(session.start_time)}</span>
                          </div>
                          {session.duration && (
                            <div className="flex items-center gap-1">
                              <Clock className="w-4 h-4" />
                              <span>{session.duration} min</span>
                            </div>
                          )}
                        </div>
                      </div>
                      <Button size="sm" variant="outline" className="ml-4">
                        Continuer
                      </Button>
                    </div>
                  </div>
                ))
              )}
            </>
          )}
        </div>
      </CardContent>
    </Card>
  );
}
