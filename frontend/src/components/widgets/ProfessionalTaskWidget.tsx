'use client';

import React, { useState, useEffect } from 'react';
import { 
  FileText, 
  BookOpen, 
  Clock, 
  Calendar, 
  Eye, 
  Upload, 
  CheckSquare,
  AlertCircle,
  Target,
  TrendingUp
} from 'lucide-react';

interface Homework {
  id: number;
  title: string;
  description: string;
  subject: string;
  dueDate: string;
  priority: string;
  status: string;
  estimatedTime: number;
  attachments: string[];
  instructions: string;
  attachment?: {
    name: string;
    size: number;
    url: string;
    type: string;
    filename?: string;
  } | null;
  submission?: {
    id: number;
    submitted_file: string;
    submitted_at: string;
    status: string;
    grade?: number;
    feedback?: string;
  } | null;
}

interface ProfessionalTaskWidgetProps {
  homeworks: Homework[];
  onHomeworkUpdate?: (updatedHomework: Homework) => void;
  className?: string;
}

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export default function ProfessionalTaskWidget({ 
  homeworks, 
  onHomeworkUpdate, 
  className = '' 
}: ProfessionalTaskWidgetProps) {
  const [filteredHomeworks, setFilteredHomeworks] = useState<Homework[]>(homeworks);
  const [filter, setFilter] = useState<'all' | 'pending' | 'in_progress' | 'completed'>('all');
  const [sortBy, setSortBy] = useState<'priority' | 'dueDate' | 'title'>('priority');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [showDetails, setShowDetails] = useState(false);
  const [selectedHomework, setSelectedHomework] = useState<Homework | null>(null);

  useEffect(() => {
    let filtered = homeworks;
    
    // Filtrage
    if (filter !== 'all') {
      filtered = homeworks.filter(hw => {
        if (filter === 'pending') return !hw.submission;
        if (filter === 'completed') return hw.status === 'completed';
        if (filter === 'in_progress') return hw.submission && hw.status !== 'completed';
        return true;
      });
    }
    
    // Tri
    filtered.sort((a, b) => {
      switch (sortBy) {
        case 'priority':
          const priorityOrder = { high: 3, medium: 2, low: 1 };
          return (priorityOrder[b.priority as keyof typeof priorityOrder] || 0) - (priorityOrder[a.priority as keyof typeof priorityOrder] || 0);
        case 'dueDate':
          return new Date(a.dueDate).getTime() - new Date(b.dueDate).getTime();
        case 'title':
          return a.title.localeCompare(b.title);
        default:
          return 0;
      }
    });
    
    setFilteredHomeworks(filtered);
  }, [homeworks, filter, sortBy]);

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'high': return 'bg-gradient-to-r from-rose-500 to-pink-500 text-white';
      case 'medium': return 'bg-gradient-to-r from-amber-500 to-orange-500 text-white';
      case 'low': return 'bg-gradient-to-r from-emerald-500 to-teal-500 text-white';
      default: return 'bg-gradient-to-r from-slate-500 to-gray-500 text-white';
    }
  };

  const getPriorityLabel = (priority: string) => {
    switch (priority) {
      case 'high': return 'Élevée';
      case 'medium': return 'Moyenne';
      case 'low': return 'Faible';
      default: return 'Standard';
    }
  };

  const getStatusColor = (hasSubmission: boolean) => {
    return hasSubmission 
      ? 'bg-gradient-to-r from-blue-500 to-indigo-500 text-white'
      : 'bg-gradient-to-r from-slate-500 to-gray-500 text-white';
  };

  const getStatusLabel = (hasSubmission: boolean) => {
    return hasSubmission ? 'Soumis' : 'À faire';
  };

  const handleSubmitAssignment = async (homeworkId: number, file: File) => {
    try {
      const token = localStorage.getItem('najah_token');
      const user = localStorage.getItem('najah_user');
      if (!token || !user) return;

      const userData = JSON.parse(user);
      
      const formData = new FormData();
      formData.append('submission_file', file);
      
      const response = await fetch(`${API_BASE_URL}/api/v1/assignments/student/${userData.id}/submit/${homeworkId}`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`
        },
        body: formData
      });

      if (response.ok) {
        const result = await response.json();
        console.log('✅ Tâche soumise avec succès:', result);
        
        // Mettre à jour l'état local
        const updatedHomework = homeworks.find(hw => hw.id === homeworkId);
        if (updatedHomework && onHomeworkUpdate) {
          onHomeworkUpdate({
            ...updatedHomework,
            status: 'submitted',
            submission: {
              id: result.submission_id,
              submitted_file: file.name,
              submitted_at: result.submitted_at,
              status: result.status
            }
          });
        }
        
        alert('Tâche soumise avec succès !');
      } else {
        const error = await response.json();
        console.error('❌ Erreur lors de la soumission:', error);
        alert(`Erreur lors de la soumission: ${error.detail}`);
      }
    } catch (error) {
      console.error('❌ Erreur lors de la soumission:', error);
      alert('Erreur lors de la soumission de la tâche');
    }
  };

  const viewAssignment = (homework: Homework) => {
    if (homework.attachment && homework.attachment.url) {
      const urlParts = homework.attachment.url.split('/');
      const serverFilename = urlParts[urlParts.length - 1];
      const fileUrl = `${API_BASE_URL}/api/v1/uploads/assignments/${serverFilename}`;
      window.open(fileUrl, '_blank');
    } else {
      alert('Aucun fichier attaché à cette tâche');
    }
  };

  return (
    <div className={`bg-gradient-to-br from-white via-gray-50 to-blue-50 rounded-3xl shadow-2xl border border-gray-100 p-8 ${className}`}>
      {/* Header professionnel moderne */}
      <div className="flex items-center justify-between mb-8">
        <div className="flex items-center gap-5">
          <div className="w-16 h-16 bg-gradient-to-br from-blue-600 to-indigo-700 rounded-2xl flex items-center justify-center shadow-xl">
            <Target className="w-8 h-8 text-white" />
          </div>
          <div>
            <h2 className="text-3xl font-bold text-gray-900 mb-2">Gestion des Tâches</h2>
            <p className="text-gray-600 text-lg">Suivi et organisation de vos missions</p>
          </div>
        </div>
        <div className="flex items-center gap-4">
          <select
            value={sortBy}
            onChange={(e) => setSortBy(e.target.value as 'priority' | 'dueDate' | 'title')}
            className="px-6 py-3 border border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 bg-white shadow-lg font-medium"
          >
            <option value="priority">Par priorité</option>
            <option value="dueDate">Par date</option>
            <option value="title">Par titre</option>
          </select>
        </div>
      </div>

      {/* Filtres professionnels */}
      <div className="flex gap-4 mb-8">
        <button
          onClick={() => setFilter('all')}
          className={`px-8 py-4 rounded-2xl text-sm font-bold transition-all duration-300 ${
            filter === 'all' 
              ? 'bg-gradient-to-r from-blue-500 to-indigo-600 text-white shadow-xl transform scale-105' 
              : 'bg-white text-gray-600 hover:bg-gray-50 border border-gray-200 shadow-lg hover:shadow-xl hover:scale-105'
          }`}
        >
          Toutes
        </button>
        <button
          onClick={() => setFilter('pending')}
          className={`px-8 py-4 rounded-2xl text-sm font-bold transition-all duration-300 ${
            filter === 'pending' 
              ? 'bg-gradient-to-r from-amber-500 to-orange-600 text-white shadow-xl transform scale-105' 
              : 'bg-white text-gray-600 hover:bg-gray-50 border border-gray-200 shadow-lg hover:shadow-xl hover:scale-105'
          }`}
        >
          À faire
        </button>
        <button
          onClick={() => setFilter('in_progress')}
          className={`px-8 py-4 rounded-2xl text-sm font-bold transition-all duration-300 ${
            filter === 'in_progress' 
              ? 'bg-gradient-to-r from-blue-500 to-indigo-600 text-white shadow-xl transform scale-105' 
              : 'bg-white text-gray-600 hover:bg-gray-50 border border-gray-200 shadow-lg hover:shadow-xl hover:scale-105'
          }`}
        >
          En cours
        </button>
        <button
          onClick={() => setFilter('completed')}
          className={`px-8 py-4 rounded-2xl text-sm font-bold transition-all duration-300 ${
            filter === 'completed' 
              ? 'bg-gradient-to-r from-emerald-500 to-teal-600 text-white shadow-xl transform scale-105' 
              : 'bg-white text-gray-600 hover:bg-gray-50 border border-gray-200 shadow-lg hover:shadow-xl hover:scale-105'
          }`}
        >
          Terminées
        </button>
      </div>

      {error && (
        <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-2xl text-red-700 text-sm">
          {error}
        </div>
      )}

      <div className="space-y-6">
        {loading ? (
          <div className="text-center py-16">
            <div className="w-16 h-16 border-4 border-blue-500 border-t-transparent rounded-full animate-spin mx-auto mb-6"></div>
            <p className="text-xl font-semibold text-gray-700 mb-3">Chargement des tâches...</p>
            <p className="text-gray-500">Veuillez patienter</p>
          </div>
        ) : filteredHomeworks.length === 0 ? (
          <div className="text-center py-20 text-gray-500">
            <div className="w-20 h-20 bg-gradient-to-br from-gray-100 to-gray-200 rounded-full flex items-center justify-center mx-auto mb-6">
              <Target className="w-10 h-10 text-gray-400" />
            </div>
            <p className="text-2xl font-semibold text-gray-600 mb-3">Aucune tâche {filter === 'pending' ? 'à faire' : filter === 'in_progress' ? 'en cours' : filter === 'completed' ? 'terminée' : 'assignée'}</p>
            <p className="text-gray-500">Vos professeurs vous assigneront des tâches bientôt</p>
          </div>
        ) : (
          filteredHomeworks.map((homework) => (
            <div
              key={homework.id}
              className="bg-white rounded-2xl shadow-lg border border-gray-100 p-8 hover:shadow-2xl transition-all duration-500 transform hover:scale-[1.02]"
            >
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  {/* En-tête de la tâche */}
                  <div className="flex items-center gap-4 mb-4">
                    <h3 className="text-2xl font-bold text-gray-900">{homework.title}</h3>
                    <span className={`px-4 py-2 rounded-full text-xs font-bold ${getPriorityColor(homework.priority)}`}>
                      {getPriorityLabel(homework.priority)}
                    </span>
                    <span className={`px-4 py-2 rounded-full text-xs font-bold ${getStatusColor(!!homework.submission)}`}>
                      {getStatusLabel(!!homework.submission)}
                    </span>
                  </div>
                  
                  {/* Métadonnées */}
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
                    <div className="flex items-center gap-3 p-4 bg-gray-50 rounded-xl border border-gray-200">
                      <BookOpen className="w-5 h-5 text-blue-600" />
                      <span className="text-sm font-medium text-gray-700">{homework.subject}</span>
                    </div>
                    <div className="flex items-center gap-3 p-4 bg-gray-50 rounded-xl border border-gray-200">
                      <Clock className="w-5 h-5 text-blue-600" />
                      <span className="text-sm font-medium text-gray-700">{homework.estimatedTime} min</span>
                    </div>
                    <div className="flex items-center gap-3 p-4 bg-gray-50 rounded-xl border border-gray-200">
                      <Calendar className="w-5 h-5 text-blue-600" />
                      <span className="text-sm font-medium text-gray-700">{new Date(homework.dueDate).toLocaleDateString('fr-FR')}</span>
                    </div>
                  </div>

                  {/* Description */}
                  {homework.description && (
                    <div className="mb-6">
                      <h4 className="text-lg font-semibold text-gray-800 mb-3 flex items-center gap-2">
                        <div className="w-6 h-6 bg-blue-100 rounded-lg flex items-center justify-center">
                          <BookOpen className="w-3 h-3 text-blue-600" />
                        </div>
                        Description
                      </h4>
                      <p className="text-gray-700 leading-relaxed">{homework.description}</p>
                    </div>
                  )}

                  {/* Instructions */}
                  {homework.instructions && (
                    <div className="mb-6 p-6 bg-gradient-to-r from-blue-50 to-indigo-50 rounded-2xl border border-blue-200">
                      <h4 className="text-lg font-semibold text-gray-800 mb-3 flex items-center gap-2">
                        <div className="w-6 h-6 bg-blue-100 rounded-lg flex items-center justify-center">
                          <CheckSquare className="w-3 h-3 text-blue-600" />
                        </div>
                        Instructions
                      </h4>
                      <p className="text-gray-700 leading-relaxed">{homework.instructions}</p>
                    </div>
                  )}

                  {/* Pièces jointes */}
                  {homework.attachments && homework.attachments.length > 0 && (
                    <div className="mb-6">
                      <h4 className="text-lg font-semibold text-gray-800 mb-3 flex items-center gap-2">
                        <div className="w-6 h-6 bg-purple-100 rounded-lg flex items-center justify-center">
                          <FileText className="w-3 h-3 text-purple-600" />
                        </div>
                        Pièces jointes
                      </h4>
                      <div className="flex flex-wrap gap-3">
                        {homework.attachments.map((attachment, index) => (
                          <div key={index} className="flex items-center gap-2 px-4 py-2 bg-white rounded-xl border border-gray-200 shadow-sm">
                            <FileText className="w-4 h-4 text-gray-500" />
                            <span className="text-sm font-medium text-gray-700">{attachment}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </div>

                {/* Actions */}
                <div className="flex flex-col gap-4 ml-8">
                  {/* Debug info */}
                  <div className="text-center p-3 bg-gray-100 rounded-xl border border-gray-200">
                    <p className="text-xs text-gray-600 font-medium">
                      Debug: attachment={homework.attachment ? 'Oui' : 'Non'}
                    </p>
                  </div>
                  
                  {/* Bouton Visualiser */}
                  <button
                    onClick={() => viewAssignment(homework)}
                    className="flex items-center justify-center gap-3 px-6 py-3 bg-gradient-to-r from-emerald-500 to-teal-600 text-white rounded-xl font-semibold shadow-lg hover:shadow-xl transition-all duration-300 transform hover:scale-105"
                    title="Visualiser la tâche"
                  >
                    <Eye className="w-5 h-5" />
                    Visualiser
                  </button>

                  {/* Bouton Détails */}
                  <button
                    onClick={() => {
                      setSelectedHomework(homework);
                      setShowDetails(true);
                    }}
                    className="flex items-center justify-center gap-3 px-6 py-3 bg-gradient-to-r from-blue-500 to-indigo-600 text-white rounded-xl font-semibold shadow-lg hover:shadow-xl transition-all duration-300 transform hover:scale-105"
                  >
                    <Eye className="w-5 h-5" />
                    Détails
                  </button>

                  {/* Bouton Soumettre */}
                  {!homework.submission && (
                    <button
                      onClick={() => {
                        const input = document.createElement('input');
                        input.type = 'file';
                        input.accept = '.pdf,.doc,.docx,.txt';
                        input.onchange = (e) => {
                          const file = (e.target as HTMLInputElement).files?.[0];
                          if (file) {
                            handleSubmitAssignment(homework.id, file);
                          }
                        };
                        input.click();
                      }}
                      className="flex items-center justify-center gap-3 px-6 py-3 bg-gradient-to-r from-purple-500 to-pink-600 text-white rounded-xl font-semibold shadow-lg hover:shadow-xl transition-all duration-300 transform hover:scale-105"
                      title="Soumettre la tâche"
                    >
                      <Upload className="w-5 h-5" />
                      Soumettre
                    </button>
                  )}

                  {/* Statut de soumission */}
                  {homework.submission && (
                    <div className="text-center p-4 bg-gradient-to-r from-emerald-50 to-teal-50 border border-emerald-200 rounded-xl">
                      <p className="text-sm font-bold text-emerald-700 mb-1">Soumis</p>
                      <p className="text-xs text-emerald-600">
                        {new Date(homework.submission.submitted_at).toLocaleDateString('fr-FR')}
                      </p>
                    </div>
                  )}
                </div>
              </div>
            </div>
          ))
        )}
      </div>

      {/* Modal de détails professionnel */}
      {showDetails && selectedHomework && (
        <div className="fixed inset-0 bg-black bg-opacity-60 flex items-center justify-center z-50 backdrop-blur-sm">
          <div className="bg-white rounded-3xl shadow-2xl p-10 max-w-4xl w-full mx-6 max-h-[90vh] overflow-y-auto">
            <div className="flex items-center justify-between mb-8">
              <div className="flex items-center gap-4">
                <div className="w-12 h-12 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-2xl flex items-center justify-center shadow-lg">
                  <Target className="w-6 h-6 text-white" />
                </div>
                <h3 className="text-2xl font-bold text-gray-900">Détails de la Tâche</h3>
              </div>
              <button
                onClick={() => setShowDetails(false)}
                className="w-10 h-10 bg-gray-100 hover:bg-gray-200 rounded-xl flex items-center justify-center text-gray-600 transition-all duration-300 hover:scale-110"
              >
                ✕
              </button>
            </div>
            
            <div className="space-y-8">
              {/* En-tête de la tâche */}
              <div className="bg-gradient-to-r from-blue-50 to-indigo-50 p-8 rounded-2xl border border-blue-200">
                <h4 className="text-3xl font-bold text-gray-900 mb-4">{selectedHomework.title}</h4>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <div className="flex items-center gap-3 p-4 bg-white rounded-xl border border-blue-200 shadow-sm">
                    <BookOpen className="w-6 h-6 text-blue-600" />
                    <span className="text-base font-semibold text-gray-700">{selectedHomework.subject}</span>
                  </div>
                  <div className="flex items-center gap-3 p-4 bg-white rounded-xl border border-blue-200 shadow-sm">
                    <Clock className="w-6 h-6 text-blue-600" />
                    <span className="text-base font-semibold text-gray-700">{selectedHomework.estimatedTime} min</span>
                  </div>
                  <div className="flex items-center gap-3 p-4 bg-white rounded-xl border border-blue-200 shadow-sm">
                    <Calendar className="w-6 h-6 text-blue-600" />
                    <span className="text-base font-semibold text-gray-700">{new Date(selectedHomework.dueDate).toLocaleDateString('fr-FR')}</span>
                  </div>
                </div>
              </div>
              
              {selectedHomework.description && (
                <div className="bg-white p-8 rounded-2xl border border-gray-200 shadow-sm">
                  <h5 className="text-xl font-bold text-gray-800 mb-4 flex items-center gap-3">
                    <div className="w-8 h-8 bg-blue-100 rounded-xl flex items-center justify-center">
                      <BookOpen className="w-4 h-4 text-blue-600" />
                    </div>
                    Description
                  </h5>
                  <p className="text-gray-700 leading-relaxed text-lg">{selectedHomework.description}</p>
                </div>
              )}
              
              {selectedHomework.instructions && (
                <div className="bg-white p-8 rounded-2xl border border-gray-200 shadow-sm">
                  <h5 className="text-xl font-bold text-gray-800 mb-4 flex items-center gap-3">
                    <div className="w-8 h-8 bg-green-100 rounded-xl flex items-center justify-center">
                      <CheckSquare className="w-4 h-4 text-green-600" />
                    </div>
                    Instructions
                  </h5>
                  <p className="text-gray-700 leading-relaxed text-lg">{selectedHomework.instructions}</p>
                </div>
              )}
              
              {selectedHomework.attachments && selectedHomework.attachments.length > 0 && (
                <div className="bg-white p-8 rounded-2xl border border-gray-200 shadow-sm">
                  <h5 className="text-xl font-bold text-gray-800 mb-4 flex items-center gap-3">
                    <div className="w-8 h-8 bg-purple-100 rounded-xl flex items-center justify-center">
                      <FileText className="w-4 h-4 text-purple-600" />
                    </div>
                    Pièces jointes
                  </h5>
                  <div className="space-y-3">
                    {selectedHomework.attachments.map((attachment, index) => (
                      <div key={index} className="flex items-center gap-3 p-4 bg-gray-50 rounded-xl border border-gray-200">
                        <FileText className="w-5 h-5 text-gray-500" />
                        <span className="text-base font-medium text-gray-700">{attachment}</span>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
            
            <div className="mt-10 flex justify-end">
              <button
                onClick={() => setShowDetails(false)}
                className="px-8 py-4 bg-gradient-to-r from-blue-500 to-indigo-600 hover:from-blue-600 hover:to-indigo-700 text-white rounded-2xl font-bold shadow-lg hover:shadow-xl transition-all duration-300 transform hover:scale-105"
              >
                Fermer
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

