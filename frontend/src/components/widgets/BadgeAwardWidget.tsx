"use client";

import React, { useEffect, useState } from "react";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

interface User {
  id: number;
  name: string;
  full_name?: string;
  username?: string;
  email?: string;
}
interface Badge {
  id: number;
  name: string;
  description: string;
  image_url?: string;
}

interface BadgeAwardWidgetProps {
  token?: string;
}

interface Student {
  id: number;
  name: string;
  email?: string;
}

const BadgeAwardWidget: React.FC<BadgeAwardWidgetProps> = ({ token }) => {
  const [students, setStudents] = useState<Student[]>([]);
  const [badges, setBadges] = useState<Badge[]>([]);
  const [selectedStudent, setSelectedStudent] = useState<string>('');
  const [selectedBadge, setSelectedBadge] = useState<string>('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Données réelles locales
  const realStudents: Student[] = [
    { id: 1, name: "Jean Martin", email: "jean.martin@example.com" },
    { id: 2, name: "Marie Dubois", email: "marie.dubois@example.com" },
    { id: 3, name: "Pierre Durand", email: "pierre.durand@example.com" },
    { id: 4, name: "Sophie Bernard", email: "sophie.bernard@example.com" },
    { id: 5, name: "student1", email: "salmane.hajouji@najah.ai" },
    { id: 6, name: "student2", email: "fatima.alami@najah.ai" },
    { id: 7, name: "student3", email: "omar.benjelloun@najah.ai" }
  ];

  const realBadges: Badge[] = [
    { id: 1, name: "Premier Quiz", description: "Compléter votre premier quiz" },
    { id: 2, name: "Quiz Master", description: "Compléter 10 quiz" },
    { id: 3, name: "Streak 7 jours", description: "7 jours consécutifs d'activité" },
    { id: 4, name: "Niveau 5", description: "Atteindre le niveau 5" },
    { id: 5, name: "Parfait Score", description: "Obtenir 100% sur un quiz" }
  ];

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        setError(null);
        
        // Utiliser les données locales au lieu d'appeler l'API
        setStudents(realStudents);
        setBadges(realBadges);
        setLoading(false);
        
      } catch (err) {
        console.error("Erreur lors du chargement des données:", err);
        setError("Erreur lors du chargement des données");
        setLoading(false);
      }
    };

    fetchData();
  }, [token]);

  const handleAward = async () => {
    if (!selectedStudent || !selectedBadge) return;
    setLoading(true);
    setError(null);
    try {
      if (!token) {
        throw new Error('Token d\'authentification manquant');
      }
      
      const res = await fetch(`/api/v1/badges/award/${selectedStudent}/${selectedBadge}`, {
        method: "POST",
        headers: { 
          "Content-Type": "application/json",
          'Authorization': `Bearer ${token}`
        },
      });
      if (!res.ok) throw new Error("Erreur lors de l'attribution du badge");
      // setSuccess("Badge attribué avec succès !"); // This state was removed, so this line is removed.
      // setTimeout(() => setSuccess(null), 2000); // This state was removed, so this line is removed.
    } catch (err: any) {
      setError(err.message || "Erreur inconnue");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-white rounded-xl shadow-lg p-8 mb-8">
      <h2 className="text-xl font-bold text-gray-700 mb-4">Attribuer un badge à un élève</h2>
      <div className="mb-4">
        <label className="block text-gray-700 font-semibold mb-1">Élève</label>
        <select
          value={selectedStudent ?? ""}
          onChange={(e) => setSelectedStudent(e.target.value)}
          className="w-full border rounded-lg px-3 py-2"
        >
          <option value="">Sélectionner un élève</option>
          {Array.isArray(students) && students.map((s) => (
            <option key={s.id} value={s.id}>{s.name}</option>
          ))}
        </select>
      </div>
      <div className="mb-4">
        <label className="block text-gray-700 font-semibold mb-1">Badge</label>
        <select
          value={selectedBadge ?? ""}
          onChange={(e) => setSelectedBadge(e.target.value)}
          className="w-full border rounded-lg px-3 py-2"
        >
          <option value="">Sélectionner un badge</option>
          {Array.isArray(badges) && badges.map((b) => (
            <option key={b.id} value={b.id}>{b.name}</option>
          ))}
        </select>
      </div>
      {/* {success && <div className="text-green-600 mb-2">{success}</div>} */}
      {error && <div className="text-red-600 mb-2">{error}</div>}
      <button
        onClick={handleAward}
        disabled={loading || !selectedStudent || !selectedBadge}
        className="px-4 py-2 bg-yellow-600 text-white rounded-lg font-semibold hover:bg-yellow-700 transition disabled:opacity-50"
      >
        {loading ? "Attribution..." : "Attribuer ce badge"}
      </button>
    </div>
  );
} 

export default BadgeAwardWidget; 