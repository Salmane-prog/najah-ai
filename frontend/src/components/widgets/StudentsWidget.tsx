"use client";

import React, { useEffect, useState } from 'react';
import { useDashboard } from '../../contexts/DashboardContext';
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

interface Student {
  id: number;
  name: string;
  email: string;
  className?: string;
}

interface StudentsWidgetProps {
  classId?: number;
}

// Composant de détail élève (modale)
function StudentDetailModal({ student, onClose }: { student: Student | null; onClose: () => void }) {
  const [profile, setProfile] = useState<unknown>(null);
  const [progression, setProgression] = useState<number>(0);
  const [badges, setBadges] = useState<unknown[]>([]);
  const [quiz, setQuiz] = useState<unknown[]>([]);
  const [parcours, setParcours] = useState<unknown[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (!student) return;
    setLoading(true);
    const token = typeof window !== "undefined" ? localStorage.getItem("najah_token") : null;
    const headers: Record<string, string> = {};
    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }
    
    Promise.all([
      fetch(`${API_BASE_URL}/api/v1/users/${student.id}`, { headers }).then(r => r.ok ? r.json() : null),
      fetch(`${API_BASE_URL}/api/v1/learning_history/?student_id=${student.id}`, { headers }).then(r => r.ok ? r.json() : []),
      fetch(`${API_BASE_URL}/api/v1/badges/user/${student.id}`, { headers }).then(r => r.ok ? r.json() : []),
      fetch(`${API_BASE_URL}/api/v1/quiz_results/user/${student.id}`, { headers }).then(r => r.ok ? r.json() : []),
      fetch(`${API_BASE_URL}/api/v1/learning_paths/`, { headers }).then(r => r.ok ? r.json() : [])
    ]).then(([profile, history, badges, quiz, parcours]) => {
      setProfile(profile);
      setBadges(Array.isArray(badges) ? badges : []);
      setQuiz(Array.isArray(quiz) ? quiz : []);
      const parcoursArray = Array.isArray(parcours) ? parcours : [];
      setParcours(parcoursArray.filter((p: unknown) => {
        if (typeof p === 'object' && p !== null) {
          const path = p as { students?: unknown[] };
          return path.students?.some((s: unknown) => {
            if (typeof s === 'object' && s !== null) {
              const student = s as { id?: unknown };
              return student.id === student.id;
            }
            return false;
          });
        }
        return false;
      }));
      // Progression simple : % d'items dans l'historique
      const historyArray = Array.isArray(history) ? history : [];
      setProgression(historyArray.length > 0 ? Math.round((historyArray.length / 10) * 100) : 0);
      setLoading(false);
    });
  }, [student]);

  if (!student) return null;
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-30">
      <div className="bg-white rounded-2xl shadow-2xl p-8 max-w-lg w-full relative">
        <button onClick={onClose} className="absolute top-4 right-4 text-gray-400 hover:text-blue-600 text-xl font-bold">×</button>
        <h3 className="text-2xl font-bold text-blue-700 mb-2">{student.name}</h3>
        <div className="mb-2 text-gray-600">Email : {student.email}</div>
        <div className="mb-2 text-gray-600">Classe : {student.className || '-'}</div>
        {loading ? (
          <div className="text-blue-600 font-semibold">Chargement...</div>
        ) : (
          <>
            <div className="mb-2 text-gray-700 font-semibold">Progression : {progression}%</div>
            <div className="mb-2 text-gray-700 font-semibold">Badges : {badges.length}</div>
            <div className="mb-2 text-gray-700 font-semibold">Quiz complétés : {quiz.length}</div>
            <div className="mb-2 text-gray-700 font-semibold">Parcours assignés : {parcours.length}</div>
            {/* On peut détailler chaque section ici si besoin */}
          </>
        )}
      </div>
    </div>
  );
}

export default function StudentsWidget({ classId }: StudentsWidgetProps) {
  const { refreshTrigger } = useDashboard();
  const [students, setStudents] = useState<Student[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [search, setSearch] = useState('');
  const [sortKey, setSortKey] = useState<'name' | 'email'>('name');
  const [sortAsc, setSortAsc] = useState(true);
  const [selectedStudent, setSelectedStudent] = useState<Student | null>(null);

  useEffect(() => {
    setLoading(true);
    setError(null);
    const token = typeof window !== "undefined" ? localStorage.getItem("najah_token") : null;
    const headers: Record<string, string> = {};
    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }
    
    if (classId) {
      fetch(`${API_BASE_URL}/api/v1/teacher/classes/${classId}/students`, { headers })
        .then(res => {
          if (!res.ok) throw new Error('Erreur lors du chargement des élèves de la classe');
          return res.json();
        })
        .then(data => {
          const studentsRaw: unknown[] = Array.isArray(data) ? data : [];
          const students: Student[] = studentsRaw.map((s) => {
            if (typeof s === 'object' && s !== null) {
              const stu = s as Record<string, unknown>;
              return {
                id: Number(stu.id),
                name: String(stu.name || stu.username || stu.email || `Élève #${stu.id}`),
                email: String(stu.email || ''),
                className: String(stu.class_name || stu.class || ''),
              };
            }
            return { id: 0, name: 'Élève inconnu', email: '', className: '' };
          });
          setStudents(students);
          setLoading(false);
        })
        .catch(err => {
          setError(err.message || 'Erreur inconnue');
          setLoading(false);
        });
    } else {
      fetch(`${API_BASE_URL}/api/v1/users/students-by-role`, { headers })
        .then(res => {
          if (!res.ok) throw new Error('Erreur lors du chargement des utilisateurs');
          return res.json();
        })
        .then((data: unknown[]) => {
          if (!Array.isArray(data)) {
            throw new Error('Réponse inattendue du serveur');
          }
          const students: Student[] = data
            .filter(u => typeof u === 'object' && u !== null && (u as { role?: unknown }).role === 'student')
            .map(u => {
              const user = u as { id?: unknown; name?: unknown; username?: unknown; email?: unknown; class?: unknown };
              return {
                id: Number(user.id),
                name: String(user.name || user.username || user.email || `Élève #${user.id}`),
                email: String(user.email || ''),
                className: String(user.class || ''),
              };
            });
          setStudents(students);
          setLoading(false);
        })
        .catch(err => {
          setError(err.message || 'Erreur inconnue');
          setLoading(false);
        });
    }
  }, [classId, refreshTrigger]); // Ajouter refreshTrigger comme dépendance

  // Filtrage et tri
  const filtered = students.filter(s =>
    s.name.toLowerCase().includes(search.toLowerCase()) ||
    s.email.toLowerCase().includes(search.toLowerCase())
  );
  const sorted = [...filtered].sort((a, b) => {
    const valA = a[sortKey].toLowerCase();
    const valB = b[sortKey].toLowerCase();
    if (valA < valB) return sortAsc ? -1 : 1;
    if (valA > valB) return sortAsc ? 1 : -1;
    return 0;
  });

  return (
    <div className="bg-white rounded-xl shadow-lg p-8 mb-8">
      <h2 className="text-xl font-bold text-gray-700 mb-4">
        {classId ? 'Élèves de la classe' : 'Tous les élèves'}
      </h2>
      {/* Contrôles de recherche et tri */}
      <div className="flex flex-wrap items-center gap-4 mb-4">
        <input
          type="text"
          placeholder="Rechercher par nom ou email..."
          value={search}
          onChange={e => setSearch(e.target.value)}
          className="border rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-400"
        />
        <button
          className={`px-3 py-2 rounded-lg text-sm font-medium ${sortKey === 'name' ? 'bg-blue-100 text-blue-700' : 'bg-gray-100 text-gray-700'}`}
          onClick={() => setSortKey('name')}
        >
          Trier par nom
        </button>
        <button
          className={`px-3 py-2 rounded-lg text-sm font-medium ${sortKey === 'email' ? 'bg-blue-100 text-blue-700' : 'bg-gray-100 text-gray-700'}`}
          onClick={() => setSortKey('email')}
        >
          Trier par email
        </button>
        <button
          className="px-3 py-2 rounded-lg text-sm font-medium bg-gray-100 text-gray-700"
          onClick={() => setSortAsc(a => !a)}
        >
          {sortAsc ? 'Ascendant' : 'Descendant'}
        </button>
      </div>
      {loading ? (
        <div className="text-blue-600 font-semibold">Chargement...</div>
      ) : error ? (
        <div className="text-red-600 font-semibold">{error}</div>
      ) : sorted.length === 0 ? (
        <div className="text-gray-500 italic">Aucun élève trouvé.</div>
      ) : (
        <table className="min-w-full divide-y divide-gray-200">
          <thead>
            <tr>
              <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">Nom</th>
              <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">Email</th>
              {!classId && (
                <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase">Classe</th>
              )}
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-100">
            {sorted.map(student => (
              <tr
                key={student.id}
                className="hover:bg-blue-50 transition cursor-pointer"
                onClick={() => setSelectedStudent(student)}
              >
                <td className="px-4 py-2 font-medium text-gray-800">{student.name}</td>
                <td className="px-4 py-2 text-gray-700">{student.email}</td>
                {!classId && (
                  <td className="px-4 py-2 text-gray-700">{student.className}</td>
                )}
              </tr>
            ))}
          </tbody>
        </table>
      )}
      {/* Modale de détail élève */}
      {selectedStudent && (
        <StudentDetailModal student={selectedStudent} onClose={() => setSelectedStudent(null)} />
      )}
    </div>
  );
} 