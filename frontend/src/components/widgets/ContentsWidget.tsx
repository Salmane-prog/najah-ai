"use client";
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
import React, { useEffect, useState } from 'react';

interface Content {
  id: number;
  title: string;
  description?: string;
  subject: string;
  level: string;
  file_url?: string;
  category_id?: number;
  quiz_id?: number;
}

interface Category {
  id: number;
  name: string;
}

interface Quiz {
  id: number;
  title: string;
}

function CreateContentModal({ onClose, onCreated, categories, quizzes }: {
  onClose: () => void;
  onCreated: () => void;
  categories: Category[];
  quizzes: Quiz[];
}) {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [subject, setSubject] = useState('');
  const [level, setLevel] = useState('');
  const [categoryId, setCategoryId] = useState<number | undefined>(undefined);
  const [type, setType] = useState('texte');
  const [file, setFile] = useState<File | null>(null);
  const [quizId, setQuizId] = useState<number | undefined>(undefined);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    let file_url = undefined;
    try {
      if ((type === 'pdf' || type === 'video') && file) {
        const formData = new FormData();
        formData.append('file', file);
        const res = await fetch(`${API_BASE_URL}/api/v1/contents/upload/`, {
          method: 'POST',
          body: formData
        });
        if (!res.ok) throw new Error('Erreur upload fichier');
        const data = await res.json();
        file_url = data.file_url;
      }
      const res = await fetch(`${API_BASE_URL}/api/v1/contents/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          title, description, subject, level, file_url, category_id: categoryId, quiz_id: quizId
        })
      });
      if (!res.ok) throw new Error('Erreur création contenu');
      onCreated();
      onClose();
    } catch (err: any) {
      setError(err.message || 'Erreur inconnue');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-30">
      <form onSubmit={handleSubmit} className="bg-white rounded-2xl shadow-2xl p-8 max-w-md w-full relative">
        <button type="button" onClick={onClose} className="absolute top-4 right-4 text-gray-400 hover:text-blue-600 text-xl font-bold">×</button>
        <h3 className="text-2xl font-bold text-blue-700 mb-4">Nouveau contenu pédagogique</h3>
        <div className="mb-3">
          <label className="block text-gray-700 font-semibold mb-1">Titre</label>
          <input value={title} onChange={e => setTitle(e.target.value)} required className="w-full border rounded-lg px-3 py-2" />
        </div>
        <div className="mb-3">
          <label className="block text-gray-700 font-semibold mb-1">Description</label>
          <textarea value={description} onChange={e => setDescription(e.target.value)} className="w-full border rounded-lg px-3 py-2" />
        </div>
        <div className="mb-3">
          <label className="block text-gray-700 font-semibold mb-1">Sujet/Matière</label>
          <input value={subject} onChange={e => setSubject(e.target.value)} required className="w-full border rounded-lg px-3 py-2" />
        </div>
        <div className="mb-3">
          <label className="block text-gray-700 font-semibold mb-1">Niveau</label>
          <input value={level} onChange={e => setLevel(e.target.value)} required className="w-full border rounded-lg px-3 py-2" />
        </div>
        <div className="mb-3">
          <label className="block text-gray-700 font-semibold mb-1">Catégorie</label>
          <select value={categoryId} onChange={e => setCategoryId(Number(e.target.value) || undefined)} className="w-full border rounded-lg px-3 py-2">
            <option value="">Aucune</option>
            {categories.map(cat => <option key={cat.id} value={cat.id}>{cat.name}</option>)}
          </select>
        </div>
        <div className="mb-3">
          <label className="block text-gray-700 font-semibold mb-1">Type</label>
          <select value={type} onChange={e => setType(e.target.value)} className="w-full border rounded-lg px-3 py-2">
            <option value="texte">Texte</option>
            <option value="pdf">PDF</option>
            <option value="video">Vidéo</option>
            <option value="quiz">Quiz</option>
          </select>
        </div>
        {(type === 'pdf' || type === 'video') && (
          <div className="mb-3">
            <label className="block text-gray-700 font-semibold mb-1">Fichier</label>
            <input type="file" accept={type === 'pdf' ? '.pdf' : 'video/*'} onChange={e => setFile(e.target.files?.[0] || null)} className="w-full" />
          </div>
        )}
        {type === 'quiz' && (
          <div className="mb-3">
            <label className="block text-gray-700 font-semibold mb-1">Quiz à lier</label>
            <select value={quizId} onChange={e => setQuizId(Number(e.target.value) || undefined)} className="w-full border rounded-lg px-3 py-2">
              <option value="">Aucun</option>
              {quizzes.map(q => <option key={q.id} value={q.id}>{q.title}</option>)}
            </select>
          </div>
        )}
        {error && <div className="text-red-600 mb-2">{error}</div>}
        <button type="submit" disabled={loading} className="px-4 py-2 bg-blue-600 text-white rounded-lg font-semibold hover:bg-blue-700 transition">
          {loading ? 'Création...' : 'Créer'}
        </button>
      </form>
    </div>
  );
}

function EditContentModal({ content, onClose, onUpdated, categories, quizzes }: {
  content: Content;
  onClose: () => void;
  onUpdated: () => void;
  categories: Category[];
  quizzes: Quiz[];
}) {
  const [title, setTitle] = useState(content.title);
  const [description, setDescription] = useState(content.description || '');
  const [subject, setSubject] = useState(content.subject);
  const [level, setLevel] = useState(content.level);
  const [categoryId, setCategoryId] = useState<number | undefined>(content.category_id);
  const [type, setType] = useState(content.file_url ? (content.file_url.endsWith('.pdf') ? 'pdf' : 'video') : (content.quiz_id ? 'quiz' : 'texte'));
  const [file, setFile] = useState<File | null>(null);
  const [quizId, setQuizId] = useState<number | undefined>(content.quiz_id);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    let file_url = content.file_url;
    try {
      if ((type === 'pdf' || type === 'video') && file) {
        const formData = new FormData();
        formData.append('file', file);
        const res = await fetch(`${API_BASE_URL}/api/v1/contents/upload/`, {
          method: 'POST',
          body: formData
        });
        if (!res.ok) throw new Error('Erreur upload fichier');
        const data = await res.json();
        file_url = data.file_url;
      }
      const res = await fetch(`${API_BASE_URL}/api/v1/contents/${content.id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          title, description, subject, level, file_url, category_id: categoryId, quiz_id: quizId
        })
      });
      if (!res.ok) throw new Error('Erreur modification contenu');
      onUpdated();
      onClose();
    } catch (err: any) {
      setError(err.message || 'Erreur inconnue');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-30">
      <form onSubmit={handleSubmit} className="bg-white rounded-2xl shadow-2xl p-8 max-w-md w-full relative">
        <button type="button" onClick={onClose} className="absolute top-4 right-4 text-gray-400 hover:text-blue-600 text-xl font-bold">×</button>
        <h3 className="text-2xl font-bold text-blue-700 mb-4">Modifier le contenu</h3>
        <div className="mb-3">
          <label className="block text-gray-700 font-semibold mb-1">Titre</label>
          <input value={title} onChange={e => setTitle(e.target.value)} required className="w-full border rounded-lg px-3 py-2" />
        </div>
        <div className="mb-3">
          <label className="block text-gray-700 font-semibold mb-1">Description</label>
          <textarea value={description} onChange={e => setDescription(e.target.value)} className="w-full border rounded-lg px-3 py-2" />
        </div>
        <div className="mb-3">
          <label className="block text-gray-700 font-semibold mb-1">Sujet/Matière</label>
          <input value={subject} onChange={e => setSubject(e.target.value)} required className="w-full border rounded-lg px-3 py-2" />
        </div>
        <div className="mb-3">
          <label className="block text-gray-700 font-semibold mb-1">Niveau</label>
          <input value={level} onChange={e => setLevel(e.target.value)} required className="w-full border rounded-lg px-3 py-2" />
        </div>
        <div className="mb-3">
          <label className="block text-gray-700 font-semibold mb-1">Catégorie</label>
          <select value={categoryId} onChange={e => setCategoryId(Number(e.target.value) || undefined)} className="w-full border rounded-lg px-3 py-2">
            <option value="">Aucune</option>
            {categories.map(cat => <option key={cat.id} value={cat.id}>{cat.name}</option>)}
          </select>
        </div>
        <div className="mb-3">
          <label className="block text-gray-700 font-semibold mb-1">Type</label>
          <select value={type} onChange={e => setType(e.target.value)} className="w-full border rounded-lg px-3 py-2">
            <option value="texte">Texte</option>
            <option value="pdf">PDF</option>
            <option value="video">Vidéo</option>
            <option value="quiz">Quiz</option>
          </select>
        </div>
        {(type === 'pdf' || type === 'video') && (
          <div className="mb-3">
            <label className="block text-gray-700 font-semibold mb-1">Fichier</label>
            <input type="file" accept={type === 'pdf' ? '.pdf' : 'video/*'} onChange={e => setFile(e.target.files?.[0] || null)} className="w-full" />
          </div>
        )}
        {type === 'quiz' && (
          <div className="mb-3">
            <label className="block text-gray-700 font-semibold mb-1">Quiz à lier</label>
            <select value={quizId} onChange={e => setQuizId(Number(e.target.value) || undefined)} className="w-full border rounded-lg px-3 py-2">
              <option value="">Aucun</option>
              {quizzes.map(q => <option key={q.id} value={q.id}>{q.title}</option>)}
            </select>
          </div>
        )}
        {error && <div className="text-red-600 mb-2">{error}</div>}
        <button type="submit" disabled={loading} className="px-4 py-2 bg-blue-600 text-white rounded-lg font-semibold hover:bg-blue-700 transition">
          {loading ? 'Modification...' : 'Enregistrer'}
        </button>
      </form>
    </div>
  );
}

function ConfirmDeleteModal({ content, onClose, onDeleted }: {
  content: Content;
  onClose: () => void;
  onDeleted: () => void;
}) {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleDelete = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await fetch(`${API_BASE_URL}/api/v1/contents/${content.id}`, { method: 'DELETE' });
      if (!res.ok) throw new Error('Erreur lors de la suppression du contenu');
      onDeleted();
      onClose();
    } catch (err: any) {
      setError(err.message || 'Erreur inconnue');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-30">
      <div className="bg-white rounded-2xl shadow-2xl p-8 max-w-md w-full relative">
        <button type="button" onClick={onClose} className="absolute top-4 right-4 text-gray-400 hover:text-blue-600 text-xl font-bold">×</button>
        <h3 className="text-2xl font-bold text-red-700 mb-4">Supprimer le contenu</h3>
        <p className="mb-4">Confirmer la suppression du contenu <span className="font-bold">{content.title}</span> ? Cette action est irréversible.</p>
        {error && <div className="text-red-600 mb-2">{error}</div>}
        <div className="flex gap-4">
          <button onClick={onClose} className="px-4 py-2 bg-gray-200 rounded-lg font-semibold">Annuler</button>
          <button onClick={handleDelete} disabled={loading} className="px-4 py-2 bg-red-600 text-white rounded-lg font-semibold hover:bg-red-700 transition">
            {loading ? 'Suppression...' : 'Supprimer'}
          </button>
        </div>
      </div>
    </div>
  );
}

export default function ContentsWidget() {
  const [contents, setContents] = useState<Content[]>([]);
  const [categories, setCategories] = useState<Category[]>([]);
  const [quizzes, setQuizzes] = useState<Quiz[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showCreate, setShowCreate] = useState(false);
  const [editContent, setEditContent] = useState<Content | null>(null);
  const [deleteContent, setDeleteContent] = useState<Content | null>(null);

  const refresh = () => {
    setLoading(true);
    setError(null);
    const token = typeof window !== "undefined" ? localStorage.getItem("najah_token") : null;
    Promise.all([
      fetch(`${API_BASE_URL}/api/v1/contents/`, {
        headers: {
          ...(token ? { 'Authorization': `Bearer ${token}` } : {}),
          'Content-Type': 'application/json'
        }
      }).then(res => res.json()),
      fetch(`${API_BASE_URL}/api/v1/categories/`, {
        headers: {
          ...(token ? { 'Authorization': `Bearer ${token}` } : {}),
          'Content-Type': 'application/json'
        }
      }).then(res => res.json()),
      fetch(`${API_BASE_URL}/api/v1/quizzes/`, {
        headers: {
          ...(token ? { 'Authorization': `Bearer ${token}` } : {}),
          'Content-Type': 'application/json'
        }
      }).then(res => res.json()),
    ]).then(([contents, categories, quizzes]) => {
      console.log("Contenus reçus :", contents);
      setContents(Array.isArray(contents) ? contents : []);
      setCategories(Array.isArray(categories) ? categories : []);
      setQuizzes(Array.isArray(quizzes) ? quizzes : []);
      setLoading(false);
    }).catch(err => {
      setContents([]); // Sécurise le state en cas d'erreur
      setError('Erreur lors du chargement des données');
      setLoading(false);
    });
  };

  useEffect(() => {
    refresh();
  }, []);

  return (
    <div className="bg-white rounded-xl shadow-lg p-8 mb-8">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-xl font-bold text-gray-700">Contenus pédagogiques</h2>
        <button onClick={() => setShowCreate(true)} className="px-4 py-2 bg-blue-600 text-white rounded-lg font-semibold hover:bg-blue-700 transition">Nouveau contenu</button>
      </div>
      {loading ? (
        <div className="text-blue-600 font-semibold">Chargement...</div>
      ) : error ? (
        <div className="text-red-600 font-semibold">{error}</div>
      ) : Array.isArray(contents) && contents.length === 0 ? (
        <div className="text-gray-500 italic">Aucun contenu trouvé.</div>
      ) : Array.isArray(contents) ? (
        <ul className="divide-y divide-gray-200">
          {contents.map(content => (
            <li key={content.id} className="py-4">
              <div className="font-bold text-blue-700 text-lg mb-1">{content.title}</div>
              {content.description && <div className="text-gray-600 mb-1">{content.description}</div>}
              <div className="text-xs text-gray-500">Sujet : {content.subject} | Niveau : {content.level}</div>
              {content.category_id && (
                <div className="text-xs text-gray-500">Catégorie : {categories.find(c => c.id === content.category_id)?.name}</div>
              )}
              {content.file_url && (
                <div className="text-xs text-gray-500">Fichier : <a href={content.file_url} className="text-blue-600 underline" target="_blank" rel="noopener noreferrer">Voir</a></div>
              )}
              {content.quiz_id && (
                <div className="text-xs text-gray-500">Quiz lié : {quizzes.find(q => q.id === content.quiz_id)?.title}</div>
              )}
              <div className="flex gap-2 mt-2">
                <button onClick={() => setEditContent(content)} className="px-3 py-1 bg-yellow-500 text-white rounded-lg text-sm font-semibold hover:bg-yellow-600 transition">Modifier</button>
                <button onClick={() => setDeleteContent(content)} className="px-3 py-1 bg-red-600 text-white rounded-lg text-sm font-semibold hover:bg-red-700 transition">Supprimer</button>
              </div>
            </li>
          ))}
        </ul>
      ) : (
        <div className="text-red-600">Erreur de chargement des contenus</div>
      )}
      {showCreate && <CreateContentModal onClose={() => setShowCreate(false)} onCreated={refresh} categories={categories} quizzes={quizzes} />}
      {editContent && <EditContentModal content={editContent} onClose={() => setEditContent(null)} onUpdated={refresh} categories={categories} quizzes={quizzes} />}
      {deleteContent && <ConfirmDeleteModal content={deleteContent} onClose={() => setDeleteContent(null)} onDeleted={refresh} />}
    </div>
  );
} 