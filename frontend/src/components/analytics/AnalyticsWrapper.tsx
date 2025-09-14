'use client';

import React, { useState, useEffect } from 'react';
import AdvancedAnalyticsDashboard from './AdvancedAnalyticsDashboard';

interface AnalyticsWrapperProps {
  classId?: number;
  teacherId?: number;
  viewMode?: 'class' | 'student' | 'overview';
  onNavigate?: (route: string) => void;
}

const AnalyticsWrapper: React.FC<AnalyticsWrapperProps> = ({
  classId,
  teacherId,
  viewMode = 'overview',
  onNavigate
}) => {
  const [isLoading, setIsLoading] = useState(true);
  const [analyticsData, setAnalyticsData] = useState(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadAnalyticsData();
  }, [classId, teacherId, viewMode]);

  const loadAnalyticsData = async () => {
    try {
      setIsLoading(true);
      setError(null);

      let endpoint = '';
      let params = {};

      switch (viewMode) {
        case 'class':
          if (classId) {
            endpoint = `/api/v1/advanced/dashboard/class-overview?class_id=${classId}`;
          }
          break;
        case 'student':
          // Pour l'analyse d'un étudiant spécifique
          endpoint = `/api/v1/advanced/cognitive/generate-profile`;
          break;
        case 'overview':
        default:
          // Vue d'ensemble générale
          endpoint = '/api/v1/analytics/overview';
          break;
      }

      if (endpoint) {
        const response = await fetch(endpoint, {
          method: viewMode === 'student' ? 'POST' : 'GET',
          headers: {
            'Content-Type': 'application/json',
          },
          body: viewMode === 'student' ? JSON.stringify(params) : undefined,
        });

        if (response.ok) {
          const data = await response.json();
          setAnalyticsData(data);
        } else {
          throw new Error(`Erreur HTTP: ${response.status}`);
        }
      } else {
        // Utiliser des données simulées si l'endpoint n'est pas défini
        setAnalyticsData(generateMockData());
      }
    } catch (error) {
      console.error('Erreur lors du chargement des analytics:', error);
      setError(error instanceof Error ? error.message : 'Erreur inconnue');
      
      // Utiliser des données simulées en cas d'erreur
      setAnalyticsData(generateMockData());
    } finally {
      setIsLoading(false);
    }
  };

  const generateMockData = () => {
    // Données simulées pour le développement
    return {
      class_overview: {
        class_id: classId || 1,
        class_name: "Classe 6ème A",
        total_students: 25,
        average_performance: 78.5,
        cognitive_insights: {
          learning_styles_distribution: {
            visual: 40,
            auditory: 25,
            kinesthetic: 20,
            reading_writing: 15
          },
          common_strengths: ["logique mathématique", "compréhension écrite"],
          common_weaknesses: ["résolution de problèmes", "mémoire à long terme"],
          recommendations: [
            "Intégrer plus d'exercices pratiques",
            "Utiliser des supports visuels pour les concepts abstraits",
            "Encourager la collaboration entre pairs"
          ]
        },
        irt_insights: {
          optimal_difficulty_range: "4-6",
          cognitive_load_balance: "équilibré",
          adaptation_recommendations: [
            "Augmenter progressivement la difficulté",
            "Alterner entre types de questions",
            "Surveiller la charge cognitive"
          ]
        }
      },
      student_progress: {
        student_id: 1,
        student_name: "Alice Martin",
        overall_progress: 78.5,
        cognitive_evolution: {
          confidence_level: "increasing",
          learning_efficiency: "improving",
          error_patterns: "decreasing",
          response_time: "stabilizing"
        },
        subject_performance: {
          math: { score: 85, trend: "up", weaknesses: ["géométrie"] },
          french: { score: 72, trend: "stable", weaknesses: ["grammaire"] },
          science: { score: 88, trend: "up", weaknesses: [] }
        },
        irt_analysis: {
          current_ability: 6.2,
          optimal_difficulty: 6,
          learning_curve: "positive",
          next_milestone: "difficulty 7"
        },
        recommendations: [
          "Continuer avec les exercices de géométrie",
          "Renforcer la grammaire française",
          "Maintenir le niveau en sciences"
        ]
      }
    };
  };

  const handleRefresh = () => {
    loadAnalyticsData();
  };

  const handleExport = (format: 'pdf' | 'excel' | 'csv') => {
    console.log(`Export en format ${format}...`);
    // Implémenter l'export selon le format
  };

  const handleNavigate = (route: string) => {
    if (onNavigate) {
      onNavigate(route);
    }
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-gray-50 to-blue-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <h2 className="text-xl font-semibold text-gray-700 mb-2">
            Chargement des analytics...
          </h2>
          <p className="text-gray-500">
            Analyse des données en cours
          </p>
        </div>
      </div>
    );
  }

  if (error && !analyticsData) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-red-50 to-pink-50 flex items-center justify-center">
        <div className="text-center max-w-md mx-auto p-6">
          <div className="text-red-500 text-6xl mb-4">⚠️</div>
          <h2 className="text-xl font-semibold text-gray-700 mb-2">
            Erreur de chargement
          </h2>
          <p className="text-gray-500 mb-4">
            {error}
          </p>
          <button
            onClick={handleRefresh}
            className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors"
          >
            Réessayer
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <AdvancedAnalyticsDashboard
        data={analyticsData}
        viewMode={viewMode}
        onRefresh={handleRefresh}
        onExport={handleExport}
        onNavigate={handleNavigate}
        classId={classId}
        teacherId={teacherId}
      />
    </div>
  );
};

export default AnalyticsWrapper;












