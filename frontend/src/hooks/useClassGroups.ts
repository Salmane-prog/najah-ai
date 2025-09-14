import { useEffect, useState, useCallback } from "react";

export interface ClassGroup {
  id: number;
  name: string;
  description?: string;
  teacher_id?: number;
}

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export function useClassGroups() {
  const [data, setData] = useState<ClassGroup[] | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchClasses = useCallback(() => {
    setLoading(true);
    const token = typeof window !== "undefined" ? localStorage.getItem("najah_token") : null;
    fetch(`${API_BASE_URL}/api/v1/class_groups/`, {
      headers: token ? { 'Authorization': `Bearer ${token}` } : {}
    })
      .then(async (res) => {
        if (!res.ok) throw new Error("Erreur lors du chargement des classes");
        const json = await res.json();
        setData(json);
      })
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, []);

  useEffect(() => {
    fetchClasses();
  }, [fetchClasses]);

  return { data, loading, error, refetch: fetchClasses };
} 