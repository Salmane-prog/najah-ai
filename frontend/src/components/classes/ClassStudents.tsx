import React, { useState, useEffect } from "react";
import { useClassGroupDetails } from "@/hooks/useClassGroupDetails";
import { useStudents } from "@/hooks/useStudents";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export default function ClassStudents({ classGroup, onClose }: {
  classGroup: { id: number; name: string };
  onClose: () => void;
}) {
  const { data, loading, error } = useClassGroupDetails(classGroup?.id);
  const { data: allStudents, loading: loadingStudents, error: errorStudents } = useStudents();
  const [selectedStudent, setSelectedStudent] = useState<string>("");
  const [actionLoading, setActionLoading] = useState(false);
  const [actionError, setActionError] = useState<string | null>(null);
  const [refreshKey, setRefreshKey] = useState(0);
  const [studentsPerformance, setStudentsPerformance] = useState<any[]>([]);
  const [loadingPerformance, setLoadingPerformance] = useState(false);
  const [errorPerformance, setErrorPerformance] = useState<string | null>(null);

  // Rafraîchir la liste après ajout/retrait
  const refetch = () => setRefreshKey(k => k + 1);

  useEffect(() => {
    if (!classGroup?.id) return;
    setLoadingPerformance(true);
    setErrorPerformance(null);
    fetch(`${API_BASE_URL}/api/v1/student_performance/class/${classGroup.id}/students-performance`)
      .then(res => {
        if (!res.ok) throw new Error("Erreur lors du chargement des élèves");
        return res.json();
      })
      .then(data => setStudentsPerformance(data))
      .catch(e => setErrorPerformance(e.message))
      .finally(() => setLoadingPerformance(false));
  }, [classGroup?.id, refreshKey]);

  // Ajout d'un élève
  const handleAdd = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedStudent) return;
    setActionLoading(true);
    setActionError(null);
    try {
      const res = await fetch(`${API_BASE_URL}/api/v1/class_groups/${classGroup.id}/students/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ student_id: Number(selectedStudent) }),
      });
      if (!res.ok) throw new Error("Erreur lors de l'ajout de l'élève");
      setSelectedStudent("");
      refetch();
    } catch (err: any) {
      setActionError(err.message);
    } finally {
      setActionLoading(false);
    }
  };

  // Retrait d'un élève
  const handleRemove = async (studentId: number) => {
    if (!window.confirm("Retirer cet élève de la classe ?")) return;
    setActionLoading(true);
    setActionError(null);
    try {
      const res = await fetch(`${API_BASE_URL}/api/v1/class_groups/${classGroup.id}/students/${studentId}`, {
        method: "DELETE"
      });
      if (!res.ok) throw new Error("Erreur lors du retrait de l'élève");
      refetch();
    } catch (err: any) {
      setActionError(err.message);
    } finally {
      setActionLoading(false);
    }
  };

  // Filtrer les élèves non déjà inscrits
  const availableStudents = allStudents && data ? allStudents.filter(s => !data.students.some(e => e.id === s.id)) : [];

  return (
    <div className="fixed inset-0 bg-black bg-opacity-30 flex items-center justify-center z-50">
      <div className="bg-white rounded shadow p-6 w-full max-w-lg">
        <h2 className="text-xl font-bold mb-4">
          Gérer les élèves de la classe : {classGroup?.name}
        </h2>
        {(loading || loadingStudents || actionLoading) && <div>Chargement...</div>}
        {error && <div className="text-red-500">Erreur : {error}</div>}
        {errorStudents && <div className="text-red-500">Erreur : {errorStudents}</div>}
        {actionError && <div className="text-red-500">{actionError}</div>}
        {data && (
          <div>
            <h3 className="font-semibold mb-2">Élèves inscrits :</h3>
            {loadingPerformance && <div>Chargement des élèves...</div>}
            {errorPerformance && <div className="text-red-500">{errorPerformance}</div>}
            {studentsPerformance && studentsPerformance.length > 0 ? (
              <table className="mb-4 w-full text-xs">
                <thead>
                  <tr>
                    <th>Nom</th>
                    <th>Email</th>
                    <th>Progression</th>
                    <th>Badges</th>
                    <th>Quiz</th>
                    <th>Parcours</th>
                    <th></th>
                  </tr>
                </thead>
                <tbody>
                  {studentsPerformance.map((student) => (
                    <tr key={student.id}>
                      <td>{student.username}</td>
                      <td>{student.email}</td>
                      <td>{student.progression}%</td>
                      <td>{student.badges}</td>
                      <td>{student.quiz_completed}</td>
                      <td>{student.parcours_assigned}</td>
                      <td>
                        <button
                          className="ml-2 px-2 py-1 bg-red-500 text-white rounded"
                          onClick={() => handleRemove(student.id)}
                          disabled={actionLoading}
                        >
                          Retirer
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            ) : (
              !loadingPerformance && <div className="text-gray-500 mb-4">Aucun élève dans cette classe.</div>
            )}
            <form onSubmit={handleAdd} className="flex gap-2 items-end mb-2">
              <div>
                <label className="block font-medium mb-1">Ajouter un élève</label>
                <select
                  className="border rounded px-2 py-1"
                  value={selectedStudent}
                  onChange={e => setSelectedStudent(e.target.value)}
                  disabled={actionLoading || availableStudents.length === 0}
                >
                  <option value="">-- Sélectionner --</option>
                  {availableStudents.map(s => (
                    <option key={s.id} value={s.id}>{s.username} ({s.email})</option>
                  ))}
                </select>
              </div>
              <button
                type="submit"
                className="px-4 py-2 bg-blue-600 text-white rounded"
                disabled={actionLoading || !selectedStudent}
              >
                Ajouter
              </button>
            </form>
          </div>
        )}
        <button className="mt-4 px-4 py-2 bg-gray-300 rounded" onClick={onClose} disabled={actionLoading}>Fermer</button>
      </div>
    </div>
  );
} 