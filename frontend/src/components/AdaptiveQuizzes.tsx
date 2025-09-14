import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';
import { Button } from '@/components/ui/button';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Brain, Target, TrendingUp, Clock, Zap, Lightbulb, BarChart3, Play } from 'lucide-react';
import StudentQuiz from './StudentQuiz';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

interface DashboardData {
  students: Array<{id: number, name: string}>;
  subjects: Array<{id: string, name: string}>;
  current_level: string;
  completed_quizzes: number;
  average_score: number;
  coherence_percentage: number;
  difficulty_progression: number;
  trend: string;
  next_recommended_level: string;
  level_progression: number;
  student_specific?: {
    current_level: string;
    completed_quizzes: number;
    average_score: number;
    coherence_percentage: number;
    difficulty_progression: number;
    trend: string;
    next_recommended_level: string;
    level_progression: number;
  };
}

interface GeneratedQuiz {
  quiz_id: number;
  title: string;
  subject: string;
  difficulty: string;
  question_count: number;
  estimated_duration: number;
  adaptation_reason: string;
  questions: Array<{
    id: number;
    question: string;
    options: string[];
    correct_answer: number;
  }>;
}

const AdaptiveQuizzes: React.FC = () => {
  console.log('🚀 AdaptiveQuizzes component is rendering!');
  
  const [dashboardData, setDashboardData] = useState<DashboardData | null>(null);
  const [selectedStudent, setSelectedStudent] = useState<string>('');
  const [selectedSubject, setSelectedSubject] = useState<string>('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [generating, setGenerating] = useState(false);
  const [generatedQuiz, setGeneratedQuiz] = useState<GeneratedQuiz | null>(null);
  const [showStudentQuiz, setShowStudentQuiz] = useState(false);

  useEffect(() => {
    console.log('AdaptiveQuizzes component mounted');
    fetchDashboardData();
  }, []);

  // Recharger les données quand l'étudiant sélectionné change
  useEffect(() => {
    if (selectedStudent) {
      console.log('🔍 [FRONTEND] Étudiant sélectionné changé, rechargement des données...');
      fetchDashboardData();
    }
  }, [selectedStudent]);

  const fetchDashboardData = async () => {
    try {
      console.log('🔍 [FRONTEND] Début de récupération des données adaptive quizzes...');
      setLoading(true);
      setError(null);

      // Construire l'URL avec l'étudiant sélectionné si disponible
      let url = `${API_BASE_URL}/api/v1/adaptive_quizzes/dashboard-data`;
      if (selectedStudent) {
        url += `?student_id=${selectedStudent}`;
        console.log('🔍 [FRONTEND] Récupération des données pour étudiant:', selectedStudent);
      } else {
        console.log('🔍 [FRONTEND] Récupération des données globales (vue prof)');
      }

      const response = await fetch(url, {
        headers: {
          'Content-Type': 'application/json'
        }
      });

      console.log('🔍 [FRONTEND] Response status:', response.status);
      console.log('🔍 [FRONTEND] Response ok:', response.ok);

      if (!response.ok) {
        throw new Error(`Erreur ${response.status}: ${response.statusText}`);
      }

      const data = await response.json();
      console.log('🔍 [FRONTEND] Adaptive Quizzes Data reçu:', data);
      console.log('🔍 [FRONTEND] Students:', data.students);
      console.log('🔍 [FRONTEND] Subjects:', data.subjects);
      console.log('🔍 [FRONTEND] Student specific:', data.student_specific);
      console.log('🔍 [FRONTEND] DashboardData state before:', dashboardData);
      setDashboardData(data);
      console.log('🔍 [FRONTEND] DashboardData state after set:', data);
      
      // Pré-sélectionner le premier étudiant et matière si pas encore fait
      if (data.students && data.students.length > 0 && !selectedStudent) {
        console.log('🔍 [FRONTEND] Setting selected student:', data.students[0].id.toString());
        setSelectedStudent(data.students[0].id.toString());
      }
      if (data.subjects && data.subjects.length > 0 && !selectedSubject) {
        console.log('🔍 [FRONTEND] Setting selected subject:', data.subjects[0].id);
        setSelectedSubject(data.subjects[0].id);
      }
      
    } catch (err) {
      console.error('❌ [FRONTEND] Erreur adaptive quizzes:', err);
      setError('Erreur lors du chargement des données');
    } finally {
      setLoading(false);
    }
  };

  const generateAdaptiveQuiz = async () => {
    try {
      console.log('🔍 [FRONTEND] Début de génération de quiz adaptatif...');
      console.log('🔍 [FRONTEND] Paramètres:', { selectedStudent, selectedSubject });
      
      setGenerating(true);
      setError(null);
      setGeneratedQuiz(null);

      if (!selectedStudent || !selectedSubject) {
        throw new Error('Veuillez sélectionner un étudiant et une matière');
      }

      const response = await fetch(`${API_BASE_URL}/api/v1/adaptive_quizzes/generate-test/${selectedStudent}?subject=${encodeURIComponent(selectedSubject)}&question_count=10`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        }
      });

      console.log('🔍 [FRONTEND] Response status:', response.status);

      if (!response.ok) {
        const errorText = await response.text();
        console.error('❌ [FRONTEND] Erreur HTTP:', response.status, errorText);
        throw new Error(`Erreur ${response.status}: ${response.statusText}`);
      }

      const quizData = await response.json();
      console.log('🔍 [FRONTEND] Quiz généré:', quizData);
      
      setGeneratedQuiz(quizData);
      
    } catch (err) {
      console.error('❌ [FRONTEND] Erreur generate quiz:', err);
      setError(err instanceof Error ? err.message : 'Erreur lors de la génération du quiz adaptatif');
    } finally {
      setGenerating(false);
    }
  };

  const handleStartQuiz = () => {
    if (generatedQuiz) {
      setShowStudentQuiz(true);
    }
  };

  const handleQuizComplete = (score: number, results: any) => {
    console.log('Quiz terminé avec score:', score);
    // Ici vous pouvez ajouter la logique pour mettre à jour les métriques
  };

  const handleCloseQuiz = () => {
    setShowStudentQuiz(false);
    setGeneratedQuiz(null);
  };

  const getDifficultyColor = (difficulty: string) => {
    switch (difficulty.toLowerCase()) {
      case 'facile': return 'bg-green-100 text-green-800';
      case 'moyen': return 'bg-yellow-100 text-yellow-800';
      case 'difficile': return 'bg-red-100 text-red-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const getDifficultyTrendIcon = (trend: string) => {
    switch (trend.toLowerCase()) {
      case 'amélioration':
        return <TrendingUp className="h-4 w-4 text-green-500" />;
      case 'régression':
        return <TrendingUp className="h-4 w-4 text-red-500 transform rotate-180" />;
      case 'stable':
        return <TrendingUp className="h-4 w-4 text-yellow-500" />;
      default:
        return <TrendingUp className="h-4 w-4 text-gray-400" />;
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (error) {
    return (
      <Alert variant="destructive">
        <AlertDescription>{error}</AlertDescription>
      </Alert>
    );
  }

  if (showStudentQuiz && generatedQuiz) {
    return (
      <StudentQuiz 
        quizData={generatedQuiz}
        onQuizComplete={handleQuizComplete}
        onClose={handleCloseQuiz}
      />
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-bold">Tests Adaptatifs</h2>
        <Badge variant="outline" className="text-sm">
          <Brain className="h-4 w-4 mr-1" />
          IA Adaptative
        </Badge>
      </div>

      {/* Contrôles */}
      <Card>
        <CardHeader>
          <CardTitle>Génération de Quiz Adaptatif</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="flex gap-4">
            <div className="flex-1">
              <label className="text-sm font-medium">Étudiant</label>
              <select 
                value={selectedStudent} 
                onChange={(e) => setSelectedStudent(e.target.value)}
                className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="">Sélectionner un étudiant</option>
                {dashboardData?.students && dashboardData.students.length > 0 ? (
                  dashboardData.students.map(student => (
                    <option key={student.id} value={student.id.toString()}>
                      {student.name}
                    </option>
                  ))
                ) : (
                  <option value="no-data" disabled>Aucun étudiant disponible</option>
                )}
              </select>
              {console.log('🔍 [FRONTEND] Rendering students dropdown with:', dashboardData?.students)}
            </div>

            <div className="flex-1">
              <label className="text-sm font-medium">Matière</label>
              <select 
                value={selectedSubject} 
                onChange={(e) => setSelectedSubject(e.target.value)}
                className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="">Sélectionner une matière</option>
                {dashboardData?.subjects && dashboardData.subjects.length > 0 ? (
                  dashboardData.subjects.map(subject => (
                    <option key={subject.id} value={subject.id}>
                      {subject.name}
                    </option>
                  ))
                ) : (
                  <option value="no-data" disabled>Aucune matière disponible</option>
                )}
              </select>
              {console.log('🔍 [FRONTEND] Rendering subjects dropdown with:', dashboardData?.subjects)}
            </div>
          </div>

          <Button 
            onClick={generateAdaptiveQuiz} 
            disabled={generating}
            className="w-full"
          >
            {generating ? (
              <>
                <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                Génération en cours...
              </>
            ) : (
              <>
                <Zap className="h-4 w-4 mr-2" />
                Générer Quiz Adaptatif
              </>
            )}
          </Button>
        </CardContent>
      </Card>

      {/* Quiz généré */}
      {generatedQuiz && (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Target className="h-5 w-5" />
              Quiz Adaptatif Généré
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <h3 className="text-lg font-semibold">{generatedQuiz.title}</h3>
                <Badge className={getDifficultyColor(generatedQuiz.difficulty)}>
                  {generatedQuiz.difficulty}
                </Badge>
              </div>

              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                <div className="text-center">
                  <div className="text-2xl font-bold">{generatedQuiz.question_count}</div>
                  <div className="text-xs text-muted-foreground">Questions</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold">{generatedQuiz.estimated_duration}min</div>
                  <div className="text-xs text-muted-foreground">Temps estimé</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold">{generatedQuiz.subject}</div>
                  <div className="text-xs text-muted-foreground">Matière</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold">Niveau {generatedQuiz.difficulty}</div>
                  <div className="text-xs text-muted-foreground">Niveau adaptatif</div>
                </div>
              </div>

              <div className="bg-blue-50 p-3 rounded-lg">
                <p className="text-sm text-blue-700">
                  <Lightbulb className="h-4 w-4 inline mr-1" />
                  <strong>Adaptation :</strong> {generatedQuiz.adaptation_reason}
                </p>
              </div>

              {/* Questions du quiz */}
              <div className="space-y-4">
                <h4 className="font-semibold text-gray-800">Questions :</h4>
                {generatedQuiz.questions.map((question, index) => (
                  <div key={question.id} className="border rounded-lg p-4 bg-gray-50">
                    <div className="flex items-start gap-2 mb-3">
                      <span className="bg-blue-500 text-white rounded-full w-6 h-6 flex items-center justify-center text-sm font-medium">
                        {index + 1}
                      </span>
                      <p className="text-gray-800 font-medium">{question.question}</p>
                    </div>
                    
                    <div className="space-y-2 ml-8">
                      {question.options.map((option, optionIndex) => (
                        <label key={optionIndex} className="flex items-center gap-2 cursor-pointer hover:bg-gray-100 p-2 rounded">
                          <input 
                            type="radio" 
                            name={`question-${question.id}`}
                            value={optionIndex}
                            className="text-blue-600"
                          />
                          <span className="text-gray-700">{option}</span>
                        </label>
                      ))}
                    </div>
                  </div>
                ))}
              </div>

              <div className="flex gap-2">
                <Button className="flex-1" variant="outline">
                  <Clock className="h-4 w-4 mr-2" />
                  Sauvegarder
                </Button>
                <Button 
                  className="flex-1"
                  onClick={handleStartQuiz}
                  disabled={!generatedQuiz}
                >
                  <Play className="h-4 w-4 mr-2" />
                  Commencer le Quiz
                </Button>
              </div>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Progression adaptative */}
      {dashboardData && (
        <div className="space-y-6">
          {/* Métriques de progression */}
          <Card>
            <CardHeader>
              <CardTitle>Progression Adaptative</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                <div className="text-center">
                  <div className="text-2xl font-bold">{dashboardData.current_level}</div>
                  <div className="text-xs text-muted-foreground">Niveau actuel</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold">{dashboardData.completed_quizzes}</div>
                  <div className="text-xs text-muted-foreground">Quiz complétés</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold">{dashboardData.average_score}%</div>
                  <div className="text-xs text-muted-foreground">Score moyen</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold">{dashboardData.coherence_percentage}%</div>
                  <div className="text-xs text-muted-foreground">Cohérence</div>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Tendances de difficulté */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <TrendingUp className="h-5 w-5" />
                Évolution de la Difficulté
                {dashboardData.student_specific && (
                  <Badge variant="secondary" className="ml-2">
                    Données personnalisées
                  </Badge>
                )}
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <span className="text-sm font-medium">Tendance actuelle</span>
                  <div className="flex items-center gap-2">
                    {getDifficultyTrendIcon(dashboardData.trend)}
                    <span className="text-sm capitalize">
                      {dashboardData.trend}
                    </span>
                  </div>
                </div>

                <div className="flex items-center justify-between">
                  <span className="text-sm font-medium">Prochain niveau recommandé</span>
                  <Badge variant="outline">
                    Niveau {dashboardData.next_recommended_level}
                  </Badge>
                </div>

                <Progress 
                  value={dashboardData.level_progression * 10} 
                  className="h-2" 
                />
                <p className="text-xs text-muted-foreground">
                  Progression: Niveau {dashboardData.current_level} sur 10
                </p>
              </div>
            </CardContent>
          </Card>

          {/* Recommandations */}
          {/* This section will be updated to display recommendations */}
          {/* For now, it will show a placeholder or be removed if not needed */}
          {/* {dashboardData.recommendations && dashboardData.recommendations.length > 0 && (
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Lightbulb className="h-5 w-5 text-yellow-500" />
                  Recommandations Adaptatives
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-2">
                  {dashboardData.recommendations.map((rec, index) => (
                    <div key={index} className="flex items-start gap-2 p-3 bg-yellow-50 rounded-lg">
                      <Lightbulb className="h-4 w-4 mt-0.5 text-yellow-500" />
                      <span className="text-sm">{rec}</span>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          )} */}
        </div>
      )}
    </div>
  );
};

export default AdaptiveQuizzes; 