'use client';

import React, { useState, useEffect } from 'react';
import Sidebar from '../../../../components/Sidebar';
import { useAuth  } from '../../../../hooks/useAuth';
import { useDashboard } from '../../../../contexts/DashboardContext';
import { Users, Plus, Edit, Trash2, UserPlus, BookOpen, Award, Target } from 'lucide-react';

interface Class {
  id: number;
  name: string;
  description: string;
  subject: string;
  student_count: number;
  created_at: string;
  teacher: {
    id: number;
    name: string;
    email: string;
  };
  students: Array<{
    id: number;
    name: string;
    email: string;
    progress: number;
    last_activity: string;
  }>;
}

export default function TeacherClasses() {
  const { user, token } = useAuth();
  const { triggerRefresh } = useDashboard();
  const [classes, setClasses] = useState<Class[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [showEditModal, setShowEditModal] = useState(false);
  const [showStudentsModal, setShowStudentsModal] = useState(false);
  const [selectedClass, setSelectedClass] = useState<Class | null>(null);
  const [searchTerm, setSearchTerm] = useState('');

  // États pour les formulaires
  const [createForm, setCreateForm] = useState({
    name: '',
    description: '',
    subject: ''
  });

  const [editForm, setEditForm] = useState({
    name: '',
    description: '',
    subject: ''
  });

  useEffect(() => {
    if (token) {
      fetchClasses();
    }
  }, [token]);

  const fetchClasses = async () => {
    try {
      setLoading(true);
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/v1/teacher/classes/`, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });

      if (response.ok) {
        const data = await response.json();
        setClasses(data);
        setError(null); // Effacer les erreurs précédentes
      } else {
        const errorData = await response.json();
        setError(`Erreur lors du chargement des classes: ${errorData.detail || 'Erreur inconnue'}`);
      }
    } catch (err) {
      setError('Erreur de connexion au serveur');
    } finally {
      setLoading(false);
    }
  };

  const createClass = async () => {
    try {
      setError(null); // Effacer les erreurs précédentes
      
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/v1/teacher/classes/`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          name: createForm.name,
          description: createForm.description,
          subject: createForm.subject,
          level: 'middle', // Niveau par défaut
          max_students: 30 // Capacité par défaut
        })
      });

      if (response.ok) {
        const newClass = await response.json();
        setShowCreateModal(false);
        setCreateForm({ name: '', description: '', subject: '' });
        fetchClasses(); // Recharger la liste
        triggerRefresh(); // Déclencher la mise à jour du dashboard
        setError(null);
      } else {
        const errorData = await response.json();
        setError(`Erreur lors de la création de la classe: ${errorData.detail || 'Erreur inconnue'}`);
      }
    } catch (err) {
      setError('Erreur de connexion au serveur');
    }
  };

  const updateClass = async () => {
    if (!selectedClass) return;

    try {
      setError(null);
      
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/v1/teacher/classes/${selectedClass.id}`, {
        method: 'PUT',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          name: editForm.name,
          description: editForm.description,
          subject: editForm.subject,
          level: 'middle', // Niveau par défaut
          max_students: 30 // Capacité par défaut
        })
      });

      if (response.ok) {
        setShowEditModal(false);
        setSelectedClass(null);
        setEditForm({ name: '', description: '', subject: '' });
        fetchClasses(); // Recharger la liste
        triggerRefresh(); // Déclencher la mise à jour du dashboard
        setError(null);
      } else {
        const errorData = await response.json();
        setError(`Erreur lors de la mise à jour de la classe: ${errorData.detail || 'Erreur inconnue'}`);
      }
    } catch (err) {
      setError('Erreur de connexion au serveur');
    }
  };

  const deleteClass = async (classId: number) => {
    if (!confirm('Êtes-vous sûr de vouloir supprimer cette classe ?')) return;

    try {
      setError(null);
      
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/v1/teacher/classes/${classId}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });

      if (response.ok) {
        fetchClasses(); // Recharger la liste
        triggerRefresh(); // Déclencher la mise à jour du dashboard
        setError(null);
      } else {
        const errorData = await response.json();
        setError(`Erreur lors de la suppression de la classe: ${errorData.detail || 'Erreur inconnue'}`);
      }
    } catch (err) {
      setError('Erreur de connexion au serveur');
    }
  };

  const openStudentsModal = (cls: Class) => {
    setSelectedClass(cls);
    setShowStudentsModal(true);
  };

  const handleEdit = (classData: Class) => {
    setSelectedClass(classData);
    setEditForm({
              name: classData.name || '',
        description: classData.description || '',
        subject: classData.subject || ''
    });
    setShowEditModal(true);
  };

  const filteredClasses = classes.filter(classData =>
            (classData.name || '').toLowerCase().includes(searchTerm.toLowerCase()) ||
        (classData.subject || '').toLowerCase().includes(searchTerm.toLowerCase())
  );

  if (loading) {
    return (
      <div className="flex min-h-screen bg-gray-50">
        <Sidebar userType="teacher" />
        <div className="flex-1 flex items-center justify-center">
          <div className="text-blue-600 animate-pulse text-xl font-bold">Chargement des classes...</div>
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
          <div className="mb-6">
            <h1 className="text-3xl font-bold text-gray-800 mb-2">Classes</h1>
            <p className="text-gray-600">Gérez vos classes et leurs élèves</p>
          </div>

          {error && (
            <div className="mb-4 p-4 bg-red-50 border border-red-200 rounded-lg">
              <p className="text-red-800">{error}</p>
            </div>
          )}

          {/* Actions */}
          <div className="mb-6 flex flex-wrap items-center justify-between gap-4">
            <div className="flex items-center gap-4">
              <div className="relative">
                <input
                  type="text"
                  placeholder="Rechercher une classe..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
                <Users className="absolute left-3 top-2.5 text-gray-400" size={16} />
              </div>
            </div>

            <button
              onClick={() => setShowCreateModal(true)}
              className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
            >
              <Plus size={16} />
              Nouvelle Classe
            </button>
          </div>

          {/* Liste des classes */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {filteredClasses.map((classData) => (
              <div key={classData.id} className="bg-white rounded-xl shadow-lg p-6">
                <div className="flex items-start justify-between mb-4">
                  <div className="flex-1">
                    <h3 className="text-lg font-bold text-gray-800 mb-1">{classData.name || 'Classe sans nom'}</h3>
                    <p className="text-sm text-gray-600 mb-2">{classData.subject || 'Matière non définie'}</p>
                    <p className="text-sm text-gray-500">{classData.description || 'Aucune description'}</p>
                  </div>
                  <div className="flex items-center gap-2">
                    <button
                      onClick={() => openStudentsModal(classData)}
                      className="p-2 text-gray-600 hover:text-green-600 hover:bg-green-50 rounded-lg"
                      title="Gérer les étudiants"
                    >
                      <UserPlus size={16} />
                    </button>
                    <button
                      onClick={() => handleEdit(classData)}
                      className="p-2 text-gray-600 hover:text-blue-600 hover:bg-blue-50 rounded-lg"
                      title="Modifier"
                    >
                      <Edit size={16} />
                    </button>
                    <button
                      onClick={() => deleteClass(classData.id)}
                      className="p-2 text-gray-600 hover:text-red-600 hover:bg-red-50 rounded-lg"
                      title="Supprimer"
                    >
                      <Trash2 size={16} />
                    </button>
                  </div>
                </div>

                <div className="space-y-3">
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-gray-600">Élèves</span>
                    <span className="font-medium text-gray-800">{classData.student_count ?? 0}</span>
                  </div>

                  <div className="flex items-center justify-between">
                    <span className="text-sm text-gray-600">Créée le</span>
                    <span className="text-sm text-gray-600">
                      {classData.created_at ? new Date(classData.created_at).toLocaleDateString('fr-FR') : 'Date inconnue'}
                    </span>
                  </div>

                  <div className="pt-3 border-t border-gray-200">
                    <h4 className="text-sm font-medium text-gray-700 mb-2">Élèves récents</h4>
                    <div className="space-y-2">
                      {(classData.students || []).slice(0, 3).map((student) => (
                        <div key={student.id} className="flex items-center justify-between">
                          <div className="flex items-center gap-2">
                            <div className="w-6 h-6 bg-blue-600 rounded-full flex items-center justify-center">
                              <span className="text-white text-xs font-medium">
                                {student.name?.charAt(0) || '?'}
                              </span>
                            </div>
                            <span className="text-sm text-gray-700">{student.name || 'Élève sans nom'}</span>
                          </div>
                          <span className={`text-xs font-medium ${(student.progress ?? 0) >= 80 ? 'text-green-600' : (student.progress ?? 0) >= 60 ? 'text-yellow-600' : 'text-red-600'}`}>
                            {student.progress ?? 0}%
                          </span>
                        </div>
                      ))}
                      {(classData.students || []).length > 3 && (
                        <p className="text-xs text-gray-500">
                          +{(classData.students || []).length - 3} autres élèves
                        </p>
                      )}
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>

          {filteredClasses.length === 0 && (
            <div className="text-center py-12">
              <Users className="mx-auto text-gray-400 mb-4" size={48} />
              <p className="text-gray-600">Aucune classe trouvée</p>
              <p className="text-sm text-gray-500">Créez votre première classe pour commencer</p>
            </div>
          )}

          {/* Modal de création */}
          {showCreateModal && (
            <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
              <div className="bg-white rounded-xl p-6 w-full max-w-md">
                <h3 className="text-lg font-bold text-gray-800 mb-4">Nouvelle Classe</h3>
                <div className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Nom de la classe</label>
                    <input
                      type="text"
                      value={createForm.name}
                      onChange={(e) => setCreateForm({ ...createForm, name: e.target.value })}
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                      placeholder="Ex: Français Avancé"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Matière</label>
                    <input
                      type="text"
                      value={createForm.subject}
                      onChange={(e) => setCreateForm({ ...createForm, subject: e.target.value })}
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                      placeholder="Ex: Français"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Description</label>
                    <textarea
                      value={createForm.description}
                      onChange={(e) => setCreateForm({ ...createForm, description: e.target.value })}
                      rows={3}
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                      placeholder="Description de la classe..."
                    />
                  </div>
                </div>
                <div className="flex justify-end gap-3 mt-6">
                  <button
                    onClick={() => setShowCreateModal(false)}
                    className="px-4 py-2 text-gray-600 hover:text-gray-800"
                  >
                    Annuler
                  </button>
                  <button
                    onClick={createClass}
                    disabled={!createForm.name || !createForm.subject}
                    className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50"
                  >
                    Créer
                  </button>
                </div>
              </div>
            </div>
          )}

          {/* Modal de modification */}
          {showEditModal && selectedClass && (
            <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
              <div className="bg-white rounded-xl p-6 w-full max-w-md">
                <h3 className="text-lg font-bold text-gray-800 mb-4">Modifier la Classe</h3>
                <div className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Nom de la classe</label>
                    <input
                      type="text"
                      value={editForm.name}
                      onChange={(e) => setEditForm({ ...editForm, name: e.target.value })}
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Matière</label>
                    <input
                      type="text"
                      value={editForm.subject}
                      onChange={(e) => setEditForm({ ...editForm, subject: e.target.value })}
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Description</label>
                    <textarea
                      value={editForm.description}
                      onChange={(e) => setEditForm({ ...editForm, description: e.target.value })}
                      rows={3}
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                  </div>
                </div>
                <div className="flex justify-end gap-3 mt-6">
                  <button
                    onClick={() => setShowEditModal(false)}
                    className="px-4 py-2 text-gray-600 hover:text-gray-800"
                  >
                    Annuler
                  </button>
                  <button
                    onClick={updateClass}
                    disabled={!editForm.name || !editForm.subject}
                    className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50"
                  >
                    Modifier
                  </button>
                </div>
              </div>
            </div>
          )}

          {/* Modal de gestion des étudiants */}
          {showStudentsModal && selectedClass && (
            <StudentsManagementModal
              classData={selectedClass}
              onClose={() => setShowStudentsModal(false)}
              onRefresh={fetchClasses}
              token={token}
              isOpen={showStudentsModal}
            />
          )}
        </div>
      </div>
    </div>
  );
}

// Composant Modal de gestion des étudiants
interface StudentsManagementModalProps {
  classData: Class;
  onClose: () => void;
  onRefresh: () => void;
  token: string;
  isOpen: boolean;
}

function StudentsManagementModal({ classData, onClose, onRefresh, token, isOpen }: StudentsManagementModalProps) {
  const [students, setStudents] = useState<any[]>([]);
  const [availableStudents, setAvailableStudents] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedStudentId, setSelectedStudentId] = useState('');
  const [addingStudent, setAddingStudent] = useState(false);

  useEffect(() => {
    if (isOpen) {
      fetchClassStudents();
      fetchAvailableStudents();
    }
  }, [isOpen]);

  const fetchClassStudents = async () => {
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/v1/teacher/classes/${classData.id}/students`, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });
      
      if (response.ok) {
        const data = await response.json();
        setStudents(data);
      }
    } catch (err) {
      console.error('Erreur lors du chargement des étudiants:', err);
    } finally {
      setLoading(false);
    }
  };

  const fetchAvailableStudents = async () => {
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/v1/users/?role=student`, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });
      
      if (response.ok) {
        const data = await response.json();
        // Filtrer les étudiants qui ne sont pas déjà dans cette classe
        const classStudentIds = students.map(s => s.id);
        const available = data.filter((student: any) => !classStudentIds.includes(student.id));
        setAvailableStudents(available);
      }
    } catch (err) {
      console.error('Erreur lors du chargement des étudiants disponibles:', err);
    }
  };

  const addStudentToClass = async () => {
    if (!selectedStudentId) return;
    
    try {
      setAddingStudent(true);
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/v1/teacher/classes/${classData.id}/students/${selectedStudentId}`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });
      
             if (response.ok) {
         setSelectedStudentId('');
         // Forcer le rafraîchissement immédiat
         await fetchClassStudents();
         await fetchAvailableStudents();
         onRefresh(); // Rafraîchir la liste des classes
         // Fermer le modal après succès
         onClose();
       } else {
        const errorData = await response.json();
        alert(`Erreur: ${errorData.detail || 'Erreur inconnue'}`);
      }
    } catch (err) {
      alert('Erreur lors de l\'ajout de l\'étudiant');
    } finally {
      setAddingStudent(false);
    }
  };

  const removeStudentFromClass = async (studentId: number) => {
    if (!confirm('Êtes-vous sûr de vouloir retirer cet étudiant de la classe ?')) return;
    
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/v1/teacher/classes/${classData.id}/students/${studentId}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });
      
      if (response.ok) {
        fetchClassStudents();
        fetchAvailableStudents();
        onRefresh();
      } else {
        const errorData = await response.json();
        alert(`Erreur: ${errorData.detail || 'Erreur inconnue'}`);
      }
    } catch (err) {
      alert('Erreur lors du retrait de l\'étudiant');
    }
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-xl p-6 w-full max-w-2xl max-h-[90vh] overflow-y-auto">
        <div className="flex items-center justify-between mb-6">
          <h3 className="text-xl font-bold text-gray-800">
            Gérer les étudiants - {classData.name}
          </h3>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-gray-600 text-2xl font-bold"
          >
            ×
          </button>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Étudiants actuels de la classe */}
          <div>
            <h4 className="text-lg font-semibold text-gray-700 mb-4">
              Étudiants de la classe ({students.length})
            </h4>
            {loading ? (
              <div className="text-center py-4">Chargement...</div>
            ) : students.length === 0 ? (
              <div className="text-center py-8 text-gray-500">
                <Users size={32} className="mx-auto mb-2 text-gray-400" />
                <p>Aucun étudiant dans cette classe</p>
              </div>
            ) : (
              <div className="space-y-2">
                {students.map((student) => (
                  <div key={student.id} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                    <div>
                      <div className="font-medium">{student.name || student.username}</div>
                      <div className="text-sm text-gray-600">{student.email}</div>
                    </div>
                    <button
                      onClick={() => removeStudentFromClass(student.id)}
                      className="text-red-600 hover:text-red-800 p-1"
                      title="Retirer de la classe"
                    >
                      <Trash2 size={16} />
                    </button>
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* Ajouter des étudiants */}
          <div>
            <h4 className="text-lg font-semibold text-gray-700 mb-4">
              Ajouter des étudiants
            </h4>
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Sélectionner un étudiant
                </label>
                <select
                  value={selectedStudentId}
                  onChange={(e) => setSelectedStudentId(e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  disabled={availableStudents.length === 0}
                >
                  <option value="">-- Choisir un étudiant --</option>
                  {availableStudents.map((student) => (
                    <option key={student.id} value={student.id}>
                      {student.name || student.username} ({student.email})
                    </option>
                  ))}
                </select>
                {availableStudents.length === 0 && (
                  <p className="text-sm text-gray-500 mt-1">
                    Tous les étudiants sont déjà assignés à une classe
                  </p>
                )}
              </div>
              
              <button
                onClick={addStudentToClass}
                disabled={!selectedStudentId || addingStudent}
                className="w-full px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {addingStudent ? 'Ajout en cours...' : 'Ajouter à la classe'}
              </button>
            </div>
          </div>
        </div>

        <div className="mt-6 flex justify-end">
          <button
            onClick={onClose}
            className="px-4 py-2 text-gray-600 hover:text-gray-800"
          >
            Fermer
          </button>
        </div>
      </div>
    </div>
  );
} 