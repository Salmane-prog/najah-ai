'use client';

import React, { useEffect, useState } from 'react';
import { useAuth } from '@/hooks/useAuthSimple';
import { GapAnalysisService, GapAnalysis } from '@/services/gapAnalysisService';
import { Brain, TrendingUp, Target, Clock, Lightbulb, BarChart3, Zap, Activity, BookOpen, Users, Award } from 'lucide-react';

export default function AIAdvancedPage() {
  const { user, token } = useAuth();
  const [gapAnalysis, setGapAnalysis] = useState<GapAnalysis | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedSubject, setSelectedSubject] = useState('Français');
  const [aiInsights, setAiInsights] = useState<any[]>([]);
  const [selectedInsight, setSelectedInsight] = useState<number | null>(null);

  useEffect(() => {
    if (user && token) {
      loadAIInsights();
    }
  }, [user, token, selectedSubject]);

  const loadAIInsights = async () => {
    if (!user || !token) return;

    setLoading(true);
    setError(null);

    try {
      console.log('🧠 [AI ADVANCED PAGE] Chargement des insights IA...');
      
      // Charger l'analyse des lacunes
      const analysis = await GapAnalysisService.analyzeGaps(token, user.id, selectedSubject);
      setGapAnalysis(analysis);
      
      // Générer des insights IA basés sur l'analyse
      const insights = generateAIInsights(analysis);
      setAiInsights(insights);
      
      console.log('✅ [AI ADVANCED PAGE] Insights générés:', insights);
    } catch (error) {
      console.error('❌ [AI ADVANCED PAGE] Erreur:', error);
      setError('Erreur lors du chargement des insights IA');
    } finally {
      setLoading(false);
    }
  };

  const generateAIInsights = (analysis: GapAnalysis): any[] => {
    const insights = [];

    // Insight 1: Analyse des tendances de performance
    if (analysis.overall_score < 70) {
      insights.push({
        id: 1,
        type: 'trend',
        title: '📉 Tendance de Performance',
        description: 'Votre performance globale montre une tendance à la baisse',
        details: `Avec un score de ${analysis.overall_score}%, vous êtes en dessous du seuil de réussite de 70%.`,
        recommendations: [
          'Concentrez-vous sur les domaines identifiés comme faibles',
          'Pratiquez quotidiennement avec des exercices ciblés',
          'Utilisez les ressources de remédiation proposées'
        ],
        priority: 'high',
        icon: <TrendingUp className="w-6 h-6 text-red-500" />
      });
    } else {
      insights.push({
        id: 1,
        type: 'trend',
        title: '📈 Tendance de Performance',
        description: 'Votre performance globale est stable et positive',
        details: `Avec un score de ${analysis.overall_score}%, vous maintenez un bon niveau.`,
        recommendations: [
          'Continuez à pratiquer pour maintenir votre niveau',
          'Tentez des exercices plus difficiles pour progresser',
          'Partagez vos connaissances avec d\'autres étudiants'
        ],
        priority: 'low',
        icon: <TrendingUp className="w-6 h-6 text-green-500" />
      });
    }

    // Insight 2: Analyse des domaines faibles
    if (analysis.weak_areas.length > 0) {
      const criticalAreas = analysis.weak_areas.filter(area => area.success_rate < 50);
      const moderateAreas = analysis.weak_areas.filter(area => area.success_rate >= 50 && area.success_rate < 70);
      
      insights.push({
        id: 2,
        type: 'weakness',
        title: '🎯 Analyse des Domaines Faibles',
        description: `Identifié ${analysis.weak_areas.length} domaines nécessitant une attention particulière`,
        details: `${criticalAreas.length} domaines critiques (< 50%) et ${moderateAreas.length} domaines modérés (50-70%)`,
        recommendations: [
          'Priorisez les domaines critiques en premier',
          'Utilisez des exercices de difficulté progressive',
          'Pratiquez régulièrement pour consolider les acquis'
        ],
        priority: criticalAreas.length > 0 ? 'high' : 'medium',
        icon: <Target className="w-6 h-6 text-orange-500" />
      });
    }

    // Insight 3: Recommandations de temps d'étude
    insights.push({
      id: 3,
      type: 'time',
      title: '⏰ Optimisation du Temps d\'Étude',
      description: 'Recommandations personnalisées pour maximiser votre efficacité',
      details: `Temps estimé pour combler vos lacunes: ${Math.round(analysis.estimated_study_time / 60)}h ${analysis.estimated_study_time % 60 > 0 ? `${analysis.estimated_study_time % 60}min` : ''}`,
      recommendations: [
        'Étudiez par sessions de 25-30 minutes avec des pauses',
        'Planifiez vos sessions d\'étude à l\'avance',
        'Utilisez la technique Pomodoro pour rester concentré'
      ],
      priority: 'medium',
      icon: <Clock className="w-6 h-6 text-blue-500" />
    });

    // Insight 4: Stratégies d'apprentissage adaptatives
    insights.push({
      id: 4,
      type: 'strategy',
      title: '🧠 Stratégies d\'Apprentissage Adaptatives',
      description: 'Méthodes d\'apprentissage optimisées selon votre profil',
      details: 'Basé sur l\'analyse de vos performances et préférences d\'apprentissage',
      recommendations: [
        'Alterner entre différents types d\'exercices',
        'Utiliser la répétition espacée pour la mémorisation',
        'Pratiquer l\'auto-évaluation régulière'
      ],
      priority: 'medium',
      icon: <Brain className="w-6 h-6 text-purple-500" />
    });

    // Insight 5: Comparaison avec les pairs (simulé)
    insights.push({
      id: 5,
        type: 'comparison',
        title: '👥 Analyse Comparative',
        description: 'Votre position par rapport aux autres étudiants',
        details: analysis.overall_score >= 80 ? 'Vous êtes dans le top 20% des étudiants' :
                 analysis.overall_score >= 60 ? 'Vous êtes dans la moyenne supérieure' :
                 'Vous avez un potentiel de progression important',
        recommendations: [
          'Identifiez les meilleures pratiques des étudiants performants',
          'Participez aux sessions d\'étude en groupe',
          'Demandez de l\'aide aux professeurs sur les points difficiles'
        ],
        priority: 'low',
        icon: <Users className="w-6 h-6 text-indigo-500" />
    });

    // Insight 6: Prédictions et objectifs
    insights.push({
      id: 6,
        type: 'prediction',
        title: '🔮 Prédictions et Objectifs',
        description: 'Projections basées sur vos tendances actuelles',
        details: `Avec un effort régulier, vous pourriez atteindre un score de ${Math.min(100, analysis.overall_score + 15)}% dans les 2-3 prochaines semaines`,
        recommendations: [
          'Fixez-vous des objectifs hebdomadaires réalistes',
          'Suivez votre progression avec des métriques claires',
          'Célébrez vos petites victoires pour rester motivé'
        ],
        priority: 'medium',
        icon: <Award className="w-6 h-6 text-yellow-500" />
    });

    return insights;
  };

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'high': return 'border-red-300 bg-red-50';
      case 'medium': return 'border-yellow-300 bg-yellow-50';
      case 'low': return 'border-green-300 bg-green-50';
      default: return 'border-gray-300 bg-gray-50';
    }
  };

  const getPriorityBadge = (priority: string) => {
    switch (priority) {
      case 'high': return 'bg-red-100 text-red-800';
      case 'medium': return 'bg-yellow-100 text-yellow-800';
      case 'low': return 'bg-green-100 text-green-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-purple-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Génération de vos insights IA...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="max-w-4xl mx-auto p-6">
        <div className="bg-red-50 border border-red-200 rounded-lg p-4">
          <h2 className="text-red-800 font-semibold mb-2">Erreur</h2>
          <p className="text-red-700">{error}</p>
          <button 
            onClick={loadAIInsights}
            className="mt-4 px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700"
          >
            Réessayer
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-6xl mx-auto p-6">
      {/* En-tête */}
      <div className="mb-8">
        <div className="flex items-center gap-3 mb-4">
          <Brain className="w-8 h-8 text-purple-500" />
          <h1 className="text-3xl font-bold text-gray-900">IA Avancée</h1>
        </div>
        <p className="text-gray-600 text-lg">
          Découvrez les insights intelligents de votre tuteur IA basés sur vos performances
        </p>
      </div>

      {/* Sélecteur de matière */}
      <div className="mb-6">
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Matière à analyser
        </label>
        <select
          value={selectedSubject}
          onChange={(e) => setSelectedSubject(e.target.value)}
          className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-purple-500"
        >
          <option value="Français">Français</option>
          <option value="Mathématiques">Mathématiques</option>
          <option value="Histoire">Histoire</option>
          <option value="Géographie">Géographie</option>
          <option value="Sciences">Sciences</option>
        </select>
      </div>

      {gapAnalysis && aiInsights.length > 0 && (
        <>
          {/* Résumé des insights */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
            <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
              <div className="flex items-center justify-between mb-2">
                <Lightbulb className="w-6 h-6 text-yellow-500" />
                <span className="text-sm text-gray-500">Insights Générés</span>
              </div>
              <div className="text-3xl font-bold text-yellow-600">
                {aiInsights.length}
              </div>
              <p className="text-sm text-gray-600 mt-1">
                analyses intelligentes
              </p>
            </div>

            <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
              <div className="flex items-center justify-between mb-2">
                <BarChart3 className="w-6 h-6 text-blue-500" />
                <span className="text-sm text-gray-500">Score Global</span>
              </div>
              <div className={`text-3xl font-bold ${
                gapAnalysis.overall_score >= 80 ? 'text-green-600' :
                gapAnalysis.overall_score >= 60 ? 'text-blue-600' :
                gapAnalysis.overall_score >= 40 ? 'text-yellow-600' :
                'text-red-600'
              }`}>
                {gapAnalysis.overall_score}%
              </div>
              <p className="text-sm text-gray-600 mt-1">
                performance actuelle
              </p>
            </div>

            <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
              <div className="flex items-center justify-between mb-2">
                <Activity className="w-6 h-6 text-green-500" />
                <span className="text-sm text-gray-500">Priorité</span>
              </div>
              <div className="text-lg font-semibold px-3 py-1 rounded-full text-sm bg-red-100 text-red-800">
                {gapAnalysis.priority_level === 'high' ? 'Élevée' : 
                 gapAnalysis.priority_level === 'medium' ? 'Moyenne' : 'Faible'}
              </div>
              <p className="text-sm text-gray-600 mt-1">
                niveau d'attention requis
              </p>
            </div>
          </div>

          {/* Insights détaillés */}
          <div className="mb-8">
            <h2 className="text-2xl font-bold text-gray-900 mb-4 flex items-center gap-2">
              <Zap className="w-6 h-6 text-yellow-500" />
              Insights IA Personnalisés
            </h2>
            
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {aiInsights.map((insight) => (
                <div 
                  key={insight.id}
                  className={`p-6 rounded-lg border-2 transition-all duration-200 cursor-pointer hover:shadow-lg ${
                    selectedInsight === insight.id ? 'ring-2 ring-purple-500' : ''
                  } ${getPriorityColor(insight.priority)}`}
                  onClick={() => setSelectedInsight(selectedInsight === insight.id ? null : insight.id)}
                >
                  {/* En-tête de l'insight */}
                  <div className="flex items-start justify-between mb-4">
                    <div className="flex items-center gap-3">
                      {insight.icon}
                      <div>
                        <h3 className="font-semibold text-gray-900">{insight.title}</h3>
                        <span className={`px-2 py-1 rounded-full text-xs font-medium ${getPriorityBadge(insight.priority)}`}>
                          {insight.priority === 'high' ? 'Priorité Élevée' : 
                           insight.priority === 'medium' ? 'Priorité Moyenne' : 'Priorité Faible'}
                        </span>
                      </div>
                    </div>
                  </div>

                  {/* Description */}
                  <p className="text-gray-700 mb-3">
                    {insight.description}
                  </p>

                  {/* Détails */}
                  <p className="text-gray-600 text-sm mb-4">
                    {insight.details}
                  </p>

                  {/* Recommandations (expandables) */}
                  {selectedInsight === insight.id && (
                    <div className="mt-4 p-4 bg-white rounded-lg border border-gray-200">
                      <h4 className="font-medium text-gray-900 mb-3 flex items-center gap-2">
                        <BookOpen className="w-4 h-4 text-blue-500" />
                        Recommandations Spécifiques
                      </h4>
                      <ul className="space-y-2">
                        {insight.recommendations.map((rec, index) => (
                          <li key={index} className="flex items-start gap-2 text-sm text-gray-700">
                            <span className="w-2 h-2 bg-blue-500 rounded-full mt-2 flex-shrink-0"></span>
                            {rec}
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>

          {/* Actions recommandées */}
          <div className="bg-gradient-to-r from-purple-50 to-blue-50 p-6 rounded-lg border border-purple-200">
            <h2 className="text-2xl font-bold text-gray-900 mb-4 flex items-center gap-2">
              <Target className="w-6 h-6 text-purple-500" />
              Actions Recommandées par l'IA
            </h2>
            
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div className="text-center p-4 bg-white rounded-lg shadow-sm">
                <Target className="w-12 h-12 text-blue-500 mx-auto mb-3" />
                <h3 className="font-semibold text-gray-900 mb-2">Plan de Remédiation</h3>
                <p className="text-sm text-gray-600 mb-3">
                  Suivez un plan personnalisé basé sur l'analyse IA
                </p>
                <button 
                  onClick={() => window.location.href = '/dashboard/student/remediation'}
                  className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition-colors"
                >
                  Commencer
                </button>
              </div>

              <div className="text-center p-4 bg-white rounded-lg shadow-sm">
                <Brain className="w-12 h-12 text-purple-500 mx-auto mb-3" />
                <h3 className="font-semibold text-gray-900 mb-2">Analyse des Lacunes</h3>
                <p className="text-sm text-gray-600 mb-3">
                  Approfondissez l'analyse de vos points faibles
                </p>
                <button 
                  onClick={() => window.location.href = '/dashboard/student/gap-analysis'}
                  className="px-4 py-2 bg-purple-600 text-white rounded hover:bg-purple-700 transition-colors"
                >
                  Analyser
                </button>
              </div>

              <div className="text-center p-4 bg-white rounded-lg shadow-sm">
                <Zap className="w-12 h-12 text-yellow-500 mx-auto mb-3" />
                <h3 className="font-semibold text-gray-900 mb-2">Quiz Adaptatifs</h3>
                <p className="text-sm text-gray-600 mb-3">
                  Testez vos connaissances avec des quiz intelligents
                </p>
                <button 
                  onClick={() => window.location.href = '/dashboard/student/learning-path'}
                  className="px-4 py-2 bg-yellow-600 text-white rounded hover:bg-yellow-700 transition-colors"
                >
                  Pratiquer
                </button>
              </div>
            </div>
          </div>
        </>
      )}

      {/* Message si pas de données */}
      {!gapAnalysis && !loading && (
        <div className="text-center py-12">
          <Brain className="w-16 h-16 text-gray-400 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-gray-900 mb-2">Aucun insight IA disponible</h3>
          <p className="text-gray-600 mb-4">
            Commencez par passer quelques quiz pour générer des analyses intelligentes
          </p>
          <button 
            onClick={() => window.location.href = '/dashboard/student/learning-path'}
            className="px-6 py-3 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors"
          >
            Commencer un Quiz
          </button>
        </div>
      )}
    </div>
  );
}
