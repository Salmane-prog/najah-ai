'use client';

import React, { useState, useEffect } from 'react';
import { useSearchParams } from 'next/navigation';
import Sidebar from '@/components/Sidebar';
import { useAuth  } from '@/hooks/useAuth';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { 
  ArrowLeft, 
  Target, 
  Clock, 
  Users, 
  BookOpen, 
  CheckCircle,
  Award,
  FileText,
  Eye,
  Edit
} from 'lucide-react';
import { FormativeEvaluation } from '@/services/formativeEvaluationService';

interface PreviewFormativeTestProps {
  searchParams: { [key: string]: string | string[] | undefined };
}

export default function PreviewFormativeTest({ searchParams }: PreviewFormativeTestProps) {
  const { user, token } = useAuth();
  const [evaluation, setEvaluation] = useState<FormativeEvaluation | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (searchParams.previewId) {
      loadEvaluation();
    }
  }, [searchParams.previewId]);

  const loadEvaluation = async () => {
    try {
      setLoading(true);
      setError(null);
      
      // Récupérer l'évaluation depuis localStorage
      const previewId = searchParams.previewId as string;
      const storedData = localStorage.getItem(`formativePreview_${previewId}`);
      
      if (storedData) {
        const parsedEvaluation = JSON.parse(storedData);
        setEvaluation(parsedEvaluation);
        console.log('✅ Évaluation chargée depuis localStorage:', parsedEvaluation);
      } else {
        setError('Aucune évaluation trouvée. Veuillez revenir à la liste et cliquer sur Prévisualiser.');
      }
    } catch (err) {
      console.error('❌ Erreur lors du chargement:', err);
      setError('Erreur lors du chargement de l\'évaluation');
    } finally {
      setLoading(false);
    }
  };

  const handleBackToList = () => {
    window.history.back();
  };

  const handleEdit = () => {
    if (evaluation) {
      // Rediriger vers la page de modification
      window.open(`/dashboard/teacher/adaptive-evaluation/edit-assessment?id=${evaluation.id}`, '_blank');
    }
  };

  if (loading) {
    return (
      <div className="flex h-screen">
        <Sidebar />
        <div className="flex-1 flex items-center justify-center">
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-orange-600 mx-auto mb-4"></div>
            <p className="text-gray-600">Chargement de l'évaluation...</p>
          </div>
        </div>
      </div>
    );
  }

  if (error || !evaluation) {
    return (
      <div className="flex h-screen">
        <Sidebar />
        <div className="flex-1 flex items-center justify-center">
          <div className="text-center max-w-md">
            <div className="text-red-500 text-6xl mb-4">⚠️</div>
            <h2 className="text-xl font-semibold text-gray-800 mb-2">Erreur de chargement</h2>
            <p className="text-gray-600 mb-6">{error || 'Évaluation non trouvée'}</p>
            <Button onClick={handleBackToList} className="bg-orange-600 hover:bg-orange-700">
              <ArrowLeft className="w-4 h-4 mr-2" />
              Retour à la liste
            </Button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="flex h-screen">
      <Sidebar />
      <div className="flex-1 overflow-y-auto bg-gray-50">
        {/* Header */}
        <div className="bg-white border-b border-gray-200 px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <Button
                onClick={handleBackToList}
                variant="ghost"
                className="text-gray-600 hover:text-gray-800"
              >
                <ArrowLeft className="w-4 h-4 mr-2" />
                Retour
              </Button>
              <div>
                <h1 className="text-2xl font-bold text-gray-900">Prévisualisation de l'Évaluation</h1>
                <p className="text-gray-600">Aperçu détaillé de l'évaluation formative</p>
              </div>
            </div>
            <div className="flex space-x-3">
              <Button
                onClick={handleEdit}
                className="bg-blue-600 hover:bg-blue-700 text-white"
              >
                <Edit className="w-4 h-4 mr-2" />
                Modifier
              </Button>
            </div>
          </div>
        </div>

        {/* Contenu principal */}
        <div className="p-6 max-w-4xl mx-auto">
          {/* Informations générales */}
          <Card className="mb-6">
            <CardHeader>
              <CardTitle className="flex items-center space-x-3">
                <span className="text-2xl">{evaluation.title}</span>
                <Badge variant={evaluation.is_active ? "default" : "secondary"}>
                  {evaluation.is_active ? 'Active' : 'Inactive'}
                </Badge>
                <Badge variant="outline" className="bg-orange-50 text-orange-700 border-orange-200">
                  {evaluation.assessment_type}
                </Badge>
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-gray-700 text-lg mb-6">{evaluation.description}</p>
              
              {/* Métadonnées */}
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
                <div className="flex items-center space-x-2 text-gray-600">
                  <Target className="w-4 h-4" />
                  <span>Niveau {evaluation.target_level}</span>
                </div>
                <div className="flex items-center space-x-2 text-gray-600">
                  <Clock className="w-4 h-4" />
                  <span>{evaluation.duration_minutes} min</span>
                </div>
                <div className="flex items-center space-x-2 text-gray-600">
                  <Users className="w-4 h-4" />
                  <span>Max {evaluation.max_students}</span>
                </div>
                <div className="flex items-center space-x-2 text-gray-600">
                  <BookOpen className="w-4 h-4" />
                  <span>{evaluation.questions?.length || 0} questions</span>
                </div>
              </div>

              {/* Objectifs d'apprentissage */}
              {evaluation.learning_objectives && evaluation.learning_objectives.length > 0 && (
                <div className="mb-6">
                  <h3 className="text-lg font-semibold text-gray-800 mb-3 flex items-center">
                    <Target className="w-5 h-5 mr-2 text-blue-600" />
                    Objectifs d'apprentissage
                  </h3>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                    {evaluation.learning_objectives.map((objective, index) => (
                      <div key={index} className="flex items-center space-x-2 text-gray-700">
                        <CheckCircle className="w-4 h-4 text-green-500" />
                        <span>{objective}</span>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </CardContent>
          </Card>

          {/* Critères d'évaluation */}
          {evaluation.criteria && evaluation.criteria.length > 0 && (
            <Card className="mb-6">
              <CardHeader>
                <CardTitle className="flex items-center">
                  <Award className="w-5 h-5 mr-2 text-purple-600" />
                  Critères d'évaluation
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {evaluation.criteria.map((criterion, index) => (
                    <div key={index} className="border-l-4 border-purple-200 pl-4 py-2">
                      <div className="flex items-center justify-between mb-2">
                        <h4 className="font-semibold text-gray-800">{criterion.name}</h4>
                        <Badge variant="outline" className="bg-purple-50 text-purple-700">
                          {criterion.weight}% - {criterion.max_points} pts
                        </Badge>
                      </div>
                      <p className="text-gray-600 text-sm">{criterion.description}</p>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          )}

          {/* Grille de notation */}
          {evaluation.rubric && (
            <Card className="mb-6">
              <CardHeader>
                <CardTitle className="flex items-center">
                  <FileText className="w-5 h-5 mr-2 text-green-600" />
                  Grille de notation
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {Object.entries(evaluation.rubric).map(([level, details]: [string, any]) => (
                    <div key={level} className="border rounded-lg p-4">
                      <div className="flex items-center justify-between mb-2">
                        <h4 className="font-semibold capitalize text-gray-800">
                          {level === 'excellent' ? 'Excellent' : 
                           level === 'good' ? 'Bon' : 
                           level === 'satisfactory' ? 'Satisfaisant' : 
                           level === 'needs_improvement' ? 'À améliorer' : level}
                        </h4>
                        <Badge variant="outline" className="bg-green-50 text-green-700">
                          {details.points} pts
                        </Badge>
                      </div>
                      <p className="text-gray-600 text-sm">{details.description}</p>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          )}

          {/* Questions */}
          {evaluation.questions && evaluation.questions.length > 0 && (
            <Card className="mb-6">
              <CardHeader>
                <CardTitle className="flex items-center">
                  <BookOpen className="w-5 h-5 mr-2 text-orange-600" />
                  Questions ({evaluation.questions.length})
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {evaluation.questions.map((question, index) => (
                    <div key={index} className="border rounded-lg p-4 bg-gray-50">
                      <div className="flex items-center justify-between mb-2">
                        <h4 className="font-semibold text-gray-800">
                          Question {index + 1}
                        </h4>
                        <Badge variant="outline" className="bg-orange-50 text-orange-700">
                          {question.max_points} pts
                        </Badge>
                      </div>
                      <p className="text-gray-700 mb-2">{question.question}</p>
                      <div className="flex items-center space-x-2 text-sm text-gray-500">
                        <span>Type: {question.type}</span>
                        <span>•</span>
                        <span>Points max: {question.max_points}</span>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          )}

          {/* Instructions */}
          {evaluation.instructions && (
            <Card className="mb-6">
              <CardHeader>
                <CardTitle className="flex items-center">
                  <Eye className="w-5 h-5 mr-2 text-blue-600" />
                  Instructions
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="bg-blue-50 border-l-4 border-blue-200 p-4">
                  <p className="text-gray-700 whitespace-pre-line">{evaluation.instructions}</p>
                </div>
              </CardContent>
            </Card>
          )}

          {/* Indicateurs de succès */}
          {evaluation.success_indicators && evaluation.success_indicators.length > 0 && (
            <Card className="mb-6">
              <CardHeader>
                <CardTitle className="flex items-center">
                  <CheckCircle className="w-5 h-5 mr-2 text-green-600" />
                  Indicateurs de succès
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-2">
                  {evaluation.success_indicators.map((indicator, index) => (
                    <div key={index} className="flex items-center space-x-2 text-gray-700">
                      <CheckCircle className="w-4 h-4 text-green-500" />
                      <span>{indicator}</span>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          )}

          {/* Informations de création */}
          <Card className="bg-gray-50">
            <CardContent className="pt-6">
              <div className="text-center text-sm text-gray-500">
                <p>Évaluation créée le {new Date(evaluation.created_at).toLocaleDateString('fr-FR', {
                  year: 'numeric',
                  month: 'long',
                  day: 'numeric',
                  hour: '2-digit',
                  minute: '2-digit'
                })}</p>
                <p>ID: {evaluation.id}</p>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}
