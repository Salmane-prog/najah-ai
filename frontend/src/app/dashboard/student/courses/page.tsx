"use client";
import React, { useState, useEffect } from 'react';
import { useAuth  } from '../../../../hooks/useAuth';
import { Card } from '../../../../components/Card';
import Button from '../../../../components/Button';
import { 
  BookOpen, 
  Play, 
  Pause, 
  CheckCircle, 
  Clock, 
  Star, 
  Download, 
  Eye,
  Calendar,
  Users,
  BarChart3,
  FileText,
  Video,
  Headphones,
  Book,
  Award
} from 'lucide-react';
import Sidebar from '../../../../components/Sidebar';

interface Course {
  id: number;
  title: string;
  description: string;
  instructor: string;
  instructor_avatar: string;
  duration: number; // en heures
  modules_count: number;
  completed_modules: number;
  progress: number; // 0-100
  rating: number;
  enrolled_students: number;
  difficulty: 'beginner' | 'intermediate' | 'advanced';
  category: string;
  thumbnail: string;
  last_accessed?: string;
  certificate_available: boolean;
  price: number;
  is_free: boolean;
}

interface Module {
  id: number;
  course_id: number;
  title: string;
  description: string;
  duration: number; // en minutes
  content_type: 'video' | 'text' | 'quiz' | 'assignment';
  is_completed: boolean;
  is_locked: boolean;
  resources: Resource[];
}

interface Resource {
  id: number;
  title: string;
  type: 'pdf' | 'video' | 'audio' | 'link';
  url: string;
  size?: string;
  duration?: number;
}

const CoursesPage: React.FC = () => {
  const { user, token } = useAuth();
  const [courses, setCourses] = useState<Course[]>([]);
  const [selectedCourse, setSelectedCourse] = useState<Course | null>(null);
  const [modules, setModules] = useState<Module[]>([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState<'all' | 'enrolled' | 'completed' | 'in_progress'>('all');
  const [searchTerm, setSearchTerm] = useState('');
  const [showCourseDetails, setShowCourseDetails] = useState(false);

  useEffect(() => {
    const fetchCourses = async () => {
      try {
        const response = await fetch(`http://localhost:8000/api/v1/courses/student/${user?.id}`, {
          headers: { 'Authorization': `Bearer ${token}` }
        });
        if (response.ok) {
          const data = await response.json();
          setCourses(data.courses || []);
        }
      } catch (error) {
        console.error('Erreur lors du chargement des cours:', error);
      } finally {
        setLoading(false);
      }
    };

    if (user && token) {
      fetchCourses();
    }
  }, [user, token]);

  const fetchModules = async (courseId: number) => {
    try {
      const response = await fetch(`http://localhost:8000/api/v1/courses/${courseId}/modules`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (response.ok) {
        const data = await response.json();
        setModules(data.modules || []);
      }
    } catch (error) {
      console.error('Erreur lors du chargement des modules:', error);
    }
  };

  const handleCourseSelect = (course: Course) => {
    setSelectedCourse(course);
    fetchModules(course.id);
    setShowCourseDetails(true);
  };

  const handleModuleComplete = async (moduleId: number) => {
    try {
      const response = await fetch(`http://localhost:8000/api/v1/modules/${moduleId}/complete`, {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (response.ok) {
        // Mettre à jour l'état local
        setModules(prev => prev.map(m => 
          m.id === moduleId ? { ...m, is_completed: true } : m
        ));
        // Mettre à jour la progression du cours
        setSelectedCourse(prev => prev ? {
          ...prev,
          completed_modules: prev.completed_modules + 1,
          progress: ((prev.completed_modules + 1) / prev.modules_count) * 100
        } : null);
      }
    } catch (error) {
      console.error('Erreur lors de la complétion du module:', error);
    }
  };

  const getDifficultyColor = (difficulty: string) => {
    switch (difficulty) {
      case 'beginner': return 'bg-green-100 text-green-800';
      case 'intermediate': return 'bg-yellow-100 text-yellow-800';
      case 'advanced': return 'bg-red-100 text-red-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const getContentTypeIcon = (type: string) => {
    switch (type) {
      case 'video': return <Video className="w-4 h-4" />;
      case 'text': return <FileText className="w-4 h-4" />;
      case 'quiz': return <Book className="w-4 h-4" />;
      case 'assignment': return <Award className="w-4 h-4" />;
      default: return <FileText className="w-4 h-4" />;
    }
  };

  const getResourceIcon = (type: string) => {
    switch (type) {
      case 'pdf': return <FileText className="w-4 h-4" />;
      case 'video': return <Video className="w-4 h-4" />;
      case 'audio': return <Headphones className="w-4 h-4" />;
      case 'link': return <Eye className="w-4 h-4" />;
      default: return <FileText className="w-4 h-4" />;
    }
  };

  const filteredCourses = courses.filter(course => {
    const matchesSearch = course.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         course.description.toLowerCase().includes(searchTerm.toLowerCase());
    
    if (filter === 'enrolled') return matchesSearch && course.progress > 0;
    if (filter === 'completed') return matchesSearch && course.progress === 100;
    if (filter === 'in_progress') return matchesSearch && course.progress > 0 && course.progress < 100;
    
    return matchesSearch;
  });

  const formatDuration = (minutes: number) => {
    const hours = Math.floor(minutes / 60);
    const mins = minutes % 60;
    return hours > 0 ? `${hours}h ${mins}min` : `${mins}min`;
  };

  if (loading) {
    return (
      <div className="flex min-h-screen bg-gray-50">
        <Sidebar />
        <div className="flex-1 flex items-center justify-center ml-64">
          <div className="text-blue-600 animate-pulse text-xl font-bold">
            Chargement des cours...
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="flex min-h-screen bg-gray-50">
      <Sidebar />
      <div className="flex-1 ml-64 overflow-y-auto">
        <div className="max-w-7xl mx-auto px-4 py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Mes Cours</h1>
          <p className="text-gray-600">Gérez vos cours et suivez votre progression</p>
        </div>

        {/* Filtres et recherche */}
        <div className="mb-6 flex flex-col sm:flex-row gap-4">
          <div className="flex-1">
            <div className="relative">
              <BookOpen className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
              <input
                type="text"
                placeholder="Rechercher un cours..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
          </div>
          <div className="flex gap-2">
            {['all', 'enrolled', 'in_progress', 'completed'].map((filterType) => (
              <button
                key={filterType}
                onClick={() => setFilter(filterType as any)}
                className={`px-4 py-2 rounded-lg font-medium transition-colors ${
                  filter === filterType
                    ? 'bg-blue-500 text-white'
                    : 'bg-white text-gray-700 hover:bg-gray-50'
                }`}
              >
                {filterType === 'all' && 'Tous'}
                {filterType === 'enrolled' && 'Inscrits'}
                {filterType === 'in_progress' && 'En cours'}
                {filterType === 'completed' && 'Terminés'}
              </button>
            ))}
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Liste des cours */}
          <div className="lg:col-span-2">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {filteredCourses.map((course) => (
                <Card key={course.id} className="hover:shadow-lg transition-shadow cursor-pointer">
                  <div onClick={() => handleCourseSelect(course)}>
                    {/* Thumbnail */}
                    <div className="relative h-48 bg-gradient-to-br from-blue-500 to-purple-600 rounded-t-lg flex items-center justify-center">
                      <BookOpen className="w-16 h-16 text-white opacity-80" />
                      {course.progress > 0 && (
                        <div className="absolute top-2 right-2 bg-white bg-opacity-90 rounded-full px-2 py-1">
                          <span className="text-sm font-semibold text-blue-600">
                            {Math.round(course.progress)}%
                          </span>
                        </div>
                      )}
                    </div>

                    <div className="p-6">
                      {/* Header */}
                      <div className="flex items-start justify-between mb-3">
                        <div>
                          <h3 className="font-bold text-lg text-gray-900 mb-1">{course.title}</h3>
                          <p className="text-sm text-gray-600 line-clamp-2">{course.description}</p>
                        </div>
                        <div className="flex items-center space-x-1">
                          <Star className="w-4 h-4 text-yellow-400 fill-current" />
                          <span className="text-sm font-medium">{course.rating}</span>
                        </div>
                      </div>

                      {/* Stats */}
                      <div className="flex items-center justify-between text-sm text-gray-500 mb-4">
                        <div className="flex items-center space-x-1">
                          <Clock className="w-4 h-4" />
                          <span>{course.duration}h</span>
                        </div>
                        <div className="flex items-center space-x-1">
                          <Users className="w-4 h-4" />
                          <span>{course.enrolled_students}</span>
                        </div>
                        <div className="flex items-center space-x-1">
                          <BookOpen className="w-4 h-4" />
                          <span>{course.modules_count} modules</span>
                        </div>
                      </div>

                      {/* Progress bar */}
                      {course.progress > 0 && (
                        <div className="mb-4">
                          <div className="flex justify-between text-sm mb-1">
                            <span className="text-gray-600">Progression</span>
                            <span className="text-blue-600 font-medium">{Math.round(course.progress)}%</span>
                          </div>
                          <div className="w-full bg-gray-200 rounded-full h-2">
                            <div
                              className="bg-blue-500 h-2 rounded-full transition-all duration-300"
                              style={{ width: `${course.progress}%` }}
                            />
                          </div>
                        </div>
                      )}

                      {/* Footer */}
                      <div className="flex items-center justify-between">
                        <div className="flex items-center space-x-2">
                          <div className="w-8 h-8 bg-gray-100 rounded-full flex items-center justify-center">
                            <span className="text-sm font-semibold text-gray-600">
                              {course.instructor_avatar}
                            </span>
                          </div>
                          <span className="text-sm text-gray-600">{course.instructor}</span>
                        </div>
                        <span className={`px-2 py-1 rounded-full text-xs font-medium ${getDifficultyColor(course.difficulty)}`}>
                          {course.difficulty}
                        </span>
                      </div>
                    </div>
                  </div>
                </Card>
              ))}
            </div>

            {filteredCourses.length === 0 && (
              <div className="text-center py-12">
                <BookOpen className="w-16 h-16 text-gray-400 mx-auto mb-4" />
                <h3 className="text-lg font-semibold text-gray-600 mb-2">Aucun cours trouvé</h3>
                <p className="text-gray-500">Essayez de modifier vos filtres ou recherchez un autre cours</p>
              </div>
            )}
          </div>

          {/* Détails du cours sélectionné */}
          {selectedCourse && showCourseDetails && (
            <div className="lg:col-span-1">
              <Card>
                <div className="p-6">
                  <div className="flex items-center justify-between mb-4">
                    <h2 className="text-xl font-bold text-gray-900">Détails du cours</h2>
                    <button
                      onClick={() => setShowCourseDetails(false)}
                      className="text-gray-400 hover:text-gray-600"
                    >
                      ×
                    </button>
                  </div>

                  <div className="mb-6">
                    <h3 className="font-semibold text-gray-900 mb-2">{selectedCourse.title}</h3>
                    <p className="text-sm text-gray-600 mb-4">{selectedCourse.description}</p>

                    {/* Progress */}
                    <div className="mb-4">
                      <div className="flex justify-between text-sm mb-1">
                        <span className="text-gray-600">Progression globale</span>
                        <span className="text-blue-600 font-medium">
                          {selectedCourse.completed_modules}/{selectedCourse.modules_count} modules
                        </span>
                      </div>
                      <div className="w-full bg-gray-200 rounded-full h-3">
                        <div
                          className="bg-blue-500 h-3 rounded-full transition-all duration-300"
                          style={{ width: `${selectedCourse.progress}%` }}
                        />
                      </div>
                    </div>

                    {/* Stats */}
                    <div className="grid grid-cols-2 gap-4 mb-6">
                      <div className="text-center p-3 bg-blue-50 rounded-lg">
                        <Clock className="w-6 h-6 text-blue-600 mx-auto mb-1" />
                        <div className="text-sm font-medium text-blue-600">{selectedCourse.duration}h</div>
                        <div className="text-xs text-gray-500">Durée totale</div>
                      </div>
                      <div className="text-center p-3 bg-green-50 rounded-lg">
                        <CheckCircle className="w-6 h-6 text-green-600 mx-auto mb-1" />
                        <div className="text-sm font-medium text-green-600">{selectedCourse.completed_modules}</div>
                        <div className="text-xs text-gray-500">Modules terminés</div>
                      </div>
                    </div>
                  </div>

                  {/* Modules */}
                  <div>
                    <h4 className="font-semibold text-gray-900 mb-3">Modules du cours</h4>
                    <div className="space-y-3">
                      {modules.map((module, index) => (
                        <div
                          key={module.id}
                          className={`p-3 rounded-lg border ${
                            module.is_completed
                              ? 'bg-green-50 border-green-200'
                              : module.is_locked
                              ? 'bg-gray-50 border-gray-200'
                              : 'bg-white border-gray-200 hover:border-blue-300'
                          }`}
                        >
                          <div className="flex items-center justify-between">
                            <div className="flex items-center space-x-3">
                              <div className={`w-8 h-8 rounded-full flex items-center justify-center ${
                                module.is_completed
                                  ? 'bg-green-500 text-white'
                                  : module.is_locked
                                  ? 'bg-gray-300 text-gray-500'
                                  : 'bg-blue-500 text-white'
                              }`}>
                                {module.is_completed ? (
                                  <CheckCircle className="w-4 h-4" />
                                ) : (
                                  <span className="text-sm font-medium">{index + 1}</span>
                                )}
                              </div>
                              <div className="flex-1">
                                <h5 className="font-medium text-gray-900">{module.title}</h5>
                                <div className="flex items-center space-x-2 text-sm text-gray-500">
                                  {getContentTypeIcon(module.content_type)}
                                  <span>{formatDuration(module.duration)}</span>
                                </div>
                              </div>
                            </div>
                            {!module.is_locked && !module.is_completed && (
                              <Button
                                size="sm"
                                onClick={() => handleModuleComplete(module.id)}
                                className="bg-blue-500 hover:bg-blue-600"
                              >
                                Terminer
                              </Button>
                            )}
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              </Card>
            </div>
          )}
        </div>
        </div>
      </div>
    </div>
  );
};

export default CoursesPage; 