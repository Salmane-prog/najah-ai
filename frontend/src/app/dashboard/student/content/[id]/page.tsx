'use client';

import { useAuth  } from '../../../../../hooks/useAuth';
import { useRouter, useParams } from 'next/navigation';
import { useState, useEffect } from 'react';
import Sidebar from '../../../../../components/Sidebar';
import { Card } from '../../../../../components/Card';
import Button from '../../../../../components/Button';
import { 
  Play, 
  Pause, 
  Volume2, 
  VolumeX, 
  BookOpen, 
  Edit3, 
  Save, 
  Clock,
  CheckCircle,
  Eye,
  EyeOff
} from 'lucide-react';

interface Content {
  id: number;
  title: string;
  description: string;
  content_type: string;
  content_data: string;
  file_url?: string;
  thumbnail_url?: string;
  difficulty: string;
  estimated_time: number;
  tags?: string[];
  learning_objectives?: string[];
  created_at: string;
}

interface Note {
  id: number;
  text: string;
  timestamp: number;
  created_at: string;
}

export default function ContentPage() {
  const { user, token } = useAuth();
  const params = useParams();
  const contentId = params.id;
  const router = useRouter();
  
  const [content, setContent] = useState<Content | null>(null);
  const [notes, setNotes] = useState<Note[]>([]);
  const [currentNote, setCurrentNote] = useState('');
  const [isPlaying, setIsPlaying] = useState(false);
  const [currentTime, setCurrentTime] = useState(0);
  const [duration, setDuration] = useState(0);
  const [volume, setVolume] = useState(1);
  const [isMuted, setIsMuted] = useState(false);
  const [progress, setProgress] = useState(0);
  const [loading, setLoading] = useState(true);
  const [showNotes, setShowNotes] = useState(true);

  useEffect(() => {
    if (contentId && token) {
      fetchContent();
      fetchNotes();
    }
  }, [contentId, token]);

  const fetchContent = async () => {
    try {
      const response = await fetch(`http://localhost:8000/api/v1/contents/${contentId}`, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });

      if (response.ok) {
        const data = await response.json();
        setContent(data);
      } else {
        console.error('Erreur lors du chargement du contenu');
      }
    } catch (error) {
      console.error('Erreur:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchNotes = async () => {
    try {
      const response = await fetch(`http://localhost:8000/api/v1/contents/${contentId}/notes`, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });

      if (response.ok) {
        const data = await response.json();
        setNotes(data);
      }
    } catch (error) {
      console.error('Erreur lors du chargement des notes:', error);
    }
  };

  const addNote = async () => {
    if (!currentNote.trim()) return;

    try {
      const response = await fetch(`http://localhost:8000/api/v1/contents/${contentId}/notes`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          text: currentNote,
          timestamp: currentTime
        })
      });

      if (response.ok) {
        const newNote = await response.json();
        setNotes([...notes, newNote]);
        setCurrentNote('');
      }
    } catch (error) {
      console.error('Erreur lors de l\'ajout de la note:', error);
    }
  };

  const updateProgress = async (newProgress: number) => {
    try {
      await fetch(`http://localhost:8000/api/v1/contents/${contentId}/progress`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          progress: newProgress
        })
      });
    } catch (error) {
      console.error('Erreur lors de la mise à jour de la progression:', error);
    }
  };

  const handleTimeUpdate = (time: number) => {
    setCurrentTime(time);
    const newProgress = (time / duration) * 100;
    setProgress(newProgress);
    
    // Mettre à jour la progression toutes les 30 secondes
    if (Math.floor(time) % 30 === 0) {
      updateProgress(newProgress);
    }
  };

  const togglePlay = () => {
    setIsPlaying(!isPlaying);
  };

  const toggleMute = () => {
    setIsMuted(!isMuted);
  };

  const handleVolumeChange = (newVolume: number) => {
    setVolume(newVolume);
    setIsMuted(newVolume === 0);
  };

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  const renderContentPlayer = () => {
    if (!content) return null;

    switch (content.content_type) {
      case 'video':
        return (
          <div className="relative bg-black rounded-lg overflow-hidden">
            <video
              className="w-full h-96 object-cover"
              src={content.file_url}
              poster={content.thumbnail_url}
              controls
              onTimeUpdate={(e) => handleTimeUpdate(e.currentTarget.currentTime)}
              onLoadedMetadata={(e) => setDuration(e.currentTarget.duration)}
            />
          </div>
        );

      case 'audio':
        return (
          <div className="bg-white rounded-lg p-6 shadow-sm">
            <div className="flex items-center space-x-4 mb-4">
              <button
                onClick={togglePlay}
                className="w-12 h-12 bg-blue-600 text-white rounded-full flex items-center justify-center hover:bg-blue-700"
              >
                {isPlaying ? <Pause size={20} /> : <Play size={20} />}
              </button>
              
              <div className="flex-1">
                <div className="text-sm text-gray-500">
                  {formatTime(currentTime)} / {formatTime(duration)}
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div 
                    className="bg-blue-600 h-2 rounded-full"
                    style={{ width: `${(currentTime / duration) * 100}%` }}
                  ></div>
                </div>
              </div>
              
              <div className="flex items-center space-x-2">
                <button onClick={toggleMute}>
                  {isMuted ? <VolumeX size={20} /> : <Volume2 size={20} />}
                </button>
                <input
                  type="range"
                  min="0"
                  max="1"
                  step="0.1"
                  value={isMuted ? 0 : volume}
                  onChange={(e) => handleVolumeChange(parseFloat(e.target.value))}
                  className="w-20"
                />
              </div>
            </div>
          </div>
        );

      case 'text':
        return (
          <div className="bg-white rounded-lg p-6 shadow-sm">
            <div className="prose max-w-none">
              <div dangerouslySetInnerHTML={{ __html: content.content_data }} />
            </div>
          </div>
        );

      case 'interactive':
        return (
          <div className="bg-white rounded-lg p-6 shadow-sm">
            <div className="prose max-w-none">
              <div dangerouslySetInnerHTML={{ __html: content.content_data }} />
            </div>
            <div className="mt-6 p-4 bg-blue-50 rounded-lg">
              <h4 className="font-semibold text-blue-900 mb-2">Activité Interactive</h4>
              <p className="text-blue-700 text-sm">
                Ce contenu contient des éléments interactifs. Cliquez sur les éléments pour interagir.
              </p>
            </div>
          </div>
        );

      default:
        return (
          <div className="bg-white rounded-lg p-6 shadow-sm">
            <p className="text-gray-500">Type de contenu non supporté</p>
          </div>
        );
    }
  };

  if (loading) {
    return (
      <div className="flex min-h-screen bg-gray-50">
        <Sidebar />
        <div className="flex-1 flex items-center justify-center">
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
            <p className="mt-4 text-gray-600">Chargement du contenu...</p>
          </div>
        </div>
      </div>
    );
  }

  if (!content) {
    return (
      <div className="flex min-h-screen bg-gray-50">
        <Sidebar />
        <div className="flex-1 flex items-center justify-center">
          <div className="text-center">
            <BookOpen className="w-16 h-16 text-gray-400 mx-auto mb-4" />
            <h2 className="text-xl font-semibold text-gray-900 mb-2">Contenu non trouvé</h2>
            <p className="text-gray-600 mb-4">Le contenu que vous recherchez n'existe pas.</p>
            <Button onClick={() => router.back()}>
              Retour
            </Button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="flex min-h-screen bg-gray-50">
      <Sidebar />
      <div className="flex-1 overflow-auto">
        <div className="p-6">
          {/* En-tête */}
          <div className="mb-6">
            <div className="flex items-center justify-between">
              <div>
                <h1 className="text-3xl font-bold text-gray-900 mb-2">
                  {content.title}
                </h1>
                <p className="text-gray-600">{content.description}</p>
              </div>
              <div className="flex items-center space-x-2">
                <Button
                  onClick={() => setShowNotes(!showNotes)}
                  variant="outline"
                  size="sm"
                >
                  {showNotes ? <EyeOff className="w-4 h-4 mr-2" /> : <Eye className="w-4 h-4 mr-2" />}
                  {showNotes ? 'Masquer' : 'Afficher'} les notes
                </Button>
              </div>
            </div>
            
            <div className="flex items-center mt-4 space-x-4 text-sm text-gray-500">
              <span className="flex items-center">
                <Clock className="w-4 h-4 mr-1" />
                {content.estimated_time} min
              </span>
              <span className={`px-2 py-1 rounded ${
                content.difficulty === 'facile' ? 'bg-green-100 text-green-700' :
                content.difficulty === 'moyen' ? 'bg-yellow-100 text-yellow-700' :
                'bg-red-100 text-red-700'
              }`}>
                {content.difficulty}
              </span>
              <span className="flex items-center">
                <CheckCircle className="w-4 h-4 mr-1" />
                {Math.round(progress)}% terminé
              </span>
            </div>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Lecteur de contenu */}
            <div className="lg:col-span-2">
              {renderContentPlayer()}
            </div>

            {/* Panneau des notes */}
            {showNotes && (
              <div className="space-y-4">
                <Card>
                  <div className="flex items-center justify-between mb-4">
                    <h3 className="text-lg font-semibold text-gray-900">
                      Mes Notes
                    </h3>
                    <Edit3 className="w-5 h-5 text-gray-400" />
                  </div>
                  
                  <div className="space-y-3">
                    <div className="flex space-x-2">
                      <input
                        type="text"
                        value={currentNote}
                        onChange={(e) => setCurrentNote(e.target.value)}
                        placeholder="Ajouter une note..."
                        className="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                        onKeyPress={(e) => e.key === 'Enter' && addNote()}
                      />
                      <Button onClick={addNote} size="sm">
                        <Save className="w-4 h-4" />
                      </Button>
                    </div>
                    
                    <div className="space-y-2 max-h-64 overflow-y-auto">
                      {notes.map((note) => (
                        <div key={note.id} className="p-3 bg-gray-50 rounded-lg">
                          <div className="flex items-center justify-between mb-1">
                            <span className="text-xs text-gray-500">
                              {formatTime(note.timestamp)}
                            </span>
                            <span className="text-xs text-gray-400">
                              {new Date(note.created_at).toLocaleDateString()}
                            </span>
                          </div>
                          <p className="text-sm text-gray-700">{note.text}</p>
                        </div>
                      ))}
                      
                      {notes.length === 0 && (
                        <p className="text-center text-gray-500 text-sm py-4">
                          Aucune note pour le moment
                        </p>
                      )}
                    </div>
                  </div>
                </Card>

                {/* Objectifs d'apprentissage */}
                {content.learning_objectives && content.learning_objectives.length > 0 && (
                  <Card>
                    <h3 className="text-lg font-semibold text-gray-900 mb-3">
                      Objectifs d'Apprentissage
                    </h3>
                    <ul className="space-y-2">
                      {content.learning_objectives.map((objective, index) => (
                        <li key={index} className="flex items-start space-x-2">
                          <CheckCircle className="w-4 h-4 text-green-600 mt-0.5 flex-shrink-0" />
                          <span className="text-sm text-gray-700">{objective}</span>
                        </li>
                      ))}
                    </ul>
                  </Card>
                )}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
} 