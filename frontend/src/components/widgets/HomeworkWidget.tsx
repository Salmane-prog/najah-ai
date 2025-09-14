'use client';

import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Calendar, Clock, BookOpen, FileText, Plus, CheckCircle, AlertCircle } from 'lucide-react';
import { homeworkAPI, Homework, HomeworkSubmission } from '@/api/student/homework';
import { useAuth  } from '@/hooks/useAuth';

interface HomeworkWidgetProps {
  className?: string;
}

export default function HomeworkWidget({ className }: HomeworkWidgetProps) {
  const { user } = useAuth();
  const [homeworks, setHomeworks] = useState<Homework[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedFilter, setSelectedFilter] = useState<'all' | 'pending' | 'completed' | 'overdue'>('all');

  useEffect(() => {
    loadHomeworks();
  }, []);

  const loadHomeworks = async () => {
    try {
      setLoading(true);
      const data = await homeworkAPI.getHomeworks();
      
      // Ensure data is an array
      if (Array.isArray(data)) {
        setHomeworks(data);
      } else {
        console.error('Expected array but received:', typeof data, data);
        setHomeworks([]);
        setError('Format de données invalide');
      }
    } catch (err) {
      setError('Erreur lors du chargement des devoirs');
      console.error('Erreur:', err);
      setHomeworks([]);
    } finally {
      setLoading(false);
    }
  };

  const getFilteredHomeworks = () => {
    const now = new Date();
    
    // Ensure homeworks is an array
    if (!Array.isArray(homeworks)) {
      return [];
    }
    
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
      <Card className={className}>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <BookOpen className="w-5 h-5" />
            Devoirs
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="animate-pulse space-y-4">
            {[1, 2, 3].map((i) => (
              <div key={i} className="flex items-center space-x-4">
                <div className="w-4 h-4 bg-gray-200 rounded"></div>
                <div className="flex-1 space-y-2">
                  <div className="h-4 bg-gray-200 rounded w-3/4"></div>
                  <div className="h-3 bg-gray-200 rounded w-1/2"></div>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    );
  }

  if (error) {
    return (
      <Card className={className}>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <BookOpen className="w-5 h-5" />
            Devoirs
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="text-center text-red-500">
            <AlertCircle className="w-8 h-8 mx-auto mb-2" />
            <p>{error}</p>
            <Button onClick={loadHomeworks} className="mt-2">
              Réessayer
            </Button>
          </div>
        </CardContent>
      </Card>
    );
  }

  const filteredHomeworks = getFilteredHomeworks();

  return (
    <Card className={className}>
      <CardHeader>
        <div className="flex items-center justify-between">
          <CardTitle className="flex items-center gap-2">
            <BookOpen className="w-5 h-5" />
            Devoirs
          </CardTitle>
          <div className="flex gap-2">
            <select
              value={selectedFilter}
              onChange={(e) => setSelectedFilter(e.target.value as any)}
              className="px-3 py-1 text-sm border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              <option value="all">Tous</option>
              <option value="pending">En attente</option>
              <option value="completed">Terminés</option>
              <option value="overdue">En retard</option>
            </select>
          </div>
        </div>
      </CardHeader>
      <CardContent>
        <div className="space-y-4 max-h-96 overflow-y-auto">
          {filteredHomeworks.length === 0 ? (
            <div className="text-center text-gray-500 py-8">
              <FileText className="w-12 h-12 mx-auto mb-2 opacity-50" />
              <p>Aucun devoir {selectedFilter !== 'all' ? `(${selectedFilter})` : ''}</p>
            </div>
          ) : (
            filteredHomeworks.map((homework) => (
              <div key={homework.id} className="border rounded-lg p-4 hover:shadow-md transition-shadow">
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <div className="flex items-center gap-2 mb-2">
                      {getStatusIcon(homework)}
                      <h3 className="font-semibold text-gray-900">{homework.title}</h3>
                      <Badge className={getPriorityColor(homework.priority)}>
                        {homework.priority}
                      </Badge>
                    </div>
                    <p className="text-sm text-gray-600 mb-2">{homework.description}</p>
                    <div className="flex items-center gap-4 text-sm text-gray-500">
                      <div className="flex items-center gap-1">
                        <Calendar className="w-4 h-4" />
                        <span>{formatDate(homework.due_date)}</span>
                      </div>
                      <div className="flex items-center gap-1">
                        <Clock className="w-4 h-4" />
                        <span>{formatTime(homework.due_date)}</span>
                      </div>
                      {homework.estimated_time && (
                        <div className="flex items-center gap-1">
                          <Clock className="w-4 h-4" />
                          <span>{homework.estimated_time} min</span>
                        </div>
                      )}
                    </div>
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
              </div>
            ))
          )}
        </div>
      </CardContent>
    </Card>
  );
}