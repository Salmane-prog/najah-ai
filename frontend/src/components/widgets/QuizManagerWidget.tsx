import React, { useEffect, useState } from 'react';

interface QuizFile {
  matiere: string;
  filename: string;
  path: string;
}

interface QuizData {
  metadata: any;
  dataset_entrainement_enrichi: QuizQuestion[];
}

interface QuizQuestion {
  id: string;
  section: number;
  type: string;
  difficulte: string;
  theme_semantique: string;
  prefixe: string;
  texte_entree: string;
  texte_cible: string;
}

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export default function QuizManagerWidget() {
  const [quizFiles, setQuizFiles] = useState<QuizFile[]>([]);
  const [selectedQuiz, setSelectedQuiz] = useState<QuizFile | null>(null);
  const [quizData, setQuizData] = useState<QuizData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showCreateQuiz, setShowCreateQuiz] = useState(false);
  const [showQuestionModal, setShowQuestionModal] = useState<null | { mode: 'create' | 'edit', question?: QuizQuestion }>(null);
  const [questionEditIndex, setQuestionEditIndex] = useState<number | null>(null);
  const [showAssignModal, setShowAssignModal] = useState(false);
  const [assignLoading, setAssignLoading] = useState(false);
  const [assignSuccess, setAssignSuccess] = useState<string|null>(null);
  const [assignError, setAssignError] = useState<string|null>(null);
  const [classesList, setClassesList] = useState<any[]>([]);
  const [studentsList, setStudentsList] = useState<any[]>([]);
  const [selectedClasses, setSelectedClasses] = useState<string[]>([]);
  const [selectedStudents, setSelectedStudents] = useState<string[]>([]);

  // Charger la liste des quiz JSON
  const refresh = () => {
    setLoading(true);
    setError(null);
    fetch(`${API_BASE_URL}/api/v1/quiz_json/json/list`)
      .then(res => res.json())
      .then((data: QuizFile[]) => {
        setQuizFiles(data);
        setLoading(false);
      })
      .catch(() => {
        setError('Erreur lors du chargement des quiz');
        setLoading(false);
      });
  };

  useEffect(() => {
    refresh();
  }, []);

  // Charger les questions d’un quiz sélectionné
  const loadQuiz = (quiz: QuizFile) => {
    setSelectedQuiz(quiz);
    setQuizData(null);
    setLoading(true);
    fetch(`${API_BASE_URL}/api/v1/quiz_json/json/${quiz.matiere}/${quiz.filename}`)
      .then(res => res.json())
      .then((data: QuizData) => {
        setQuizData(data);
        setLoading(false);
      })
      .catch(() => {
        setError('Erreur lors du chargement du quiz');
        setLoading(false);
      });
  };

  // Grouper les quiz par matière
  const quizzesByMatiere = quizFiles.reduce((acc, quiz) => {
    acc[quiz.matiere] = acc[quiz.matiere] || [];
    acc[quiz.matiere].push(quiz);
    return acc;
  }, {} as Record<string, QuizFile[]>);

  // Charger la liste des classes (pour la modale d'affectation)
  useEffect(() => {
    if (showAssignModal) {
      fetch(`${API_BASE_URL}/api/v1/classes`)
        .then(res => res.json())
        .then(data => setClassesList(data))
        .catch(() => setClassesList([]));
    }
  }, [showAssignModal]);

  // Charger la liste des élèves selon les classes sélectionnées
  useEffect(() => {
    if (showAssignModal && selectedClasses.length > 0) {
      fetch(`${API_BASE_URL}/api/v1/students?classes=${selectedClasses.join(',')}`)
        .then(res => res.json())
        .then(data => setStudentsList(data))
        .catch(() => setStudentsList([]));
    } else {
      setStudentsList([]);
    }
  }, [showAssignModal, selectedClasses]);

  // Ajout des modales pour création/édition/suppression quiz et questions
  function CreateQuizModal({ matieres, onClose, onCreated }: { matieres: string[]; onClose: () => void; onCreated: () => void }) {
    const [matiere, setMatiere] = useState(matieres[0] || '');
    const [filename, setFilename] = useState('');
    const [titre, setTitre] = useState('');
    const [auteur, setAuteur] = useState('');
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const handleSubmit = async (e: React.FormEvent) => {
      e.preventDefault();
      setLoading(true);
      setError(null);
      try {
        const res = await fetch(`${API_BASE_URL}/api/v1/quiz_json/json/${matiere}/create`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            filename: filename.endsWith('.json') ? filename : filename + '.json',
            metadata: { titre, auteur }
          })
        });
        if (!res.ok) throw new Error('Erreur création quiz');
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
          <h3 className="text-2xl font-bold text-blue-700 mb-4">Créer un quiz</h3>
          <div className="mb-3">
            <label className="block text-gray-700 font-semibold mb-1">Matière</label>
            <select value={matiere} onChange={e => setMatiere(e.target.value)} className="w-full border rounded-lg px-3 py-2">
              {matieres.map(m => <option key={m} value={m}>{m}</option>)}
            </select>
          </div>
          <div className="mb-3">
            <label className="block text-gray-700 font-semibold mb-1">Nom du fichier</label>
            <input value={filename} onChange={e => setFilename(e.target.value)} required className="w-full border rounded-lg px-3 py-2" placeholder="ex: mon_quiz" />
          </div>
          <div className="mb-3">
            <label className="block text-gray-700 font-semibold mb-1">Titre</label>
            <input value={titre} onChange={e => setTitre(e.target.value)} required className="w-full border rounded-lg px-3 py-2" />
          </div>
          <div className="mb-3">
            <label className="block text-gray-700 font-semibold mb-1">Auteur</label>
            <input value={auteur} onChange={e => setAuteur(e.target.value)} className="w-full border rounded-lg px-3 py-2" />
          </div>
          {error && <div className="text-red-600 mb-2">{error}</div>}
          <button type="submit" disabled={loading} className="px-4 py-2 bg-blue-600 text-white rounded-lg font-semibold hover:bg-blue-700 transition">
            {loading ? 'Création...' : 'Créer'}
          </button>
        </form>
      </div>
    );
  }

  function QuestionModal({ mode, question, onClose, onSave }: {
    mode: 'create' | 'edit';
    question?: QuizQuestion;
    onClose: () => void;
    onSave: (q: QuizQuestion) => void;
  }) {
    const [q, setQ] = useState<QuizQuestion>(question || {
      id: '', section: 1, type: '', difficulte: '', theme_semantique: '', prefixe: '', texte_entree: '', texte_cible: ''
    });
    const [error, setError] = useState<string | null>(null);

    const handleChange = (field: keyof QuizQuestion, value: any) => {
      setQ(prev => ({ ...prev, [field]: value }));
    };

    const handleSubmit = (e: React.FormEvent) => {
      e.preventDefault();
      if (!q.id || !q.texte_cible) {
        setError('ID et question sont obligatoires');
        return;
      }
      setError(null);
      onSave(q);
      onClose();
    };

    return (
      <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-30">
        <form onSubmit={handleSubmit} className="bg-white rounded-2xl shadow-2xl p-8 max-w-md w-full relative">
          <button type="button" onClick={onClose} className="absolute top-4 right-4 text-gray-400 hover:text-blue-600 text-xl font-bold">×</button>
          <h3 className="text-2xl font-bold text-blue-700 mb-4">{mode === 'create' ? 'Ajouter' : 'Modifier'} une question</h3>
          <div className="mb-3">
            <label className="block text-gray-700 font-semibold mb-1">ID</label>
            <input value={q.id} onChange={e => handleChange('id', e.target.value)} required className="w-full border rounded-lg px-3 py-2" />
          </div>
          <div className="mb-3">
            <label className="block text-gray-700 font-semibold mb-1">Section</label>
            <input type="number" value={q.section} onChange={e => handleChange('section', Number(e.target.value))} className="w-full border rounded-lg px-3 py-2" />
          </div>
          <div className="mb-3">
            <label className="block text-gray-700 font-semibold mb-1">Type</label>
            <input value={q.type} onChange={e => handleChange('type', e.target.value)} className="w-full border rounded-lg px-3 py-2" />
          </div>
          <div className="mb-3">
            <label className="block text-gray-700 font-semibold mb-1">Difficulté</label>
            <input value={q.difficulte} onChange={e => handleChange('difficulte', e.target.value)} className="w-full border rounded-lg px-3 py-2" />
          </div>
          <div className="mb-3">
            <label className="block text-gray-700 font-semibold mb-1">Thème</label>
            <input value={q.theme_semantique} onChange={e => handleChange('theme_semantique', e.target.value)} className="w-full border rounded-lg px-3 py-2" />
          </div>
          <div className="mb-3">
            <label className="block text-gray-700 font-semibold mb-1">Préfixe</label>
            <input value={q.prefixe} onChange={e => handleChange('prefixe', e.target.value)} className="w-full border rounded-lg px-3 py-2" />
          </div>
          <div className="mb-3">
            <label className="block text-gray-700 font-semibold mb-1">Texte d'entrée</label>
            <textarea value={q.texte_entree} onChange={e => handleChange('texte_entree', e.target.value)} className="w-full border rounded-lg px-3 py-2" />
          </div>
          <div className="mb-3">
            <label className="block text-gray-700 font-semibold mb-1">Question + choix + réponse</label>
            <textarea value={q.texte_cible} onChange={e => handleChange('texte_cible', e.target.value)} required className="w-full border rounded-lg px-3 py-2" />
          </div>
          {error && <div className="text-red-600 mb-2">{error}</div>}
          <button type="submit" className="px-4 py-2 bg-blue-600 text-white rounded-lg font-semibold hover:bg-blue-700 transition">
            {mode === 'create' ? 'Ajouter' : 'Enregistrer'}
          </button>
        </form>
      </div>
    );
  }

  // Suppression d'un quiz (fichier JSON)
  const handleDeleteQuiz = async (quiz: QuizFile) => {
    if (!window.confirm('Supprimer ce quiz ? Cette action est irréversible.')) return;
    try {
      // Suppression du fichier côté backend (à ajouter si besoin)
      const res = await fetch(`${API_BASE_URL}/api/v1/quiz_json/json/${quiz.matiere}/${quiz.filename}`, { method: 'DELETE' });
      if (!res.ok) throw new Error('Erreur suppression quiz');
      refresh();
      setSelectedQuiz(null);
      setQuizData(null);
    } catch (err) {
      alert('Erreur lors de la suppression du quiz');
    }
  };

  // Ajout d'une question
  const handleAddQuestion = async (q: QuizQuestion) => {
    if (!selectedQuiz) return;
    await fetch(`${API_BASE_URL}/api/v1/quiz_json/json/${selectedQuiz.matiere}/${selectedQuiz.filename}/add`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(q)
    });
    loadQuiz(selectedQuiz);
  };

  // Edition d'une question
  const handleEditQuestion = async (q: QuizQuestion) => {
    if (!selectedQuiz || questionEditIndex === null || !quizData) return;
    await fetch(`${API_BASE_URL}/api/v1/quiz_json/json/${selectedQuiz.matiere}/${selectedQuiz.filename}/edit/${q.id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(q)
    });
    loadQuiz(selectedQuiz);
    setQuestionEditIndex(null);
  };

  // Suppression d'une question
  const handleDeleteQuestion = async (q: QuizQuestion) => {
    if (!selectedQuiz) return;
    if (!window.confirm('Supprimer cette question ?')) return;
    await fetch(`${API_BASE_URL}/api/v1/quiz_json/json/${selectedQuiz.matiere}/${selectedQuiz.filename}/delete/${q.id}`, {
      method: 'DELETE'
    });
    loadQuiz(selectedQuiz);
  };

  const matieres = Array.from(new Set(quizFiles.map(q => q.matiere)));

  return (
    <div className="bg-white rounded-xl shadow-lg p-8 mb-8">
      <h2 className="text-xl font-bold text-gray-700 mb-4 flex items-center justify-between">
        Gestion des Quiz
        <button onClick={() => setShowCreateQuiz(true)} className="px-3 py-1 bg-blue-600 text-white rounded-lg font-semibold hover:bg-blue-700 transition text-sm">Créer un quiz</button>
      </h2>
      {loading ? (
        <div className="text-blue-600 font-semibold">Chargement...</div>
      ) : error ? (
        <div className="text-red-600 font-semibold">{error}</div>
      ) : (
        <div className="flex flex-col md:flex-row gap-8">
          {/* Liste des quiz par matière */}
          <div className="w-full md:w-1/3">
            <h3 className="text-lg font-semibold mb-2">Quiz par matière</h3>
            {Object.keys(quizzesByMatiere).length === 0 ? (
              <div className="text-gray-500 italic">Aucun quiz trouvé.</div>
            ) : (
              Object.entries(quizzesByMatiere).map(([matiere, quizzes]) => (
                <div key={matiere} className="mb-4">
                  <div className="font-bold text-blue-700 mb-1">{matiere}</div>
                  <ul className="pl-2">
                    {quizzes.map(quiz => (
                      <li key={quiz.filename} className="flex items-center gap-2">
                        <button
                          className={`text-left w-full px-2 py-1 rounded hover:bg-blue-50 ${selectedQuiz?.filename === quiz.filename && selectedQuiz?.matiere === quiz.matiere ? 'bg-blue-100 font-bold' : ''}`}
                          onClick={() => loadQuiz(quiz)}
                        >
                          {quiz.filename.replace('.json', '')}
                        </button>
                        <button onClick={() => handleDeleteQuiz(quiz)} className="text-red-600 hover:text-red-800 text-xs font-bold">Supprimer</button>
                      </li>
                    ))}
                  </ul>
                </div>
              ))
            )}
          </div>
          {/* Affichage des questions du quiz sélectionné */}
          <div className="flex-1">
            {selectedQuiz && quizData ? (
              <>
                <div className="mb-4 flex items-center justify-between">
                  <div>
                    <h3 className="text-lg font-bold text-blue-700">{selectedQuiz.filename.replace('.json', '')}</h3>
                    <div className="text-gray-600 text-sm mb-2">Matière : {selectedQuiz.matiere}</div>
                    {quizData.metadata && (
                      <div className="text-xs text-gray-500 mb-2">{quizData.metadata.titre} — {quizData.metadata.auteur}</div>
                    )}
                  </div>
                  <div className="flex gap-2">
                    <button onClick={() => setShowQuestionModal({ mode: 'create' })} className="px-3 py-1 bg-green-600 text-white rounded-lg font-semibold hover:bg-green-700 transition text-sm">Ajouter une question</button>
                    <button onClick={() => setShowAssignModal(true)} className="px-3 py-1 bg-purple-600 text-white rounded-lg font-semibold hover:bg-purple-700 transition text-sm">Affecter ce quiz</button>
                  </div>
                </div>
                <ul className="divide-y divide-gray-200">
                  {quizData.dataset_entrainement_enrichi.map((q, idx) => (
                    <li key={q.id} className="py-3 flex flex-col md:flex-row md:items-center md:justify-between gap-2">
                      <div>
                        <div className="font-semibold text-blue-800">{q.texte_cible.split('\n')[0]}</div>
                        <div className="text-xs text-gray-500">Section : {q.section} | Type : {q.type} | Difficulté : {q.difficulte}</div>
                        <div className="text-xs text-gray-500">Thème : {q.theme_semantique}</div>
                      </div>
                      <div className="flex gap-2">
                        <button onClick={() => { setShowQuestionModal({ mode: 'edit', question: q }); setQuestionEditIndex(idx); }} className="px-2 py-1 bg-yellow-500 text-white rounded-lg text-xs font-semibold hover:bg-yellow-600 transition">Modifier</button>
                        <button onClick={() => handleDeleteQuestion(q)} className="px-2 py-1 bg-red-600 text-white rounded-lg text-xs font-semibold hover:bg-red-700 transition">Supprimer</button>
                      </div>
                    </li>
                  ))}
                </ul>
              </>
            ) : (
              <div className="text-gray-500 italic">Sélectionne un quiz pour voir les questions.</div>
            )}
          </div>
        </div>
      )}
      {showCreateQuiz && <CreateQuizModal matieres={matieres} onClose={() => setShowCreateQuiz(false)} onCreated={refresh} />}
      {showQuestionModal && (
        <QuestionModal
          mode={showQuestionModal.mode}
          question={showQuestionModal.question}
          onClose={() => { setShowQuestionModal(null); setQuestionEditIndex(null); }}
          onSave={showQuestionModal.mode === 'create' ? handleAddQuestion : handleEditQuestion}
        />
      )}
      {showAssignModal && selectedQuiz && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-30">
          <div className="bg-white rounded-2xl shadow-2xl p-8 max-w-lg w-full relative">
            <button type="button" onClick={() => setShowAssignModal(false)} className="absolute top-4 right-4 text-gray-400 hover:text-blue-600 text-xl font-bold">×</button>
            <h3 className="text-2xl font-bold text-purple-700 mb-4">Affecter ce quiz</h3>
            {/* Sélecteur multi-classes */}
            <div className="mb-4">
              <label className="block text-gray-700 font-semibold mb-1">Classes</label>
              <select multiple value={selectedClasses} onChange={e => setSelectedClasses(Array.from(e.target.selectedOptions, o => o.value))} className="w-full border rounded-lg px-3 py-2">
                {classesList.map((c: any) => (
                  <option key={c.id} value={c.id}>{c.nom}</option>
                ))}
              </select>
            </div>
            {/* Sélecteur multi-élèves (optionnel) */}
            <div className="mb-4">
              <label className="block text-gray-700 font-semibold mb-1">Élèves (optionnel)</label>
              <select multiple value={selectedStudents} onChange={e => setSelectedStudents(Array.from(e.target.selectedOptions, o => o.value))} className="w-full border rounded-lg px-3 py-2">
                {studentsList.map((s: any) => (
                  <option key={s.id} value={s.id}>{s.nom}</option>
                ))}
              </select>
              <div className="text-xs text-gray-500 mt-1">Si aucun élève n'est sélectionné, le quiz sera affecté à tous les élèves des classes choisies.</div>
            </div>
            {/* Message de succès/erreur */}
            {assignSuccess && <div className="text-green-600 mb-2">{assignSuccess}</div>}
            {assignError && <div className="text-red-600 mb-2">{assignError}</div>}
            {/* Bouton de validation */}
            <button onClick={async () => {
              setAssignLoading(true);
              setAssignError(null);
              setAssignSuccess(null);
              try {
                const res = await fetch(`${API_BASE_URL}/api/v1/quiz_json/assign`, {
                  method: 'POST',
                  headers: { 'Content-Type': 'application/json' },
                  body: JSON.stringify({
                    filename: selectedQuiz.filename,
                    matiere: selectedQuiz.matiere,
                    class_ids: selectedClasses,
                    student_ids: selectedStudents
                  })
                });
                if (!res.ok) throw new Error('Erreur lors de l\'affectation');
                setAssignSuccess('Quiz affecté avec succès !');
                setTimeout(() => { setShowAssignModal(false); setAssignSuccess(null); }, 1200);
              } catch (err: any) {
                setAssignError(err.message || 'Erreur inconnue');
              } finally {
                setAssignLoading(false);
              }
            }}
            disabled={assignLoading || selectedClasses.length === 0}
            className="px-4 py-2 bg-purple-600 text-white rounded-lg font-semibold hover:bg-purple-700 transition disabled:opacity-50">
              {assignLoading ? 'Affectation...' : 'Affecter'}
            </button>
          </div>
        </div>
      )}
    </div>
  );
} 