'use client';

import React, { useState, useEffect } from 'react';
import { useAuth } from '../../hooks/useAuth';
import { Target, CheckCircle, Clock, TrendingUp, AlertCircle, Play, Award, RefreshCw } from 'lucide-react';
import SimpleIcon, { SimpleIconWithBackground } from '../ui/SimpleIcon';

interface Assessment {
  id: number;
  title: string;
  description: string;
  subject: string;
  difficulty: string;
  estimated_time: number;
  status: 'pending' | 'in_progress' | 'completed';
  created_at: string;
  due_date?: string;
}

interface AssessmentResult {
  id: number;
  assessment_id: number;
  score: number;
  max_score: number;
  percentage: number;
  completed_at: string;
  strengths: string[];
  weaknesses: string[];
  recommendations: string[];
}

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export default function InitialAssessmentWidget({ className = '' }: { className?: string }) {
  const { user, token } = useAuth();
  const [assessments, setAssessments] = useState<Assessment[]>([]);
  const [completedAssessments, setCompletedAssessments] = useState<Assessment[]>([]);
  const [pendingAssessments, setPendingAssessments] = useState<Assessment[]>([]);
  const [selectedAssessment, setSelectedAssessment] = useState<Assessment | null>(null);
  const [assessmentResult, setAssessmentResult] = useState<AssessmentResult | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showResults, setShowResults] = useState(false);

  useEffect(() => {
    if (user?.id && token) {
      console.log('[InitialAssessmentWidget] 🔐 Authentification OK:', { userId: user.id, hasToken: !!token });
      loadAssessments();
    } else {
      console.log('[InitialAssessmentWidget] ❌ Authentification manquante:', { user: user?.id, hasToken: !!token });
    }
  }, [user?.id, token]);

  const loadAssessments = async () => {
    try {
      setLoading(true);
      setError(null);

      console.log('[InitialAssessmentWidget] 📡 Chargement des évaluations pour l\'utilisateur:', user?.id);

      // Appels parallèles pour récupérer les évaluations françaises
      const [profileRes, testStatusRes] = await Promise.all([
        fetch(`${API_BASE_URL}/api/v1/french-optimized/student/${user?.id}/profile`, {
          headers: { 'Authorization': `Bearer ${token}` }
        }),
        fetch(`${API_BASE_URL}/api/v1/french-optimized/student/start`, {
          method: 'POST',
          headers: { 
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ student_id: user?.id })
        })
      ]);

      console.log('[InitialAssessmentWidget] 📊 Réponses API:', { 
        profileStatus: profileRes.status, 
        testStatusStatus: testStatusRes.status 
      });

      // Traitement du profil français
      if (profileRes.ok) {
        const profileData = await profileRes.json();
        console.log('[InitialAssessmentWidget] ✅ Profil français récupéré:', profileData);
        
        // Créer une évaluation simulée basée sur le profil
        const simulatedAssessment = {
          id: 1,
          title: 'Évaluation Française',
          description: 'Test de niveau français',
          subject: 'Français',
          difficulty: profileData.french_level || 'A1',
          estimated_time: 30,
          status: 'pending'
        };
        
        setPendingAssessments([simulatedAssessment]);
      } else {
        console.log('[InitialAssessmentWidget] ❌ Erreur profil français:', profileRes.status, profileRes.statusText);
        setPendingAssessments([]);
      }

      // Traitement du statut du test
      if (testStatusRes.ok) {
        const testData = await testStatusRes.json();
        console.log('[InitialAssessmentWidget] ✅ Statut du test récupéré:', testData);
        
        if (testData.status === 'completed') {
          const completedAssessment = {
            id: 2,
            title: 'Évaluation Française',
            description: 'Test de niveau français terminé',
            subject: 'Français',
            difficulty: testData.final_level || 'A1',
            estimated_time: 30,
            status: 'completed',
            score: testData.final_score || 0
          };
          
          setCompletedAssessments([completedAssessment]);
        } else {
          setCompletedAssessments([]);
        }
      } else {
        console.log('[InitialAssessmentWidget] ❌ Erreur statut du test:', testStatusRes.status, testStatusRes.statusText);
        setCompletedAssessments([]);
      }

      setAssessments([...pendingAssessments, ...completedAssessments]);
    } catch (err) {
      console.error('[InitialAssessmentWidget] 💥 Erreur lors du chargement des évaluations:', err);
      setError('Erreur lors du chargement des évaluations');
      // En cas d'erreur, vider les listes
      setPendingAssessments([]);
      setCompletedAssessments([]);
      setAssessments([]);
    } finally {
      setLoading(false);
    }
  };

  // Fonction de rechargement forcé
  const forceRefresh = () => {
    console.log('[InitialAssessmentWidget] 🔄 Rechargement forcé des évaluations');
    setError(null);
    loadAssessments();
  };

  const startAssessment = async (assessment: Assessment) => {
    try {
      setError(null);
      setSelectedAssessment(assessment);

      console.log('[InitialAssessmentWidget] 🚀 Démarrage de l\'évaluation:', assessment.id);

      const response = await fetch(`${API_BASE_URL}/api/v1/assessments/${assessment.id}/start`, {
        method: 'POST',
        headers: { 
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });

      if (!response.ok) {
        throw new Error('Erreur lors du démarrage de l\'évaluation');
      }

      // Rediriger vers la page d'évaluation ou afficher les questions
      console.log('[InitialAssessmentWidget] ✅ Évaluation démarrée:', assessment.title);
    } catch (err) {
      console.error('[InitialAssessmentWidget] 💥 Erreur lors du démarrage de l\'évaluation:', err);
      setError('Erreur lors du démarrage de l\'évaluation');
    }
  };

  const viewResults = async (assessment: Assessment) => {
    try {
      setError(null);
      setSelectedAssessment(assessment);

      console.log('[InitialAssessmentWidget] 📊 Affichage des résultats pour:', assessment.id);

      const response = await fetch(`${API_BASE_URL}/api/v1/assessments/${assessment.id}/results`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });

      if (!response.ok) {
        throw new Error('Erreur lors de la récupération des résultats');
      }

      const result = await response.json();
      console.log('[InitialAssessmentWidget] ✅ Résultats récupérés:', result);
      setAssessmentResult(result);
      setShowResults(true);
    } catch (err) {
      console.error('[InitialAssessmentWidget] 💥 Erreur lors de la récupération des résultats:', err);
      setError('Erreur lors de la récupération des résultats');
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'completed':
        return <CheckCircle className="w-5 h-5 text-green-500" />;
      case 'in_progress':
        return <Clock className="w-5 h-5 text-yellow-500" />;
      case 'pending':
        return <AlertCircle className="w-5 h-5 text-blue-500" />;
      default:
        return <AlertCircle className="w-5 h-5 text-gray-500" />;
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed':
        return 'bg-green-100 text-green-800 border-green-200';
      case 'in_progress':
        return 'bg-yellow-100 text-yellow-800 border-yellow-200';
      case 'pending':
        return 'bg-blue-100 text-blue-800 border-blue-200';
      default:
        return 'bg-gray-100 text-gray-800 border-gray-200';
    }
  };

  if (loading) {
    return (
      <div className={`card-unified ${className}`}>
        <div className="card-unified-header">
          <div className="flex items-center gap-3">
            <SimpleIconWithBackground name="target" backgroundType="primary" size="lg" />
            <h3 className="text-lg font-semibold">Évaluation Initiale</h3>
          </div>
        </div>
        <div className="card-unified-body">
          <div className="flex items-center justify-center py-8">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
            <span className="ml-3 text-muted">Chargement des évaluations...</span>
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
            <SimpleIconWithBackground name="target" backgroundType="primary" size="lg" />
            <h3 className="text-lg font-semibold">Évaluation Initiale</h3>
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
              <SimpleIconWithBackground name="target" backgroundType="primary" size="lg" />
              <h3 className="text-lg font-semibold">Évaluation Initiale</h3>
            </div>
            <button
              onClick={forceRefresh}
              className="btn-unified btn-unified-secondary flex items-center gap-2"
              title="Recharger les données"
            >
              <RefreshCw className="w-4 h-4" />
              Actualiser
            </button>
          </div>
        </div>
        <div className="card-unified-body">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
            <div className="text-center p-4 bg-blue-50 rounded-lg border border-blue-200">
              <div className="text-2xl font-bold text-blue-600">{pendingAssessments.length}</div>
              <div className="text-sm text-blue-600">En attente</div>
            </div>
            <div className="text-center p-4 bg-yellow-50 rounded-lg border border-yellow-200">
              <div className="text-2xl font-bold text-yellow-600">
                {assessments.filter(a => a.status === 'in_progress').length}
              </div>
              <div className="text-sm text-yellow-600">En cours</div>
            </div>
            <div className="text-center p-4 bg-green-50 rounded-lg border border-green-200">
              <div className="text-2xl font-bold text-green-600">{completedAssessments.length}</div>
              <div className="text-sm text-green-600">Terminées</div>
            </div>
          </div>

          {/* Évaluations en attente */}
          {pendingAssessments.length > 0 && (
            <div className="space-y-4">
              <h4 className="font-semibold text-primary flex items-center gap-2">
                <AlertCircle className="w-4 h-4" />
                Évaluations à passer
              </h4>
              <div className="space-y-3">
                {pendingAssessments.map((assessment) => (
                  <div key={assessment.id} className="p-4 bg-blue-50 rounded-lg border border-blue-200">
                    <div className="flex items-center justify-between">
                      <div className="flex-1">
                        <h5 className="font-semibold text-primary">{assessment.title}</h5>
                        <p className="text-sm text-secondary mb-2">{assessment.description}</p>
                        <div className="flex items-center gap-4 text-xs text-muted">
                          <span className="flex items-center gap-1">
                            <Target className="w-3 h-3" />
                            {assessment.subject}
                          </span>
                          <span className="flex items-center gap-1">
                            <Clock className="w-3 h-3" />
                            {assessment.estimated_time} min
                          </span>
                          <span className={`px-2 py-1 rounded-full text-xs font-medium border ${getStatusColor(assessment.status)}`}>
                            {assessment.status === 'pending' ? 'En attente' : assessment.status}
                          </span>
                        </div>
                      </div>
                      <button
                        onClick={() => startAssessment(assessment)}
                        className="btn-unified btn-unified-primary flex items-center gap-2"
                      >
                        <Play className="w-4 h-4" />
                        Commencer
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Évaluations terminées */}
          {completedAssessments.length > 0 && (
            <div className="space-y-4">
              <h4 className="font-semibold text-primary flex items-center gap-2">
                <CheckCircle className="w-4 h-4" />
                Évaluations terminées
              </h4>
              <div className="space-y-3">
                {completedAssessments.map((assessment) => (
                  <div key={assessment.id} className="p-4 bg-green-50 rounded-lg border border-green-200">
                    <div className="flex items-center justify-between">
                      <div className="flex-1">
                        <h5 className="font-semibold text-primary">{assessment.title}</h5>
                        <p className="text-sm text-secondary mb-2">{assessment.description}</p>
                        <div className="flex items-center gap-4 text-xs text-muted">
                          <span className="flex items-center gap-1">
                            <Target className="w-3 h-3" />
                            {assessment.subject}
                          </span>
                          <span className="flex items-center gap-1">
                            <Award className="w-3 h-3" />
                            Terminé
                          </span>
                        </div>
                      </div>
                      <button
                        onClick={() => viewResults(assessment)}
                        className="btn-unified btn-unified-secondary flex items-center gap-2"
                      >
                        <TrendingUp className="w-4 h-4" />
                        Voir résultats
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Aucune évaluation */}
          {assessments.length === 0 && (
            <div className="text-center py-8">
              <Target className="w-16 h-16 text-gray-300 mx-auto mb-4" />
              <p className="text-lg font-semibold text-gray-600 mb-2">Aucune évaluation disponible</p>
              <p className="text-base text-gray-400">Vos professeurs vous assigneront des évaluations bientôt.</p>
              <button
                onClick={forceRefresh}
                className="btn-unified btn-unified-primary mt-4 flex items-center gap-2 mx-auto"
              >
                <RefreshCw className="w-4 h-4" />
                Actualiser
              </button>
            </div>
          )}
        </div>
      </div>

      {/* Modal des résultats */}
      {showResults && assessmentResult && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 max-w-2xl w-full mx-4 max-h-[80vh] overflow-y-auto">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-xl font-bold text-primary">Résultats de l'évaluation</h3>
              <button
                onClick={() => setShowResults(false)}
                className="text-gray-400 hover:text-gray-600"
              >
                ✕
              </button>
            </div>
            
            <div className="space-y-4">
              <div className="text-center p-4 bg-gradient-to-r from-blue-50 to-green-50 rounded-lg">
                <div className="text-3xl font-bold text-primary mb-2">
                  {assessmentResult.percentage}%
                </div>
                <div className="text-sm text-secondary">
                  Score: {assessmentResult.score}/{assessmentResult.max_score}
                </div>
              </div>

              {assessmentResult.strengths.length > 0 && (
                <div>
                  <h4 className="font-semibold text-green-700 mb-2 flex items-center gap-2">
                    <CheckCircle className="w-4 h-4" />
                    Points forts
                  </h4>
                  <ul className="space-y-1">
                    {assessmentResult.strengths.map((strength, index) => (
                      <li key={index} className="text-sm text-green-600 flex items-center gap-2">
                        <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                        {strength}
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              {assessmentResult.weaknesses.length > 0 && (
                <div>
                  <h4 className="font-semibold text-orange-700 mb-2 flex items-center gap-2">
                    <AlertCircle className="w-4 h-4" />
                    Points à améliorer
                  </h4>
                  <ul className="space-y-1">
                    {assessmentResult.weaknesses.map((weakness, index) => (
                      <li key={index} className="text-sm text-orange-600 flex items-center gap-2">
                        <div className="w-2 h-2 bg-orange-500 rounded-full"></div>
                        {weakness}
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              {assessmentResult.recommendations.length > 0 && (
                <div>
                  <h4 className="font-semibold text-blue-700 mb-2 flex items-center gap-2">
                    <TrendingUp className="w-4 h-4" />
                    Recommandations
                  </h4>
                  <ul className="space-y-1">
                    {assessmentResult.recommendations.map((recommendation, index) => (
                      <li key={index} className="text-sm text-blue-600 flex items-center gap-2">
                        <div className="w-2 h-2 bg-blue-500 rounded-full"></div>
                        {recommendation}
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>

            <div className="mt-6 flex justify-end">
              <button
                onClick={() => setShowResults(false)}
                className="btn-unified btn-unified-primary"
              >
                Fermer
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
