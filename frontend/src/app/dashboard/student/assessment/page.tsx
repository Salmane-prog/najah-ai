'use client';

import React, { useState, useEffect } from 'react';
import Sidebar from '../../../../components/Sidebar';
import { useAuth  } from '../../../../hooks/useAuth';
import SimpleIcon, { SimpleIconWithBackground } from '../../../../components/ui/SimpleIcon';

// Composants français OPTIMISÉS (20 questions)
import FrenchAdaptiveTestOptimized from '@/components/french/FrenchAdaptiveTestOptimized';
import FrenchLearningProfileAdvanced from '@/components/french/FrenchLearningProfileAdvanced';

const AssessmentPage: React.FC = () => {
  const { user, token } = useAuth();
  const [activeTab, setActiveTab] = useState('french-test');
  const [testCompleted, setTestCompleted] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const [testData, setTestData] = useState<any>(null);
  const [profileData, setProfileData] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (user && token) {
      loadUserData();
    }
  }, [user, token]);

  // Fonction de chargement des données avec gestion d'erreur
  const loadUserData = async () => {
    try {
      setIsLoading(true);
      setError(null);
      console.log('🔄 Chargement des données d\'évaluation...');

      // Vérifier le statut du statut du test
      await checkTestStatus();
      
      // Charger le profil si disponible
      await loadProfileData();
      
    } catch (error) {
      console.error('❌ Erreur lors du chargement des données:', error);
      setError(`Erreur lors du chargement: ${error instanceof Error ? error.message : 'Erreur inconnue'}`);
    } finally {
      setIsLoading(false);
    }
  };

  const checkTestStatus = async () => {
    if (!user?.id) return;
    
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/v1/french-optimized/student/start`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ student_id: user.id })
      });

      if (response.ok) {
        const data = await response.json();
        console.log('✅ Statut du test récupéré:', data);
        
        if (data.status === 'completed') {
          setTestCompleted(true);
          setTestData(data);
        } else if (data.status === 'in_progress') {
          setTestData(data);
        }
      } else if (response.status === 400) {
        // Test déjà en cours, essayer de le récupérer
        console.log('ℹ️ Test déjà en cours, récupération...');
        await loadExistingTest();
      } else {
        console.warn(`⚠️ Réponse inattendue du serveur: ${response.status}`);
      }
    } catch (error) {
      console.error('❌ Erreur lors de la vérification du statut:', error);
      setError(`Erreur lors de la vérification du statut: ${error instanceof Error ? error.message : 'Erreur inconnue'}`);
    }
  };

  const loadExistingTest = async () => {
    if (!user?.id) return;
    
    try {
      // Essayer de récupérer le test existant
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/v1/french-optimized/student/${user.id}/profile`, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });

      if (response.ok) {
        const data = await response.json();
        console.log('✅ Test existant récupéré:', data);
        setTestData(data);
      } else {
        console.warn(`⚠️ Impossible de récupérer le test existant: ${response.status}`);
      }
    } catch (error) {
      console.error('❌ Erreur lors de la récupération du test existant:', error);
      setError(`Erreur lors de la récupération du test existant: ${error instanceof Error ? error.message : 'Erreur inconnue'}`);
    }
  };

  const loadProfileData = async () => {
    if (!user?.id) return;
    
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/v1/french-optimized/student/${user.id}/profile`, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });

      if (response.ok) {
        const data = await response.json();
        console.log('✅ Profil récupéré:', data);
        setProfileData(data);
      } else {
        console.warn(`⚠️ Impossible de charger le profil: ${response.status}`);
      }
    } catch (error) {
      console.error('❌ Erreur lors du chargement du profil:', error);
      setError(`Erreur lors du chargement du profil: ${error instanceof Error ? error.message : 'Erreur inconnue'}`);
    }
  };

  const handleTestComplete = () => {
    console.log('🎉 Test terminé, actualisation des données...');
    setTestCompleted(true);
    loadUserData(); // Recharger les données
  };

  const handleRefresh = () => {
    loadUserData();
  };

  // Protection contre l'utilisateur non connecté
  if (!user || !token) {
    return (
      <div className="flex min-h-screen bg-bg-secondary">
        <Sidebar />
        <div className="flex-1 flex items-center justify-center">
          <div className="text-danger text-lg font-bold">Erreur : utilisateur non connecté ou id manquant.</div>
        </div>
      </div>
    );
  }

  // État de chargement
  if (isLoading) {
    return (
      <div className="flex min-h-screen bg-bg-secondary">
        <Sidebar />
        <div className="flex-1 flex items-center justify-center">
          <div className="text-primary animate-pulse text-xl font-bold">Chargement de l'évaluation...</div>
        </div>
      </div>
    );
  }

  return (
    <div className="flex min-h-screen bg-bg-secondary">
      <Sidebar />
      <div className="flex-1 overflow-auto pl-0 md:pl-56">
        <div className="p-6">
          {/* Header personnalisé avec thème harmonisé */}
          <div className="mb-8 flex items-center justify-between flex-wrap gap-4 animate-slide-in-up">
            <div className="animate-slide-in-left">
              <h1 className="text-3xl font-bold text-primary mb-2">
                Évaluation Française <span className="animate-wave inline-block">📚</span>
              </h1>
              <p className="text-secondary">Test de 20 questions pour évaluer votre niveau et générer votre profil personnalisé</p>
            </div>
            <div className="flex items-center gap-4 animate-slide-in-right">
              <div className="w-12 h-12 bg-gradient-to-br from-blue-100 to-purple-100 rounded-lg flex items-center justify-center">
                <SimpleIcon name="book" className="h-6 w-6 text-blue-600" />
              </div>
            </div>
          </div>

          {/* Widget de statistiques unifiées avec thème harmonisé */}
          <div className="mb-8 animate-scale-in">
            <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
              <div className="card-unified animate-fade-in-scale animate-delay-200">
                <div className="card-unified-body">
                  <div className="flex items-center gap-3">
                    <div className="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center">
                      <SimpleIcon name="target" className="h-5 w-5 text-blue-600" />
                    </div>
                    <div>
                      <p className="text-sm text-muted">Niveau Actuel</p>
                      <p className="text-2xl font-bold text-primary">
                        {profileData?.french_level || 'Non évalué'}
                      </p>
                    </div>
                  </div>
                </div>
              </div>

              <div className="card-unified animate-fade-in-scale animate-delay-300">
                <div className="card-unified-body">
                  <div className="flex items-center gap-3">
                    <div className="w-10 h-10 bg-green-100 rounded-lg flex items-center justify-center">
                      <SimpleIcon name="brain" className="h-5 w-5 text-green-600" />
                    </div>
                    <div>
                      <p className="text-sm text-muted">Style d'Apprentissage</p>
                      <p className="text-2xl font-bold text-primary">
                        {profileData?.learning_style ? 
                          profileData.learning_style.charAt(0).toUpperCase() + profileData.learning_style.slice(1) : 
                          'Non déterminé'
                        }
                      </p>
                    </div>
                  </div>
                </div>
              </div>

              <div className="card-unified animate-fade-in-scale animate-delay-400">
                <div className="card-unified-body">
                  <div className="flex items-center gap-3">
                    <div className="w-10 h-10 bg-purple-100 rounded-lg flex items-center justify-center">
                      <SimpleIcon name="clock" className="h-5 w-5 text-purple-600" />
                    </div>
                    <div>
                      <p className="text-sm text-muted">Rythme Préféré</p>
                      <p className="text-2xl font-bold text-primary">
                        {profileData?.preferred_pace ? 
                          profileData.preferred_pace.charAt(0).toUpperCase() + profileData.preferred_pace.slice(1) : 
                          'Non déterminé'
                        }
                      </p>
                    </div>
                  </div>
                </div>
              </div>

              <div className="card-unified animate-fade-in-scale animate-delay-500">
                <div className="card-unified-body">
                  <div className="flex items-center gap-3">
                    <div className="w-10 h-10 bg-orange-100 rounded-lg flex items-center justify-center">
                      <SimpleIcon name="zap" className="h-5 w-5 text-orange-600" />
                    </div>
                    <div>
                      <p className="text-sm text-muted">Statut du Test</p>
                      <p className="text-2xl font-bold text-primary">
                        {testData?.status === 'completed' ? 'Terminé' : 
                         testData?.status === 'in_progress' ? 'En cours' : 'Non commencé'}
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Onglets principaux avec thème harmonisé */}
          <div className="mb-8 animate-fade-in-scale animate-delay-600">
            <div className="flex space-x-1 bg-gray-100 p-1 rounded-lg">
              <button
                onClick={() => setActiveTab('french-test')}
                className={`flex-1 flex items-center justify-center gap-2 px-4 py-2 rounded-md transition-all duration-200 ${
                  activeTab === 'french-test'
                    ? 'bg-white text-primary shadow-sm'
                    : 'text-muted hover:text-primary'
                }`}
              >
                <SimpleIcon name="book" className="h-4 w-4" />
                Test d'Évaluation
              </button>
              <button
                onClick={() => setActiveTab('french-profile')}
                className={`flex-1 flex items-center justify-center gap-2 px-4 py-2 rounded-md transition-all duration-200 ${
                  activeTab === 'french-profile'
                    ? 'bg-white text-primary shadow-sm'
                    : 'text-muted hover:text-primary'
                }`}
              >
                <SimpleIcon name="user" className="h-4 w-4" />
                Mon Profil
              </button>
              <button
                onClick={() => setActiveTab('overview')}
                className={`flex-1 flex items-center justify-center gap-2 px-4 py-2 rounded-md transition-all duration-200 ${
                  activeTab === 'overview'
                    ? 'bg-white text-primary shadow-sm'
                    : 'text-muted hover:text-primary'
                }`}
              >
                <SimpleIcon name="eye" className="h-4 w-4" />
                Vue d'Ensemble
              </button>
            </div>
          </div>

          {/* Tab: Test d'Évaluation */}
          {activeTab === 'french-test' && (
            <div className="space-y-6 animate-fade-in-scale animate-delay-700">
              <div className="card-unified">
                <div className="card-unified-header">
                  <h2 className="text-xl font-bold text-primary mb-0 flex items-center gap-2">
                    <div className="w-8 h-8 bg-blue-100 rounded-lg flex items-center justify-center">
                      <SimpleIcon name="book" className="h-5 w-5 text-blue-600" />
                    </div>
                    Évaluation Française Adaptative
                  </h2>
                </div>
                <div className="card-unified-body">
                  <div className="text-sm text-secondary space-y-2 mb-6">
                    <p>
                       <strong>100+ questions diversifiées</strong> couvrant tous les niveaux (A0-C2)
                    </p>
                    <p>
                       <strong>Progression intelligente</strong> qui s'adapte à vos performances en temps réel
                    </p>
                    <p>
                       <strong>Durée estimée : 20-30 minutes</strong> selon votre niveau et votre rythme
                    </p>
                    <p>
                       <strong>Profil personnalisé</strong> généré par IA après l'évaluation
                    </p>
                  </div>
                  
                  {user ? (
                    <FrenchAdaptiveTestOptimized 
                      studentId={user.id}
                      onTestComplete={handleTestComplete}
                      testData={testData}
                      token={token}
                    />
                  ) : (
                    <div className="text-center py-8">
                      <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto mb-4"></div>
                      <p className="text-gray-600">Chargement de l'utilisateur...</p>
                    </div>
                  )}
                </div>
              </div>
            </div>
          )}

          {/* Tab: Mon Profil */}
          {activeTab === 'french-profile' && (
            <div className="space-y-6 animate-fade-in-scale animate-delay-700">
              {user ? (
                <FrenchLearningProfileAdvanced 
                  studentId={user.id}
                  profileData={profileData}
                  onRefresh={handleRefresh}
                  token={token}
                />
              ) : (
                <div className="card-unified">
                  <div className="card-unified-body">
                    <div className="text-center py-8">
                      <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary mx-auto mb-4"></div>
                      <p className="text-secondary">Chargement de l'utilisateur...</p>
                    </div>
                  </div>
                </div>
              )}
            </div>
          )}

          {/* Tab: Vue d'Ensemble */}
          {activeTab === 'overview' && (
            <div className="space-y-6 animate-fade-in-scale animate-delay-700">
              <div className="card-unified">
                <div className="card-unified-header">
                  <h2 className="text-xl font-bold text-primary mb-0 flex items-center gap-2">
                    <div className="w-8 h-8 bg-purple-100 rounded-lg flex items-center justify-center">
                      <SimpleIcon name="bar-chart" className="h-5 w-5 text-purple-600" />
                    </div>
                    Vue d'Ensemble de l'Apprentissage
                  </h2>
                </div>
                <div className="card-unified-body">
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-6">
                    {/* Statistiques générales */}
                    <div className="bg-gradient-to-br from-blue-50 to-blue-100 rounded-lg p-4 animate-fade-in-scale animate-delay-200">
                      <div className="flex items-center justify-between">
                        <div>
                          <p className="text-sm font-medium text-blue-700">Niveau Actuel</p>
                          <p className="text-2xl font-bold text-blue-900">
                            {profileData?.french_level || 'A1'}
                          </p>
                        </div>
                        <SimpleIcon name="trending-up" className="h-8 w-8 text-blue-600" />
                      </div>
                    </div>

                    <div className="bg-gradient-to-br from-green-50 to-green-100 rounded-lg p-4 animate-fade-in-scale animate-delay-300">
                      <div className="flex items-center justify-between">
                        <div>
                          <p className="text-sm font-medium text-green-700">Questions Répondues</p>
                          <p className="text-2xl font-bold text-green-900">
                            {testData?.progress?.current || 0}
                          </p>
                        </div>
                        <SimpleIcon name="book" className="h-8 w-8 text-green-600" />
                      </div>
                    </div>

                    <div className="bg-gradient-to-br from-purple-50 to-purple-100 rounded-lg p-4 animate-fade-in-scale animate-delay-400">
                      <div className="flex items-center justify-between">
                        <div>
                          <p className="text-sm font-medium text-purple-700">Score Actuel</p>
                          <p className="text-2xl font-bold text-purple-900">
                            {testData?.final_score ? 
                              `${Math.round((testData.final_score / (testData.progress?.current * 10)) * 100)}%` : 
                              '0%'
                            }
                          </p>
                        </div>
                        <SimpleIcon name="brain" className="h-8 w-8 text-purple-700" />
                      </div>
                    </div>
                  </div>

                  {/* Recommandations */}
                  {profileData?.recommendations && (
                    <div className="mb-6 animate-fade-in-scale animate-delay-500">
                      <h3 className="text-lg font-semibold text-primary mb-4">Recommandations IA</h3>
                      <div className="space-y-3">
                        {JSON.parse(profileData.recommendations).slice(0, 3).map((rec: any, index: number) => (
                          <div key={index} className="card-unified">
                            <div className="card-unified-body">
                              <div className="flex items-start gap-3">
                                <div className="h-2 w-2 rounded-full bg-primary mt-2 flex-shrink-0"></div>
                                <div>
                                  <p className="font-medium text-primary">{rec.title}</p>
                                  <p className="text-sm text-secondary">{rec.description}</p>
                                </div>
                              </div>
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Actions rapides */}
                  <div className="animate-fade-in-scale animate-delay-600">
                    <h3 className="text-lg font-semibold text-primary mb-4">Actions Rapides</h3>
                    <div className="flex flex-wrap gap-3">
                      <button 
                        onClick={() => setActiveTab('french-test')}
                        className="btn-unified btn-unified-primary flex items-center gap-2"
                      >
                        <SimpleIcon name="play" className="h-4 w-4" />
                        {testData?.status === 'completed' ? 'Repasser le Test' : 'Continuer le Test'}
                      </button>
                      
                      <button 
                        onClick={() => setActiveTab('french-profile')}
                        className="btn-unified btn-unified-secondary flex items-center gap-2"
                      >
                        <SimpleIcon name="user" className="h-4 w-4" />
                        Voir Mon Profil
                      </button>
                      
                      <button 
                        onClick={handleRefresh}
                        className="btn-unified btn-unified-secondary flex items-center gap-2"
                      >
                        <SimpleIcon name="refresh" className="h-4 w-4" />
                        Actualiser
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Erreur globale */}
          {error && (
            <div className="bg-red-50 border-l-4 border-red-400 p-4 rounded-lg animate-fade-in-scale">
              <div className="flex items-center gap-3">
                <SimpleIcon name="alert-triangle" className="h-5 w-5 text-red-400" />
                <p className="text-red-700 font-medium">{error}</p>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default AssessmentPage; 