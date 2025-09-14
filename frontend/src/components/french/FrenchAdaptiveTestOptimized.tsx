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
  AlertCircle,
  BarChart3,
  Zap
} from 'lucide-react';

interface Question {
  id: number;
  question: string;
  options: string[];
  correct: string;
  explanation: string;
  difficulty: string;
  topic: string;
}

interface TestProgress {
  current: number;
  total: number;
  difficulty: string;
  level_progression: string;
  current_level: string;
}

interface TestData {
  test_id: number;
  status: string;
  current_question: Question;
  progress: TestProgress;
  questions_sequence?: number[];
  current_question_id?: number;
}

interface FrenchAdaptiveTestOptimizedProps {
  studentId: number;
  onTestComplete: () => void;
  testData?: TestData | null;
  token: string;
}

const FrenchAdaptiveTestOptimized: React.FC<FrenchAdaptiveTestOptimizedProps> = ({
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
  const [finalProfile, setFinalProfile] = useState<any>(null);

  const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
  const OPTIMIZED_API_PATH = '/api/v1/french-optimized';

  useEffect(() => {
    if (testData) {
      setTestStatus(testData.status === 'completed' ? 'completed' : 'in_progress');
      setCurrentQuestion(testData.current_question);
      setTestProgress(testData.progress);
      setTestId(testData.test_id);
      
      if (testData.status === 'in_progress') {
        setQuestionsAnswered(testData.progress.current);
      }
    }
  }, [testData]);

  const startTest = async () => {
    try {
      setIsLoading(true);
      setError(null);

      console.log('🚀 Démarrage du test optimisé pour l\'étudiant:', studentId);

      const response = await fetch(`${API_BASE}${OPTIMIZED_API_PATH}/student/start`, {
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
      console.log('✅ Test optimisé démarré avec succès:', data);

      if (!data.success) {
        throw new Error(data.message || 'Erreur lors du démarrage du test');
      }

      // Validation des données reçues
      if (!data.current_question) {
        throw new Error('Aucune question reçue du serveur');
      }

      // Mise à jour de l'état
      setTestStatus('in_progress');
      setCurrentQuestion(data.current_question);
      setTestProgress(data.progress);
      setTestId(data.test_id);
      setQuestionsAnswered(data.progress.current);
      setScore(0);
      setDifficultyProgression([]);

      console.log('✅ État du test optimisé mis à jour:', {
        status: 'in_progress',
        questionId: data.current_question.id,
        testId: data.test_id,
        progress: data.progress
      });

    } catch (error) {
      console.error('❌ Erreur démarrage test optimisé:', error);
      setError(`Erreur lors du démarrage: ${error instanceof Error ? error.message : 'Erreur inconnue'}`);
      
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

      console.log('📝 Soumission réponse optimisée:', {
        answer: selectedAnswer,
        correct: currentQuestion.correct,
        wasCorrect,
        testId: testId
      });

      const response = await fetch(`${API_BASE}${OPTIMIZED_API_PATH}/${testId}/submit`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          answer: selectedAnswer
        })
      });

      if (!response.ok) {
        throw new Error(`Erreur ${response.status}: ${response.statusText}`);
      }

      const data = await response.json();
      console.log('✅ Réponse soumise avec succès:', data);

      if (!data.success) {
        throw new Error(data.message || 'Erreur lors de la soumission');
      }

      // Mettre à jour l'état local
      setScore(prev => prev + questionScore);
      const newQuestionIndex = questionsAnswered + 1;
      setQuestionsAnswered(newQuestionIndex);
      
      // Enregistrer la progression de difficulté
      setDifficultyProgression(prev => [...prev, {
        question_index: newQuestionIndex,
        difficulty: currentQuestion.difficulty,
        score: questionScore,
        was_correct: wasCorrect
      }]);

      // Vérifier si le test est terminé
      if (data.status === 'completed') {
        console.log('🏁 Test optimisé terminé, passage à l\'état completed');
        setTestStatus('completed');
        setTestProgress({
          current: 20,
          total: 20,
          difficulty: 'completed',
          level_progression: data.profile?.french_level || 'A1',
          current_level: data.profile?.french_level || 'A1'
        });
        setFinalProfile(data.profile);
        setScore(prev => prev + questionScore); // Mettre à jour le score final
        setQuestionsAnswered(20); // Forcer à 20 questions
        onTestComplete();
        return; // IMPORTANT: Arrêter ici pour éviter la progression
      } else if (data.next_question) {
        // Charger la prochaine question
        console.log('➡️ Passage à la question suivante:', data.next_question);
        setCurrentQuestion(data.next_question);
        setTestProgress(data.progress);
        setSelectedAnswer('');
      } else {
        console.error('❌ Pas de question suivante reçue du backend optimisé');
        setError('Erreur: Pas de question suivante reçue du serveur');
      }

    } catch (error) {
      console.error('❌ Erreur soumission réponse optimisée:', error);
      setError(`Erreur lors de la soumission: ${error instanceof Error ? error.message : 'Erreur inconnue'}`);
    } finally {
      setIsSubmitting(false);
    }
  };

  const getDifficultyColor = (difficulty: string) => {
    switch (difficulty.toLowerCase()) {
      case 'easy': 
      case 'facile': return 'bg-green-100 text-green-800';
      case 'medium': 
      case 'moyen': return 'bg-yellow-100 text-yellow-800';
      case 'hard': 
      case 'difficile': return 'bg-red-100 text-red-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const getDifficultyLabel = (difficulty: string) => {
    switch (difficulty.toLowerCase()) {
      case 'easy': return 'Facile';
      case 'medium': return 'Moyen';
      case 'hard': return 'Difficile';
      case 'facile': return 'Facile';
      case 'moyen': return 'Moyen';
      case 'difficile': return 'Difficile';
      default: return difficulty;
    }
  };

  const getProgressPercentage = () => {
    if (!testProgress) return 0;
    // Toujours sur 20 questions
    return (testProgress.current / 20) * 100;
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
            <p className="text-lg font-medium text-gray-900">Initialisation du test optimisé...</p>
            <p className="text-gray-600">Sélection intelligente de 20 questions personnalisées</p>
          </div>
        </CardContent>
      </Card>
    );
  }

  // Test terminé avec profil généré
  if (testStatus === 'completed') {
    return (
      <Card className="w-full">
        <CardHeader className="text-center">
          <div className="mx-auto w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mb-4">
            <Award className="h-8 w-8 text-green-600" />
          </div>
          <CardTitle className="text-2xl text-green-900">Test Terminé avec Succès !</CardTitle>
          <p className="text-gray-600">Votre profil d'apprentissage français a été généré par IA</p>
          <div className="mt-2 p-2 bg-yellow-50 border border-yellow-200 rounded-lg">
            <p className="text-sm text-yellow-800">
              🔒 <strong>Test verrouillé</strong> - Vous avez terminé les 20 questions. 
              Impossible de recommencer sans intervention administrateur.
            </p>
          </div>
        </CardHeader>
        <CardContent className="space-y-6">
          {/* Résumé des performances */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="bg-blue-50 rounded-lg p-4 text-center">
              <div className="text-2xl font-bold text-blue-900">20</div>
              <div className="text-sm text-blue-700">Questions Complétées</div>
            </div>
            <div className="bg-green-50 rounded-lg p-4 text-center">
              <div className="text-2xl font-bold text-green-900">
                {Math.round((score / 200) * 100)}%
              </div>
              <div className="text-sm text-green-700">Score Final</div>
            </div>
            <div className="bg-purple-50 rounded-lg p-4 text-center">
              <div className="text-2xl font-bold text-purple-900">
                {finalProfile?.french_level || testProgress?.current_level || 'A1'}
              </div>
              <div className="text-sm text-purple-700">Niveau Atteint</div>
            </div>
          </div>

          {/* Profil généré */}
          {finalProfile && (
            <div className="bg-gradient-to-r from-blue-50 to-purple-50 rounded-lg p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center gap-2">
                <Brain className="h-5 w-5 text-blue-600" />
                Votre Profil d'Apprentissage IA
              </h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <p className="text-sm font-medium text-gray-700">Style d'apprentissage</p>
                  <p className="text-lg text-gray-900 capitalize">{finalProfile.learning_style}</p>
                </div>
                <div>
                  <p className="text-sm font-medium text-gray-700">Rythme préféré</p>
                  <p className="text-lg text-gray-900 capitalize">{finalProfile.preferred_pace}</p>
                </div>
              </div>
              
              {finalProfile.strengths && finalProfile.strengths.length > 0 && (
                <div className="mt-4">
                  <p className="text-sm font-medium text-gray-700 mb-2">Forces identifiées</p>
                  <div className="flex flex-wrap gap-2">
                    {JSON.parse(finalProfile.strengths).map((strength: string, index: number) => (
                      <Badge key={index} className="bg-green-100 text-green-800">
                        {strength}
                      </Badge>
                    ))}
                  </div>
                </div>
              )}
            </div>
          )}

          {/* Progression de difficulté */}
          <div>
            <h3 className="text-lg font-semibold text-gray-900 mb-3 flex items-center gap-2">
              <BarChart3 className="h-5 w-5 text-purple-600" />
              Progression par Difficulté
            </h3>
            <div className="space-y-2">
              {difficultyProgression.slice(-10).map((prog, index) => (
                <div key={index} className="flex items-center gap-3 text-sm">
                  <span className="text-gray-500 w-8">Q{prog.question_index}</span>
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

          <div className="text-center space-y-3">
            <Button 
              onClick={() => {
                // Rediriger vers l'onglet profil au lieu de recharger
                const event = new CustomEvent('switchToProfile');
                window.dispatchEvent(event);
              }}
              className="bg-blue-600 hover:bg-blue-700"
            >
              <BookOpen className="h-4 w-4 mr-2" />
              Voir Mon Profil Complet
            </Button>
            
            <div className="text-sm text-gray-500">
              🔒 Le test est verrouillé. Contactez un administrateur si vous devez le repasser.
            </div>
          </div>
        </CardContent>
      </Card>
    );
  }

  // Test en cours
  if (testStatus === 'in_progress') {
    if (!currentQuestion) {
      return (
        <Card className="w-full">
          <CardContent className="flex items-center justify-center py-12">
            <div className="text-center">
              <Loader2 className="h-12 w-12 animate-spin mx-auto mb-4 text-blue-600" />
              <p className="text-lg font-medium text-gray-900">Chargement de la question...</p>
              <p className="text-gray-600">Question {questionsAnswered + 1}/20</p>
            </div>
          </CardContent>
        </Card>
      );
    }

    return (
      <Card className="w-full">
        <CardHeader>
          <div className="flex items-center justify-between mb-4">
            <CardTitle className="text-xl">Évaluation Française - 20 Questions</CardTitle>
            <Badge className={getDifficultyColor(currentQuestion.difficulty)}>
              {getDifficultyLabel(currentQuestion.difficulty)}
            </Badge>
          </div>
          
          {/* Barre de progression optimisée */}
          <div className="space-y-2">
            <div className="flex justify-between text-sm text-gray-600">
              <span>Question {testProgress?.current || 1} / 20</span>
              <span>Progression: {getProgressPercentage().toFixed(1)}%</span>
            </div>
            <Progress value={getProgressPercentage()} className="h-3" />
            <div className="text-xs text-gray-500 text-center">
              Test à 20 questions exactes - Répartition intelligente par difficulté
            </div>
          </div>
        </CardHeader>

        <CardContent className="space-y-6">
          {/* Question actuelle */}
          <div className="bg-gray-50 rounded-lg p-6">
            <div className="flex items-start gap-3 mb-4">
              <div className="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center flex-shrink-0">
                <span className="text-blue-600 font-semibold">{testProgress?.current || 1}</span>
              </div>
              <div>
                <h3 className="text-lg font-medium text-gray-900 mb-2">{currentQuestion.question}</h3>
                <div className="flex items-center gap-2">
                  <Badge variant="outline" className="text-xs">
                    {currentQuestion.topic}
                  </Badge>
                  <Badge className={getDifficultyColor(currentQuestion.difficulty)} variant="outline">
                    {getDifficultyLabel(currentQuestion.difficulty)}
                  </Badge>
                </div>
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

          {/* Actions et informations */}
          <div className="flex justify-between items-center">
            <div className="text-sm text-gray-600 space-y-1">
              <div className="flex items-center gap-2">
                <Target className="h-4 w-4" />
                <span>Niveau: {testProgress?.current_level || 'A1'}</span>
              </div>
              <div className="flex items-center gap-2">
                <TrendingUp className="h-4 w-4" />
                <span>Score: {score}/200 pts</span>
              </div>
              <div className="flex items-center gap-2">
                <Zap className="h-4 w-4" />
                <span>Restant: {20 - (testProgress?.current || 1)} questions</span>
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
        <CardTitle className="text-2xl text-gray-900">Évaluation Française Optimisée</CardTitle>
        <p className="text-gray-600">
          Test intelligent de 20 questions avec sélection adaptative et génération de profil IA
        </p>
      </CardHeader>
      
      <CardContent className="space-y-6">
        {/* Informations sur le test optimisé */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="bg-blue-50 rounded-lg p-4">
            <div className="flex items-center gap-2 mb-2">
              <Target className="h-5 w-5 text-blue-600" />
              <span className="font-medium text-blue-900">20 Questions Exactes</span>
            </div>
            <p className="text-sm text-blue-700">
              Répartition optimale : 7 facile + 6 moyen + 7 difficile
            </p>
          </div>
          
          <div className="bg-green-50 rounded-lg p-4">
            <div className="flex items-center gap-2 mb-2">
              <Zap className="h-5 w-5 text-green-600" />
              <span className="font-medium text-green-900">Sélection Intelligente</span>
            </div>
            <p className="text-sm text-green-700">
              Questions non répétitives issues de votre banque existante
            </p>
          </div>
          
          <div className="bg-purple-50 rounded-lg p-4">
            <div className="flex items-center gap-2 mb-2">
              <Brain className="h-5 w-5 text-purple-600" />
              <span className="font-medium text-purple-900">Profil IA Avancé</span>
            </div>
            <p className="text-sm text-purple-700">
              Analyse cognitive et recommandations personnalisées
            </p>
          </div>
          
          <div className="bg-orange-50 rounded-lg p-4">
            <div className="flex items-center gap-2 mb-2">
              <Clock className="h-5 w-5 text-orange-600" />
              <span className="font-medium text-orange-900">Durée Optimisée</span>
            </div>
            <p className="text-sm text-orange-700">
              15-20 minutes pour un test complet et précis
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
            Commencer l'Évaluation Optimisée
          </Button>
        </div>
      </CardContent>
    </Card>
  );
};

export default FrenchAdaptiveTestOptimized;
