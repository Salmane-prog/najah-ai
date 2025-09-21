'use client';

import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Progress } from '@/components/ui/progress';
import { Badge } from '@/components/ui/badge';
import { 
  Play, 
  Pause, 
  CheckCircle, 
  XCircle, 
  Clock, 
  User,
  BookOpen,
  Target
} from 'lucide-react';
import { testTrackingService } from '@/services/testTrackingService';

interface StudentTest {
  id: number;
  title: string;
  subject: string;
  questions: Array<{
    id: number;
    question: string;
    options: string[];
    correctAnswer: number;
  }>;
  duration: number;
}

interface TestSession {
  attemptId: string;
  test: StudentTest;
  currentQuestion: number;
  answers: number[];
  startTime: Date;
  timeSpent: number;
  status: 'not_started' | 'in_progress' | 'completed' | 'abandoned';
}

const MOCK_TESTS: StudentTest[] = [
  {
    id: 1,
    title: "Test Mathématiques - Niveau Intermédiaire",
    subject: "Mathématiques",
    duration: 30,
    questions: [
      {
        id: 1,
        question: "Quel est le résultat de 15 × 8 ?",
        options: ["100", "110", "120", "130"],
        correctAnswer: 2
      },
      {
        id: 2,
        question: "Quelle est la fraction équivalente à 0.75 ?",
        options: ["1/4", "2/4", "3/4", "4/4"],
        correctAnswer: 2
      },
      {
        id: 3,
        question: "Quel est le périmètre d'un carré de côté 6 cm ?",
        options: ["12 cm", "18 cm", "24 cm", "36 cm"],
        correctAnswer: 2
      },
      {
        id: 4,
        question: "Quel est le résultat de 48 ÷ 6 ?",
        options: ["6", "7", "8", "9"],
        correctAnswer: 2
      },
      {
        id: 5,
        question: "Quelle est l'aire d'un rectangle de 8 cm × 5 cm ?",
        options: ["13 cm²", "26 cm²", "40 cm²", "45 cm²"],
        correctAnswer: 2
      }
    ]
  },
  {
    id: 2,
    title: "Test Français - Grammaire et Conjugaison",
    subject: "Français",
    duration: 25,
    questions: [
      {
        id: 1,
        question: "Quelle est la bonne conjugaison : 'Je _____ à l'école' ?",
        options: ["vais", "va", "vont", "allez"],
        correctAnswer: 0
      },
      {
        id: 2,
        question: "Quel est le pluriel de 'journal' ?",
        options: ["journaux", "journals", "journales", "journaux"],
        correctAnswer: 0
      },
      {
        id: 3,
        question: "Quelle est la nature du mot 'rapidement' ?",
        options: ["nom", "verbe", "adverbe", "adjectif"],
        correctAnswer: 2
      },
      {
        id: 4,
        question: "Conjuguez 'avoir' à la 3ème personne du pluriel au présent :",
        options: ["a", "as", "ont", "avez"],
        correctAnswer: 2
      },
      {
        id: 5,
        question: "Quel est le féminin de 'beau' ?",
        options: ["beau", "belle", "beaux", "belles"],
        correctAnswer: 1
      }
    ]
  }
];

export default function StudentTestSimulator() {
  const [selectedTest, setSelectedTest] = useState<StudentTest | null>(null);
  const [testSession, setTestSession] = useState<TestSession | null>(null);
  const [studentName, setStudentName] = useState('');
  const [studentId, setStudentId] = useState(1);
  const [timer, setTimer] = useState(0);
  const [isTimerRunning, setIsTimerRunning] = useState(false);

  // Timer effect
  useEffect(() => {
    let interval: NodeJS.Timeout;
    
    if (isTimerRunning && testSession && testSession.status === 'in_progress') {
      interval = setInterval(() => {
        setTimer(prev => {
          const newTime = prev + 1;
          
          // Mettre à jour le temps passé dans la session
          if (testSession) {
            setTestSession(prev => prev ? {
              ...prev,
              timeSpent: newTime
            } : null);
          }
          
          return newTime;
        });
      }, 1000);
    }

    return () => {
      if (interval) clearInterval(interval);
    };
  }, [isTimerRunning, testSession]);

  const startTest = async (test: StudentTest) => {
    if (!studentName.trim()) {
      alert('Veuillez entrer votre nom');
      return;
    }

    try {
      console.log('🚀 Démarrage du test:', test.title);
      
      // Démarrer le test via le service de tracking
      const attemptId = await testTrackingService.startTest(
        test.id,
        studentId,
        studentName
      );

      const session: TestSession = {
        attemptId,
        test,
        currentQuestion: 0,
        answers: new Array(test.questions.length).fill(-1),
        startTime: new Date(),
        timeSpent: 0,
        status: 'in_progress'
      };

      setTestSession(session);
      setSelectedTest(test);
      setTimer(0);
      setIsTimerRunning(true);

      console.log('✅ Test démarré avec succès, ID:', attemptId);
    } catch (error) {
      console.error('❌ Erreur lors du démarrage du test:', error);
      alert('Erreur lors du démarrage du test');
    }
  };

  const answerQuestion = (answerIndex: number) => {
    if (!testSession) return;

    const newAnswers = [...testSession.answers];
    newAnswers[testSession.currentQuestion] = answerIndex;

    setTestSession({
      ...testSession,
      answers: newAnswers
    });

    // Mettre à jour le progrès via le service de tracking
    testTrackingService.updateProgress(
      testSession.attemptId,
      newAnswers.filter(a => a !== -1).length,
      testSession.test.questions.length
    );
  };

  const nextQuestion = () => {
    if (!testSession) return;
    
    if (testSession.currentQuestion < testSession.test.questions.length - 1) {
      setTestSession({
        ...testSession,
        currentQuestion: testSession.currentQuestion + 1
      });
    }
  };

  const previousQuestion = () => {
    if (!testSession && testSession.currentQuestion > 0) return;
    
    setTestSession({
      ...testSession,
      currentQuestion: testSession.currentQuestion - 1
    });
  };

  const completeTest = async () => {
    if (!testSession) return;

    try {
      // Calculer le score
      const correctAnswers = testSession.answers.filter((answer, index) => 
        answer === testSession.test.questions[index].correctAnswer
      ).length;
      
      const score = (correctAnswers / testSession.test.questions.length) * 100;

      console.log('✅ Completion du test, score:', score.toFixed(1) + '%');

      // Terminer le test via le service de tracking
      await testTrackingService.completeTest(testSession.attemptId, score);

      setTestSession({
        ...testSession,
        status: 'completed'
      });
      setIsTimerRunning(false);

      alert(`Test terminé ! Score: ${score.toFixed(1)}%`);
    } catch (error) {
      console.error('❌ Erreur lors de la completion du test:', error);
      alert('Erreur lors de la completion du test');
    }
  };

  const abandonTest = async () => {
    if (!testSession) return;

    try {
      console.log('❌ Abandon du test');

      // Abandonner le test via le service de tracking
      await testTrackingService.abandonTest(testSession.attemptId);

      setTestSession({
        ...testSession,
        status: 'abandoned'
      });
      setIsTimerRunning(false);

      alert('Test abandonné');
    } catch (error) {
      console.error('❌ Erreur lors de l\'abandon du test:', error);
      alert('Erreur lors de l\'abandon du test');
    }
  };

  const resetTest = () => {
    setTestSession(null);
    setSelectedTest(null);
    setTimer(0);
    setIsTimerRunning(false);
  };

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  };

  if (!selectedTest && !testSession) {
    return (
      <div className="space-y-6">
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <User className="w-5 h-5 text-blue-600" />
              Simulateur de Test Étudiant
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="grid grid-cols-2 gap-4">
              <div>
                <Label htmlFor="studentName">Nom de l'étudiant</Label>
                <Input
                  id="studentName"
                  value={studentName}
                  onChange={(e) => setStudentName(e.target.value)}
                  placeholder="Entrez votre nom"
                />
              </div>
              <div>
                <Label htmlFor="studentId">ID Étudiant</Label>
                <Input
                  id="studentId"
                  type="number"
                  value={studentId}
                  onChange={(e) => setStudentId(parseInt(e.target.value))}
                  placeholder="1"
                />
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {MOCK_TESTS.map((test) => (
                <Card key={test.id} className="cursor-pointer hover:shadow-md transition-shadow">
                  <CardContent className="p-4">
                    <div className="flex items-center gap-2 mb-2">
                      <BookOpen className="w-4 h-4 text-green-600" />
                      <h3 className="font-semibold">{test.title}</h3>
                    </div>
                    <div className="flex items-center gap-2 mb-3">
                      <Target className="w-4 h-4 text-blue-600" />
                      <span className="text-sm text-gray-600">{test.subject}</span>
                      <Badge variant="secondary">{test.questions.length} questions</Badge>
                      <Badge variant="outline">{test.duration} min</Badge>
                    </div>
                    <Button 
                      onClick={() => startTest(test)}
                      className="w-full"
                      disabled={!studentName.trim()}
                    >
                      <Play className="w-4 h-4 mr-2" />
                      Commencer le Test
                    </Button>
                  </CardContent>
                </Card>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>
    );
  }

  if (!testSession) return null;

  const currentQuestion = testSession.test.questions[testSession.currentQuestion];
  const progress = (testSession.currentQuestion + 1) / testSession.test.questions.length;
  const answeredQuestions = testSession.answers.filter(a => a !== -1).length;

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <BookOpen className="w-5 h-5 text-green-600" />
              {testSession.test.title}
            </div>
            <div className="flex items-center gap-4">
              <div className="flex items-center gap-2">
                <Clock className="w-4 h-4 text-orange-600" />
                <span className="font-mono">{formatTime(timer)}</span>
              </div>
              <div className="flex items-center gap-2">
                <User className="w-4 h-4 text-blue-600" />
                <span>{studentName}</span>
              </div>
            </div>
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-6">
          {/* Barre de progression */}
          <div className="space-y-2">
            <div className="flex justify-between text-sm">
              <span>Progression: {testSession.currentQuestion + 1} / {testSession.test.questions.length}</span>
              <span>Questions répondues: {answeredQuestions} / {testSession.test.questions.length}</span>
            </div>
            <Progress value={progress * 100} className="h-2" />
          </div>

          {/* Question actuelle */}
          <div className="space-y-4">
            <div className="bg-gray-50 p-4 rounded-lg">
              <h3 className="font-semibold mb-3">
                Question {testSession.currentQuestion + 1} : {currentQuestion.question}
              </h3>
              
              <div className="space-y-2">
                {currentQuestion.options.map((option, index) => (
                  <button
                    key={index}
                    onClick={() => answerQuestion(index)}
                    className={`w-full p-3 text-left rounded-lg border transition-colors ${
                      testSession.answers[testSession.currentQuestion] === index
                        ? 'bg-blue-100 border-blue-500 text-blue-700'
                        : 'bg-white border-gray-200 hover:bg-gray-50'
                    }`}
                  >
                    <span className="font-medium mr-2">{String.fromCharCode(65 + index)}.</span>
                    {option}
                  </button>
                ))}
              </div>
            </div>

            {/* Navigation */}
            <div className="flex justify-between">
              <Button
                onClick={previousQuestion}
                disabled={testSession.currentQuestion === 0}
                variant="outline"
              >
                ← Question précédente
              </Button>

              {testSession.currentQuestion < testSession.test.questions.length - 1 ? (
                <Button
                  onClick={nextQuestion}
                  disabled={testSession.answers[testSession.currentQuestion] === -1}
                >
                  Question suivante →
                </Button>
              ) : (
                <Button
                  onClick={completeTest}
                  disabled={answeredQuestions < testSession.test.questions.length}
                  className="bg-green-600 hover:bg-green-700"
                >
                  <CheckCircle className="w-4 h-4 mr-2" />
                  Terminer le Test
                </Button>
              )}
            </div>

            {/* Bouton d'abandon */}
            <div className="text-center">
              <Button
                onClick={abandonTest}
                variant="destructive"
                size="sm"
              >
                <XCircle className="w-4 h-4 mr-2" />
                Abandonner le Test
              </Button>
            </div>
          </div>

          {/* Résumé des réponses */}
          <div className="bg-gray-50 p-4 rounded-lg">
            <h4 className="font-semibold mb-3">Résumé des réponses</h4>
            <div className="grid grid-cols-5 gap-2">
              {testSession.answers.map((answer, index) => (
                <div
                  key={index}
                  className={`p-2 text-center rounded text-sm font-medium ${
                    answer === -1
                      ? 'bg-gray-200 text-gray-500'
                      : 'bg-green-100 text-green-700'
                  }`}
                >
                  {index + 1}
                </div>
              ))}
            </div>
            <p className="text-sm text-gray-600 mt-2">
              Questions répondues: {answeredQuestions} / {testSession.test.questions.length}
            </p>
          </div>
        </CardContent>
      </Card>

      {/* Bouton de retour */}
      <div className="text-center">
        <Button onClick={resetTest} variant="outline">
          ← Retour à la sélection des tests
        </Button>
      </div>
    </div>
  );
}


















