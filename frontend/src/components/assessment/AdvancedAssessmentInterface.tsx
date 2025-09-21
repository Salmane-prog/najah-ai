'use client';

import React, { useState, useEffect, useCallback } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Progress } from '@/components/ui/progress';
import { Badge } from '@/components/ui/badge';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { 
  Brain, 
  Clock, 
  Target, 
  CheckCircle, 
  XCircle, 
  AlertTriangle,
  TrendingUp,
  TrendingDown,
  Lightbulb,
  BarChart3,
  Timer,
  Zap
} from 'lucide-react';
import { Line, Doughnut } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  ArcElement,
} from 'chart.js';

// Enregistrer Chart.js
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  ArcElement
);

interface Question {
  id: number;
  question_text: string;
  question_type: string;
  subject: string;
  difficulty: string;
  options?: string[];
  correct_answer: string;
  explanation?: string;
  estimated_time: number;
  cognitive_load_estimate: number;
}

interface AssessmentSession {
  id: string;
  student_id: number;
  questions: Question[];
  current_question_index: number;
  answers: Record<number, any>;
  response_times: Record<number, number>;
  start_time: Date;
  current_difficulty: string;
  cognitive_analysis: any;
}

interface CognitiveFeedback {
  pattern: string;
  confidence_score: number;
  cognitive_load: number;
  recommendations: string[];
  time_analysis: any;
}

const AdvancedAssessmentInterface: React.FC = () => {
  const [session, setSession] = useState<AssessmentSession | null>(null);
  const [currentAnswer, setCurrentAnswer] = useState<string>('');
  const [questionStartTime, setQuestionStartTime] = useState<Date>(new Date());
  const [showFeedback, setShowFeedback] = useState(false);
  const [feedback, setFeedback] = useState<CognitiveFeedback | null>(null);
  const [showProgressChart, setShowProgressChart] = useState(false);
  const [isLoading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // État pour l'analyse cognitive en temps réel
  const [cognitiveMetrics, setCognitiveMetrics] = useState({
    attention_span: 0,
    response_speed: 0,
    confidence_trend: 0,
    cognitive_load: 0
  });

  // État pour la progression
  const [progressData, setProgressData] = useState({
    correct: 0,
    incorrect: 0,
    skipped: 0,
    total: 0
  });

  useEffect(() => {
    // Initialiser la session d'évaluation
    initializeAssessment();
  }, []);

  useEffect(() => {
    if (session) {
      // Démarrer le chronomètre pour la question actuelle
      setQuestionStartTime(new Date());
    }
  }, [session?.current_question_index]);

  const initializeAssessment = async () => {
    setLoading(true);
    try {
      // Simuler l'initialisation d'une session d'évaluation
      const mockSession: AssessmentSession = {
        id: 'assessment_001',
        student_id: 1,
        questions: generateMockQuestions(),
        current_question_index: 0,
        answers: {},
        response_times: {},
        start_time: new Date(),
        current_difficulty: 'medium',
        cognitive_analysis: {}
      };

      setSession(mockSession);
      setProgressData({
        correct: 0,
        incorrect: 0,
        skipped: 0,
        total: mockSession.questions.length
      });
    } catch (err) {
      setError('Erreur lors de l\'initialisation de l\'évaluation');
    } finally {
      setLoading(false);
    }
  };

  const generateMockQuestions = (): Question[] => {
    return [
      {
        id: 1,
        question_text: "Quel est le résultat de 15 × 8 ?",
        question_type: "multiple_choice",
        subject: "Mathématiques",
        difficulty: "medium",
        options: ["100", "110", "120", "130"],
        correct_answer: "120",
        explanation: "15 × 8 = 120. Vous pouvez vérifier : 10 × 8 = 80 et 5 × 8 = 40, donc 80 + 40 = 120.",
        estimated_time: 60,
        cognitive_load_estimate: 2.5
      },
      {
        id: 2,
        question_text: "Conjuguez le verbe 'prendre' à la 3ème personne du pluriel au futur simple",
        question_type: "text",
        subject: "Français",
        difficulty: "hard",
        correct_answer: "ils prendront",
        explanation: "Le verbe 'prendre' se conjugue 'ils prendront' au futur simple.",
        estimated_time: 90,
        cognitive_load_estimate: 3.2
      },
      {
        id: 3,
        question_text: "Quelle est la capitale du Japon ?",
        question_type: "multiple_choice",
        subject: "Géographie",
        difficulty: "easy",
        options: ["Tokyo", "Kyoto", "Osaka", "Yokohama"],
        correct_answer: "Tokyo",
        explanation: "Tokyo est la capitale actuelle du Japon depuis 1868.",
        estimated_time: 45,
        cognitive_load_estimate: 1.8
      }
    ];
  };

  const handleAnswerSubmit = useCallback(async () => {
    if (!session || !currentAnswer.trim()) return;

    const currentQuestion = session.questions[session.current_question_index];
    const responseTime = (new Date().getTime() - questionStartTime.getTime()) / 1000;
    
    // Analyser la réponse en temps réel
    const cognitiveFeedback = await analyzeResponseInRealTime(
      currentQuestion,
      currentAnswer,
      responseTime
    );

    // Mettre à jour la session
    const newAnswers = { ...session.answers, [currentQuestion.id]: currentAnswer };
    const newResponseTimes = { ...session.response_times, [currentQuestion.id]: responseTime };
    
    // Calculer la progression
    const isCorrect = currentAnswer === currentQuestion.correct_answer;
    const newProgress = {
      ...progressData,
      correct: progressData.correct + (isCorrect ? 1 : 0),
      incorrect: progressData.incorrect + (isCorrect ? 0 : 1)
    };

    setProgressData(newProgress);
    setFeedback(cognitiveFeedback);
    setShowFeedback(true);

    // Mettre à jour les métriques cognitives
    updateCognitiveMetrics(cognitiveFeedback);

    // Passer à la question suivante après un délai
    setTimeout(() => {
      if (session.current_question_index < session.questions.length - 1) {
        setSession(prev => prev ? {
          ...prev,
          current_question_index: prev.current_question_index + 1,
          answers: newAnswers,
          response_times: newResponseTimes
        } : null);
        setCurrentAnswer('');
        setShowFeedback(false);
      } else {
        // Évaluation terminée
        completeAssessment();
      }
    }, 3000);
  }, [session, currentAnswer, questionStartTime, progressData]);

  const analyzeResponseInRealTime = async (
    question: Question,
    answer: string,
    responseTime: number
  ): Promise<CognitiveFeedback> => {
    // Simulation d'analyse cognitive en temps réel
    const isCorrect = answer === question.correct_answer;
    
    // Analyse du pattern de réponse
    let pattern = 'analytical';
    if (responseTime < 10) pattern = 'impulsive';
    else if (responseTime < 30) pattern = 'confident';
    else if (responseTime > 120) pattern = 'struggling';
    
    // Score de confiance basé sur le temps et la difficulté
    const optimalTime = question.estimated_time;
    const timeEfficiency = Math.max(0, 1 - Math.abs(responseTime - optimalTime) / optimalTime);
    const confidenceScore = isCorrect ? timeEfficiency : timeEfficiency * 0.5;
    
    // Charge cognitive estimée
    const cognitiveLoad = Math.min(5, question.cognitive_load_estimate * (responseTime / optimalTime));
    
    // Recommandations personnalisées
    const recommendations = generateRecommendations(pattern, confidenceScore, cognitiveLoad, isCorrect);
    
    // Analyse temporelle
    const timeAnalysis = {
      response_time: responseTime,
      optimal_time: optimalTime,
      efficiency: timeEfficiency,
      category: responseTime < optimalTime ? 'rapide' : 'réfléchi'
    };

    return {
      pattern,
      confidence_score: confidenceScore,
      cognitive_load: cognitiveLoad,
      recommendations,
      time_analysis: timeAnalysis
    };
  };

  const generateRecommendations = (
    pattern: string,
    confidence: number,
    cognitiveLoad: number,
    isCorrect: boolean
  ): string[] => {
    const recommendations: string[] = [];
    
    if (pattern === 'impulsive' && !isCorrect) {
      recommendations.push("Prenez le temps de lire attentivement la question avant de répondre");
    }
    
    if (pattern === 'struggling') {
      recommendations.push("Cette question semble difficile - utilisez les indices fournis");
    }
    
    if (confidence < 0.5) {
      recommendations.push("Revoyez les concepts de base de cette matière");
    }
    
    if (cognitiveLoad > 4) {
      recommendations.push("Considérez une pause si vous vous sentez fatigué");
    }
    
    if (isCorrect && confidence > 0.8) {
      recommendations.push("Excellente performance ! Continuez ainsi");
    }
    
    return recommendations;
  };

  const updateCognitiveMetrics = (feedback: CognitiveFeedback) => {
    setCognitiveMetrics(prev => ({
      attention_span: Math.min(100, prev.attention_span + (feedback.confidence_score > 0.7 ? 5 : -3)),
      response_speed: Math.max(0, prev.response_speed + (feedback.time_analysis.efficiency > 0.8 ? 3 : -2)),
      confidence_trend: Math.min(100, prev.confidence_trend + (feedback.confidence_score > 0.6 ? 4 : -3)),
      cognitive_load: Math.min(100, prev.cognitive_load + (feedback.cognitive_load > 3 ? 8 : -2))
    }));
  };

  const completeAssessment = () => {
    // Logique de finalisation de l'évaluation
    console.log('Évaluation terminée !');
  };

  const getCurrentQuestion = () => {
    if (!session) return null;
    return session.questions[session.current_question_index];
  };

  const getProgressPercentage = () => {
    if (!session) return 0;
    return ((session.current_question_index + 1) / session.questions.length) * 100;
  };

  const getTimeRemaining = () => {
    if (!session) return 0;
    const currentQuestion = getCurrentQuestion();
    if (!currentQuestion) return 0;
    
    const elapsed = (new Date().getTime() - questionStartTime.getTime()) / 1000;
    return Math.max(0, currentQuestion.estimated_time - elapsed);
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Initialisation de l'évaluation...</p>
        </div>
      </div>
    );
  }

  if (!session) {
    return (
      <div className="text-center py-8">
        <p className="text-red-600">Erreur : Session d'évaluation non initialisée</p>
        <Button onClick={initializeAssessment} className="mt-4">
          Réessayer
        </Button>
      </div>
    );
  }

  const currentQuestion = getCurrentQuestion();
  if (!currentQuestion) return null;

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-6">
      <div className="max-w-6xl mx-auto space-y-6">
        
        {/* Header de l'évaluation */}
        <Card className="bg-white shadow-lg">
          <CardHeader className="pb-4">
            <div className="flex items-center justify-between">
              <div>
                <CardTitle className="text-2xl font-bold text-gray-800">
                  Évaluation Adaptative - {currentQuestion.subject}
                </CardTitle>
                <p className="text-gray-600 mt-2">
                  Question {session.current_question_index + 1} sur {session.questions.length}
                </p>
              </div>
              
              <div className="flex items-center space-x-4">
                <div className="text-center">
                  <div className="text-2xl font-bold text-blue-600">
                    {Math.floor(getTimeRemaining())}s
                  </div>
                  <div className="text-sm text-gray-500">Temps restant</div>
                </div>
                
                <Button
                  variant="outline"
                  onClick={() => setShowProgressChart(!showProgressChart)}
                  className="flex items-center space-x-2"
                >
                  <BarChart3 className="w-4 h-4" />
                  <span>Progression</span>
                </Button>
              </div>
            </div>
          </CardHeader>
          
          {/* Barre de progression interactive */}
          <CardContent>
            <div className="space-y-4">
              <div className="flex items-center justify-between text-sm text-gray-600">
                <span>Progression globale</span>
                <span>{Math.round(getProgressPercentage())}%</span>
              </div>
              <Progress value={getProgressPercentage()} className="h-3" />
              
              {/* Métriques de progression */}
              <div className="grid grid-cols-4 gap-4 text-center">
                <div className="bg-green-50 p-3 rounded-lg">
                  <div className="text-lg font-bold text-green-600">{progressData.correct}</div>
                  <div className="text-xs text-green-600">Correctes</div>
                </div>
                <div className="bg-red-50 p-3 rounded-lg">
                  <div className="text-lg font-bold text-red-600">{progressData.incorrect}</div>
                  <div className="text-xs text-red-600">Incorrectes</div>
                </div>
                <div className="bg-yellow-50 p-3 rounded-lg">
                  <div className="text-lg font-bold text-yellow-600">{progressData.skipped}</div>
                  <div className="text-xs text-yellow-600">Sautées</div>
                </div>
                <div className="bg-blue-50 p-3 rounded-lg">
                  <div className="text-lg font-bold text-blue-600">{progressData.total}</div>
                  <div className="text-xs text-blue-600">Total</div>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Question actuelle */}
        <Card className="bg-white shadow-lg">
          <CardHeader>
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-3">
                <Badge variant="outline" className="text-sm">
                  {currentQuestion.difficulty}
                </Badge>
                <Badge variant="secondary" className="text-sm">
                  {currentQuestion.question_type}
                </Badge>
                <Badge variant="outline" className="text-sm">
                  <Brain className="w-3 h-3 mr-1" />
                  {currentQuestion.cognitive_load_estimate}/5
                </Badge>
              </div>
              
              <div className="text-sm text-gray-500">
                Temps estimé : {currentQuestion.estimated_time}s
              </div>
            </div>
          </CardHeader>
          
          <CardContent className="space-y-6">
            {/* Texte de la question */}
            <div className="text-lg text-gray-800 leading-relaxed">
              {currentQuestion.question_text}
            </div>
            
            {/* Options pour les QCM */}
            {currentQuestion.options && (
              <div className="space-y-3">
                {currentQuestion.options.map((option, index) => (
                  <Button
                    key={index}
                    variant={currentAnswer === option ? "default" : "outline"}
                    className="w-full justify-start h-auto p-4 text-left"
                    onClick={() => setCurrentAnswer(option)}
                  >
                    <span className="mr-3 text-sm font-medium text-gray-500">
                      {String.fromCharCode(65 + index)}
                    </span>
                    {option}
                  </Button>
                ))}
              </div>
            )}
            
            {/* Champ de réponse pour les questions texte */}
            {currentQuestion.question_type === 'text' && (
              <div className="space-y-3">
                <label className="block text-sm font-medium text-gray-700">
                  Votre réponse :
                </label>
                <textarea
                  value={currentAnswer}
                  onChange={(e) => setCurrentAnswer(e.target.value)}
                  className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  rows={3}
                  placeholder="Tapez votre réponse ici..."
                />
              </div>
            )}
            
            {/* Bouton de soumission */}
            <Button
              onClick={handleAnswerSubmit}
              disabled={!currentAnswer.trim()}
              className="w-full py-3 text-lg font-semibold"
            >
              <Zap className="w-5 h-5 mr-2" />
              Valider ma réponse
            </Button>
          </CardContent>
        </Card>

        {/* Feedback cognitif en temps réel */}
        {showFeedback && feedback && (
          <Card className="bg-white shadow-lg border-l-4 border-blue-500">
            <CardHeader>
              <CardTitle className="flex items-center text-blue-600">
                <Lightbulb className="w-5 h-5 mr-2" />
                Analyse Cognitive en Temps Réel
              </CardTitle>
            </CardHeader>
            
            <CardContent className="space-y-4">
              {/* Métriques cognitives */}
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                <div className="text-center p-3 bg-blue-50 rounded-lg">
                  <div className="text-lg font-bold text-blue-600">
                    {feedback.pattern}
                  </div>
                  <div className="text-xs text-blue-600">Pattern</div>
                </div>
                
                <div className="text-center p-3 bg-green-50 rounded-lg">
                  <div className="text-lg font-bold text-green-600">
                    {Math.round(feedback.confidence_score * 100)}%
                  </div>
                  <div className="text-xs text-green-600">Confiance</div>
                </div>
                
                <div className="text-center p-3 bg-orange-50 rounded-lg">
                  <div className="text-lg font-bold text-orange-600">
                    {feedback.cognitive_load.toFixed(1)}/5
                  </div>
                  <div className="text-xs text-orange-600">Charge cognitive</div>
                </div>
                
                <div className="text-center p-3 bg-purple-50 rounded-lg">
                  <div className="text-lg font-bold text-purple-600">
                    {feedback.time_analysis.category}
                  </div>
                  <div className="text-xs text-purple-600">Style de réponse</div>
                </div>
              </div>
              
              {/* Recommandations */}
              <div className="bg-yellow-50 p-4 rounded-lg">
                <h4 className="font-semibold text-yellow-800 mb-2">💡 Recommandations personnalisées :</h4>
                <ul className="space-y-1">
                  {feedback.recommendations.map((rec, index) => (
                    <li key={index} className="text-yellow-700 text-sm flex items-start">
                      <span className="mr-2">•</span>
                      {rec}
                    </li>
                  ))}
                </ul>
              </div>
            </CardContent>
          </Card>
        )}

        {/* Graphique de progression (optionnel) */}
        {showProgressChart && (
          <Card className="bg-white shadow-lg">
            <CardHeader>
              <CardTitle className="flex items-center">
                <TrendingUp className="w-5 h-5 mr-2 text-green-600" />
                Analyse de Progression
              </CardTitle>
            </CardHeader>
            
            <CardContent>
              <div className="h-64">
                <Line
                  data={{
                    labels: ['Q1', 'Q2', 'Q3', 'Q4', 'Q5'],
                    datasets: [
                      {
                        label: 'Temps de réponse (s)',
                        data: [45, 32, 78, 56, 41],
                        borderColor: 'rgb(59, 130, 246)',
                        backgroundColor: 'rgba(59, 130, 246, 0.1)',
                        tension: 0.4
                      },
                      {
                        label: 'Charge cognitive',
                        data: [2.1, 1.8, 3.2, 2.8, 2.3],
                        borderColor: 'rgb(147, 51, 234)',
                        backgroundColor: 'rgba(147, 51, 234, 0.1)',
                        tension: 0.4,
                        yAxisID: 'y1'
                      }
                    ]
                  }}
                  options={{
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                      y: {
                        type: 'linear',
                        display: true,
                        position: 'left',
                        title: { display: true, text: 'Temps (secondes)' }
                      },
                      y1: {
                        type: 'linear',
                        display: true,
                        position: 'right',
                        title: { display: true, text: 'Charge cognitive' },
                        grid: { drawOnChartArea: false }
                      }
                    }
                  }}
                />
              </div>
            </CardContent>
          </Card>
        )}
      </div>
    </div>
  );
};

export default AdvancedAssessmentInterface;















