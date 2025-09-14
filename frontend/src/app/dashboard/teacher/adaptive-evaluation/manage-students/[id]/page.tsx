'use client';

import React, { useState, useEffect } from 'react';
import { ArrowLeft, Users, Plus, Search, Filter, Mail, MessageSquare, Eye, Edit, Trash2, CheckCircle, XCircle, Clock } from 'lucide-react';
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

interface Student {
  id: number;
  name: string;
  email: string;
  enrollment_date: string;
  status: 'enrolled' | 'active' | 'completed' | 'dropped';
  progress: number;
  last_activity: string;
  score?: number;
  feedback_count: number;
}

export default function ManageStudentsPage({ params }: { params: { id: string } }) {
  const [assessment, setAssessment] = useState<Assessment | null>(null);
  const [students, setStudents] = useState<Student[]>([]);
  const [filteredStudents, setFilteredStudents] = useState<Student[]>([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [statusFilter, setStatusFilter] = useState<string>('all');
  const [showAddStudent, setShowAddStudent] = useState(false);
  const [newStudent, setNewStudent] = useState({ name: '', email: '' });
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Récupérer l'évaluation depuis localStorage
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
      
      // Générer des étudiants simulés
      const mockStudents: Student[] = Array.from({ length: foundAssessment.student_count || 0 }, (_, i) => ({
        id: i + 1,
        name: `Étudiant ${i + 1}`,
        email: `etudiant${i + 1}@example.com`,
        enrollment_date: new Date(Date.now() - Math.random() * 30 * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
        status: Math.random() > 0.1 ? 'active' : Math.random() > 0.5 ? 'completed' : 'enrolled',
        progress: Math.floor(Math.random() * 100),
        last_activity: new Date(Date.now() - Math.random() * 7 * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
        score: Math.random() > 0.3 ? Math.floor(Math.random() * 40) + 60 : undefined,
        feedback_count: Math.floor(Math.random() * 5)
      }));
      
      setStudents(mockStudents);
      setFilteredStudents(mockStudents);
    }
    
    setIsLoading(false);
  }, [params.id]);

  useEffect(() => {
    let filtered = students;
    
    if (searchTerm) {
      filtered = filtered.filter(student => 
        student.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        student.email.toLowerCase().includes(searchTerm.toLowerCase())
      );
    }
    
    if (statusFilter !== 'all') {
      filtered = filtered.filter(student => student.status === statusFilter);
    }
    
    setFilteredStudents(filtered);
  }, [students, searchTerm, statusFilter]);

  const handleAddStudent = () => {
    if (newStudent.name && newStudent.email) {
      const student: Student = {
        id: Date.now(),
        name: newStudent.name,
        email: newStudent.email,
        enrollment_date: new Date().toISOString().split('T')[0],
        status: 'enrolled',
        progress: 0,
        last_activity: new Date().toISOString().split('T')[0],
        feedback_count: 0
      };
      
      setStudents([...students, student]);
      setNewStudent({ name: '', email: '' });
      setShowAddStudent(false);
    }
  };

  const handleRemoveStudent = (studentId: number) => {
    setStudents(students.filter(s => s.id !== studentId));
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active': return 'text-green-600 bg-green-100';
      case 'completed': return 'text-blue-600 bg-blue-100';
      case 'enrolled': return 'text-yellow-600 bg-yellow-100';
      case 'dropped': return 'text-red-600 bg-red-100';
      default: return 'text-gray-600 bg-gray-100';
    }
  };

  const getStatusLabel = (status: string) => {
    switch (status) {
      case 'active': return 'Actif';
      case 'completed': return 'Terminé';
      case 'enrolled': return 'Inscrit';
      case 'dropped': return 'Abandonné';
      default: return status;
    }
  };

  const getProgressColor = (progress: number) => {
    if (progress >= 80) return 'text-green-600';
    if (progress >= 60) return 'text-yellow-600';
    if (progress >= 40) return 'text-orange-600';
    return 'text-red-600';
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Chargement...</p>
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
      <div className="max-w-7xl mx-auto py-8 px-4">
        {/* Header */}
        <div className="mb-8">
          <Link
            href={`/dashboard/teacher/adaptive-evaluation/view-assessment/${assessment.id}`}
            className="inline-flex items-center text-blue-600 hover:text-blue-700 mb-4"
          >
            <ArrowLeft className="w-4 h-4 mr-2" />
            Retour à l'évaluation
          </Link>
          <h1 className="text-3xl font-bold text-gray-900">Gestion des Étudiants</h1>
          <p className="text-gray-600 mt-2">{assessment.title}</p>
        </div>

        {/* Statistiques générales */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <div className="flex items-center">
              <Users className="w-8 h-8 text-blue-600" />
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Total Étudiants</p>
                <p className="text-2xl font-bold text-gray-900">{students.length}</p>
              </div>
            </div>
          </div>
          
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <div className="flex items-center">
              <CheckCircle className="w-8 h-8 text-green-600" />
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Actifs</p>
                <p className="text-2xl font-bold text-gray-900">
                  {students.filter(s => s.status === 'active').length}
                </p>
              </div>
            </div>
          </div>
          
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <div className="flex items-center">
              <Clock className="w-8 h-8 text-yellow-600" />
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">En cours</p>
                <p className="text-2xl font-bold text-gray-900">
                  {students.filter(s => s.status === 'enrolled').length}
                </p>
              </div>
            </div>
          </div>
          
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <div className="flex items-center">
              <CheckCircle className="w-8 h-8 text-blue-600" />
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Terminés</p>
                <p className="text-2xl font-bold text-gray-900">
                  {students.filter(s => s.status === 'completed').length}
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* Contrôles et recherche */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-6">
          <div className="flex flex-col md:flex-row md:items-center md:justify-between space-y-4 md:space-y-0">
            <div className="flex flex-col sm:flex-row space-y-2 sm:space-y-0 sm:space-x-4">
              <div className="relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
                <input
                  type="text"
                  placeholder="Rechercher un étudiant..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>
              
              <select
                value={statusFilter}
                onChange={(e) => setStatusFilter(e.target.value)}
                className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="all">Tous les statuts</option>
                <option value="enrolled">Inscrits</option>
                <option value="active">Actifs</option>
                <option value="completed">Terminés</option>
                <option value="dropped">Abandonnés</option>
              </select>
            </div>
            
            <button
              onClick={() => setShowAddStudent(true)}
              className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors flex items-center"
            >
              <Plus className="w-4 h-4 mr-2" />
              Ajouter un étudiant
            </button>
          </div>
        </div>

        {/* Modal d'ajout d'étudiant */}
        {showAddStudent && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
            <div className="bg-white rounded-lg p-6 w-full max-w-md">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Ajouter un étudiant</h3>
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Nom complet</label>
                  <input
                    type="text"
                    value={newStudent.name}
                    onChange={(e) => setNewStudent({ ...newStudent, name: e.target.value })}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    placeholder="Nom de l'étudiant"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Email</label>
                  <input
                    type="email"
                    value={newStudent.email}
                    onChange={(e) => setNewStudent({ ...newStudent, email: e.target.value })}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    placeholder="email@example.com"
                  />
                </div>
                <div className="flex space-x-3 pt-4">
                  <button
                    onClick={handleAddStudent}
                    className="flex-1 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
                  >
                    Ajouter
                  </button>
                  <button
                    onClick={() => setShowAddStudent(false)}
                    className="flex-1 px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors"
                  >
                    Annuler
                  </button>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Liste des étudiants */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200">
          <div className="px-6 py-4 border-b border-gray-200">
            <h2 className="text-lg font-semibold text-gray-900">
              Étudiants ({filteredStudents.length})
            </h2>
          </div>
          
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Étudiant
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Statut
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Progression
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Score
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Dernière activité
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Actions
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {filteredStudents.map((student) => (
                  <tr key={student.id} className="hover:bg-gray-50">
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div>
                        <div className="text-sm font-medium text-gray-900">{student.name}</div>
                        <div className="text-sm text-gray-500">{student.email}</div>
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className={`px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(student.status)}`}>
                        {getStatusLabel(student.status)}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="flex items-center">
                        <div className="w-16 bg-gray-200 rounded-full h-2 mr-2">
                          <div 
                            className={`h-2 rounded-full ${getProgressColor(student.progress)}`}
                            style={{ width: `${student.progress}%` }}
                          ></div>
                        </div>
                        <span className={`text-sm font-medium ${getProgressColor(student.progress)}`}>
                          {student.progress}%
                        </span>
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm text-gray-900">
                        {student.score ? `${student.score}%` : 'N/A'}
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm text-gray-900">{student.last_activity}</div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                      <div className="flex space-x-2">
                        <button className="text-blue-600 hover:text-blue-900" title="Voir le profil">
                          <Eye className="w-4 h-4" />
                        </button>
                        <button className="text-green-600 hover:text-green-900" title="Envoyer un message">
                          <MessageSquare className="w-4 h-4" />
                        </button>
                        <button className="text-purple-600 hover:text-purple-900" title="Modifier">
                          <Edit className="w-4 h-4" />
                        </button>
                        <button 
                          onClick={() => handleRemoveStudent(student.id)}
                          className="text-red-600 hover:text-red-900" 
                          title="Retirer"
                        >
                          <Trash2 className="w-4 h-4" />
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {filteredStudents.length === 0 && (
          <div className="text-center py-12">
            <Users className="w-16 h-16 text-gray-400 mx-auto mb-4" />
            <h3 className="text-lg font-medium text-gray-900 mb-2">Aucun étudiant trouvé</h3>
            <p className="text-gray-500">
              {searchTerm || statusFilter !== 'all' 
                ? 'Aucun étudiant ne correspond à vos critères de recherche.'
                : 'Aucun étudiant n\'est encore inscrit à cette évaluation.'
              }
            </p>
          </div>
        )}
      </div>
    </div>
  );
}
























