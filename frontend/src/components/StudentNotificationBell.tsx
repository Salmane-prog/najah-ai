"use client";
import React, { useState, useEffect } from 'react';
import { Bell, X } from 'lucide-react';
import { useAuth  } from '../hooks/useAuth';

interface Notification {
  id: number;
  title: string;
  message: string;
  type: string;
  data: any;
  is_read: boolean;
  created_at: string;
}

const StudentNotificationBell: React.FC = () => {
  const { user, token } = useAuth();
  const [notifications, setNotifications] = useState<Notification[]>([]);
  const [unreadCount, setUnreadCount] = useState(0);
  const [showDropdown, setShowDropdown] = useState(false);
  const [loading, setLoading] = useState(false);

  const fetchNotifications = async () => {
    if (!token) return;
    
    try {
      setLoading(true);
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/v1/student_messaging/notifications`, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });
      
      if (response.ok) {
        const data = await response.json();
        setNotifications(data.notifications || []);
        
        // Compter les notifications non lues
        const unread = data.notifications?.filter((n: Notification) => !n.is_read).length || 0;
        setUnreadCount(unread);
      }
    } catch (error) {
      console.error('Erreur lors du chargement des notifications:', error);
    } finally {
      setLoading(false);
    }
  };

  const markAsRead = async (notificationId: number) => {
    if (!token) return;
    
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/v1/student_messaging/notifications/${notificationId}/mark-read`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });
      
      if (response.ok) {
        // Mettre à jour l'état local
        setNotifications(prev => 
          prev.map(n => n.id === notificationId ? { ...n, is_read: true } : n)
        );
        setUnreadCount(prev => Math.max(0, prev - 1));
      }
    } catch (error) {
      console.error('Erreur lors du marquage de la notification:', error);
    }
  };

  const formatTimeAgo = (dateString: string) => {
    const date = new Date(dateString);
    const now = new Date();
    const diffInMinutes = Math.floor((now.getTime() - date.getTime()) / (1000 * 60));
    
    if (diffInMinutes < 1) return 'À l\'instant';
    if (diffInMinutes < 60) return `Il y a ${diffInMinutes} min`;
    if (diffInMinutes < 1440) return `Il y a ${Math.floor(diffInMinutes / 60)}h`;
    return `Il y a ${Math.floor(diffInMinutes / 1440)}j`;
  };

  useEffect(() => {
    if (user && token) {
      fetchNotifications();
      // Auto-refresh toutes les 30 secondes
      const interval = setInterval(fetchNotifications, 30000);
      return () => clearInterval(interval);
    }
  }, [user, token]);

  if (!user || !token) return null;

  return (
    <div className="relative">
      {/* Bouton de notification */}
      <button
        onClick={() => setShowDropdown(!showDropdown)}
        className="relative p-2 text-gray-600 hover:text-gray-800 hover:bg-gray-100 rounded-full transition-colors"
      >
        <Bell className="w-5 h-5" />
        {unreadCount > 0 && (
          <span className="absolute -top-1 -right-1 bg-red-500 text-white text-xs rounded-full w-5 h-5 flex items-center justify-center">
            {unreadCount > 9 ? '9+' : unreadCount}
          </span>
        )}
      </button>

      {/* Dropdown des notifications */}
      {showDropdown && (
        <div className="absolute right-0 mt-2 w-80 bg-white border border-gray-200 rounded-lg shadow-lg z-50">
          <div className="p-4 border-b border-gray-200 flex items-center justify-between">
            <h3 className="font-semibold text-gray-800">Notifications</h3>
            <button
              onClick={() => setShowDropdown(false)}
              className="text-gray-400 hover:text-gray-600"
            >
              <X className="w-4 h-4" />
            </button>
          </div>
          
          <div className="max-h-96 overflow-y-auto">
            {loading ? (
              <div className="p-4 text-center text-gray-500">
                Chargement...
              </div>
            ) : notifications.length === 0 ? (
              <div className="p-4 text-center text-gray-500">
                Aucune notification
              </div>
            ) : (
              notifications.map((notification) => (
                <div
                  key={notification.id}
                  className={`p-4 border-b border-gray-100 hover:bg-gray-50 transition-colors ${
                    !notification.is_read ? 'bg-blue-50' : ''
                  }`}
                >
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <h4 className="font-medium text-gray-800 mb-1">
                        {notification.title}
                      </h4>
                      <p className="text-sm text-gray-600 mb-2">
                        {notification.message}
                      </p>
                      {notification.data?.message_preview && (
                        <p className="text-xs text-gray-500 italic">
                          "{notification.data.message_preview}"
                        </p>
                      )}
                      <p className="text-xs text-gray-400 mt-2">
                        {formatTimeAgo(notification.created_at)}
                      </p>
                    </div>
                    {!notification.is_read && (
                      <button
                        onClick={() => markAsRead(notification.id)}
                        className="ml-2 text-xs text-blue-600 hover:text-blue-800"
                      >
                        Marquer comme lu
                      </button>
                    )}
                  </div>
                </div>
              ))
            )}
          </div>
          
          {notifications.length > 0 && (
            <div className="p-3 border-t border-gray-200 bg-gray-50">
              <button
                onClick={() => {
                  // Marquer toutes les notifications comme lues
                  notifications.forEach(n => {
                    if (!n.is_read) markAsRead(n.id);
                  });
                }}
                className="text-sm text-blue-600 hover:text-blue-800"
              >
                Marquer tout comme lu
              </button>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default StudentNotificationBell; 