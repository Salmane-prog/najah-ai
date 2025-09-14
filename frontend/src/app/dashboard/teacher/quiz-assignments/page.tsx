'use client';

import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Badge } from '@/components/ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { 
  Calendar, 
  Users, 
  BookOpen, 
  Clock, 
  CheckCircle, 
  AlertTriangle,
  Plus,
  Search,
  Filter
} from 'lucide-react';

interface Quiz {
  id: number;
  title: string;
  subject: string;
  difficulty: string;
  time_limit: number;
  total_questions: number;
}

interface Student {
  id: number;
  username: string;
  email: string;
}

interface QuizAssignment {
  id: number;
  quiz_id: number;
  quiz_title: string;
  student_id: number;
  student_name: string;
  due_date: string;
  status: string;
  assigned_at: string;
  student_status: string;
  score?: number;
  completed_at?: string;
}

const QuizAssignmentsPage = () => {
  const [assignments, setAssignments] = useState<QuizAssignment[]>([]);
  const [quizzes, setQuizzes] = useState<Quiz[]>([]);
  const [students, setStudents] = useState<Student[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterStatus, setFilterStatus] = useState('all');
  const [showAssignForm, setShowAssignForm] = useState(false);
  
  // Form state
  const [selectedQuiz, setSelectedQuiz] = useState('');
  const [selectedStudents, setSelectedStudents] = useState<number[]>([]);
  const [dueDate, setDueDate] = useState('');

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      // Récupérer les assignations du professeur
      const assignmentsResponse = await fetch('/api/v1/quiz_assignments/teacher/1/assignments');
      if (assignmentsResponse.ok) {
        const data = await assignmentsResponse.json();
        setAssignments(data.assignments || []);
      }

      // Récupérer la liste des quiz disponibles
      const quizzesResponse = await fetch('/api/v1/quizzes');
      if (quizzesResponse.ok) {
        const quizzesData = await quizzesResponse.json();
        setQuizzes(quizzesData || []);
      }

      // Récupérer la liste des étudiants
      const studentsResponse = await fetch('/api/v1/users/students');
      if (studentsResponse.ok) {
        const studentsData = await studentsResponse.json();
        setStudents(studentsData || []);
      }
    } catch (error) {
      console.error('Erreur lors du chargement des données:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleAssignQuiz = async () => {
    if (!selectedQuiz || selectedStudents.length === 0) {
      alert('Veuillez sélectionner un quiz et au moins un étudiant');
      return;
    }

    try {
      const response = await fetch('/api/v1/quiz_assignments/assign', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          quiz_id: parseInt(selectedQuiz),
          student_ids: selectedStudents,
          due_date: dueDate || null,
          class_id: null
        }),
      });

      if (response.ok) {
        const result = await response.json();
        alert(result.message);
        setShowAssignForm(false);
        resetForm();
        fetchData(); // Recharger les données
      } else {
        const error = await response.json();
        alert(`Erreur: ${error.detail}`);
      }
    } catch (error) {
      console.error('Erreur lors de l\'assignation:', error);
      alert('Erreur lors de l\'assignation');
    }
  };

  const resetForm = () => {
    setSelectedQuiz('');
    setSelectedStudents([]);
    setDueDate('');
  };

  const getStatusBadge = (status: string) => {
    switch (status) {
      case 'assigned':
        return <Badge variant="secondary">Assigné</Badge>;
      case 'in_progress':
        return <Badge variant="default">En cours</Badge>;
      case 'completed':
        return <Badge variant="success">Terminé</Badge>;
      case 'overdue':
        return <Badge variant="destructive">En retard</Badge>;
      default:
        return <Badge variant="outline">{status}</Badge>;
    }
  };

  const getStudentStatusBadge = (status: string) => {
    switch (status) {
      case 'assigné':
        return <Badge variant="secondary">À faire</Badge>;
      case 'en cours':
        return <Badge variant="default">En cours</Badge>;
      case 'fait':
        return <Badge variant="success">Terminé</Badge>;
      default:
        return <Badge variant="outline">{status}</Badge>;
    }
  };

  const filteredAssignments = assignments.filter(assignment => {
    const matchesSearch = assignment.quiz_title.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         assignment.student_name.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesStatus = filterStatus === 'all' || assignment.student_status === filterStatus;
    return matchesSearch && matchesStatus;
  });

  const pendingAssignments = assignments.filter(a => a.student_status === 'assigné');
  const completedAssignments = assignments.filter(a => a.student_status === 'fait');
  const overdueAssignments = assignments.filter(a => {
    if (!a.due_date) return false;
    return new Date(a.due_date) < new Date() && a.student_status !== 'fait';
  });

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-gray-900"></div>
      </div>
    );
  }

  return (
    <div className="container mx-auto p-6 space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Gestion des Quiz Assignés</h1>
          <p className="text-gray-600">Assignez et suivez les quiz de vos étudiants</p>
        </div>
        <Button onClick={() => setShowAssignForm(true)} className="flex items-center gap-2">
          <Plus className="h-4 w-4" />
          Assigner un Quiz
        </Button>
      </div>

      {/* Statistiques rapides */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card>
          <CardContent className="p-4">
            <div className="flex items-center space-x-2">
              <BookOpen className="h-8 w-8 text-blue-600" />
              <div>
                <p className="text-sm font-medium text-gray-600">Total Assignations</p>
                <p className="text-2xl font-bold text-gray-900">{assignments.length}</p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-4">
            <div className="flex items-center space-x-2">
              <Clock className="h-8 w-8 text-yellow-600" />
              <div>
                <p className="text-sm font-medium text-gray-600">En Attente</p>
                <p className="text-2xl font-bold text-yellow-600">{pendingAssignments.length}</p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-4">
            <div className="flex items-center space-x-2">
              <CheckCircle className="h-8 w-8 text-green-600" />
              <div>
                <p className="text-sm font-medium text-gray-600">Terminés</p>
                <p className="text-2xl font-bold text-green-600">{completedAssignments.length}</p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-4">
            <div className="flex items-center space-x-2">
              <AlertTriangle className="h-8 w-8 text-red-600" />
              <div>
                <p className="text-sm font-medium text-gray-600">En Retard</p>
                <p className="text-2xl font-bold text-red-600">{overdueAssignments.length}</p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Formulaire d'assignation */}
      {showAssignForm && (
        <Card>
          <CardHeader>
            <CardTitle>Assigner un Quiz</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <Label htmlFor="quiz">Quiz</Label>
                <Select value={selectedQuiz} onValueChange={setSelectedQuiz}>
                  <SelectTrigger>
                    <SelectValue placeholder="Sélectionner un quiz" />
                  </SelectTrigger>
                  <SelectContent>
                    {quizzes.map((quiz) => (
                      <SelectItem key={quiz.id} value={quiz.id.toString()}>
                        {quiz.title} ({quiz.subject})
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              <div>
                <Label htmlFor="dueDate">Date d'échéance (optionnel)</Label>
                <Input
                  type="datetime-local"
                  value={dueDate}
                  onChange={(e) => setDueDate(e.target.value)}
                />
              </div>
            </div>

            <div>
              <Label>Étudiants</Label>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-2 mt-2 max-h-40 overflow-y-auto border rounded-md p-2">
                {students.map((student) => (
                  <label key={student.id} className="flex items-center space-x-2">
                    <input
                      type="checkbox"
                      checked={selectedStudents.includes(student.id)}
                      onChange={(e) => {
                        if (e.target.checked) {
                          setSelectedStudents([...selectedStudents, student.id]);
                        } else {
                          setSelectedStudents(selectedStudents.filter(id => id !== student.id));
                        }
                      }}
                    />
                    <span className="text-sm">{student.username}</span>
                  </label>
                ))}
              </div>
            </div>

            <div className="flex justify-end space-x-2">
              <Button variant="outline" onClick={() => setShowAssignForm(false)}>
                Annuler
              </Button>
              <Button onClick={handleAssignQuiz}>
                Assigner
              </Button>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Filtres et recherche */}
      <Card>
        <CardContent className="p-4">
          <div className="flex flex-col md:flex-row gap-4">
            <div className="flex-1">
              <Label htmlFor="search">Rechercher</Label>
              <div className="relative">
                <Search className="absolute left-3 top-3 h-4 w-4 text-gray-400" />
                <Input
                  id="search"
                  placeholder="Rechercher par quiz ou étudiant..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="pl-10"
                />
              </div>
            </div>

            <div>
              <Label htmlFor="status">Statut</Label>
              <Select value={filterStatus} onValueChange={setFilterStatus}>
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">Tous</SelectItem>
                  <SelectItem value="assigné">À faire</SelectItem>
                  <SelectItem value="en cours">En cours</SelectItem>
                  <SelectItem value="fait">Terminé</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Liste des assignations */}
      <Tabs defaultValue="all" className="w-full">
        <TabsList className="grid w-full grid-cols-4">
          <TabsTrigger value="all">Toutes ({assignments.length})</TabsTrigger>
          <TabsTrigger value="pending">En Attente ({pendingAssignments.length})</TabsTrigger>
          <TabsTrigger value="completed">Terminés ({completedAssignments.length})</TabsTrigger>
          <TabsTrigger value="overdue">En Retard ({overdueAssignments.length})</TabsTrigger>
        </TabsList>

        <TabsContent value="all" className="space-y-4">
          <AssignmentsList assignments={filteredAssignments} />
        </TabsContent>

        <TabsContent value="pending" className="space-y-4">
          <AssignmentsList assignments={pendingAssignments} />
        </TabsContent>

        <TabsContent value="completed" className="space-y-4">
          <AssignmentsList assignments={completedAssignments} />
        </TabsContent>

        <TabsContent value="overdue" className="space-y-4">
          <AssignmentsList assignments={overdueAssignments} />
        </TabsContent>
      </Tabs>
    </div>
  );
};

// Composant pour afficher la liste des assignations
const AssignmentsList = ({ assignments }: { assignments: QuizAssignment[] }) => {
  if (assignments.length === 0) {
    return (
      <Card>
        <CardContent className="p-8 text-center">
          <BookOpen className="h-12 w-12 text-gray-400 mx-auto mb-4" />
          <p className="text-gray-500">Aucune assignation trouvée</p>
        </CardContent>
      </Card>
    );
  }

  return (
    <div className="space-y-4">
      {assignments.map((assignment) => (
        <Card key={assignment.id}>
          <CardContent className="p-4">
            <div className="flex items-center justify-between">
              <div className="flex-1">
                <div className="flex items-center space-x-3 mb-2">
                  <h3 className="font-semibold text-lg">{assignment.quiz_title}</h3>
                  {getStatusBadge(assignment.status)}
                  {getStudentStatusBadge(assignment.student_status)}
                </div>
                
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm text-gray-600">
                  <div>
                    <span className="font-medium">Étudiant:</span> {assignment.student_name}
                  </div>
                  <div>
                    <span className="font-medium">Assigné le:</span> {new Date(assignment.assigned_at).toLocaleDateString()}
                  </div>
                  {assignment.due_date && (
                    <div>
                      <span className="font-medium">Échéance:</span> {new Date(assignment.due_date).toLocaleDateString()}
                    </div>
                  )}
                  {assignment.score !== undefined && (
                    <div>
                      <span className="font-medium">Score:</span> {assignment.score}/100
                    </div>
                  )}
                </div>

                {assignment.completed_at && (
                  <div className="mt-2 text-sm text-gray-500">
                    Terminé le: {new Date(assignment.completed_at).toLocaleDateString()}
                  </div>
                )}
              </div>

              <div className="flex space-x-2">
                {assignment.student_status === 'fait' && (
                  <Button variant="outline" size="sm">
                    Voir les détails
                  </Button>
                )}
                <Button variant="outline" size="sm">
                  Modifier
                </Button>
              </div>
            </div>
          </CardContent>
        </Card>
      ))}
    </div>
  );
};

export default QuizAssignmentsPage;










