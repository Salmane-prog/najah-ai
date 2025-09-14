"use client";
import React, { useState, useEffect, useRef } from 'react';
import { useAuth  } from '../../../../hooks/useAuth';
import { Card } from '../../../../components/Card';
import Button from '../../../../components/Button';
import { 
  Plus, 
  Search, 
  Filter, 
  Edit, 
  Trash2, 
  Download, 
  Tag, 
  BookOpen,
  Calendar,
  Save,
  X
} from 'lucide-react';
import Sidebar from '../../../../components/Sidebar';

interface Note {
  id: number;
  title: string;
  content: string;
  subject: string;
  content_id?: number;
  created_at: string;
  updated_at: string;
  tags: string[];
}

const NotesPage: React.FC = () => {
  const { user, token } = useAuth();
  const [notes, setNotes] = useState<Note[]>([]);
  const [selectedNote, setSelectedNote] = useState<Note | null>(null);
  const [isEditing, setIsEditing] = useState(false);
  const [isCreating, setIsCreating] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedSubject, setSelectedSubject] = useState('');
  const [subjects, setSubjects] = useState<string[]>([]);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  
  // Form states
  const [noteTitle, setNoteTitle] = useState('');
  const [noteContent, setNoteContent] = useState('');
  const [noteSubject, setNoteSubject] = useState('');
  const [noteTags, setNoteTags] = useState<string[]>([]);
  const [newTag, setNewTag] = useState('');

  const editorRef = useRef<HTMLTextAreaElement>(null);

  // Charger les notes
  useEffect(() => {
    if (user && token) {
      fetchNotes();
      fetchSubjects();
    }
  }, [user, token]);

  const fetchNotes = async () => {
    try {
      setLoading(true);
      const params = new URLSearchParams();
      if (searchTerm) params.append('search', searchTerm);
      if (selectedSubject) params.append('subject', selectedSubject);

      const response = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/v1/notes/?${params}`,
        {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        }
      );

      if (response.ok) {
        const data = await response.json();
        setNotes(data.notes || []);
      }
    } catch (error) {
      console.error('Erreur lors du chargement des notes:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchSubjects = async () => {
    try {
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/v1/notes/subjects/list`,
        {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        }
      );

      if (response.ok) {
        const data = await response.json();
        setSubjects(data.subjects || []);
      }
    } catch (error) {
      console.error('Erreur lors du chargement des matières:', error);
    }
  };

  const handleCreateNote = () => {
    setIsCreating(true);
    setIsEditing(false);
    setSelectedNote(null);
    setNoteTitle('');
    setNoteContent('');
    setNoteSubject('');
    setNoteTags([]);
  };

  const handleEditNote = (note: Note) => {
    setSelectedNote(note);
    setIsEditing(true);
    setIsCreating(false);
    setNoteTitle(note.title);
    setNoteContent(note.content);
    setNoteSubject(note.subject);
    setNoteTags(note.tags);
  };

  const handleSaveNote = async () => {
    if (!noteTitle.trim()) {
      alert('Le titre de la note ne peut pas être vide');
      return;
    }

    try {
      setSaving(true);
      const noteData = {
        title: noteTitle,
        content: noteContent,
        subject: noteSubject,
        tags: noteTags
      };

      const url = isEditing && selectedNote
        ? `${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/v1/notes/${selectedNote.id}`
        : `${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/v1/notes/`;

      const response = await fetch(url, {
        method: isEditing ? 'PUT' : 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(noteData)
      });

      if (response.ok) {
        const savedNote = await response.json();
        
        if (isEditing) {
          setNotes(prev => prev.map(n => n.id === selectedNote?.id ? savedNote : n));
        } else {
          setNotes(prev => [savedNote, ...prev]);
        }
        
        setIsCreating(false);
        setIsEditing(false);
        setSelectedNote(null);
        setNoteTitle('');
        setNoteContent('');
        setNoteSubject('');
        setNoteTags([]);
      }
    } catch (error) {
      console.error('Erreur lors de la sauvegarde:', error);
      alert('Erreur lors de la sauvegarde de la note');
    } finally {
      setSaving(false);
    }
  };

  const handleDeleteNote = async (noteId: number) => {
    if (!confirm('Êtes-vous sûr de vouloir supprimer cette note ?')) return;

    try {
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/v1/notes/${noteId}`,
        {
          method: 'DELETE',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        }
      );

      if (response.ok) {
        setNotes(prev => prev.filter(n => n.id !== noteId));
        if (selectedNote?.id === noteId) {
          setSelectedNote(null);
          setIsEditing(false);
        }
      }
    } catch (error) {
      console.error('Erreur lors de la suppression:', error);
    }
  };

  const handleExportNote = async (noteId: number) => {
    try {
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/v1/notes/export/${noteId}?format=pdf`,
        {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        }
      );

      if (response.ok) {
        const data = await response.json();
        // Simulation de téléchargement
        alert('Export réussi ! (Dans un vrai projet, le fichier serait téléchargé)');
      }
    } catch (error) {
      console.error('Erreur lors de l\'export:', error);
    }
  };

  const addTag = () => {
    if (newTag.trim() && !noteTags.includes(newTag.trim())) {
      setNoteTags(prev => [...prev, newTag.trim()]);
      setNewTag('');
    }
  };

  const removeTag = (tagToRemove: string) => {
    setNoteTags(prev => prev.filter(tag => tag !== tagToRemove));
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('fr-FR', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const filteredNotes = notes.filter(note =>
    note.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
    note.content.toLowerCase().includes(searchTerm.toLowerCase())
  );

  if (!user || !token) {
    return (
      <div className="flex min-h-screen bg-gray-50">
        <Sidebar />
        <div className="flex-1 flex items-center justify-center ml-64">
          <div className="text-center">
            <h2 className="text-xl font-semibold text-gray-600">Non authentifié</h2>
            <p className="text-gray-500">Veuillez vous connecter pour accéder aux notes</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="flex min-h-screen bg-gray-50">
      <Sidebar />
      <div className="flex-1 flex ml-64">
      {/* Sidebar des notes */}
      <div className="w-80 bg-white border-r border-gray-200 flex flex-col">
        {/* Header */}
        <div className="p-4 border-b border-gray-200">
          <div className="flex items-center justify-between mb-4">
            <h1 className="text-xl font-bold text-gray-800">Mes Notes</h1>
            <Button
              onClick={handleCreateNote}
              className="flex items-center gap-2"
            >
              <Plus className="w-4 h-4" />
              Nouvelle note
            </Button>
          </div>
          
          {/* Recherche */}
          <div className="relative mb-3">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
            <input
              type="text"
              placeholder="Rechercher dans les notes..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>

          {/* Filtre par matière */}
          <div className="relative">
            <Filter className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
            <select
              value={selectedSubject}
              onChange={(e) => setSelectedSubject(e.target.value)}
              className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              <option value="">Toutes les matières</option>
              {subjects.map(subject => (
                <option key={subject} value={subject}>{subject}</option>
              ))}
            </select>
          </div>
        </div>

        {/* Liste des notes */}
        <div className="flex-1 overflow-y-auto">
          {loading ? (
            <div className="p-4 text-center text-gray-500">Chargement...</div>
          ) : filteredNotes.length === 0 ? (
            <div className="p-4 text-center text-gray-500">
              <BookOpen className="w-12 h-12 mx-auto mb-2 text-gray-300" />
              <p>Aucune note trouvée</p>
              <p className="text-sm mt-2">Créez votre première note !</p>
            </div>
          ) : (
            filteredNotes.map((note) => (
              <div
                key={note.id}
                className={`p-4 border-b border-gray-100 cursor-pointer hover:bg-gray-50 transition-colors ${
                  selectedNote?.id === note.id ? 'bg-blue-50 border-blue-200' : ''
                }`}
                onClick={() => setSelectedNote(note)}
              >
                <div className="flex items-start justify-between">
                  <div className="flex-1 min-w-0">
                    <h3 className="font-semibold text-gray-800 truncate">{note.title}</h3>
                    <p className="text-sm text-gray-600 truncate mt-1">
                      {note.content.substring(0, 100)}...
                    </p>
                    <div className="flex items-center gap-2 mt-2">
                      {note.subject && (
                        <span className="text-xs bg-blue-100 text-blue-800 px-2 py-1 rounded">
                          {note.subject}
                        </span>
                      )}
                      <span className="text-xs text-gray-500">
                        {formatDate(note.updated_at)}
                      </span>
                    </div>
                  </div>
                  <div className="flex items-center gap-1 ml-2">
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        handleEditNote(note);
                      }}
                      className="p-1 text-gray-400 hover:text-blue-600"
                    >
                      <Edit className="w-4 h-4" />
                    </button>
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        handleDeleteNote(note.id);
                      }}
                      className="p-1 text-gray-400 hover:text-red-600"
                    >
                      <Trash2 className="w-4 h-4" />
                    </button>
                  </div>
                </div>
              </div>
            ))
          )}
        </div>
      </div>

      {/* Zone d'édition */}
      <div className="flex-1 flex flex-col">
        {isCreating || isEditing ? (
          <div className="flex-1 flex flex-col">
            {/* Header de l'éditeur */}
            <div className="bg-white border-b border-gray-200 p-4">
              <div className="flex items-center justify-between">
                <h2 className="text-lg font-semibold text-gray-800">
                  {isCreating ? 'Nouvelle note' : 'Modifier la note'}
                </h2>
                <div className="flex items-center gap-2">
                  <Button
                    onClick={handleSaveNote}
                    disabled={saving}
                    className="flex items-center gap-2"
                  >
                    <Save className="w-4 h-4" />
                    {saving ? 'Sauvegarde...' : 'Sauvegarder'}
                  </Button>
                  <Button
                    onClick={() => {
                      setIsCreating(false);
                      setIsEditing(false);
                      setSelectedNote(null);
                    }}
                    variant="outline"
                    className="flex items-center gap-2"
                  >
                    <X className="w-4 h-4" />
                    Annuler
                  </Button>
                </div>
              </div>
            </div>

            {/* Formulaire d'édition */}
            <div className="flex-1 p-6">
              <div className="max-w-4xl mx-auto space-y-6">
                {/* Titre */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Titre de la note
                  </label>
                  <input
                    type="text"
                    value={noteTitle}
                    onChange={(e) => setNoteTitle(e.target.value)}
                    placeholder="Titre de votre note..."
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />
                </div>

                {/* Matière */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Matière
                  </label>
                  <input
                    type="text"
                    value={noteSubject}
                    onChange={(e) => setNoteSubject(e.target.value)}
                    placeholder="Mathématiques, Français, Sciences..."
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />
                </div>

                {/* Tags */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Tags
                  </label>
                  <div className="flex items-center gap-2 mb-2">
                    <input
                      type="text"
                      value={newTag}
                      onChange={(e) => setNewTag(e.target.value)}
                      onKeyPress={(e) => e.key === 'Enter' && addTag()}
                      placeholder="Ajouter un tag..."
                      className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    />
                    <Button onClick={addTag} size="sm">
                      <Tag className="w-4 h-4" />
                    </Button>
                  </div>
                  <div className="flex flex-wrap gap-2">
                    {noteTags.map((tag, index) => (
                      <span
                        key={index}
                        className="flex items-center gap-1 bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm"
                      >
                        {tag}
                        <button
                          onClick={() => removeTag(tag)}
                          className="text-blue-600 hover:text-blue-800"
                        >
                          <X className="w-3 h-3" />
                        </button>
                      </span>
                    ))}
                  </div>
                </div>

                {/* Contenu */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Contenu
                  </label>
                  <textarea
                    ref={editorRef}
                    value={noteContent}
                    onChange={(e) => setNoteContent(e.target.value)}
                    placeholder="Tapez votre note ici... Vous pouvez utiliser Markdown pour le formatage."
                    className="w-full h-96 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none font-mono"
                  />
                  <p className="text-xs text-gray-500 mt-1">
                    Support Markdown : **gras**, *italique*, # titres, - listes
                  </p>
                </div>
              </div>
            </div>
          </div>
        ) : selectedNote ? (
          <div className="flex-1 flex flex-col">
            {/* Header de la note */}
            <div className="bg-white border-b border-gray-200 p-4">
              <div className="flex items-center justify-between">
                <div>
                  <h2 className="text-lg font-semibold text-gray-800">{selectedNote.title}</h2>
                  <div className="flex items-center gap-4 mt-1">
                    {selectedNote.subject && (
                      <span className="text-sm bg-blue-100 text-blue-800 px-2 py-1 rounded">
                        {selectedNote.subject}
                      </span>
                    )}
                    <span className="text-sm text-gray-500">
                      <Calendar className="w-4 h-4 inline mr-1" />
                      {formatDate(selectedNote.updated_at)}
                    </span>
                  </div>
                </div>
                <div className="flex items-center gap-2">
                  <Button
                    onClick={() => handleEditNote(selectedNote)}
                    variant="outline"
                    className="flex items-center gap-2"
                  >
                    <Edit className="w-4 h-4" />
                    Modifier
                  </Button>
                  <Button
                    onClick={() => handleExportNote(selectedNote.id)}
                    variant="outline"
                    className="flex items-center gap-2"
                  >
                    <Download className="w-4 h-4" />
                    Exporter
                  </Button>
                </div>
              </div>
            </div>

            {/* Contenu de la note */}
            <div className="flex-1 p-6 overflow-y-auto">
              <div className="max-w-4xl mx-auto">
                {/* Tags */}
                {selectedNote.tags.length > 0 && (
                  <div className="mb-4">
                    <div className="flex flex-wrap gap-2">
                      {selectedNote.tags.map((tag, index) => (
                        <span
                          key={index}
                          className="bg-gray-100 text-gray-800 px-3 py-1 rounded-full text-sm"
                        >
                          {tag}
                        </span>
                      ))}
                    </div>
                  </div>
                )}

                {/* Contenu formaté */}
                <div className="prose max-w-none">
                  <pre className="whitespace-pre-wrap font-mono text-gray-800 bg-gray-50 p-4 rounded-lg">
                    {selectedNote.content}
                  </pre>
                </div>
              </div>
            </div>
          </div>
        ) : (
          <div className="flex-1 flex items-center justify-center">
            <div className="text-center">
              <BookOpen className="w-16 h-16 mx-auto mb-4 text-gray-300" />
              <h3 className="text-lg font-semibold text-gray-600 mb-2">Sélectionnez une note</h3>
              <p className="text-gray-500">Choisissez une note dans la liste ou créez-en une nouvelle</p>
            </div>
          </div>
        )}
      </div>
      </div>
    </div>
  );
};

export default NotesPage; 