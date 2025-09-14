"use client";

import React from 'react';
import { useDashboard } from '../../contexts/DashboardContext';

interface ClassGroup {
  id: number;
  name: string;
  level: string;
  student_count: number;
}

interface Student {
  id: number;
  name: string;
  progression: number; // Pour la démo, progression en %
}

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export default function ClassesWidget() {
  const { refreshTrigger } = useDashboard();
  const [classes, setClasses] = React.useState<ClassGroup[]>([]);
  const [loading, setLoading] = React.useState(true);
  const [error, setError] = React.useState<string | null>(null);
  const [selectedClass, setSelectedClass] = React.useState<ClassGroup | null>(null);
  const [isModalOpen, setIsModalOpen] = React.useState(false);
  const [students, setStudents] = React.useState<Student[]>([]);
  const [loadingStudents, setLoadingStudents] = React.useState(false);
  const [errorStudents, setErrorStudents] = React.useState<string | null>(null);

  React.useEffect(() => {
    setLoading(true);
    const token = typeof window !== "undefined" ? localStorage.getItem("najah_token") : null;
    fetch(`${API_BASE_URL}/api/v1/teacher/classes/`, {
      headers: {
        ...(token ? { 'Authorization': `Bearer ${token}` } : {}),
        'Content-Type': 'application/json'
      }
    })
      .then(res => {
        if (!res.ok) throw new Error('Erreur lors du chargement des classes');
        return res.json();
      })
      .then((data: ClassGroup[]) => {
        setClasses(data);
        setLoading(false);
        setError(null);
      })
      .catch(err => {
        setError(err.message || 'Erreur inconnue');
        setLoading(false);
      });
  }, [refreshTrigger]); // Ajouter refreshTrigger comme dépendance

  const fetchStudentProgression = async (studentId: number): Promise<number> => {
    try {
      const res = await fetch(`${API_BASE_URL}/api/v1/learning_history/?student_id=${studentId}`);
      if (!res.ok) throw new Error('Erreur progression');
      const history = await res.json();
      // Exemple : progression = % d'items complétés (ou score moyen si dispo)
      if (Array.isArray(history) && history.length > 0) {
        // Si chaque item a un champ 'progress' ou 'score', on peut faire la moyenne
        const scores = history.map((h: any) => typeof h.score === 'number' ? h.score : 1); // fallback 1 si pas de score
        const avg = Math.round((scores.reduce((a, b) => a + b, 0) / scores.length) * 100);
        return avg > 100 ? 100 : avg;
      }
      return 0;
    } catch {
      return 0;
    }
  };

  const handleClassClick = async (classGroup: ClassGroup) => {
    setSelectedClass(classGroup);
    setIsModalOpen(true);
    setLoadingStudents(true);
    setErrorStudents(null);
    setStudents([]);
    // On suppose que GET /api/v1/class_groups/{id} retourne les élèves dans un champ 'students'
    try {
      const res = await fetch(`${API_BASE_URL}/api/v1/teacher/classes/${classGroup.id}/students`);
      if (!res.ok) throw new Error('Erreur lors du chargement des élèves');
      const data = await res.json();
      const studentsRaw: unknown[] = Array.isArray(data) ? data : [];
      // Pour chaque élève, on va chercher la progression réelle
      const students: Student[] = await Promise.all(studentsRaw.map(async (s) => {
        if (typeof s === 'object' && s !== null) {
          const stu = s as Record<string, unknown>;
          const id = Number(stu.id);
          const name = String(stu.name || stu.username || stu.email || `Élève #${stu.id}`);
          const progression = await fetchStudentProgression(id);
          return { id, name, progression };
        }
        return { id: 0, name: 'Élève inconnu', progression: 0 };
      }));
      setStudents(students);
      setLoadingStudents(false);
    } catch (err: any) {
      setErrorStudents(err.message || 'Erreur inconnue');
      setLoadingStudents(false);
    }
  };
  const closeModal = () => {
    setIsModalOpen(false);
    setSelectedClass(null);
    setStudents([]);
  };

  return (
    <div className="bg-white rounded-xl shadow-lg p-8 mb-8">
      <h2 className="text-xl font-bold text-gray-700 mb-4">Mes classes</h2>
      {loading ? (
        <div className="text-blue-600 font-semibold">Chargement...</div>
      ) : error ? (
        <div className="text-red-600 font-semibold">{error}</div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {classes.map((classGroup) => (
            <div
              key={classGroup.id}
              className="p-6 bg-blue-50 rounded-xl shadow-md cursor-pointer hover:scale-105 transition"
              onClick={() => handleClassClick(classGroup)}
            >
              <div className="text-lg font-bold text-blue-700 mb-2">{classGroup.name}</div>
              <div className="text-sm text-gray-600 mb-1">Niveau : {classGroup.level}</div>
              <div className="text-sm text-gray-600">Élèves : <span className="font-semibold text-blue-800">{classGroup.student_count}</span></div>
            </div>
          ))}
        </div>
      )}

      {/* Modale de détail de la classe */}
      {isModalOpen && selectedClass && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-30">
          <div className="bg-white rounded-2xl shadow-2xl p-8 max-w-lg w-full relative">
            <button onClick={closeModal} className="absolute top-4 right-4 text-gray-400 hover:text-blue-600 text-xl font-bold">×</button>
            <h3 className="text-2xl font-bold text-blue-700 mb-2">{selectedClass.name}</h3>
            <div className="mb-2 text-gray-600">Niveau : {selectedClass.level}</div>
            <div className="mb-4 text-gray-600">Nombre d&apos;élèves : <span className="font-semibold text-blue-800">{selectedClass.student_count}</span></div>
            <div className="mb-4 flex gap-2 justify-end">
              <button
                onClick={async () => {
                  const url = `${API_BASE_URL}/api/v1/reports/class/${selectedClass.id}/export?format=csv`;
                  const res = await fetch(url);
                  if (!res.ok) { alert('Erreur export CSV'); return; }
                  const blob = await res.blob();
                  const link = document.createElement('a');
                  link.href = window.URL.createObjectURL(blob);
                  link.download = `rapport_classe_${selectedClass.id}.csv`;
                  document.body.appendChild(link);
                  link.click();
                  document.body.removeChild(link);
                }}
                className="px-4 py-2 bg-blue-600 text-white rounded-lg font-semibold hover:bg-blue-700 transition"
              >
                Exporter (CSV)
              </button>
              <button
                onClick={async () => {
                  const url = `${API_BASE_URL}/api/v1/reports/class/${selectedClass.id}/export?format=pdf`;
                  const res = await fetch(url);
                  if (!res.ok) { alert('Erreur export PDF'); return; }
                  const blob = await res.blob();
                  const link = document.createElement('a');
                  link.href = window.URL.createObjectURL(blob);
                  link.download = `rapport_classe_${selectedClass.id}.pdf`;
                  document.body.appendChild(link);
                  link.click();
                  document.body.removeChild(link);
                }}
                className="px-4 py-2 bg-purple-600 text-white rounded-lg font-semibold hover:bg-purple-700 transition"
              >
                Exporter (PDF)
              </button>
            </div>
            <h4 className="text-lg font-semibold text-gray-800 mb-2">Liste des élèves</h4>
            {loadingStudents ? (
              <div className="text-blue-600 font-semibold">Chargement des élèves...</div>
            ) : errorStudents ? (
              <div className="text-red-600 font-semibold">{errorStudents}</div>
            ) : students.length === 0 ? (
              <div className="text-gray-500 italic">Aucun élève dans cette classe.</div>
            ) : (
              <ul className="divide-y divide-gray-200">
                {students.map((student) => (
                  <li key={student.id} className="py-2 flex items-center justify-between">
                    <span className="font-medium text-gray-700">{student.name}</span>
                    <span className="text-sm text-blue-700 font-semibold">Progression : {student.progression}%</span>
                  </li>
                ))}
              </ul>
            )}
          </div>
        </div>
      )}
    </div>
  );
} 