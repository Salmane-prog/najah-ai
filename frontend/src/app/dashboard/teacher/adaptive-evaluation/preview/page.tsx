'use client';

import { useEffect, useState } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import { Brain, ArrowLeft, Clock, Users, Target } from 'lucide-react';

interface TestQuestion {
  id: number;
  question: string;
  type: string;
  difficulty: number;
  options?: string[];
  correctAnswer: number;
  explanation: string;
  learningObjective: string;
}

interface PreviewTest {
  id: number;
  title: string;
  subject: string;
  description: string;
  difficulty_range_min: number;
  difficulty_range_max: number;
  estimated_duration: number;
  question_count: number;
  adaptiveType: string;
  learning_objectives: string;
  is_active: boolean;
  created_at: string;
  questions: TestQuestion[];
}

export default function TestPreviewPage() {
  const [test, setTest] = useState<PreviewTest | null>(null);
  const [questions, setQuestions] = useState<TestQuestion[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const router = useRouter();
  const searchParams = useSearchParams();

  useEffect(() => {
    const loadTest = async () => {
      console.log('🔄 loadTest appelé');
      console.log('🔍 searchParams:', searchParams);
      console.log('🔍 URL complète:', window.location.href);
      
      try {
        // Récupérer l'ID de prévisualisation depuis l'URL
        const previewId = searchParams.get('previewId');
        console.log('🔑 previewId depuis URL:', previewId);
        
        if (!previewId) {
          console.log('⚠️ Aucun previewId dans l\'URL, tentative de fallback...');
          // Fallback: essayer de récupérer l'ID depuis localStorage
          const currentPreviewId = localStorage.getItem('currentPreviewId');
          console.log('🔍 currentPreviewId depuis localStorage:', currentPreviewId);
          
          if (currentPreviewId) {
            console.log('🔄 Utilisation de l\'ID de prévisualisation depuis localStorage:', currentPreviewId);
            const testData = localStorage.getItem(`previewTest_${currentPreviewId}`);
            console.log('🔍 testData récupéré:', testData ? 'OUI' : 'NON');
            
            if (testData) {
              const parsedTest = JSON.parse(testData);
              console.log('📋 Test récupéré pour prévisualisation:', parsedTest);
              
              setTest(parsedTest);
              
              if (parsedTest.questions && Array.isArray(parsedTest.questions)) {
                console.log(`✅ ${parsedTest.questions.length} questions trouvées dans le test`);
                setQuestions(parsedTest.questions);
              } else {
                console.warn('⚠️ Aucune question trouvée dans le test');
                setQuestions([]);
              }
              setIsLoading(false);
              return;
            }
          }
          
          console.log('❌ Aucun test trouvé, affichage de l\'erreur');
          setError('Aucun test à prévisualiser. Veuillez générer un test d\'abord.');
          setIsLoading(false);
          return;
        }

        // Récupérer le test avec l'ID spécifique
        const testData = localStorage.getItem(`previewTest_${previewId}`);
        if (testData) {
          const parsedTest = JSON.parse(testData);
          console.log('📋 Test récupéré pour prévisualisation:', parsedTest);
          console.log('🔍 Structure des questions:', parsedTest.questions);
          console.log('🔍 Première question:', parsedTest.questions?.[0]);
          
          setTest(parsedTest);
          
          if (parsedTest.questions && Array.isArray(parsedTest.questions)) {
            console.log(`✅ ${parsedTest.questions.length} questions trouvées dans le test`);
            setQuestions(parsedTest.questions);
          } else {
            console.warn('⚠️ Aucune question trouvée dans le test');
            setQuestions([]);
          }
        } else {
          setError(`Test avec l'ID ${previewId} non trouvé. Il a peut-être expiré.`);
        }
      } catch (error) {
        console.error('❌ Erreur lors du chargement du test:', error);
        setError('Erreur lors du chargement du test. Veuillez réessayer.');
      }
      setIsLoading(false);
    };

    loadTest();
  }, [searchParams]);

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-purple-600"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="container mx-auto px-4 py-8 text-center">
        <div className="bg-red-50 border border-red-200 rounded-lg p-6 max-w-md mx-auto">
          <p className="text-red-600 mb-4">{error}</p>
          <button 
            onClick={() => router.back()}
            className="px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700"
          >
            Retour
          </button>
        </div>
      </div>
    );
  }

  if (!test) {
    return (
      <div className="container mx-auto px-4 py-8 text-center">
        <p className="text-red-600">Aucun test à prévisualiser</p>
        <button 
          onClick={() => router.back()}
          className="mt-4 px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700"
        >
          Retour
        </button>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8">
      {/* Header avec bouton retour */}
      <div className="flex items-center mb-8">
        <button 
          onClick={() => router.back()}
          className="flex items-center space-x-2 text-purple-600 hover:text-purple-800 mr-6"
        >
          <ArrowLeft className="w-5 h-5" />
          <span>Retour</span>
        </button>
        <div className="flex items-center">
          <Brain className="w-8 h-8 text-purple-600 mr-3" />
          <h1 className="text-3xl font-bold text-gray-900">Prévisualisation du Test</h1>
        </div>
      </div>

      {/* Informations du test */}
      <div className="bg-white rounded-lg shadow-lg p-6 mb-8">
        <h2 className="text-2xl font-bold text-gray-900 mb-4">{test.title}</h2>
        <p className="text-gray-600 mb-6">{test.description}</p>
        
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
          <div className="flex items-center space-x-2">
            <Target className="w-5 h-5 text-blue-600" />
            <span className="text-sm text-gray-600">
              Niveau {test.difficulty_range_min}-{test.difficulty_range_max}
            </span>
          </div>
          <div className="flex items-center space-x-2">
            <Users className="w-5 h-5 text-green-600" />
            <span className="text-sm text-gray-600">
              {questions.length} questions
            </span>
          </div>
          <div className="flex items-center space-x-2">
            <Clock className="w-5 h-5 text-purple-600" />
            <span className="text-sm text-gray-600">
              {test.estimated_duration} min
            </span>
          </div>
          <div className="text-sm text-gray-600">
            {test.subject}
          </div>
        </div>

        {test.learning_objectives && (
          <div className="bg-blue-50 p-4 rounded-lg">
            <h3 className="font-semibold text-blue-900 mb-2">Objectifs d'apprentissage :</h3>
            <p className="text-blue-800">{test.learning_objectives}</p>
          </div>
        )}
      </div>

      {/* Questions */}
      <div className="bg-white rounded-lg shadow-lg p-6">
        <h3 className="text-xl font-bold text-gray-900 mb-4">
          Questions du Test ({questions.length} questions)
        </h3>
        
        {questions.length === 0 ? (
          <div className="text-center py-8 text-gray-500">
            <p>Aucune question disponible pour ce test</p>
            <div className="mt-4 p-4 bg-yellow-50 border border-yellow-200 rounded-lg">
              <p className="text-sm text-yellow-800">
                <strong>Debug:</strong> Vérifiez la console pour plus de détails
              </p>
            </div>
          </div>
        ) : (
          questions.map((question, index) => (
            <div key={question.id || index} className="border border-gray-200 rounded-lg p-4 mb-4">
              <div className="flex items-center justify-between mb-3">
                <h4 className="font-semibold text-gray-900">
                  Question {index + 1}
                </h4>
                <span className="text-sm text-gray-500">
                  Niveau {question.difficulty || 'N/A'}
                </span>
              </div>
              
              <p className="text-gray-800 mb-4">{question.question || 'Question non disponible'}</p>
              
              {question.type === 'multiple_choice' && question.options && Array.isArray(question.options) && (
                <div className="space-y-2 mb-4">
                  {question.options.map((option, optIndex) => (
                    <div key={optIndex} className="flex items-center space-x-2">
                      <input 
                        type="radio" 
                        name={`question-${question.id || index}`}
                        disabled
                        className="text-purple-600"
                      />
                      <span className={`text-gray-700 ${optIndex === question.correctAnswer ? 'font-semibold' : ''}`}>
                        {option || 'Option non disponible'}
                        {optIndex === question.correctAnswer && ' ✓'}
                      </span>
                    </div>
                  ))}
                </div>
              )}
              
              <div className="bg-green-50 p-3 rounded-lg">
                <p className="text-sm text-green-800">
                  <strong>Réponse correcte :</strong> {question.options && Array.isArray(question.options) && question.options[question.correctAnswer] ? question.options[question.correctAnswer] : 'Non disponible'}
                </p>
                {question.explanation && (
                  <p className="text-sm text-green-700 mt-2">
                    <strong>Explication :</strong> {question.explanation}
                  </p>
                )}
                {question.learningObjective && (
                  <p className="text-sm text-blue-700 mt-2">
                    <strong>Objectif d'apprentissage :</strong> {question.learningObjective}
                  </p>
                )}
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
