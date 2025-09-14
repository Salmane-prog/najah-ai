import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { TrendingUp, TrendingDown, Users, Clock, Target, AlertTriangle } from 'lucide-react';
import { apiClient } from '@/api/apiClient';

interface PerformanceMetrics {
  total_quizzes_today: number;
  average_score: number;
  active_students: number;
  total_learning_time: number;
  score_trend: string;
  participation_rate: number;
}

interface PerformanceAlert {
  type: string;
  severity: string;
  message: string;
  recommendation: string;
}

interface PerformanceData {
  class_id: number;
  timestamp: string;
  metrics: PerformanceMetrics;
  alerts: PerformanceAlert[];
}

const PerformanceMonitoring: React.FC = () => {
  const [performanceData, setPerformanceData] = useState<PerformanceData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchPerformanceData();
    const interval = setInterval(fetchPerformanceData, 30000); // Rafraîchir toutes les 30 secondes
    return () => clearInterval(interval);
  }, []);

  const fetchPerformanceData = async () => {
    try {
      setLoading(true);
      const response = await apiClient.get('/api/v1/performance_monitoring/real-time/class/1');
      setPerformanceData(response.data);
      setError(null);
    } catch (err) {
      setError('Erreur lors du chargement des données de performance');
      console.error('Erreur performance monitoring:', err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (error) {
    return (
      <Alert variant="destructive">
        <AlertTriangle className="h-4 w-4" />
        <AlertDescription>{error}</AlertDescription>
      </Alert>
    );
  }

  if (!performanceData) {
    return <div>Aucune donnée disponible</div>;
  }

  const { metrics, alerts } = performanceData;

  // Vérification de sécurité pour éviter les erreurs TypeError
  if (!metrics) {
    return (
      <Alert variant="destructive">
        <AlertTriangle className="h-4 w-4" />
        <AlertDescription>Données de performance non disponibles</AlertDescription>
      </Alert>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-bold">Monitoring des Performances</h2>
        <Badge variant="outline" className="text-sm">
          Temps réel
        </Badge>
      </div>

      {/* Métriques principales */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Quiz Aujourd'hui</CardTitle>
            <Target className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{metrics.total_quizzes_today}</div>
            <p className="text-xs text-muted-foreground">
              Quiz complétés aujourd'hui
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Score Moyen</CardTitle>
            {metrics.score_trend === 'up' ? (
              <TrendingUp className="h-4 w-4 text-green-600" />
            ) : metrics.score_trend === 'down' ? (
              <TrendingDown className="h-4 w-4 text-red-600" />
            ) : (
              <div className="h-4 w-4 text-gray-400">─</div>
            )}
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{metrics.average_score}%</div>
            <p className="text-xs text-muted-foreground">
              Tendance: {metrics.score_trend === 'up' ? 'Amélioration' : 
                        metrics.score_trend === 'down' ? 'Baisse' : 'Stable'}
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Étudiants Actifs</CardTitle>
            <Users className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{metrics.active_students}</div>
            <p className="text-xs text-muted-foreground">
              {metrics.participation_rate}% de participation
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Temps d'Apprentissage</CardTitle>
            <Clock className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{Math.round(metrics.total_learning_time / 60)}min</div>
            <p className="text-xs text-muted-foreground">
              Temps total aujourd'hui
            </p>
          </CardContent>
        </Card>
      </div>

      {/* Taux de participation */}
      <Card>
        <CardHeader>
          <CardTitle>Taux de Participation</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-2">
            <div className="flex justify-between text-sm">
              <span>Participation actuelle</span>
              <span>{metrics.participation_rate}%</span>
            </div>
            <Progress value={metrics.participation_rate} className="h-2" />
            <p className="text-xs text-muted-foreground">
              {metrics.active_students} étudiants actifs sur le total
            </p>
          </div>
        </CardContent>
      </Card>

      {/* Alertes */}
      {alerts.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <AlertTriangle className="h-5 w-5 text-orange-500" />
              Alertes de Performance
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              {alerts.map((alert, index) => (
                <Alert key={index} variant={alert.severity === 'high' ? 'destructive' : 'default'}>
                  <AlertTriangle className="h-4 w-4" />
                  <AlertDescription>
                    <div className="font-medium">{alert.message}</div>
                    <div className="text-sm text-muted-foreground mt-1">
                      Recommandation: {alert.recommendation}
                    </div>
                  </AlertDescription>
                </Alert>
              ))}
            </div>
          </CardContent>
        </Card>
      )}

      {/* Dernière mise à jour */}
      <div className="text-xs text-muted-foreground text-center">
        Dernière mise à jour: {new Date(performanceData.timestamp).toLocaleString()}
      </div>
    </div>
  );
};

export default PerformanceMonitoring; 