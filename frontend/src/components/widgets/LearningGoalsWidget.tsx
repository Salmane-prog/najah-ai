'use client';

import React, { useState, useEffect } from 'react';
import { useAuth  } from '../../hooks/useAuth';
import { Target, Plus, Edit, Trash2, Calendar, CheckCircle } from 'lucide-react';

interface LearningGoal {
  id: number;
  title: string;
  description: string;
  subject: string;
  target_date: string | null;
  progress: number;
  status: string;
  created_at: string;
}

interface LearningGoalsWidgetProps {
  className?: string;
}

export default function LearningGoalsWidget({ className }: LearningGoalsWidgetProps) {
  const { user, token } = useAuth();
  const [goals, setGoals] = useState<LearningGoal[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [editingGoal, setEditingGoal] = useState<LearningGoal | null>(null);
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    subject: '',
    target_date: ''
  });

  useEffect(() => {
    if (token) {
      fetchLearningGoals();
    }
  }, [token]);

  const fetchLearningGoals = async () => {
    try {
      setLoading(true);
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/v1/learning-goals`, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });

      if (response.ok) {
        const data = await response.json();
        setGoals(data);
      } else {
        console.error('Erreur lors du chargement des objectifs:', response.status);
        setError('Erreur lors du chargement des objectifs');
      }
    } catch (error) {
      console.error('Erreur lors du chargement des objectifs:', error);
      setError('Erreur de connexion');
    } finally {
      setLoading(false);
    }
  };

  const createGoal = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/v1/learning-goals`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
      });

      if (response.ok) {
        await fetchLearningGoals();
        setShowCreateModal(false);
        setFormData({ title: '', description: '', subject: '', target_date: '' });
      } else {
        console.error('Erreur lors de la création de l\'objectif');
      }
    } catch (error) {
      console.error('Erreur lors de la création de l\'objectif:', error);
    }
  };

  const updateGoal = async (goalId: number, updatedData: Partial<LearningGoal>) => {
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/v1/learning-goals/${goalId}/update`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(updatedData)
      });

      if (response.ok) {
        await fetchLearningGoals();
        setEditingGoal(null);
      } else {
        console.error('Erreur lors de la mise à jour de l\'objectif');
      }
    } catch (error) {
      console.error('Erreur lors de la mise à jour de l\'objectif:', error);
    }
  };

  const deleteGoal = async (goalId: number) => {
    if (!confirm('Êtes-vous sûr de vouloir supprimer cet objectif ?')) return;

    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/v1/learning-goals/${goalId}/delete`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });

      if (response.ok) {
        await fetchLearningGoals();
      } else {
        console.error('Erreur lors de la suppression de l\'objectif');
      }
    } catch (error) {
      console.error('Erreur lors de la suppression de l\'objectif:', error);
    }
  };

  const formatDate = (dateString: string | null) => {
    if (!dateString) return 'Aucune date';
    return new Date(dateString).toLocaleDateString('fr-FR');
  };

  const getProgressColor = (progress: number) => {
    if (progress >= 80) return 'text-green-600';
    if (progress >= 50) return 'text-yellow-600';
    return 'text-red-600';
  };

  if (loading) {
    return (
      <div className={`bg-white rounded-lg shadow-sm p-6 ${className}`}>
        <div className="animate-pulse">
          <div className="h-6 bg-gray-200 rounded mb-4"></div>
          <div className="space-y-3">
            <div className="h-4 bg-gray-200 rounded"></div>
            <div className="h-4 bg-gray-200 rounded"></div>
            <div className="h-4 bg-gray-200 rounded"></div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className={`bg-white rounded-lg shadow-sm p-6 ${className}`}>
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-xl font-bold text-gray-800">Mes Objectifs d'Apprentissage</h2>
        <button
          onClick={() => setShowCreateModal(true)}
          className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition"
        >
          <Plus size={16} />
          Nouvel Objectif
        </button>
      </div>

      {error && (
        <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg">
          <p className="text-red-600 text-sm">{error}</p>
        </div>
      )}

      {goals.length === 0 ? (
        <div className="text-center py-8">
          <Target className="mx-auto text-gray-400 mb-4" size={48} />
          <p className="text-gray-600 mb-2">Aucun objectif défini</p>
          <p className="text-sm text-gray-500">Commencez par créer votre premier objectif d'apprentissage</p>
        </div>
      ) : (
        <div className="space-y-4 max-h-96 overflow-y-auto">
          {goals.map((goal) => (
            <div key={goal.id} className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition">
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <div className="flex items-center gap-2 mb-2">
                    <h3 className="font-semibold text-gray-800">{goal.title}</h3>
                    <span className={`px-2 py-1 text-xs rounded-full ${
                      goal.status === 'active' ? 'bg-green-100 text-green-800' :
                      goal.status === 'completed' ? 'bg-blue-100 text-blue-800' :
                      'bg-gray-100 text-gray-800'
                    }`}>
                      {goal.status === 'active' ? 'En cours' :
                       goal.status === 'completed' ? 'Terminé' : 'Abandonné'}
                    </span>
                  </div>
                  
                  {goal.description && (
                    <p className="text-gray-600 text-sm mb-2">{goal.description}</p>
                  )}
                  
                  <div className="flex items-center gap-4 text-sm text-gray-500">
                    {goal.subject && (
                      <span className="flex items-center gap-1">
                        <Target size={14} />
                        {goal.subject}
                      </span>
                    )}
                    {goal.target_date && (
                      <span className="flex items-center gap-1">
                        <Calendar size={14} />
                        {formatDate(goal.target_date)}
                      </span>
                    )}
                  </div>
                  
                  <div className="mt-3">
                    <div className="flex items-center justify-between mb-1">
                      <span className="text-sm text-gray-600">Progression</span>
                      <span className={`text-sm font-medium ${getProgressColor(goal.progress)}`}>
                        {Math.round(goal.progress * 100)}%
                      </span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-2">
                      <div
                        className={`h-2 rounded-full transition-all ${
                          goal.progress >= 80 ? 'bg-green-500' :
                          goal.progress >= 50 ? 'bg-yellow-500' : 'bg-red-500'
                        }`}
                        style={{ width: `${goal.progress * 100}%` }}
                      ></div>
                    </div>
                  </div>
                </div>
                
                <div className="flex items-center gap-2 ml-4">
                  <button
                    onClick={() => setEditingGoal(goal)}
                    className="p-2 text-gray-400 hover:text-blue-600 hover:bg-blue-50 rounded-lg transition"
                  >
                    <Edit size={16} />
                  </button>
                  <button
                    onClick={() => deleteGoal(goal.id)}
                    className="p-2 text-gray-400 hover:text-red-600 hover:bg-red-50 rounded-lg transition"
                  >
                    <Trash2 size={16} />
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Modal de création */}
      {showCreateModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-30">
          <div className="bg-white rounded-xl shadow-2xl p-6 max-w-md w-full">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-xl font-bold text-gray-800">Nouvel Objectif</h3>
              <button
                onClick={() => setShowCreateModal(false)}
                className="text-gray-400 hover:text-gray-600"
              >
                ✕
              </button>
            </div>
            
            <form onSubmit={createGoal} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Titre de l'objectif
                </label>
                <input
                  type="text"
                  value={formData.title}
                  onChange={(e) => setFormData({...formData, title: e.target.value})}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  required
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Description
                </label>
                <textarea
                  value={formData.description}
                  onChange={(e) => setFormData({...formData, description: e.target.value})}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  rows={3}
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Matière
                </label>
                <input
                  type="text"
                  value={formData.subject}
                  onChange={(e) => setFormData({...formData, subject: e.target.value})}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Date cible
                </label>
                <input
                  type="date"
                  value={formData.target_date}
                  onChange={(e) => setFormData({...formData, target_date: e.target.value})}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
              
              <div className="flex gap-3 pt-4">
                <button
                  type="button"
                  onClick={() => setShowCreateModal(false)}
                  className="flex-1 px-4 py-2 text-gray-600 border border-gray-300 rounded-lg hover:bg-gray-50"
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

      {/* Modal d'édition */}
      {editingGoal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-30">
          <div className="bg-white rounded-xl shadow-2xl p-6 max-w-md w-full">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-xl font-bold text-gray-800">Modifier l'Objectif</h3>
              <button
                onClick={() => setEditingGoal(null)}
                className="text-gray-400 hover:text-gray-600"
              >
                ✕
              </button>
            </div>
            
            <form onSubmit={(e) => {
              e.preventDefault();
              updateGoal(editingGoal.id, formData);
            }} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Titre de l'objectif
                </label>
                <input
                  type="text"
                  value={formData.title}
                  onChange={(e) => setFormData({...formData, title: e.target.value})}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  required
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Description
                </label>
                <textarea
                  value={formData.description}
                  onChange={(e) => setFormData({...formData, description: e.target.value})}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  rows={3}
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Matière
                </label>
                <input
                  type="text"
                  value={formData.subject}
                  onChange={(e) => setFormData({...formData, subject: e.target.value})}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Date cible
                </label>
                <input
                  type="date"
                  value={formData.target_date}
                  onChange={(e) => setFormData({...formData, target_date: e.target.value})}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
              
              <div className="flex gap-3 pt-4">
                <button
                  type="button"
                  onClick={() => setEditingGoal(null)}
                  className="flex-1 px-4 py-2 text-gray-600 border border-gray-300 rounded-lg hover:bg-gray-50"
                >
                  Annuler
                </button>
                <button
                  type="submit"
                  className="flex-1 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
                >
                  Modifier
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
