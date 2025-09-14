'use client';

import React, { useState, useEffect } from 'react';
import { useAuth  } from '@/hooks/useAuth';
import { homeworkAPI, Homework, HomeworkSubmission } from '@/api/student/homework';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { 
  BookOpen, 
  Calendar, 
  Clock, 
  FileText, 
  Plus, 
  CheckCircle, 
  AlertCircle,
  Upload,
  Download
} from 'lucide-react';

export default function HomeworkPage() {
  const { user } = useAuth();
  const [homeworks, setHomeworks] = useState<Homework[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedFilter, setSelectedFilter] = useState<'all' | 'pending' | 'completed' | 'overdue'>('all');
  const [selectedSubject, setSelectedSubject] = useState<string>('');
  const [showSubmitModal, setShowSubmitModal] = useState(false);
  const [selectedHomework, setSelectedHomework] = useState<Homework | null>(null);
  const [submissionContent, setSubmissionContent] = useState('');
  const [submissionFiles, setSubmissionFiles] = useState<File[]>([]);

  useEffect(() => {
    loadHomeworks();
  }, []);

  const loadHomeworks = async () => {
    try {
      setLoading(true);
      const data = await homeworkAPI.getHomeworks(selectedSubject);
      setHomeworks(data);
    } catch (err) {
      setError('Erreur lors du chargement des devoirs');
      console.error('Erreur:', err);
    } finally {
      setLoading(false);
    }
  };

  const getFilteredHomeworks = () => {
    const now = new Date();
    return homeworks.filter(homework => {
      const dueDate = new Date(homework.due_date);
      const isOverdue = dueDate < now;
      const isCompleted = homework.submissions_count && homework.submissions_count > 0;

      switch (selectedFilter) {
        case 'pending':
          return !isCompleted && !isOverdue;
        case 'completed':
          return isCompleted;
        case 'overdue':
          return isOverdue && !isCompleted;
        default:
          return true;
      }
    });
  };

  const handleSubmitHomework = async () => {
    if (!selectedHomework) return;

    try {
      const submissionData = {
        content: submissionContent,
        attachments: submissionFiles.map(file => file.name)
      };

      await homeworkAPI.submitHomework(selectedHomework.id, submissionData);
      setShowSubmitModal(false);
      setSelectedHomework(null);
      setSubmissionContent('');
      setSubmissionFiles([]);
      await loadHomeworks();
    } catch (err) {
      console.error('Erreur lors de la soumission:', err);
    }
  };

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'high':
        return 'bg-red-100 text-red-800';
      case 'medium':
        return 'bg-yellow-100 text-yellow-800';
      case 'low':
        return 'bg-green-100 text-green-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const getStatusIcon = (homework: Homework) => {
    const dueDate = new Date(homework.due_date);
    const now = new Date();
    const isOverdue = dueDate < now;
    const isCompleted = homework.submissions_count && homework.submissions_count > 0;

    if (isCompleted) {
      return <CheckCircle className="w-4 h-4 text-green-500" />;
    } else if (isOverdue) {
      return <AlertCircle className="w-4 h-4 text-red-500" />;
    } else {
      return <Clock className="w-4 h-4 text-blue-500" />;
    }
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('fr-FR', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
    });
  };

  const formatTime = (dateString: string) => {
    return new Date(dateString).toLocaleTimeString('fr-FR', {
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 p-8">
        <div className="max-w-7xl mx-auto">
          <div className="animate-pulse space-y-6">
            {[1, 2, 3].map((i) => (
              <div key={i} className="bg-white rounded-lg p-6">
                <div className="h-4 bg-gray-200 rounded w-1/4 mb-4"></div>
                <div className="h-3 bg-gray-200 rounded w-3/4 mb-2"></div>
                <div className="h-3 bg-gray-200 rounded w-1/2"></div>
              </div>
            ))}
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 flex items-center gap-2">
            <BookOpen className="w-8 h-8 text-blue-600" />
            Gestion des Devoirs
          </h1>
          <p className="text-gray-600 mt-2">
            Gérez vos devoirs, soumettez vos travaux et suivez vos progrès
          </p>
        </div>

        {/* Filters */}
        <div className="bg-white rounded-lg shadow-sm p-6 mb-6">
          <div className="flex flex-wrap gap-4">
            <Select value={selectedFilter} onValueChange={(value: any) => setSelectedFilter(value)}>
              <SelectTrigger className="w-48">
                <SelectValue placeholder="Filtrer par statut" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">Tous les devoirs</SelectItem>
                <SelectItem value="pending">En attente</SelectItem>
                <SelectItem value="completed">Terminés</SelectItem>
                <SelectItem value="overdue">En retard</SelectItem>
              </SelectContent>
            </Select>

            <Select value={selectedSubject} onValueChange={setSelectedSubject}>
              <SelectTrigger className="w-48">
                <SelectValue placeholder="Filtrer par matière" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="">Toutes les matières</SelectItem>
                <SelectItem value="math">Mathématiques</SelectItem>
                <SelectItem value="physics">Physique</SelectItem>
                <SelectItem value="chemistry">Chimie</SelectItem>
                <SelectItem value="biology">Biologie</SelectItem>
                <SelectItem value="history">Histoire</SelectItem>
                <SelectItem value="geography">Géographie</SelectItem>
                <SelectItem value="literature">Littérature</SelectItem>
                <SelectItem value="english">Anglais</SelectItem>
              </SelectContent>
            </Select>

            <Button onClick={loadHomeworks} variant="outline">
              Actualiser
            </Button>
          </div>
        </div>

        {/* Homework List */}
        <div className="grid gap-6">
          {getFilteredHomeworks().length === 0 ? (
            <Card>
              <CardContent className="text-center py-12">
                <FileText className="w-12 h-12 text-gray-400 mx-auto mb-4" />
                <h3 className="text-lg font-medium text-gray-900 mb-2">
                  Aucun devoir {selectedFilter !== 'all' ? `(${selectedFilter})` : ''}
                </h3>
                <p className="text-gray-500">
                  {selectedFilter === 'all' 
                    ? 'Aucun devoir assigné pour le moment.'
                    : `Aucun devoir ${selectedFilter} trouvé.`
                  }
                </p>
              </CardContent>
            </Card>
          ) : (
            getFilteredHomeworks().map((homework) => (
              <Card key={homework.id} className="hover:shadow-md transition-shadow">
                <CardHeader>
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <div className="flex items-center gap-2 mb-2">
                        {getStatusIcon(homework)}
                        <CardTitle className="text-xl">{homework.title}</CardTitle>
                        <Badge className={getPriorityColor(homework.priority)}>
                          {homework.priority}
                        </Badge>
                      </div>
                      <p className="text-gray-600">{homework.description}</p>
                    </div>
                    <div className="flex flex-col items-end gap-2">
                      <span className="text-sm font-medium text-gray-900">
                        {homework.max_score} points
                      </span>
                      {homework.submissions_count && homework.submissions_count > 0 && (
                        <Badge className="bg-green-100 text-green-800">
                          Soumis
                        </Badge>
                      )}
                    </div>
                  </div>
                </CardHeader>
                <CardContent>
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
                    <div className="flex items-center gap-2 text-sm text-gray-500">
                      <Calendar className="w-4 h-4" />
                      <span>Échéance: {formatDate(homework.due_date)}</span>
                    </div>
                    <div className="flex items-center gap-2 text-sm text-gray-500">
                      <Clock className="w-4 h-4" />
                      <span>{formatTime(homework.due_date)}</span>
                    </div>
                    {homework.estimated_time && (
                      <div className="flex items-center gap-2 text-sm text-gray-500">
                        <Clock className="w-4 h-4" />
                        <span>Durée estimée: {homework.estimated_time} min</span>
                      </div>
                    )}
                  </div>

                  {homework.instructions && (
                    <div className="mb-4">
                      <h4 className="font-medium text-gray-900 mb-2">Instructions:</h4>
                      <p className="text-sm text-gray-600">{homework.instructions}</p>
                    </div>
                  )}

                  <div className="flex gap-2">
                    {!homework.submissions_count && (
                      <Button
                        onClick={() => {
                          setSelectedHomework(homework);
                          setShowSubmitModal(true);
                        }}
                      >
                        <Plus className="w-4 h-4 mr-2" />
                        Soumettre
                      </Button>
                    )}
                    <Button variant="outline">
                      <Download className="w-4 h-4 mr-2" />
                      Télécharger
                    </Button>
                  </div>
                </CardContent>
              </Card>
            ))
          )}
        </div>

        {/* Submit Modal */}
        {showSubmitModal && selectedHomework && (
          <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50">
            <div className="bg-white rounded-lg p-6 w-full max-w-2xl mx-4">
              <div className="flex items-center justify-between mb-4">
                <h2 className="text-xl font-semibold">Soumettre le devoir</h2>
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => setShowSubmitModal(false)}
                >
                  ×
                </Button>
              </div>

              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Contenu de la soumission
                  </label>
                  <Textarea
                    value={submissionContent}
                    onChange={(e) => setSubmissionContent(e.target.value)}
                    placeholder="Décrivez votre travail ou ajoutez des commentaires..."
                    rows={4}
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Fichiers joints
                  </label>
                  <div className="border-2 border-dashed border-gray-300 rounded-lg p-4">
                    <div className="text-center">
                      <Upload className="w-8 h-8 text-gray-400 mx-auto mb-2" />
                      <p className="text-sm text-gray-500">
                        Glissez-déposez vos fichiers ici ou cliquez pour sélectionner
                      </p>
                      <input
                        type="file"
                        multiple
                        onChange={(e) => setSubmissionFiles(Array.from(e.target.files || []))}
                        className="hidden"
                        id="file-upload"
                      />
                      <label htmlFor="file-upload" className="cursor-pointer">
                        <Button variant="outline" className="mt-2">
                          Sélectionner des fichiers
                        </Button>
                      </label>
                    </div>
                  </div>
                  {submissionFiles.length > 0 && (
                    <div className="mt-2">
                      <p className="text-sm font-medium text-gray-700 mb-1">Fichiers sélectionnés:</p>
                      <ul className="text-sm text-gray-600">
                        {submissionFiles.map((file, index) => (
                          <li key={index}>{file.name}</li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>

                <div className="flex justify-end gap-2">
                  <Button
                    variant="outline"
                    onClick={() => setShowSubmitModal(false)}
                  >
                    Annuler
                  </Button>
                  <Button
                    onClick={handleSubmitHomework}
                    disabled={!submissionContent.trim()}
                  >
                    Soumettre
                  </Button>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
