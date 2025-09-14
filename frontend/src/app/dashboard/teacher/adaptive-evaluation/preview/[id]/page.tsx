'use client';

import React, { useState, useEffect } from 'react';
import { ArrowLeft, Eye, Clock, Target, BookOpen, Users } from 'lucide-react';
import Link from 'next/link';

interface Question {
  id: number;
  question: string;
  type: string;
  difficulty: number;
  options: string[];
  correctAnswer: number;
  explanation: string;
  learningObjective: string;
}

interface Test {
  id: number;
  title: string;
  subject: string;
  description: string;
  difficulty_range_min: number;
  difficulty_range_max: number;
  estimated_duration: number;
  question_count: number;
  student_count: number;
  questions: Question[];
}

export default function PreviewTest({ params }: { params: { id: string } }) {
  const [test, setTest] = useState<Test | null>(null);
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [selectedAnswers, setSelectedAnswers] = useState<number[]>([]);
  const [showResults, setShowResults] = useState(false);

  useEffect(() => {
    // Récupérer le test depuis localStorage
    const previewTest = localStorage.getItem('previewTest');
    if (previewTest) {
      const testData = JSON.parse(previewTest);
      
      // Si le test n'a pas de questions ou des questions incomplètes, générer des questions par défaut
      if (!testData.questions || testData.questions.length === 0 || 
          testData.questions[0].options === undefined || testData.questions[0].options.length === 0) {
        
        const enhancedTest = {
          ...testData,
          questions: generateDefaultQuestions(testData.subject || 'Français', testData.question_count || 5)
        };
        setTest(enhancedTest);
      } else {
        setTest(testData);
      }
    }
  }, []);

  // Fonction pour générer des questions par défaut si le test n'en a pas
  const generateDefaultQuestions = (subject: string, count: number) => {
    const questionsBySubject = {
      'Français': [
        {
          question: "Quelle est la forme correcte du verbe 'aller' à la 3ème personne du pluriel du présent ?",
          options: ["vont", "allez", "allons", "va"],
          correctAnswer: 0,
          explanation: "Le verbe 'aller' à la 3ème personne du pluriel du présent se conjugue 'vont'."
        },
        {
          question: "Dans la phrase 'Les enfants jouent dans le jardin', quel est le sujet ?",
          options: ["jouent", "dans", "le jardin", "Les enfants"],
          correctAnswer: 3,
          explanation: "Le sujet est 'Les enfants' car c'est ce qui fait l'action de jouer."
        }
      ],
      'Mathématiques': [
        {
          question: "Quelle est la solution de l'équation 2x + 5 = 13 ?",
          options: ["x = 4", "x = 3", "x = 5", "x = 6"],
          correctAnswer: 0,
          explanation: "2x + 5 = 13 → 2x = 8 → x = 4"
        },
        {
          question: "Quel est le périmètre d'un carré de côté 6 cm ?",
          options: ["12 cm", "24 cm", "36 cm", "18 cm"],
          correctAnswer: 1,
          explanation: "Le périmètre d'un carré est 4 × côté = 4 × 6 = 24 cm"
        }
      ],
      'Histoire': [
        {
          question: "En quelle année a eu lieu la Révolution française ?",
          options: ["1789", "1799", "1769", "1779"],
          correctAnswer: 0,
          explanation: "La Révolution française a commencé en 1789 avec la prise de la Bastille."
        },
        {
          question: "Qui était Napoléon Bonaparte ?",
          options: ["Un roi de France", "Un empereur français", "Un président", "Un général seulement"],
          correctAnswer: 1,
          explanation: "Napoléon Bonaparte était un empereur français qui a régné de 1804 à 1815."
        }
      ],
      'Sciences': [
        {
          question: "Quel est le symbole chimique de l'oxygène ?",
          options: ["O", "Ox", "O2", "Oxy"],
          correctAnswer: 0,
          explanation: "Le symbole chimique de l'oxygène est O."
        },
        {
          question: "Quelle est la formule de l'eau ?",
          options: ["H2O", "CO2", "O2", "H2"],
          correctAnswer: 0,
          explanation: "La formule de l'eau est H2O (deux atomes d'hydrogène et un d'oxygène)."
        }
      ]
    };

    const subjectQuestions = questionsBySubject[subject as keyof typeof questionsBySubject] || questionsBySubject['Français'];
    
    // Générer le nombre de questions demandé en répétant si nécessaire
    return Array.from({ length: count }, (_, i) => {
      const questionIndex = i % subjectQuestions.length;
      const baseQuestion = subjectQuestions[questionIndex];
      
      return {
        id: i + 1,
        question: baseQuestion.question,
        type: 'multiple_choice',
        difficulty: Math.floor(Math.random() * 5) + 3,
        options: baseQuestion.options,
        correctAnswer: baseQuestion.correctAnswer,
        explanation: baseQuestion.explanation,
        learningObjective: `Objectif d'apprentissage ${i + 1}`
      };
    });
  };

  const handleAnswerSelect = (questionIndex: number, answerIndex: number) => {
    const newAnswers = [...selectedAnswers];
    newAnswers[questionIndex] = answerIndex;
    setSelectedAnswers(newAnswers);
  };

  const handleNextQuestion = () => {
    if (currentQuestionIndex < (test?.questions.length || 0) - 1) {
      setCurrentQuestionIndex(currentQuestionIndex + 1);
    } else {
      setShowResults(true);
    }
  };

  const handlePreviousQuestion = () => {
    if (currentQuestionIndex > 0) {
      setCurrentQuestionIndex(currentQuestionIndex - 1);
    }
  };

  const calculateScore = () => {
    if (!test) return 0;
    let correct = 0;
    test.questions.forEach((question, index) => {
      if (selectedAnswers[index] === question.correctAnswer) {
        correct++;
      }
    });
    return Math.round((correct / test.questions.length) * 100);
  };

  if (!test) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-purple-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Chargement du test...</p>
        </div>
      </div>
    );
  }

  const currentQuestion = test.questions[currentQuestionIndex];
  const progress = ((currentQuestionIndex + 1) / test.questions.length) * 100;

  if (showResults) {
    const score = calculateScore();
    return (
      <div className="min-h-screen bg-gray-50">
        <div className="max-w-4xl mx-auto py-8 px-4">
          <div className="mb-8">
            <Link
              href="/dashboard/teacher/adaptive-evaluation"
              className="inline-flex items-center text-purple-600 hover:text-purple-700 mb-4"
            >
              <ArrowLeft className="w-4 h-4 mr-2" />
              Retour à l'évaluation adaptative
            </Link>
            <h1 className="text-3xl font-bold text-gray-900">Résultats de la Prévisualisation</h1>
            <p className="text-gray-600 mt-2">Test: {test.title}</p>
          </div>

          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-8 text-center">
            <div className="mb-8">
              <div className="text-6xl font-bold text-purple-600 mb-4">{score}%</div>
              <div className="text-xl text-gray-700 mb-2">Score de Prévisualisation</div>
              <div className="text-gray-500">Ce score simule les performances d'un élève</div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
              <div className="text-center p-4 bg-gray-50 rounded-lg">
                <div className="text-2xl font-bold text-blue-600">{test.questions.length}</div>
                <div className="text-sm text-gray-600">Questions</div>
              </div>
              <div className="text-center p-4 bg-gray-50 rounded-lg">
                <div className="text-2xl font-bold text-green-600">{test.estimated_duration}</div>
                <div className="text-sm text-gray-600">Minutes</div>
              </div>
              <div className="text-center p-4 bg-gray-50 rounded-lg">
                <div className="text-2xl font-bold text-purple-600">{test.difficulty_range_min}-{test.difficulty_range_max}</div>
                <div className="text-sm text-gray-600">Difficulté</div>
              </div>
            </div>

            <div className="space-y-4">
              <h3 className="text-lg font-semibold text-gray-900">Détails des Réponses</h3>
              {test.questions.map((question, index) => (
                <div key={question.id} className="p-4 border border-gray-200 rounded-lg text-left">
                  <div className="flex items-center justify-between mb-2">
                    <div className="font-medium text-gray-900">Question {question.id}</div>
                    <div className={`px-2 py-1 rounded-full text-xs font-medium ${
                      selectedAnswers[index] === question.correctAnswer
                        ? 'bg-green-100 text-green-800'
                        : 'bg-red-100 text-red-800'
                    }`}>
                      {selectedAnswers[index] === question.correctAnswer ? 'Correct' : 'Incorrect'}
                    </div>
                  </div>
                  <div className="text-sm text-gray-600 mb-2">{question.question}</div>
                  <div className="text-xs text-gray-500">
                    Réponse sélectionnée: {question.options[selectedAnswers[index] || 0]}
                    {selectedAnswers[index] !== question.correctAnswer && (
                      <span className="ml-2 text-green-600">
                        | Correcte: {question.options[question.correctAnswer]}
                      </span>
                    )}
                  </div>
                </div>
              ))}
            </div>

            <div className="mt-8 flex justify-center space-x-4">
              <button
                onClick={() => {
                  setShowResults(false);
                  setCurrentQuestionIndex(0);
                  setSelectedAnswers([]);
                }}
                className="px-6 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors"
              >
                Recommencer
              </button>
              <Link
                href="/dashboard/teacher/adaptive-evaluation"
                className="px-6 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors"
              >
                Retour aux Tests
              </Link>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-4xl mx-auto py-8 px-4">
        {/* Header */}
        <div className="mb-8">
          <Link
            href="/dashboard/teacher/adaptive-evaluation"
            className="inline-flex items-center text-purple-600 hover:text-purple-700 mb-4"
          >
            <ArrowLeft className="w-4 h-4 mr-2" />
            Retour à l'évaluation adaptative
          </Link>
          <h1 className="text-3xl font-bold text-gray-900">Prévisualisation du Test</h1>
          <p className="text-gray-600 mt-2">{test.title}</p>
        </div>

        {/* Informations du test */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-6">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-center">
            <div>
              <div className="text-2xl font-bold text-blue-600">{test.question_count}</div>
              <div className="text-sm text-gray-600">Questions</div>
            </div>
            <div>
              <div className="text-2xl font-bold text-green-600">{test.estimated_duration}</div>
              <div className="text-sm text-gray-600">Minutes</div>
            </div>
            <div>
              <div className="text-2xl font-bold text-purple-600">{test.difficulty_range_min}-{test.difficulty_range_max}</div>
              <div className="text-sm text-gray-600">Difficulté</div>
            </div>
            <div>
              <div className="text-2xl font-bold text-orange-600">{test.subject}</div>
              <div className="text-sm text-gray-600">Matière</div>
            </div>
          </div>
        </div>

        {/* Barre de progression */}
        <div className="mb-6">
          <div className="flex justify-between items-center mb-2">
            <span className="text-sm font-medium text-gray-700">
              Question {currentQuestionIndex + 1} sur {test.questions.length}
            </span>
            <span className="text-sm text-gray-500">{Math.round(progress)}%</span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div
              className="bg-purple-600 h-2 rounded-full transition-all duration-300"
              style={{ width: `${progress}%` }}
            ></div>
          </div>
        </div>

        {/* Question actuelle */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-8">
          <div className="mb-6">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-xl font-semibold text-gray-900">
                Question {currentQuestion.id}
              </h2>
              <div className="flex items-center space-x-4 text-sm text-gray-500">
                <span className="flex items-center">
                  <Target className="w-4 h-4 mr-1" />
                  Difficulté: {currentQuestion.difficulty}
                </span>
                <span className="flex items-center">
                  <BookOpen className="w-4 h-4 mr-1" />
                  {currentQuestion.type}
                </span>
              </div>
            </div>
            
            <p className="text-lg text-gray-700 mb-6">{currentQuestion.question}</p>
            
            <div className="space-y-3">
              {currentQuestion.options.map((option, index) => (
                <label
                  key={index}
                  className={`flex items-center p-4 border rounded-lg cursor-pointer transition-colors ${
                    selectedAnswers[currentQuestionIndex] === index
                      ? 'border-purple-500 bg-purple-50'
                      : 'border-gray-200 hover:border-purple-300'
                  }`}
                >
                  <input
                    type="radio"
                    name={`question-${currentQuestion.id}`}
                    value={index}
                    checked={selectedAnswers[currentQuestionIndex] === index}
                    onChange={() => handleAnswerSelect(currentQuestionIndex, index)}
                    className="mr-3 text-purple-600 focus:ring-purple-500"
                  />
                  <span className="text-gray-700">{option}</span>
                </label>
              ))}
            </div>
          </div>

          {/* Navigation */}
          <div className="flex justify-between items-center pt-6 border-t border-gray-200">
            <button
              onClick={handlePreviousQuestion}
              disabled={currentQuestionIndex === 0}
              className="px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              Précédent
            </button>
            
            <button
              onClick={handleNextQuestion}
              disabled={selectedAnswers[currentQuestionIndex] === undefined}
              className="px-6 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              {currentQuestionIndex === test.questions.length - 1 ? 'Terminer' : 'Suivant'}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
