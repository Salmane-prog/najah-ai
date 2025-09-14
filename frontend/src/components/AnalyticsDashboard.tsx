'use client';

import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
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
  Server,
  BarChart3,
  Target,
  BookOpen,
  RefreshCw
} from 'lucide-react';
import { analyticsService } from '@/services/analyticsService';
import { testTrackingService } from '@/services/testTrackingService';
import { 
  PerformanceMetrics, 
  RealTimeAnalytics, 
  StudentPerformance, 
 TestPerformance 
} from '@/types/analytics';
import MetricsCustomizer from './MetricsCustomizer';
import SmartAlerts from './SmartAlerts';
import ProgressChart from './analytics/ProgressChart';
import SubjectDistributionChart from './analytics/SubjectDistributionChart';

export default function AnalyticsDashboard() {
  const [activeTab, setActiveTab] = useState('overview');
  const [metrics, setMetrics] = useState<PerformanceMetrics | null>(null);
  const [realTimeData, setRealTimeData] = useState<RealTimeAnalytics | null>(null);
  const [studentPerformances, setStudentPerformances] = useState<StudentPerformance[]>([]);
  const [testPerformances, setTestPerformances] = useState<TestPerformance[]>([]);
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
      
      const [
        performanceMetrics,
        studentData,
        testData
      ] = await Promise.all([
        analyticsService.getPerformanceMetrics(),
        analyticsService.getStudentPerformances(),
        analyticsService.getTestPerformances(),
      ]);

      setMetrics(performanceMetrics);
      setStudentPerformances(studentData);
      setTestPerformances(testData);
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
        <Button onClick={loadAnalytics} className="mt-4">
          Réessayer
        </Button>
      </div>
    );
  }

  if (!metrics) {
    return null;
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-bold">Tableau de Bord Analytics</h2>
        <Button onClick={loadAnalytics} variant="outline">
          <RefreshCw className="w-4 h-4 mr-2" />
          Actualiser
        </Button>
      </div>

      <Tabs value={activeTab} onValueChange={setActiveTab}>
        <TabsList className="grid w-full grid-cols-6">
          <TabsTrigger value="overview">Vue d'ensemble</TabsTrigger>
          <TabsTrigger value="students">Étudiants</TabsTrigger>
          <TabsTrigger value="tests">Tests</TabsTrigger>
          <TabsTrigger value="realtime">Temps Réel</TabsTrigger>
          <TabsTrigger value="customization">Personnalisation</TabsTrigger>
          <TabsTrigger value="alerts">Alertes</TabsTrigger>
        </TabsList>

        <TabsContent value="overview" className="space-y-6">
          {/* Métriques principales */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Score Moyen</CardTitle>
                <TrendingUp className="h-4 w-4 text-green-600" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{metrics.overallAverageScore.toFixed(1)}%</div>
                <p className="text-xs text-muted-foreground">
                  {metrics.totalTestsCompleted} tests complétés
                </p>
              </CardContent>
            </Card>

            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Taux de Completion</CardTitle>
                <CheckCircle className="h-4 w-4 text-green-600" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{metrics.completionRate.toFixed(1)}%</div>
                <p className="text-xs text-muted-foreground">
                  {metrics.totalStudents} étudiants actifs
                </p>
              </CardContent>
            </Card>

            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Tests Difficiles</CardTitle>
                <AlertCircle className="h-4 w-4 text-orange-600" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{metrics.difficultTestsPercentage}%</div>
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
                <div className="text-2xl font-bold">{metrics.totalTestsCompleted}</div>
                <p className="text-xs text-muted-foreground">
                  Tests créés et complétés
                </p>
              </CardContent>
            </Card>
          </div>

          {/* Progrès hebdomadaire */}
          <Card>
            <CardHeader>
              <CardTitle>Progrès Hebdomadaire</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-7 gap-2">
                {metrics.weeklyProgress.map((week, index) => (
                  <div key={index} className="text-center">
                    <div className="text-sm font-medium mb-1">{week.week}</div>
                    <div className="text-lg font-bold text-blue-600">
                      {week.averageScore.toFixed(0)}%
                    </div>
                    <div className="text-xs text-gray-500">
                      {week.testsCompleted} tests
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>

          {/* Tests créés mensuellement */}
          <Card>
            <CardHeader>
              <CardTitle>Tests Créés (Mensuel)</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-7 gap-2">
                {metrics.monthlyStats.map((month, index) => (
                  <div key={index} className="text-center">
                    <div className="text-sm font-medium mb-1">{month.month}</div>
                    <div className="text-lg font-bold text-green-600">
                      {month.testsCreated}
                    </div>
                    <div className="text-xs text-gray-500">
                      {month.testsCompleted} complétés
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="students" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Progrès des Étudiants</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                {studentPerformances.map((student) => (
                  <div key={student.id} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                    <div className="flex items-center space-x-3">
                      {getTrendIcon(student.improvementTrend)}
                      <div>
                        <h4 className="font-medium">{student.name}</h4>
                        <p className="text-sm text-gray-600">{student.email}</p>
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
                      <div className="text-xs text-gray-400">
                        Dernier test: {new Date(student.lastTestDate).toLocaleDateString()}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="tests" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Tests les Plus Performants</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                {testPerformances.map((test) => (
                  <div key={test.id} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                    <div>
                      <h4 className="font-medium">{test.title}</h4>
                      <p className="text-sm text-gray-600">{test.subject}</p>
                      <p className="text-sm text-gray-600">Difficulté: {test.difficultyLevel}/10</p>
                    </div>
                    <div className="text-right">
                      <div className="text-lg font-bold text-green-600">
                        {test.averageScore.toFixed(1)}%
                      </div>
                      <div className="text-sm text-gray-500">
                        {test.participants} participants
                      </div>
                      <div className="text-sm text-gray-500">
                        Completion: {test.completionRate}%
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="realtime" className="space-y-6">
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

                {/* Completions récentes */}
                {realTimeData.recentCompletions.length > 0 && (
                  <div className="mt-4 pt-4 border-t">
                    <h4 className="text-sm font-medium mb-2">Completions Récentes</h4>
                    <div className="space-y-2">
                      {realTimeData.recentCompletions.map((completion, index) => (
                        <div key={index} className="flex items-center justify-between text-sm">
                          <span>{completion.studentName}</span>
                          <span className="font-medium">{completion.score}%</span>
                          <span className="text-gray-500">{completion.testTitle}</span>
                          <span className="text-xs text-gray-400">
                            {new Date(completion.completionTime).toLocaleTimeString()}
                          </span>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </CardContent>
            </Card>
          )}
        </TabsContent>

        <TabsContent value="customization" className="space-y-6">
          <MetricsCustomizer />
        </TabsContent>

        <TabsContent value="alerts" className="space-y-6">
          <SmartAlerts />
        </TabsContent>
      </Tabs>
    </div>
  );
}
