import { useEffect, useState } from "react";
import { ClassGroup } from "@/hooks/useClassGroups";

export interface Student {
  id: number;
  username: string;
  email: string;
}

export interface ClassGroupDetails extends ClassGroup {
  students: Student[];
}

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export function useClassGroupDetails(classId: number | undefined) {
  const [data, setData] = useState<ClassGroupDetails | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!classId) return;
    setLoading(true);
    const token = typeof window !== "undefined" ? localStorage.getItem("najah_token") : null;
    fetch(`${API_BASE_URL}/api/v1/class_groups/${classId}`, {
      headers: token ? { 'Authorization': `Bearer ${token}` } : {}
    })
      .then(async (res) => {
        if (!res.ok) throw new Error("Erreur lors du chargement de la classe");
        const json = await res.json();
        setData(json);
      })
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, [classId]);

  return { data, loading, error };
} 