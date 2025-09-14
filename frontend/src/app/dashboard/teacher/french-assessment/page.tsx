'use client';

import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { 
  BookOpen, 
  Users, 
  Target, 
  TrendingUp, 
  CheckCircle,
  AlertTriangle,
  Loader2,
  Play,
  Eye,
  BarChart3,
  RefreshCw,
  Download
} from 'lucide-react';

interface Student {
  id: number;
  email: string;
  first_name?: string;
  last_name?: string;
  role: string;
}

interface FrenchAssessment {
  id: number;
  student_id: number;
  test_type: string;
  status: string;
  started_at: string;
  completed_at?: string;
  final_score?: number;
  student_name: string;
}

const FrenchAssessmentPage: React.FC = () => {
  const [students, setStudents] = useState<Student[]>([]);
  const [selectedStudent, setSelectedStudent] = useState<number | null>(null);
  const [assessments, setAssessments] = useState<FrenchAssessment[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [isStartingTest, setIsStartingTest] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

  useEffect(() => {
    loadStudents();
    loadAssessments();
  }, []);

  const loadStudents = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await fetch(`${API_BASE_URL}/api/v1/students/`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (response.ok) {
        const data = await response.json();
        setStudents(data.students || []);
      }
    } catch (error) {
      console.error('Erreur lors du chargement des étudiants:', error);
    }
  };

  const loadAssessments = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await fetch(`${API_BASE_URL}/api/v1/french/initial-assessment/teacher/overview`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (response.ok) {
        const data = await response.json();
        setAssessments(data.assessments || []);
      }
    } catch (error) {
      console.error('Erreur lors du chargement des évaluations:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const startAssessment = async () => {
    if (!selectedStudent) return;

    setIsStartingTest(true);
    setError(null);

    try {
      const token = localStorage.getItem('token');
      const response = await fetch(`${API_BASE_URL}/api/v1/french/initial-assessment/start`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ student_id: selectedStudent })
      });

      if (response.ok) {
        const data = await response.json();
        console.log('Test démarré avec succès:', data);
        
        // Recharger les évaluations
        await loadAssessments();
        
        // Réinitialiser la sélection
        setSelectedStudent(null);
      } else {
        const errorData = await response.json();
        setError(errorData.detail || 'Erreur lors du démarrage du test');
      }
    } catch (error) {
      setError('Erreur de connexion au serveur');
    } finally {
      setIsStartingTest(false);
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'in_progress': return 'bg-blue-100 text-blue-800';
      case 'completed': return 'bg-green-100 text-green-800';
      case 'paused': return 'bg-yellow-100 text-yellow-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const getStatusLabel = (status: string) => {
    switch (status) {
      case 'in_progress': return 'En cours';
      case 'completed': return 'Terminé';
      case 'paused': return 'En pause';
      default: return 'Inconnu';
    }
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('fr-FR', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const getStudentName = (studentId: number) => {
    const student = students.find(s => s.id === studentId);
    if (student) {
      return `${student.first_name || ''} ${student.last_name || ''}`.trim() || student.email;
    }
    return 'Étudiant inconnu';
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <Loader2 className="h-8 w-8 animate-spin mr-3" />
        <span>Chargement...</span>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8">
      {/* En-tête de la page */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">
          Gestion des Évaluations Françaises
        </h1>
        <p className="text-gray-600">
          Lancez et suivez les évaluations initiales françaises de vos étudiants
        </p>
      </div>

      {/* Statistiques */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <Card>
          <CardContent className="p-6 text-center">
            <Users className="w-8 h-8 text-blue-500 mx-auto mb-2" />
            <div className="text-2xl font-bold text-gray-900">{students.length}</div>
            <div className="text-sm text-gray-500">Total étudiants</div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-6 text-center">
            <BookOpen className="w-8 h-8 text-green-500 mx-auto mb-2" />
            <div className="text-2xl font-bold text-gray-900">
              {assessments.filter(a => a.status === 'completed').length}
            </div>
            <div className="text-sm text-gray-500">Tests terminés</div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-6 text-center">
            <Target className="w-8 h-8 text-yellow-500 mx-auto mb-2" />
            <div className="text-2xl font-bold text-gray-900">
              {assessments.filter(a => a.status === 'in_progress').length}
            </div>
            <div className="text-sm text-gray-500">Tests en cours</div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-6 text-center">
            <BarChart3 className="w-8 h-8 text-purple-500 mx-auto mb-2" />
            <div className="text-2xl font-bold text-gray-900">
              {assessments.length > 0 
                ? Math.round(assessments.filter(a => a.status === 'completed').length / assessments.length * 100)
                : 0
              }%
            </div>
            <div className="text-sm text-gray-500">Taux de completion</div>
          </CardContent>
        </Card>
      </div>

      {/* Lancement d'évaluation */}
      <Card className="mb-8">
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Play className="h-6 w-6 text-blue-600" />
            Lancer une Évaluation
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div>
              <Label htmlFor="student-select">Sélectionner un étudiant</Label>
              <Select value={selectedStudent?.toString() || ''} onValueChange={(value) => setSelectedStudent(Number(value))}>
                <SelectTrigger>
                  <SelectValue placeholder="Choisir un étudiant" />
                </SelectTrigger>
                <SelectContent>
                  {students.map((student) => (
                    <SelectItem key={student.id} value={student.id.toString()}>
                      {`${student.first_name || ''} ${student.last_name || ''}`.trim() || student.email}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>

            {error && (
              <Alert variant="destructive">
                <AlertTriangle className="h-4 w-4" />
                <AlertDescription>{error}</AlertDescription>
              </Alert>
            )}

            <Button 
              onClick={startAssessment}
              disabled={!selectedStudent || isStartingTest}
              className="w-full sm:w-auto"
            >
              {isStartingTest ? (
                <>
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                  Démarrage...
                </>
              ) : (
                <>
                  <Play className="mr-2 h-4 w-4" />
                  Lancer l'Évaluation
                </>
              )}
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* Liste des évaluations */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Eye className="h-6 w-6 text-green-600" />
            Suivi des Évaluations
          </CardTitle>
        </CardHeader>
        <CardContent>
          {assessments.length === 0 ? (
            <div className="text-center py-8">
              <BookOpen className="h-16 w-16 text-gray-400 mx-auto mb-4" />
              <h3 className="text-lg font-semibold mb-2">Aucune évaluation</h3>
              <p className="text-gray-600">
                Aucune évaluation française n'a encore été lancée.
              </p>
            </div>
          ) : (
            <div className="space-y-4">
              {assessments.map((assessment) => (
                <Card key={assessment.id} className="hover:shadow-md transition-shadow">
                  <CardContent className="p-6">
                    <div className="flex items-center justify-between">
                      <div className="flex-1">
                        <div className="flex items-center gap-3 mb-2">
                          <h3 className="font-semibold text-lg">
                            {getStudentName(assessment.student_id)}
                          </h3>
                          <Badge className={getStatusColor(assessment.status)}>
                            {getStatusLabel(assessment.status)}
                          </Badge>
                        </div>
                        
                        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm text-gray-600">
                          <div>
                            <span className="font-medium">Type:</span> {assessment.test_type}
                          </div>
                          <div>
                            <span className="font-medium">Démarré:</span> {formatDate(assessment.started_at)}
                          </div>
                          {assessment.completed_at && (
                            <div>
                              <span className="font-medium">Terminé:</span> {formatDate(assessment.completed_at)}
                            </div>
                          )}
                        </div>

                        {assessment.final_score !== undefined && (
                          <div className="mt-3">
                            <span className="font-medium text-green-600">
                              Score final: {assessment.final_score}%
                            </span>
                          </div>
                        )}
                      </div>

                      <div className="flex gap-2">
                        <Button variant="outline" size="sm">
                          <Eye className="h-4 w-4 mr-2" />
                          Détails
                        </Button>
                        {assessment.status === 'in_progress' && (
                          <Button variant="outline" size="sm">
                            <Target className="h-4 w-4 mr-2" />
                            Suivre
                          </Button>
                        )}
                      </div>
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          )}
        </CardContent>
      </Card>

      {/* Actions rapides */}
      <Card className="mt-8">
        <CardHeader>
          <CardTitle>Actions Rapides</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex flex-wrap gap-4">
            <Button variant="outline" onClick={loadAssessments}>
              <RefreshCw className="h-4 w-4 mr-2" />
              Actualiser
            </Button>
            <Button variant="outline">
              <Download className="h-4 w-4 mr-2" />
              Exporter les Résultats
            </Button>
            <Button variant="outline">
              <BarChart3 className="h-4 w-4 mr-2" />
              Voir les Statistiques
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default FrenchAssessmentPage;
