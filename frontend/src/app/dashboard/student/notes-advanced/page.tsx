'use client';

import React, { useState, useEffect } from 'react';
import Sidebar from '../../../../components/Sidebar';
import { useAuth  } from '../../../../hooks/useAuth';
import NotificationBell from '../../../../components/NotificationBell';
import { notesAPI, Note, Attachment, Subject, Chapter } from '../../../../api/student/notes';
import { 
  Plus, 
  Search, 
  Filter, 
  BookOpen, 
  Tag, 
  Share2, 
  Download, 
  Edit3, 
  Trash2, 
  Eye,
  Calendar,
  User,
  Star,
  Folder,
  FileText,
  Image,
  Link,
  Bold,
  Italic,
  Underline,
  List,
  ListOrdered,
  Quote,
  Code,
  Palette,
  Save,
  MoreVertical
} from 'lucide-react';



export default function AdvancedNotesPage() {
  const { user, token } = useAuth();
  const [notes, setNotes] = useState<Note[]>([]);
  const [subjects, setSubjects] = useState<Subject[]>([]);
  const [chapters, setChapters] = useState<Chapter[]>([]);
  const [selectedNote, setSelectedNote] = useState<Note | null>(null);
  const [isEditing, setIsEditing] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedSubject, setSelectedSubject] = useState<number | null>(null);
  const [selectedChapter, setSelectedChapter] = useState<number | null>(null);
  const [showNewNote, setShowNewNote] = useState(false);
  const [loading, setLoading] = useState(true);
  const [newNoteForm, setNewNoteForm] = useState({
    title: '',
    content: '',
    subject_id: 0,
    chapter_id: 0,
    tags: [] as string[],
    color: '#3B82F6'
  });
  const [creatingNote, setCreatingNote] = useState(false);

  // Données mockées
  const mockSubjects: Subject[] = [
    { id: 1, name: 'Mathématiques', color: 'bg-blue-500', note_count: 12 },
    { id: 2, name: 'Sciences', color: 'bg-green-500', note_count: 8 },
    { id: 3, name: 'Français', color: 'bg-purple-500', note_count: 15 },
    { id: 4, name: 'Histoire', color: 'bg-orange-500', note_count: 6 },
    { id: 5, name: 'Anglais', color: 'bg-red-500', note_count: 9 },
  ];

  const mockChapters: Chapter[] = [
    { id: 1, name: 'Équations du second degré', subject_id: 1, note_count: 4 },
    { id: 2, name: 'Fonctions', subject_id: 1, note_count: 3 },
    { id: 3, name: 'Géométrie', subject_id: 1, note_count: 5 },
    { id: 4, name: 'Photosynthèse', subject_id: 2, note_count: 2 },
    { id: 5, name: 'Électricité', subject_id: 2, note_count: 3 },
    { id: 6, name: 'Grammaire', subject_id: 3, note_count: 7 },
    { id: 7, name: 'Littérature', subject_id: 3, note_count: 8 },
  ];

  const mockNotes: Note[] = [
    {
      id: 1,
      title: 'Résolution des équations du second degré',
      content: `<h2>Équations du second degré</h2>
<p>Une équation du second degré est de la forme : <strong>ax² + bx + c = 0</strong></p>
<h3>Méthode de résolution :</h3>
<ol>
<li>Calculer le discriminant : <em>Δ = b² - 4ac</em></li>
<li>Si Δ > 0 : deux solutions réelles</li>
<li>Si Δ = 0 : une solution double</li>
<li>Si Δ < 0 : pas de solution réelle</li>
</ol>
<h3>Exemple :</h3>
<p>Résoudre x² + 5x + 6 = 0</p>
<ul>
<li>a = 1, b = 5, c = 6</li>
<li>Δ = 25 - 24 = 1</li>
<li>x = (-5 ± √1) / 2</li>
<li>x₁ = -2 et x₂ = -3</li>
</ul>`,
      subject: 'Mathématiques',
      chapter: 'Équations du second degré',
      tags: ['équation', 'second degré', 'discriminant'],
      created_at: '2024-01-15T10:30:00Z',
      updated_at: '2024-01-15T14:20:00Z',
      is_favorite: true,
      is_shared: true,
      shared_with: ['Thomas L.', 'Sophie M.'],
      version: 3,
      color: 'bg-blue-100',
      attachments: [
        { id: 1, name: 'formule-discriminant.png', type: 'image', url: '/images/formule-discriminant.png' },
        { id: 2, name: 'exercices-equations.pdf', type: 'document', url: '/documents/exercices-equations.pdf', size: '2.3 MB' }
      ]
    },
    {
      id: 2,
      title: 'Processus de photosynthèse',
      content: `<h2>La photosynthèse</h2>
<p>La photosynthèse est le processus par lequel les plantes convertissent l'énergie lumineuse en énergie chimique.</p>
<h3>Équation générale :</h3>
<p><strong>6CO₂ + 6H₂O + lumière → C₆H₁₂O₆ + 6O₂</strong></p>
<h3>Étapes principales :</h3>
<ol>
<li><strong>Phase photochimique :</strong> Absorption de la lumière</li>
<li><strong>Phase chimique :</strong> Réduction du CO₂</li>
</ol>
<h3>Facteurs influençant la photosynthèse :</h3>
<ul>
<li>Intensité lumineuse</li>
<li>Concentration en CO₂</li>
<li>Température</li>
<li>Disponibilité en eau</li>
</ul>`,
      subject: 'Sciences',
      chapter: 'Photosynthèse',
      tags: ['biologie', 'photosynthèse', 'plantes'],
      created_at: '2024-01-14T15:45:00Z',
      updated_at: '2024-01-14T16:30:00Z',
      is_favorite: false,
      is_shared: false,
      shared_with: [],
      version: 2,
      color: 'bg-green-100',
      attachments: [
        { id: 3, name: 'schema-photosynthese.png', type: 'image', url: '/images/schema-photosynthese.png' }
      ]
    },
    {
      id: 3,
      title: 'Conjugaison du verbe être',
      content: `<h2>Conjugaison du verbe "être"</h2>
<p>Le verbe être est un verbe irrégulier très important en français.</p>
<h3>Présent de l'indicatif :</h3>
<table>
<tr><td>Je</td><td>suis</td></tr>
<tr><td>Tu</td><td>es</td></tr>
<tr><td>Il/Elle</td><td>est</td></tr>
<tr><td>Nous</td><td>sommes</td></tr>
<tr><td>Vous</td><td>êtes</td></tr>
<tr><td>Ils/Elles</td><td>sont</td></tr>
</table>
<h3>Utilisations principales :</h3>
<ul>
<li>État : <em>Je suis fatigué</em></li>
<li>Identité : <em>Je suis étudiant</em></li>
<li>Localisation : <em>Je suis à l'école</em></li>
</ul>`,
      subject: 'Français',
      chapter: 'Grammaire',
      tags: ['conjugaison', 'grammaire', 'verbe être'],
      created_at: '2024-01-13T09:20:00Z',
      updated_at: '2024-01-13T11:15:00Z',
      is_favorite: true,
      is_shared: true,
      shared_with: ['Marie D.'],
      version: 4,
      color: 'bg-purple-100',
      attachments: []
    }
  ];

  useEffect(() => {
    const loadData = async () => {
      try {
        setLoading(true);
        
        // Initialiser avec des tableaux vides par sécurité
        setNotes([]);
        setSubjects([]);
        setChapters([]);
        
        const [subjectsData, chaptersData, notesData] = await Promise.all([
          notesAPI.getSubjects(),
          notesAPI.getChapters(),
          notesAPI.getNotes()
        ]);
        
        // Vérifier que les données sont des tableaux
        if (Array.isArray(subjectsData)) {
          setSubjects(subjectsData);
        } else {
          console.warn('Subjects data is not an array:', subjectsData);
          setSubjects(mockSubjects);
        }
        
        if (Array.isArray(chaptersData)) {
          setChapters(chaptersData);
        } else {
          console.warn('Chapters data is not an array:', chaptersData);
          setChapters(mockChapters);
        }
        
        if (Array.isArray(notesData)) {
          setNotes(notesData);
        } else {
          console.warn('Notes data is not an array:', notesData);
          setNotes(mockNotes);
        }
        
      } catch (error) {
        console.error('Error loading notes data:', error);
        // Fallback aux données mockées en cas d'erreur
        setSubjects(mockSubjects);
        setChapters(mockChapters);
        setNotes(mockNotes);
      } finally {
        setLoading(false);
      }
    };

    loadData();
  }, []);

  const filteredNotes = (notes || []).filter(note => {
    const matchesSubject = !selectedSubject || note.subject_id === selectedSubject;
    const matchesChapter = !selectedChapter || note.chapter_id === selectedChapter;
    const matchesSearch = !searchTerm || 
      note.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
      note.content.toLowerCase().includes(searchTerm.toLowerCase()) ||
      (note.tags && note.tags.some(tag => tag.toLowerCase().includes(searchTerm.toLowerCase())));
    return matchesSubject && matchesChapter && matchesSearch;
  });

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('fr-FR', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const handleFavorite = async (noteId: number) => {
    try {
      await notesAPI.toggleFavorite(noteId);
      // Mettre à jour l'état local après le changement
      setNotes(prev => prev.map(note => 
        note.id === noteId ? { ...note, is_favorite: !note.is_favorite } : note
      ));
    } catch (error) {
      console.error('Error toggling favorite:', error);
    }
  };

  const handleShare = async (noteId: number) => {
    try {
      await notesAPI.toggleShare(noteId);
      // Mettre à jour l'état local après le changement
      setNotes(prev => prev.map(note => 
        note.id === noteId ? { ...note, is_shared: !note.is_shared } : note
      ));
    } catch (error) {
      console.error('Error toggling share:', error);
    }
  };

  const handleDelete = async (noteId: number) => {
    try {
      await notesAPI.deleteNote(noteId);
      setNotes(prev => prev.filter(note => note.id !== noteId));
      if (selectedNote?.id === noteId) {
        setSelectedNote(null);
      }
    } catch (error) {
      console.error('Error deleting note:', error);
    }
  };

  const handleCreateNote = async () => {
    if (!newNoteForm.title || !newNoteForm.content || !newNoteForm.subject_id) {
      alert('Veuillez remplir tous les champs obligatoires');
      return;
    }

    setCreatingNote(true);
    try {
      console.log('Création de note avec les données:', newNoteForm);
      
      const newNote = await notesAPI.createNote({
        title: newNoteForm.title,
        content: newNoteForm.content,
        subject_id: newNoteForm.subject_id,
        chapter_id: newNoteForm.chapter_id || 1,  // Valeur par défaut si pas de chapitre
        tags: newNoteForm.tags,
        color: newNoteForm.color
      });

      console.log('Note créée avec succès:', newNote);
      
      setNotes(prev => [newNote, ...prev]);
      setShowNewNote(false);
      setNewNoteForm({
        title: '',
        content: '',
        subject_id: 0,
        chapter_id: 0,
        tags: [],
        color: '#3B82F6'
      });
    } catch (error) {
      console.error('Erreur détaillée lors de la création:', error);
      
      // Afficher des détails sur l'erreur
      let errorMessage = 'Erreur lors de la création de la note';
      if (error instanceof Error) {
        errorMessage += `: ${error.message}`;
      }
      
      alert(errorMessage);
    } finally {
      setCreatingNote(false);
    }
  };

  const handleAddTag = (tag: string) => {
    if (tag && !newNoteForm.tags.includes(tag)) {
      setNewNoteForm(prev => ({
        ...prev,
        tags: [...prev.tags, tag]
      }));
    }
  };

  const handleRemoveTag = (tagToRemove: string) => {
    setNewNoteForm(prev => ({
      ...prev,
      tags: prev.tags.filter(tag => tag !== tagToRemove)
    }));
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
            <h1 className="text-3xl font-bold text-gray-900 mb-2">Mes Notes Avancées</h1>
            <p className="text-gray-600">Organisez et partagez vos notes avec un éditeur riche</p>
          </div>
          <div className="flex items-center space-x-4">
            <NotificationBell />
            <button
              onClick={() => setShowNewNote(true)}
              className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-lg flex items-center space-x-2 transition-colors"
            >
              <Plus size={20} />
              <span>Nouvelle note</span>
            </button>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
          {/* Sidebar - Filtres */}
          <div className="lg:col-span-1 space-y-6">
            {/* Recherche */}
            <div className="bg-white rounded-xl shadow-sm p-6">
              <div className="relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" size={20} />
                <input
                  type="text"
                  placeholder="Rechercher dans les notes..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>
            </div>

            {/* Matières */}
            <div className="bg-white rounded-xl shadow-sm p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
                <BookOpen size={20} className="mr-2" />
                Matières
              </h3>
              <div className="space-y-3">
                <button
                  onClick={() => setSelectedSubject(null)}
                  className={`w-full text-left px-4 py-3 rounded-lg transition-colors ${
                    selectedSubject === null 
                      ? 'bg-blue-50 text-blue-700 border border-blue-200' 
                      : 'hover:bg-gray-50'
                  }`}
                >
                  <div className="flex items-center justify-between">
                    <span className="font-medium">Toutes les matières</span>
                    <span className="text-sm text-gray-500">{notes.length}</span>
                  </div>
                </button>
                {subjects.map(subject => (
                  <button
                    key={subject.id}
                    onClick={() => setSelectedSubject(subject.id)}
                    className={`w-full text-left px-4 py-3 rounded-lg transition-colors ${
                      selectedSubject === subject.id 
                        ? 'bg-blue-50 text-blue-700 border border-blue-200' 
                        : 'hover:bg-gray-50'
                    }`}
                  >
                    <div className="flex items-center justify-between">
                      <div className="flex items-center">
                        <div className={`w-3 h-3 rounded-full ${subject.color} mr-3`}></div>
                        <span className="font-medium">{subject.name}</span>
                      </div>
                      <span className="text-sm text-gray-500">{subject.note_count}</span>
                    </div>
                  </button>
                ))}
              </div>
            </div>

            {/* Chapitres */}
            {selectedSubject && (
              <div className="bg-white rounded-xl shadow-sm p-6">
                <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
                  <Folder size={20} className="mr-2" />
                  Chapitres
                </h3>
                <div className="space-y-3">
                  <button
                    onClick={() => setSelectedChapter(null)}
                    className={`w-full text-left px-4 py-3 rounded-lg transition-colors ${
                      selectedChapter === null 
                        ? 'bg-blue-50 text-blue-700 border border-blue-200' 
                        : 'hover:bg-gray-50'
                    }`}
                  >
                    <span className="font-medium">Tous les chapitres</span>
                  </button>
                  {chapters
                    .filter(chapter => chapter.subject_id === selectedSubject)
                    .map(chapter => (
                      <button
                        key={chapter.id}
                        onClick={() => setSelectedChapter(chapter.id)}
                        className={`w-full text-left px-4 py-3 rounded-lg transition-colors ${
                          selectedChapter === chapter.id 
                            ? 'bg-blue-50 text-blue-700 border border-blue-200' 
                            : 'hover:bg-gray-50'
                        }`}
                      >
                        <div className="flex items-center justify-between">
                          <span className="font-medium">{chapter.name}</span>
                          <span className="text-sm text-gray-500">{chapter.note_count}</span>
                        </div>
                      </button>
                    ))}
                </div>
              </div>
            )}
          </div>

          {/* Main Content */}
          <div className="lg:col-span-3">
            {selectedNote ? (
              /* Note Detail View */
              <div className="bg-white rounded-xl shadow-sm">
                {/* Note Header */}
                <div className="p-6 border-b border-gray-200">
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <div className="flex items-center space-x-3 mb-3">
                        <span className={`px-3 py-1 rounded-full text-sm font-medium ${
                          subjects.find(s => s.id === selectedNote.subject_id)?.name === 'Mathématiques' ? 'bg-blue-100 text-blue-700' :
                          subjects.find(s => s.id === selectedNote.subject_id)?.name === 'Sciences' ? 'bg-green-100 text-green-700' :
                          subjects.find(s => s.id === selectedNote.subject_id)?.name === 'Français' ? 'bg-purple-100 text-purple-700' :
                          'bg-gray-100 text-gray-700'
                        }`}>
                          {subjects.find(s => s.id === selectedNote.subject_id)?.name || 'Matière inconnue'}
                        </span>
                        <span className="px-3 py-1 bg-gray-100 text-gray-700 rounded-full text-sm">
                          {chapters.find(c => c.id === selectedNote.chapter_id)?.name || 'Chapitre inconnu'}
                        </span>
                        {selectedNote.is_favorite && (
                          <Star className="text-yellow-500" size={16} />
                        )}
                      </div>
                      <h2 className="text-2xl font-bold text-gray-900 mb-3">{selectedNote.title}</h2>
                      <div className="flex items-center space-x-4 text-sm text-gray-500">
                        <div className="flex items-center">
                          <Calendar size={16} className="mr-1" />
                          Modifié le {formatDate(selectedNote.updated_at)}
                        </div>
                        <div className="flex items-center">
                          <FileText size={16} className="mr-1" />
                          Version {selectedNote.version}
                        </div>
                        {selectedNote.is_shared && (
                          <div className="flex items-center">
                            <Share2 size={16} className="mr-1" />
                            Partagé avec {selectedNote.shared_with ? selectedNote.shared_with.length : 0} personne(s)
                          </div>
                        )}
                      </div>
                    </div>
                    <div className="flex items-center space-x-2">
                      <button
                        onClick={() => setIsEditing(!isEditing)}
                        className="p-2 text-gray-500 hover:text-blue-600 rounded-lg hover:bg-gray-100"
                      >
                        <Edit3 size={20} />
                      </button>
                      <button
                        onClick={() => handleFavorite(selectedNote.id)}
                        className={`p-2 rounded-lg ${
                          selectedNote.is_favorite 
                            ? 'text-yellow-500 bg-yellow-50' 
                            : 'text-gray-500 hover:text-yellow-500 hover:bg-gray-100'
                        }`}
                      >
                        <Star size={20} />
                      </button>
                      <button
                        onClick={() => handleShare(selectedNote.id)}
                        className={`p-2 rounded-lg ${
                          selectedNote.is_shared 
                            ? 'text-blue-500 bg-blue-50' 
                            : 'text-gray-500 hover:text-blue-500 hover:bg-gray-100'
                        }`}
                      >
                        <Share2 size={20} />
                      </button>
                      <button
                        onClick={() => handleDelete(selectedNote.id)}
                        className="p-2 text-gray-500 hover:text-red-600 rounded-lg hover:bg-gray-100"
                      >
                        <Trash2 size={20} />
                      </button>
                      <button
                        onClick={() => setSelectedNote(null)}
                        className="text-gray-400 hover:text-gray-600"
                      >
                        ×
                      </button>
                    </div>
                  </div>

                  {/* Tags */}
                  {selectedNote.tags && selectedNote.tags.length > 0 && (
                    <div className="flex items-center space-x-2 mt-4">
                      {selectedNote.tags.map(tag => (
                        <span key={tag} className="px-2 py-1 bg-blue-100 text-blue-700 rounded-full text-xs">
                          {tag}
                        </span>
                      ))}
                    </div>
                  )}

                  {/* Attachments */}
                  {selectedNote.attachments && selectedNote.attachments.length > 0 && (
                    <div className="mt-4">
                      <h4 className="font-medium text-gray-900 mb-2">Pièces jointes</h4>
                      <div className="flex items-center space-x-4">
                        {selectedNote.attachments.map(attachment => (
                          <div key={attachment.id} className="flex items-center space-x-2 p-2 bg-gray-50 rounded-lg">
                            {attachment.type === 'image' && <Image size={16} className="text-blue-500" />}
                            {attachment.type === 'document' && <FileText size={16} className="text-green-500" />}
                            {attachment.type === 'link' && <Link size={16} className="text-purple-500" />}
                            <span className="text-sm text-gray-700">{attachment.name}</span>
                            {attachment.size && (
                              <span className="text-xs text-gray-500">({attachment.size})</span>
                            )}
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </div>

                {/* Note Content */}
                <div className="p-6">
                  {isEditing ? (
                    <div>
                      <div className="mb-4">
                        <input
                          type="text"
                          value={selectedNote.title}
                          className="w-full text-2xl font-bold text-gray-900 border-none focus:ring-0 p-0"
                          placeholder="Titre de la note..."
                        />
                      </div>
                      
                      {/* Toolbar */}
                      <div className="flex items-center space-x-2 mb-4 p-2 bg-gray-50 rounded-lg">
                        <button className="p-2 hover:bg-gray-200 rounded">
                          <Bold size={16} />
                        </button>
                        <button className="p-2 hover:bg-gray-200 rounded">
                          <Italic size={16} />
                        </button>
                        <button className="p-2 hover:bg-gray-200 rounded">
                          <Underline size={16} />
                        </button>
                        <div className="w-px h-6 bg-gray-300"></div>
                        <button className="p-2 hover:bg-gray-200 rounded">
                          <List size={16} />
                        </button>
                        <button className="p-2 hover:bg-gray-200 rounded">
                          <ListOrdered size={16} />
                        </button>
                        <button className="p-2 hover:bg-gray-200 rounded">
                          <Quote size={16} />
                        </button>
                        <button className="p-2 hover:bg-gray-200 rounded">
                          <Code size={16} />
                        </button>
                        <div className="w-px h-6 bg-gray-300"></div>
                        <button className="p-2 hover:bg-gray-200 rounded">
                          <Image size={16} />
                        </button>
                        <button className="p-2 hover:bg-gray-200 rounded">
                          <Link size={16} />
                        </button>
                        <button className="p-2 hover:bg-gray-200 rounded">
                          <Palette size={16} />
                        </button>
                      </div>

                      <textarea
                        value={selectedNote.content}
                        className="w-full h-96 p-4 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        placeholder="Tapez votre note..."
                      />
                      
                      <div className="flex justify-end mt-4 space-x-3">
                        <button
                          onClick={() => setIsEditing(false)}
                          className="px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50"
                        >
                          Annuler
                        </button>
                        <button className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 flex items-center space-x-2">
                          <Save size={16} />
                          <span>Sauvegarder</span>
                        </button>
                      </div>
                    </div>
                  ) : (
                    <div 
                      className="prose max-w-none"
                      dangerouslySetInnerHTML={{ __html: selectedNote.content }}
                    />
                  )}
                </div>
              </div>
            ) : (
              /* Notes List View */
              <div className="space-y-6">
                {/* Notes Grid */}
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                  {filteredNotes.map(note => (
                    <div
                      key={note.id}
                      className={`bg-white rounded-xl shadow-sm p-6 hover:shadow-md transition-shadow cursor-pointer border-l-4 ${
                        subjects.find(s => s.id === note.subject_id)?.name === 'Mathématiques' ? 'border-l-blue-500' :
                        subjects.find(s => s.id === note.subject_id)?.name === 'Sciences' ? 'border-l-green-500' :
                        subjects.find(s => s.id === note.subject_id)?.name === 'Français' ? 'border-l-purple-500' :
                        subjects.find(s => s.id === note.subject_id)?.name === 'Histoire' ? 'border-l-orange-500' :
                        'border-l-red-500'
                      }`}
                      onClick={() => setSelectedNote(note)}
                    >
                      <div className="flex items-start justify-between mb-3">
                        <div className="flex-1">
                          <div className="flex items-center space-x-2 mb-2">
                            <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                              subjects.find(s => s.id === note.subject_id)?.name === 'Mathématiques' ? 'bg-blue-100 text-blue-700' :
                              subjects.find(s => s.id === note.subject_id)?.name === 'Sciences' ? 'bg-green-100 text-green-700' :
                              subjects.find(s => s.id === note.subject_id)?.name === 'Français' ? 'bg-purple-100 text-purple-700' :
                              'bg-gray-100 text-gray-700'
                            }`}>
                              {subjects.find(s => s.id === note.subject_id)?.name || 'Matière inconnue'}
                            </span>
                            {note.is_favorite && (
                              <Star className="text-yellow-500" size={14} />
                            )}
                            {note.is_shared && (
                              <Share2 className="text-blue-500" size={14} />
                            )}
                          </div>
                          <h3 className="text-lg font-semibold text-gray-900 mb-2 line-clamp-2">
                            {note.title}
                          </h3>
                          <p className="text-gray-600 text-sm mb-3 line-clamp-3">
                            {note.content.replace(/<[^>]*>/g, '')}
                          </p>
                        </div>
                        <button className="text-gray-400 hover:text-gray-600">
                          <MoreVertical size={16} />
                        </button>
                      </div>
                      
                      <div className="flex items-center justify-between">
                        <div className="flex items-center space-x-4 text-xs text-gray-500">
                          <div className="flex items-center">
                            <Calendar size={12} className="mr-1" />
                            {formatDate(note.updated_at)}
                          </div>
                          <div className="flex items-center">
                            <FileText size={12} className="mr-1" />
                            v{note.version}
                          </div>
                          {note.attachments && note.attachments.length > 0 && (
                            <div className="flex items-center">
                              <Image size={12} className="mr-1" />
                              {note.attachments.length}
                            </div>
                          )}
                        </div>
                        <div className="flex items-center space-x-1">
                          {note.tags && note.tags.slice(0, 2).map(tag => (
                            <span key={tag} className="px-1 py-0.5 bg-blue-100 text-blue-700 rounded text-xs">
                              {tag}
                            </span>
                          ))}
                          {note.tags && note.tags.length > 2 && (
                            <span className="px-1 py-0.5 bg-gray-100 text-gray-700 rounded text-xs">
                              +{note.tags.length - 2}
                            </span>
                          )}
                        </div>
                      </div>
                    </div>
                  ))}
                </div>

                {filteredNotes.length === 0 && (
                  <div className="text-center py-12">
                    <FileText className="mx-auto text-gray-400 mb-4" size={48} />
                    <h3 className="text-lg font-medium text-gray-900 mb-2">Aucune note trouvée</h3>
                    <p className="text-gray-500">Essayez de modifier vos critères de recherche</p>
                  </div>
                )}
              </div>
            )}
          </div>
        </div>

        {/* Modal pour créer une nouvelle note */}
        {showNewNote && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
            <div className="bg-white rounded-xl shadow-xl w-full max-w-4xl max-h-[90vh] overflow-y-auto">
              <div className="p-6 border-b border-gray-200">
                <div className="flex items-center justify-between">
                  <h2 className="text-2xl font-bold text-gray-900">Créer une nouvelle note</h2>
                  <button
                    onClick={() => setShowNewNote(false)}
                    className="text-gray-400 hover:text-gray-600 text-2xl"
                  >
                    ×
                  </button>
                </div>
              </div>

              <div className="p-6">
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                  {/* Formulaire principal */}
                  <div className="space-y-6">
                    {/* Titre */}
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Titre *
                      </label>
                      <input
                        type="text"
                        value={newNoteForm.title}
                        onChange={(e) => setNewNoteForm(prev => ({ ...prev, title: e.target.value }))}
                        className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        placeholder="Titre de la note"
                      />
                    </div>

                    {/* Matière */}
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Matière *
                      </label>
                      <select
                        value={newNoteForm.subject_id}
                        onChange={(e) => setNewNoteForm(prev => ({ ...prev, subject_id: parseInt(e.target.value, 10) }))}
                        className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      >
                        <option value="">Sélectionner une matière</option>
                        {subjects.map(subject => (
                          <option key={subject.id} value={subject.id}>
                            {subject.name}
                          </option>
                        ))}
                      </select>
                    </div>

                    {/* Chapitre */}
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Chapitre
                      </label>
                      <select
                        value={newNoteForm.chapter_id}
                        onChange={(e) => setNewNoteForm(prev => ({ ...prev, chapter_id: parseInt(e.target.value, 10) }))}
                        className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        placeholder="Chapitre (optionnel)"
                      >
                        <option value="">Sélectionner un chapitre</option>
                        {chapters
                          .filter(chapter => chapter.subject_id === newNoteForm.subject_id)
                          .map(chapter => (
                            <option key={chapter.id} value={chapter.id}>
                              {chapter.name}
                            </option>
                          ))}
                      </select>
                    </div>

                    {/* Tags */}
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Tags
                      </label>
                      <div className="space-y-3">
                        <div className="flex items-center space-x-2">
                          <input
                            type="text"
                            placeholder="Ajouter un tag"
                            onKeyPress={(e) => {
                              if (e.key === 'Enter') {
                                e.preventDefault();
                                const input = e.target as HTMLInputElement;
                                handleAddTag(input.value);
                                input.value = '';
                              }
                            }}
                            className="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                          />
                          <button
                            onClick={() => {
                              const input = document.querySelector('input[placeholder="Ajouter un tag"]') as HTMLInputElement;
                              if (input && input.value) {
                                handleAddTag(input.value);
                                input.value = '';
                              }
                            }}
                            className="px-4 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
                          >
                            Ajouter
                          </button>
                        </div>
                        <div className="flex flex-wrap gap-2">
                          {newNoteForm.tags.map(tag => (
                            <span
                              key={tag}
                              className="px-3 py-1 bg-blue-100 text-blue-700 rounded-full text-sm flex items-center space-x-1"
                            >
                              <span>{tag}</span>
                              <button
                                onClick={() => handleRemoveTag(tag)}
                                className="text-blue-500 hover:text-blue-700"
                              >
                                ×
                              </button>
                            </span>
                          ))}
                        </div>
                      </div>
                    </div>

                    {/* Couleur */}
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Couleur
                      </label>
                      <div className="flex space-x-2">
                        {['bg-blue-100', 'bg-green-100', 'bg-yellow-100', 'bg-red-100', 'bg-purple-100'].map(color => (
                          <button
                            key={color}
                            onClick={() => setNewNoteForm(prev => ({ ...prev, color }))}
                            className={`w-8 h-8 rounded-full border-2 ${
                              newNoteForm.color === color ? 'border-gray-400' : 'border-gray-200'
                            } ${color}`}
                          />
                        ))}
                      </div>
                    </div>
                  </div>

                  {/* Éditeur de contenu */}
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Contenu *
                    </label>
                    <textarea
                      value={newNoteForm.content}
                      onChange={(e) => setNewNoteForm(prev => ({ ...prev, content: e.target.value }))}
                      className="w-full h-64 px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
                      placeholder="Contenu de votre note..."
                    />
                  </div>
                </div>
              </div>

              <div className="p-6 border-t border-gray-200 flex justify-end space-x-3">
                <button
                  onClick={() => setShowNewNote(false)}
                  className="px-6 py-3 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50"
                >
                  Annuler
                </button>
                <button
                  onClick={handleCreateNote}
                  disabled={creatingNote}
                  className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center space-x-2"
                >
                  {creatingNote ? (
                    <>
                      <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                      <span>Création...</span>
                    </>
                  ) : (
                    <>
                      <Save size={16} />
                      <span>Créer la note</span>
                    </>
                  )}
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
} 