'use client';

import React, { useState, useEffect } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import { Line, Doughnut, Bar } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  ArcElement,
  BarElement,
} from 'chart.js';

// Enregistrer les composants Chart.js
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  ArcElement,
  BarElement
);

interface CognitiveProfile {
  learning_style: string;
  strengths: string[];
  weaknesses: string[];
  recommendations: string[];
  confidence_level: number;
}

export default function CognitiveProfilePage() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const [profile, setProfile] = useState<CognitiveProfile | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Récupérer le profil depuis les paramètres d'URL ou l'API
    const profileParam = searchParams.get('profile');
    if (profileParam) {
      try {
        const profileData = JSON.parse(profileParam);
        setProfile(profileData);
      } catch (error) {
        console.error('Erreur lors du parsing du profil:', error);
      }
    } else {
      // Charger le profil depuis l'API
      loadCognitiveProfile();
    }
    setLoading(false);
  }, [searchParams]);

  const loadCognitiveProfile = async () => {
    try {
      // Simuler un appel API
      const mockProfile: CognitiveProfile = {
        learning_style: "visuel",
        strengths: ["logique mathématique", "compréhension visuelle", "mémoire spatiale"],
        weaknesses: ["compréhension auditive", "expression orale"],
        recommendations: [
          "Utilisez des diagrammes et schémas pour apprendre",
          "Regardez des vidéos explicatives",
          "Créez des mind maps pour organiser vos idées"
        ],
        confidence_level: 0.85
      };
      setProfile(mockProfile);
    } catch (error) {
      console.error('Erreur lors du chargement du profil:', error);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Chargement de votre profil cognitif...</p>
        </div>
      </div>
    );
  }

  if (!profile) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="text-red-500 text-6xl mb-4">⚠️</div>
          <h2 className="text-xl font-semibold text-gray-700 mb-2">
            Profil non trouvé
          </h2>
          <p className="text-gray-500 mb-4">
            Aucun profil cognitif n'a été trouvé pour votre compte.
          </p>
          <button
            onClick={() => router.push('/assessment/adaptive')}
            className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors"
          >
            Passer une évaluation pour générer un profil
          </button>
        </div>
      </div>
    );
  }

  // Données pour les graphiques
  const learningStyleData = {
    labels: ['Visuel', 'Auditif', 'Kinesthésique', 'Lecture/Écriture'],
    datasets: [
      {
        data: [65, 15, 10, 10],
        backgroundColor: [
          '#3B82F6',
          '#10B981',
          '#F59E0B',
          '#8B5CF6'
        ],
        borderWidth: 2,
        borderColor: '#fff'
      }
    ]
  };

  const strengthsData = {
    labels: profile.strengths,
    datasets: [
      {
        label: 'Niveau de compétence',
        data: [90, 85, 80, 75, 70],
        backgroundColor: 'rgba(59, 130, 246, 0.8)',
        borderColor: '#3B82F6',
        borderWidth: 2
      }
    ]
  };

  const confidenceData = {
    labels: ['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Juin'],
    datasets: [
      {
        label: 'Niveau de confiance',
        data: [0.6, 0.65, 0.7, 0.75, 0.8, profile.confidence_level],
        borderColor: '#10B981',
        backgroundColor: 'rgba(16, 185, 129, 0.1)',
        tension: 0.4,
        fill: true
      }
    ]
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold text-gray-900">
                🧠 Mon Profil Cognitif
              </h1>
              <p className="text-gray-600 mt-1">
                Analyse personnalisée de votre style d'apprentissage
              </p>
            </div>
            <div className="flex space-x-3">
              <button
                onClick={() => router.push('/assessment/adaptive')}
                className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors"
              >
                🔄 Nouvelle Évaluation
              </button>
              <button
                onClick={() => router.push('/dashboard/student')}
                className="bg-gray-100 text-gray-700 px-4 py-2 rounded-lg hover:bg-gray-200 transition-colors"
              >
                ← Retour au Dashboard
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Contenu principal */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Résumé du profil */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
          <div className="bg-white rounded-xl shadow-lg p-6">
            <div className="text-center">
              <div className="text-4xl mb-2">🎯</div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">
                Style d'Apprentissage
              </h3>
              <p className="text-2xl font-bold text-blue-600 capitalize">
                {profile.learning_style}
              </p>
            </div>
          </div>

          <div className="bg-white rounded-xl shadow-lg p-6">
            <div className="text-center">
              <div className="text-4xl mb-2">📊</div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">
                Niveau de Confiance
              </h3>
              <p className="text-2xl font-bold text-green-600">
                {Math.round(profile.confidence_level * 100)}%
              </p>
            </div>
          </div>

          <div className="bg-white rounded-xl shadow-lg p-6">
            <div className="text-center">
              <div className="text-4xl mb-2">🚀</div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">
                Recommandations
              </h3>
              <p className="text-2xl font-bold text-purple-600">
                {profile.recommendations.length}
              </p>
            </div>
          </div>
        </div>

        {/* Graphiques */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
          {/* Style d'apprentissage */}
          <div className="bg-white rounded-xl shadow-lg p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4 text-center">
              Répartition du Style d'Apprentissage
            </h3>
            <div className="h-64">
              <Doughnut
                data={learningStyleData}
                options={{
                  responsive: true,
                  maintainAspectRatio: false,
                  plugins: {
                    legend: {
                      position: 'bottom'
                    }
                  }
                }}
              />
            </div>
          </div>

          {/* Évolution de la confiance */}
          <div className="bg-white rounded-xl shadow-lg p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4 text-center">
              Évolution de la Confiance
            </h3>
            <div className="h-64">
              <Line
                data={confidenceData}
                options={{
                  responsive: true,
                  maintainAspectRatio: false,
                  scales: {
                    y: {
                      beginAtZero: true,
                      max: 1
                    }
                  },
                  plugins: {
                    legend: {
                      position: 'bottom'
                    }
                  }
                }}
              />
            </div>
          </div>
        </div>

        {/* Forces et faiblesses */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
          {/* Forces */}
          <div className="bg-white rounded-xl shadow-lg p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4 text-center">
              💪 Mes Forces
            </h3>
            <div className="space-y-3">
              {profile.strengths.map((strength, index) => (
                <div key={index} className="flex items-center space-x-3 p-3 bg-green-50 rounded-lg">
                  <div className="text-green-500">✅</div>
                  <span className="text-gray-700">{strength}</span>
                </div>
              ))}
            </div>
          </div>

          {/* Faiblesses */}
          <div className="bg-white rounded-xl shadow-lg p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4 text-center">
              🔧 Mes Points d'Amélioration
            </h3>
            <div className="space-y-3">
              {profile.weaknesses.map((weakness, index) => (
                <div key={index} className="flex items-center space-x-3 p-3 bg-orange-50 rounded-lg">
                  <div className="text-orange-500">⚠️</div>
                  <span className="text-gray-700">{weakness}</span>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Recommandations */}
        <div className="bg-white rounded-xl shadow-lg p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4 text-center">
            💡 Recommandations Personnalisées
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {profile.recommendations.map((recommendation, index) => (
              <div key={index} className="flex items-start space-x-3 p-4 bg-blue-50 rounded-lg">
                <div className="text-blue-500 text-lg">💡</div>
                <span className="text-gray-700">{recommendation}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Actions */}
        <div className="text-center mt-8">
          <button
            onClick={() => router.push('/assessment/adaptive')}
            className="bg-gradient-to-r from-blue-600 to-indigo-600 text-white px-8 py-3 rounded-lg text-lg font-semibold hover:from-blue-700 hover:to-indigo-700 transition-all duration-200 transform hover:scale-105 shadow-lg mr-4"
          >
            🔄 Passer une Nouvelle Évaluation
          </button>
          <button
            onClick={() => router.push('/dashboard/student/progress')}
            className="bg-gray-600 text-white px-8 py-3 rounded-lg text-lg font-semibold hover:bg-gray-700 transition-all duration-200"
          >
            📈 Voir ma Progression
          </button>
        </div>
      </div>
    </div>
  );
}












