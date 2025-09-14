import { useEffect, useState } from "react";
import { Student } from "@/hooks/useClassGroupDetails";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
console.log("API_BASE_URL:", API_BASE_URL);

export function useStudents() {
  const [data, setData] = useState<Student[] | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    setLoading(true);
    const token = typeof window !== "undefined" ? localStorage.getItem("najah_token") : null;
    fetch(`${API_BASE_URL}/api/v1/users/`, {
      headers: token ? { 'Authorization': `Bearer ${token}` } : {}
    })
      .then(async (res) => {
        if (!res.ok) throw new Error("Erreur lors du chargement des utilisateurs");
        const json = await res.json();
        setData(json);
      })
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, []);

  return { data, loading, error };
} 