'use client';

import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import DashboardLayout from '../dashboard/DashboardLayout';

interface CognitiveProfile {
  id: string;
  studentName: string;
  learningStyle: string;
  cognitiveStrengths: string[];
  cognitiveWeaknesses: string[];
  irtAbility: number;
  confidence: number;
  lastAssessment: string;
  progress: number;
}

interface IRTModel {
  id: string;
  name: string;
  subject: string;
  totalQuestions: number;
  calibratedQuestions: number;
  averageDifficulty: number;
  discrimination: number;
  guessing: number;
  reliability: number;
  lastUpdated: string;
}

interface AnalyticsData {
  totalStudents: number;
  cognitiveProfiles: number;
  irtModels: number;
  averageAbility: number;
  topPerformers: number;
  strugglingStudents: number;
  subjectPerformance: {
    subject: string;
    averageScore: number;
    totalAssessments: number;
    irtReliability: number;
  }[];
}

export default function AdvancedAnalytics() {
  const router = useRouter();
  const [activeTab, setActiveTab] = useState<'overview' | 'cognitive' | 'irt' | 'performance'>('overview');
  const [analyticsData, setAnalyticsData] = useState<AnalyticsData | null>(null);
  const [cognitiveProfiles, setCognitiveProfiles] = useState<CognitiveProfile[]>([]);
  const [irtModels, setIrtModels] = useState<IRTModel[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedStudent, setSelectedStudent] = useState<string>('');

  useEffect(() => {
    // Simuler le chargement des données
    setTimeout(() => {
      setAnalyticsData({
        totalStudents: 156,
        cognitiveProfiles: 142,
        irtModels: 8,
        averageAbility: 0.68,
        topPerformers: 23,
        strugglingStudents: 18,
        subjectPerformance: [
          { subject: 'Mathématiques', averageScore: 78.5, totalAssessments: 45, irtReliability: 0.89 },
          { subject: 'Physique', averageScore: 72.3, totalAssessments: 38, irtReliability: 0.85 },
          { subject: 'Chimie', averageScore: 81.2, totalAssessments: 42, irtReliability: 0.91 },
          { subject: 'Histoire', averageScore: 75.8, totalAssessments: 35, irtReliability: 0.82 }
        ]
      });

      setCognitiveProfiles([
        {
          id: '1',
          studentName: 'Ahmed Ben Ali',
          learningStyle: 'Visuel + Kinesthésique',
          cognitiveStrengths: ['Raisonnement spatial', 'Mémoire visuelle', 'Résolution de problèmes'],
          cognitiveWeaknesses: ['Calcul mental', 'Mémorisation verbale'],
          irtAbility: 0.82,
          confidence: 0.75,
          lastAssessment: 'Il y a 2 jours',
          progress: 85
        },
        {
          id: '2',
          studentName: 'Fatima Zahra',
          learningStyle: 'Auditif + Logique',
          cognitiveStrengths: ['Compréhension orale', 'Pensée logique', 'Analyse critique'],
          cognitiveWeaknesses: ['Représentation spatiale', 'Coordination motrice'],
          irtAbility: 0.91,
          confidence: 0.88,
          lastAssessment: 'Il y a 1 jour',
          progress: 92
        },
        {
          id: '3',
          studentName: 'Omar Hassan',
          learningStyle: 'Kinesthésique + Social',
          cognitiveStrengths: ['Apprentissage pratique', 'Travail en équipe', 'Communication'],
          cognitiveWeaknesses: ['Théorie abstraite', 'Concentration prolongée'],
          irtAbility: 0.65,
          confidence: 0.52,
          lastAssessment: 'Il y a 3 jours',
          progress: 68
        }
      ]);

      setIrtModels([
        {
          id: '1',
          name: 'Modèle Mathématiques - Algèbre',
          subject: 'Mathématiques',
          totalQuestions: 156,
          calibratedQuestions: 142,
          averageDifficulty: 0.65,
          discrimination: 0.78,
          guessing: 0.22,
          reliability: 0.89,
          lastUpdated: 'Il y a 2 jours'
        },
        {
          id: '2',
          name: 'Modèle Physique - Mécanique',
          subject: 'Physique',
          totalQuestions: 98,
          calibratedQuestions: 87,
          averageDifficulty: 0.72,
          discrimination: 0.81,
          guessing: 0.18,
          reliability: 0.85,
          lastUpdated: 'Il y a 1 semaine'
        },
        {
          id: '3',
          name: 'Modèle Chimie - Réactions',
          subject: 'Chimie',
          totalQuestions: 124,
          calibratedQuestions: 118,
          averageDifficulty: 0.58,
          discrimination: 0.85,
          guessing: 0.15,
          reliability: 0.91,
          lastUpdated: 'Il y a 3 jours'
        }
      ]);

      setLoading(false);
    }, 1500);
  }, []);

  const getLearningStyleColor = (style: string) => {
    if (style.includes('Visuel')) return 'text-blue-600';
    if (style.includes('Auditif')) return 'text-green-600';
    if (style.includes('Kinesthésique')) return 'text-purple-600';
    if (style.includes('Logique')) return 'text-orange-600';
    return 'text-gray-600';
  };

  const getAbilityColor = (ability: number) => {
    if (ability >= 0.8) return 'text-green-600';
    if (ability >= 0.6) return 'text-blue-600';
    if (ability >= 0.4) return 'text-yellow-600';
    return 'text-red-600';
  };

  const getReliabilityColor = (reliability: number) => {
    if (reliability >= 0.9) return 'text-green-600';
    if (reliability >= 0.8) return 'text-blue-600';
    if (reliability >= 0.7) return 'text-yellow-600';
    return 'text-red-600';
  };

  if (loading) {
    return (
      <DashboardLayout userType="teacher" title="Analytics Avancés" subtitle="Chargement...">
        <div className="flex items-center justify-center h-64">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
        </div>
      </DashboardLayout>
    );
  }

  return (
    <DashboardLayout 
      userType="teacher" 
      title="Analytics Avancés" 
      subtitle="Analyse cognitive et modèles IRT"
    >
      {/* En-tête avec métriques principales */}
      <div className="mb-8">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <div className="bg-white rounded-lg shadow p-6 border-l-4 border-blue-500">
            <div className="flex items-center">
              <div className="p-3 rounded-full bg-blue-100 text-blue-600">
                <span className="text-2xl">🧠</span>
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Profils Cognitifs</p>
                <p className="text-2xl font-semibold text-gray-900">{analyticsData?.cognitiveProfiles}</p>
                <p className="text-xs text-gray-500">sur {analyticsData?.totalStudents} étudiants</p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6 border-l-4 border-green-500">
            <div className="flex items-center">
              <div className="p-3 rounded-full bg-green-100 text-green-600">
                <span className="text-2xl">📊</span>
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Modèles IRT</p>
                <p className="text-2xl font-semibold text-gray-900">{analyticsData?.irtModels}</p>
                <p className="text-xs text-gray-500">actifs</p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6 border-l-4 border-purple-500">
            <div className="flex items-center">
              <div className="p-3 rounded-full bg-purple-100 text-purple-600">
                <span className="text-2xl">📈</span>
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Habileté Moyenne</p>
                <p className="text-2xl font-semibold text-gray-900">{(analyticsData?.averageAbility || 0) * 100}%</p>
                <p className="text-xs text-gray-500">niveau global</p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6 border-l-4 border-orange-500">
            <div className="flex items-center">
              <div className="p-3 rounded-full bg-orange-100 text-orange-600">
                <span className="text-2xl">🎯</span>
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Étudiants en Difficulté</p>
                <p className="text-2xl font-semibold text-gray-900">{analyticsData?.strugglingStudents}</p>
                <p className="text-xs text-gray-500">nécessitent attention</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Onglets de navigation */}
      <div className="bg-white rounded-lg shadow mb-8">
        <div className="border-b border-gray-200">
          <nav className="flex space-x-8 px-6">
            {[
              { id: 'overview', label: 'Vue d\'ensemble', icon: '📊' },
              { id: 'cognitive', label: 'Profils Cognitifs', icon: '🧠' },
              { id: 'irt', label: 'Modèles IRT', icon: '📈' },
              { id: 'performance', label: 'Performance par Matière', icon: '📚' }
            ].map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id as any)}
                className={`flex items-center space-x-2 py-4 px-1 border-b-2 font-medium text-sm ${
                  activeTab === tab.id
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                <span>{tab.icon}</span>
                <span>{tab.label}</span>
              </button>
            ))}
          </nav>
        </div>

        <div className="p-6">
          {/* Vue d'ensemble */}
          {activeTab === 'overview' && (
            <div className="space-y-6">
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {/* Distribution des styles d'apprentissage */}
                <div className="bg-gray-50 rounded-lg p-6">
                  <h3 className="text-lg font-semibold text-gray-900 mb-4">Distribution des Styles d'Apprentissage</h3>
                  <div className="space-y-3">
                    {[
                      { style: 'Visuel', count: 45, percentage: 32 },
                      { style: 'Auditif', count: 38, percentage: 27 },
                      { style: 'Kinesthésique', count: 35, percentage: 25 },
                      { style: 'Logique', count: 24, percentage: 17 }
                    ].map((item) => (
                      <div key={item.style} className="flex items-center justify-between">
                        <span className="text-sm font-medium text-gray-700">{item.style}</span>
                        <div className="flex items-center space-x-3">
                          <div className="w-24 bg-gray-200 rounded-full h-2">
                            <div 
                              className="bg-blue-500 h-2 rounded-full"
                              style={{ width: `${item.percentage}%` }}
                            ></div>
                          </div>
                          <span className="text-sm text-gray-600 w-12 text-right">{item.percentage}%</span>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Performance des modèles IRT */}
                <div className="bg-gray-50 rounded-lg p-6">
                  <h3 className="text-lg font-semibold text-gray-900 mb-4">Performance des Modèles IRT</h3>
                  <div className="space-y-3">
                    {irtModels.slice(0, 4).map((model) => (
                      <div key={model.id} className="flex items-center justify-between">
                        <span className="text-sm font-medium text-gray-700">{model.subject}</span>
                        <div className="flex items-center space-x-2">
                          <span className={`text-sm font-semibold ${getReliabilityColor(model.reliability)}`}>
                            {(model.reliability * 100).toFixed(0)}%
                          </span>
                          <span className="text-xs text-gray-500">fiabilité</span>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </div>

              {/* Graphique de progression globale */}
              <div className="bg-gray-50 rounded-lg p-6">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Progression Globale des Étudiants</h3>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                  <div className="text-center">
                    <div className="w-24 h-24 mx-auto mb-3 relative">
                      <svg className="w-24 h-24 transform -rotate-90" viewBox="0 0 36 36">
                        <path
                          className="text-gray-200"
                          strokeWidth="3"
                          fill="none"
                          d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                        />
                        <path
                          className="text-green-500"
                          strokeWidth="3"
                          strokeDasharray="68, 100"
                          strokeLinecap="round"
                          fill="none"
                          d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                        />
                      </svg>
                      <div className="absolute inset-0 flex items-center justify-center">
                        <span className="text-lg font-semibold text-gray-900">68%</span>
                      </div>
                    </div>
                    <p className="text-sm text-gray-600">Progression Moyenne</p>
                  </div>

                  <div className="text-center">
                    <div className="w-24 h-24 mx-auto mb-3 relative">
                      <svg className="w-24 h-24 transform -rotate-90" viewBox="0 0 36 36">
                        <path
                          className="text-gray-200"
                          strokeWidth="3"
                          fill="none"
                          d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                        />
                        <path
                          className="text-blue-500"
                          strokeWidth="3"
                          strokeDasharray="85, 100"
                          strokeLinecap="round"
                          fill="none"
                          d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                        />
                      </svg>
                      <div className="absolute inset-0 flex items-center justify-center">
                        <span className="text-lg font-semibold text-gray-900">85%</span>
                      </div>
                    </div>
                    <p className="text-sm text-gray-600">Fiabilité IRT</p>
                  </div>

                  <div className="text-center">
                    <div className="w-24 h-24 mx-auto mb-3 relative">
                      <svg className="w-24 h-24 transform -rotate-90" viewBox="0 0 36 36">
                        <path
                          className="text-gray-200"
                          strokeWidth="3"
                          fill="none"
                          d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                        />
                        <path
                          className="text-purple-500"
                          strokeWidth="3"
                          strokeDasharray="72, 100"
                          strokeLinecap="round"
                          fill="none"
                          d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                        />
                      </svg>
                      <div className="absolute inset-0 flex items-center justify-center">
                        <span className="text-lg font-semibold text-gray-900">72%</span>
                      </div>
                    </div>
                    <p className="text-sm text-gray-600">Engagement Étudiants</p>
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Profils cognitifs */}
          {activeTab === 'cognitive' && (
            <div className="space-y-6">
              <div className="flex justify-between items-center">
                <h3 className="text-lg font-semibold text-gray-900">Profils Cognitifs des Étudiants</h3>
                <button className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors">
                  Exporter les données
                </button>
              </div>

              <div className="overflow-x-auto">
                <table className="min-w-full divide-y divide-gray-200">
                  <thead className="bg-gray-50">
                    <tr>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Étudiant
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Style d'Apprentissage
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Habileté IRT
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Progression
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Actions
                      </th>
                    </tr>
                  </thead>
                  <tbody className="bg-white divide-y divide-gray-200">
                    {cognitiveProfiles.map((profile) => (
                      <tr key={profile.id} className="hover:bg-gray-50">
                        <td className="px-6 py-4 whitespace-nowrap">
                          <div className="flex items-center">
                            <div className="w-8 h-8 bg-gradient-to-r from-blue-500 to-indigo-600 rounded-full flex items-center justify-center text-white font-medium text-sm">
                              {profile.studentName.split(' ').map(n => n[0]).join('')}
                            </div>
                            <div className="ml-3">
                              <div className="text-sm font-medium text-gray-900">{profile.studentName}</div>
                              <div className="text-sm text-gray-500">{profile.lastAssessment}</div>
                            </div>
                          </div>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap">
                          <span className={`text-sm font-medium ${getLearningStyleColor(profile.learningStyle)}`}>
                            {profile.learningStyle}
                          </span>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap">
                          <span className={`text-sm font-semibold ${getAbilityColor(profile.irtAbility)}`}>
                            {(profile.irtAbility * 100).toFixed(0)}%
                          </span>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap">
                          <div className="flex items-center">
                            <div className="w-20 bg-gray-200 rounded-full h-2 mr-2">
                              <div 
                                className="bg-green-500 h-2 rounded-full"
                                style={{ width: `${profile.progress}%` }}
                              ></div>
                            </div>
                            <span className="text-sm text-gray-600">{profile.progress}%</span>
                          </div>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                          <button className="text-blue-600 hover:text-blue-900 mr-3">Voir détails</button>
                          <button className="text-green-600 hover:text-green-900">Recommandations</button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}

          {/* Modèles IRT */}
          {activeTab === 'irt' && (
            <div className="space-y-6">
              <div className="flex justify-between items-center">
                <h3 className="text-lg font-semibold text-gray-900">Modèles IRT et Calibration</h3>
                <button className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors">
                  Nouveau Modèle
                </button>
              </div>

              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {irtModels.map((model) => (
                  <div key={model.id} className="bg-gray-50 rounded-lg p-6">
                    <div className="flex justify-between items-start mb-4">
                      <div>
                        <h4 className="text-lg font-semibold text-gray-900">{model.name}</h4>
                        <p className="text-sm text-gray-500">{model.subject}</p>
                      </div>
                      <span className={`px-2 py-1 text-xs font-medium rounded-full ${
                        model.reliability >= 0.9 ? 'bg-green-100 text-green-800' :
                        model.reliability >= 0.8 ? 'bg-blue-100 text-blue-800' :
                        model.reliability >= 0.7 ? 'bg-yellow-100 text-yellow-800' :
                        'bg-red-100 text-red-800'
                      }`}>
                        {(model.reliability * 100).toFixed(0)}% fiabilité
                      </span>
                    </div>

                    <div className="grid grid-cols-2 gap-4 mb-4">
                      <div>
                        <p className="text-sm text-gray-600">Questions totales</p>
                        <p className="text-lg font-semibold text-gray-900">{model.totalQuestions}</p>
                      </div>
                      <div>
                        <p className="text-sm text-gray-600">Calibrées</p>
                        <p className="text-lg font-semibold text-gray-900">{model.calibratedQuestions}</p>
                      </div>
                      <div>
                        <p className="text-sm text-gray-600">Difficulté moyenne</p>
                        <p className="text-lg font-semibold text-gray-900">{(model.averageDifficulty * 100).toFixed(0)}%</p>
                      </div>
                      <div>
                        <p className="text-sm text-gray-600">Discrimination</p>
                        <p className="text-lg font-semibold text-gray-900">{model.discrimination.toFixed(2)}</p>
                      </div>
                    </div>

                    <div className="flex justify-between items-center">
                      <span className="text-xs text-gray-500">Mis à jour {model.lastUpdated}</span>
                      <div className="space-x-2">
                        <button className="px-3 py-1 text-xs bg-blue-100 text-blue-800 rounded hover:bg-blue-200">
                          Calibrer
                        </button>
                        <button className="px-3 py-1 text-xs bg-green-100 text-green-800 rounded hover:bg-green-200">
                          Analyser
                        </button>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Performance par matière */}
          {activeTab === 'performance' && (
            <div className="space-y-6">
              <h3 className="text-lg font-semibold text-gray-900">Performance par Matière</h3>
              
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {analyticsData?.subjectPerformance.map((subject) => (
                  <div key={subject.subject} className="bg-white border border-gray-200 rounded-lg p-6">
                    <div className="flex justify-between items-start mb-4">
                      <h4 className="text-lg font-semibold text-gray-900">{subject.subject}</h4>
                      <span className={`px-2 py-1 text-xs font-medium rounded-full ${
                        subject.irtReliability >= 0.9 ? 'bg-green-100 text-green-800' :
                        subject.irtReliability >= 0.8 ? 'bg-blue-100 text-blue-800' :
                        'bg-yellow-100 text-yellow-800'
                      }`}>
                        {(subject.irtReliability * 100).toFixed(0)}% fiabilité
                      </span>
                    </div>

                    <div className="space-y-3">
                      <div className="flex justify-between items-center">
                        <span className="text-sm text-gray-600">Score moyen</span>
                        <span className="text-lg font-semibold text-gray-900">{subject.averageScore}%</span>
                      </div>
                      <div className="flex justify-between items-center">
                        <span className="text-sm text-gray-600">Total évaluations</span>
                        <span className="text-sm font-medium text-gray-900">{subject.totalAssessments}</span>
                      </div>
                      <div className="flex justify-between items-center">
                        <span className="text-sm text-gray-600">Fiabilité IRT</span>
                        <span className={`text-sm font-semibold ${getReliabilityColor(subject.irtReliability)}`}>
                          {(subject.irtReliability * 100).toFixed(0)}%
                        </span>
                      </div>
                    </div>

                    <div className="mt-4 pt-4 border-t border-gray-200">
                      <button className="w-full px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors">
                        Voir l'analyse détaillée
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </DashboardLayout>
  );
}















