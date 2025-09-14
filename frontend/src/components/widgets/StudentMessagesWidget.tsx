'use client';

import React, { useState, useEffect, useRef } from 'react';
import { MessageCircle, User, Clock, Reply, MoreVertical, AlertCircle, Search, Send, RefreshCw, ArrowRight } from 'lucide-react';
import { useAuth } from '../../hooks/useAuth';

interface Message {
  id: number;
  content: string;
  timestamp: string;
  is_teacher: boolean;
  teacher_name?: string;
  student_name?: string;
}

interface Conversation {
  id: number;
  title: string;
  last_message: string;
  last_message_timestamp: string;
  unread_count: number;
  teacher_name: string;
  subject: string;
  status: 'active' | 'resolved' | 'pending';
}

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export default function StudentMessagesWidget({ className = '' }: { className?: string }) {
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [selectedConversation, setSelectedConversation] = useState<Conversation | null>(null);
  const [messages, setMessages] = useState<Message[]>([]);
  const [newMessage, setNewMessage] = useState('');
  const [searchTerm, setSearchTerm] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [sending, setSending] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const { user, token } = useAuth();

  // Auto-scroll vers le bas
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Charger les conversations
  useEffect(() => {
    if (user?.id && token) {
      loadConversations();
      // Auto-refresh toutes les 30 secondes
      const interval = setInterval(loadConversations, 30000);
      return () => clearInterval(interval);
    }
  }, [user?.id, token]);

  const loadConversations = async () => {
    try {
      setLoading(true);
      setError(null);

      console.log('[StudentMessagesWidget] 🔐 Chargement des conversations pour l\'utilisateur:', user?.id);

      const response = await fetch(`${API_BASE_URL}/api/v1/student_messaging/conversations`, {
        headers: { 
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });

      console.log('[StudentMessagesWidget] 📊 Réponse API conversations:', response.status);

      if (response.ok) {
        const data = await response.json();
        console.log('[StudentMessagesWidget] ✅ Conversations récupérées (RAW):', JSON.stringify(data, null, 2));
        
        // Vérifier et nettoyer les données
        let conversationsData = data.conversations || data || [];
        
        // S'assurer que c'est un tableau
        if (!Array.isArray(conversationsData)) {
          console.warn('[StudentMessagesWidget] ⚠️ Les données ne sont pas un tableau:', conversationsData);
          if (conversationsData && typeof conversationsData === 'object') {
            // Si c'est un objet unique, le convertir en tableau
            conversationsData = [conversationsData];
            console.log('[StudentMessagesWidget] 🔄 Objet unique converti en tableau:', conversationsData);
          } else {
            conversationsData = [];
          }
        }
        
        // Filtrer et valider chaque conversation
        conversationsData = conversationsData.filter(conv => {
          if (!conv || typeof conv !== 'object') {
            console.warn('[StudentMessagesWidget] ⚠️ Conversation invalide:', conv);
            return false;
          }
          
          // Vérifier que toutes les propriétés requises existent
          const isValid = conv.id !== undefined && 
                         (conv.title !== undefined || conv.title === '') &&
                         (conv.teacher_name !== undefined || conv.teacher_name === '') &&
                         (conv.subject !== undefined || conv.subject === '');
          
          if (!isValid) {
            console.warn('[StudentMessagesWidget] ⚠️ Conversation avec propriétés manquantes:', conv);
          }
          
          return isValid;
        });
        
        console.log('[StudentMessagesWidget] 🔧 Conversations nettoyées et validées:', conversationsData);
        setConversations(conversationsData);
      } else {
        console.log('[StudentMessagesWidget] ❌ Erreur conversations:', response.status, response.statusText);
        // En cas d'erreur, utiliser des données simulées
        setConversations(generateMockConversations());
      }
    } catch (error) {
      console.error('[StudentMessagesWidget] 💥 Erreur lors du chargement des conversations:', error);
      setError('Erreur lors du chargement des conversations');
      // Utiliser des données simulées
      setConversations(generateMockConversations());
    } finally {
      setLoading(false);
    }
  };

  const loadMessages = async (conversationId: number) => {
    try {
      setError(null);

      console.log('[StudentMessagesWidget] 📨 Chargement des messages pour la conversation:', conversationId);

      const response = await fetch(`${API_BASE_URL}/api/v1/student_messaging/conversations/${conversationId}/messages`, {
        headers: { 
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });

      console.log('[StudentMessagesWidget] 📊 Réponse API messages:', response.status);

      if (response.ok) {
        const data = await response.json();
        console.log('[StudentMessagesWidget] ✅ Messages récupérés (RAW):', JSON.stringify(data, null, 2));
        
        // Vérifier et nettoyer les données
        let messagesData = data.messages || data || [];
        
        // S'assurer que c'est un tableau
        if (!Array.isArray(messagesData)) {
          console.warn('[StudentMessagesWidget] ⚠️ Les messages ne sont pas un tableau:', messagesData);
          if (messagesData && typeof messagesData === 'object') {
            // Si c'est un objet unique, le convertir en tableau
            messagesData = [messagesData];
            console.log('[StudentMessagesWidget] 🔄 Message unique converti en tableau:', messagesData);
          } else {
            messagesData = [];
          }
        }
        
        // Filtrer et valider chaque message
        messagesData = messagesData.filter(msg => {
          if (!msg || typeof msg !== 'object') {
            console.warn('[StudentMessagesWidget] ⚠️ Message invalide:', msg);
            return false;
          }
          
          // Vérifier que toutes les propriétés requises existent
          const isValid = msg.id !== undefined && 
                         (msg.content !== undefined || msg.content === '') &&
                         (msg.timestamp !== undefined || msg.timestamp === '') &&
                         msg.is_teacher !== undefined;
          
          if (!isValid) {
            console.warn('[StudentMessagesWidget] ⚠️ Message avec propriétés manquantes:', msg);
          }
          
          return isValid;
        });
        
        console.log('[StudentMessagesWidget] 🔧 Messages nettoyés et validés:', messagesData);
        setMessages(messagesData);
      } else {
        console.log('[StudentMessagesWidget] ❌ Erreur messages:', response.status, response.statusText);
        // En cas d'erreur, utiliser des données simulées
        setMessages(generateMockMessages(conversationId));
      }
    } catch (error) {
      console.error('[StudentMessagesWidget] 💥 Erreur lors du chargement des messages:', error);
      setError('Erreur lors du chargement des messages');
      // Utiliser des données simulées
      setMessages(generateMockMessages(conversationId));
    }
  };

  const sendMessage = async () => {
    if (!selectedConversation || !newMessage.trim()) return;

    try {
      setSending(true);
      setError(null);

      console.log('[StudentMessagesWidget] 📤 Envoi du message:', newMessage);

      const response = await fetch(`${API_BASE_URL}/api/v1/student_messaging/conversations/${selectedConversation.id}/messages`, {
        method: 'POST',
        headers: { 
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          content: newMessage,
          student_id: user?.id
        })
      });

      console.log('[StudentMessagesWidget] 📊 Réponse API envoi:', response.status);

      if (response.ok) {
        const sentMessage = await response.json();
        console.log('[StudentMessagesWidget] ✅ Message envoyé:', sentMessage);
        
        // Ajouter le message à la liste locale
        setMessages(prev => [...prev, {
          id: Date.now(),
          content: newMessage,
          timestamp: new Date().toISOString(),
          is_teacher: false,
          student_name: user?.full_name || 'Vous'
        }]);
        
        setNewMessage('');
        
        // Mettre à jour la dernière conversation
        setConversations(prev => 
          prev.map(conv => 
            conv.id === selectedConversation.id 
              ? { ...conv, last_message: newMessage, last_message_timestamp: new Date().toISOString() }
              : conv
          )
        );
      } else {
        console.log('[StudentMessagesWidget] ❌ Erreur envoi:', response.status, response.statusText);
        throw new Error('Erreur lors de l\'envoi du message');
      }
    } catch (error) {
      console.error('[StudentMessagesWidget] 💥 Erreur lors de l\'envoi:', error);
      setError('Erreur lors de l\'envoi du message');
    } finally {
      setSending(false);
    }
  };

  // Fonction de rechargement forcé
  const forceRefresh = () => {
    console.log('[StudentMessagesWidget] 🔄 Rechargement forcé des conversations');
    setError(null);
    loadConversations();
  };

  // Génération de données simulées pour le développement
  const generateMockConversations = (): Conversation[] => {
    try {
      return [
        {
          id: 1,
          title: 'Question sur le devoir de Mathématiques',
          last_message: 'Merci pour votre aide !',
          last_message_timestamp: new Date(Date.now() - 2 * 60 * 60 * 1000).toISOString(),
          unread_count: 0,
          teacher_name: 'Prof. Martin',
          subject: 'Mathématiques',
          status: 'active'
        },
        {
          id: 2,
          title: 'Clarification sur le cours de Français',
          last_message: 'Pouvez-vous m\'expliquer ce concept ?',
          last_message_timestamp: new Date(Date.now() - 1 * 60 * 60 * 1000).toISOString(),
          unread_count: 1,
          teacher_name: 'Prof. Dubois',
          subject: 'Français',
          status: 'pending'
        },
        {
          id: 3,
          title: 'Problème avec le quiz de Sciences',
          last_message: 'J\'ai terminé le quiz',
          last_message_timestamp: new Date(Date.now() - 30 * 60 * 1000).toISOString(),
          unread_count: 0,
          teacher_name: 'Prof. Bernard',
          subject: 'Sciences',
          status: 'resolved'
        }
      ];
    } catch (error) {
      console.error('[StudentMessagesWidget] 💥 Erreur lors de la génération des conversations simulées:', error);
      return [];
    }
  };

  const generateMockMessages = (conversationId: number): Message[] => {
    try {
      return [
        {
          id: 1,
          content: 'Bonjour, j\'ai une question sur le devoir de Mathématiques.',
          timestamp: new Date(Date.now() - 2 * 60 * 60 * 1000).toISOString(),
          is_teacher: false,
          student_name: user?.full_name || 'Vous'
        },
        {
          id: 2,
          content: 'Bonjour ! Je suis là pour vous aider. Quelle est votre question ?',
          timestamp: new Date(Date.now() - 1.5 * 60 * 60 * 1000).toISOString(),
          is_teacher: true,
          teacher_name: 'Prof. Martin'
        },
        {
          id: 3,
          content: 'Je ne comprends pas l\'exercice 3 de la page 45.',
          timestamp: new Date(Date.now() - 1 * 60 * 60 * 1000).toISOString(),
          is_teacher: false,
          student_name: user?.full_name || 'Vous'
        },
        {
          id: 4,
          content: 'Ah je vois ! Laissez-moi vous expliquer étape par étape...',
          timestamp: new Date(Date.now() - 30 * 60 * 1000).toISOString(),
          is_teacher: true,
          teacher_name: 'Prof. Martin'
        }
      ];
    } catch (error) {
      console.error('[StudentMessagesWidget] 💥 Erreur lors de la génération des messages simulés:', error);
      return [];
    }
  };

  const handleConversationSelect = (conversation: Conversation) => {
    setSelectedConversation(conversation);
    loadMessages(conversation.id);
  };

  const handleViewAllMessages = () => {
    // Rediriger vers la page Messages complète
    window.location.href = '/dashboard/student/messages';
  };

  const formatTimeAgo = (timestamp: string) => {
    try {
      const now = new Date();
      const messageTime = new Date(timestamp);
      
      // Vérifier si la date est valide
      if (isNaN(messageTime.getTime())) {
        return 'Date invalide';
      }
      
      const diffInMinutes = Math.floor((now.getTime() - messageTime.getTime()) / (1000 * 60));

      if (diffInMinutes < 1) return 'À l\'instant';
      if (diffInMinutes < 60) return `Il y a ${diffInMinutes} min`;
      if (diffInMinutes < 1440) return `Il y a ${Math.floor(diffInMinutes / 60)}h`;
      return `Il y a ${Math.floor(diffInMinutes / 1440)}j`;
    } catch (error) {
      return 'Date invalide';
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active':
        return 'bg-green-100 text-green-800';
      case 'pending':
        return 'bg-yellow-100 text-yellow-800';
      case 'resolved':
        return 'bg-blue-100 text-blue-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const getStatusLabel = (status: string) => {
    switch (status) {
      case 'active':
        return 'Active';
      case 'pending':
        return 'En attente';
      case 'resolved':
        return 'Résolu';
      default:
        return 'Inconnu';
    }
  };

  if (loading) {
    return (
      <div className={`card-unified ${className}`}>
        <div className="card-unified-header">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 bg-gradient-to-br from-blue-500 to-green-600 rounded-lg flex items-center justify-center">
              <MessageCircle className="w-5 h-5 text-white" />
            </div>
            <h3 className="text-lg font-semibold">Messages</h3>
          </div>
        </div>
        <div className="card-unified-body">
          <div className="flex items-center justify-center py-8">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
            <span className="ml-3 text-muted">Chargement des conversations...</span>
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className={`card-unified ${className}`}>
        <div className="card-unified-header">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 bg-gradient-to-br from-blue-500 to-green-600 rounded-lg flex items-center justify-center">
              <MessageCircle className="w-5 h-5 text-white" />
            </div>
            <h3 className="text-lg font-semibold">Messages</h3>
          </div>
        </div>
        <div className="card-unified-body">
          <div className="flex items-center justify-center py-8 text-danger">
            <AlertCircle className="w-5 h-5 mr-2" />
            {error}
          </div>
          <div className="flex justify-center mt-4">
            <button
              onClick={forceRefresh}
              className="btn-unified btn-unified-primary flex items-center gap-2"
            >
              <RefreshCw className="w-4 h-4" />
              Réessayer
            </button>
          </div>
        </div>
      </div>
    );
  }

  // Vérification finale des données avant le rendu
  if (!Array.isArray(conversations)) {
    console.error('[StudentMessagesWidget] 💥 Conversations n\'est pas un tableau:', conversations);
    setConversations([]);
    return (
      <div className={`card-unified ${className}`}>
        <div className="card-unified-header">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 bg-gradient-to-br from-blue-500 to-green-600 rounded-lg flex items-center justify-center">
              <MessageCircle className="w-5 h-5 text-white" />
            </div>
            <h3 className="text-lg font-semibold">Messages</h3>
          </div>
        </div>
        <div className="card-unified-body">
          <div className="flex items-center justify-center py-8 text-danger">
            <AlertCircle className="w-5 h-5 mr-2" />
            Erreur de format des données
          </div>
          <div className="flex justify-center mt-4">
            <button
              onClick={forceRefresh}
              className="btn-unified btn-unified-primary flex items-center gap-2"
            >
              <RefreshCw className="w-4 h-4" />
              Réessayer
            </button>
          </div>
        </div>
      </div>
    );
  }

  // Vérification supplémentaire des messages
  if (!Array.isArray(messages)) {
    console.error('[StudentMessagesWidget] 💥 Messages n\'est pas un tableau:', messages);
    setMessages([]);
  }

  return (
    <div className={`space-y-6 ${className}`}>
      {/* En-tête du widget */}
      <div className="card-unified">
        <div className="card-unified-header">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="w-8 h-8 bg-gradient-to-br from-blue-500 to-green-600 rounded-lg flex items-center justify-center">
                <MessageCircle className="w-5 h-5 text-white" />
              </div>
              <h3 className="text-lg font-semibold">Messages</h3>
            </div>
            <div className="flex items-center gap-2">
              <button
                onClick={handleViewAllMessages}
                className="btn-unified btn-unified-secondary flex items-center gap-2"
                title="Voir tous les messages"
              >
                <MessageCircle className="w-4 h-4" />
                Tous
              </button>
              <button
                onClick={forceRefresh}
                className="btn-unified btn-unified-secondary flex items-center gap-2"
                title="Actualiser les conversations"
              >
                <RefreshCw className="w-4 h-4" />
                Actualiser
              </button>
            </div>
          </div>
        </div>

        <div className="card-unified-body max-h-96 overflow-hidden">
          {/* Barre de recherche */}
          <div className="mb-4">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400" />
              <input
                type="text"
                placeholder="Rechercher des conversations..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              />
            </div>
          </div>

          {/* Liste des conversations */}
          {conversations.length > 0 ? (
            <div className="space-y-3 max-h-48 overflow-y-auto pr-2">
              {conversations
                .filter(conv => {
                  // Vérification stricte de chaque conversation
                  if (!conv || typeof conv !== 'object' || conv.id === undefined) {
                    console.warn('[StudentMessagesWidget] ⚠️ Conversation filtrée (invalide):', conv);
                    return false;
                  }
                  
                  // Vérification des propriétés requises
                  if (conv.title === undefined || conv.teacher_name === undefined || conv.subject === undefined) {
                    console.warn('[StudentMessagesWidget] ⚠️ Conversation filtrée (propriétés manquantes):', conv);
                    return false;
                  }
                  
                  // Filtrage par recherche
                  const matchesSearch = (conv.title || '').toLowerCase().includes(searchTerm.toLowerCase()) ||
                                      (conv.teacher_name || '').toLowerCase().includes(searchTerm.toLowerCase()) ||
                                      (conv.subject || '').toLowerCase().includes(searchTerm.toLowerCase());
                  
                  return matchesSearch;
                })
                .slice(0, 5)
                .map((conversation) => {
                  // Vérification finale avant le rendu
                  if (!conversation || typeof conversation !== 'object') {
                    console.error('[StudentMessagesWidget] 💥 Conversation invalide dans le map:', conversation);
                    return null;
                  }
                  
                  return (
                    <div
                      key={conversation.id}
                      className={`p-3 rounded-lg border cursor-pointer transition-all duration-200 hover:shadow-md ${
                        selectedConversation?.id === conversation.id
                          ? 'bg-blue-50 border-blue-200'
                          : 'bg-white border-gray-200 hover:border-blue-300'
                      }`}
                      onClick={() => handleConversationSelect(conversation)}
                    >
                      <div className="flex items-start justify-between mb-2">
                        <div className="flex-1">
                          <h4 className="font-semibold text-gray-800 text-sm">{conversation.title || 'Sans titre'}</h4>
                          <p className="text-xs text-gray-600">{conversation.teacher_name || 'Prof. Inconnu'} • {conversation.subject || 'Matière non définie'}</p>
                        </div>
                        <div className="flex items-center gap-2">
                          <span className={`px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(conversation.status)}`}>
                            {getStatusLabel(conversation.status)}
                          </span>
                          {conversation.unread_count > 0 && (
                            <span className="w-5 h-5 bg-red-500 text-white text-xs rounded-full flex items-center justify-center">
                              {conversation.unread_count}
                            </span>
                          )}
                        </div>
                      </div>
                      
                      <div className="flex items-center justify-between">
                        <p className="text-xs text-gray-500 truncate max-w-48">
                          {conversation.last_message || 'Aucun message'}
                        </p>
                        <span className="text-xs text-gray-400">
                          {formatTimeAgo(conversation.last_message_timestamp)}
                        </span>
                      </div>
                    </div>
                  );
                })
                .filter(Boolean) // Éliminer les valeurs null
              }
            </div>
          ) : (
            <div className="text-center py-8">
              <MessageCircle className="w-16 h-16 text-gray-300 mx-auto mb-4" />
              <p className="text-lg font-semibold text-gray-600 mb-2">Aucune conversation disponible</p>
              <p className="text-base text-gray-400">Sélectionnez une conversation pour voir les messages.</p>
            </div>
          )}

          {/* Lien vers tous les messages */}
          {conversations.length > 0 && (
            <div className="mt-6 text-center">
              <button
                onClick={handleViewAllMessages}
                className="btn-unified btn-unified-secondary flex items-center gap-2 mx-auto"
              >
                <MessageCircle className="w-4 h-4" />
                Voir toutes les conversations
                <ArrowRight className="w-4 h-4" />
              </button>
            </div>
          )}
        </div>
      </div>

      {/* Zone de messages sélectionnée */}
      {selectedConversation && (
        <div className="card-unified">
          <div className="card-unified-header">
            <div className="flex items-center justify-between">
              <div>
                <h4 className="font-semibold text-gray-800">{selectedConversation.title || 'Sans titre'}</h4>
                <p className="text-sm text-gray-600">{selectedConversation.teacher_name || 'Prof. Inconnu'} • {selectedConversation.subject || 'Matière non définie'}</p>
              </div>
              <button
                onClick={() => setSelectedConversation(null)}
                className="text-gray-400 hover:text-gray-600"
              >
                ✕
              </button>
            </div>
          </div>

          <div className="card-unified-body max-h-64 overflow-hidden">
            {/* Messages */}
            <div className="flex-1 overflow-y-auto p-4 space-y-4 max-h-32">
              {messages.length === 0 ? (
                <div className="text-center text-gray-500 py-4">
                  <p>Aucun message dans cette conversation</p>
                  <p className="text-sm mt-2">Commencez la conversation en envoyant un message</p>
                </div>
              ) : (
                messages
                  .filter(msg => {
                    // Vérification stricte de chaque message
                    if (!msg || typeof msg !== 'object' || msg.id === undefined) {
                      console.warn('[StudentMessagesWidget] ⚠️ Message filtré (invalide):', msg);
                      return false;
                    }
                    
                    // Vérification des propriétés requises
                    if (msg.content === undefined || msg.timestamp === undefined || msg.is_teacher === undefined) {
                      console.warn('[StudentMessagesWidget] ⚠️ Message filtré (propriétés manquantes):', msg);
                      return false;
                    }
                    
                    return true;
                  })
                  .map((message) => {
                    // Vérification finale avant le rendu
                    if (!message || typeof message !== 'object') {
                      console.error('[StudentMessagesWidget] 💥 Message invalide dans le map:', message);
                      return null;
                    }
                    
                    return (
                      <div
                        key={message.id}
                        className={`flex ${message.is_teacher ? 'justify-start' : 'justify-end'}`}
                      >
                        <div
                          className={`max-w-xs px-4 py-2 rounded-lg shadow-sm ${
                            message.is_teacher
                              ? 'bg-gray-200 text-gray-800'
                              : 'bg-blue-500 text-white'
                          }`}
                        >
                          <p className="text-sm leading-relaxed">{message.content || 'Message vide'}</p>
                          <p className={`text-xs mt-1 ${
                            message.is_teacher ? 'text-gray-500' : 'text-blue-100'
                          }`}>
                            {formatTimeAgo(message.timestamp || new Date().toISOString())}
                          </p>
                        </div>
                      </div>
                    );
                  })
                  .filter(Boolean) // Éliminer les valeurs null
              )}
              <div ref={messagesEndRef} />
            </div>

            {/* Zone de saisie */}
            <div className="p-4 border-t border-gray-200">
              <div className="flex gap-2">
                <input
                  type="text"
                  value={newMessage}
                  onChange={(e) => setNewMessage(e.target.value)}
                  placeholder="Écrire un message..."
                  className="flex-1 border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
                  disabled={sending}
                />
                <button
                  onClick={sendMessage}
                  disabled={sending || !newMessage.trim()}
                  className="px-4 py-2 bg-blue-600 text-white rounded-lg font-semibold hover:bg-blue-700 transition disabled:opacity-50 flex items-center gap-2"
                >
                  <Send className="w-4 h-4" />
                  Envoyer
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
