"use client";
import React, { useState, useEffect, useRef } from 'react';
import { useAuth  } from '../../../../hooks/useAuth';
import { Card } from '../../../../components/Card';
import Button from '../../../../components/Button';
import { Send, Search, MoreVertical, Paperclip, Smile, Phone, Video } from 'lucide-react';
import StudentNotificationBell from '../../../../components/StudentNotificationBell';
import Sidebar from '../../../../components/Sidebar';

interface Message {
  id: number;
  content: string;
  timestamp: string;
  user_id: number;
  is_teacher: boolean;
  sender_name: string;
}

interface Conversation {
  id: number;
  teacher_id: number;
  teacher_name: string;
  teacher_email: string;
  last_message: {
    content: string;
    timestamp: string;
    user_id: number;
  };
  unread_count: number;
}

const MessagesPage: React.FC = () => {
  const { user, token } = useAuth();
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [selectedConversation, setSelectedConversation] = useState<Conversation | null>(null);
  const [messages, setMessages] = useState<Message[]>([]);
  const [newMessage, setNewMessage] = useState('');
  const [searchTerm, setSearchTerm] = useState('');
  const [loading, setLoading] = useState(true);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Auto-scroll vers le bas
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Charger les conversations
  useEffect(() => {
    const fetchConversations = async () => {
      try {
        setLoading(true);
        const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/v1/student_messaging/conversations`, {
          headers: { 
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        });
        if (response.ok) {
          const data = await response.json();
          setConversations(data.conversations || []);
        } else {
          console.error('Erreur lors du chargement des conversations:', response.status);
        }
      } catch (error) {
        console.error('Erreur lors du chargement des conversations:', error);
      } finally {
        setLoading(false);
      }
    };

    if (user && token) {
      fetchConversations();
      // Auto-refresh toutes les 30 secondes
      const interval = setInterval(fetchConversations, 30000);
      return () => clearInterval(interval);
    }
  }, [user, token]);

  // Charger les messages d'une conversation
  const loadMessages = async (conversationId: number) => {
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/v1/student_messaging/conversation/${conversationId}/messages`, {
        headers: { 
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });
      if (response.ok) {
        const data = await response.json();
        setMessages(data.messages || []);
        
        // Marquer les messages comme lus
        await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/v1/student_messaging/conversation/${conversationId}/mark-read`, {
          method: 'POST',
          headers: { 
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        });
      }
    } catch (error) {
      console.error('Erreur lors du chargement des messages:', error);
    }
  };

  const handleSendMessage = async () => {
    if (!newMessage.trim() || !selectedConversation) return;

    const messageData = {
      content: newMessage
    };

    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/v1/student_messaging/conversation/${selectedConversation.id}/send`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(messageData)
      });

      if (response.ok) {
        const sentMessage = await response.json();
        setMessages(prev => [...prev, {
          id: sentMessage.message_id,
          content: newMessage,
          timestamp: sentMessage.timestamp,
          user_id: user?.id || 0,
          is_teacher: false,
          sender_name: user?.name || 'Vous'
        }]);
        setNewMessage('');
      }
    } catch (error) {
      console.error('Erreur lors de l\'envoi du message:', error);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const filteredConversations = conversations.filter(conv =>
    conv.teacher_name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const formatTime = (dateString: string) => {
    const date = new Date(dateString);
    const now = new Date();
    const diffInHours = (now.getTime() - date.getTime()) / (1000 * 60 * 60);
    
    if (diffInHours < 24) {
      return date.toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' });
    } else {
      return date.toLocaleDateString('fr-FR', { day: '2-digit', month: '2-digit' });
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

  if (!user || !token) {
    return (
      <div className="flex min-h-screen bg-gray-50">
        <Sidebar />
        <div className="flex-1 flex items-center justify-center ml-64">
          <div className="text-center">
            <h2 className="text-xl font-semibold text-gray-600">Non authentifié</h2>
            <p className="text-gray-500">Veuillez vous connecter pour accéder aux messages</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="flex min-h-screen bg-gray-50">
      <Sidebar />
      <div className="flex-1 flex ml-64">
      {/* Sidebar des conversations */}
      <div className="w-80 bg-white border-r border-gray-200 flex flex-col">
        {/* Header */}
        <div className="p-4 border-b border-gray-200">
          <h1 className="text-xl font-bold text-gray-800">Messages</h1>
          <div className="mt-3 relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
            <input
              type="text"
              placeholder="Rechercher des conversations..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
        </div>

        {/* Liste des conversations */}
        <div className="flex-1 overflow-y-auto">
          {loading ? (
            <div className="p-4 text-center text-gray-500">Chargement...</div>
          ) : filteredConversations.length === 0 ? (
            <div className="p-4 text-center text-gray-500">
              <p>Aucune conversation trouvée</p>
              <p className="text-sm mt-2">Les professeurs peuvent vous envoyer des messages ici</p>
            </div>
          ) : (
            filteredConversations.map((conversation) => (
              <div
                key={conversation.id}
                onClick={() => {
                  setSelectedConversation(conversation);
                  loadMessages(conversation.id);
                }}
                className={`p-4 border-b border-gray-100 cursor-pointer hover:bg-gray-50 transition-colors ${
                  selectedConversation?.id === conversation.id ? 'bg-blue-50 border-blue-200' : ''
                }`}
              >
                <div className="flex items-center space-x-3">
                  <div className="relative">
                    <div className="w-12 h-12 bg-gradient-to-r from-green-500 to-blue-600 rounded-full flex items-center justify-center text-white font-semibold">
                      {conversation.teacher_name.charAt(0).toUpperCase()}
                    </div>
                    <div className="absolute bottom-0 right-0 w-3 h-3 bg-green-500 border-2 border-white rounded-full"></div>
                  </div>
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center justify-between">
                      <h3 className="font-semibold text-gray-800 truncate">{conversation.teacher_name}</h3>
                      <span className="text-xs text-gray-500">
                        {conversation.last_message.timestamp ? formatTimeAgo(conversation.last_message.timestamp) : ''}
                      </span>
                    </div>
                    <p className="text-sm text-gray-600 truncate">
                      {conversation.last_message.content || 'Aucun message'}
                    </p>
                  </div>
                  {conversation.unread_count > 0 && (
                    <div className="bg-blue-500 text-white text-xs rounded-full w-5 h-5 flex items-center justify-center">
                      {conversation.unread_count}
                    </div>
                  )}
                </div>
              </div>
            ))
          )}
        </div>
      </div>

      {/* Zone de chat */}
      <div className="flex-1 flex flex-col">
        {selectedConversation ? (
          <>
            {/* Header de la conversation */}
            <div className="bg-white border-b border-gray-200 p-4 flex items-center justify-between">
              <div className="flex items-center space-x-3">
                <div className="relative">
                  <div className="w-10 h-10 bg-gradient-to-r from-green-500 to-blue-600 rounded-full flex items-center justify-center text-white font-semibold">
                    {selectedConversation.teacher_name.charAt(0).toUpperCase()}
                  </div>
                  <div className="absolute bottom-0 right-0 w-2.5 h-2.5 bg-green-500 border-2 border-white rounded-full"></div>
                </div>
                <div>
                  <h2 className="font-semibold text-gray-800">{selectedConversation.teacher_name}</h2>
                  <p className="text-sm text-gray-500">Professeur</p>
                </div>
              </div>
              <div className="flex items-center space-x-2">
                <StudentNotificationBell />
                <button className="p-2 hover:bg-gray-100 rounded-full transition-colors">
                  <MoreVertical className="w-5 h-5 text-gray-600" />
                </button>
              </div>
            </div>

            {/* Messages */}
            <div className="flex-1 overflow-y-auto p-4 space-y-4">
              {messages.length === 0 ? (
                <div className="text-center text-gray-500 py-8">
                  <p>Aucun message dans cette conversation</p>
                  <p className="text-sm mt-2">Commencez la conversation en envoyant un message</p>
                </div>
              ) : (
                messages.map((message) => (
                  <div
                    key={message.id}
                    className={`flex ${message.is_teacher ? 'justify-start' : 'justify-end'}`}
                  >
                    <div
                      className={`max-w-xs lg:max-w-md px-4 py-2 rounded-lg shadow-sm ${
                        message.is_teacher
                          ? 'bg-gray-200 text-gray-800'
                          : 'bg-blue-500 text-white'
                      }`}
                    >
                      <p className="leading-relaxed">{message.content}</p>
                      <p className={`text-xs mt-1 ${
                        message.is_teacher ? 'text-gray-500' : 'text-blue-100'
                      }`}>
                        {formatTimeAgo(message.timestamp)}
                      </p>
                    </div>
                  </div>
                ))
              )}
              <div ref={messagesEndRef} />
            </div>

            {/* Zone de saisie */}
            <div className="bg-white border-t border-gray-200 p-4">
              <div className="flex items-center space-x-2">
                <div className="flex-1 relative">
                  <input
                    type="text"
                    value={newMessage}
                    onChange={(e) => setNewMessage(e.target.value)}
                    onKeyPress={handleKeyPress}
                    placeholder="Tapez votre message..."
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />
                </div>
                <button
                  onClick={handleSendMessage}
                  disabled={!newMessage.trim()}
                  className="p-2 bg-blue-500 text-white rounded-full hover:bg-blue-600 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                >
                  <Send className="w-5 h-5" />
                </button>
              </div>
            </div>
          </>
        ) : (
          <div className="flex-1 flex items-center justify-center">
            <div className="text-center">
              <div className="w-16 h-16 bg-gray-200 rounded-full flex items-center justify-center mx-auto mb-4">
                <Search className="w-8 h-8 text-gray-400" />
              </div>
              <h3 className="text-lg font-semibold text-gray-600 mb-2">Sélectionnez une conversation</h3>
              <p className="text-gray-500">Choisissez une conversation pour commencer à discuter</p>
            </div>
          </div>
        )}
      </div>
      </div>
    </div>
  );
};

export default MessagesPage; 