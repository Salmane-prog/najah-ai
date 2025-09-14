"use client";
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
import React, { useEffect, useState } from 'react';

interface LearningPath {
  id: number;
  name: string;
  description?: string;
  students?: { id: number; name?: string }[];
  class_id?: number;
  steps?: string[]; // Added for edit modal
}

interface LearningPathsWidgetProps {
  studentId?: number;
  classId?: number;
}

function CreatePathModal({ onClose, onCreated }: { onClose: () => void; onCreated: () => void }) {
  const [name, setName] = useState('');
  const [description, setDescription] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      const token = localStorage.getItem('najah_token');
      const res = await fetch(`${API_BASE_URL}/api/v1/learning_paths/`, {
        method: 'POST',
        headers: { 
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ name, description })
      });
      if (!res.ok) throw new Error('Erreur lors de la création du parcours');
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
        <h3 className="text-2xl font-bold text-blue-700 mb-4">Nouveau parcours</h3>
        <div className="mb-4">
          <label className="block text-gray-700 font-semibold mb-1">Nom</label>
          <input value={name} onChange={e => setName(e.target.value)} required className="w-full border rounded-lg px-3 py-2" />
        </div>
        <div className="mb-4">
          <label className="block text-gray-700 font-semibold mb-1">Description</label>
          <textarea value={description} onChange={e => setDescription(e.target.value)} className="w-full border rounded-lg px-3 py-2" />
        </div>
        {error && <div className="text-red-600 mb-2">{error}</div>}
        <button type="submit" disabled={loading} className="px-4 py-2 bg-blue-600 text-white rounded-lg font-semibold hover:bg-blue-700 transition">
          {loading ? 'Création...' : 'Créer'}
        </button>
      </form>
    </div>
  );
}

function AssignPathModal({ pathId, onClose, onAssigned }: { pathId: number; onClose: () => void; onAssigned: () => void }) {
  const [studentId, setStudentId] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      const token = localStorage.getItem('najah_token');
      const res = await fetch(`${API_BASE_URL}/api/v1/learning_paths/assign/`, {
        method: 'POST',
        headers: { 
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ path_id: pathId, student_id: Number(studentId) })
      });
      if (!res.ok) throw new Error('Erreur lors de l\'assignation');
      onAssigned();
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
        <h3 className="text-2xl font-bold text-blue-700 mb-4">Assigner à un élève</h3>
        <div className="mb-4">
          <label className="block text-gray-700 font-semibold mb-1">ID de l'élève</label>
          <input value={studentId} onChange={e => setStudentId(e.target.value)} required className="w-full border rounded-lg px-3 py-2" />
        </div>
        {error && <div className="text-red-600 mb-2">{error}</div>}
        <button type="submit" disabled={loading} className="px-4 py-2 bg-blue-600 text-white rounded-lg font-semibold hover:bg-blue-700 transition">
          {loading ? 'Assignation...' : 'Assigner'}
        </button>
      </form>
    </div>
  );
}

// 1. Ajouter le composant EditPathModal
function EditPathModal({ path, onClose, onUpdated }: { path: LearningPath; onClose: () => void; onUpdated: () => void }) {
  const [name, setName] = useState(path.name);
  const [description, setDescription] = useState(path.description || '');
  const [steps, setSteps] = useState<string[]>(path.steps || []);
  const [newStep, setNewStep] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Ajout d'une étape
  const handleAddStep = () => {
    if (newStep.trim()) {
      setSteps([...steps, newStep.trim()]);
      setNewStep('');
    }
  };
  // Suppression d'une étape
  const handleRemoveStep = (idx: number) => {
    setSteps(steps.filter((_, i) => i !== idx));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      const token = localStorage.getItem('najah_token');
      const res = await fetch(`${API_BASE_URL}/api/v1/learning_paths/${path.id}`, {
        method: 'PUT',
        headers: { 
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ name, description, steps })
      });
      if (!res.ok) throw new Error('Erreur lors de la modification du parcours');
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
        <h3 className="text-2xl font-bold text-blue-700 mb-4">Modifier le parcours</h3>
        <div className="mb-4">
          <label className="block text-gray-700 font-semibold mb-1">Nom</label>
          <input value={name} onChange={e => setName(e.target.value)} required className="w-full border rounded-lg px-3 py-2" />
        </div>
        <div className="mb-4">
          <label className="block text-gray-700 font-semibold mb-1">Description</label>
          <textarea value={description} onChange={e => setDescription(e.target.value)} className="w-full border rounded-lg px-3 py-2" />
        </div>
        <div className="mb-4">
          <label className="block text-gray-700 font-semibold mb-1">Étapes</label>
          <ul className="mb-2">
            {steps.map((step, idx) => (
              <li key={idx} className="flex items-center gap-2 mb-1">
                <span className="flex-1">{step}</span>
                <button type="button" onClick={() => handleRemoveStep(idx)} className="text-red-500 hover:text-red-700">Supprimer</button>
              </li>
            ))}
          </ul>
          <div className="flex gap-2">
            <input value={newStep} onChange={e => setNewStep(e.target.value)} className="flex-1 border rounded-lg px-2 py-1" placeholder="Nouvelle étape" />
            <button type="button" onClick={handleAddStep} className="px-2 py-1 bg-blue-500 text-white rounded-lg">Ajouter</button>
          </div>
        </div>
        {error && <div className="text-red-600 mb-2">{error}</div>}
        <button type="submit" disabled={loading} className="px-4 py-2 bg-blue-600 text-white rounded-lg font-semibold hover:bg-blue-700 transition">
          {loading ? 'Modification...' : 'Enregistrer'}
        </button>
      </form>
    </div>
  );
}

// 2. Ajouter le composant ConfirmDeleteModal
function ConfirmDeleteModal({ path, onClose, onDeleted }: { path: LearningPath; onClose: () => void; onDeleted: () => void }) {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleDelete = async () => {
    setLoading(true);
    setError(null);
    try {
      const token = localStorage.getItem('najah_token');
      const res = await fetch(`${API_BASE_URL}/api/v1/learning_paths/${path.id}`, { 
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      if (!res.ok) throw new Error('Erreur lors de la suppression du parcours');
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
        <h3 className="text-2xl font-bold text-red-700 mb-4">Supprimer le parcours</h3>
        <p className="mb-4">Confirmer la suppression du parcours <span className="font-bold">{path.name}</span> ? Cette action est irréversible.</p>
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

export default function LearningPathsWidget({ studentId, classId }: LearningPathsWidgetProps) {
  const [paths, setPaths] = useState<LearningPath[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [search, setSearch] = useState('');
  const [showCreate, setShowCreate] = useState(false);
  const [assignPathId, setAssignPathId] = useState<number | null>(null);
  const [editPath, setEditPath] = useState<LearningPath | null>(null);
  const [deletePath, setDeletePath] = useState<LearningPath | null>(null);

  const refresh = () => {
    setLoading(true);
    setError(null);
    const token = typeof window !== "undefined" ? localStorage.getItem("najah_token") : null;
    fetch(`${API_BASE_URL}/api/v1/learning_paths/`, {
      headers: {
        ...(token ? { 'Authorization': `Bearer ${token}` } : {}),
        'Content-Type': 'application/json'
      }
    })
      .then(res => {
        if (!res.ok) throw new Error('Erreur lors du chargement des parcours');
        return res.json();
      })
      .then((data: LearningPath[]) => {
        setPaths(data);
        setLoading(false);
      })
      .catch(err => {
        setError(err.message || 'Erreur inconnue');
        setLoading(false);
      });
  };

  useEffect(() => {
    refresh();
  }, []);

  // Filtrage par élève ou classe
  let filtered = paths;
  if (studentId) {
    filtered = filtered.filter(p => Array.isArray(p.students) && p.students.some(s => s.id === studentId));
  }
  if (classId) {
    filtered = filtered.filter(p => p.class_id === classId);
  }
  if (search) {
    filtered = filtered.filter(p => p.name.toLowerCase().includes(search.toLowerCase()));
  }

  return (
    <div className="bg-white rounded-xl shadow-lg p-8 mb-8">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-xl font-bold text-gray-700">Parcours d'apprentissage</h2>
        <button onClick={() => setShowCreate(true)} className="px-4 py-2 bg-blue-600 text-white rounded-lg font-semibold hover:bg-blue-700 transition">Nouveau parcours</button>
      </div>
      <div className="flex flex-wrap items-center gap-4 mb-4">
        <input
          type="text"
          placeholder="Rechercher un parcours..."
          value={search}
          onChange={e => setSearch(e.target.value)}
          className="border rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-400"
        />
      </div>
      {loading ? (
        <div className="text-blue-600 font-semibold">Chargement...</div>
      ) : error ? (
        <div className="text-red-600 font-semibold">{error}</div>
      ) : filtered.length === 0 ? (
        <div className="text-gray-500 italic">Aucun parcours trouvé.</div>
      ) : (
        <ul className="divide-y divide-gray-200">
          {filtered.map(path => (
            <li key={path.id} className="py-4">
              <div className="font-bold text-blue-700 text-lg mb-1">{path.name}</div>
              {path.description && <div className="text-gray-600 mb-1">{path.description}</div>}
              {Array.isArray(path.students) && path.students.length > 0 && (
                <div className="text-xs text-gray-500">Élèves assignés : {path.students.map(s => s.name || s.id).join(', ')}</div>
              )}
              {path.class_id && (
                <div className="text-xs text-gray-500">Classe assignée : {path.class_id}</div>
              )}
              <div className="flex gap-2 mt-2">
                <button onClick={() => setAssignPathId(path.id)} className="px-3 py-1 bg-green-600 text-white rounded-lg text-sm font-semibold hover:bg-green-700 transition">Assigner</button>
                <button onClick={() => setEditPath(path)} className="px-3 py-1 bg-yellow-500 text-white rounded-lg text-sm font-semibold hover:bg-yellow-600 transition">Modifier</button>
                <button onClick={() => setDeletePath(path)} className="px-3 py-1 bg-red-600 text-white rounded-lg text-sm font-semibold hover:bg-red-700 transition">Supprimer</button>
              </div>
            </li>
          ))}
        </ul>
      )}
      {showCreate && <CreatePathModal onClose={() => setShowCreate(false)} onCreated={refresh} />}
      {assignPathId && <AssignPathModal pathId={assignPathId} onClose={() => setAssignPathId(null)} onAssigned={refresh} />}
      {editPath && <EditPathModal path={editPath} onClose={() => setEditPath(null)} onUpdated={refresh} />}
      {deletePath && <ConfirmDeleteModal path={deletePath} onClose={() => setDeletePath(null)} onDeleted={refresh} />}
    </div>
  );
} 