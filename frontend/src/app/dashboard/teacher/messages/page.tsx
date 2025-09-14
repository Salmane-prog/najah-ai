'use client';

import React, { useState, useEffect, useRef } from 'react';
import { useAuth  } from '../../../../hooks/useAuth';
import { Card } from '../../../../components/Card';
import Sidebar from '../../../../components/Sidebar';
import { 
  MessageSquare, 
  Send, 
  Clock, 
  Search,
  Plus
} from 'lucide-react';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

// Vérifier l'URL de l'API
console.log('API_BASE_URL:', API_BASE_URL);

interface Message {
  id: number;
  content: string;
  timestamp: string;
  user_id: number;
  is_teacher: boolean;
  sender_name: string;
}

interface Conversation {
  thread_id: number | null;
  student: {
    id: number;
    name: string;
    email: string;
  };
  last_message: {
    content: string;
    timestamp: string | null;
    user_id: number | null;
  } | null;
  unread_count: number;
}

interface Student {
  id: number;
  name: string;
  email: string;
  role: string;
}

export default function TeacherMessages() {
  const { user, token, isAuthenticated } = useAuth();
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [selectedConversation, setSelectedConversation] = useState<Conversation | null>(null);
  const [messages, setMessages] = useState<Message[]>([]);
  const [newMessage, setNewMessage] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [sending, setSending] = useState(false);
  const [students, setStudents] = useState<Student[]>([]);
  const [showStudentSelector, setShowStudentSelector] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Debug: Afficher les informations d'authentification
  console.log('Auth debug:', { user, token: token ? 'present' : 'missing', isAuthenticated });

  useEffect(() => {
    if (token) {
      console.log('Token disponible, chargement des conversations...');
      fetchConversations();
      fetchStudents();
      
      // Auto-refresh toutes les 30 secondes
      const interval = setInterval(() => {
        fetchConversations();
      }, 30000);
      
      return () => clearInterval(interval);
    } else {
      console.log('Token non disponible');
      setError('Token d\'authentification manquant');
    }
  }, [token]);

  const fetchConversations = async () => {
    try {
      setLoading(true);
      setError(null); // Effacer les erreurs précédentes
      
      const response = await fetch(`${API_BASE_URL}/api/v1/teacher_messaging/conversations`, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });

      if (response.ok) {
        const data = await response.json();
        setConversations(data.conversations || []);
        setError(null); // S'assurer qu'il n'y a pas d'erreur
      } else {
        console.error('Erreur API:', response.status, response.statusText);
        setError('Erreur lors du chargement des conversations');
      }
    } catch (err) {
      console.error('Erreur de connexion:', err);
      setError('Erreur de connexion au serveur');
    } finally {
      setLoading(false);
    }
  };

  const fetchStudents = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/v1/users/students`, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });

      if (response.ok) {
        const data = await response.json();
        setStudents(data || []); // L'endpoint retourne directement un array
      } else {
        console.error('Erreur lors du chargement des étudiants');
      }
    } catch (err) {
      console.error('Erreur de connexion pour les étudiants:', err);
    }
  };

  const fetchMessages = async (studentId: number) => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/v1/teacher_messaging/conversation/${studentId}`, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });

      if (response.ok) {
        const data = await response.json();
        setMessages(data.messages || []);
        setError(null); // Effacer les erreurs si succès
      } else {
        console.error('Erreur API messages:', response.status, response.statusText);
        setError('Erreur lors du chargement des messages');
      }
    } catch (err) {
      console.error('Erreur de connexion messages:', err);
      setError('Erreur de connexion au serveur');
    }
  };

  const sendMessage = async () => {
    if (!newMessage.trim() || !selectedConversation) return;

    try {
      setSending(true);
      const response = await fetch(`${API_BASE_URL}/api/v1/teacher_messaging/conversation/${selectedConversation.student.id}/send`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ content: newMessage })
      });

      if (response.ok) {
        setNewMessage('');
        // Recharger les messages
        await fetchMessages(selectedConversation.student.id);
        // Recharger les conversations
        await fetchConversations();
      } else {
        setError('Erreur lors de l\'envoi du message');
      }
    } catch (err) {
      setError('Erreur de connexion');
    } finally {
      setSending(false);
    }
  };

  const handleConversationSelect = async (conversation: Conversation) => {
    setSelectedConversation(conversation);
    await fetchMessages(conversation.student.id);
    
    // Marquer les messages comme lus si il y a un thread
    if (conversation.thread_id) {
      try {
        await fetch(`${API_BASE_URL}/api/v1/teacher_messaging/conversation/${conversation.thread_id}/mark-read`, {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        });
        // Recharger les conversations pour mettre à jour les compteurs
        await fetchConversations();
      } catch (err) {
        console.error('Erreur lors du marquage des messages comme lus:', err);
      }
    }
  };

  const startNewConversation = async (student: Student) => {
    try {
      // Créer une nouvelle conversation
      const response = await fetch(`${API_BASE_URL}/api/v1/teacher_messaging/conversation/${student.id}`, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });

      if (response.ok) {
        const data = await response.json();
        // Créer un objet conversation pour la nouvelle conversation
        const newConversation: Conversation = {
          thread_id: data.thread_id,
          student: {
            id: student.id,
            name: student.name,
            email: student.email
          },
          last_message: null,
          unread_count: 0
        };
        
        setSelectedConversation(newConversation);
        setMessages([]);
        setShowStudentSelector(false);
        
        // Rafraîchir la liste des conversations
        await fetchConversations();
      }
    } catch (err) {
      console.error('Erreur lors de la création de la conversation:', err);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const formatTimeAgo = (timestamp: string) => {
    const now = new Date();
    const messageTime = new Date(timestamp);
    const diffInMinutes = Math.floor((now.getTime() - messageTime.getTime()) / (1000 * 60));
    
    if (diffInMinutes < 1) return "À l'instant";
    if (diffInMinutes < 60) return `Il y a ${diffInMinutes} min`;
    if (diffInMinutes < 1440) return `Il y a ${Math.floor(diffInMinutes / 60)}h`;
    return `Il y a ${Math.floor(diffInMinutes / 1440)}j`;
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  if (!isAuthenticated || !token) {
    return (
      <div className="flex min-h-screen bg-gray-50">
        <Sidebar />
        <div className="flex-1 flex items-center justify-center ml-64">
          <div className="text-center">
            <div className="text-red-600 text-xl font-bold mb-2">Non authentifié</div>
            <div className="text-gray-600">Veuillez vous connecter pour accéder aux messages</div>
          </div>
        </div>
      </div>
    );
  }

  if (loading) {
    return (
      <div className="flex min-h-screen bg-gray-50">
        <Sidebar />
        <div className="flex-1 flex items-center justify-center ml-64">
          <div className="text-blue-600 animate-pulse text-xl font-bold">Chargement des messages...</div>
        </div>
      </div>
    );
  }

  return (
    <div className="flex min-h-screen bg-gray-50">
      <Sidebar />
      <div className="flex-1 flex flex-col lg:grid lg:grid-cols-3 gap-6 p-6 ml-64">
        {/* Liste des conversations */}
        <div className="bg-white rounded-xl shadow-lg flex flex-col">
          <div className="p-4 border-b border-gray-200">
            <div className="flex items-center justify-between">
              <h2 className="text-lg font-semibold text-gray-900">Messages</h2>
              <button 
                onClick={() => setShowStudentSelector(true)}
                className="p-2 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded-lg transition"
                title="Nouvelle conversation"
              >
                <Plus size={20} />
              </button>
            </div>
            <div className="mt-3 relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" size={16} />
              <input
                type="text"
                placeholder="Rechercher..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
          </div>

          <div className="flex-1 overflow-hidden">
            {error ? (
              <div className="text-red-600 text-center py-8">{error}</div>
            ) : conversations.length === 0 ? (
              <div className="text-center py-8">
                <MessageSquare className="mx-auto text-gray-400 mb-4" size={48} />
                <p className="text-gray-600">Aucune conversation</p>
                <p className="text-sm text-gray-500">Commencez à discuter avec vos élèves</p>
              </div>
            ) : (
              <div className="space-y-2 max-h-[calc(100vh-300px)] overflow-y-auto">
                {conversations
                  .filter(conv => 
                    conv.student.name?.toLowerCase().includes(searchTerm.toLowerCase()) ||
                    conv.student.email?.toLowerCase().includes(searchTerm.toLowerCase())
                  )
                  .map((conversation) => (
                  <div
                    key={conversation.student.id}
                    onClick={() => handleConversationSelect(conversation)}
                    className={`p-3 rounded-lg cursor-pointer transition ${
                      selectedConversation?.student.id === conversation.student.id
                        ? 'bg-blue-50 border border-blue-200'
                        : 'hover:bg-gray-50'
                    }`}
                  >
                    <div className="flex items-center gap-3">
                      <div className="w-10 h-10 bg-blue-600 rounded-full flex items-center justify-center">
                        <span className="text-white text-sm font-medium">
                          {conversation.student.name?.charAt(0) || conversation.student.email?.charAt(0) || 'U'}
                        </span>
                      </div>
                      <div className="flex-1 min-w-0">
                        <p className="font-medium text-gray-900 truncate">
                          {conversation.student.name || conversation.student.email}
                        </p>
                        <p className="text-sm text-gray-500 truncate">
                          {conversation.last_message?.content || 'Aucun message'}
                        </p>
                        <div className="flex items-center gap-2 mt-1">
                          <Clock className="text-gray-400" size={12} />
                          <span className="text-xs text-gray-500">
                            {conversation.last_message?.timestamp 
                              ? formatTimeAgo(conversation.last_message.timestamp)
                              : 'Aucune activité'
                            }
                          </span>
                          {conversation.unread_count > 0 && (
                            <span className="bg-red-500 text-white text-xs rounded-full px-2 py-1">
                              {conversation.unread_count}
                            </span>
                          )}
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>

        {/* Zone de messages */}
        <div className="lg:col-span-2 bg-white rounded-xl shadow-lg flex flex-col">
          {selectedConversation ? (
            <>
              {/* Header de la conversation */}
              <div className="p-4 border-b border-gray-200">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 bg-blue-600 rounded-full flex items-center justify-center">
                    <span className="text-white text-sm font-medium">
                      {selectedConversation.student.name?.charAt(0) || selectedConversation.student.email?.charAt(0) || 'U'}
                    </span>
                  </div>
                                     <div>
                     <p className="font-medium text-gray-900">
                       {selectedConversation.student.name || selectedConversation.student.email}
                     </p>
                     <p className="text-sm text-gray-500">
                       <span className="inline-block w-2 h-2 bg-green-500 rounded-full mr-2"></span>
                       En ligne
                     </p>
                   </div>
                </div>
              </div>

              {/* Messages */}
              <div className="flex-1 p-4 overflow-y-auto max-h-[calc(100vh-400px)]">
                <div className="space-y-4">
                  {messages.length === 0 ? (
                    <div className="text-center py-8">
                      <MessageSquare className="mx-auto text-gray-400 mb-4" size={48} />
                      <p className="text-gray-600">Aucun message</p>
                      <p className="text-sm text-gray-500">Commencez la conversation</p>
                    </div>
                  ) : (
                    messages.map((message) => {
                      const isOwnMessage = message.user_id === user?.id;
                      return (
                        <div
                          key={message.id}
                          className={`flex ${isOwnMessage ? 'justify-end' : 'justify-start'}`}
                        >
                          <div
                            className={`max-w-xs lg:max-w-md px-4 py-3 rounded-lg shadow-sm ${
                              isOwnMessage
                                ? 'bg-blue-600 text-white'
                                : 'bg-gray-100 text-gray-900'
                            }`}
                          >
                            <p className="text-sm leading-relaxed">{message.content}</p>
                                                         <p className={`text-xs mt-2 ${
                               isOwnMessage ? 'text-blue-100' : 'text-gray-500'
                             }`}>
                               {formatTimeAgo(message.timestamp)}
                             </p>
                          </div>
                        </div>
                      );
                                         })
                   )}
                   <div ref={messagesEndRef} />
                 </div>
               </div>

              {/* Zone de saisie */}
              <div className="p-4 border-t border-gray-200">
                <div className="flex gap-3">
                  <input
                    type="text"
                    value={newMessage}
                    onChange={(e) => setNewMessage(e.target.value)}
                    onKeyPress={handleKeyPress}
                    placeholder="Tapez votre message..."
                    className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    disabled={sending}
                  />
                  <button
                    onClick={sendMessage}
                    disabled={!newMessage.trim() || sending}
                    className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    <Send size={16} />
                  </button>
                </div>
              </div>
            </>
          ) : (
            <div className="flex-1 flex items-center justify-center">
              <div className="text-center">
                <MessageSquare className="mx-auto text-gray-400 mb-4" size={48} />
                <p className="text-gray-600">Sélectionnez une conversation</p>
                <p className="text-sm text-gray-500">Choisissez un élève pour commencer à discuter</p>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Modal de sélection d'étudiant */}
      {showStudentSelector && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-xl p-6 w-full max-w-md max-h-[80vh] overflow-y-auto">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-semibold text-gray-900">Nouvelle conversation</h3>
              <button
                onClick={() => setShowStudentSelector(false)}
                className="text-gray-400 hover:text-gray-600"
              >
                ✕
              </button>
            </div>
            
            <div className="mb-4">
              <input
                type="text"
                placeholder="Rechercher un étudiant..."
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                onChange={(e) => setSearchTerm(e.target.value)}
              />
            </div>

            <div className="space-y-2 max-h-96 overflow-y-auto">
              {students
                .filter(student => 
                  student.name?.toLowerCase().includes(searchTerm.toLowerCase()) ||
                  student.email?.toLowerCase().includes(searchTerm.toLowerCase())
                )
                .map((student) => (
                  <div
                    key={student.id}
                    onClick={() => startNewConversation(student)}
                    className="p-3 rounded-lg cursor-pointer hover:bg-gray-50 border border-gray-200"
                  >
                    <div className="flex items-center gap-3">
                      <div className="w-10 h-10 bg-green-600 rounded-full flex items-center justify-center">
                        <span className="text-white text-sm font-medium">
                          {student.name?.charAt(0) || student.email?.charAt(0) || 'U'}
                        </span>
                      </div>
                      <div>
                        <p className="font-medium text-gray-900">
                          {student.name || student.email}
                        </p>
                        <p className="text-sm text-gray-500">
                          {student.email}
                        </p>
                      </div>
                    </div>
                  </div>
                ))}
            </div>

            {students.length === 0 && (
              <div className="text-center py-8">
                <p className="text-gray-600">Aucun étudiant trouvé</p>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
} 