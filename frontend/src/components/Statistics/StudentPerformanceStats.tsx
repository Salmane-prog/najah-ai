'use client';

import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { 
  TrendingUp, 
  TrendingDown, 
  Users, 
  Target, 
  Calendar,
  Download,
  RefreshCw
} from 'lucide-react';

interface PerformanceData {
  student_id: number;
  student_name: string;
  total_quizzes: number;
  average_score: number;
  completion_rate: number;
  subjects: {
    [subject: string]: {
      quizzes_taken: number;
      average_score: number;
      best_score: number;
      worst_score: number;
    };
  };
  recent_performance: {
    date: string;
    score: number;
    quiz_title: string;
  }[];
  improvement_trend: 'improving' | 'declining' | 'stable';
}

interface ClassStats {
  total_students: number;
  class_average: number;
  completion_rate: number;
  top_performers: PerformanceData[];
  struggling_students: PerformanceData[];
  subject_performance: {
    [subject: string]: {
      average_score: number;
      total_quizzes: number;
      pass_rate: number;
    };
  };
}

const StudentPerformanceStats = () => {
  const [performanceData, setPerformanceData] = useState<PerformanceData[]>([]);
  const [classStats, setClassStats] = useState<ClassStats | null>(null);
  const [selectedPeriod, setSelectedPeriod] = useState('month');
  const [selectedSubject, setSelectedSubject] = useState('all');
  const [loading, setLoading] = useState(true);
  const [viewMode, setViewMode] = useState<'individual' | 'class'>('class');

  useEffect(() => {
    fetchPerformanceData();
  }, [selectedPeriod, selectedSubject]);

  const fetchPerformanceData = async () => {
    setLoading(true);
    try {
      // Récupérer les statistiques de classe
      const classResponse = await fetch(`/api/v1/analytics/class/performance?period=${selectedPeriod}&subject=${selectedSubject}`);
      if (classResponse.ok) {
        const classData = await classResponse.json();
        setClassStats(classData);
      }

      // Récupérer les performances individuelles
      const individualResponse = await fetch(`/api/v1/analytics/students/performance?period=${selectedPeriod}&subject=${selectedSubject}`);
      if (individualResponse.ok) {
        const individualData = await individualResponse.json();
        setPerformanceData(individualData.students || []);
      }
    } catch (error) {
      console.error('Erreur lors du chargement des statistiques:', error);
    } finally {
      setLoading(false);
    }
  };

  const exportData = () => {
    const data = {
      period: selectedPeriod,
      subject: selectedSubject,
      class_stats: classStats,
      individual_performance: performanceData,
      export_date: new Date().toISOString()
    };

    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `performance_stats_${selectedPeriod}_${selectedSubject}.json`;
    a.click();
    URL.revokeObjectURL(url);
  };

  const getImprovementIcon = (trend: string) => {
    switch (trend) {
      case 'improving':
        return <TrendingUp className="h-4 w-4 text-green-500" />;
      case 'declining':
        return <TrendingDown className="h-4 w-4 text-red-500" />;
      case 'stable':
        return <Target className="h-4 w-4 text-blue-500" />;
      default:
        return <Target className="h-4 w-4 text-gray-500" />;
    }
  };

  const getScoreColor = (score: number) => {
    if (score >= 80) return 'text-green-600';
    if (score >= 60) return 'text-yellow-600';
    return 'text-red-600';
  };

  const getScoreBadge = (score: number) => {
    if (score >= 80) return <Badge variant="success">Excellent</Badge>;
    if (score >= 60) return <Badge variant="default">Bon</Badge>;
    return <Badge variant="destructive">À améliorer</Badge>;
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center p-8">
        <RefreshCw className="h-8 w-8 animate-spin" />
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header avec contrôles */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center space-y-4 md:space-y-0">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Statistiques de Performance</h1>
          <p className="text-gray-600">Analysez les performances de vos étudiants</p>
        </div>
        
        <div className="flex items-center space-x-4">
          <Select value={selectedPeriod} onValueChange={setSelectedPeriod}>
            <SelectTrigger className="w-32">
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="week">Semaine</SelectItem>
              <SelectItem value="month">Mois</SelectItem>
              <SelectItem value="quarter">Trimestre</SelectItem>
              <SelectItem value="year">Année</SelectItem>
            </SelectContent>
          </Select>

          <Select value={selectedSubject} onValueChange={setSelectedSubject}>
            <SelectTrigger className="w-40">
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">Toutes matières</SelectItem>
              <SelectItem value="Français">Français</SelectItem>
              <SelectItem value="Mathématiques">Mathématiques</SelectItem>
              <SelectItem value="Histoire">Histoire</SelectItem>
              <SelectItem value="Sciences">Sciences</SelectItem>
            </SelectContent>
          </Select>

          <div className="flex space-x-2">
            <Button
              variant={viewMode === 'class' ? 'default' : 'outline'}
              onClick={() => setViewMode('class')}
            >
              Vue Classe
            </Button>
            <Button
              variant={viewMode === 'individual' ? 'default' : 'outline'}
              onClick={() => setViewMode('individual')}
            >
              Vue Individuelle
            </Button>
          </div>

          <Button variant="outline" onClick={exportData} className="flex items-center gap-2">
            <Download className="h-4 w-4" />
            Exporter
          </Button>
        </div>
      </div>

      {/* Vue Classe */}
      {viewMode === 'class' && classStats && (
        <div className="space-y-6">
          {/* Statistiques générales */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <Card>
              <CardContent className="p-4">
                <div className="flex items-center space-x-2">
                  <Users className="h-8 w-8 text-blue-600" />
                  <div>
                    <p className="text-sm font-medium text-gray-600">Total Étudiants</p>
                    <p className="text-2xl font-bold text-gray-900">{classStats.total_students}</p>
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardContent className="p-4">
                <div className="flex items-center space-x-2">
                  <Target className="h-8 w-8 text-green-600" />
                  <div>
                    <p className="text-sm font-medium text-gray-600">Moyenne Classe</p>
                    <p className="text-2xl font-bold text-green-600">{classStats.class_average.toFixed(1)}%</p>
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardContent className="p-4">
                <div className="flex items-center space-x-2">
                  <Calendar className="h-8 w-8 text-purple-600" />
                  <div>
                    <p className="text-sm font-medium text-gray-600">Taux Réussite</p>
                    <p className="text-2xl font-bold text-purple-600">{classStats.completion_rate.toFixed(1)}%</p>
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardContent className="p-4">
                <div className="flex items-center space-x-2">
                  <TrendingUp className="h-8 w-8 text-orange-600" />
                  <div>
                    <p className="text-sm font-medium text-gray-600">Quiz Total</p>
                    <p className="text-2xl font-bold text-orange-600">
                      {performanceData.reduce((sum, student) => sum + student.total_quizzes, 0)}
                    </p>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Performance par matière */}
          <Card>
            <CardHeader>
              <CardTitle>Performance par Matière</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                {Object.entries(classStats.subject_performance).map(([subject, stats]) => (
                  <div key={subject} className="p-4 border rounded-lg">
                    <h3 className="font-semibold mb-2">{subject}</h3>
                    <div className="space-y-2 text-sm">
                      <div className="flex justify-between">
                        <span>Moyenne:</span>
                        <span className={getScoreColor(stats.average_score)}>
                          {stats.average_score.toFixed(1)}%
                        </span>
                      </div>
                      <div className="flex justify-between">
                        <span>Quiz:</span>
                        <span>{stats.total_quizzes}</span>
                      </div>
                      <div className="flex justify-between">
                        <span>Taux réussite:</span>
                        <span>{stats.pass_rate.toFixed(1)}%</span>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>

          {/* Top performers et étudiants en difficulté */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <Card>
              <CardHeader>
                <CardTitle className="text-green-700">Top Performers</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {classStats.top_performers.slice(0, 5).map((student, index) => (
                    <div key={student.student_id} className="flex items-center justify-between p-3 bg-green-50 rounded-lg">
                      <div className="flex items-center space-x-3">
                        <Badge variant="outline">#{index + 1}</Badge>
                        <span className="font-medium">{student.student_name}</span>
                      </div>
                      <div className="text-right">
                        <div className="font-semibold text-green-700">{student.average_score.toFixed(1)}%</div>
                        <div className="text-sm text-gray-600">{student.total_quizzes} quiz</div>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="text-red-700">Étudiants en Difficulté</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {classStats.struggling_students.slice(0, 5).map((student, index) => (
                    <div key={student.student_id} className="flex items-center justify-between p-3 bg-red-50 rounded-lg">
                      <div className="flex items-center space-x-3">
                        <Badge variant="outline">#{index + 1}</Badge>
                        <span className="font-medium">{student.student_name}</span>
                      </div>
                      <div className="text-right">
                        <div className="font-semibold text-red-700">{student.average_score.toFixed(1)}%</div>
                        <div className="text-sm text-gray-600">{student.total_quizzes} quiz</div>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      )}

      {/* Vue Individuelle */}
      {viewMode === 'individual' && (
        <div className="space-y-6">
          {/* Tableau des performances individuelles */}
          <Card>
            <CardHeader>
              <CardTitle>Performances Individuelles</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="overflow-x-auto">
                <table className="w-full">
                  <thead>
                    <tr className="border-b">
                      <th className="text-left p-3">Étudiant</th>
                      <th className="text-left p-3">Quiz</th>
                      <th className="text-left p-3">Moyenne</th>
                      <th className="text-left p-3">Taux Réussite</th>
                      <th className="text-left p-3">Tendance</th>
                      <th className="text-left p-3">Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    {performanceData.map((student) => (
                      <tr key={student.student_id} className="border-b hover:bg-gray-50">
                        <td className="p-3">
                          <div className="font-medium">{student.student_name}</div>
                        </td>
                        <td className="p-3">{student.total_quizzes}</td>
                        <td className="p-3">
                          <div className="flex items-center space-x-2">
                            <span className={`font-semibold ${getScoreColor(student.average_score)}`}>
                              {student.average_score.toFixed(1)}%
                            </span>
                            {getScoreBadge(student.average_score)}
                          </div>
                        </td>
                        <td className="p-3">{student.completion_rate.toFixed(1)}%</td>
                        <td className="p-3">
                          <div className="flex items-center space-x-2">
                            {getImprovementIcon(student.improvement_trend)}
                            <span className="text-sm">
                              {student.improvement_trend === 'improving' && 'Amélioration'}
                              {student.improvement_trend === 'declining' && 'Baisse'}
                              {student.improvement_trend === 'stable' && 'Stable'}
                            </span>
                          </div>
                        </td>
                        <td className="p-3">
                          <Button variant="outline" size="sm">
                            Détails
                          </Button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </CardContent>
          </Card>

          {/* Graphique de tendance pour un étudiant sélectionné */}
          {performanceData.length > 0 && (
            <Card>
              <CardHeader>
                <CardTitle>Tendance de Performance - {performanceData[0]?.student_name}</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="h-64 bg-gray-50 rounded-lg flex items-center justify-center">
                  <div className="text-center text-gray-500">
                    <TrendingUp className="h-12 w-12 mx-auto mb-2" />
                    <p>Graphique de tendance</p>
                    <p className="text-sm">Intégration avec Chart.js ou Recharts</p>
                  </div>
                </div>
              </CardContent>
            </Card>
          )}
        </div>
      )}
    </div>
  );
};

export default StudentPerformanceStats;










