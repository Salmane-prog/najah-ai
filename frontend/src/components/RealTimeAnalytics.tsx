'use client';

import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { 
  TrendingUp, 
  TrendingDown, 
  Minus, 
  Users, 
  Activity,
  Clock,
  CheckCircle,
  AlertCircle,
  Database,
  Server
} from 'lucide-react';
import { analyticsService } from '@/services/analyticsService';
import { 
  PerformanceMetrics, 
  RealTimeAnalytics, 
  StudentPerformance, 
  TestPerformance 
} from '@/types/analytics';
import ProgressChart from './analytics/ProgressChart';
import SubjectDistributionChart from './analytics/SubjectDistributionChart';

export default function RealTimeAnalytics() {
  const [metrics, setMetrics] = useState<PerformanceMetrics | null>(null);
  const [realTimeData, setRealTimeData] = useState<RealTimeAnalytics | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadAnalytics();
    startRealTimeTracking();

    return () => {
      analyticsService.stopRealTimeTracking();
    };
  }, []);

  const loadAnalytics = async () => {
    try {
      setLoading(true);
      setError(null);
      
      console.log('🔄 Chargement des analytics...');
      
      // Récupérer le token d'authentification
      const token = localStorage.getItem('najah_token');
      console.log('🔑 Token récupéré:', token ? 'EXISTE' : 'MANQUANT');
      console.log('🔑 Token complet:', token);
      console.log('🔑 localStorage keys:', Object.keys(localStorage));
      
      if (!token) {
        console.log('🔑 Token manquant, utilisation des données de fallback');
        setError('Token d\'authentification manquant');
        setLoading(false);
        return;
      }

      console.log('✅ Token trouvé, appel des endpoints...');
      
      // Appeler directement nos endpoints qui fonctionnent
      console.log('🚀 Appel des endpoints analytics...');
      
      const [classOverview, studentPerformances, weeklyProgress, monthlyStats] = await Promise.all([
        fetch('http://localhost:8000/api/v1/analytics/class-overview', {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
          },
        }),
        fetch('http://localhost:8000/api/v1/analytics/student-performances', {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
          },
        }),
        fetch('http://localhost:8000/api/v1/analytics/weekly-progress', {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
          },
        }),
        fetch('http://localhost:8000/api/v1/analytics/monthly-stats', {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
          },
        })
      ]);

      console.log('📡 Réponses des endpoints reçues:');
      console.log('  - classOverview:', classOverview.status, classOverview.ok);
      console.log('  - studentPerformances:', studentPerformances.status, studentPerformances.ok);
      console.log('  - weeklyProgress:', weeklyProgress.status, weeklyProgress.ok);
      console.log('  - monthlyStats:', monthlyStats.status, monthlyStats.ok);

      // Vérifier que tous les endpoints fonctionnent
      if (!classOverview.ok || !studentPerformances.ok || !weeklyProgress.ok || !monthlyStats.ok) {
        console.log(`⚠️ Certains endpoints ne fonctionnent pas, utilisation des données de fallback`);
        setError('Erreur lors de la récupération des données');
        setLoading(false);
        return;
      }

      console.log('📥 Récupération des données JSON...');
      const [overviewData, studentsData, weeklyData, monthlyData] = await Promise.all([
        classOverview.json(),
        studentPerformances.json(),
        weeklyProgress.json(),
        monthlyStats.json()
      ]);

      console.log('📊 Données reçues:');
      console.log('  - overviewData:', overviewData);
      console.log('  - studentsData:', studentsData);
      console.log('  - weeklyData:', weeklyData);
      console.log('  - monthlyData:', monthlyData);

      // Construire l'objet PerformanceMetrics avec les vraies données
      const realMetrics: PerformanceMetrics = {
        overallAverageScore: overviewData.averageScore || 0,
        totalTestsCompleted: studentsData.length * 2 || 0, // Estimation
        completionRate: 85, // Valeur par défaut
        totalStudents: overviewData.activeStudents || 0,
        difficultTestsPercentage: 15, // Valeur par défaut
        topPerformingStudents: studentsData.slice(0, 3).map((student: any) => ({
          id: student.id || Math.random(),
          name: student.name || 'Étudiant',
          score: student.averageScore || 0,
          trend: 'up' as const
        })),
        topPerformingTests: [], // À implémenter plus tard
        weeklyProgress: weeklyData || [],
        monthlyStats: monthlyData || []
      };

      console.log('📊 Métriques de performance récupérées depuis les vrais endpoints:', realMetrics);
      console.log('📈 weeklyProgress:', realMetrics.weeklyProgress);
      console.log('📊 monthlyStats:', realMetrics.monthlyStats);
      
      setMetrics(realMetrics);
    } catch (err) {
      console.error('❌ Erreur lors du chargement des analytics:', err);
      setError('Erreur lors du chargement des données');
    } finally {
      setLoading(false);
    }
  };

  const startRealTimeTracking = () => {
    analyticsService.startRealTimeTracking();
    
    const unsubscribe = analyticsService.subscribe((data) => {
      setRealTimeData(data);
    });

    return unsubscribe;
  };

  const getTrendIcon = (trend: 'up' | 'down' | 'stable') => {
    switch (trend) {
      case 'up':
        return <TrendingUp className="w-4 h-4 text-green-600" />;
      case 'down':
        return <TrendingDown className="w-4 h-4 text-red-600" />;
      default:
        return <Minus className="w-4 h-4 text-gray-600" />;
    }
  };

  const getSystemHealthColor = (status: string) => {
    switch (status) {
      case 'online':
      case 'healthy':
        return 'text-green-600';
      case 'degraded':
      case 'slow':
        return 'text-yellow-600';
      case 'offline':
      case 'error':
        return 'text-red-600';
      default:
        return 'text-gray-600';
    }
  };

  if (loading) {
    return (
      <div className="space-y-6">
        <div className="animate-pulse">
          <div className="h-8 bg-gray-200 rounded w-1/4 mb-4"></div>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            {[...Array(4)].map((_, i) => (
              <div key={i} className="h-24 bg-gray-200 rounded"></div>
            ))}
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="text-center py-8">
        <AlertCircle className="w-12 h-12 text-red-500 mx-auto mb-4" />
        <p className="text-red-600">{error}</p>
        <button 
          onClick={loadAnalytics}
          className="mt-4 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
        >
          Réessayer
        </button>
      </div>
    );
  }

  if (!metrics) {
    return null;
  }

  return (
    <div className="space-y-6">
      {/* Métriques principales */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Score Moyen</CardTitle>
            <TrendingUp className="h-4 w-4 text-green-600" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{metrics?.overallAverageScore?.toFixed(1) || '0'}%</div>
            <p className="text-xs text-muted-foreground">
              {metrics?.totalTestsCompleted || 0} tests complétés
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Taux de Completion</CardTitle>
            <CheckCircle className="h-4 w-4 text-green-600" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{metrics?.completionRate?.toFixed(1) || '0'}%</div>
            <p className="text-xs text-muted-foreground">
              {metrics?.totalStudents || 0} étudiants actifs
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Tests Difficiles</CardTitle>
            <AlertCircle className="h-4 w-4 text-orange-600" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{metrics?.difficultTestsPercentage || 0}%</div>
            <p className="text-xs text-muted-foreground">
              Nécessitent attention
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Tests</CardTitle>
            <Activity className="h-4 w-4 text-blue-600" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{metrics?.totalTestsCompleted || 0}</div>
            <p className="text-xs text-muted-foreground">
              Tests créés et complétés
            </p>
          </CardContent>
        </Card>
      </div>

      {/* Données en temps réel */}
      {realTimeData && (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Activity className="w-5 h-5 text-green-600" />
              Données en Temps Réel
              <Badge variant="secondary" className="ml-2">
                Live
              </Badge>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="flex items-center space-x-2">
                <Users className="w-4 h-4 text-blue-600" />
                <span className="text-sm font-medium">Étudiants en ligne:</span>
                <span className="text-lg font-bold">{realTimeData.studentsOnline}</span>
              </div>
              
              <div className="flex items-center space-x-2">
                <Clock className="w-4 h-4 text-orange-600" />
                <span className="text-sm font-medium">Tests en cours:</span>
                <span className="text-lg font-bold">{realTimeData.testsInProgress}</span>
              </div>
              
              <div className="flex items-center space-x-2">
                <CheckCircle className="w-4 h-4 text-green-600" />
                <span className="text-sm font-medium">Tests actifs:</span>
                <span className="text-lg font-bold">{realTimeData.currentActiveTests}</span>
              </div>
            </div>

            {/* Santé du système */}
            <div className="mt-4 pt-4 border-t">
              <h4 className="text-sm font-medium mb-2">État du Système</h4>
              <div className="flex items-center space-x-4">
                <div className="flex items-center space-x-2">
                  <Server className={`w-4 h-4 ${getSystemHealthColor(realTimeData.systemHealth.backendStatus)}`} />
                  <span className="text-sm">Backend: {realTimeData.systemHealth.backendStatus}</span>
                </div>
                <div className="flex items-center space-x-2">
                  <Database className={`w-4 h-4 ${getSystemHealthColor(realTimeData.systemHealth.databaseStatus)}`} />
                  <span className="text-sm">Base: {realTimeData.systemHealth.databaseStatus}</span>
                </div>
                <div className="text-xs text-gray-500">
                  Dernière mise à jour: {new Date(realTimeData.systemHealth.lastUpdate).toLocaleTimeString()}
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Progrès hebdomadaire */}
      <Card>
        <CardHeader>
          <CardTitle>Progrès Hebdomadaire</CardTitle>
        </CardHeader>
        <CardContent>
          <ProgressChart 
            data={metrics?.weeklyProgress || []} 
            title="Progression des Scores"
            type="line"
          />
        </CardContent>
      </Card>

      {/* Tests créés mensuellement */}
      <Card>
        <CardHeader>
          <CardTitle>Tests Créés (Mensuel)</CardTitle>
        </CardHeader>
        <CardContent>
          <SubjectDistributionChart 
            data={metrics?.monthlyStats || []} 
          />
        </CardContent>
      </Card>

      {/* Tests les plus performants */}
      <Card>
        <CardHeader>
          <CardTitle>Tests les Plus Performants</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-3">
            {metrics?.topPerformingTests?.map((test) => (
              <div key={test.id} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                <div>
                  <h4 className="font-medium">{test.title}</h4>
                  <p className="text-sm text-gray-600">{test.subject}</p>
                </div>
                <div className="text-right">
                  <div className="text-lg font-bold text-green-600">
                    {test.averageScore.toFixed(1)}%
                  </div>
                  <div className="text-sm text-gray-500">
                    {test.participants} participants
                  </div>
                </div>
              </div>
            )) || (
              <div className="text-center py-4 text-gray-500">
                Aucun test disponible
              </div>
            )}
          </div>
        </CardContent>
      </Card>

      {/* Progrès des étudiants */}
      <Card>
        <CardHeader>
          <CardTitle>Progrès des Étudiants</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-3">
            {metrics?.topPerformingStudents?.map((student) => (
              <div key={student.id} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                <div className="flex items-center space-x-3">
                  {getTrendIcon(student.improvementTrend)}
                  <div>
                    <h4 className="font-medium">{student.name}</h4>
                    <p className="text-sm text-gray-600">{student.testsCompleted} tests complétés</p>
                  </div>
                </div>
                <div className="text-right">
                  <div className="text-lg font-bold text-blue-600">
                    {student.progressPercentage}%
                  </div>
                  <div className="text-sm text-gray-500">
                    Score moy: {student.averageScore}%
                  </div>
                </div>
              </div>
            )) || (
              <div className="text-center py-4 text-gray-500">
                Aucun étudiant disponible
              </div>
            )}
          </div>
        </CardContent>
      </Card>
    </div>
  );
}

