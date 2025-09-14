'use client';

import React, { useState, useEffect } from 'react';
import { Card } from '@/components/Card';
import Button from '@/components/Button';
import Sidebar from '@/components/Sidebar';
import { useAuth } from '@/hooks/useAuthSimple';
import { 
  BookOpen, 
  Users, 
  TrendingUp, 
  Eye, 
  Download,
  Filter,
  Search,
  Calendar,
  Clock,
  Target,
  CheckCircle,
  XCircle
} from 'lucide-react';

interface TestResult {
  id: number;
  test_id: number;
  test_title: string;
  test_subject: string;
  student_id: number;
  student_name: string;
  score: number;
  max_score: number;
  percentage: number;
  status: string;
  started_at: string;
  completed_at: string;
  quiz_type: string;
}

interface StudentResponse {
  question_id: number;
  question_text: string;
  student_answer: string;
  correct_answer: string;
  is_correct: boolean;
  points_earned: number;
  max_points: number;
}

const TeacherTestResultsPage = () => {
  const { user, token } = useAuth();
  const [results, setResults] = useState<TestResult[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedResult, setSelectedResult] = useState<TestResult | null>(null);
  const [studentResponses, setStudentResponses] = useState<StudentResponse[]>([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterSubject, setFilterSubject] = useState('all');
  const [filterStatus, setFilterStatus] = useState('all');

  useEffect(() => {
    if (user && token) {
      fetchTestResults();
    }
  }, [user, token]);

  const fetchTestResults = async () => {
    try {
      setLoading(true);
      
      // Récupérer tous les résultats des tests adaptatifs
      const response = await fetch('/api/v1/adaptive-evaluation/results/all', {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });

      if (response.ok) {
        const data = await response.json();
        setResults(data);
        console.log('🔥 [DEBUG] Résultats récupérés:', data);
      } else {
        console.error('❌ Erreur lors de la récupération des résultats:', response.status);
      }
    } catch (error) {
      console.error('❌ Erreur lors de la récupération des résultats:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchStudentResponses = async (testId: number, studentId: number) => {
    try {
      const response = await fetch(`/api/v1/adaptive-evaluation/tests/${testId}/student/${studentId}/responses`, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });

      if (response.ok) {
        const data = await response.json();
        setStudentResponses(data);
        console.log('🔥 [DEBUG] Réponses de l\'étudiant:', data);
      } else {
        console.error('❌ Erreur lors de la récupération des réponses:', response.status);
      }
    } catch (error) {
      console.error('❌ Erreur lors de la récupération des réponses:', error);
    }
  };

  const viewStudentResponses = (result: TestResult) => {
    setSelectedResult(result);
    fetchStudentResponses(result.test_id, result.student_id);
  };

  const getScoreColor = (percentage: number) => {
    if (percentage >= 80) return 'text-green-600';
    if (percentage >= 60) return 'text-yellow-600';
    return 'text-red-600';
  };

  const getScoreBadge = (percentage: number) => {
    if (percentage >= 80) return <span className="px-2 py-1 rounded-full text-xs font-medium bg-green-100 text-green-800">Excellent</span>;
    if (percentage >= 60) return <span className="px-2 py-1 rounded-full text-xs font-medium bg-blue-100 text-blue-800">Bon</span>;
    return <span className="px-2 py-1 rounded-full text-xs font-medium bg-red-100 text-red-800">À améliorer</span>;
  };

  const getStatusBadge = (status: string) => {
    switch (status) {
      case 'completed':
        return <span className="px-2 py-1 rounded-full text-xs font-medium bg-green-100 text-green-800">Terminé</span>;
      case 'in_progress':
        return <span className="px-2 py-1 rounded-full text-xs font-medium bg-blue-100 text-blue-800">En cours</span>;
      case 'abandoned':
        return <span className="px-2 py-1 rounded-full text-xs font-medium bg-red-100 text-red-800">Abandonné</span>;
      default:
        return <span className="px-2 py-1 rounded-full text-xs font-medium bg-gray-100 text-gray-800">{status}</span>;
    }
  };

  const filteredResults = results.filter(result => {
    const matchesSearch = result.test_title.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         result.student_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         result.test_subject.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesSubject = filterSubject === 'all' || result.test_subject === filterSubject;
    const matchesStatus = filterStatus === 'all' || result.status === filterStatus;
    
    return matchesSearch && matchesSubject && matchesStatus;
  });

  const subjects = Array.from(new Set(results.map(r => r.test_subject)));
  const totalTests = results.length;
  const completedTests = results.filter(r => r.status === 'completed').length;
  const averageScore = results.length > 0 ? 
    Math.round(results.reduce((sum, r) => sum + r.percentage, 0) / results.length) : 0;

  if (!user || !token) {
    return (
      <div className="flex h-screen bg-gray-50">
        <Sidebar />
        <div className="flex-1 ml-56 flex items-center justify-center">
          <div className="text-center">
            <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-purple-600 mx-auto"></div>
            <p className="mt-4 text-gray-600">Chargement de l'utilisateur...</p>
          </div>
        </div>
      </div>
    );
  }

  if (loading) {
    return (
      <div className="flex h-screen bg-gray-50">
        <Sidebar />
        <div className="flex-1 ml-56 flex items-center justify-center">
          <div className="text-center">
            <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-purple-600 mx-auto"></div>
            <p className="mt-4 text-gray-600">Chargement des résultats...</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="flex h-screen bg-gray-50">
      <Sidebar />
      <div className="flex-1 ml-56 p-8 overflow-y-auto">
        {/* En-tête */}
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className="text-4xl font-bold text-gray-900">Résultats des Tests Adaptatifs</h1>
            <p className="text-xl text-gray-600 mt-2">Suivez les performances de vos étudiants et analysez leurs réponses</p>
          </div>
          <Button onClick={fetchTestResults} className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-xl flex items-center space-x-2">
            <TrendingUp className="h-4 w-4" />
            <span>Actualiser</span>
          </Button>
        </div>

        {/* Statistiques */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <Card className="p-6">
            <div className="flex items-center space-x-3">
              <div className="p-3 bg-blue-100 rounded-xl">
                <BookOpen className="h-6 w-6 text-blue-600" />
              </div>
              <div>
                <p className="text-sm font-medium text-gray-600">Total Tests</p>
                <p className="text-2xl font-bold text-gray-900">{totalTests}</p>
              </div>
            </div>
          </Card>

          <Card className="p-6">
            <div className="flex items-center space-x-3">
              <div className="p-3 bg-green-100 rounded-xl">
                <CheckCircle className="h-6 w-6 text-green-600" />
              </div>
              <div>
                <p className="text-sm font-medium text-gray-600">Tests Terminés</p>
                <p className="text-2xl font-bold text-gray-900">{completedTests}</p>
              </div>
            </div>
          </Card>

          <Card className="p-6">
            <div className="flex items-center space-x-3">
              <div className="p-3 bg-purple-100 rounded-xl">
                <Users className="h-6 w-6 text-purple-600" />
              </div>
              <div>
                <p className="text-sm font-medium text-gray-600">Étudiants Actifs</p>
                <p className="text-2xl font-bold text-gray-900">
                  {new Set(results.map(r => r.student_id)).size}
                </p>
              </div>
            </div>
          </Card>

          <Card className="p-6">
            <div className="flex items-center space-x-3">
              <div className="p-3 bg-orange-100 rounded-xl">
                <TrendingUp className="h-6 w-6 text-orange-600" />
              </div>
              <div>
                <p className="text-sm font-medium text-gray-600">Score Moyen</p>
                <p className="text-2xl font-bold text-gray-900">{averageScore}%</p>
              </div>
            </div>
          </Card>
        </div>

        {/* Filtres et recherche */}
        <Card className="p-6 mb-8">
          <div className="flex flex-col md:flex-row gap-4">
            <div className="flex-1">
              <label htmlFor="search" className="block text-sm font-medium text-gray-700 mb-2">Rechercher</label>
              <div className="relative">
                <Search className="absolute left-3 top-3 h-4 w-4 text-gray-400" />
                <input
                  id="search"
                  type="text"
                  placeholder="Rechercher par titre, étudiant ou matière..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200"
                />
              </div>
            </div>
            
            <div>
              <label htmlFor="subject" className="block text-sm font-medium text-gray-700 mb-2">Matière</label>
              <select
                id="subject"
                value={filterSubject}
                onChange={(e) => setFilterSubject(e.target.value)}
                className="px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200"
              >
                <option value="all">Toutes matières</option>
                {subjects.map(subject => (
                  <option key={subject} value={subject}>{subject}</option>
                ))}
              </select>
            </div>
            
            <div>
              <label htmlFor="status" className="block text-sm font-medium text-gray-700 mb-2">Statut</label>
              <select
                id="status"
                value={filterStatus}
                onChange={(e) => setFilterStatus(e.target.value)}
                className="px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200"
              >
                <option value="all">Tous statuts</option>
                <option value="completed">Terminés</option>
                <option value="in_progress">En cours</option>
                <option value="abandoned">Abandonnés</option>
              </select>
            </div>
          </div>
        </Card>

        {/* Liste des résultats */}
        <Card className="p-6">
          <h2 className="text-2xl font-bold text-gray-900 mb-6">Résultats des Tests ({filteredResults.length})</h2>
          
          {filteredResults.length === 0 ? (
            <div className="text-center py-12">
              <BookOpen className="h-16 w-16 text-gray-300 mx-auto mb-4" />
              <h3 className="text-xl font-medium text-gray-900 mb-2">Aucun résultat trouvé</h3>
              <p className="text-gray-500">Aucun résultat ne correspond à vos critères de recherche</p>
            </div>
          ) : (
            <div className="space-y-6">
              {filteredResults.map((result) => (
                <Card key={result.id} className="p-6 hover:shadow-xl transition-all duration-200 rounded-2xl">
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <div className="flex items-center space-x-3 mb-4">
                        <h3 className="text-xl font-semibold text-gray-800">{result.test_title}</h3>
                        {getStatusBadge(result.status)}
                        <span className="px-2 py-1 rounded-full text-xs font-medium bg-purple-100 text-purple-800">
                          Test Adaptatif
                        </span>
                      </div>
                        
                      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm text-gray-600 mb-4">
                        <div className="flex items-center space-x-2">
                          <Users className="h-4 w-4 text-gray-400" />
                          <span><span className="font-medium">Étudiant:</span> {result.student_name}</span>
                        </div>
                        
                        <div className="flex items-center space-x-2">
                          <BookOpen className="h-4 w-4 text-gray-400" />
                          <span><span className="font-medium">Matière:</span> {result.test_subject}</span>
                        </div>
                        
                        <div className="flex items-center space-x-2">
                          <Calendar className="h-4 w-4 text-gray-400" />
                          <span><span className="font-medium">Terminé le:</span> {new Date(result.completed_at).toLocaleDateString()}</span>
                        </div>
                        
                        <div className="flex items-center space-x-2">
                          <Clock className="h-4 w-4 text-gray-400" />
                          <span><span className="font-medium">Durée:</span> {result.completed_at ? 
                            Math.round((new Date(result.completed_at).getTime() - new Date(result.started_at).getTime()) / (1000 * 60)) : 'N/A'} min</span>
                        </div>
                      </div>

                      {/* Score */}
                      <div className="flex items-center space-x-2 mb-4">
                        <TrendingUp className="h-4 w-4 text-gray-400" />
                        <span className="font-medium">Score:</span>
                        <span className={`font-semibold ${getScoreColor(result.percentage)}`}>
                          {result.score}/{result.max_score} ({result.percentage}%)
                        </span>
                        {getScoreBadge(result.percentage)}
                      </div>
                    </div>

                    <div className="flex flex-col space-y-2 ml-4">
                      <Button 
                        onClick={() => viewStudentResponses(result)}
                        className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-xl flex items-center space-x-2"
                      >
                        <Eye className="h-4 w-4" />
                        <span>Voir réponses</span>
                      </Button>
                      
                      <Button 
                        className="bg-gray-600 hover:bg-gray-700 text-white px-4 py-2 rounded-xl flex items-center space-x-2"
                      >
                        <Download className="h-4 w-4" />
                        <span>Exporter</span>
                      </Button>
                    </div>
                  </div>
                </Card>
              ))}
            </div>
          )}
        </Card>

        {/* Modal des réponses de l'étudiant */}
        {selectedResult && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
            <div className="bg-white rounded-2xl max-w-4xl w-full max-h-[90vh] overflow-y-auto">
              <div className="p-6">
                <div className="flex items-center justify-between mb-6">
                  <h2 className="text-2xl font-bold text-gray-900">Réponses de l'étudiant</h2>
                  <Button 
                    onClick={() => setSelectedResult(null)}
                    className="bg-gray-600 hover:bg-gray-700 text-white px-4 py-2 rounded-xl"
                  >
                    <XCircle className="h-4 w-4" />
                  </Button>
                </div>
              
              <div className="mb-4">
                <h3 className="text-lg font-semibold mb-2">{selectedResult.test_title}</h3>
                <p className="text-gray-600">Étudiant: {selectedResult.student_name} | Score: {selectedResult.score}/{selectedResult.max_score} ({selectedResult.percentage}%)</p>
              </div>

                {studentResponses.length > 0 ? (
                  <div className="space-y-4">
                    {studentResponses.map((response, index) => (
                      <Card key={response.question_id} className="p-4 rounded-xl">
                        <div className="flex items-start space-x-3">
                          <div className="flex-shrink-0">
                            {response.is_correct ? (
                              <CheckCircle className="h-6 w-6 text-green-600" />
                            ) : (
                              <XCircle className="h-6 w-6 text-red-600" />
                            )}
                          </div>
                          
                          <div className="flex-1">
                            <div className="flex items-center justify-between mb-2">
                              <h4 className="font-medium text-gray-900">Question {index + 1}</h4>
                              <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                                response.is_correct ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                              }`}>
                                {response.points_earned}/{response.max_points} pts
                              </span>
                            </div>
                            
                            <p className="text-gray-700 mb-3">{response.question_text}</p>
                            
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
                              <div>
                                <span className="font-medium text-gray-600">Réponse de l'étudiant:</span>
                                <p className={`mt-1 p-3 rounded-xl ${response.is_correct ? 'bg-green-50 text-green-800' : 'bg-red-50 text-red-800'}`}>
                                  {response.student_answer}
                                </p>
                              </div>
                              
                              <div>
                                <span className="font-medium text-gray-600">Réponse correcte:</span>
                                <p className="mt-1 p-3 rounded-xl bg-gray-50 text-gray-800">
                                  {response.correct_answer}
                                </p>
                              </div>
                            </div>
                          </div>
                        </div>
                      </Card>
                    ))}
                  </div>
                ) : (
                  <div className="text-center py-8">
                    <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto mb-4"></div>
                    <p className="text-gray-500">Chargement des réponses...</p>
                  </div>
                )}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default TeacherTestResultsPage;



