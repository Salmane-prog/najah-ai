'use client';

import React, { useState, useEffect } from 'react';
import { BookOpen, Clock, Target, CheckCircle, Eye, Calendar, Star, AlertCircle, FileText, Upload } from 'lucide-react';

interface Homework {
  id: number;
  title: string;
  subject: string;
  description: string;
  assignedAt: string;
  dueDate: string;
  priority: 'low' | 'medium' | 'high';
  status: 'pending' | 'in_progress' | 'completed' | 'overdue';
  estimatedTime: number;
  attachments?: string[];
  instructions?: string;
  submissionType?: 'file' | 'text' | 'link';
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

interface EnhancedHomeworkWidgetProps {
  className?: string;
}

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export default function EnhancedHomeworkWidget({ className = '' }: EnhancedHomeworkWidgetProps) {
  const [homeworks, setHomeworks] = useState<Homework[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedHomework, setSelectedHomework] = useState<Homework | null>(null);
  const [showDetails, setShowDetails] = useState(false);
  const [filter, setFilter] = useState<'all' | 'pending' | 'in_progress' | 'completed'>('all');
  const [sortBy, setSortBy] = useState<'dueDate' | 'priority' | 'subject'>('dueDate');

  useEffect(() => {
    loadHomeworks();
  }, []);

  const loadHomeworks = async () => {
    try {
      setLoading(true);
      const token = localStorage.getItem('najah_token');
      const user = localStorage.getItem('najah_user');
      
      if (!token || !user) return;
      
      const userData = JSON.parse(user);
      
      // Charger les devoirs assignés depuis le nouveau endpoint
      const response = await fetch(`${API_BASE_URL}/api/v1/assignments/student/${userData.id}/assigned`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (response.ok) {
        const assignments = await response.json();
        // Convertir les assignations en format Homework
        const homeworkList = assignments.map((assignment: any) => ({
          id: assignment.id,
          title: assignment.title,
          description: assignment.description,
          subject: assignment.subject,
          dueDate: assignment.due_date,
          priority: assignment.priority,
          status: assignment.status || 'pending',
          estimatedTime: assignment.estimated_time || 60,
          assignedAt: assignment.created_at || new Date().toISOString(),
          attachments: assignment.attachment ? [assignment.attachment.name] : [],
          instructions: assignment.description, // Utiliser la description comme instructions
          attachment: assignment.attachment, // Inclure les informations sur le fichier
          submission: assignment.submission || null // Inclure les informations sur la soumission
        }));
        setHomeworks(homeworkList);
      }
    } catch (error) {
      console.error('Erreur lors du chargement des devoirs:', error);
      setError('Erreur lors du chargement des devoirs');
    } finally {
      setLoading(false);
    }
  };



  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'high': return 'bg-rose-100 text-rose-800 border-rose-200';
      case 'medium': return 'bg-amber-100 text-amber-800 border-amber-200';
      case 'low': return 'bg-emerald-100 text-emerald-800 border-emerald-200';
      default: return 'bg-slate-100 text-slate-800 border-slate-200';
    }
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
        console.log('✅ Devoir soumis avec succès:', result);
        
        // Mettre à jour l'état local
        setHomeworks(prev => prev.map(hw => 
          hw.id === homeworkId ? { 
            ...hw, 
            status: 'submitted',
            submission: {
              id: result.submission_id,
              submitted_file: file.name,
              submitted_at: result.submitted_at,
              status: result.status
            }
          } : hw
        ));
        
        alert('Devoir soumis avec succès !');
      } else {
        const error = await response.json();
        console.error('❌ Erreur lors de la soumission:', error);
        alert(`Erreur lors de la soumission: ${error.detail}`);
      }
    } catch (error) {
      console.error('❌ Erreur lors de la soumission:', error);
      alert('Erreur lors de la soumission du devoir');
    }
  };

  const viewAssignment = (homework: Homework) => {
    console.log('🔍 Tentative de visualisation du devoir:', homework);
    console.log('📎 Attachment:', homework.attachment);
    
    if (homework.attachment && homework.attachment.url) {
      // Extraire le nom du fichier depuis l'URL
      const urlParts = homework.attachment.url.split('/');
      const serverFilename = urlParts[urlParts.length - 1];
      const fileUrl = `${API_BASE_URL}/api/v1/uploads/assignments/${serverFilename}`;
      
      console.log('🔗 URL du fichier:', fileUrl);
      console.log('📄 Nom du fichier sur le serveur:', serverFilename);
      window.open(fileUrl, '_blank');
    } else {
      console.log('❌ Pas de fichier attaché ou URL manquante');
      console.log('📋 Détails du devoir:', {
        id: homework.id,
        title: homework.title,
        hasAttachment: !!homework.attachment,
        attachmentData: homework.attachment
      });
      alert('Aucun fichier attaché à ce devoir');
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed': return 'bg-emerald-100 text-emerald-800';
      case 'in_progress': return 'bg-amber-100 text-amber-800';
      case 'overdue': return 'bg-slate-100 text-slate-800';
      case 'pending': return 'bg-slate-100 text-slate-800';
      default: return 'bg-slate-100 text-slate-800';
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'completed': return <CheckCircle className="w-4 h-4" />;
      case 'in_progress': return <Clock className="w-4 h-4" />;
      case 'overdue': return <AlertCircle className="w-4 h-4" />;
      case 'pending': return <Target className="w-4 h-4" />;
      default: return <Target className="w-4 h-4" />;
    }
  };

  const isOverdue = (dueDate: string) => {
    return new Date(dueDate) < new Date();
  };

  const getDaysUntilDue = (dueDate: string) => {
    const due = new Date(dueDate);
    const now = new Date();
    const diffTime = due.getTime() - now.getTime();
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    return diffDays;
  };

  const filteredAndSortedHomeworks = (homeworks || [])
    .filter(homework => {
      if (filter === 'all') return true;
      return homework.status === filter;
    })
    .sort((a, b) => {
      switch (sortBy) {
        case 'dueDate':
          return new Date(a.dueDate).getTime() - new Date(b.dueDate).getTime();
        case 'priority':
          const priorityOrder = { high: 3, medium: 2, low: 1 };
          return priorityOrder[b.priority] - priorityOrder[a.priority];
        case 'subject':
          return a.subject.localeCompare(b.subject);
        default:
          return 0;
      }
    });

  return (
          <div className={`enhanced-homework-widget bg-white rounded-xl shadow-lg p-6 ${className}`}>
              <div className="flex items-center justify-between mb-6">
          <h2 className="text-xl font-bold text-gray-800 flex items-center gap-2">
            <div className="w-8 h-8 bg-blue-100 rounded-lg flex items-center justify-center">
              <FileText className="w-5 h-5 text-blue-600" />
            </div>
            Gestion des Tâches
          </h2>
        <div className="flex gap-2">
          <select
            value={sortBy}
            onChange={(e) => setSortBy(e.target.value as any)}
            className="px-3 py-1 rounded-lg text-sm border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="dueDate">Par date</option>
            <option value="priority">Par priorité</option>
            <option value="subject">Par matière</option>
          </select>
        </div>
      </div>

      {/* Filtres avec scroll horizontal si nécessaire */}
      <div className="flex gap-2 mb-4 overflow-x-auto pb-2">
        <button
          onClick={() => setFilter('all')}
          className={`px-4 py-2 rounded-lg text-sm font-medium transition-all ${
            filter === 'all' 
              ? 'bg-blue-600 text-white shadow-md' 
              : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
          }`}
        >
          Toutes
        </button>
        <button
          onClick={() => setFilter('pending')}
          className={`px-4 py-2 rounded-lg text-sm font-medium transition-all ${
            filter === 'pending' 
              ? 'bg-amber-600 text-white shadow-md' 
              : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
          }`}
        >
          À faire
        </button>
        <button
          onClick={() => setFilter('in_progress')}
          className={`px-4 py-2 rounded-lg text-sm font-medium transition-all ${
            filter === 'in_progress' 
              ? 'bg-blue-600 text-white shadow-md' 
              : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
          }`}
        >
          En cours
        </button>
        <button
          onClick={() => setFilter('completed')}
          className={`px-4 py-2 rounded-lg text-sm font-medium transition-all ${
            filter === 'completed' 
              ? 'bg-emerald-600 text-white shadow-md' 
              : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
          }`}
        >
          Terminées
        </button>
      </div>

      {error && (
        <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg text-red-700 text-sm">
          {error}
        </div>
      )}

      <div className="space-y-4 max-h-96 overflow-y-auto pr-2">
        {loading ? (
          <div className="text-center py-12">
            <div className="w-12 h-12 border-4 border-blue-500 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
            <p className="text-lg font-medium text-gray-600 mb-2">Chargement des tâches...</p>
            <p className="text-sm text-gray-500">Veuillez patienter</p>
          </div>
        ) : filteredAndSortedHomeworks.length === 0 ? (
          <div className="text-center py-12 text-gray-500">
            <div className="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <FileText className="w-8 h-8 text-gray-400" />
            </div>
            <p className="text-xl font-medium text-gray-600 mb-2">Aucune tâche {filter === 'pending' ? 'à faire' : filter === 'in_progress' ? 'en cours' : filter === 'completed' ? 'terminée' : 'assignée'}</p>
            <p className="text-sm text-gray-500">Vos professeurs vous assigneront des tâches bientôt</p>
          </div>
        ) : (
          filteredAndSortedHomeworks.map((homework) => {
            const overdue = isOverdue(homework.dueDate);
            const daysUntilDue = getDaysUntilDue(homework.dueDate);
            
            return (
              <div
                key={homework.id}
                className="bg-white rounded-2xl shadow-lg border border-gray-100 p-6 hover:shadow-xl transition-all duration-300"
              >
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <div className="flex items-center gap-3 mb-2">
                      <h3 className="font-semibold text-gray-800">{homework.title}</h3>
                      <span className={`px-2 py-1 rounded-full text-xs font-medium border ${getPriorityColor(homework.priority)}`}>
                        {homework.priority === 'high' ? 'Élevée' : homework.priority === 'medium' ? 'Moyenne' : 'Faible'}
                      </span>
                      <span className={`px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(homework.status)}`}>
                        {homework.submission ? 'Soumis' : 'À faire'}
                      </span>
                    </div>
                    
                    <div className="flex items-center gap-4 text-sm text-gray-600 mb-3">
                      <span className="flex items-center gap-1">
                        <BookOpen className="w-4 h-4" />
                        {homework.subject}
                      </span>
                      <span className="flex items-center gap-1">
                        <Clock className="w-4 h-4" />
                        {homework.estimatedTime} min
                      </span>
                      <span className="flex items-center gap-1">
                        <Calendar className="w-4 h-4" />
                        {new Date(homework.dueDate).toLocaleDateString('fr-FR')}
                      </span>
                    </div>

                    {homework.description && (
                      <p className="text-sm text-gray-600 mb-3 line-clamp-2">{homework.description}</p>
                    )}

                    {/* Indicateur de priorité professionnel */}
                    <div className="flex items-center gap-2 text-gray-600 text-sm mb-3">
                      <div className="flex items-center gap-1">
                        <span className="text-xs font-medium text-gray-500">Priorité:</span>
                        <span className={`px-2 py-1 rounded-full text-xs font-medium ${getPriorityColor(homework.priority)}`}>
                          {homework.priority === 'high' ? 'Élevée' : homework.priority === 'medium' ? 'Moyenne' : 'Faible'}
                        </span>
                      </div>
                    </div>

                    {/* Instructions */}
                    {homework.instructions && (
                      <div className="mb-3 p-3 bg-blue-50 rounded-lg">
                        <p className="text-sm font-medium text-blue-800 mb-1">Instructions:</p>
                        <p className="text-sm text-blue-700">{homework.instructions}</p>
                      </div>
                    )}

                    {/* Pièces jointes */}
                    {homework.attachments && homework.attachments.length > 0 && (
                      <div className="mb-3">
                        <p className="text-sm font-medium text-gray-700 mb-2">Pièces jointes:</p>
                        <div className="flex flex-wrap gap-2">
                          {homework.attachments.map((attachment, index) => (
                            <span
                              key={index}
                              className="px-2 py-1 bg-gray-100 text-gray-700 text-xs rounded-full flex items-center gap-1"
                            >
                              <FileText className="w-3 h-3" />
                              {attachment}
                            </span>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>

                  <div className="flex flex-col gap-2 ml-4">
                    {/* Debug info */}
                    <div className="text-xs text-gray-500 mb-2">
                      Debug: attachment={homework.attachment ? 'Oui' : 'Non'}
                    </div>
                    
                    {/* Bouton Visualiser le devoir - Toujours affiché pour test */}
                    <button
                      onClick={() => viewAssignment(homework)}
                      className="flex items-center gap-2 px-4 py-2 bg-green-600 text-white rounded-lg text-sm font-medium"
                      title="Visualiser le devoir"
                    >
                      <Eye className="w-4 h-4" />
                      Visualiser
                    </button>

                    {/* Bouton Détails */}
                    <button
                      onClick={() => {
                        setSelectedHomework(homework);
                        setShowDetails(true);
                      }}
                      className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg text-sm font-medium"
                    >
                      <Eye className="w-4 h-4" />
                      Détails
                    </button>

                    {/* Bouton Soumettre */}
                    {homework.status !== 'submitted' && homework.status !== 'completed' && (
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
                        className="flex items-center gap-2 px-4 py-2 bg-purple-600 text-white rounded-lg text-sm font-medium"
                        title="Soumettre le devoir"
                      >
                        <Upload className="w-4 h-4" />
                        Soumettre
                      </button>
                    )}

                                    {/* Statut automatique - affichage seulement */}
                <div className="text-center p-2 bg-gray-50 border border-gray-200 rounded-lg">
                  <p className="text-xs text-gray-700 font-medium">
                    {homework.submission ? 'Soumis' : 'À faire'}
                  </p>
                  {homework.submission && (
                    <p className="text-xs text-gray-600">
                      {new Date(homework.submission.submitted_at).toLocaleDateString('fr-FR')}
                    </p>
                  )}
                </div>

                    {/* Statut de soumission */}
                    {homework.submission && (
                      <div className="text-center p-2 bg-green-50 border border-green-200 rounded-lg">
                        <p className="text-xs text-green-700 font-medium">Soumis</p>
                        <p className="text-xs text-green-600">
                          {new Date(homework.submission.submitted_at).toLocaleDateString('fr-FR')}
                        </p>
                      </div>
                    )}
                  </div>
                </div>
              </div>
            );
          })
        )}
      </div>

      {/* Modal de détails professionnel */}
      {showDetails && selectedHomework && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-xl shadow-2xl p-8 max-w-3xl w-full mx-4 max-h-[85vh] overflow-y-auto">
            <div className="flex items-center justify-between mb-6">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center">
                  <BookOpen className="w-5 h-5 text-blue-600" />
                </div>
                <h3 className="text-xl font-semibold text-gray-900">Détails de la tâche</h3>
              </div>
              <button
                onClick={() => setShowDetails(false)}
                className="w-8 h-8 bg-gray-100 hover:bg-gray-200 rounded-lg flex items-center justify-center text-gray-600 transition-colors"
              >
                ✕
              </button>
            </div>
            
            <div className="space-y-4">
              <div>
                <h4 className="font-semibold text-gray-800 mb-2">{selectedHomework.title}</h4>
                <div className="flex items-center gap-4 text-sm text-gray-600 mb-3">
                  <span className="flex items-center gap-1">
                    <BookOpen className="w-4 h-4" />
                    {selectedHomework.subject}
                  </span>
                  <span className="flex items-center gap-1">
                    <Clock className="w-4 h-4" />
                    {selectedHomework.estimatedTime} min
                  </span>
                  <span className="flex items-center gap-1">
                    <Calendar className="w-4 h-4" />
                    {new Date(selectedHomework.dueDate).toLocaleDateString('fr-FR')}
                  </span>
                </div>
              </div>
              
              {selectedHomework.description && (
                <div className="bg-white p-6 rounded-xl border border-gray-200">
                  <h5 className="font-semibold text-gray-800 mb-3 flex items-center gap-2">
                    <div className="w-6 h-6 bg-blue-100 rounded-lg flex items-center justify-center">
                      <BookOpen className="w-3 h-3 text-blue-600" />
                    </div>
                    Description
                  </h5>
                  <p className="text-gray-700 leading-relaxed">{selectedHomework.description}</p>
                </div>
              )}
              
              {selectedHomework.instructions && (
                <div className="bg-white p-6 rounded-xl border border-gray-200">
                  <h5 className="font-semibold text-gray-800 mb-3 flex items-center gap-2">
                    <div className="w-6 h-6 bg-green-100 rounded-lg flex items-center justify-center">
                      <CheckSquare className="w-3 h-3 text-green-600" />
                    </div>
                    Instructions
                  </h5>
                  <p className="text-gray-700 leading-relaxed">{selectedHomework.instructions}</p>
                </div>
              )}
              
              {selectedHomework.attachments && selectedHomework.attachments.length > 0 && (
                <div className="bg-white p-6 rounded-xl border border-gray-200">
                  <h5 className="font-semibold text-gray-800 mb-3 flex items-center gap-2">
                    <div className="w-6 h-6 bg-purple-100 rounded-lg flex items-center justify-center">
                      <FileText className="w-3 h-3 text-purple-600" />
                    </div>
                    Pièces jointes
                  </h5>
                  <div className="space-y-3">
                    {selectedHomework.attachments.map((attachment, index) => (
                      <div key={index} className="flex items-center gap-3 p-3 bg-gray-50 rounded-lg border border-gray-200">
                        <FileText className="w-4 h-4 text-gray-500" />
                        <span className="text-sm font-medium text-gray-700">{attachment}</span>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
            
            <div className="mt-8 flex justify-end">
              <button
                onClick={() => setShowDetails(false)}
                className="px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-medium transition-colors shadow-sm"
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

