'use client';

import React, { useState, useEffect } from 'react';
import Sidebar from '../../../../components/Sidebar';
import { useAuth  } from '../../../../hooks/useAuth';
import { 
  Target, 
  Plus, 
  Users, 
  BookOpen, 
  TrendingUp, 
  FileText,
  Edit,
  Trash2,
  Eye,
  BarChart3,
  Award,
  Clock
} from 'lucide-react';

interface Competency {
  id: number;
  name: string;
  description: string;
  subject: string;
  level: string;
  category: string;
}

interface ContinuousAssessment {
  id: number;
  title: string;
  description: string;
  assessment_type: string;
  subject: string;
  competencies_targeted: number[];
  weight: number;
  due_date: string;
  created_at: string;
}

interface StudentCompetency {
  id: number;
  competency_id: number;
  competency_name: string;
  competency_subject: string;
  level_achieved: string;
  progress_percentage: number;
  last_assessed: string;
  assessment_count: number;
}

export default function ContinuousAssessmentPage() {
  const { user, token } = useAuth();
  const [competencies, setCompetencies] = useState<Competency[]>([]);
  const [assessments, setAssessments] = useState<ContinuousAssessment[]>([]);
  const [studentCompetencies, setStudentCompetencies] = useState<StudentCompetency[]>([]);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState<'competencies' | 'assessments' | 'progress'>('competencies');
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [showAssessmentModal, setShowAssessmentModal] = useState(false);
  const [selectedStudent, setSelectedStudent] = useState<number | null>(null);

  // Formulaires
  const [competencyForm, setCompetencyForm] = useState({
    name: '',
    description: '',
    subject: '',
    level: 'beginner',
    category: 'knowledge'
  });

  const [assessmentForm, setAssessmentForm] = useState({
    title: '',
    description: '',
    assessment_type: 'quiz',
    subject: '',
    competencies_targeted: [] as number[],
    weight: 1.0,
    due_date: ''
  });

  useEffect(() => {
    if (token) {
      fetchData();
    }
  }, [token, activeTab]);

  const fetchData = async () => {
    try {
      setLoading(true);
      
      if (activeTab === 'competencies') {
        const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/v1/continuous_assessment/competencies`, {
          headers: { 'Authorization': `Bearer ${token}` }
        });
        if (response.ok) {
          const data = await response.json();
          setCompetencies(data);
        }
      } else if (activeTab === 'assessments') {
        const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/v1/continuous_assessment/assessments`, {
          headers: { 'Authorization': `Bearer ${token}` }
        });
        if (response.ok) {
          const data = await response.json();
          setAssessments(data);
        }
      }
    } catch (err) {
      console.error('Erreur lors du chargement des données:', err);
    } finally {
      setLoading(false);
    }
  };

  const createCompetency = async () => {
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/v1/continuous_assessment/competencies`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(competencyForm)
      });

      if (response.ok) {
        setShowCreateModal(false);
        setCompetencyForm({
          name: '',
          description: '',
          subject: '',
          level: 'beginner',
          category: 'knowledge'
        });
        fetchData();
      }
    } catch (err) {
      console.error('Erreur lors de la création de la compétence:', err);
    }
  };

  const createAssessment = async () => {
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/v1/continuous_assessment/assessments`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(assessmentForm)
      });

      if (response.ok) {
        setShowAssessmentModal(false);
        setAssessmentForm({
          title: '',
          description: '',
          assessment_type: 'quiz',
          subject: '',
          competencies_targeted: [],
          weight: 1.0,
          due_date: ''
        });
        fetchData();
      }
    } catch (err) {
      console.error('Erreur lors de la création de l\'évaluation:', err);
    }
  };

  const getLevelColor = (level: string) => {
    switch (level) {
      case 'beginner': return 'bg-green-100 text-green-800';
      case 'intermediate': return 'bg-yellow-100 text-yellow-800';
      case 'advanced': return 'bg-red-100 text-red-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const getAssessmentTypeIcon = (type: string) => {
    switch (type) {
      case 'quiz': return <FileText size={16} />;
      case 'project': return <BookOpen size={16} />;
      case 'presentation': return <Users size={16} />;
      case 'observation': return <Eye size={16} />;
      default: return <Target size={16} />;
    }
  };

  if (loading) {
    return (
      <div className="flex min-h-screen bg-gray-50">
        <Sidebar userType="teacher" />
        <div className="flex-1 flex items-center justify-center">
          <div className="text-blue-600 animate-pulse text-xl font-bold">Chargement...</div>
        </div>
      </div>
    );
  }

  return (
    <div className="flex min-h-screen bg-gray-50">
      <Sidebar userType="teacher" />
      <div className="flex-1 overflow-auto pl-0 md:pl-56">
        <div className="p-6">
          {/* Header */}
          <div className="mb-6 flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-gray-800 mb-2">Évaluation Continue</h1>
              <p className="text-gray-600">Gérez les compétences et les évaluations continues</p>
            </div>
            <div className="flex gap-2">
              {activeTab === 'competencies' && (
                <button
                  onClick={() => setShowCreateModal(true)}
                  className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition"
                >
                  <Plus size={16} />
                  Nouvelle compétence
                </button>
              )}
              {activeTab === 'assessments' && (
                <button
                  onClick={() => setShowAssessmentModal(true)}
                  className="flex items-center gap-2 px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition"
                >
                  <Plus size={16} />
                  Nouvelle évaluation
                </button>
              )}
            </div>
          </div>

          {/* Navigation par onglets */}
          <div className="mb-6">
            <div className="flex space-x-1 bg-white rounded-lg p-1 shadow-sm">
              {[
                { id: 'competencies', label: 'Compétences', icon: <Target size={16} /> },
                { id: 'assessments', label: 'Évaluations', icon: <FileText size={16} /> },
                { id: 'progress', label: 'Progression', icon: <TrendingUp size={16} /> }
              ].map((tab) => (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id as any)}
                  className={`flex items-center gap-2 px-4 py-2 rounded-md font-medium transition ${
                    activeTab === tab.id
                      ? 'bg-blue-100 text-blue-700'
                      : 'text-gray-600 hover:text-gray-900'
                  }`}
                >
                  {tab.icon}
                  {tab.label}
                </button>
              ))}
            </div>
          </div>

          {/* Contenu des onglets */}
          {activeTab === 'competencies' && (
            <div className="bg-white rounded-xl shadow-lg p-6">
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {competencies.map((competency) => (
                  <div key={competency.id} className="border rounded-lg p-4 hover:shadow-md transition">
                    <div className="flex items-start justify-between mb-2">
                      <h3 className="font-semibold text-gray-800">{competency.name}</h3>
                      <span className={`px-2 py-1 rounded-full text-xs font-medium ${getLevelColor(competency.level)}`}>
                        {competency.level}
                      </span>
                    </div>
                    <p className="text-sm text-gray-600 mb-3">{competency.description}</p>
                    <div className="flex items-center justify-between text-xs text-gray-500">
                      <span>{competency.subject}</span>
                      <span className="capitalize">{competency.category}</span>
                    </div>
                  </div>
                ))}
              </div>
              
              {competencies.length === 0 && (
                <div className="text-center py-12">
                  <Target className="mx-auto text-gray-400 mb-4" size={48} />
                  <p className="text-gray-600">Aucune compétence créée</p>
                  <p className="text-sm text-gray-500">Créez votre première compétence pour commencer</p>
                </div>
              )}
            </div>
          )}

          {activeTab === 'assessments' && (
            <div className="bg-white rounded-xl shadow-lg p-6">
              <div className="space-y-4">
                {assessments.map((assessment) => (
                  <div key={assessment.id} className="border rounded-lg p-4 hover:shadow-md transition">
                    <div className="flex items-start justify-between mb-3">
                      <div className="flex items-center gap-2">
                        {getAssessmentTypeIcon(assessment.assessment_type)}
                        <h3 className="font-semibold text-gray-800">{assessment.title}</h3>
                      </div>
                      <div className="flex gap-2">
                        <button className="p-1 text-gray-400 hover:text-blue-600">
                          <Edit size={14} />
                        </button>
                        <button className="p-1 text-gray-400 hover:text-red-600">
                          <Trash2 size={14} />
                        </button>
                      </div>
                    </div>
                    <p className="text-sm text-gray-600 mb-3">{assessment.description}</p>
                    <div className="flex items-center justify-between text-xs text-gray-500">
                      <div className="flex items-center gap-4">
                        <span>{assessment.subject}</span>
                        <span className="capitalize">{assessment.assessment_type}</span>
                        <span>Poids: {assessment.weight}</span>
                      </div>
                      <div className="flex items-center gap-2">
                        <Clock size={12} />
                        <span>{new Date(assessment.due_date).toLocaleDateString()}</span>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
              
              {assessments.length === 0 && (
                <div className="text-center py-12">
                  <FileText className="mx-auto text-gray-400 mb-4" size={48} />
                  <p className="text-gray-600">Aucune évaluation créée</p>
                  <p className="text-sm text-gray-500">Créez votre première évaluation pour commencer</p>
                </div>
              )}
            </div>
          )}

          {activeTab === 'progress' && (
            <div className="bg-white rounded-xl shadow-lg p-6">
              <div className="mb-4">
                <h3 className="text-lg font-semibold text-gray-800 mb-2">Progression des étudiants</h3>
                <p className="text-sm text-gray-600">Sélectionnez un étudiant pour voir sa progression</p>
              </div>
              
              <div className="text-center py-12">
                <TrendingUp className="mx-auto text-gray-400 mb-4" size={48} />
                <p className="text-gray-600">Interface de progression en cours de développement</p>
                <p className="text-sm text-gray-500">Cette fonctionnalité sera bientôt disponible</p>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Modal de création de compétence */}
      {showCreateModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 w-full max-w-md">
            <h2 className="text-xl font-bold mb-4">Nouvelle compétence</h2>
            <form onSubmit={(e) => { e.preventDefault(); createCompetency(); }}>
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Nom</label>
                  <input
                    type="text"
                    value={competencyForm.name}
                    onChange={(e) => setCompetencyForm({...competencyForm, name: e.target.value})}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    required
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Description</label>
                  <textarea
                    value={competencyForm.description}
                    onChange={(e) => setCompetencyForm({...competencyForm, description: e.target.value})}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    rows={3}
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Matière</label>
                  <input
                    type="text"
                    value={competencyForm.subject}
                    onChange={(e) => setCompetencyForm({...competencyForm, subject: e.target.value})}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    required
                  />
                </div>
                
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Niveau</label>
                    <select
                      value={competencyForm.level}
                      onChange={(e) => setCompetencyForm({...competencyForm, level: e.target.value})}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    >
                      <option value="beginner">Débutant</option>
                      <option value="intermediate">Intermédiaire</option>
                      <option value="advanced">Avancé</option>
                    </select>
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Catégorie</label>
                    <select
                      value={competencyForm.category}
                      onChange={(e) => setCompetencyForm({...competencyForm, category: e.target.value})}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    >
                      <option value="knowledge">Connaissances</option>
                      <option value="skills">Compétences</option>
                      <option value="attitudes">Attitudes</option>
                    </select>
                  </div>
                </div>
              </div>
              
              <div className="flex gap-3 mt-6">
                <button
                  type="button"
                  onClick={() => setShowCreateModal(false)}
                  className="flex-1 px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50"
                >
                  Annuler
                </button>
                <button
                  type="submit"
                  className="flex-1 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
                >
                  Créer
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Modal de création d'évaluation */}
      {showAssessmentModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 w-full max-w-md">
            <h2 className="text-xl font-bold mb-4">Nouvelle évaluation</h2>
            <form onSubmit={(e) => { e.preventDefault(); createAssessment(); }}>
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Titre</label>
                  <input
                    type="text"
                    value={assessmentForm.title}
                    onChange={(e) => setAssessmentForm({...assessmentForm, title: e.target.value})}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    required
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Description</label>
                  <textarea
                    value={assessmentForm.description}
                    onChange={(e) => setAssessmentForm({...assessmentForm, description: e.target.value})}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    rows={3}
                  />
                </div>
                
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Type</label>
                    <select
                      value={assessmentForm.assessment_type}
                      onChange={(e) => setAssessmentForm({...assessmentForm, assessment_type: e.target.value})}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    >
                      <option value="quiz">Quiz</option>
                      <option value="project">Projet</option>
                      <option value="presentation">Présentation</option>
                      <option value="observation">Observation</option>
                    </select>
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Matière</label>
                    <input
                      type="text"
                      value={assessmentForm.subject}
                      onChange={(e) => setAssessmentForm({...assessmentForm, subject: e.target.value})}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                      required
                    />
                  </div>
                </div>
                
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Poids</label>
                    <input
                      type="number"
                      step="0.1"
                      min="0"
                      value={assessmentForm.weight}
                      onChange={(e) => setAssessmentForm({...assessmentForm, weight: parseFloat(e.target.value)})}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Date limite</label>
                    <input
                      type="datetime-local"
                      value={assessmentForm.due_date}
                      onChange={(e) => setAssessmentForm({...assessmentForm, due_date: e.target.value})}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                  </div>
                </div>
              </div>
              
              <div className="flex gap-3 mt-6">
                <button
                  type="button"
                  onClick={() => setShowAssessmentModal(false)}
                  className="flex-1 px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50"
                >
                  Annuler
                </button>
                <button
                  type="submit"
                  className="flex-1 px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700"
                >
                  Créer
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
} 