'use client';

import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Progress } from '@/components/ui/progress';
import Sidebar from '../../../../components/Sidebar';
import { useAuth  } from '../../../../hooks/useAuth';
import { 
  BookOpen, 
  Brain, 
  Target, 
  TrendingUp, 
  CheckCircle,
  AlertTriangle,
  Loader2,
  Play,
  BarChart3,
  User,
  Eye,
  Award,
  Lightbulb,
  Clock,
  Zap,
  RefreshCw,
  Star,
  Activity
} from 'lucide-react';

// Composants français optimisés
import FrenchAdaptiveTestOptimized from '@/components/french/FrenchAdaptiveTestOptimized';
import FrenchLearningProfileAdvanced from '@/components/french/FrenchLearningProfileAdvanced';

const AssessmentPageOptimized: React.FC = () => {
  const { user, token } = useAuth();
  const [activeTab, setActiveTab] = useState('french-test');
  const [testCompleted, setTestCompleted] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const [testData, setTestData] = useState<any>(null);
  const [profileData, setProfileData] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);
  const [availableQuestions, setAvailableQuestions] = useState<any>(null);

  const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
  const OPTIMIZED_API_PATH = '/api/v1/french-optimized';

  useEffect(() => {
    if (user && token) {
      loadUserData();
    }
  }, [user, token]);

  const loadUserData = async () => {
    try {
      setIsLoading(true);
      setError(null);
      console.log('🔄 Chargement des données d\'évaluation optimisées...');

      // Charger les données en parallèle pour améliorer la performance
      await Promise.all([
        checkTestStatus(),
        loadProfileData(),
        checkAvailableQuestions()
      ]);
      
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
      const response = await fetch(`${API_BASE}${OPTIMIZED_API_PATH}/student/${user.id}/test-status`, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });

      if (response.ok) {
        const data = await response.json();
        console.log('✅ Statut du test optimisé récupéré:', data);
        
        if (data.success && data.test_status !== 'not_started') {
          const testStatus = data.test_status;
          setTestData({
            test_id: testStatus.id,
            status: testStatus.status,
            progress: {
              current: testStatus.current_question || 1,
              total: 20,
              difficulty: testStatus.current_difficulty || 'medium',
              level_progression: 'A1',
              current_level: 'A1'
            }
          });
          
          if (testStatus.status === 'completed') {
            setTestCompleted(true);
          }
        }
      } else {
        console.warn(`⚠️ Réponse inattendue du serveur: ${response.status}`);
      }
    } catch (error) {
      console.error('❌ Erreur lors de la vérification du statut:', error);
      // Ne pas lever l'erreur pour ne pas bloquer le chargement
    }
  };

  const loadProfileData = async () => {
    if (!user?.id) return;
    
    try {
      const response = await fetch(`${API_BASE}${OPTIMIZED_API_PATH}/student/${user.id}/profile`, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });

      if (response.ok) {
        const data = await response.json();
        console.log('✅ Profil optimisé récupéré:', data);
        
        if (data.success && data.profile) {
          setProfileData(data.profile);
        }
      } else {
        console.warn(`⚠️ Impossible de charger le profil: ${response.status}`);
      }
    } catch (error) {
      console.error('❌ Erreur lors du chargement du profil:', error);
    }
  };

  const checkAvailableQuestions = async () => {
    try {
      const response = await fetch(`${API_BASE}${OPTIMIZED_API_PATH}/questions/available`, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });

      if (response.ok) {
        const data = await response.json();
        console.log('✅ Questions disponibles:', data);
        
        if (data.success) {
          setAvailableQuestions(data.counts);
        }
      }
    } catch (error) {
      console.error('❌ Erreur lors de la vérification des questions:', error);
    }
  };

  const handleTestComplete = () => {
    console.log('🎉 Test optimisé terminé, actualisation des données...');
    setTestCompleted(true);
    loadUserData();
  };

  const handleRefresh = () => {
    loadUserData();
  };

  // Gérer le changement d'onglet depuis le composant de test
  useEffect(() => {
    const handleSwitchToProfile = () => {
      setActiveTab('french-profile');
    };

    window.addEventListener('switchToProfile', handleSwitchToProfile);
    return () => {
      window.removeEventListener('switchToProfile', handleSwitchToProfile);
    };
  }, []);

  // Protection contre l'utilisateur non connecté
  if (!user || !token) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <Loader2 className="h-12 w-12 animate-spin mx-auto mb-4 text-gray-400" />
          <h2 className="text-xl font-semibold text-gray-900 mb-2">Chargement...</h2>
          <p className="text-gray-600">Vérification de votre connexion</p>
        </div>
      </div>
    );
  }

  // État de chargement
  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50">
        <Sidebar />
        <div className="ml-64 p-8">
          <div className="flex items-center justify-center py-12">
            <div className="text-center">
              <Loader2 className="h-12 w-12 animate-spin mx-auto mb-4 text-blue-600" />
              <p className="text-lg font-medium text-gray-900">Chargement de l'évaluation optimisée...</p>
              <p className="text-gray-600">Préparation de votre espace d'apprentissage français intelligent</p>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Sidebar />
      <div className="ml-64 p-8">
        {/* En-tête de la page optimisée */}
        <div className="mb-8">
          <div className="flex items-center gap-3 mb-4">
            <div className="w-12 h-12 bg-gradient-to-br from-blue-100 to-purple-100 rounded-lg flex items-center justify-center">
              <Brain className="h-6 w-6 text-blue-600" />
            </div>
            <div>
              <h1 className="text-3xl font-bold text-gray-900">Évaluation Française IA</h1>
              <p className="text-gray-600">Test intelligent de 20 questions avec profil personnalisé générés par IA</p>
            </div>
          </div>

          {/* Statistiques système */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div className="bg-white rounded-lg p-4 border border-gray-200">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center">
                  <Target className="h-5 w-5 text-blue-600" />
                </div>
                <div>
                  <p className="text-sm text-gray-600">Niveau Actuel</p>
                  <p className="font-semibold text-gray-900">
                    {profileData?.french_level || 'Non évalué'}
                  </p>
                </div>
              </div>
            </div>

            <div className="bg-white rounded-lg p-4 border border-gray-200">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 bg-green-100 rounded-lg flex items-center justify-center">
                  <Brain className="h-5 w-5 text-green-600" />
                </div>
                <div>
                  <p className="text-sm text-gray-600">Style d'Apprentissage</p>
                  <p className="font-semibold text-gray-900 capitalize">
                    {profileData?.learning_style || 'Non déterminé'}
                  </p>
                </div>
              </div>
            </div>

            <div className="bg-white rounded-lg p-4 border border-gray-200">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 bg-purple-100 rounded-lg flex items-center justify-center">
                  <Zap className="h-5 w-5 text-purple-600" />
                </div>
                <div>
                  <p className="text-sm text-gray-600">Questions Disponibles</p>
                  <p className="font-semibold text-gray-900">
                    {availableQuestions?.total || 'Chargement...'}
                  </p>
                </div>
              </div>
            </div>

            <div className="bg-white rounded-lg p-4 border border-gray-200">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 bg-orange-100 rounded-lg flex items-center justify-center">
                  <Activity className="h-5 w-5 text-orange-600" />
                </div>
                <div>
                  <p className="text-sm text-gray-600">Statut du Test</p>
                  <p className="font-semibold text-gray-900">
                    {testData?.status === 'completed' ? 'Terminé' : 
                     testData?.status === 'in_progress' ? 'En cours' : 'Disponible'}
                  </p>
                </div>
              </div>
            </div>
          </div>

          {/* Informations sur les questions disponibles */}
          {availableQuestions && (
            <div className="mt-4 p-4 bg-blue-50 rounded-lg border border-blue-200">
              <div className="flex items-center gap-2 mb-2">
                <CheckCircle className="h-5 w-5 text-blue-600" />
                <span className="font-medium text-blue-900">Système Intelligent Actif</span>
              </div>
              <p className="text-sm text-blue-700">
                {availableQuestions.total} questions françaises disponibles • 
                Sélection automatique garantissant 20 questions uniques • 
                Répartition optimale par difficulté
              </p>
            </div>
          )}
        </div>

        {/* Onglets principaux */}
        <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-6">
          <TabsList className="grid w-full grid-cols-3">
            <TabsTrigger value="french-test" className="flex items-center gap-2">
              <BookOpen className="h-4 w-4" />
              Test d'Évaluation IA
            </TabsTrigger>
            <TabsTrigger value="french-profile" className="flex items-center gap-2">
              <User className="h-4 w-4" />
              Profil Avancé
            </TabsTrigger>
            <TabsTrigger value="overview" className="flex items-center gap-2">
              <BarChart3 className="h-4 w-4" />
              Vue d'Ensemble
            </TabsTrigger>
          </TabsList>

          {/* Tab: Test d'Évaluation Optimisé */}
          <TabsContent value="french-test" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-3 text-xl">
                  <Brain className="h-6 w-6 text-blue-600" />
                  Évaluation Française Intelligente
                </CardTitle>
                <div className="text-sm text-gray-600 space-y-2">
                  <p>
                    🎯 <strong>20 questions exactes</strong> avec répartition équilibrée (7 facile + 6 moyen + 7 difficile)
                  </p>
                  <p>
                    🧠 <strong>Sélection intelligente</strong> depuis votre banque existante ({availableQuestions?.total || 'N/A'} questions disponibles)
                  </p>
                  <p>
                    ⏱️ <strong>Durée optimisée : 15-20 minutes</strong> pour un test complet et précis
                  </p>
                  <p>
                    🤖 <strong>Profil IA personnalisé</strong> généré automatiquement après les 20 questions
                  </p>
                </div>
              </CardHeader>
              <CardContent>
                {user ? (
                  <FrenchAdaptiveTestOptimized 
                    studentId={user.id}
                    onTestComplete={handleTestComplete}
                    testData={testData}
                    token={token}
                  />
                ) : (
                  <div className="text-center py-8">
                    <Loader2 className="h-8 w-8 animate-spin mx-auto mb-4 text-gray-400" />
                    <p className="text-gray-600">Chargement de l'utilisateur...</p>
                  </div>
                )}
              </CardContent>
            </Card>
          </TabsContent>

          {/* Tab: Profil Avancé */}
          <TabsContent value="french-profile" className="space-y-6">
            {user ? (
              <FrenchLearningProfileAdvanced 
                studentId={user.id}
                profileData={profileData}
                onRefresh={handleRefresh}
                token={token}
              />
            ) : (
              <div className="text-center py-8">
                <Loader2 className="h-8 w-8 animate-spin mx-auto mb-4 text-gray-400" />
                <p className="text-gray-600">Chargement de l'utilisateur...</p>
              </div>
            )}
          </TabsContent>

          {/* Tab: Vue d'Ensemble Optimisée */}
          <TabsContent value="overview" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-3 text-xl">
                  <BarChart3 className="h-6 w-6 text-purple-600" />
                  Dashboard d'Apprentissage Intelligent
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                  {/* Statistiques de performance */}
                  <div className="bg-gradient-to-br from-blue-50 to-blue-100 rounded-lg p-4">
                    <div className="flex items-center justify-between">
                      <div>
                        <p className="text-sm font-medium text-blue-700">Niveau Détecté</p>
                        <p className="text-2xl font-bold text-blue-900">
                          {profileData?.french_level || 'A1'}
                        </p>
                      </div>
                      <Target className="h-8 w-8 text-blue-600" />
                    </div>
                    <p className="text-xs text-blue-600 mt-2">Évaluation IA basée sur 20 questions</p>
                  </div>

                  <div className="bg-gradient-to-br from-green-50 to-green-100 rounded-lg p-4">
                    <div className="flex items-center justify-between">
                      <div>
                        <p className="text-sm font-medium text-green-700">Questions Analysées</p>
                        <p className="text-2xl font-bold text-green-900">
                          {testData?.progress?.current || '0'}/20
                        </p>
                      </div>
                      <BookOpen className="h-8 w-8 text-green-600" />
                    </div>
                    <p className="text-xs text-green-600 mt-2">Progression garantie sur 20 questions</p>
                  </div>

                  <div className="bg-gradient-to-br from-purple-50 to-purple-100 rounded-lg p-4">
                    <div className="flex items-center justify-between">
                      <div>
                        <p className="text-sm font-medium text-purple-700">Système IA</p>
                        <p className="text-2xl font-bold text-purple-900">Actif</p>
                      </div>
                      <Brain className="h-8 w-8 text-purple-700" />
                    </div>
                    <p className="text-xs text-purple-600 mt-2">Sélection et analyse intelligente</p>
                  </div>
                </div>

                {/* Fonctionnalités du système */}
                <div className="mt-8">
                  <h3 className="text-lg font-semibold text-gray-900 mb-4">Fonctionnalités Intelligentes</h3>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div className="bg-white border border-gray-200 rounded-lg p-4">
                      <div className="flex items-start gap-3">
                        <div className="w-8 h-8 bg-blue-100 rounded-lg flex items-center justify-center">
                          <Zap className="h-4 w-4 text-blue-600" />
                        </div>
                        <div>
                          <h4 className="font-medium text-gray-900">Sélection Adaptative</h4>
                          <p className="text-sm text-gray-600">Questions choisies intelligemment depuis votre banque existante</p>
                        </div>
                      </div>
                    </div>

                    <div className="bg-white border border-gray-200 rounded-lg p-4">
                      <div className="flex items-start gap-3">
                        <div className="w-8 h-8 bg-green-100 rounded-lg flex items-center justify-center">
                          <Target className="h-4 w-4 text-green-600" />
                        </div>
                        <div>
                          <h4 className="font-medium text-gray-900">Répartition Équilibrée</h4>
                          <p className="text-sm text-gray-600">7 facile + 6 moyen + 7 difficile = 20 questions exactes</p>
                        </div>
                      </div>
                    </div>

                    <div className="bg-white border border-gray-200 rounded-lg p-4">
                      <div className="flex items-start gap-3">
                        <div className="w-8 h-8 bg-purple-100 rounded-lg flex items-center justify-center">
                          <Brain className="h-4 w-4 text-purple-600" />
                        </div>
                        <div>
                          <h4 className="font-medium text-gray-900">Profil IA Avancé</h4>
                          <p className="text-sm text-gray-600">Analyse cognitive et recommandations personnalisées</p>
                        </div>
                      </div>
                    </div>

                    <div className="bg-white border border-gray-200 rounded-lg p-4">
                      <div className="flex items-start gap-3">
                        <div className="w-8 h-8 bg-orange-100 rounded-lg flex items-center justify-center">
                          <RefreshCw className="h-4 w-4 text-orange-600" />
                        </div>
                        <div>
                          <h4 className="font-medium text-gray-900">Anti-Répétition</h4>
                          <p className="text-sm text-gray-600">Système garantissant des questions uniques à chaque test</p>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>

                {/* Actions rapides optimisées */}
                <div className="mt-8">
                  <h3 className="text-lg font-semibold text-gray-900 mb-4">Actions Rapides</h3>
                  <div className="flex flex-wrap gap-3">
                    <Button 
                      onClick={() => setActiveTab('french-test')}
                      variant="outline"
                      className="flex items-center gap-2"
                    >
                      <Play className="h-4 w-4" />
                      {testData?.status === 'completed' ? 'Nouveau Test' : 'Commencer le Test IA'}
                    </Button>
                    
                    <Button 
                      onClick={() => setActiveTab('french-profile')}
                      variant="outline"
                      className="flex items-center gap-2"
                    >
                      <User className="h-4 w-4" />
                      Profil Avancé
                    </Button>
                    
                    <Button 
                      onClick={handleRefresh}
                      variant="outline"
                      className="flex items-center gap-2"
                    >
                      <RefreshCw className="h-4 w-4" />
                      Actualiser
                    </Button>
                  </div>
                </div>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>

        {/* Erreur globale */}
        {error && (
          <Alert variant="destructive">
            <AlertTriangle className="h-4 w-4" />
            <AlertDescription>{error}</AlertDescription>
          </Alert>
        )}
      </div>
    </div>
  );
};

export default AssessmentPageOptimized;

