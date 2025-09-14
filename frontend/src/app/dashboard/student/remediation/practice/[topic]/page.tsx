'use client';

import React, { useState, useEffect } from 'react';
import { useParams, useRouter } from 'next/navigation';
import { useAuth } from '@/hooks/useAuth';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Progress } from '@/components/ui/progress';
import { Badge } from '@/components/ui/badge';
import { Input } from '@/components/ui/input';
import { ArrowLeft, Target, CheckCircle, XCircle, Clock, Trophy, Lightbulb } from 'lucide-react';

interface PracticeExercise {
  id: number;
  type: 'fill_blank' | 'multiple_choice' | 'matching' | 'ordering';
  question: string;
  content: any;
  correct_answer: any;
  explanation: string;
  difficulty: 'easy' | 'medium' | 'hard';
  points: number;
}

export default function RemediationPracticePage() {
  const { topic } = useParams();
  const router = useRouter();
  const { user, token } = useAuth();
  
  const [currentExerciseIndex, setCurrentExerciseIndex] = useState(0);
  const [userAnswer, setUserAnswer] = useState<any>(null);
  const [showResult, setShowResult] = useState(false);
  const [score, setScore] = useState(0);
  const [totalPoints, setTotalPoints] = useState(0);
  const [timeLeft, setTimeLeft] = useState(600); // 10 minutes
  const [practiceCompleted, setPracticeCompleted] = useState(false);
  const [completedExercises, setCompletedExercises] = useState<number[]>([]);

  const [exercises, setExercises] = useState<PracticeExercise[]>([]);

  useEffect(() => {
    if (topic) {
      generatePracticeExercises(topic as string);
    }
  }, [topic]);

  useEffect(() => {
    if (timeLeft > 0 && !practiceCompleted) {
      const timer = setInterval(() => setTimeLeft(prev => prev - 1), 1000);
      return () => clearInterval(timer);
    } else if (timeLeft === 0 && !practiceCompleted) {
      completePractice();
    }
  }, [timeLeft, practiceCompleted]);

  const generatePracticeExercises = (topic: string) => {
    const exerciseMap: { [key: string]: PracticeExercise[] } = {
      'fondamentaux': [
        {
          id: 1,
          type: 'fill_blank',
          question: "Complétez la phrase avec le bon article :",
          content: {
            sentence: "___ table est ___ meuble ___ salon.",
            blanks: [
              { id: 1, options: ["Le", "La", "Les", "Un"] },
              { id: 2, options: ["un", "une", "des", "du"] },
              { id: 3, options: ["du", "de la", "des", "le"] }
            ]
          },
          correct_answer: ["La", "un", "du"],
          explanation: "La table (féminin singulier) est un meuble (masculin singulier) du salon (préposition + article contracté).",
          difficulty: 'easy',
          points: 10
        },
        {
          id: 2,
          type: 'multiple_choice',
          question: "Quel est le genre du mot 'livre' ?",
          content: {
            options: ["Masculin", "Féminin", "Les deux", "Aucun"]
          },
          correct_answer: 0,
          explanation: "Le mot 'livre' est un nom masculin. On dit 'un livre'.",
          difficulty: 'easy',
          points: 5
        },
        {
          id: 3,
          type: 'ordering',
          question: "Remettez dans l'ordre les éléments de cette phrase :",
          content: {
            elements: ["belle", "une", "table", "ronde"],
            correctOrder: [1, 0, 3, 2] // une belle ronde table
          },
          correct_answer: [1, 0, 3, 2],
          explanation: "L'ordre correct est : Article (une) + Adjectif (belle) + Adjectif (ronde) + Nom (table).",
          difficulty: 'medium',
          points: 15
        }
      ],
      'conjugaison': [
        {
          id: 1,
          type: 'fill_blank',
          question: "Conjuguez le verbe 'parler' au présent :",
          content: {
            sentence: "Je ___, tu ___, il ___, nous ___, vous ___, ils ___.",
            blanks: [
              { id: 1, options: ["parle", "parles", "parlons", "parlez", "parlent"] },
              { id: 2, options: ["parle", "parles", "parlons", "parlez", "parlent"] },
              { id: 3, options: ["parle", "parles", "parlons", "parlez", "parlent"] },
              { id: 4, options: ["parle", "parles", "parlons", "parlez", "parlent"] },
              { id: 5, options: ["parle", "parles", "parlons", "parlez", "parlent"] },
              { id: 6, options: ["parle", "parles", "parlons", "parlez", "parlent"] }
            ]
          },
          correct_answer: ["parle", "parles", "parle", "parlons", "parlez", "parlent"],
          explanation: "Au présent : je parle, tu parles, il parle, nous parlons, vous parlez, ils parlent.",
          difficulty: 'medium',
          points: 20
        },
        {
          id: 2,
          type: 'matching',
          question: "Associez chaque verbe à son groupe :",
          content: {
            pairs: [
              { left: "parler", right: "1er groupe (-er)" },
              { left: "finir", right: "2ème groupe (-ir)" },
              { left: "être", right: "3ème groupe (irrégulier)" },
              { left: "manger", right: "1er groupe (-er)" }
            ]
          },
          correct_answer: [0, 1, 2, 0], // Indices des bonnes associations
          explanation: "Les verbes en -er sont du 1er groupe, ceux en -ir du 2ème groupe, et 'être' est du 3ème groupe.",
          difficulty: 'easy',
          points: 15
        }
      ],
      'vocabulaire': [
        {
          id: 1,
          type: 'matching',
          question: "Trouvez les synonymes de 'rapide' :",
          content: {
            pairs: [
              { left: "rapide", right: "vite" },
              { left: "rapide", right: "prompt" },
              { left: "rapide", right: "accéléré" },
              { left: "rapide", right: "hâtif" }
            ]
          },
          correct_answer: [0, 1, 2, 3], // Tous sont corrects
          explanation: "'Rapide', 'vite', 'prompt', 'accéléré' et 'hâtif' sont tous des synonymes exprimant la vitesse.",
          difficulty: 'medium',
          points: 20
        },
        {
          id: 2,
          type: 'multiple_choice',
          question: "Quel est l'antonyme de 'grand' ?",
          content: {
            options: ["Petit", "Moyen", "Énorme", "Large"]
          },
          correct_answer: 0,
          explanation: "L'antonyme de 'grand' est 'petit'. Ce sont des mots de sens opposé.",
          difficulty: 'easy',
          points: 10
        }
      ]
    };

    const selectedExercises = exerciseMap[topic.toLowerCase()] || exerciseMap['fondamentaux'];
    setExercises(selectedExercises);
    
    // Calculer le total des points disponibles
    const totalPointsAvailable = selectedExercises.reduce((sum, exercise) => sum + exercise.points, 0);
    setTotalPoints(totalPointsAvailable);
  };

  const handleAnswerSubmit = () => {
    if (userAnswer === null) return;

    const currentExercise = exercises[currentExerciseIndex];
    let isCorrect = false;

    // Vérifier la réponse selon le type d'exercice
    switch (currentExercise.type) {
      case 'fill_blank':
        isCorrect = JSON.stringify(userAnswer) === JSON.stringify(currentExercise.correct_answer);
        break;
      case 'multiple_choice':
        isCorrect = userAnswer === currentExercise.correct_answer;
        break;
      case 'matching':
        isCorrect = JSON.stringify(userAnswer) === JSON.stringify(currentExercise.correct_answer);
        break;
      case 'ordering':
        isCorrect = JSON.stringify(userAnswer) === JSON.stringify(currentExercise.correct_answer);
        break;
    }

    if (isCorrect) {
      setScore(prev => prev + currentExercise.points);
    }

    if (!completedExercises.includes(currentExercise.id)) {
      setCompletedExercises(prev => [...prev, currentExercise.id]);
    }

    setShowResult(true);
  };

  const handleNextExercise = () => {
    if (currentExerciseIndex < exercises.length - 1) {
      setCurrentExerciseIndex(prev => prev + 1);
      setUserAnswer(null);
      setShowResult(false);
    } else {
      completePractice();
    }
  };

  const completePractice = async () => {
    setPracticeCompleted(true);
    
    // Sauvegarder le résultat des exercices pratiques
    if (user && token) {
      try {
        const { RemediationService } = await import('@/services/remediationService');
        
        const result = {
          student_id: user.id,
          topic: topic as string,
          exercise_type: 'practice' as const,
          score: score,
          max_score: totalPoints,
          percentage: Math.round((score / totalPoints) * 100),
          time_spent: 600 - timeLeft, // Temps passé
          weak_areas_improved: [topic as string],
        };
        
        await RemediationService.saveRemediationResult(token, result);
        console.log('✅ [PRACTICE] Résultat des exercices sauvegardé:', result);
        
        // Mettre à jour l'analyse des lacunes
        await RemediationService.updateGapAnalysis(token, user.id, 'Français');
        console.log('✅ [PRACTICE] Analyse des lacunes mise à jour');
        
      } catch (error) {
        console.error('❌ [PRACTICE] Erreur sauvegarde résultat:', error);
      }
    }
  };

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  const renderExerciseContent = (exercise: PracticeExercise) => {
    switch (exercise.type) {
      case 'fill_blank':
        return (
          <div className="space-y-4">
            <p className="text-lg text-gray-700">
              {exercise.content.sentence.split('___').map((part: string, index: number) => (
                <span key={index}>
                  {part}
                  {index < exercise.content.blanks.length && (
                    <select
                      value={userAnswer?.[index] || ''}
                      onChange={(e) => {
                        const newAnswer = [...(userAnswer || [])];
                        newAnswer[index] = e.target.value;
                        setUserAnswer(newAnswer);
                      }}
                      className="mx-2 px-3 py-2 border border-gray-300 rounded-md bg-white"
                    >
                      <option value="">Choisir...</option>
                      {exercise.content.blanks[index].options.map((option: string, optIndex: number) => (
                        <option key={optIndex} value={option}>{option}</option>
                      ))}
                    </select>
                  )}
                </span>
              ))}
            </p>
          </div>
        );

      case 'multiple_choice':
        return (
          <div className="space-y-3">
            {exercise.content.options.map((option: string, index: number) => (
              <button
                key={index}
                onClick={() => setUserAnswer(index)}
                className={`w-full p-4 text-left rounded-lg border-2 transition-all ${
                  userAnswer === index
                    ? 'border-blue-500 bg-blue-50'
                    : 'border-gray-200 hover:border-gray-300'
                }`}
              >
                <div className="flex items-center space-x-3">
                  <div className={`w-6 h-6 rounded-full border-2 flex items-center justify-center ${
                    userAnswer === index
                      ? 'border-blue-500 bg-blue-500 text-white'
                      : 'border-gray-300'
                  }`}>
                    {userAnswer === index && (
                      <div className="w-2 h-2 bg-white rounded-full"></div>
                    )}
                  </div>
                  <span className="text-lg">{option}</span>
                </div>
              </button>
            ))}
          </div>
        );

      case 'matching':
        return (
          <div className="space-y-4">
            {exercise.content.pairs.map((pair: any, index: number) => (
              <div key={index} className="flex items-center justify-between p-3 border border-gray-200 rounded-lg">
                <span className="font-medium">{pair.left}</span>
                <span className="text-gray-500">→</span>
                <select
                  value={userAnswer?.[index] || ''}
                  onChange={(e) => {
                    const newAnswer = [...(userAnswer || [])];
                    newAnswer[index] = parseInt(e.target.value);
                    setUserAnswer(newAnswer);
                  }}
                  className="px-3 py-2 border border-gray-300 rounded-md bg-white"
                >
                  <option value="">Associer à...</option>
                  {exercise.content.pairs.map((p: any, pIndex: number) => (
                    <option key={pIndex} value={pIndex}>{p.right}</option>
                  ))}
                </select>
              </div>
            ))}
          </div>
        );

      case 'ordering':
        return (
          <div className="space-y-4">
            <p className="text-lg text-gray-700 mb-4">
              Cliquez sur les éléments dans l'ordre souhaité :
            </p>
            <div className="grid grid-cols-2 gap-4">
              {exercise.content.elements.map((element: string, index: number) => {
                const isSelected = userAnswer?.includes(index);
                const selectionIndex = userAnswer ? userAnswer.indexOf(index) : -1;
                
                return (
                  <button
                    key={index}
                    onClick={() => {
                      if (!userAnswer) {
                        setUserAnswer([index]);
                      } else if (userAnswer.includes(index)) {
                        // Retirer l'élément s'il est déjà sélectionné
                        setUserAnswer(userAnswer.filter(i => i !== index));
                      } else {
                        // Ajouter l'élément à la fin de la sélection
                        setUserAnswer([...userAnswer, index]);
                      }
                    }}
                    className={`p-3 border-2 rounded-lg text-center transition-all duration-200 ${
                      isSelected
                        ? 'border-blue-500 bg-blue-50 text-blue-700'
                        : 'border-gray-300 bg-white hover:border-gray-400 hover:bg-gray-50'
                    }`}
                  >
                    <div className="flex flex-col items-center space-y-2">
                      <span className="text-lg font-medium">{element}</span>
                      {isSelected && (
                        <div className="w-6 h-6 rounded-full bg-blue-500 text-white text-sm font-bold flex items-center justify-center">
                          {selectionIndex + 1}
                        </div>
                      )}
                    </div>
                  </button>
                );
              })}
            </div>
            {userAnswer && userAnswer.length > 0 && (
              <div className="mt-4 p-3 bg-blue-50 border border-blue-200 rounded-lg">
                <p className="text-sm text-blue-700 font-medium mb-2">Ordre sélectionné :</p>
                <div className="flex flex-wrap gap-2">
                  {userAnswer.map((index, orderIndex) => (
                    <span key={index} className="px-2 py-1 bg-blue-100 text-blue-800 rounded text-sm">
                      {orderIndex + 1}. {exercise.content.elements[index]}
                    </span>
                  ))}
                </div>
              </div>
            )}
            <p className="text-sm text-gray-600">
              Cliquez sur les éléments dans l'ordre souhaité. Cliquez à nouveau pour désélectionner.
            </p>
          </div>
        );

      default:
        return <p>Type d'exercice non reconnu</p>;
    }
  };

  if (!exercises.length) {
    return (
      <div className="min-h-screen bg-gray-50 p-6">
        <div className="max-w-4xl mx-auto">
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
            <p>Chargement des exercices pratiques...</p>
          </div>
        </div>
      </div>
    );
  }

  if (practiceCompleted) {
    const percentage = Math.round((score / totalPoints) * 100);
    return (
      <div className="min-h-screen bg-gray-50 p-6">
        <div className="max-w-4xl mx-auto">
          <Card className="mb-6">
            <CardHeader className="text-center">
              <CardTitle className="text-2xl text-green-600">
                Exercices Terminés ! 🎯✨
              </CardTitle>
            </CardHeader>
            <CardContent className="text-center space-y-4">
              <div className="text-4xl font-bold text-blue-600">
                {score}/{totalPoints} points
              </div>
              <div className="text-xl text-gray-600">
                Score : {percentage}%
              </div>
              <Progress value={percentage} className="w-full max-w-md mx-auto" />
              
              <div className="flex items-center justify-center space-x-2 text-yellow-600">
                <Trophy className="w-6 h-6" />
                <span className="text-lg font-semibold">
                  {percentage >= 80 ? 'Excellent !' : percentage >= 60 ? 'Bien !' : 'Continuez à pratiquer !'}
                </span>
              </div>
              
              <div className="flex justify-center space-x-4 mt-6">
                <Button 
                  onClick={() => router.push('/dashboard/student/remediation')}
                  variant="outline"
                >
                  <ArrowLeft className="w-4 h-4 mr-2" />
                  Retour au Plan
                </Button>
                <Button 
                  onClick={() => window.location.reload()}
                  className="bg-blue-600 hover:bg-blue-700"
                >
                  Recommencer
                </Button>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    );
  }

  const currentExercise = exercises[currentExerciseIndex];
  const progress = ((currentExerciseIndex + 1) / exercises.length) * 100;

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="flex items-center justify-between mb-6">
          <Button 
            variant="outline" 
            onClick={() => router.push('/dashboard/student/remediation')}
          >
            <ArrowLeft className="w-4 h-4 mr-2" />
            Retour
          </Button>
          
          <div className="text-center">
            <h1 className="text-2xl font-bold text-gray-900">
              Exercices Pratiques - {topic?.charAt(0).toUpperCase() + topic?.slice(1)}
            </h1>
            <p className="text-gray-600">Exercice {currentExerciseIndex + 1} sur {exercises.length}</p>
          </div>

          <div className="flex items-center space-x-4">
            <div className="flex items-center space-x-2">
              <Clock className="w-4 h-4 text-red-500" />
              <span className="font-mono text-lg">{formatTime(timeLeft)}</span>
            </div>
            <Badge variant="secondary">
              Score: {score} points
            </Badge>
          </div>
        </div>

        {/* Progress Bar */}
        <div className="mb-6">
          <Progress value={progress} className="w-full" />
          <div className="flex justify-between text-sm text-gray-600 mt-1">
            <span>Progression</span>
            <span>{Math.round(progress)}%</span>
          </div>
        </div>

        {/* Exercise Card */}
        <Card className="mb-6">
          <CardHeader>
            <div className="flex items-center justify-between">
              <CardTitle className="text-xl">
                {currentExercise.question}
              </CardTitle>
              <div className="flex items-center space-x-3">
                <Badge 
                  variant={currentExercise.difficulty === 'easy' ? 'default' : 
                          currentExercise.difficulty === 'medium' ? 'secondary' : 'destructive'}
                >
                  {currentExercise.difficulty === 'easy' ? 'Facile' : 
                   currentExercise.difficulty === 'medium' ? 'Intermédiaire' : 'Difficile'}
                </Badge>
                <Badge variant="outline">
                  {currentExercise.points} points
                </Badge>
              </div>
            </div>
          </CardHeader>
          
          <CardContent className="space-y-6">
            {/* Exercise Content */}
            {renderExerciseContent(currentExercise)}

            {/* Result and Navigation */}
            {showResult && (
              <div className="mt-6 p-4 bg-gray-50 rounded-lg">
                <div className="flex items-center space-x-2 mb-3">
                  {JSON.stringify(userAnswer) === JSON.stringify(currentExercise.correct_answer) ? (
                    <CheckCircle className="w-5 h-5 text-green-600" />
                  ) : (
                    <XCircle className="w-5 h-5 text-red-600" />
                  )}
                  <span className={`font-semibold ${
                    JSON.stringify(userAnswer) === JSON.stringify(currentExercise.correct_answer) ? 'text-green-600' : 'text-red-600'
                  }`}>
                    {JSON.stringify(userAnswer) === JSON.stringify(currentExercise.correct_answer) ? 'Correct !' : 'Incorrect'}
                  </span>
                </div>
                
                <p className="text-gray-700 mb-4">
                  <strong>Explication :</strong> {currentExercise.explanation}
                </p>

                <Button 
                  onClick={handleNextExercise}
                  className="w-full bg-blue-600 hover:bg-blue-700"
                >
                  {currentExerciseIndex < exercises.length - 1 ? 'Exercice Suivant' : 'Terminer les Exercices'}
                </Button>
              </div>
            )}

            {!showResult && (
              <Button 
                onClick={handleAnswerSubmit}
                disabled={userAnswer === null}
                className="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400"
              >
                Valider la Réponse
              </Button>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
