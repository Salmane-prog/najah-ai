'use client';

import React, { useState, useEffect } from 'react';
import Sidebar from '../../../../components/Sidebar';
import { useAuth  } from '../../../../hooks/useAuth';
import { User, Search, Filter, Award, BookOpen, Target, TrendingUp, Mail, Phone } from 'lucide-react';
import StudentGamificationWidget from '../../../../components/StudentGamificationWidget';

interface Student {
  id: number;
  name: string;
  email: string;
  role: string;
  avatar_url?: string;
  bio?: string;
  phone?: string;
  overall_progress: number;
  quizzes_completed: number;
  average_score: number;
  last_activity: string;
  classes: Array<{
    id: number;
    name: string;
    subject: string;
    progress: number;
  }>;
  badges: Array<{
    id: number;
    name: string;
    description: string;
    icon: string;
    awarded_at: string;
  }>;
  recent_activity: Array<{
    id: number;
    type: string;
    description: string;
    timestamp: string;
  }>;
}

export default function TeacherStudents() {
  const { user, token } = useAuth();
  const [students, setStudents] = useState<Student[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterClass, setFilterClass] = useState<string>('all');
  const [sortBy, setSortBy] = useState<'name' | 'progress' | 'score' | 'activity'>('name');
  const [selectedStudent, setSelectedStudent] = useState<Student | null>(null);
  const [showStudentModal, setShowStudentModal] = useState(false);

  useEffect(() => {
    if (token) {
      fetchStudents();
    }
  }, [token]);

  const fetchStudents = async () => {
    try {
      setLoading(true);
      setError(null);
      
      // Utiliser l'endpoint existant pour récupérer les vraies données
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/v1/teacher-dashboard/students`, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });

      if (response.ok) {
        const data = await response.json();
        
        // Transformer les données pour correspondre à l'interface Student
        const studentsWithStats = data.students.map((studentData: any) => {
          return {
            id: studentData.id,
            name: studentData.name || `Élève ${studentData.id}`,
            email: studentData.email || 'Email non défini',
            role: 'student', // Par défaut
            avatar_url: '', // L'endpoint existant ne fournit pas l'avatar
            bio: '', // L'endpoint existant ne fournit pas la bio
            phone: '', // L'endpoint existant ne fournit pas le téléphone
            overall_progress: studentData.average_score || 0, // Utiliser le score moyen comme progression
            quizzes_completed: studentData.total_attempts || 0,
            average_score: studentData.average_score || 0,
            last_activity: studentData.last_activity || '',
            classes: [{ id: 1, name: studentData.class_name || 'Classe par défaut' }], // Adapter la structure
            badges: [], // L'endpoint existant ne fournit pas les badges
            recent_activity: [] // L'endpoint existant ne fournit pas l'activité récente
          };
        });

        setStudents(studentsWithStats);
      } else {
        console.error('Erreur API:', response.status, response.statusText);
        setError('Erreur lors du chargement des élèves');
      }
    } catch (err) {
      console.error('Erreur de connexion:', err);
      setError('Erreur de connexion au serveur');
    } finally {
      setLoading(false);
    }
  };

  const getProgressColor = (progress: number) => {
    if (progress >= 80) return 'text-green-600';
    if (progress >= 60) return 'text-yellow-600';
    return 'text-red-600';
  };

  const getScoreColor = (score: number) => {
    if (score >= 80) return 'text-green-600';
    if (score >= 60) return 'text-yellow-600';
    return 'text-red-600';
  };

  const getActivityColor = (activity: string) => {
    if (!activity || activity === 'Invalid Date') return 'text-red-600';
    
    try {
      const activityDate = new Date(activity);
      if (isNaN(activityDate.getTime())) return 'text-red-600';
      
      const daysSince = Math.floor((Date.now() - activityDate.getTime()) / (1000 * 60 * 60 * 24));
      if (daysSince <= 1) return 'text-green-600';
      if (daysSince <= 7) return 'text-yellow-600';
      return 'text-red-600';
    } catch {
      return 'text-red-600';
    }
  };

  const filteredAndSortedStudents = students
    .filter(student => {
      const matchesSearch = (student.name || '').toLowerCase().includes(searchTerm.toLowerCase()) ||
                          (student.email || '').toLowerCase().includes(searchTerm.toLowerCase());
      const matchesClass = filterClass === 'all' || 
                          (student.classes || []).some(c => c.id.toString() === filterClass);
      return matchesSearch && matchesClass;
    })
    .sort((a, b) => {
      switch (sortBy) {
        case 'name':
          return (a.name || '').localeCompare(b.name || '');
        case 'progress':
          return (b.overall_progress ?? 0) - (a.overall_progress ?? 0);
        case 'score':
          return (b.average_score ?? 0) - (a.average_score ?? 0);
        case 'activity':
          return new Date(b.last_activity || '').getTime() - new Date(a.last_activity || '').getTime();
        default:
          return 0;
      }
    });

  const handleStudentClick = (student: Student) => {
    setSelectedStudent(student);
    setShowStudentModal(true);
  };

  if (loading) {
    return (
      <div className="flex min-h-screen bg-gray-50">
        <Sidebar userType="teacher" />
        <div className="flex-1 flex items-center justify-center">
          <div className="text-blue-600 animate-pulse text-xl font-bold">Chargement des élèves...</div>
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
            <h1 className="text-3xl font-bold text-gray-800 mb-2">Élèves</h1>
            <p className="text-gray-600">Gérez et suivez les progrès de vos élèves</p>
          </div>

          {error && (
            <div className="mb-4 p-4 bg-red-50 border border-red-200 rounded-lg">
              <p className="text-red-800">{error}</p>
            </div>
          )}

          {/* Filtres et recherche */}
          <div className="mb-6 flex flex-wrap items-center gap-4">
            <div className="flex items-center gap-4">
              <div className="relative">
                <Search className="absolute left-3 top-2.5 text-gray-400" size={16} />
                <input
                  type="text"
                  placeholder="Rechercher un élève..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>

              <div className="flex items-center gap-2">
                <Filter className="text-gray-600" size={16} />
                <select
                  value={filterClass}
                  onChange={(e) => setFilterClass(e.target.value)}
                  className="px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="all">Toutes les classes</option>
                  <option value="1">Français Avancé</option>
                  <option value="2">Mathématiques</option>
                  <option value="3">Histoire</option>
                </select>
              </div>

              <div className="flex items-center gap-2">
                <span className="text-sm text-gray-600">Trier par:</span>
                <select
                  value={sortBy}
                  onChange={(e) => setSortBy(e.target.value as any)}
                  className="px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="name">Nom</option>
                  <option value="progress">Progression</option>
                  <option value="score">Score</option>
                  <option value="activity">Activité</option>
                </select>
              </div>
            </div>

            <div className="ml-auto">
              <span className="text-sm text-gray-600">
                {filteredAndSortedStudents.length} élève(s) trouvé(s)
              </span>
            </div>
          </div>

          {/* Liste des élèves */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                         {filteredAndSortedStudents.map((student, index) => (
                             <div
                 key={`${student.id}-${student.name}-${index}`}
                 onClick={() => handleStudentClick(student)}
                 className="bg-white rounded-xl shadow-lg p-6 cursor-pointer hover:shadow-xl transition-shadow"
               >
                <div className="flex items-start justify-between mb-4">
                  <div className="flex items-center gap-3">
                    <div className="w-12 h-12 bg-blue-600 rounded-full flex items-center justify-center">
                      <span className="text-white text-lg font-medium">
                        {student.name?.charAt(0) || '?'}
                      </span>
                    </div>
                    <div>
                      <h3 className="font-bold text-gray-800">{student.name || 'Élève sans nom'}</h3>
                      <p className="text-sm text-gray-600">{student.email || 'Email non défini'}</p>
                    </div>
                  </div>
                  <div className="text-right">
                    <span className={`text-sm font-medium ${getProgressColor(student.overall_progress ?? 0)}`}>
                      {student.overall_progress ?? 0}%
                    </span>
                    <p className="text-xs text-gray-500">progression</p>
                  </div>
                </div>

                <div className="space-y-3">
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-gray-600">Score moyen</span>
                    <span className={`font-medium ${getScoreColor(student.average_score ?? 0)}`}>
                      {student.average_score ?? 0}%
                    </span>
                  </div>

                  <div className="flex items-center justify-between">
                    <span className="text-sm text-gray-600">Quiz complétés</span>
                    <span className="font-medium text-gray-800">{student.quizzes_completed ?? 0}</span>
                  </div>

                  <div className="flex items-center justify-between">
                    <span className="text-sm text-gray-600">Classes</span>
                    <span className="font-medium text-gray-800">{(student.classes || []).length}</span>
                  </div>

                  <div className="flex items-center justify-between">
                    <span className="text-sm text-gray-600">Dernière activité</span>
                    <span className={`text-xs font-medium ${getActivityColor(student.last_activity || '')}`}>
                      {student.last_activity && student.last_activity !== 'Invalid Date' 
                        ? new Date(student.last_activity).toLocaleDateString('fr-FR') 
                        : 'Aucune activité'}
                    </span>
                  </div>

                  {/* Badges */}
                  {(student.badges || []).length > 0 && (
                    <div className="pt-3 border-t border-gray-200">
                      <h4 className="text-sm font-medium text-gray-700 mb-2">Badges récents</h4>
                      <div className="flex flex-wrap gap-1">
                        {(student.badges || []).slice(0, 3).map((badge) => (
                          <span
                            key={badge.id}
                            className="px-2 py-1 bg-yellow-100 text-yellow-800 rounded-full text-xs"
                            title={badge.description}
                          >
                            {badge.name}
                          </span>
                        ))}
                        {(student.badges || []).length > 3 && (
                          <span className="text-xs text-gray-500">
                            +{(student.badges || []).length - 3}
                          </span>
                        )}
                      </div>
                    </div>
                  )}

                  {/* Progression par classe */}
                  <div className="pt-3 border-t border-gray-200">
                    <h4 className="text-sm font-medium text-gray-700 mb-2">Classes</h4>
                    <div className="space-y-2">
                      {(student.classes || []).slice(0, 2).map((classData) => (
                        <div key={classData.id} className="flex items-center justify-between">
                          <span className="text-sm text-gray-700 truncate">{classData.name}</span>
                          <span className={`text-xs font-medium ${getProgressColor(classData.progress)}`}>
                            {classData.progress}%
                          </span>
                        </div>
                      ))}
                      {(student.classes || []).length > 2 && (
                        <p className="text-xs text-gray-500">
                          +{(student.classes || []).length - 2} autres classes
                        </p>
                      )}
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>

          {filteredAndSortedStudents.length === 0 && (
            <div className="text-center py-12">
              <User className="mx-auto text-gray-400 mb-4" size={48} />
              <p className="text-gray-600">Aucun élève trouvé</p>
              <p className="text-sm text-gray-500">Ajustez vos filtres de recherche</p>
            </div>
          )}

          {/* Modal de détails de l'élève */}
          {showStudentModal && selectedStudent && (
            <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
              <div className="bg-white rounded-xl p-6 w-full max-w-2xl max-h-[90vh] overflow-y-auto">
                <div className="flex items-center justify-between mb-6">
                  <h3 className="text-xl font-bold text-gray-800">Détails de l'élève</h3>
                  <button
                    onClick={() => setShowStudentModal(false)}
                    className="text-gray-400 hover:text-gray-600"
                  >
                    ✕
                  </button>
                </div>

                <div className="space-y-6">
                  {/* Informations de base */}
                  <div className="flex items-center gap-4">
                    <div className="w-16 h-16 bg-blue-600 rounded-full flex items-center justify-center">
                      <span className="text-white text-xl font-medium">
                        {selectedStudent.name?.charAt(0) || '?'}
                      </span>
                    </div>
                    <div>
                      <h4 className="text-lg font-bold text-gray-800">{selectedStudent.name || 'Élève sans nom'}</h4>
                      <p className="text-gray-600">{selectedStudent.email || 'Email non défini'}</p>
                      {selectedStudent.phone && (
                        <p className="text-sm text-gray-500 flex items-center gap-1">
                          <Phone size={12} />
                          {selectedStudent.phone}
                        </p>
                      )}
                    </div>
                  </div>

                  {/* Statistiques */}
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <div className="bg-blue-50 p-4 rounded-lg">
                      <div className="flex items-center gap-2 mb-2">
                        <Target className="text-blue-600" size={16} />
                        <span className="text-sm font-medium text-blue-800">Progression</span>
                      </div>
                      <p className={`text-2xl font-bold ${getProgressColor(selectedStudent.overall_progress)}`}>
                        {selectedStudent.overall_progress}%
                      </p>
                    </div>

                    <div className="bg-green-50 p-4 rounded-lg">
                      <div className="flex items-center gap-2 mb-2">
                        <Award className="text-green-600" size={16} />
                        <span className="text-sm font-medium text-green-800">Score moyen</span>
                      </div>
                      <p className={`text-2xl font-bold ${getScoreColor(selectedStudent.average_score)}`}>
                        {selectedStudent.average_score}%
                      </p>
                    </div>

                    <div className="bg-purple-50 p-4 rounded-lg">
                      <div className="flex items-center gap-2 mb-2">
                        <BookOpen className="text-purple-600" size={16} />
                        <span className="text-sm font-medium text-purple-800">Quiz complétés</span>
                      </div>
                      <p className="text-2xl font-bold text-purple-800">
                        {selectedStudent.quizzes_completed}
                      </p>
                    </div>
                  </div>

                  {/* Classes */}
                  <div>
                    <h5 className="font-semibold text-gray-800 mb-3">Classes</h5>
                    <div className="space-y-3">
                      {selectedStudent.classes.map((classData) => (
                        <div key={classData.id} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                          <div>
                            <p className="font-medium text-gray-800">{classData.name}</p>
                            <p className="text-sm text-gray-600">{classData.subject}</p>
                          </div>
                          <div className="text-right">
                            <span className={`font-bold ${getProgressColor(classData.progress)}`}>
                              {classData.progress}%
                            </span>
                            <div className="w-20 bg-gray-200 rounded-full h-2 mt-1">
                              <div
                                className="bg-blue-600 h-2 rounded-full"
                                style={{ width: `${classData.progress}%` }}
                              ></div>
                            </div>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>

                  {/* Badges */}
                  {selectedStudent.badges.length > 0 && (
                    <div>
                      <h5 className="font-semibold text-gray-800 mb-3">Badges ({selectedStudent.badges.length})</h5>
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                        {selectedStudent.badges.map((badge) => (
                          <div key={badge.id} className="flex items-center gap-3 p-3 bg-yellow-50 rounded-lg">
                            <div className="w-8 h-8 bg-yellow-600 rounded-full flex items-center justify-center">
                              <span className="text-white text-sm">🏆</span>
                            </div>
                            <div>
                              <p className="font-medium text-gray-800">{badge.name}</p>
                              <p className="text-sm text-gray-600">{badge.description}</p>
                              <p className="text-xs text-gray-500">
                                Obtenu le {new Date(badge.awarded_at).toLocaleDateString('fr-FR')}
                              </p>
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Activité récente */}
                  {selectedStudent.recent_activity.length > 0 && (
                    <div>
                      <h5 className="font-semibold text-gray-800 mb-3">Activité récente</h5>
                      <div className="space-y-2">
                        {selectedStudent.recent_activity.slice(0, 5).map((activity) => (
                          <div key={activity.id} className="flex items-center gap-3 p-2 bg-gray-50 rounded-lg">
                            <div className="w-2 h-2 bg-blue-500 rounded-full"></div>
                            <div className="flex-1">
                              <p className="text-sm text-gray-700">{activity.description}</p>
                              <p className="text-xs text-gray-500">
                                {new Date(activity.timestamp).toLocaleDateString('fr-FR')}
                              </p>
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Gamification Avancée */}
                  <div className="mt-8">
                    <h5 className="font-semibold text-gray-800 mb-4">Gamification Avancée</h5>
                    <StudentGamificationWidget 
                      studentId={selectedStudent.id} 
                      token={token} 
                    />
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
} 