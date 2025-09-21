'use client';

import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';

interface Question {
  id: number;
  question_text: string;
  question_type: string;
  subject: string;
  difficulty: number;
  competency: string;
  learning_style: string;
  estimated_time: number;
  cognitive_load: number;
  tags: string[];
}

export default function QuestionBankPage() {
  const router = useRouter();
  const [questions, setQuestions] = useState<Question[]>([]);
  const [loading, setLoading] = useState(true);
  const [filters, setFilters] = useState({
    subject: '',
    difficulty: '',
    questionType: '',
    learningStyle: ''
  });
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    loadQuestions();
  }, [filters]);

  const loadQuestions = async () => {
    try {
      setLoading(true);
      
      // Construire l'URL avec les filtres
      const params = new URLSearchParams();
      if (filters.subject) params.append('subject', filters.subject);
      if (filters.difficulty) params.append('difficulty', filters.difficulty);
      if (filters.questionType) params.append('question_type', filters.questionType);
      if (filters.learningStyle) params.append('learning_style', filters.learningStyle);
      params.append('limit', '50');

      const response = await fetch(`/api/v1/advanced/questions/extended?${params.toString()}`);
      
      if (response.ok) {
        const data = await response.json();
        setQuestions(data.questions || []);
      } else {
        console.error('Erreur lors du chargement des questions');
        // Utiliser des questions simulées
        setQuestions(generateMockQuestions());
      }
    } catch (error) {
      console.error('Erreur de connexion:', error);
      setQuestions(generateMockQuestions());
    } finally {
      setLoading(false);
    }
  };

  const generateMockQuestions = (): Question[] => {
    return [
      {
        id: 1,
        question_text: "Quel est le résultat de 15 + 27 ?",
        question_type: "multiple_choice",
        subject: "math",
        difficulty: 3,
        competency: "calcul mental",
        learning_style: "visuel",
        estimated_time: 30,
        cognitive_load: 0.3,
        tags: ["addition", "nombres", "facile"]
      },
      {
        id: 2,
        question_text: "Complétez la phrase : 'Le chat ___ sur le toit.'",
        question_type: "free_text",
        subject: "french",
        difficulty: 4,
        competency: "conjugaison",
        learning_style: "auditif",
        estimated_time: 45,
        cognitive_load: 0.4,
        tags: ["grammaire", "verbes", "conjugaison"]
      },
      {
        id: 3,
        question_text: "Expliquez le processus de photosynthèse.",
        question_type: "free_text",
        subject: "science",
        difficulty: 7,
        competency: "compréhension scientifique",
        learning_style: "kinesthésique",
        estimated_time: 120,
        cognitive_load: 0.8,
        tags: ["biologie", "photosynthèse", "processus"]
      }
    ];
  };

  const filteredQuestions = questions.filter(question => {
    const matchesSearch = question.question_text.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         question.competency.toLowerCase().includes(searchTerm.toLowerCase());
    
    const matchesFilters = (!filters.subject || question.subject === filters.subject) &&
                          (!filters.difficulty || question.difficulty === parseInt(filters.difficulty)) &&
                          (!filters.questionType || question.question_type === filters.questionType) &&
                          (!filters.learningStyle || question.learning_style === filters.learningStyle);

    return matchesSearch && matchesFilters;
  });

  const getDifficultyColor = (difficulty: number) => {
    if (difficulty <= 3) return 'bg-green-100 text-green-800';
    if (difficulty <= 6) return 'bg-yellow-100 text-yellow-800';
    return 'bg-red-100 text-red-800';
  };

  const getDifficultyLabel = (difficulty: number) => {
    if (difficulty <= 3) return 'Facile';
    if (difficulty <= 6) return 'Moyen';
    return 'Difficile';
  };

  const getQuestionTypeIcon = (type: string) => {
    switch (type) {
      case 'multiple_choice': return '🔘';
      case 'free_text': return '📝';
      case 'image': return '🖼️';
      default: return '❓';
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Chargement de la banque de questions...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold text-gray-900">
                🗃️ Banque de Questions Étendue
              </h1>
              <p className="text-gray-600 mt-1">
                Gérer et organiser votre collection de questions intelligentes
              </p>
            </div>
            <div className="flex space-x-3">
              <button
                onClick={() => router.push('/dashboard/teacher/questions/create')}
                className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors"
              >
                ➕ Créer une Question
              </button>
              <button
                onClick={() => router.push('/dashboard/teacher')}
                className="bg-gray-100 text-gray-700 px-4 py-2 rounded-lg hover:bg-gray-200 transition-colors"
              >
                ← Retour au Dashboard
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Filtres et recherche */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <div className="bg-white rounded-xl shadow-lg p-6 mb-6">
          <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
            {/* Recherche */}
            <div className="md:col-span-2">
              <label className="block text-sm font-medium text-gray-700 mb-2">
                🔍 Rechercher
              </label>
              <input
                type="text"
                placeholder="Rechercher dans les questions..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full p-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              />
            </div>

            {/* Filtre matière */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                📚 Matière
              </label>
              <select
                value={filters.subject}
                onChange={(e) => setFilters(prev => ({ ...prev, subject: e.target.value }))}
                className="w-full p-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              >
                <option value="">Toutes</option>
                <option value="math">Mathématiques</option>
                <option value="french">Français</option>
                <option value="science">Sciences</option>
                <option value="history">Histoire</option>
              </select>
            </div>

            {/* Filtre difficulté */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                🎯 Difficulté
              </label>
              <select
                value={filters.difficulty}
                onChange={(e) => setFilters(prev => ({ ...prev, difficulty: e.target.value }))}
                className="w-full p-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              >
                <option value="">Toutes</option>
                <option value="3">Facile (1-3)</option>
                <option value="5">Moyen (4-6)</option>
                <option value="8">Difficile (7-10)</option>
              </select>
            </div>

            {/* Filtre type de question */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                ❓ Type
              </label>
              <select
                value={filters.questionType}
                onChange={(e) => setFilters(prev => ({ ...prev, questionType: e.target.value }))}
                className="w-full p-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              >
                <option value="">Tous</option>
                <option value="multiple_choice">QCM</option>
                <option value="free_text">Texte libre</option>
                <option value="image">Image</option>
              </select>
            </div>
          </div>
        </div>

        {/* Statistiques */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-6">
          <div className="bg-white rounded-xl shadow-lg p-6 text-center">
            <div className="text-3xl font-bold text-blue-600">{questions.length}</div>
            <div className="text-gray-600">Questions totales</div>
          </div>
          <div className="bg-white rounded-xl shadow-lg p-6 text-center">
            <div className="text-3xl font-bold text-green-600">
              {questions.filter(q => q.difficulty <= 3).length}
            </div>
            <div className="text-gray-600">Questions faciles</div>
          </div>
          <div className="bg-white rounded-xl shadow-lg p-6 text-center">
            <div className="text-3xl font-bold text-yellow-600">
              {questions.filter(q => q.difficulty > 3 && q.difficulty <= 6).length}
            </div>
            <div className="text-gray-600">Questions moyennes</div>
          </div>
          <div className="bg-white rounded-xl shadow-lg p-6 text-center">
            <div className="text-3xl font-bold text-red-600">
              {questions.filter(q => q.difficulty > 6).length}
            </div>
            <div className="text-gray-600">Questions difficiles</div>
          </div>
        </div>

        {/* Liste des questions */}
        <div className="bg-white rounded-xl shadow-lg overflow-hidden">
          <div className="px-6 py-4 border-b border-gray-200">
            <h3 className="text-lg font-semibold text-gray-900">
              Questions ({filteredQuestions.length})
            </h3>
          </div>
          
          <div className="divide-y divide-gray-200">
            {filteredQuestions.map((question) => (
              <div key={question.id} className="p-6 hover:bg-gray-50 transition-colors">
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <div className="flex items-center space-x-3 mb-2">
                      <span className="text-2xl">{getQuestionTypeIcon(question.question_type)}</span>
                      <span className="text-sm text-gray-500 capitalize">{question.subject}</span>
                      <span className={`px-2 py-1 rounded-full text-xs font-medium ${getDifficultyColor(question.difficulty)}`}>
                        {getDifficultyLabel(question.difficulty)}
                      </span>
                      <span className="text-sm text-gray-500">
                        ⏱️ {question.estimated_time}s
                      </span>
                      <span className="text-sm text-gray-500">
                        🧠 {Math.round(question.cognitive_load * 100)}%
                      </span>
                    </div>
                    
                    <h4 className="text-lg font-medium text-gray-900 mb-2">
                      {question.question_text}
                    </h4>
                    
                    <div className="flex items-center space-x-4 text-sm text-gray-600">
                      <span>🎯 {question.competency}</span>
                      <span>👁️ {question.learning_style}</span>
                    </div>
                    
                    {question.tags && question.tags.length > 0 && (
                      <div className="flex flex-wrap gap-2 mt-3">
                        {question.tags.map((tag, index) => (
                          <span
                            key={index}
                            className="px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded-full"
                          >
                            {tag}
                          </span>
                        ))}
                      </div>
                    )}
                  </div>
                  
                  <div className="flex space-x-2 ml-4">
                    <button
                      onClick={() => router.push(`/dashboard/teacher/questions/edit/${question.id}`)}
                      className="bg-blue-100 text-blue-700 px-3 py-1 rounded-md text-sm hover:bg-blue-200 transition-colors"
                    >
                      ✏️ Modifier
                    </button>
                    <button
                      onClick={() => router.push(`/dashboard/teacher/questions/view/${question.id}`)}
                      className="bg-green-100 text-green-700 px-3 py-1 rounded-md text-sm hover:bg-green-200 transition-colors"
                    >
                      👁️ Voir
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
          
          {filteredQuestions.length === 0 && (
            <div className="p-12 text-center">
              <div className="text-gray-400 text-6xl mb-4">🔍</div>
              <h3 className="text-lg font-medium text-gray-900 mb-2">
                Aucune question trouvée
              </h3>
              <p className="text-gray-500">
                Essayez de modifier vos filtres ou créez une nouvelle question.
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}















