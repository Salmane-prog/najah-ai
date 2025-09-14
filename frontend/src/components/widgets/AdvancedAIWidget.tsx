import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';
import { 
  Brain, 
  TrendingUp, 
  Target, 
  Lightbulb, 
  Award,
  AlertTriangle,
  CheckCircle,
  TrendingDown,
  Minus,
  AlertCircle
} from 'lucide-react';
import { apiClient } from '../../utils/api';

interface AIAnalysis {
  total_quizzes: number;
  completed_quizzes: number;
  completion_rate: number;
  average_score: number;
  recent_performance: number;
  performance_trend: string;
  strengths: string[];
  weaknesses: string[];
  recommendations: string[];
}

interface Prediction {
  prediction: string;
  confidence: number;
  trend: string;
}

interface ContentRecommendation {
  type: string;
  subject: string;
  title: string;
  description: string;
  priority: string;
  estimated_time: string;
}

interface AdvancedAIWidgetProps {
  classId?: number;
  token?: string;
}

interface AIAnalysisData {
  completed_quizzes: number;
  average_score: number;
  recommendations: string[];
}

const AdvancedAIWidget: React.FC<AdvancedAIWidgetProps> = ({ classId, token }) => {
  const [analysis, setAnalysis] = useState<AIAnalysisData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchAIAnalysis = async () => {
      try {
        setLoading(true);
        setError(null);
        
        const headers: HeadersInit = {
          'Content-Type': 'application/json',
        };
        if (token) {
          headers['Authorization'] = `Bearer ${token}`;
        }

        // Appel API réel
        const response = await apiClient.get('/api/v1/analytics/');
        
        setAnalysis({
          completed_quizzes: response.data.completed_quizzes || 0,
          average_score: response.data.average_score || 0,
          recommendations: [
            "Surveillez les performances des étudiants en difficulté",
            "Encouragez la participation aux quiz",
            "Analysez les tendances de progression"
          ]
        });
        
        setLoading(false);
        
      } catch (err) {
        console.error("Erreur lors de la récupération de l'analyse IA:", err);
        setError("Erreur lors du chargement de l'analyse");
        setLoading(false);
      }
    };

    fetchAIAnalysis();
  }, [classId, token]);

  const getTrendIcon = (trend: string) => {
    switch (trend) {
      case 'improving':
        return <TrendingUp className="w-4 h-4 text-green-500" />;
      case 'declining':
        return <TrendingDown className="w-4 h-4 text-red-500" />;
      default:
        return <Minus className="w-4 h-4 text-gray-500" />;
    }
  };

  if (loading) {
    return (
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Brain className="w-5 h-5" />
            Analyse IA Avancée
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex items-center justify-center py-8">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
          </div>
        </CardContent>
      </Card>
    );
  }

  if (error) {
    return (
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Brain className="w-5 h-5" />
            Analyse IA Avancée
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="text-red-600 text-center py-4">
            <AlertCircle className="w-8 h-8 mx-auto mb-2" />
            <p>{error}</p>
          </div>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card className="h-full">
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Brain className="w-5 h-5" />
          Analyse IA Avancée
        </CardTitle>
      </CardHeader>
      <CardContent>
        {analysis ? (
          <div className="space-y-4">
            <div className="grid grid-cols-2 gap-4">
              <div className="bg-blue-50 p-3 rounded-lg">
                <div className="text-sm text-blue-600 font-medium">Quiz Completés</div>
                <div className="text-2xl font-bold text-blue-900">
                  {analysis.completed_quizzes || 0}
                </div>
              </div>
              <div className="bg-green-50 p-3 rounded-lg">
                <div className="text-sm text-green-600 font-medium">Score Moyen</div>
                <div className="text-2xl font-bold text-green-900">
                  {analysis.average_score || 0}%
                </div>
              </div>
            </div>

            {analysis.recommendations && analysis.recommendations.length > 0 && (
              <div className="mt-4">
                <h4 className="font-semibold mb-2 text-sm">Recommandations</h4>
                <div className="text-xs text-gray-600">
                  {analysis.recommendations.slice(0, 2).map((rec: string, index: number) => (
                    <div key={index} className="flex items-start gap-1 mb-1">
                      <Lightbulb className="w-3 h-3 text-yellow-500 mt-0.5 flex-shrink-0" />
                      <span>{rec}</span>
                    </div>
                  ))}
                  {analysis.recommendations.length > 2 && (
                    <div className="text-xs text-blue-600 mt-1">+{analysis.recommendations.length - 2} autres</div>
                  )}
                </div>
              </div>
            )}
          </div>
        ) : (
          <div className="text-center py-4 text-gray-500">
            Aucune donnée d'analyse disponible
          </div>
        )}
      </CardContent>
    </Card>
  );
};

export default AdvancedAIWidget; 