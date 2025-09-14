'use client';

import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Progress } from '@/components/ui/progress';
import { 
  BarChart3, 
  Users, 
  CheckCircle, 
  Clock, 
  TrendingUp, 
  Activity,
  BookOpen,
  FileText,
  Target,
  Award
} from 'lucide-react';
import realStudentAnalyticsService, {
  AdaptiveTestsAnalytics,
  FormativeEvaluationsAnalytics,
  RealTimeMonitoring,
  GlobalStudentAnalytics
} from '../../../../services/realStudentAnalyticsService';

export default function TestRealAnalyticsPage() {
  const [adaptiveTestsData, setAdaptiveTestsData] = useState<AdaptiveTestsAnalytics | null>(null);
  const [formativeEvaluationsData, setFormativeEvaluationsData] = useState<FormativeEvaluationsAnalytics | null>(null);
  const [realTimeData, setRealTimeData] = useState<RealTimeMonitoring | null>(null);
  const [globalAnalytics, setGlobalAnalytics] = useState<GlobalStudentAnalytics | null>(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('overview');

  useEffect(() => {
    loadAllData();
  }, []);

  const loadAllData = async () => {
    setLoading(true);
    try {
      const [adaptiveData, formativeData, realTimeData, globalData] = await Promise.all([
        realStudentAnalyticsService.getAdaptiveTestsOverview(),
        realStudentAnalyticsService.getFormativeEvaluationsOverview(),
        realStudentAnalyticsService.getRealTimeMonitoring(),
        realStudentAnalyticsService.getGlobalStudentAnalytics()
      ]);

      setAdaptiveTestsData(adaptiveData);
      setFormativeEvaluationsData(formativeData);
      setRealTimeData(realTimeData);
      setGlobalAnalytics(globalData);
    } catch (error) {
      console.error('Erreur lors du chargement des données:', error);
    } finally {
      setLoading(false);
    }
  };

  const refreshData = () => {
    loadAllData();
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-lg">Chargement des analytics réelles...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="container mx-auto p-6 space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">🧪 Test des Analytics Réelles</h1>
          <p className="text-gray-600 mt-2">
            Vérification de la connexion aux vraies données des étudiants
          </p>
        </div>
        <Button onClick={refreshData} variant="outline">
          🔄 Actualiser
        </Button>
      </div>

      <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-6">
        <TabsList className="grid w-full grid-cols-4">
          <TabsTrigger value="overview">Vue d'ensemble</TabsTrigger>
          <TabsTrigger value="adaptive">Tests Adaptatifs</TabsTrigger>
          <TabsTrigger value="formative">Évaluations Formatives</TabsTrigger>
          <TabsTrigger value="monitoring">Monitoring Temps Réel</TabsTrigger>
        </TabsList>

        {/* VUE D'ENSEMBLE */}
        <TabsContent value="overview" className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {/* Tests Adaptatifs */}
            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Tests Adaptatifs</CardTitle>
                <BookOpen className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">
                  {adaptiveTestsData?.overview.total_tests || 0}
                </div>
                <p className="text-xs text-muted-foreground">
                  {adaptiveTestsData?.overview.total_assigned || 0} assignés, {adaptiveTestsData?.overview.total_completed || 0} terminés
                </p>
                <Progress 
                  value={adaptiveTestsData?.overview.completion_rate || 0} 
                  className="mt-2" 
                />
              </CardContent>
            </Card>

            {/* Évaluations Formatives */}
            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Évaluations Formatives</CardTitle>
                <FileText className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">
                  {formativeEvaluationsData?.overview.total_evaluations || 0}
                </div>
                <p className="text-xs text-muted-foreground">
                  {formativeEvaluationsData?.overview.total_submitted || 0} soumises, {formativeEvaluationsData?.overview.total_graded || 0} notées
                </p>
                <Progress 
                  value={formativeEvaluationsData?.overview.submission_rate || 0} 
                  className="mt-2" 
                />
              </CardContent>
            </Card>

            {/* Tests Actifs */}
            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Tests Actifs</CardTitle>
                <Activity className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">
                  {realTimeData?.real_time_stats.active_adaptive_tests || 0}
                </div>
                <p className="text-xs text-muted-foreground">
                  En cours d'exécution
                </p>
              </CardContent>
            </Card>

            {/* Notes en Attente */}
            <Card>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">Notes en Attente</CardTitle>
                <Clock className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">
                  {realTimeData?.real_time_stats.pending_grades || 0}
                </div>
                <p className="text-xs text-muted-foreground">
                  À noter
                </p>
              </CardContent>
            </Card>
          </div>

          {/* Statistiques Globales */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <BarChart3 className="h-5 w-5" />
                Statistiques Globales des Étudiants
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <h4 className="font-semibold mb-3">Tests Adaptatifs</h4>
                  <div className="space-y-2">
                    {globalAnalytics?.student_analytics.slice(0, 3).map((student) => (
                      <div key={student.student_id} className="flex items-center justify-between p-2 bg-gray-50 rounded">
                        <span className="text-sm">{student.name}</span>
                        <div className="flex items-center gap-2">
                          <Badge variant="outline">
                            {student.adaptive_tests.completion_rate.toFixed(1)}%
                          </Badge>
                          <span className="text-sm font-medium">
                            {student.adaptive_tests.average_score}/100
                          </span>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
                <div>
                  <h4 className="font-semibold mb-3">Évaluations Formatives</h4>
                  <div className="space-y-2">
                    {globalAnalytics?.student_analytics.slice(0, 3).map((student) => (
                      <div key={student.student_id} className="flex items-center justify-between p-2 bg-gray-50 rounded">
                        <span className="text-sm">{student.name}</span>
                        <div className="flex items-center gap-2">
                          <Badge variant="outline">
                            {student.formative_evaluations.submission_rate.toFixed(1)}%
                          </Badge>
                          <span className="text-sm font-medium">
                            {student.formative_evaluations.average_score}/100
                          </span>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* TESTS ADAPTATIFS */}
        <TabsContent value="adaptive" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <BookOpen className="h-5 w-5" />
                Tests Adaptatifs - Analytics Réelles
              </CardTitle>
              <CardDescription>
                Données en temps réel des tests adaptatifs assignés aux étudiants
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {adaptiveTestsData?.tests.map((test) => (
                  <div key={test.id} className="border rounded-lg p-4">
                    <div className="flex items-center justify-between mb-3">
                      <h4 className="font-semibold">{test.title}</h4>
                      <Badge variant="outline">{test.subject}</Badge>
                    </div>
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
                      <div>
                        <span className="text-gray-600">Questions:</span>
                        <div className="font-medium">{test.total_questions}</div>
                      </div>
                      <div>
                        <span className="text-gray-600">Durée:</span>
                        <div className="font-medium">{test.estimated_duration} min</div>
                      </div>
                      <div>
                        <span className="text-gray-600">Étudiants:</span>
                        <div className="font-medium">{test.assigned_students}</div>
                      </div>
                      <div>
                        <span className="text-gray-600">Moyenne:</span>
                        <div className="font-medium">{test.average_score}/100</div>
                      </div>
                    </div>
                    <div className="mt-3">
                      <div className="flex items-center justify-between text-sm mb-1">
                        <span>Progression</span>
                        <span>{test.completed_tests}/{test.assigned_students}</span>
                      </div>
                      <Progress 
                        value={(test.completed_tests / test.assigned_students) * 100} 
                        className="h-2" 
                      />
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* ÉVALUATIONS FORMATIVES */}
        <TabsContent value="formative" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <FileText className="h-5 w-5" />
                Évaluations Formatives - Analytics Réelles
              </CardTitle>
              <CardDescription>
                Données en temps réel des évaluations formatives et des soumissions des étudiants
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {formativeEvaluationsData?.evaluations.map((evaluation) => (
                  <div key={evaluation.id} className="border rounded-lg p-4">
                    <div className="flex items-center justify-between mb-3">
                      <h4 className="font-semibold">{evaluation.title}</h4>
                      <div className="flex gap-2">
                        <Badge variant="outline">{evaluation.subject}</Badge>
                        <Badge variant="secondary">{evaluation.evaluation_type}</Badge>
                      </div>
                    </div>
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
                      <div>
                        <span className="text-gray-600">Points:</span>
                        <div className="font-medium">{evaluation.total_points}</div>
                      </div>
                      <div>
                        <span className="text-gray-600">Date limite:</span>
                        <div className="font-medium">{evaluation.due_date}</div>
                      </div>
                      <div>
                        <span className="text-gray-600">Soumises:</span>
                        <div className="font-medium">{evaluation.submitted_assignments}/{evaluation.assigned_students}</div>
                      </div>
                      <div>
                        <span className="text-gray-600">Moyenne:</span>
                        <div className="font-medium">{evaluation.average_score}/100</div>
                      </div>
                    </div>
                    <div className="mt-3">
                      <div className="flex items-center justify-between text-sm mb-1">
                        <span>Taux de soumission</span>
                        <span>{((evaluation.submitted_assignments / evaluation.assigned_students) * 100).toFixed(1)}%</span>
                      </div>
                      <Progress 
                        value={(evaluation.submitted_assignments / evaluation.assigned_students) * 100} 
                        className="h-2" 
                      />
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* MONITORING TEMPS RÉEL */}
        <TabsContent value="monitoring" className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Activités Tests Adaptatifs */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Activity className="h-5 w-5" />
                  Activités Tests Adaptatifs
                </CardTitle>
                <CardDescription>
                  Activités récentes des étudiants sur les tests adaptatifs
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {realTimeData?.recent_adaptive_activities.map((activity, index) => (
                    <div key={index} className="flex items-center justify-between p-2 bg-gray-50 rounded">
                      <div>
                        <div className="font-medium text-sm">{activity.student_name}</div>
                        <div className="text-xs text-gray-600">{activity.test_title}</div>
                      </div>
                      <div className="text-right">
                        <Badge variant={activity.status === 'completed' ? 'default' : 'secondary'}>
                          {activity.status}
                        </Badge>
                        {activity.current_score && (
                          <div className="text-xs text-gray-600 mt-1">
                            Score: {activity.current_score}
                          </div>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>

            {/* Activités Évaluations Formatives */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Target className="h-5 w-5" />
                  Activités Évaluations Formatives
                </CardTitle>
                <CardDescription>
                  Activités récentes des étudiants sur les évaluations formatives
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {realTimeData?.recent_formative_activities.map((activity, index) => (
                    <div key={index} className="flex items-center justify-between p-2 bg-gray-50 rounded">
                      <div>
                        <div className="font-medium text-sm">{activity.student_name}</div>
                        <div className="text-xs text-gray-600">{activity.evaluation_title}</div>
                      </div>
                      <div className="text-right">
                        <Badge variant={activity.status === 'graded' ? 'default' : 'secondary'}>
                          {activity.status}
                        </Badge>
                        {activity.score && (
                          <div className="text-xs text-gray-600 mt-1">
                            Note: {activity.score}
                          </div>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Dernière Mise à Jour */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <TrendingUp className="h-5 w-5" />
                Dernière Mise à Jour
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-center">
                <div className="text-2xl font-bold text-green-600">
                  {realTimeData?.real_time_stats.last_updated ? 
                    new Date(realTimeData.real_time_stats.last_updated).toLocaleString('fr-FR') : 
                    'Non disponible'
                  }
                </div>
                <p className="text-gray-600 mt-2">
                  Les données sont mises à jour en temps réel depuis la base de données
                </p>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>

      {/* FOOTER INFORMATIF */}
      <Card className="bg-blue-50 border-blue-200">
        <CardContent className="pt-6">
          <div className="text-center">
            <h3 className="text-lg font-semibold text-blue-800 mb-2">
              🎯 Connexion aux Données Réelles
            </h3>
            <p className="text-blue-700">
              Cette page teste la connexion entre le frontend et les vrais endpoints backend. 
              Les données affichées proviennent directement de la base de données SQLite 
              et reflètent l'activité réelle des étudiants.
            </p>
            <div className="mt-4 flex items-center justify-center gap-4 text-sm text-blue-600">
              <span className="flex items-center gap-1">
                <CheckCircle className="h-4 w-4" />
                Tests Adaptatifs
              </span>
              <span className="flex items-center gap-1">
                <CheckCircle className="h-4 w-4" />
                Évaluations Formatives
              </span>
              <span className="flex items-center gap-1">
                <CheckCircle className="h-4 w-4" />
                Monitoring Temps Réel
              </span>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}























