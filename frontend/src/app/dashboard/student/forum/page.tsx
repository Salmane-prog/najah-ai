'use client';

import React, { useState, useEffect } from 'react';
import Sidebar from '../../../../components/Sidebar';
import { useAuth  } from '../../../../hooks/useAuth';
import NotificationBell from '../../../../components/NotificationBell';
import { forumAPI, ForumCategory, ForumThread, ForumMessage } from '../../../../api/student/forum';
import { 
  MessageCircle, 
  Plus, 
  Search, 
  Filter, 
  ThumbsUp, 
  ThumbsDown, 
  Share2, 
  Flag,
  Bookmark,
  Calendar,
  User,
  Tag,
  Eye,
  MessageSquare
} from 'lucide-react';



export default function ForumPage() {
  const { user, token } = useAuth();
  const [categories, setCategories] = useState<ForumCategory[]>([]);
  const [threads, setThreads] = useState<ForumThread[]>([]);
  const [selectedCategory, setSelectedCategory] = useState<number | null>(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [showNewThread, setShowNewThread] = useState(false);
  const [selectedThread, setSelectedThread] = useState<ForumThread | null>(null);
  const [messages, setMessages] = useState<ForumMessage[]>([]);
  const [loading, setLoading] = useState(true);

  // États pour le formulaire de création de thread
  const [newThreadForm, setNewThreadForm] = useState({
    category_id: '',
    title: '',
    content: '',
    tags: ''
  });
  const [creatingThread, setCreatingThread] = useState(false);

  // États pour le formulaire de réponse
  const [replyForm, setReplyForm] = useState({
    content: ''
  });
  const [creatingReply, setCreatingReply] = useState(false);

  useEffect(() => {
    const loadData = async () => {
      try {
        setLoading(true);
        
        // Log de débogage pour vérifier l'API
        console.log('🔍 Debug: forumAPI object:', forumAPI);
        console.log('🔍 Debug: API_BASE_URL from config:', process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1');
        
        // Charger les catégories d'abord
        try {
          const categoriesData = await forumAPI.getCategories();
          console.log('✅ Categories loaded:', categoriesData);
          setCategories(categoriesData);
        } catch (error) {
          console.error('❌ Error loading categories:', error);
          setCategories([]);
        }
        
        // Charger les threads ensuite
        try {
          const threadsData = await forumAPI.getThreads();
          console.log('✅ Threads loaded:', threadsData);
          setThreads(threadsData);
        } catch (error) {
          console.error('❌ Error loading threads:', error);
          setThreads([]);
        }
        
      } catch (error) {
        console.error('❌ Error loading forum data:', error);
        // Ne plus utiliser les données mockées - afficher une erreur claire
        setCategories([]);
        setThreads([]);
        alert('Erreur lors du chargement des données du forum. Veuillez réessayer ou contacter l\'administrateur.');
      } finally {
        setLoading(false);
      }
    };

    loadData();
  }, []);

  const filteredThreads = threads.filter(thread => {
    // Vérifier que thread.category est un objet avec une propriété name
    const categoryName = typeof thread.category === 'string' 
      ? thread.category 
      : thread.category?.name || 'Général';
    
    const matchesCategory = !selectedCategory || 
      categoryName === categories.find(c => c.id === selectedCategory)?.name;
    
    const matchesSearch = !searchTerm || 
      thread.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
      thread.content.toLowerCase().includes(searchTerm.toLowerCase()) ||
      (Array.isArray(thread.tags) && thread.tags.some(tag => tag.toLowerCase().includes(searchTerm.toLowerCase())));
    
    return matchesCategory && matchesSearch;
  });

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    const now = new Date();
    const diffInHours = (now.getTime() - date.getTime()) / (1000 * 60 * 60);
    
    if (diffInHours < 1) return 'À l\'instant';
    if (diffInHours < 24) return `Il y a ${Math.floor(diffInHours)}h`;
    if (diffInHours < 168) return `Il y a ${Math.floor(diffInHours / 24)}j`;
    return date.toLocaleDateString('fr-FR');
  };

  const handleVote = async (threadId: number, voteType: 'up' | 'down') => {
    try {
      await forumAPI.voteThread(threadId, voteType);
      // Mettre à jour l'état local après le vote
      setThreads(prev => prev.map(thread => 
        thread.id === threadId 
          ? { 
              ...thread, 
              votes: { 
                up: (thread.votes?.up || 0) + (voteType === 'up' ? 1 : 0),
                down: (thread.votes?.down || 0) + (voteType === 'down' ? 1 : 0)
              } 
            }
          : thread
      ));
    } catch (error) {
      console.error('Error voting on thread:', error);
    }
  };

  const handleMessageVote = async (messageId: number, voteType: 'up' | 'down') => {
    try {
      await forumAPI.voteMessage(messageId, voteType);
      // Mettre à jour l'état local après le vote
      setMessages(prev => prev.map(message => 
        message.id === messageId 
          ? { 
              ...message, 
              votes: { 
                up: (message.votes?.up || 0) + (voteType === 'up' ? 1 : 0),
                down: (message.votes?.down || 0) + (voteType === 'down' ? 1 : 0)
              } 
            }
          : message
      ));
    } catch (error) {
      console.error('Error voting on message:', error);
    }
  };

  const handleCreateThread = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!newThreadForm.category_id || !newThreadForm.title || !newThreadForm.content) {
      alert('Veuillez remplir tous les champs obligatoires');
      return;
    }

    try {
      setCreatingThread(true);
      
      const threadData = {
        title: newThreadForm.title,
        content: newThreadForm.content,
        category_id: parseInt(newThreadForm.category_id),
        tags: newThreadForm.tags ? JSON.stringify(newThreadForm.tags.split(',').map(tag => tag.trim()).filter(tag => tag.length > 0)) : null
      };

      const newThread = await forumAPI.createThread(threadData);
      
      // Ajouter le nouveau thread à la liste
      setThreads(prev => [newThread, ...prev]);
      
      // Réinitialiser le formulaire
      setNewThreadForm({
        category_id: '',
        title: '',
        content: '',
        tags: ''
      });
      
      // Fermer le modal
      setShowNewThread(false);
      
    } catch (error) {
      console.error('Error creating thread:', error);
      alert('Erreur lors de la création du thread');
    } finally {
      setCreatingThread(false);
    }
  };

  const handleCreateReply = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!replyForm.content.trim()) {
      alert('Veuillez entrer le contenu de votre réponse');
      return;
    }

    if (!selectedThread) {
      alert('Aucun thread sélectionné');
      return;
    }

    try {
      setCreatingReply(true);
      
      console.log('🔍 Création de réponse pour le thread:', selectedThread.id);
      console.log('🔍 Contenu de la réponse:', replyForm.content);
      
      const replyData = {
        content: replyForm.content.trim()
      };

      console.log('🔍 Données envoyées:', replyData);

      const newReply = await forumAPI.createReply(selectedThread.id, replyData);
      
      console.log('✅ Réponse créée avec succès:', newReply);
      
      // Ajouter la nouvelle réponse à la liste
      setMessages(prev => [...prev, newReply]);
      
      // Mettre à jour le compteur de réponses du thread
      setThreads(prev => prev.map(thread => 
        thread.id === selectedThread.id 
          ? { ...thread, reply_count: (thread.reply_count || 0) + 1 }
          : thread
      ));
      
      // Réinitialiser le formulaire
      setReplyForm({ content: '' });
      
      // Afficher un message de succès
      alert('Réponse ajoutée avec succès !');
      
    } catch (error) {
      console.error('❌ Erreur lors de la création de la réponse:', error);
      
      // Message d'erreur plus détaillé
      let errorMessage = 'Erreur lors de la création de la réponse';
      if (error instanceof Error) {
        errorMessage = error.message;
      }
      
      alert(`Erreur: ${errorMessage}`);
    } finally {
      setCreatingReply(false);
    }
  };

  // Charger les réponses d'un thread
  const loadThreadReplies = async (threadId: number) => {
    try {
      const threadData = await forumAPI.getThread(threadId);
      if (threadData.replies && Array.isArray(threadData.replies)) {
        setMessages(threadData.replies);
      } else {
        setMessages([]);
      }
    } catch (error) {
      console.error('Error loading thread replies:', error);
      setMessages([]);
    }
  };

  if (loading) {
    return (
      <div className="flex min-h-screen bg-gray-50">
        <Sidebar />
        <div className="flex-1 ml-56 p-8 pb-32">
          <div className="animate-pulse">
            <div className="h-8 bg-gray-200 rounded w-1/4 mb-6"></div>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {[...Array(6)].map((_, i) => (
                <div key={i} className="h-48 bg-gray-200 rounded-lg"></div>
              ))}
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="flex min-h-screen bg-gray-50">
      <Sidebar />
      <div className="flex-1 ml-56 p-8 pb-32">
        {/* Header */}
        <div className="flex justify-between items-center mb-8">
          <div>
            <h1 className="text-3xl font-bold text-gray-900 mb-2">Forum d'entraide</h1>
            <p className="text-gray-600">Posez vos questions et partagez vos connaissances</p>
          </div>
          <div className="flex items-center space-x-4">
            <NotificationBell />
            <button
              onClick={() => setShowNewThread(true)}
              className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-lg flex items-center space-x-2 transition-colors"
            >
              <Plus size={20} />
              <span>Nouveau sujet</span>
            </button>
          </div>
        </div>


        {/* Message d'erreur si pas de données */}
        {!loading && (
          <>
            {categories.length === 0 && (
              <div className="bg-red-50 border border-red-200 rounded-xl p-6 mb-6">
                <div className="flex items-center">
                  <div className="flex-shrink-0">
                    <svg className="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
                      <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                    </svg>
                  </div>
                  <div className="ml-3">
                    <h3 className="text-sm font-medium text-red-800">
                      Erreur de chargement des catégories
                    </h3>
                    <div className="mt-2 text-sm text-red-700">
                      <p>Impossible de charger les catégories du forum.</p>
                    </div>
                  </div>
                </div>
              </div>
            )}
            
            {threads.length === 0 && categories.length > 0 && (
              <div className="bg-yellow-50 border border-yellow-200 rounded-xl p-6 mb-6">
                <div className="flex items-center">
                  <div className="flex-shrink-0">
                    <svg className="h-5 w-5 text-yellow-400" viewBox="0 0 20 20" fill="currentColor">
                      <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
                    </svg>
                  </div>
                  <div className="ml-3">
                    <h3 className="text-sm font-medium text-yellow-800">
                      Aucun sujet trouvé
                    </h3>
                    <div className="mt-2 text-sm text-yellow-700">
                      <p>Les catégories sont chargées mais aucun sujet n'a été trouvé.</p>
                      <p className="mt-2">Soyez le premier à créer un sujet !</p>
                    </div>
                  </div>
                </div>
              </div>
            )}
          </>
        )}

        <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
          {/* Sidebar - Catégories */}
          <div className="lg:col-span-1">
            <div className="bg-white rounded-xl shadow-sm p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
                <Filter size={20} className="mr-2" />
                Catégories
              </h3>
              <div className="space-y-3">
                <button
                  onClick={() => setSelectedCategory(null)}
                  className={`w-full text-left px-4 py-3 rounded-lg transition-colors ${
                    selectedCategory === null 
                      ? 'bg-blue-50 text-blue-700 border border-blue-200' 
                      : 'hover:bg-gray-50'
                  }`}
                >
                  <div className="flex items-center justify-between">
                    <span className="font-medium">Toutes les catégories</span>
                    <span className="text-sm text-gray-500">{threads.length}</span>
                  </div>
                </button>
                {categories.map(category => (
                  <button
                    key={category.id}
                    onClick={() => setSelectedCategory(category.id)}
                    className={`w-full text-left px-4 py-3 rounded-lg transition-colors ${
                      selectedCategory === category.id 
                        ? 'bg-blue-50 text-blue-700 border border-blue-200' 
                        : 'hover:bg-gray-50'
                    }`}
                  >
                    <div className="flex items-center justify-between">
                      <div className="flex items-center">
                        <div className={`w-3 h-3 rounded-full ${category.color || 'bg-gray-500'} mr-3`}></div>
                        <span className="font-medium">{category.name}</span>
                      </div>
                      <span className="text-sm text-gray-500">{category.thread_count || 0}</span>
                    </div>
                  </button>
                ))}
              </div>
            </div>
          </div>

          {/* Main Content */}
          <div className="lg:col-span-3">
            {selectedThread ? (
              /* Thread Detail View */
              <div className="bg-white rounded-xl shadow-sm">
                {/* Thread Header */}
                <div className="p-6 border-b border-gray-200">
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <div className="flex items-center space-x-3 mb-3">
                        <span className={`px-3 py-1 rounded-full text-sm font-medium ${
                          (typeof selectedThread.category === 'string' ? selectedThread.category : selectedThread.category?.name) === 'Mathématiques' ? 'bg-blue-100 text-blue-700' :
                          (typeof selectedThread.category === 'string' ? selectedThread.category : selectedThread.category?.name) === 'Sciences' ? 'bg-green-100 text-green-700' :
                          (typeof selectedThread.category === 'string' ? selectedThread.category : selectedThread.category?.name) === 'Langues' ? 'bg-purple-100 text-purple-700' :
                          'bg-gray-100 text-gray-700'
                        }`}>
                          {typeof selectedThread.category === 'string' ? selectedThread.category : selectedThread.category?.name || 'Général'}
                        </span>
                        {selectedThread.is_pinned && (
                          <span className="px-2 py-1 bg-yellow-100 text-yellow-700 rounded-full text-xs">
                            Épinglé
                          </span>
                        )}
                      </div>
                      <h2 className="text-2xl font-bold text-gray-900 mb-3">{selectedThread.title}</h2>
                      <div className="flex items-center space-x-4 text-sm text-gray-500">
                        <div className="flex items-center">
                          <User size={16} className="mr-1" />
                          {selectedThread.author?.name || 'Utilisateur'}
                        </div>
                        <div className="flex items-center">
                          <Calendar size={16} className="mr-1" />
                          {formatDate(selectedThread.created_at)}
                        </div>
                        <div className="flex items-center">
                          <Eye size={16} className="mr-1" />
                          {selectedThread.view_count || selectedThread.views_count || 0} vues
                        </div>
                      </div>
                    </div>
                    <button
                      onClick={() => setSelectedThread(null)}
                      className="text-gray-400 hover:text-gray-600"
                    >
                      ×
                    </button>
                  </div>
                  <div className="mt-4 p-4 bg-gray-50 rounded-lg">
                    <p className="text-gray-700">{selectedThread.content}</p>
                    <div className="flex items-center justify-between mt-4">
                      <div className="flex items-center space-x-4">
                        <button
                          onClick={() => handleVote(selectedThread.id, 'up')}
                          className="flex items-center space-x-1 text-gray-500 hover:text-green-600"
                        >
                          <ThumbsUp size={16} />
                          <span>{selectedThread.votes?.up || 0}</span>
                        </button>
                        <button
                          onClick={() => handleVote(selectedThread.id, 'down')}
                          className="flex items-center space-x-1 text-gray-500 hover:text-red-600"
                        >
                          <ThumbsDown size={16} />
                          <span>{selectedThread.votes?.down || 0}</span>
                        </button>
                        <button className="flex items-center space-x-1 text-gray-500 hover:text-blue-600">
                          <Share2 size={16} />
                          <span>Partager</span>
                        </button>
                        <button className="flex items-center space-x-1 text-gray-500 hover:text-red-600">
                          <Flag size={16} />
                          <span>Signaler</span>
                        </button>
                      </div>
                      <div className="flex items-center space-x-2">
                        {Array.isArray(selectedThread.tags) && selectedThread.tags.map(tag => (
                          <span key={tag} className="px-2 py-1 bg-blue-100 text-blue-700 rounded-full text-xs">
                            {tag}
                          </span>
                        ))}
                      </div>
                    </div>
                  </div>
                </div>

                {/* Messages */}
                <div className="p-6">
                  <h3 className="text-lg font-semibold text-gray-900 mb-4">
                    Réponses ({messages.length})
                  </h3>
                  <div className="space-y-6">
                    {messages.map(message => (
                      <div key={message.id} className={`p-4 rounded-lg border ${
                        message.is_solution ? 'border-green-200 bg-green-50' : 'border-gray-200 bg-white'
                      }`}>
                        {message.is_solution && (
                          <div className="flex items-center mb-3">
                            <div className="bg-green-100 text-green-700 px-2 py-1 rounded-full text-xs font-medium">
                              Solution acceptée
                            </div>
                          </div>
                        )}
                        <div className="flex items-start space-x-4">
                          <div className="flex-shrink-0">
                            <div className="w-10 h-10 bg-blue-500 rounded-full flex items-center justify-center text-white font-semibold">
                              {message.author?.name?.charAt(0) || 'U'}
                            </div>
                          </div>
                          <div className="flex-1">
                            <div className="flex items-center space-x-2 mb-2">
                              <span className="font-medium text-gray-900">{message.author?.name || 'Utilisateur'}</span>
                              <span className="text-sm text-gray-500">{formatDate(message.created_at)}</span>
                            </div>
                            <p className="text-gray-700 mb-3">{message.content}</p>
                            <div className="flex items-center space-x-4">
                              <button
                                onClick={() => handleMessageVote(message.id, 'up')}
                                className="flex items-center space-x-1 text-gray-500 hover:text-green-600"
                              >
                                <ThumbsUp size={16} />
                                <span>{message.votes?.up || 0}</span>
                              </button>
                              <button
                                onClick={() => handleMessageVote(message.id, 'down')}
                                className="flex items-center space-x-1 text-gray-500 hover:text-red-600"
                              >
                                <ThumbsDown size={16} />
                                <span>{message.votes?.down || 0}</span>
                              </button>
                              <button className="flex items-center space-x-1 text-gray-500 hover:text-blue-600">
                                <MessageSquare size={16} />
                                <span>Répondre</span>
                              </button>
                              <button className="flex items-center space-x-1 text-gray-500 hover:text-red-600">
                                <Flag size={16} />
                                <span>Signaler</span>
                              </button>
                            </div>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>

                  {/* Reply Form */}
                  <div className="mt-8 p-4 border border-gray-200 rounded-lg">
                    <h4 className="font-medium text-gray-900 mb-3">Ajouter une réponse</h4>
                    <textarea
                      className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      rows={4}
                      placeholder="Tapez votre réponse..."
                      value={replyForm.content}
                      onChange={(e) => setReplyForm(prev => ({ ...prev, content: e.target.value }))}
                    ></textarea>
                    <div className="flex justify-end mt-3">
                      <button 
                        onClick={handleCreateReply}
                        className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded-lg transition-colors disabled:opacity-50"
                        disabled={creatingReply}
                      >
                        {creatingReply ? 'Création...' : 'Publier'}
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            ) : (
              /* Thread List View */
              <div className="space-y-6">
                {/* Search and Filters */}
                <div className="bg-white rounded-xl shadow-sm p-6">
                  <div className="flex items-center space-x-4">
                    <div className="flex-1 relative">
                      <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" size={20} />
                      <input
                        type="text"
                        placeholder="Rechercher dans le forum..."
                        value={searchTerm}
                        onChange={(e) => setSearchTerm(e.target.value)}
                        className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      />
                    </div>
                    <button className="px-4 py-3 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors">
                      <Filter size={20} />
                    </button>
                  </div>
                </div>

                {/* Threads List */}
                <div className="space-y-4">
                  {filteredThreads.map(thread => (
                    <div
                      key={thread.id}
                      className="bg-white rounded-xl shadow-sm p-6 hover:shadow-md transition-shadow cursor-pointer"
                      onClick={() => {
                        setSelectedThread(thread);
                        loadThreadReplies(thread.id);
                      }}
                    >
                      <div className="flex items-start justify-between">
                        <div className="flex-1">
                          <div className="flex items-center space-x-3 mb-2">
                            <span className={`px-3 py-1 rounded-full text-sm font-medium ${
                              (typeof thread.category === 'string' ? thread.category : thread.category?.name) === 'Mathématiques' ? 'bg-blue-100 text-blue-700' :
                              (typeof thread.category === 'string' ? thread.category : thread.category?.name) === 'Sciences' ? 'bg-green-100 text-green-700' :
                              (typeof thread.category === 'string' ? thread.category : thread.category?.name) === 'Langues' ? 'bg-purple-100 text-purple-700' :
                              'bg-gray-100 text-gray-700'
                            }`}>
                              {typeof thread.category === 'string' ? thread.category : thread.category?.name || 'Général'}
                            </span>
                            {thread.is_pinned && (
                              <span className="px-2 py-1 bg-yellow-100 text-yellow-700 rounded-full text-xs">
                                Épinglé
                              </span>
                            )}
                          </div>
                          <h3 className="text-lg font-semibold text-gray-900 mb-2 hover:text-blue-600">
                            {thread.title}
                          </h3>
                          <p className="text-gray-600 text-sm mb-3 line-clamp-2">
                            {thread.content}
                          </p>
                          <div className="flex items-center justify-between">
                            <div className="flex items-center space-x-4 text-sm text-gray-500">
                              <div className="flex items-center">
                                <User size={16} className="mr-1" />
                                {thread.author?.name || 'Utilisateur'}
                              </div>
                              <div className="flex items-center">
                                <Calendar size={16} className="mr-1" />
                                {formatDate(thread.created_at)}
                              </div>
                              <div className="flex items-center">
                                <MessageSquare size={16} className="mr-1" />
                                {thread.reply_count || thread.replies_count || 0} réponses
                              </div>
                              <div className="flex items-center">
                                <Eye size={16} className="mr-1" />
                                {thread.view_count || thread.views_count || 0} vues
                              </div>
                            </div>
                            <div className="flex items-center space-x-2">
                              {Array.isArray(thread.tags) && thread.tags.slice(0, 3).map(tag => (
                                <span key={tag} className="px-2 py-1 bg-blue-100 text-blue-700 rounded-full text-xs">
                                  {tag}
                                </span>
                              ))}
                              {Array.isArray(thread.tags) && thread.tags.length > 3 && (
                                <span className="px-2 py-1 bg-gray-100 text-gray-700 rounded-full text-xs">
                                  +{thread.tags.length - 3}
                                </span>
                              )}
                            </div>
                          </div>
                        </div>
                        <div className="flex items-center space-x-2 ml-4">
                          <button
                            onClick={(e) => {
                              e.stopPropagation();
                              handleVote(thread.id, 'up');
                            }}
                            className="flex items-center space-x-1 text-gray-500 hover:text-green-600"
                          >
                            <ThumbsUp size={16} />
                            <span>{thread.votes?.up || 0}</span>
                          </button>
                          <button
                            onClick={(e) => {
                              e.stopPropagation();
                              handleVote(thread.id, 'down');
                            }}
                            className="flex items-center space-x-1 text-gray-500 hover:text-red-600"
                          >
                            <ThumbsDown size={16} />
                            <span>{thread.votes?.down || 0}</span>
                          </button>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>

                {filteredThreads.length === 0 && (
                  <div className="text-center py-12">
                    <MessageCircle className="mx-auto text-gray-400 mb-4" size={48} />
                    <h3 className="text-lg font-medium text-gray-900 mb-2">Aucun sujet trouvé</h3>
                    <p className="text-gray-500">Essayez de modifier vos critères de recherche</p>
                  </div>
                )}
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Modal pour créer un nouveau sujet */}
      {showNewThread && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-xl shadow-xl p-6 w-full max-w-2xl mx-4">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-2xl font-bold text-gray-900">Nouveau sujet</h2>
              <button
                onClick={() => setShowNewThread(false)}
                className="text-gray-400 hover:text-gray-600"
              >
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
            
            <form onSubmit={handleCreateThread}>
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Catégorie
                  </label>
                  <select 
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    value={newThreadForm.category_id}
                    onChange={(e) => setNewThreadForm(prev => ({ ...prev, category_id: e.target.value }))}
                    required
                  >
                    <option value="">Sélectionner une catégorie</option>
                    {categories.map(category => (
                      <option key={category.id} value={category.id}>
                        {category.name}
                      </option>
                    ))}
                  </select>
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Titre du sujet
                  </label>
                  <input
                    type="text"
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    placeholder="Entrez le titre de votre sujet..."
                    value={newThreadForm.title}
                    onChange={(e) => setNewThreadForm(prev => ({ ...prev, title: e.target.value }))}
                    required
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Contenu
                  </label>
                  <textarea
                    rows={6}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    placeholder="Décrivez votre question ou partagez vos connaissances..."
                    value={newThreadForm.content}
                    onChange={(e) => setNewThreadForm(prev => ({ ...prev, content: e.target.value }))}
                    required
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Tags (optionnel)
                  </label>
                  <input
                    type="text"
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    placeholder="maths, équation, algèbre (séparés par des virgules)"
                    value={newThreadForm.tags}
                    onChange={(e) => setNewThreadForm(prev => ({ ...prev, tags: e.target.value }))}
                  />
                </div>
              </div>
              
              <div className="flex items-center justify-end space-x-3 mt-6">
                <button
                  type="button"
                  onClick={() => setShowNewThread(false)}
                  className="px-4 py-2 text-gray-700 bg-gray-100 rounded-lg hover:bg-gray-200 transition-colors"
                  disabled={creatingThread}
                >
                  Annuler
                </button>
                <button
                  type="submit"
                  className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50"
                  disabled={creatingThread}
                >
                  {creatingThread ? 'Création...' : 'Créer le sujet'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
} 