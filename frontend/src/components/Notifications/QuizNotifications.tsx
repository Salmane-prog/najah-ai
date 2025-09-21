'use client';

import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { 
  Bell, 
  AlertTriangle, 
  Clock, 
  CheckCircle, 
  X,
  RefreshCw
} from 'lucide-react';

interface QuizNotification {
  id: string;
  type: 'overdue' | 'due_soon' | 'completed' | 'low_score';
  title: string;
  message: string;
  quiz_title: string;
  student_name: string;
  due_date?: string;
  score?: number;
  created_at: string;
  is_read: boolean;
  priority: 'high' | 'medium' | 'low';
}

interface OverdueQuiz {
  id: number;
  quiz_title: string;
  student_name: string;
  due_date: string;
  days_overdue: number;
  assignment_id: number;
}

const QuizNotifications = () => {
  const [notifications, setNotifications] = useState<QuizNotification[]>([]);
  const [overdueQuizzes, setOverdueQuizzes] = useState<OverdueQuiz[]>([]);
  const [loading, setLoading] = useState(true);
  const [showAll, setShowAll] = useState(false);

  useEffect(() => {
    fetchNotifications();
    fetchOverdueQuizzes();
    
    // Actualiser toutes les 5 minutes
    const interval = setInterval(() => {
      fetchNotifications();
      fetchOverdueQuizzes();
    }, 5 * 60 * 1000);

    return () => clearInterval(interval);
  }, []);

  const fetchNotifications = async () => {
    try {
      const response = await fetch('/api/v1/notifications/quiz');
      if (response.ok) {
        const data = await response.json();
        setNotifications(data.notifications || []);
      }
    } catch (error) {
      console.error('Erreur lors du chargement des notifications:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchOverdueQuizzes = async () => {
    try {
      const response = await fetch('/api/v1/quiz_assignments/overdue');
      if (response.ok) {
        const data = await response.json();
        setOverdueQuizzes(data.overdue_quizzes || []);
      }
    } catch (error) {
      console.error('Erreur lors du chargement des quiz en retard:', error);
    }
  };

  const markAsRead = async (notificationId: string) => {
    try {
      const response = await fetch(`/api/v1/notifications/${notificationId}/read`, {
        method: 'PUT'
      });
      
      if (response.ok) {
        setNotifications(prev => 
          prev.map(n => 
            n.id === notificationId ? { ...n, is_read: true } : n
          )
        );
      }
    } catch (error) {
      console.error('Erreur lors de la mise à jour:', error);
    }
  };

  const markAllAsRead = async () => {
    try {
      const response = await fetch('/api/v1/notifications/mark-all-read', {
        method: 'PUT'
      });
      
      if (response.ok) {
        setNotifications(prev => 
          prev.map(n => ({ ...n, is_read: true }))
        );
      }
    } catch (error) {
      console.error('Erreur lors de la mise à jour:', error);
    }
  };

  const getNotificationIcon = (type: string) => {
    switch (type) {
      case 'overdue':
        return <AlertTriangle className="h-5 w-5 text-red-500" />;
      case 'due_soon':
        return <Clock className="h-5 w-5 text-yellow-500" />;
      case 'completed':
        return <CheckCircle className="h-5 w-5 text-green-500" />;
      case 'low_score':
        return <AlertTriangle className="h-5 w-5 text-orange-500" />;
      default:
        return <Bell className="h-5 w-5 text-blue-500" />;
    }
  };

  const getPriorityBadge = (priority: string) => {
    switch (priority) {
      case 'high':
        return <Badge variant="destructive">Haute</Badge>;
      case 'medium':
        return <Badge variant="default">Moyenne</Badge>;
      case 'low':
        return <Badge variant="secondary">Basse</Badge>;
      default:
        return <Badge variant="outline">{priority}</Badge>;
    }
  };

  const getTypeLabel = (type: string) => {
    switch (type) {
      case 'overdue':
        return 'En retard';
      case 'due_soon':
        return 'Échéance proche';
      case 'completed':
        return 'Terminé';
      case 'low_score':
        return 'Score faible';
      default:
        return type;
    }
  };

  const unreadCount = notifications.filter(n => !n.is_read).length;
  const highPriorityCount = notifications.filter(n => n.priority === 'high' && !n.is_read).length;

  if (loading) {
    return (
      <div className="flex items-center justify-center p-4">
        <RefreshCw className="h-6 w-6 animate-spin" />
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {/* Header avec compteurs */}
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-3">
          <Bell className="h-6 w-6 text-blue-600" />
          <div>
            <h2 className="text-xl font-semibold">Notifications</h2>
            <p className="text-sm text-gray-600">
              {unreadCount} non lue{unreadCount > 1 ? 's' : ''}
              {highPriorityCount > 0 && ` • ${highPriorityCount} priorité haute`}
            </p>
          </div>
        </div>
        
        <div className="flex space-x-2">
          <Button 
            variant="outline" 
            size="sm"
            onClick={() => setShowAll(!showAll)}
          >
            {showAll ? 'Voir moins' : 'Voir tout'}
          </Button>
          {unreadCount > 0 && (
            <Button 
              variant="outline" 
              size="sm"
              onClick={markAllAsRead}
            >
              Tout marquer comme lu
            </Button>
          )}
        </div>
      </div>

      {/* Alertes prioritaires - Quiz en retard */}
      {overdueQuizzes.length > 0 && (
        <Card className="border-red-200 bg-red-50">
          <CardHeader className="pb-3">
            <CardTitle className="flex items-center space-x-2 text-red-800">
              <AlertTriangle className="h-5 w-5" />
              <span>Quiz en Retard ({overdueQuizzes.length})</span>
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            {overdueQuizzes.slice(0, showAll ? undefined : 3).map((quiz) => (
              <div key={quiz.id} className="flex items-center justify-between p-3 bg-white rounded-lg border border-red-200">
                <div className="flex-1">
                  <div className="flex items-center space-x-2 mb-1">
                    <span className="font-medium text-red-800">{quiz.quiz_title}</span>
                    <Badge variant="destructive">
                      {quiz.days_overdue} jour{quiz.days_overdue > 1 ? 's' : ''} de retard
                    </Badge>
                  </div>
                  <p className="text-sm text-red-700">
                    Étudiant: {quiz.student_name} • Échéance: {new Date(quiz.due_date).toLocaleDateString()}
                  </p>
                </div>
                <Button variant="outline" size="sm">
                  Contacter
                </Button>
              </div>
            ))}
            
            {!showAll && overdueQuizzes.length > 3 && (
              <Button 
                variant="outline" 
                size="sm" 
                onClick={() => setShowAll(true)}
                className="w-full"
              >
                Voir tous les {overdueQuizzes.length} quiz en retard
              </Button>
            )}
          </CardContent>
        </Card>
      )}

      {/* Notifications générales */}
      <Card>
        <CardContent className="p-0">
          {notifications.length === 0 ? (
            <div className="p-6 text-center text-gray-500">
              <Bell className="h-12 w-12 mx-auto mb-3 text-gray-300" />
              <p>Aucune notification</p>
            </div>
          ) : (
            <div className="divide-y">
              {notifications
                .filter(n => showAll || !n.is_read)
                .slice(0, showAll ? undefined : 10)
                .map((notification) => (
                  <div 
                    key={notification.id} 
                    className={`p-4 hover:bg-gray-50 transition-colors ${
                      !notification.is_read ? 'bg-blue-50 border-l-4 border-l-blue-500' : ''
                    }`}
                  >
                    <div className="flex items-start space-x-3">
                      <div className="flex-shrink-0 mt-1">
                        {getNotificationIcon(notification.type)}
                      </div>
                      
                      <div className="flex-1 min-w-0">
                        <div className="flex items-center space-x-2 mb-1">
                          <span className="font-medium text-gray-900">
                            {notification.title}
                          </span>
                          {getPriorityBadge(notification.priority)}
                          <Badge variant="outline">
                            {getTypeLabel(notification.type)}
                          </Badge>
                        </div>
                        
                        <p className="text-sm text-gray-600 mb-2">
                          {notification.message}
                        </p>
                        
                        <div className="flex items-center justify-between text-xs text-gray-500">
                          <span>
                            Quiz: {notification.quiz_title} • Étudiant: {notification.student_name}
                            {notification.due_date && ` • Échéance: ${new Date(notification.due_date).toLocaleDateString()}`}
                            {notification.score !== undefined && ` • Score: ${notification.score}/100`}
                          </span>
                          <span>{new Date(notification.created_at).toLocaleDateString()}</span>
                        </div>
                      </div>
                      
                      <div className="flex-shrink-0">
                        {!notification.is_read && (
                          <Button
                            variant="ghost"
                            size="sm"
                            onClick={() => markAsRead(notification.id)}
                            className="h-8 w-8 p-0"
                          >
                            <X className="h-4 w-4" />
                          </Button>
                        )}
                      </div>
                    </div>
                  </div>
                ))}
              
              {!showAll && notifications.filter(n => !n.is_read).length > 10 && (
                <div className="p-4 text-center">
                  <Button 
                    variant="outline" 
                    onClick={() => setShowAll(true)}
                  >
                    Voir toutes les notifications
                  </Button>
                </div>
              )}
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
};

export default QuizNotifications;













