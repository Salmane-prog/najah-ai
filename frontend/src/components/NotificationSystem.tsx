"use client";
import React, { useState, useEffect } from 'react';
import { Bell, X, CheckCircle, Award, Trophy, Star } from 'lucide-react';
import { apiClient } from '../utils/api';

interface Notification {
  id: number;
  type: 'achievement' | 'challenge' | 'badge' | 'general';
  title: string;
  message: string;
  icon?: string;
  points_reward?: number;
  is_read: boolean;
  created_at: string;
}

const NotificationSystem: React.FC = () => {
  const [notifications, setNotifications] = useState<Notification[]>([]);
  const [isOpen, setIsOpen] = useState(false);
  const [unreadCount, setUnreadCount] = useState(0);
  const [isConnected, setIsConnected] = useState(false);

  const fetchNotifications = async () => {
    try {
      const user = localStorage.getItem('najah_user');
      
      if (!user) {
        console.log('[NOTIFICATIONS] Utilisateur non connecté, pas de notifications');
        return;
      }
      
      // Temporairement désactivé - endpoint non disponible
      console.log('[NOTIFICATIONS] Endpoint temporairement désactivé');
      setNotifications([]);
      setUnreadCount(0);
    } catch (error) {
      console.error('Erreur lors du chargement des notifications:', error);
    }
  };

  const markAsRead = async (notificationId: number) => {
    try {
      const user = localStorage.getItem('najah_user');
      
      if (!user) {
        console.log('[NOTIFICATIONS] Utilisateur non connecté, pas de marquage comme lu');
        return;
      }
      
      // Temporairement désactivé - endpoint non disponible
      console.log('[NOTIFICATIONS] Marquage comme lu temporairement désactivé');
    } catch (error) {
      console.error('Erreur lors du marquage comme lu:', error);
    }
  };

  const getNotificationIcon = (type: string, icon?: string) => {
    if (icon) return <span className="text-2xl">{icon}</span>;
    
    switch (type) {
      case 'achievement':
        return <Award className="w-5 h-5 text-yellow-500" />;
      case 'challenge':
        return <Trophy className="w-5 h-5 text-blue-500" />;
      case 'badge':
        return <Star className="w-5 h-5 text-purple-500" />;
      default:
        return <Bell className="w-5 h-5 text-gray-500" />;
    }
  };

  const getNotificationColor = (type: string) => {
    switch (type) {
      case 'achievement':
        return 'border-l-4 border-l-yellow-500 bg-yellow-50';
      case 'challenge':
        return 'border-l-4 border-l-blue-500 bg-blue-50';
      case 'badge':
        return 'border-l-4 border-l-purple-500 bg-purple-50';
      default:
        return 'border-l-4 border-l-gray-500 bg-gray-50';
    }
  };

  useEffect(() => {
    fetchNotifications();
    
    // Temporairement désactivé - endpoints non disponibles
    console.log('[NOTIFICATIONS] Vérification périodique désactivée');
  }, []);

  return (
    <div className="relative">
      {/* Bouton de notification */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="relative p-2 text-gray-600 hover:text-gray-900 focus:outline-none"
      >
        <Bell className="w-6 h-6" />
        {unreadCount > 0 && (
          <span className="absolute -top-1 -right-1 bg-red-500 text-white text-xs rounded-full h-5 w-5 flex items-center justify-center">
            {unreadCount > 9 ? '9+' : unreadCount}
          </span>
        )}
      </button>

      {/* Panneau de notifications */}
      {isOpen && (
        <div className="absolute right-0 mt-2 w-80 bg-white rounded-lg shadow-lg border border-gray-200 z-50">
          <div className="p-4 border-b border-gray-200">
            <div className="flex items-center justify-between">
              <h3 className="text-lg font-semibold text-gray-900">Notifications</h3>
              <button
                onClick={() => setIsOpen(false)}
                className="text-gray-400 hover:text-gray-600"
              >
                <X className="w-5 h-5" />
              </button>
            </div>
          </div>

          <div className="max-h-96 overflow-y-auto">
            {notifications.length > 0 ? (
              notifications.map((notification) => (
                <div
                  key={notification.id}
                  className={`p-4 border-b border-gray-100 hover:bg-gray-50 ${
                    !notification.is_read ? 'bg-blue-50' : ''
                  } ${getNotificationColor(notification.type)}`}
                >
                  <div className="flex items-start space-x-3">
                    <div className="flex-shrink-0 mt-1">
                      {getNotificationIcon(notification.type, notification.icon)}
                    </div>
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center justify-between">
                        <p className="text-sm font-medium text-gray-900">
                          {notification.title}
                        </p>
                        {!notification.is_read && (
                          <button
                            onClick={() => markAsRead(notification.id)}
                            className="text-xs text-blue-600 hover:text-blue-800"
                          >
                            Marquer comme lu
                          </button>
                        )}
                      </div>
                      <p className="text-sm text-gray-600 mt-1">
                        {notification.message}
                      </p>
                      {notification.points_reward && (
                        <div className="flex items-center mt-2">
                          <span className="text-xs text-green-600 font-medium">
                            +{notification.points_reward} points
                          </span>
                        </div>
                      )}
                      <p className="text-xs text-gray-400 mt-2">
                        {new Date(notification.created_at).toLocaleDateString()}
                      </p>
                    </div>
                  </div>
                </div>
              ))
            ) : (
              <div className="p-4 text-center text-gray-500">
                <Bell className="w-8 h-8 mx-auto mb-2 text-gray-300" />
                <p>Aucune notification</p>
              </div>
            )}
          </div>

          {notifications.length > 0 && (
            <div className="p-4 border-t border-gray-200">
              <button
                onClick={() => {
                  // Marquer toutes comme lues
                  notifications.forEach(n => !n.is_read && markAsRead(n.id));
                }}
                className="text-sm text-blue-600 hover:text-blue-800"
              >
                Marquer toutes comme lues
              </button>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default NotificationSystem; 