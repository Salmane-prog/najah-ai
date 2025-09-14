'use client';

import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Progress } from '@/components/ui/progress';
import { Badge } from '@/components/ui/badge';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { 
  Play, 
  CheckCircle, 
  XCircle, 
  Loader2, 
  Brain, 
  Target,
  TrendingUp,
  Clock,
  BookOpen,
  Award,
  Lightbulb,
  AlertCircle
} from 'lucide-react';

interface Question {
  id: string;
  question: string;
  options: string[];
  correct: string;
  explanation: string;
  difficulty: string;
  topic: string;
}

interface TestProgress {
  current: number;
  total: number | null;
  difficulty: string;
  level_progression: string;
  current_level: string;
}

interface TestData {
  id: number;
  status: string;
  current_question: Question;
  progress: TestProgress;
}

interface FrenchAdaptiveTestProps {
  studentId: number;
  onTestComplete: () => void;
  testData?: TestData | null;
  token: string;
}

const FrenchAdaptiveTest: React.FC<FrenchAdaptiveTestProps> = ({
  studentId,
  onTestComplete,
  testData,
  token
}) => {
  const [testStatus, setTestStatus] = useState<'not_started' | 'in_progress' | 'completed'>('not_started');
  const [currentQuestion, setCurrentQuestion] = useState<Question | null>(null);
  const [selectedAnswer, setSelectedAnswer] = useState<string>('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [testProgress, setTestProgress] = useState<TestProgress | null>(null);
  const [questionHistory, setQuestionHistory] = useState<string[]>([]);
  const [score, setScore] = useState(0);
  const [questionsAnswered, setQuestionsAnswered] = useState(0);
  const [difficultyProgression, setDifficultyProgression] = useState<Array<{
    question_index: number;
    difficulty: string;
    score: number;
    was_correct: boolean;
  }>>([]);
  const [error, setError] = useState<string | null>(null);
  const [testId, setTestId] = useState<number | null>(null);

  const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

  useEffect(() => {
    if (testData) {
      setTestStatus(testData.status === 'completed' ? 'completed' : 'in_progress');
      setCurrentQuestion(testData.current_question);
      setTestProgress(testData.progress);
      setTestId(testData.id);
      
      if (testData.status === 'in_progress') {
        setQuestionsAnswered(testData.progress.current);
      }
    }
  }, [testData]);

  const startTest = async () => {
    try {
      setIsLoading(true);
      setError(null);

      console.log('🚀 Démarrage du test pour l\'étudiant:', studentId);

      const response = await fetch(`${API_BASE}/api/v1/french/initial-assessment/student/start`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ student_id: studentId })
      });

      if (!response.ok) {
        const errorText = await response.text();
        console.error('❌ Erreur HTTP:', response.status, errorText);
        throw new Error(`Erreur ${response.status}: ${response.statusText}`);
      }

      const data = await response.json();
      console.log('✅ Test démarré avec succès:', data);

      // Validation des données reçues
      if (!data.current_question) {
        throw new Error('Aucune question reçue du serveur');
      }

      if (!data.current_question.question || !data.current_question.options || !data.current_question.correct) {
        throw new Error('Question invalide reçue du serveur');
      }

      // Mise à jour de l'état de manière atomique
      setTestStatus('in_progress');
      setCurrentQuestion(data.current_question);
      setTestProgress(data.progress);
      setTestId(data.id);
      setQuestionsAnswered(0);
      setScore(0);
      setQuestionHistory([]);
      setDifficultyProgression([]);

      console.log('✅ État du test mis à jour:', {
        status: 'in_progress',
        questionId: data.current_question.id,
        questionText: data.current_question.question.substring(0, 50) + '...',
        difficulty: data.current_question.difficulty,
        testId: data.id
      });

    } catch (error) {
      console.error('❌ Erreur démarrage test:', error);
      setError(`Erreur lors du démarrage: ${error instanceof Error ? error.message : 'Erreur inconnue'}`);
      
      // Réinitialiser l'état en cas d'erreur
      setTestStatus('not_started');
      setCurrentQuestion(null);
      setTestProgress(null);
      setTestId(null);
    } finally {
      setIsLoading(false);
    }
  };

  const submitAnswer = async () => {
    if (!selectedAnswer || !currentQuestion || !testId) return;

    try {
      setIsSubmitting(true);
      setError(null);

      const wasCorrect = selectedAnswer === currentQuestion.correct;
      const questionScore = wasCorrect ? 10 : 0;
      const newQuestionIndex = questionsAnswered + 1;

      console.log('📝 Soumission réponse:', {
        answer: selectedAnswer,
        correct: currentQuestion.correct,
        wasCorrect,
        questionIndex: newQuestionIndex,
        currentScore: score
      });

      const response = await fetch(`${API_BASE}/api/v1/french/initial-assessment/${testId}/submit`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          answer: selectedAnswer,
          question_difficulty: currentQuestion.difficulty,
          correct_answer: currentQuestion.correct
        })
      });

      if (!response.ok) {
        throw new Error(`Erreur ${response.status}: ${response.statusText}`);
      }

      const data = await response.json();
      console.log('✅ Réponse soumise:', data);
      console.log('🔍 Données reçues:', {
        status: data.status,
        hasNextQuestion: !!data.next_question,
        nextQuestion: data.next_question,
        progress: data.progress,
        currentQuestionIndex: newQuestionIndex
      });

      // Mettre à jour l'état local de manière atomique
      setScore(prev => prev + questionScore);
      setQuestionsAnswered(newQuestionIndex);
      setQuestionHistory(prev => [...prev, currentQuestion.id]);
      
      // Enregistrer la progression de difficulté avec l'index correct
      setDifficultyProgression(prev => [...prev, {
        question_index: newQuestionIndex,
        difficulty: currentQuestion.difficulty,
        score: questionScore,
        was_correct: wasCorrect
      }]);

      // Vérifier si le test est terminé
      if (data.status === 'completed') {
        console.log('🏁 Test terminé, passage à l\'état completed');
        setTestStatus('completed');
        setTestProgress(data.progress);
        onTestComplete();
      } else if (data.next_question) {
        // Charger la prochaine question
        console.log('➡️ Passage à la question suivante:', data.next_question);
        setCurrentQuestion(data.next_question);
        setTestProgress(data.progress);
        setSelectedAnswer('');
        
        // Log de confirmation
        console.log('✅ État mis à jour:', {
          newQuestion: data.next_question.id,
          newIndex: newQuestionIndex,
          newScore: score + questionScore,
          newProgress: data.progress
        });
      } else {
        // Problème : pas de question suivante
        console.error('❌ Pas de question suivante reçue du backend');
        console.error('🔍 Données reçues complètes:', data);
        setError('Erreur: Pas de question suivante reçue du serveur');
      }

    } catch (error) {
      console.error('❌ Erreur soumission réponse:', error);
      setError(`Erreur lors de la soumission: ${error instanceof Error ? error.message : 'Erreur inconnue'}`);
    } finally {
      setIsSubmitting(false);
    }
  };

  const getDifficultyColor = (difficulty: string) => {
    switch (difficulty.toLowerCase()) {
      case 'easy': return 'bg-green-100 text-green-800';
      case 'medium': return 'bg-yellow-100 text-yellow-800';
      case 'hard': return 'bg-red-100 text-red-800';
      case 'a0': return 'bg-blue-100 text-blue-800';
      case 'a1': return 'bg-green-100 text-green-800';
      case 'a2': return 'bg-yellow-100 text-yellow-800';
      case 'b1': return 'bg-orange-100 text-orange-800';
      case 'b2': return 'bg-red-100 text-red-800';
      case 'c1': return 'bg-purple-100 text-purple-800';
      case 'c2': return 'bg-gray-100 text-gray-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const getDifficultyLabel = (difficulty: string) => {
    switch (difficulty.toLowerCase()) {
      case 'easy': return 'Facile';
      case 'medium': return 'Moyen';
      case 'hard': return 'Difficile';
      case 'a0': return 'Débutant Absolu';
      case 'a1': return 'Débutant';
      case 'a2': return 'Débutant Avancé';
      case 'b1': return 'Intermédiaire';
      case 'b2': return 'Intermédiaire Avancé';
      case 'c1': return 'Avancé';
      case 'c2': return 'Expert';
      default: return difficulty;
    }
  };

  const getProgressPercentage = () => {
    if (!testProgress) return 0;
    // Pour le test à 20 questions fixes
    if (testProgress.total === 20) {
      return (testProgress.current / 20) * 100;
    }
    // Fallback si pas de total
    return Math.min((questionsAnswered / 20) * 100, 100);
  };

  // Affichage des erreurs
  if (error) {
    return (
      <Card className="w-full">
        <CardContent className="flex items-center justify-center py-12">
          <div className="text-center">
            <AlertCircle className="h-12 w-12 text-red-600 mx-auto mb-4" />
            <p className="text-lg font-medium text-red-900">Erreur détectée</p>
            <p className="text-gray-600 mb-4">{error}</p>
            <div className="space-x-3">
              <Button 
                onClick={() => {
                  setError(null);
                  setTestStatus('not_started');
                  setCurrentQuestion(null);
                }} 
                variant="outline"
              >
                Réessayer
              </Button>
              <Button 
                onClick={() => window.location.reload()} 
                variant="outline"
              >
                Recharger
              </Button>
            </div>
          </div>
        </CardContent>
      </Card>
    );
  }

  // État de chargement
  if (isLoading) {
    return (
      <Card className="w-full">
        <CardContent className="flex items-center justify-center py-12">
          <div className="text-center">
            <Loader2 className="h-12 w-12 animate-spin mx-auto mb-4 text-blue-600" />
            <p className="text-lg font-medium text-gray-900">Initialisation du test...</p>
            <p className="text-gray-600">Préparation de votre évaluation personnalisée</p>
          </div>
        </CardContent>
      </Card>
    );
  }

  // Test terminé
  if (testStatus === 'completed') {
    return (
      <Card className="w-full">
        <CardHeader className="text-center">
          <div className="mx-auto w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mb-4">
            <Award className="h-8 w-8 text-green-600" />
          </div>
          <CardTitle className="text-2xl text-green-900">Test Terminé !</CardTitle>
          <p className="text-gray-600">Votre profil d'apprentissage français a été généré</p>
        </CardHeader>
        <CardContent className="space-y-6">
          {/* Résumé des performances */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="bg-blue-50 rounded-lg p-4 text-center">
              <div className="text-2xl font-bold text-blue-900">{questionsAnswered}</div>
              <div className="text-sm text-blue-700">Questions Répondues</div>
            </div>
            <div className="bg-green-50 rounded-lg p-4 text-center">
              <div className="text-2xl font-bold text-green-900">{Math.round((score / (questionsAnswered * 10)) * 100)}%</div>
              <div className="text-sm text-green-700">Score Final</div>
            </div>
            <div className="bg-purple-50 rounded-lg p-4 text-center">
              <div className="text-2xl font-bold text-purple-900">{testProgress?.current_level || 'A1'}</div>
              <div className="text-sm text-purple-700">Niveau Atteint</div>
            </div>
          </div>

          {/* Progression de difficulté */}
          {difficultyProgression.length > 0 && (
            <div>
              <h3 className="text-lg font-semibold text-gray-900 mb-3">Progression de Difficulté</h3>
              <div className="space-y-2">
                {difficultyProgression.slice(-10).map((prog, index) => (
                  <div key={index} className="flex items-center gap-3 text-sm">
                    <span className="text-gray-500">Q{prog.question_index}</span>
                    <Badge className={getDifficultyColor(prog.difficulty)}>
                      {getDifficultyLabel(prog.difficulty)}
                    </Badge>
                    <span className={prog.was_correct ? 'text-green-600' : 'text-red-600'}>
                      {prog.was_correct ? '✓' : '✗'}
                    </span>
                    <span className="text-gray-600">{prog.score}/10</span>
                  </div>
                ))}
              </div>
            </div>
          )}

          <div className="text-center">
            <Button 
              onClick={() => window.location.reload()}
              className="bg-blue-600 hover:bg-blue-700"
            >
              <BookOpen className="h-4 w-4 mr-2" />
              Voir Mon Profil Complet
            </Button>
          </div>
        </CardContent>
      </Card>
    );
  }

  // Test en cours
  if (testStatus === 'in_progress') {
    // Si pas de question actuelle mais que le test est en cours, afficher un message de chargement
    if (!currentQuestion) {
      console.log('⚠️ Test en cours mais pas de question actuelle, affichage du chargement');
      return (
        <Card className="w-full">
          <CardContent className="flex items-center justify-center py-12">
            <div className="text-center">
              <Loader2 className="h-12 w-12 animate-spin mx-auto mb-4 text-blue-600" />
              <p className="text-lg font-medium text-gray-900">Chargement de la question...</p>
              <p className="text-gray-600">Préparation de la prochaine question</p>
              <p className="text-sm text-gray-500 mt-2">Question {questionsAnswered + 1}</p>
            </div>
          </CardContent>
        </Card>
      );
    }

    // Vérification de sécurité pour éviter les erreurs
    if (!currentQuestion.question || !currentQuestion.options || !currentQuestion.correct) {
      console.error('❌ Question invalide reçue:', currentQuestion);
      return (
        <Card className="w-full">
          <CardContent className="flex items-center justify-center py-12">
            <div className="text-center">
              <AlertCircle className="h-12 w-12 text-red-600 mx-auto mb-4" />
              <p className="text-lg font-medium text-red-900">Erreur de chargement</p>
              <p className="text-gray-600">La question n'a pas pu être chargée correctement</p>
              <Button 
                onClick={() => window.location.reload()} 
                className="mt-4"
                variant="outline"
              >
                Recharger la page
              </Button>
            </div>
          </CardContent>
        </Card>
      );
    }
    return (
      <Card className="w-full">
        <CardHeader>
          <div className="flex items-center justify-between mb-4">
            <CardTitle className="text-xl">Évaluation Française Adaptative</CardTitle>
            <Badge className={getDifficultyColor(currentQuestion.difficulty)}>
              {getDifficultyLabel(currentQuestion.difficulty)}
            </Badge>
          </div>
          
          {/* Barre de progression */}
          <div className="space-y-2">
            <div className="flex justify-between text-sm text-gray-600">
              <span>Question {testProgress?.current || questionsAnswered + 1} / 20</span>
              <span>Progression: {getProgressPercentage().toFixed(1)}%</span>
            </div>
            <Progress value={getProgressPercentage()} className="h-2" />
            <div className="text-xs text-gray-500 text-center">
              Test à 20 questions - Progression adaptative selon vos performances
            </div>
          </div>
        </CardHeader>

        <CardContent className="space-y-6">
          {/* Question actuelle */}
          <div className="bg-gray-50 rounded-lg p-6">
            <div className="flex items-start gap-3 mb-4">
              <div className="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center flex-shrink-0">
                <span className="text-blue-600 font-semibold">{questionsAnswered + 1}</span>
              </div>
              <div>
                <h3 className="text-lg font-medium text-gray-900 mb-2">{currentQuestion.question}</h3>
                <Badge variant="outline" className="text-xs">
                  {currentQuestion.topic}
                </Badge>
              </div>
            </div>

            {/* Options de réponse */}
            <div className="space-y-3">
              {currentQuestion.options.map((option, index) => (
                <button
                  key={index}
                  onClick={() => setSelectedAnswer(option)}
                  className={`w-full p-4 text-left rounded-lg border-2 transition-all ${
                    selectedAnswer === option
                      ? 'border-blue-500 bg-blue-50 text-blue-900'
                      : 'border-gray-200 hover:border-gray-300 hover:bg-gray-50'
                  }`}
                >
                  <div className="flex items-center gap-3">
                    <div className={`w-5 h-5 rounded-full border-2 flex items-center justify-center ${
                      selectedAnswer === option ? 'border-blue-500 bg-blue-500' : 'border-gray-300'
                    }`}>
                      {selectedAnswer === option && (
                        <div className="w-2 h-2 bg-white rounded-full"></div>
                      )}
                    </div>
                    <span className="font-medium">{option}</span>
                  </div>
                </button>
              ))}
            </div>
          </div>

          {/* Actions */}
          <div className="flex justify-between items-center">
            <div className="text-sm text-gray-600">
              <div className="flex items-center gap-2">
                <Target className="h-4 w-4" />
                <span>Niveau actuel: {testProgress?.current_level || 'A1'}</span>
              </div>
              <div className="flex items-center gap-2 mt-1">
                <TrendingUp className="h-4 w-4" />
                <span>Score: {score}/{questionsAnswered * 10}</span>
              </div>
            </div>

            <Button
              onClick={submitAnswer}
              disabled={!selectedAnswer || isSubmitting}
              className="bg-blue-600 hover:bg-blue-700 disabled:opacity-50"
            >
              {isSubmitting ? (
                <>
                  <Loader2 className="h-4 w-4 animate-spin mr-2" />
                  Traitement...
                </>
              ) : (
                <>
                  <CheckCircle className="h-4 w-4 mr-2" />
                  Valider la Réponse
                </>
              )}
            </Button>
          </div>

          {/* Erreur */}
          {error && (
            <Alert variant="destructive">
              <XCircle className="h-4 w-4" />
              <AlertDescription>{error}</AlertDescription>
            </Alert>
          )}
        </CardContent>
      </Card>
    );
  }

  // Test non démarré
  return (
    <Card className="w-full">
      <CardHeader className="text-center">
        <div className="mx-auto w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mb-4">
          <Brain className="h-8 w-8 text-blue-600" />
        </div>
        <CardTitle className="text-2xl text-gray-900">Évaluation Française Adaptative</CardTitle>
        <p className="text-gray-600">
          Testez votre niveau de français avec notre système intelligent de 20 questions
        </p>
      </CardHeader>
      
      <CardContent className="space-y-6">
        {/* Informations sur le test */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="bg-blue-50 rounded-lg p-4">
            <div className="flex items-center gap-2 mb-2">
              <BookOpen className="h-5 w-5 text-blue-600" />
              <span className="font-medium text-blue-900">Test à 20 Questions</span>
            </div>
            <p className="text-sm text-blue-700">
              Évaluation complète avec questions mélangées (facile-moyen-difficile)
            </p>
          </div>
          
          <div className="bg-green-50 rounded-lg p-4">
            <div className="flex items-center gap-2 mb-2">
              <Target className="h-5 w-5 text-green-600" />
              <span className="font-medium text-green-900">Progression Intelligente</span>
            </div>
            <p className="text-sm text-green-700">
              Adaptation automatique selon vos performances
            </p>
          </div>
          
          <div className="bg-purple-50 rounded-lg p-4">
            <div className="flex items-center gap-2 mb-2">
              <Lightbulb className="h-5 w-5 text-purple-600" />
              <span className="font-medium text-purple-900">Profil Personnalisé</span>
            </div>
            <p className="text-sm text-purple-700">
              Génération IA de votre profil d'apprentissage après les 20 questions
            </p>
          </div>
          
          <div className="bg-orange-50 rounded-lg p-4">
            <div className="flex items-center gap-2 mb-2">
              <Clock className="h-5 w-5 text-orange-600" />
              <span className="font-medium text-orange-900">Durée Estimée</span>
            </div>
            <p className="text-sm text-orange-700">
              15-20 minutes pour 20 questions
            </p>
          </div>
        </div>

        {/* Bouton de démarrage */}
        <div className="text-center">
          <Button
            onClick={startTest}
            size="lg"
            className="bg-blue-600 hover:bg-blue-700 px-8 py-3 text-lg"
          >
            <Play className="h-5 w-5 mr-2" />
            Commencer l'Évaluation
          </Button>
        </div>

        {/* Erreur */}
        {error && (
          <Alert variant="destructive">
            <XCircle className="h-4 w-4" />
            <AlertDescription>{error}</AlertDescription>
          </Alert>
        )}
      </CardContent>
    </Card>
  );
};

export default FrenchAdaptiveTest;
