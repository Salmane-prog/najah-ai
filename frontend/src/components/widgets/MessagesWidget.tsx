'use client';

import React, { useEffect, useState } from 'react';
import { Card } from '../Card';
import { MessageCircle, User, Clock, Reply, MoreVertical, AlertCircle } from 'lucide-react';

interface Message {
  id: number;
  user_id: number;
  content: string;
  created_at: string;
  thread_id?: number;
}

interface MessagesWidgetProps {
  messages?: Message[];
  className?: string;
}

interface Thread {
  id: number;
  title: string;
  created_by: number;
  created_at: string;
}

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export default function MessagesWidget({ messages, className = '' }: MessagesWidgetProps) {
  const [threads, setThreads] = useState<Thread[]>([]);
  const [selectedThread, setSelectedThread] = useState<Thread | null>(null);
  const [threadMessages, setThreadMessages] = useState<Message[]>([]);
  const [newMessage, setNewMessage] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);
  const [authError, setAuthError] = useState<string | null>(null);
  const [threadsLoading, setThreadsLoading] = useState(true);

  // Charger les threads
  useEffect(() => {
    const token = localStorage.getItem('najah_token');
    const user = localStorage.getItem('najah_user');
    
    if (!token || !user) {
      setThreads([]);
      setThreadsLoading(false);
      return;
    }

    // Vérifier que l'utilisateur est un enseignant
    try {
      const userData = JSON.parse(user);
      if (userData.role !== 'teacher') {
        console.log('MessagesWidget: Utilisateur non-enseignant, pas de messages');
        setThreads([]);
        setThreadsLoading(false);
        return;
      }
    } catch (e) {
      console.error('MessagesWidget: Erreur parsing user data:', e);
      setThreads([]);
      setThreadsLoading(false);
      return;
    }

    fetch(`${API_BASE_URL}/api/v1/teacher_messaging/conversations`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
      .then(res => {
        if (!res.ok) {
          if (res.status === 401 || res.status === 403) {
            console.log('MessagesWidget: Non autorisé, déconnexion');
            localStorage.removeItem('najah_token');
            localStorage.removeItem('najah_user');
            window.location.href = '/login';
            return;
          }
          throw new Error('Erreur lors du chargement des messages');
        }
        return res.json();
      })
      .then(data => {
        // S'assurer que data est un tableau
        if (Array.isArray(data)) {
          setThreads(data);
        } else {
          console.warn('API messages a retourné des données non-array:', data);
          setThreads([]);
        }
      })
      .catch((error) => {
        console.error('Erreur lors du chargement des messages:', error);
        setThreads([]);
        setAuthError('Impossible de charger les messages. Veuillez vous reconnecter.');
      })
      .finally(() => {
        setThreadsLoading(false);
      });
  }, []);

  // Charger les messages d'un thread sélectionné
  useEffect(() => {
    if (selectedThread) {
      const token = localStorage.getItem('najah_token');
      const user = localStorage.getItem('najah_user');
      
      if (!token || !user) {
        setThreadMessages([]);
        return;
      }

      // Vérifier que l'utilisateur est un enseignant
      try {
        const userData = JSON.parse(user);
        if (userData.role !== 'teacher') {
          console.log('MessagesWidget: Utilisateur non-enseignant, pas de messages');
          setThreadMessages([]);
          return;
        }
      } catch (e) {
        console.error('MessagesWidget: Erreur parsing user data:', e);
        setThreadMessages([]);
        return;
      }

      fetch(`${API_BASE_URL}/api/v1/teacher_messaging/conversation/${selectedThread.id}`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      })
        .then(res => {
          if (!res.ok) {
            if (res.status === 401 || res.status === 403) {
              console.log('MessagesWidget: Non autorisé, déconnexion');
              localStorage.removeItem('najah_token');
              localStorage.removeItem('najah_user');
              window.location.href = '/login';
              return;
            }
            throw new Error('Erreur lors du chargement des messages');
          }
          return res.json();
        })
        .then(data => {
          // S'assurer que data est un tableau
          if (Array.isArray(data)) {
            setThreadMessages(data);
          } else {
            console.warn('API messages a retourné des données non-array:', data);
            setThreadMessages([]);
          }
        })
        .catch((error) => {
          console.error('Erreur lors du chargement des messages:', error);
          setThreadMessages([]);
          setAuthError('Impossible de charger les messages. Veuillez vous reconnecter.');
        });
    }
  }, [selectedThread]);

  const handleSendMessage = async () => {
    if (!selectedThread || !newMessage.trim()) return;
    
    const token = localStorage.getItem('najah_token');
    if (!token) {
      setError('Non authentifié');
      return;
    }
    
    setLoading(true);
    setError(null);
    setSuccess(null);
    try {
      const res = await fetch(`${API_BASE_URL}/api/v1/teacher_messaging/send-message`, {
        method: 'POST',
        headers: { 
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          user_id: 1, // TODO: remplacer par l'ID utilisateur courant
          thread_id: selectedThread.id,
          content: newMessage.trim(),
        })
      });
      if (!res.ok) {
        const errorData = await res.json().catch(() => ({}));
        throw new Error(errorData.detail || 'Erreur lors de l\'envoi du message');
      }
      setNewMessage('');
      setSuccess('Message envoyé !');
      setTimeout(() => setSuccess(null), 1000);
      
      // Rafraîchir les messages du thread
      const refreshRes = await fetch(`${API_BASE_URL}/api/v1/messages/thread/${selectedThread.id}`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      if (refreshRes.ok) {
        const refreshData = await refreshRes.json();
        if (Array.isArray(refreshData)) {
          setThreadMessages(refreshData);
        }
      }
    } catch (err: any) {
      setError(err.message || 'Erreur inconnue');
    } finally {
      setLoading(false);
    }
  };

  const unreadCount = messages?.length || 0; // Simplifié pour l'exemple
  const recentMessages = messages?.slice(0, 5) || [];

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    const now = new Date();
    const diffInHours = Math.floor((now.getTime() - date.getTime()) / (1000 * 60 * 60));
    
    if (diffInHours < 1) return 'À l\'instant';
    if (diffInHours < 24) return `Il y a ${diffInHours}h`;
    if (diffInHours < 48) return 'Hier';
    return date.toLocaleDateString('fr-FR');
  };

  const truncateText = (text: string, maxLength: number = 50) => {
    return text.length > maxLength ? text.substring(0, maxLength) + '...' : text;
  };

  return (
    <Card title="Messagerie" icon={<MessageCircle />} className={`p-8 shadow-lg rounded-2xl ${className}`}>
      <div className="space-y-8">
        {/* Message d'erreur d'authentification */}
        {authError && (
          <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
            <div className="flex items-center gap-2">
              <AlertCircle className="text-yellow-600" size={20} />
              <div>
                <p className="text-yellow-800 font-medium">{authError}</p>
                <p className="text-yellow-700 text-sm mt-1">
                  Veuillez vous connecter en tant qu'enseignant pour accéder à la messagerie.
                </p>
              </div>
            </div>
          </div>
        )}
        {/* Navigation par thread */}
        <div className="mb-4">
          <h3 className="text-lg font-bold text-gray-800 mb-2">Conversations</h3>
          {threadsLoading ? (
            <div className="text-gray-500 italic">Chargement des conversations...</div>
          ) : (
            <div className="flex gap-2 overflow-x-auto">
              {Array.isArray(threads) && threads.length > 0 ? (
                threads.map(thread => (
                  <button
                    key={thread.id}
                    onClick={() => setSelectedThread(thread)}
                    className={`px-4 py-2 rounded-lg font-semibold border transition ${selectedThread?.id === thread.id ? 'bg-blue-600 text-white' : 'bg-gray-100 text-gray-700 border-gray-300 hover:bg-blue-50'}`}
                  >
                    {thread.title}
                  </button>
                ))
              ) : (
                <div className="text-gray-500 italic">Aucune conversation disponible.</div>
              )}
            </div>
          )}
        </div>
        {/* Affichage des messages du thread sélectionné */}
        {selectedThread ? (
          <div className="space-y-4">
            <h4 className="font-bold text-base text-blue-700 mb-2">Messages du thread : {selectedThread.title}</h4>
            <div className="max-h-64 overflow-y-auto bg-gray-50 rounded-lg p-4">
              {threadMessages.length > 0 ? (
                threadMessages.map((msg) => (
                  <div key={msg.id} className="mb-3">
                    <div className="flex items-center gap-2 mb-1">
                      <User className="text-blue-600" size={16} />
                      <span className="font-semibold text-gray-800">Utilisateur {msg.user_id}</span>
                      <span className="text-xs text-gray-500">{new Date(msg.created_at).toLocaleString('fr-FR')}</span>
                    </div>
                    <div className="ml-6 text-gray-700">{msg.content}</div>
                  </div>
                ))
              ) : (
                <div className="text-gray-500 italic">Aucun message dans ce thread.</div>
              )}
            </div>
            {/* Formulaire d’envoi de message */}
            <div className="flex gap-2 mt-4">
              <input
                type="text"
                value={newMessage}
                onChange={e => setNewMessage(e.target.value)}
                placeholder="Écrire un message..."
                className="flex-1 border rounded-lg px-3 py-2"
                disabled={loading}
              />
              <button
                onClick={handleSendMessage}
                disabled={loading || !newMessage.trim()}
                className="px-4 py-2 bg-blue-600 text-white rounded-lg font-semibold hover:bg-blue-700 transition disabled:opacity-50"
              >
                Envoyer
              </button>
            </div>
            {success && <div className="text-green-600 mt-2">{success}</div>}
            {error && <div className="text-red-600 mt-2">{error}</div>}
          </div>
        ) : (
          <div className="text-gray-500 italic">Sélectionne une conversation pour voir les messages.</div>
        )}
      </div>
    </Card>
  );
} 