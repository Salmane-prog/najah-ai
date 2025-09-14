'use client';

import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import DashboardLayout from '../dashboard/DashboardLayout';

interface Question {
  id: string;
  text: string;
  type: 'multiple_choice' | 'true_false' | 'short_answer' | 'essay';
  subject: string;
  topic: string;
  difficulty: number;
  cognitive_domain: string;
  irtParameters: {
    discrimination: number;
    guessing: number;
    difficulty: number;
    calibrated: boolean;
  };
  options?: string[];
  correctAnswer: string;
  explanation: string;
  tags: string[];
  createdBy: string;
  createdAt: string;
  lastUsed: string;
  usageCount: number;
  successRate: number;
}

interface Category {
  id: string;
  name: string;
  description: string;
  questionCount: number;
  color: string;
}

export default function QuestionBank() {
  const router = useRouter();
  const [questions, setQuestions] = useState<Question[]>([]);
  const [categories, setCategories] = useState<Category[]>([]);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState<'all' | 'categories' | 'create' | 'analysis'>('all');
  const [selectedCategory, setSelectedCategory] = useState<string>('all');
  const [searchQuery, setSearchQuery] = useState('');
  const [filterType, setFilterType] = useState<string>('all');
  const [filterDifficulty, setFilterDifficulty] = useState<string>('all');
  const [showCreateForm, setShowCreateForm] = useState(false);

  useEffect(() => {
    // Simuler le chargement des données
    setTimeout(() => {
      setCategories([
        { id: '1', name: 'Algèbre', description: 'Équations, inéquations, fonctions', questionCount: 45, color: 'blue' },
        { id: '2', name: 'Géométrie', description: 'Théorèmes, aires, volumes', questionCount: 38, color: 'green' },
        { id: '3', name: 'Calcul', description: 'Dérivées, intégrales, limites', questionCount: 52, color: 'purple' },
        { id: '4', name: 'Statistiques', description: 'Probabilités, distributions', questionCount: 28, color: 'orange' },
        { id: '5', name: 'Mécanique', description: 'Forces, mouvement, énergie', questionCount: 41, color: 'red' },
        { id: '6', name: 'Thermodynamique', description: 'Chaleur, entropie, cycles', questionCount: 33, color: 'indigo' }
      ]);

      setQuestions([
        {
          id: '1',
          text: 'Résolvez l\'équation du second degré : x² - 5x + 6 = 0',
          type: 'multiple_choice',
          subject: 'Mathématiques',
          topic: 'Algèbre',
          difficulty: 0.65,
          cognitive_domain: 'Application',
          irtParameters: {
            discrimination: 0.78,
            guessing: 0.22,
            difficulty: 0.65,
            calibrated: true
          },
          options: ['x = 2 ou x = 3', 'x = -2 ou x = -3', 'x = 1 ou x = 6', 'Aucune solution'],
          correctAnswer: 'x = 2 ou x = 3',
          explanation: 'En utilisant la formule quadratique ou en factorisant (x-2)(x-3) = 0',
          tags: ['équation', 'second degré', 'factorisation'],
          createdBy: 'Prof. Ben Ali',
          createdAt: '2024-01-15',
          lastUsed: 'Il y a 2 jours',
          usageCount: 23,
          successRate: 0.78
        },
        {
          id: '2',
          text: 'Calculez l\'aire d\'un cercle de rayon 7 cm',
          type: 'multiple_choice',
          subject: 'Mathématiques',
          topic: 'Géométrie',
          difficulty: 0.45,
          cognitive_domain: 'Compréhension',
          irtParameters: {
            discrimination: 0.65,
            guessing: 0.25,
            difficulty: 0.45,
            calibrated: true
          },
          options: ['49π cm²', '14π cm²', '98π cm²', '21π cm²'],
          correctAnswer: '49π cm²',
          explanation: 'A = πr² = π × 7² = 49π cm²',
          tags: ['cercle', 'aire', 'formule'],
          createdBy: 'Prof. Zahra',
          createdAt: '2024-01-10',
          lastUsed: 'Il y a 1 semaine',
          usageCount: 18,
          successRate: 0.85
        },
        {
          id: '3',
          text: 'Quelle est la dérivée de f(x) = 3x³ - 2x² + 5x - 1 ?',
          type: 'multiple_choice',
          subject: 'Mathématiques',
          topic: 'Calcul',
          difficulty: 0.75,
          cognitive_domain: 'Application',
          irtParameters: {
            discrimination: 0.82,
            guessing: 0.18,
            difficulty: 0.75,
            calibrated: true
          },
          options: ['9x² - 4x + 5', '9x² - 4x + 4', '9x² - 2x + 5', '6x² - 4x + 5'],
          correctAnswer: '9x² - 4x + 5',
          explanation: 'f\'(x) = 9x² - 4x + 5 (dérivée de chaque terme)',
          tags: ['dérivée', 'polynôme', 'calcul'],
          createdBy: 'Prof. Hassan',
          createdAt: '2024-01-08',
          lastUsed: 'Il y a 3 jours',
          usageCount: 31,
          successRate: 0.71
        }
      ]);

      setLoading(false);
    }, 1000);
  }, []);

  const filteredQuestions = questions.filter(question => {
    const matchesCategory = selectedCategory === 'all' || question.topic === categories.find(c => c.id === selectedCategory)?.name;
    const matchesSearch = question.text.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         question.tags.some(tag => tag.toLowerCase().includes(searchQuery.toLowerCase()));
    const matchesType = filterType === 'all' || question.type === filterType;
    const matchesDifficulty = filterDifficulty === 'all' || 
      (filterDifficulty === 'easy' && question.difficulty <= 0.4) ||
      (filterDifficulty === 'medium' && question.difficulty > 0.4 && question.difficulty <= 0.7) ||
      (filterDifficulty === 'hard' && question.difficulty > 0.7);
    
    return matchesCategory && matchesSearch && matchesType && matchesDifficulty;
  });

  const getDifficultyColor = (difficulty: number) => {
    if (difficulty <= 0.4) return 'bg-green-100 text-green-800';
    if (difficulty <= 0.7) return 'bg-yellow-100 text-yellow-800';
    return 'bg-red-100 text-red-800';
  };

  const getDifficultyText = (difficulty: number) => {
    if (difficulty <= 0.4) return 'Facile';
    if (difficulty <= 0.7) return 'Moyen';
    return 'Difficile';
  };

  const getTypeIcon = (type: string) => {
    switch (type) {
      case 'multiple_choice': return '☑️';
      case 'true_false': return '✅';
      case 'short_answer': return '✏️';
      case 'essay': return '📝';
      default: return '❓';
    }
  };

  const getCognitiveDomainColor = (domain: string) => {
    const colors = {
      'Compréhension': 'bg-blue-100 text-blue-800',
      'Application': 'bg-green-100 text-green-800',
      'Analyse': 'bg-purple-100 text-purple-800',
      'Évaluation': 'bg-orange-100 text-orange-800',
      'Création': 'bg-red-100 text-red-800'
    };
    return colors[domain as keyof typeof colors] || 'bg-gray-100 text-gray-800';
  };

  if (loading) {
    return (
      <DashboardLayout userType="teacher" title="Banque de Questions" subtitle="Chargement...">
        <div className="flex items-center justify-center h-64">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
        </div>
      </DashboardLayout>
    );
  }

  return (
    <DashboardLayout 
      userType="teacher" 
      title="Banque de Questions" 
      subtitle="Gérer et organiser votre collection de questions"
    >
      {/* En-tête avec statistiques */}
      <div className="mb-8">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
          <div className="bg-white rounded-lg shadow p-6 border-l-4 border-blue-500">
            <div className="flex items-center">
              <div className="p-3 rounded-full bg-blue-100 text-blue-600">
                <span className="text-2xl">❓</span>
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Total Questions</p>
                <p className="text-2xl font-semibold text-gray-900">{questions.length}</p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6 border-l-4 border-green-500">
            <div className="flex items-center">
              <div className="p-3 rounded-full bg-green-100 text-green-600">
                <span className="text-2xl">🏷️</span>
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Catégories</p>
                <p className="text-2xl font-semibold text-gray-900">{categories.length}</p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6 border-l-4 border-purple-500">
            <div className="flex items-center">
              <div className="p-3 rounded-full bg-purple-100 text-purple-600">
                <span className="text-2xl">📊</span>
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Calibrées IRT</p>
                <p className="text-2xl font-semibold text-gray-900">
                  {questions.filter(q => q.irtParameters.calibrated).length}
                </p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6 border-l-4 border-orange-500">
            <div className="flex items-center">
              <div className="p-3 rounded-full bg-orange-100 text-orange-600">
                <span className="text-2xl">📈</span>
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Taux de Réussite</p>
                <p className="text-2xl font-semibold text-gray-900">
                  {Math.round(questions.reduce((acc, q) => acc + q.successRate, 0) / questions.length * 100)}%
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Onglets de navigation */}
      <div className="bg-white rounded-lg shadow mb-8">
        <div className="border-b border-gray-200">
          <nav className="flex space-x-8 px-6">
            {[
              { id: 'all', label: 'Toutes les Questions', icon: '❓' },
              { id: 'categories', label: 'Catégories', icon: '🏷️' },
              { id: 'create', label: 'Créer', icon: '➕' },
              { id: 'analysis', label: 'Analyse', icon: '📊' }
            ].map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id as any)}
                className={`flex items-center space-x-2 py-4 px-1 border-b-2 font-medium text-sm ${
                  activeTab === tab.id
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                <span>{tab.icon}</span>
                <span>{tab.label}</span>
              </button>
            ))}
          </nav>
        </div>

        <div className="p-6">
          {/* Toutes les questions */}
          {activeTab === 'all' && (
            <div className="space-y-6">
              {/* Filtres et recherche */}
              <div className="flex flex-col lg:flex-row gap-4">
                <div className="flex-1">
                  <input
                    type="text"
                    placeholder="Rechercher par texte, tags ou sujet..."
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />
                </div>
                
                <select
                  value={selectedCategory}
                  onChange={(e) => setSelectedCategory(e.target.value)}
                  className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                >
                  <option value="all">Toutes les catégories</option>
                  {categories.map(category => (
                    <option key={category.id} value={category.id}>{category.name}</option>
                  ))}
                </select>
                
                <select
                  value={filterType}
                  onChange={(e) => setFilterType(e.target.value)}
                  className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                >
                  <option value="all">Tous les types</option>
                  <option value="multiple_choice">Choix multiple</option>
                  <option value="true_false">Vrai/Faux</option>
                  <option value="short_answer">Réponse courte</option>
                  <option value="essay">Dissertation</option>
                </select>
                
                <select
                  value={filterDifficulty}
                  onChange={(e) => setFilterDifficulty(e.target.value)}
                  className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                >
                  <option value="all">Toutes difficultés</option>
                  <option value="easy">Facile</option>
                  <option value="medium">Moyen</option>
                  <option value="hard">Difficile</option>
                </select>
              </div>

              {/* Liste des questions */}
              <div className="space-y-4">
                {filteredQuestions.map((question) => (
                  <div key={question.id} className="bg-gray-50 rounded-lg p-6 border border-gray-200 hover:border-blue-300 transition-colors">
                    <div className="flex items-start justify-between mb-4">
                      <div className="flex items-center space-x-3">
                        <span className="text-2xl">{getTypeIcon(question.type)}</span>
                        <div>
                          <h3 className="text-lg font-semibold text-gray-900">{question.text}</h3>
                          <div className="flex items-center space-x-2 mt-1">
                            <span className="text-sm text-gray-600">{question.subject}</span>
                            <span className="text-gray-400">•</span>
                            <span className="text-sm text-gray-600">{question.topic}</span>
                          </div>
                        </div>
                      </div>
                      
                      <div className="flex items-center space-x-2">
                        <span className={`px-2 py-1 text-xs font-medium rounded-full ${getDifficultyColor(question.difficulty)}`}>
                          {getDifficultyText(question.difficulty)}
                        </span>
                        <span className={`px-2 py-1 text-xs font-medium rounded-full ${getCognitiveDomainColor(question.cognitive_domain)}`}>
                          {question.cognitive_domain}
                        </span>
                      </div>
                    </div>

                    {/* Options de réponse */}
                    {question.options && (
                      <div className="mb-4">
                        <p className="text-sm font-medium text-gray-700 mb-2">Options :</p>
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
                          {question.options.map((option, index) => (
                            <div key={index} className="text-sm text-gray-600">
                              {String.fromCharCode(65 + index)}. {option}
                            </div>
                          ))}
                        </div>
                      </div>
                    )}

                    {/* Métadonnées IRT */}
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4 text-sm">
                      <div>
                        <span className="text-gray-600">Discrimination :</span>
                        <span className="ml-2 font-medium">{question.irtParameters.discrimination.toFixed(2)}</span>
                      </div>
                      <div>
                        <span className="text-gray-600">Difficulté :</span>
                        <span className="ml-2 font-medium">{(question.irtParameters.difficulty * 100).toFixed(0)}%</span>
                      </div>
                      <div>
                        <span className="text-gray-600">Taux de réussite :</span>
                        <span className="ml-2 font-medium">{(question.successRate * 100).toFixed(0)}%</span>
                      </div>
                      <div>
                        <span className="text-gray-600">Utilisations :</span>
                        <span className="ml-2 font-medium">{question.usageCount}</span>
                      </div>
                    </div>

                    {/* Tags */}
                    <div className="flex flex-wrap gap-2 mb-4">
                      {question.tags.map((tag, index) => (
                        <span key={index} className="px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded-full">
                          {tag}
                        </span>
                      ))}
                    </div>

                    {/* Actions */}
                    <div className="flex justify-between items-center">
                      <div className="text-xs text-gray-500">
                        Créé par {question.createdBy} le {question.createdAt}
                      </div>
                      <div className="flex space-x-2">
                        <button className="px-3 py-1 text-xs bg-blue-100 text-blue-800 rounded hover:bg-blue-200">
                          Modifier
                        </button>
                        <button className="px-3 py-1 text-xs bg-green-100 text-green-800 rounded hover:bg-green-200">
                          Prévisualiser
                        </button>
                        <button className="px-3 py-1 text-xs bg-purple-100 text-purple-800 rounded hover:bg-purple-200">
                          Calibrer IRT
                        </button>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Catégories */}
          {activeTab === 'categories' && (
            <div className="space-y-6">
              <div className="flex justify-between items-center">
                <h3 className="text-lg font-semibold text-gray-900">Gestion des Catégories</h3>
                <button className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors">
                  Nouvelle Catégorie
                </button>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {categories.map((category) => (
                  <div key={category.id} className="bg-gray-50 rounded-lg p-6 border border-gray-200">
                    <div className="flex items-center justify-between mb-4">
                      <h4 className="text-lg font-semibold text-gray-900">{category.name}</h4>
                      <span className="px-2 py-1 text-xs font-medium bg-blue-100 text-blue-800 rounded-full">
                        {category.questionCount} questions
                      </span>
                    </div>
                    <p className="text-sm text-gray-600 mb-4">{category.description}</p>
                    <div className="flex justify-between items-center">
                      <button className="px-3 py-1 text-xs bg-blue-100 text-blue-800 rounded hover:bg-blue-200">
                        Voir questions
                      </button>
                      <button className="px-3 py-1 text-xs bg-green-100 text-green-800 rounded hover:bg-green-200">
                        Modifier
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Créer une question */}
          {activeTab === 'create' && (
            <div className="space-y-6">
              <h3 className="text-lg font-semibold text-gray-900">Créer une Nouvelle Question</h3>
              
              <div className="bg-gray-50 rounded-lg p-6">
                <form className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Type de question
                    </label>
                    <select className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent">
                      <option value="multiple_choice">Choix multiple</option>
                      <option value="true_false">Vrai/Faux</option>
                      <option value="short_answer">Réponse courte</option>
                      <option value="essay">Dissertation</option>
                    </select>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Sujet
                    </label>
                    <select className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent">
                      <option value="mathematics">Mathématiques</option>
                      <option value="physics">Physique</option>
                      <option value="chemistry">Chimie</option>
                      <option value="history">Histoire</option>
                    </select>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Texte de la question
                    </label>
                    <textarea 
                      rows={4}
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      placeholder="Entrez le texte de votre question..."
                    />
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Difficulté estimée
                      </label>
                      <select className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent">
                        <option value="0.3">Facile (30%)</option>
                        <option value="0.5">Moyen (50%)</option>
                        <option value="0.7">Difficile (70%)</option>
                      </select>
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Domaine cognitif
                      </label>
                      <select className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent">
                        <option value="comprehension">Compréhension</option>
                        <option value="application">Application</option>
                        <option value="analysis">Analyse</option>
                        <option value="evaluation">Évaluation</option>
                        <option value="creation">Création</option>
                      </select>
                    </div>
                  </div>

                  <div className="flex justify-end space-x-3">
                    <button type="button" className="px-4 py-2 text-gray-600 hover:text-gray-800">
                      Annuler
                    </button>
                    <button type="submit" className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700">
                      Créer la Question
                    </button>
                  </div>
                </form>
              </div>
            </div>
          )}

          {/* Analyse */}
          {activeTab === 'analysis' && (
            <div className="space-y-6">
              <h3 className="text-lg font-semibold text-gray-900">Analyse de la Banque de Questions</h3>
              
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {/* Distribution par difficulté */}
                <div className="bg-gray-50 rounded-lg p-6">
                  <h4 className="text-lg font-semibold text-gray-900 mb-4">Distribution par Difficulté</h4>
                  <div className="space-y-3">
                    {[
                      { level: 'Facile', count: questions.filter(q => q.difficulty <= 0.4).length, percentage: 35 },
                      { level: 'Moyen', count: questions.filter(q => q.difficulty > 0.4 && q.difficulty <= 0.7).length, percentage: 45 },
                      { level: 'Difficile', count: questions.filter(q => q.difficulty > 0.7).length, percentage: 20 }
                    ].map((item) => (
                      <div key={item.level} className="flex items-center justify-between">
                        <span className="text-sm font-medium text-gray-700">{item.level}</span>
                        <div className="flex items-center space-x-3">
                          <div className="w-24 bg-gray-200 rounded-full h-2">
                            <div 
                              className="bg-blue-500 h-2 rounded-full"
                              style={{ width: `${item.percentage}%` }}
                            ></div>
                          </div>
                          <span className="text-sm text-gray-600 w-12 text-right">{item.count}</span>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Performance IRT */}
                <div className="bg-gray-50 rounded-lg p-6">
                  <h4 className="text-lg font-semibold text-gray-900 mb-4">Performance IRT</h4>
                  <div className="space-y-3">
                    <div className="flex justify-between items-center">
                      <span className="text-sm text-gray-700">Questions calibrées</span>
                      <span className="text-sm font-semibold text-gray-900">
                        {questions.filter(q => q.irtParameters.calibrated).length} / {questions.length}
                      </span>
                    </div>
                    <div className="flex justify-between items-center">
                      <span className="text-sm text-gray-700">Discrimination moyenne</span>
                      <span className="text-sm font-semibold text-gray-900">
                        {(questions.reduce((acc, q) => acc + q.irtParameters.discrimination, 0) / questions.length).toFixed(2)}
                      </span>
                    </div>
                    <div className="flex justify-between items-center">
                      <span className="text-sm text-gray-700">Taux de réussite moyen</span>
                      <span className="text-sm font-semibold text-gray-900">
                        {(questions.reduce((acc, q) => acc + q.successRate, 0) / questions.length * 100).toFixed(0)}%
                      </span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </DashboardLayout>
  );
}












