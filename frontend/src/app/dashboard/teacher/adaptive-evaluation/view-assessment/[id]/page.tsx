'use client';

import React, { useState, useEffect } from 'react';
import { ArrowLeft, Eye, Edit, Users, Clock, Target, BookOpen, BarChart3, CheckCircle, XCircle, AlertCircle } from 'lucide-react';
import Link from 'next/link';

interface Assessment {
  id: number;
  title: string;
  subject: string;
  assessment_type: string;
  due_date: string;
  status: string;
  student_count: number;
  average_score: number;
  config?: any;
}

interface StudentSubmission {
  id: number;
  student_name: string;
  submitted_at: string;
  score: number;
  status: 'submitted' | 'graded' | 'late' | 'missing';
  feedback?: string;
}

export default function ViewAssessmentPage({ params }: { params: { id: string } }) {
  const [assessment, setAssessment] = useState<Assessment | null>(null);
  const [studentSubmissions, setStudentSubmissions] = useState<StudentSubmission[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Récupérer toutes les évaluations depuis localStorage
    const allAssessments = JSON.parse(localStorage.getItem('formativeAssessments') || '[]');
    const defaultAssessments = [
      {
        id: 1,
        title: "Projet de Recherche - Écologie",
        subject: "Sciences",
        assessment_type: "project",
        due_date: "2024-02-15",
        status: "active",
        student_count: 22,
        average_score: 78.5
      },
      {
        id: 2,
        title: "Présentation Orale - Littérature",
        subject: "Français",
        assessment_type: "presentation",
        due_date: "2024-02-10",
        status: "completed",
        student_count: 25,
        average_score: 82.3
      },
      {
        id: 3,
        title: "Discussion Critique - Philosophie",
        subject: "Philosophie",
        assessment_type: "discussion",
        due_date: "2024-02-20",
        status: "active",
        student_count: 20,
        average_score: 0
      }
    ];

    const allAssessmentsCombined = [...defaultAssessments, ...allAssessments];
    const foundAssessment = allAssessmentsCombined.find(a => a.id === parseInt(params.id));
    
    if (foundAssessment) {
      setAssessment(foundAssessment);
      
      // Générer des soumissions d'étudiants simulées
      const mockSubmissions: StudentSubmission[] = Array.from({ length: foundAssessment.student_count || 0 }, (_, i) => ({
        id: i + 1,
        student_name: `Étudiant ${i + 1}`,
        submitted_at: new Date(Date.now() - Math.random() * 7 * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
        score: Math.floor(Math.random() * 40) + 60, // Score entre 60 et 100
        status: Math.random() > 0.8 ? 'late' : Math.random() > 0.9 ? 'missing' : 'graded',
        feedback: Math.random() > 0.5 ? 'Travail bien structuré avec des idées intéressantes.' : undefined
      }));
      
      setStudentSubmissions(mockSubmissions);
    }
    
    setIsLoading(false);
  }, [params.id]);

  const getAssessmentTypeIcon = (type: string) => {
    switch (type) {
      case 'project': return <BookOpen className="w-5 h-5" />;
      case 'presentation': return <Users className="w-5 h-5" />;
      case 'discussion': return <Target className="w-5 h-5" />;
      case 'portfolio': return <BookOpen className="w-5 h-5" />;
      case 'observation': return <Eye className="w-5 h-5" />;
      case 'self_evaluation': return <Target className="w-5 h-5" />;
      default: return <BookOpen className="w-5 h-5" />;
    }
  };

  const getAssessmentTypeLabel = (type: string) => {
    switch (type) {
      case 'project': return 'Projet de Recherche';
      case 'presentation': return 'Présentation Orale';
      case 'discussion': return 'Discussion Critique';
      case 'portfolio': return 'Portfolio';
      case 'observation': return 'Observation Participante';
      case 'self_evaluation': return 'Auto-évaluation';
      default: return type;
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active': return 'text-green-600 bg-green-100';
      case 'completed': return 'text-blue-600 bg-blue-100';
      case 'pending': return 'text-yellow-600 bg-yellow-100';
      default: return 'text-gray-600 bg-gray-100';
    }
  };

  const getStatusLabel = (status: string) => {
    switch (status) {
      case 'active': return 'En cours';
      case 'completed': return 'Terminé';
      case 'pending': return 'En attente';
      default: return status;
    }
  };

  const getSubmissionStatusIcon = (status: string) => {
    switch (status) {
      case 'submitted': return <CheckCircle className="w-4 h-4 text-blue-600" />;
      case 'graded': return <CheckCircle className="w-4 h-4 text-green-600" />;
      case 'late': return <AlertCircle className="w-4 h-4 text-yellow-600" />;
      case 'missing': return <XCircle className="w-4 h-4 text-red-600" />;
      default: return <AlertCircle className="w-4 h-4 text-gray-600" />;
    }
  };

  const getSubmissionStatusLabel = (status: string) => {
    switch (status) {
      case 'submitted': return 'Soumis';
      case 'graded': return 'Noté';
      case 'late': return 'En retard';
      case 'missing': return 'Manquant';
      default: return status;
    }
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Chargement de l'évaluation...</p>
        </div>
      </div>
    );
  }

  if (!assessment) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <XCircle className="w-16 h-16 text-red-500 mx-auto mb-4" />
          <h2 className="text-2xl font-bold text-gray-900 mb-2">Évaluation non trouvée</h2>
          <p className="text-gray-600 mb-4">L'évaluation que vous recherchez n'existe pas.</p>
          <Link
            href="/dashboard/teacher/adaptive-evaluation"
            className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
          >
            Retour aux évaluations
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-6xl mx-auto py-8 px-4">
        {/* Header */}
        <div className="mb-8">
          <Link
            href="/dashboard/teacher/adaptive-evaluation"
            className="inline-flex items-center text-blue-600 hover:text-blue-700 mb-4"
          >
            <ArrowLeft className="w-4 h-4 mr-2" />
            Retour aux évaluations
          </Link>
          <h1 className="text-3xl font-bold text-gray-900">{assessment.title}</h1>
          <p className="text-gray-600 mt-2">Détails et suivi de l'évaluation formative</p>
        </div>

        {/* Informations principales */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
          {/* Détails de l'évaluation */}
          <div className="lg:col-span-2">
            <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
              <div className="flex items-start justify-between mb-6">
                <div className="flex items-center space-x-3">
                  {getAssessmentTypeIcon(assessment.assessment_type)}
                  <div>
                    <h2 className="text-xl font-semibold text-gray-900">{assessment.title}</h2>
                    <p className="text-gray-600">{getAssessmentTypeLabel(assessment.assessment_type)}</p>
                  </div>
                </div>
                <span className={`px-3 py-1 rounded-full text-sm font-medium ${getStatusColor(assessment.status)}`}>
                  {getStatusLabel(assessment.status)}
                </span>
              </div>

              <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
                <div className="text-center p-3 bg-gray-50 rounded-lg">
                  <div className="text-2xl font-bold text-blue-600">{assessment.subject}</div>
                  <div className="text-sm text-gray-600">Matière</div>
                </div>
                <div className="text-center p-3 bg-gray-50 rounded-lg">
                  <div className="text-2xl font-bold text-green-600">{assessment.due_date}</div>
                  <div className="text-sm text-gray-600">Échéance</div>
                </div>
                <div className="text-center p-3 bg-gray-50 rounded-lg">
                  <div className="text-2xl font-bold text-purple-600">{assessment.student_count}</div>
                  <div className="text-sm text-gray-600">Étudiants</div>
                </div>
                <div className="text-center p-3 bg-gray-50 rounded-lg">
                  <div className="text-2xl font-bold text-orange-600">
                    {assessment.average_score > 0 ? `${assessment.average_score}%` : 'N/A'}
                  </div>
                  <div className="text-sm text-gray-600">Score Moyen</div>
                </div>
              </div>

              {assessment.config && (
                <div className="space-y-4">
                  {assessment.config.description && (
                    <div>
                      <h4 className="font-medium text-gray-900 mb-2">Description</h4>
                      <p className="text-gray-600">{assessment.config.description}</p>
                    </div>
                  )}
                  
                  {assessment.config.instructions && (
                    <div>
                      <h4 className="font-medium text-gray-900 mb-2">Instructions</h4>
                      <p className="text-gray-600">{assessment.config.instructions}</p>
                    </div>
                  )}

                  {assessment.config.criteria && assessment.config.criteria.length > 0 && (
                    <div>
                      <h4 className="font-medium text-gray-900 mb-2">Critères d'évaluation</h4>
                      <div className="flex flex-wrap gap-2">
                        {assessment.config.criteria.map((criterion: string, index: number) => (
                          <span key={index} className="px-2 py-1 bg-blue-100 text-blue-800 rounded-full text-xs">
                            {criterion}
                          </span>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              )}
            </div>
          </div>

          {/* Actions rapides */}
          <div className="space-y-4">
            <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Actions</h3>
              <div className="space-y-3">
                <Link
                  href={`/dashboard/teacher/adaptive-evaluation/edit-assessment/${assessment.id}`}
                  className="w-full flex items-center justify-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
                >
                  <Edit className="w-4 h-4 mr-2" />
                  Modifier
                </Link>
                <Link
                  href={`/dashboard/teacher/adaptive-evaluation/manage-students/${assessment.id}`}
                  className="w-full flex items-center justify-center px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors"
                >
                  <Users className="w-4 h-4 mr-2" />
                  Gérer les étudiants
                </Link>
                <Link
                  href={`/dashboard/teacher/adaptive-evaluation/analytics/${assessment.id}`}
                  className="w-full flex items-center justify-center px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors"
                >
                  <BarChart3 className="w-4 h-4 mr-2" />
                  Voir les analytics
                </Link>
              </div>
            </div>

            <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Statistiques</h3>
              <div className="space-y-3 text-sm">
                <div className="flex justify-between">
                  <span className="text-gray-600">Soumissions :</span>
                  <span className="font-medium">{studentSubmissions.filter(s => s.status !== 'missing').length}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">En retard :</span>
                  <span className="font-medium text-yellow-600">{studentSubmissions.filter(s => s.status === 'late').length}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Manquants :</span>
                  <span className="font-medium text-red-600">{studentSubmissions.filter(s => s.status === 'missing').length}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Notés :</span>
                  <span className="font-medium text-green-600">{studentSubmissions.filter(s => s.status === 'graded').length}</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Liste des soumissions d'étudiants */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-xl font-semibold text-gray-900">Soumissions des Étudiants</h2>
            <div className="flex space-x-2">
              <button className="px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors">
                Exporter
              </button>
              <button className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors">
                Noter en lot
              </button>
            </div>
          </div>

          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Étudiant
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Date de soumission
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Statut
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Score
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Actions
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {studentSubmissions.map((submission) => (
                  <tr key={submission.id} className="hover:bg-gray-50">
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm font-medium text-gray-900">{submission.student_name}</div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm text-gray-900">{submission.submitted_at}</div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="flex items-center space-x-2">
                        {getSubmissionStatusIcon(submission.status)}
                        <span className="text-sm text-gray-900">{getSubmissionStatusLabel(submission.status)}</span>
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm text-gray-900">
                        {submission.score > 0 ? `${submission.score}%` : 'N/A'}
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                      <div className="flex space-x-2">
                        <button className="text-blue-600 hover:text-blue-900">Voir</button>
                        <button className="text-green-600 hover:text-green-900">Noter</button>
                        <button className="text-purple-600 hover:text-purple-900">Feedback</button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
}
