'use client';

import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Progress } from '@/components/ui/progress';
import { Badge } from '@/components/ui/badge';
import { 
  TrendingUp, 
  TrendingDown, 
  Target, 
  Lightbulb, 
  User, 
  BookOpen,
  BarChart3,
  LineChart,
  PieChart,
  Activity
} from 'lucide-react';
import { realAnalyticsService } from '@/services/realAnalyticsService';

interface StudentPrediction {
  id: number;
  name: string;
  currentScore: number;
  predictedScore: number;
  trend: 'up' | 'down' | 'stable';
  confidence: number;
  recommendations: string[];
}

interface SubjectPrediction {
  subject: string;
  currentAverage: number;
  predictedAverage: number;
  trend: 'up' | 'down' | 'stable';
  confidence: number;
  studentCount: number;
}

interface AIPredictionsProps {
  className?: string;
}

export default function AIPredictions({ className }: AIPredictionsProps) {
  const [activeTab, setActiveTab] = useState<'students' | 'subjects' | 'recommendations'>('students');
  const [selectedStudent, setSelectedStudent] = useState<number | null>(null);
  const [selectedSubject, setSelectedSubject] = useState<string>('all');
  const [predictions, setPredictions] = useState<{
    students: StudentPrediction[];
    subjects: SubjectPrediction[];
  }>({
    students: [],
    subjects: []
  });
  const [loading, setLoading] = useState(true);

  // Charger les vraies prédictions IA depuis le backend
  useEffect(() => {
    const loadAIPredictions = async () => {
      try {
        setLoading(true);
        console.log('🚀 Chargement des prédictions IA depuis le backend...');
        
        const aiPredictions = await realAnalyticsService.getAIPredictions();
        console.log('✅ Prédictions IA reçues:', aiPredictions);
        
        // Convertir les données du backend au format du composant
        const convertedStudents = aiPredictions.map(pred => ({
          id: pred.student_id,
          name: pred.student_name,
          currentScore: pred.avg_score ?? 0,
          predictedScore: pred.predicted_value ?? 0,
          trend: pred.predicted_value > pred.avg_score ? 'up' : pred.predicted_value < pred.avg_score ? 'down' : 'stable',
          confidence: (pred.confidence ?? 0) * 100, // Convertir en pourcentage
          recommendations: [pred.recommendation ?? 'Aucune recommandation']
        }));
        
        setPredictions({
          students: convertedStudents,
          subjects: [] // À implémenter plus tard
        });
        
        console.log('🎯 Prédictions converties:', convertedStudents);
        
      } catch (error) {
        console.error('❌ Erreur lors du chargement des prédictions IA:', error);
        // Fallback vers les données mock en cas d'erreur
        setPredictions({
          students: [
            {
              id: 1,
              name: "Marie Dubois",
              currentScore: 75,
              predictedScore: 58,
              trend: 'down' as const,
              confidence: 5,
              recommendations: ["🚨 Score faible détecté. Demandez de l'aide à votre professeur."]
            },
            {
              id: 2,
              name: "Ahmed Benali",
              currentScore: 75,
              predictedScore: 64,
              trend: 'down' as const,
              confidence: 5,
              recommendations: ["🔄 Refaites les tests précédents pour renforcer vos connaissances."]
            }
          ],
          subjects: []
        });
      } finally {
        setLoading(false);
      }
    };
    
    loadAIPredictions();
  }, []);

  const getTrendIcon = (trend: 'up' | 'down' | 'stable') => {
    switch (trend) {
      case 'up':
        return <TrendingUp className="w-4 h-4 text-green-500" />;
      case 'down':
        return <TrendingDown className="w-4 h-4 text-red-500" />;
      default:
        return <Activity className="w-4 h-4 text-blue-500" />;
    }
  };

  const getTrendColor = (trend: 'up' | 'down' | 'stable') => {
    switch (trend) {
      case 'up':
        return 'text-green-600';
      case 'down':
        return 'text-red-600';
      default:
        return 'text-blue-600';
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <div className={`space-y-6 ${className}`}>
      {/* En-tête avec onglets */}
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-2">
          <Target className="w-6 h-6 text-blue-600" />
          <h2 className="text-2xl font-bold text-gray-900">Prédictions IA</h2>
        </div>
        <div className="flex space-x-2">
          <Button
            variant={activeTab === 'students' ? 'default' : 'outline'}
            onClick={() => setActiveTab('students')}
            className="flex items-center space-x-2"
          >
            <User className="w-4 h-4" />
            <span>Étudiants</span>
          </Button>
          <Button
            variant={activeTab === 'subjects' ? 'default' : 'outline'}
            onClick={() => setActiveTab('subjects')}
            className="flex items-center space-x-2"
          >
            <BookOpen className="w-4 h-4" />
            <span>Matières</span>
          </Button>
          <Button
            variant={activeTab === 'recommendations' ? 'default' : 'outline'}
            onClick={() => setActiveTab('recommendations')}
            className="flex items-center space-x-2"
          >
            <Lightbulb className="w-4 h-4" />
            <span>Recommandations</span>
          </Button>
        </div>
      </div>

      {/* Contenu des onglets */}
      {activeTab === 'students' && (
        <div className="space-y-6">
          {/* Filtres */}
          <div className="flex space-x-4">
            <Select value={selectedStudent?.toString() || 'all'} onValueChange={(value) => setSelectedStudent(value === 'all' ? null : parseInt(value))}>
              <SelectTrigger className="w-48">
                <SelectValue placeholder="Sélectionner un étudiant" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">Tous les étudiants</SelectItem>
                {predictions.students.map((student, index) => (
                  <SelectItem key={student.id || index} value={student.id?.toString() || index.toString()}>
                    {student.name || `Étudiant ${index + 1}`}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>

          {/* Prédictions par étudiant */}
          <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
            {predictions.students
              .filter(student => !selectedStudent || (student.id && student.id === selectedStudent))
              .map((student, index) => (
                <Card key={student.id || index} className="hover:shadow-lg transition-shadow">
                  <CardHeader className="pb-3">
                    <CardTitle className="flex items-center justify-between text-lg">
                      <span>{student.name || 'Étudiant'}</span>
                      {getTrendIcon(student.trend || 'stable')}
                    </CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    {/* Scores actuels et prédits */}
                    <div className="space-y-2">
                      <div className="flex justify-between items-center">
                        <span className="text-sm text-gray-600">Score actuel</span>
                        <span className="font-semibold">{student.currentScore || 0}%</span>
                      </div>
                      <div className="flex justify-between items-center">
                        <span className="text-sm text-gray-600">Score prédit</span>
                        <span className={`font-semibold ${getTrendColor(student.trend || 'stable')}`}>
                          {student.predictedScore || 0}%
                        </span>
                      </div>
                      <Progress value={student.predictedScore || 0} className="h-2" />
                    </div>

                    {/* Confiance de la prédiction */}
                    <div className="space-y-2">
                      <div className="flex justify-between items-center">
                        <span className="text-sm text-gray-600">Confiance IA</span>
                        <Badge variant={(student.confidence || 0) > 80 ? 'default' : (student.confidence || 0) > 60 ? 'secondary' : 'destructive'}>
                          {student.confidence || 0}%
                        </Badge>
                      </div>
                    </div>

                    {/* Recommandations */}
                    <div className="space-y-2">
                      <h4 className="text-sm font-medium text-gray-700">Recommandations IA</h4>
                      <ul className="space-y-1">
                        {(student.recommendations || []).slice(0, 2).map((rec, index) => (
                          <li key={index} className="text-xs text-gray-600 flex items-start space-x-2">
                            <Lightbulb className="w-3 h-3 text-yellow-500 mt-0.5 flex-shrink-0" />
                            <span>{rec || 'Aucune recommandation'}</span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  </CardContent>
                </Card>
              ))}
          </div>
        </div>
      )}

      {activeTab === 'subjects' && (
        <div className="space-y-6">
          <Card>
            <CardContent className="text-center py-8">
              <BookOpen className="w-12 h-12 mx-auto mb-2 text-gray-400" />
              <p className="text-gray-500">Prédictions par matière à implémenter</p>
            </CardContent>
          </Card>
        </div>
      )}

      {activeTab === 'recommendations' && (
        <div className="space-y-6">
          <Card>
            <CardContent className="text-center py-8">
              <Lightbulb className="w-12 h-12 mx-auto mb-2 text-gray-400" />
              <p className="text-gray-500">Recommandations globales à implémenter</p>
            </CardContent>
          </Card>
        </div>
      )}
    </div>
  );
}
