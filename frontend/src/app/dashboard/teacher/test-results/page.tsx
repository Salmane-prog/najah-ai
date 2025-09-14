'use client';

import React, { useEffect, useState } from 'react';
import { useAuth } from '@/hooks/useAuthSimple';
import { Card } from '@/components/Card';
import Sidebar from '@/components/Sidebar';
import { 
  BookOpen, 
  Clock, 
  CheckCircle, 
  Search,
  TrendingUp,
  Users,
  Target,
  Calendar,
  BarChart3,
  Filter
} from 'lucide-react';

interface TestResult {
  id: number;
  test_id: number;
  test_title: string;
  test_subject: string;
  student_id: number;
  student_name: string;
  student_email: string;
  score: number;
  max_score: number;
  percentage: number;
  status: string;
  started_at: string;
  completed_at: string;
  quiz_type: string;
}

export default function TeacherTestResultsPage() {
  const { user, token } = useAuth();
  const [results, setResults] = useState<TestResult[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedSubject, setSelectedSubject] = useState('all');
  const [selectedTest, setSelectedTest] = useState('all');

  // Statistiques
  const [stats, setStats] = useState({
    totalResults: 0,
    averageScore: 0,
    totalStudents: 0,
    completionRate: 0
  });

  useEffect(() => {
    if (user && token) {
      fetchResults();
    }
  }, [user, token]);

  const fetchResults = async () => {
    try {
      setLoading(true);
      
      if (!user || !token) {
        setError('Utilisateur non connecté');
        return;
      }

      console.log('🔥 [DEBUG] Récupération des résultats pour le professeur:', user.id);

      // Récupérer les résultats des tests adaptatifs
      const response = await fetch(`http://localhost:8000/api/v1/adaptive-evaluation/teacher/${user.id}/results`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });

      if (response.ok) {
        const data = await response.json();
        console.log('🔥 [DEBUG] Résultats récupérés:', data);
        setResults(data);
        
        // Calculer les statistiques
        calculateStats(data);
      } else {
        throw new Error('Erreur lors de la récupération des résultats');
      }
    } catch (error) {
      console.error('❌ Erreur:', error);
      setError('Erreur lors du chargement des résultats');
    } finally {
      setLoading(false);
    }
  };

  const calculateStats = (data: TestResult[]) => {
    if (data.length === 0) {
      setStats({
        totalResults: 0,
        averageScore: 0,
        totalStudents: 0,
        completionRate: 0
      });
      return;
    }

    const totalResults = data.length;
    const totalScore = data.reduce((sum, result) => sum + result.score, 0);
    const averageScore = Math.round(totalScore / totalResults);
    
    const uniqueStudents = new Set(data.map(result => result.student_id));
    const totalStudents = uniqueStudents.size;
    
    const completionRate = Math.round((totalResults / totalStudents) * 100);

    setStats({
      totalResults,
      averageScore,
      totalStudents,
      completionRate
    });
  };

  // Filtrage des résultats
  const filteredResults = results.filter(result => {
    const matchesSearch = result.test_title.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         result.student_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         result.test_subject.toLowerCase().includes(searchTerm.toLowerCase());
    
    const matchesSubject = selectedSubject === 'all' || result.test_subject === selectedSubject;
    const matchesTest = selectedTest === 'all' || result.test_id.toString() === selectedTest;

    return matchesSearch && matchesSubject && matchesTest;
  });

  // Obtenir les sujets uniques
  const subjects = ['all', ...Array.from(new Set(results.map(result => result.test_subject)))];
  
  // Obtenir les tests uniques
  const tests = ['all', ...Array.from(new Set(results.map(result => result.test_id)))];
  const testTitles = tests.map(testId => {
    if (testId === 'all') return 'all';
    const result = results.find(r => r.test_id.toString() === testId);
    return result ? result.test_title : testId;
  });

  const getScoreBadge = (score: number) => {
    if (score >= 80) return <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">Excellent</span>;
    if (score >= 60) return <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-yellow-100 text-yellow-800">Bon</span>;
    if (score >= 40) return <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-orange-100 text-orange-800">Moyen</span>;
    return <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-red-100 text-red-800">Faible</span>;
  };

  const getScoreColor = (score: number) => {
    if (score >= 80) return 'text-green-600';
    if (score >= 60) return 'text-yellow-600';
    if (score >= 40) return 'text-orange-600';
    return 'text-red-600';
  };

  if (loading) {
    return (
      <div className="flex h-screen bg-gray-50">
        <Sidebar />
        <div className="flex-1 ml-56 flex items-center justify-center">
          <div className="text-center">
            <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-600 mx-auto"></div>
            <p className="mt-4 text-gray-600">Chargement des résultats...</p>
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex h-screen bg-gray-50">
        <Sidebar />
        <div className="flex-1 ml-56 p-6">
          <div className="bg-red-50 border border-red-200 rounded-2xl p-6 shadow-lg">
            <h2 className="text-red-800 font-semibold mb-2 text-lg">Erreur</h2>
            <p className="text-red-700">{error}</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="flex h-screen bg-gray-50">
      <Sidebar />
      <div className="flex-1 ml-56 p-6 overflow-y-auto">
        <div className="mb-8">
          <div className="flex items-center space-x-3 mb-2">
            <BarChart3 className="h-8 w-8 text-blue-600" />
            <h1 className="text-3xl font-bold text-gray-800">Résultats des Tests</h1>
          </div>
          <p className="text-gray-600 text-lg">Consultez les performances de vos étudiants sur vos tests adaptatifs</p>
        </div>

        {/* Statistiques générales */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <Card>
            <div className="p-6">
              <div className="flex items-center space-x-3">
                <div className="p-3 bg-blue-100 rounded-xl">
                  <BookOpen className="h-6 w-6 text-blue-600" />
                </div>
                <div>
                  <p className="text-sm font-medium text-gray-600">Total Résultats</p>
                  <p className="text-2xl font-bold text-gray-900">{stats.totalResults}</p>
                </div>
              </div>
            </div>
          </Card>

          <Card>
            <div className="p-6">
              <div className="flex items-center space-x-3">
                <div className="p-3 bg-green-100 rounded-xl">
                  <TrendingUp className="h-6 w-6 text-green-600" />
                </div>
                <div>
                  <p className="text-sm font-medium text-gray-600">Score Moyen</p>
                  <p className="text-2xl font-bold text-gray-900">{stats.averageScore}%</p>
                </div>
              </div>
            </div>
          </Card>

          <Card>
            <div className="p-6">
              <div className="flex items-center space-x-3">
                <div className="p-3 bg-purple-100 rounded-xl">
                  <Users className="h-6 w-6 text-purple-600" />
                </div>
                <div>
                  <p className="text-sm font-medium text-gray-600">Étudiants</p>
                  <p className="text-2xl font-bold text-gray-900">{stats.totalStudents}</p>
                </div>
              </div>
            </div>
          </Card>

          <Card>
            <div className="p-6">
              <div className="flex items-center space-x-3">
                <div className="p-3 bg-orange-100 rounded-xl">
                  <Target className="h-6 w-6 text-orange-600" />
                </div>
                <div>
                  <p className="text-sm font-medium text-gray-600">Taux de Réussite</p>
                  <p className="text-2xl font-bold text-gray-900">{stats.completionRate}%</p>
                </div>
              </div>
            </div>
          </Card>
        </div>

        {/* Filtres et recherche */}
        <Card className="mb-6">
          <div className="p-6">
            <div className="flex items-center space-x-2 mb-4">
              <Filter className="h-5 w-5 text-gray-600" />
              <h3 className="text-lg font-semibold text-gray-800">Filtres et Recherche</h3>
            </div>
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

              <div className="md:w-48">
                <label htmlFor="subject" className="block text-sm font-medium text-gray-700 mb-2">Matière</label>
                <select
                  id="subject"
                  value={selectedSubject}
                  onChange={(e) => setSelectedSubject(e.target.value)}
                  className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200"
                >
                  {subjects.map((subject) => (
                    <option key={subject} value={subject}>
                      {subject === 'all' ? 'Toutes matières' : subject}
                    </option>
                  ))}
                </select>
              </div>

              <div className="md:w-48">
                <label htmlFor="test" className="block text-sm font-medium text-gray-700 mb-2">Test</label>
                <select
                  id="test"
                  value={selectedTest}
                  onChange={(e) => setSelectedTest(e.target.value)}
                  className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200"
                >
                  {tests.map((testId, index) => (
                    <option key={testId} value={testId}>
                      {testId === 'all' ? 'Tous les tests' : testTitles[index]}
                    </option>
                  ))}
                </select>
              </div>
            </div>
          </div>
        </Card>

        {/* Liste des résultats */}
        <Card>
          <div className="p-6">
            <div className="flex items-center space-x-2 mb-6">
              <CheckCircle className="h-6 w-6 text-green-600" />
              <h3 className="text-xl font-semibold text-gray-800">Résultats ({filteredResults.length})</h3>
            </div>
            
            {filteredResults.length === 0 ? (
              <div className="text-center py-12">
                <BookOpen className="h-16 w-16 text-gray-400 mx-auto mb-4" />
                <p className="text-gray-500 text-lg">Aucun résultat trouvé</p>
              </div>
            ) : (
              <div className="space-y-4">
                {filteredResults.map((result) => (
                  <div key={result.id} className="bg-white border border-gray-200 rounded-2xl p-6 hover:shadow-lg transition-all duration-200 hover:border-blue-300">
                    <div className="flex items-start justify-between">
                      <div className="flex-1">
                        <div className="flex items-center space-x-3 mb-4">
                          <h3 className="font-semibold text-xl text-gray-800">{result.test_title}</h3>
                          <span className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-purple-100 text-purple-800">Test Adaptatif</span>
                          {getScoreBadge(result.score)}
                        </div>
                        
                        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 text-sm text-gray-600 mb-4">
                          <div className="flex items-center space-x-2">
                            <div className="p-2 bg-blue-100 rounded-lg">
                              <Users className="h-4 w-4 text-blue-600" />
                            </div>
                            <div>
                              <span className="font-medium text-gray-800">Étudiant</span>
                              <p className="text-gray-600">{result.student_name}</p>
                            </div>
                          </div>
                          
                          <div className="flex items-center space-x-2">
                            <div className="p-2 bg-green-100 rounded-lg">
                              <BookOpen className="h-4 w-4 text-green-600" />
                            </div>
                            <div>
                              <span className="font-medium text-gray-800">Matière</span>
                              <p className="text-gray-600">{result.test_subject}</p>
                            </div>
                          </div>
                          
                          <div className="flex items-center space-x-2">
                            <div className="p-2 bg-orange-100 rounded-lg">
                              <Target className="h-4 w-4 text-orange-600" />
                            </div>
                            <div>
                              <span className="font-medium text-gray-800">Score</span>
                              <p className={`font-bold ${getScoreColor(result.score)}`}>
                                {result.score}/{result.max_score} ({result.percentage}%)
                              </p>
                            </div>
                          </div>
                          
                          <div className="flex items-center space-x-2">
                            <div className="p-2 bg-purple-100 rounded-lg">
                              <Calendar className="h-4 w-4 text-purple-600" />
                            </div>
                            <div>
                              <span className="font-medium text-gray-800">Terminé le</span>
                              <p className="text-gray-600">{new Date(result.completed_at).toLocaleDateString()}</p>
                            </div>
                          </div>
                        </div>

                        <div className="text-sm text-gray-500 bg-gray-50 rounded-lg p-3">
                          <span className="font-medium">Email:</span> {result.student_email}
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </Card>
      </div>
    </div>
  );
}



