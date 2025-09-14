import React, { useEffect, useState } from "react";
import { useClassGroups, ClassGroup } from "@/hooks/useClassGroups";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export default function ClassList({ onEdit, onManageStudents, refetch }: {
  onEdit: (cls: ClassGroup) => void;
  onManageStudents: (cls: ClassGroup) => void;
  refetch: () => void;
}) {
  const { data, loading, error } = useClassGroups();
  const [studentsByClass, setStudentsByClass] = useState<Record<number, Array<{id:number, username:string, email:string}>>>({});

  useEffect(() => {
    if (!data) return;
    const fetchStudents = async () => {
      const result: Record<number, Array<{id:number, username:string, email:string}>> = {};
      await Promise.all(data.map(async (cls) => {
        try {
          const res = await fetch(`${API_BASE_URL}/api/v1/class_groups/${cls.id}/students/`);
          if (res.ok) {
            result[cls.id] = await res.json();
          } else {
            result[cls.id] = [];
          }
        } catch {
          result[cls.id] = [];
        }
      }));
      setStudentsByClass(result);
    };
    fetchStudents();
  }, [data]);

  const handleDelete = async (cls: ClassGroup) => {
    if (!window.confirm(`Supprimer la classe "${cls.name}" ? Cette action est irréversible.`)) return;
    try {
      const res = await fetch(`${API_BASE_URL}/api/v1/class_groups/${cls.id}`, { method: "DELETE" });
      if (!res.ok) throw new Error("Erreur lors de la suppression");
      refetch();
    } catch (err: any) {
      alert(err.message);
    }
  };

  if (loading) return <div>Chargement...</div>;
  if (error) return <div className="text-red-500">Erreur : {error}</div>;

  return (
    <div className="bg-white rounded shadow p-4">
      <table className="w-full">
        <thead>
          <tr>
            <th className="text-left">Nom</th>
            <th className="text-left">Description</th>
            <th className="text-left">Actions</th>
          </tr>
        </thead>
        <tbody>
          {data && data.length > 0 ? (
            data.map((cls) => (
              <tr key={cls.id} className="border-b">
                <td>{cls.name}
                  <ul className="text-xs text-gray-600 mt-1">
                    {studentsByClass[cls.id]?.length > 0 ? (
                      studentsByClass[cls.id].map((student) => (
                        <li key={student.id}>{student.username} ({student.email})</li>
                      ))
                    ) : (
                      <li className="italic text-gray-400">Aucun élève</li>
                    )}
                  </ul>
                </td>
                <td>{cls.description || "-"}</td>
                <td>
                  <button
                    className="mr-2 px-2 py-1 bg-yellow-400 rounded"
                    onClick={() => onEdit(cls)}
                  >
                    Éditer
                  </button>
                  <button
                    className="mr-2 px-2 py-1 bg-blue-500 text-white rounded"
                    onClick={() => onManageStudents(cls)}
                  >
                    Gérer élèves
                  </button>
                  <button
                    className="px-2 py-1 bg-red-500 text-white rounded"
                    onClick={() => handleDelete(cls)}
                  >
                    Supprimer
                  </button>
                </td>
              </tr>
            ))
          ) : (
            <tr>
              <td colSpan={3} className="text-center text-gray-400 py-4">Aucune classe pour l'instant</td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  );
} 