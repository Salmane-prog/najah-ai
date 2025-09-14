'use client';

import React, { useState, useEffect } from 'react';
import { useParams, useRouter } from 'next/navigation';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Badge } from '@/components/ui/badge';
import { 
  ArrowLeft, 
  Users, 
  Calendar, 
  Target, 
  CheckCircle,
  BookOpen,
  Clock
} from 'lucide-react';

interface Student {
  id: number;
  name: string;
  email: string;
  class_name?: string;
}

interface Test {
  id: number;
  title: string;
  subject: string;
  description: string;
  total_questions: number;
  estimated_duration: number;
}

const AssignTestPage = () => {
  const params = useParams();
  const router = useRouter();
  const testId = params.id;
  
  const [test, setTest] = useState<Test | null>(null);
  const [students, setStudents] = useState<Student[]>([]);
  const [selectedStudents, setSelectedStudents] = useState<number[]>([]);
  const [dueDate, setDueDate] = useState('');
  const [loading, setLoading] = useState(true);
  const [assigning, setAssigning] = useState(false);

  useEffect(() => {
    fetchTestAndStudents();
  }, [testId]);

  const fetchTestAndStudents = async () => {
    try {
      // Récupérer les détails du test
      const testResponse = await fetch(`/api/v1/adaptive-evaluation/tests/${testId}`);
      if (testResponse.ok) {
        const testData = await testResponse.json();
        setTest(testData);
      }

      // Récupérer la liste des étudiants
      const studentsResponse = await fetch('/api/v1/users/students');
      if (studentsResponse.ok) {
        const studentsData = await studentsResponse.json();
        setStudents(studentsData);
      }
    } catch (error) {
      console.error('Erreur lors du chargement:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleStudentSelection = (studentId: number) => {
    setSelectedStudents(prev => 
      prev.includes(studentId) 
        ? prev.filter(id => id !== studentId)
        : [...prev, studentId]
    );
  };

  const handleAssignTest = async () => {
    if (selectedStudents.length === 0) {
      alert('Veuillez sélectionner au moins un étudiant');
      return;
    }

    if (!dueDate) {
      alert('Veuillez définir une date d\'échéance');
      return;
    }

    setAssigning(true);

    try {
      const assignmentData = {
        quiz_id: testId,
        student_ids: selectedStudents,
        due_date: dueDate,
        assigned_by: 1 // ID du professeur connecté
      };

      const response = await fetch('/api/v1/quiz_assignments/assign', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(assignmentData)
      });

      if (response.ok) {
        const result = await response.json();
        alert(`✅ Test assigné avec succès à ${selectedStudents.length} étudiant(s) !`);
        
        // Rediriger vers la liste des tests
        router.push('/dashboard/teacher/adaptive-evaluation');
      } else {
        const errorData = await response.json();
        alert(`❌ Erreur lors de l'assignation: ${errorData.detail || 'Erreur inconnue'}`);
      }
    } catch (error) {
      console.error('Erreur lors de l\'assignation:', error);
      alert('❌ Erreur lors de l\'assignation. Vérifiez votre connexion.');
    } finally {
      setAssigning(false);
    }
  };

  const selectAllStudents = () => {
    setSelectedStudents(students.map(s => s.id));
  };

  const deselectAllStudents = () => {
    setSelectedStudents([]);
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-gray-900"></div>
      </div>
    );
  }

  if (!test) {
    return (
      <div className="container mx-auto p-6">
        <Card>
          <CardContent className="p-8 text-center">
            <BookOpen className="h-12 w-12 text-gray-400 mx-auto mb-4" />
            <p className="text-gray-500">Test non trouvé</p>
            <Button onClick={() => router.back()} className="mt-4">
              <ArrowLeft className="h-4 w-4 mr-2" />
              Retour
            </Button>
          </CardContent>
        </Card>
      </div>
    );
  }

  return (
    <div className="container mx-auto p-6 space-y-6">
      {/* Header */}
      <div className="flex items-center space-x-4">
        <Button onClick={() => router.back()} variant="outline">
          <ArrowLeft className="h-4 w-4 mr-2" />
          Retour
        </Button>
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Assigner le Test</h1>
          <p className="text-gray-600">Sélectionnez les étudiants et définissez les paramètres d'assignation</p>
        </div>
      </div>

      {/* Détails du test */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <BookOpen className="h-5 w-5" />
            <span>Détails du Test</span>
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="flex items-center space-x-2">
              <BookOpen className="h-4 w-4" />
              <span><span className="font-medium">Titre:</span> {test.title}</span>
            </div>
            
            <div className="flex items-center space-x-2">
              <Target className="h-4 w-4" />
              <span><span className="font-medium">Matière:</span> {test.subject}</span>
            </div>
            
            <div className="flex items-center space-x-2">
              <Clock className="h-4 w-4" />
              <span><span className="font-medium">Durée:</span> {test.estimated_duration} min</span>
            </div>
          </div>
          
          <p className="text-gray-600 mt-3">{test.description}</p>
          
          <div className="mt-4">
            <Badge variant="outline">{test.total_questions} questions</Badge>
          </div>
        </CardContent>
      </Card>

      {/* Configuration de l'assignation */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <Calendar className="h-5 w-5" />
            <span>Configuration de l'Assignation</span>
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div>
            <Label htmlFor="dueDate">Date d'échéance</Label>
            <Input
              id="dueDate"
              type="date"
              value={dueDate}
              onChange={(e) => setDueDate(e.target.value)}
              min={new Date().toISOString().split('T')[0]}
              className="mt-1"
            />
          </div>
        </CardContent>
      </Card>

      {/* Sélection des étudiants */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center justify-between">
            <div className="flex items-center space-x-2">
              <Users className="h-5 w-5" />
              <span>Sélection des Étudiants</span>
            </div>
            <div className="flex space-x-2">
              <Button onClick={selectAllStudents} variant="outline" size="sm">
                Tout sélectionner
              </Button>
              <Button onClick={deselectAllStudents} variant="outline" size="sm">
                Tout désélectionner
              </Button>
            </div>
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3 max-h-96 overflow-y-auto">
            {students.map((student) => (
              <div
                key={student.id}
                className={`p-3 border rounded-lg cursor-pointer transition-colors ${
                  selectedStudents.includes(student.id)
                    ? 'border-blue-500 bg-blue-50'
                    : 'border-gray-200 hover:bg-gray-50'
                }`}
                onClick={() => handleStudentSelection(student.id)}
              >
                <div className="flex items-center space-x-2">
                  <input
                    type="checkbox"
                    checked={selectedStudents.includes(student.id)}
                    onChange={() => handleStudentSelection(student.id)}
                    className="h-4 w-4 text-blue-600"
                  />
                  <div className="flex-1">
                    <p className="font-medium">{student.name}</p>
                    <p className="text-sm text-gray-600">{student.email}</p>
                    {student.class_name && (
                      <p className="text-xs text-gray-500">{student.class_name}</p>
                    )}
                  </div>
                </div>
              </div>
            ))}
          </div>
          
          <div className="mt-4 text-sm text-gray-600">
            {selectedStudents.length > 0 ? (
              <span className="text-green-600">
                ✅ {selectedStudents.length} étudiant(s) sélectionné(s)
              </span>
            ) : (
              <span className="text-gray-500">
                Aucun étudiant sélectionné
              </span>
            )}
          </div>
        </CardContent>
      </Card>

      {/* Actions */}
      <div className="flex justify-end space-x-4">
        <Button onClick={() => router.back()} variant="outline">
          Annuler
        </Button>
        <Button 
          onClick={handleAssignTest}
          disabled={selectedStudents.length === 0 || !dueDate || assigning}
          className="flex items-center space-x-2"
        >
          {assigning ? (
            <>
              <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
              <span>Assignation en cours...</span>
            </>
          ) : (
            <>
              <CheckCircle className="h-4 w-4" />
              <span>Assigner le Test ({selectedStudents.length} étudiant(s))</span>
            </>
          )}
        </Button>
      </div>
    </div>
  );
};

export default AssignTestPage;










