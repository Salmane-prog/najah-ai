import React, { useState } from "react";
import { ClassGroup } from "@/hooks/useClassGroups";

interface Props {
  editClass: ClassGroup | null;
  onClose: () => void;
  onSuccess?: () => void;
}

export default function ClassForm({ editClass, onClose, onSuccess }: Props) {
  const [name, setName] = useState(editClass?.name || "");
  const [description, setDescription] = useState(editClass?.description || "");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      const method = editClass ? "PUT" : "POST";
      const url = editClass
        ? `/api/v1/class_groups/${editClass.id}`
        : "/api/v1/class_groups/";
      const res = await fetch(url, {
        method,
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, description }),
      });
      if (!res.ok) throw new Error("Erreur lors de l'enregistrement de la classe");
      if (onSuccess) onSuccess();
      onClose();
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-30 flex items-center justify-center z-50">
      <div className="bg-white rounded shadow p-6 w-full max-w-md">
        <h2 className="text-xl font-bold mb-4">
          {editClass ? "Modifier la classe" : "Créer une nouvelle classe"}
        </h2>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block font-medium mb-1">Nom *</label>
            <input
              type="text"
              className="w-full border rounded px-3 py-2"
              value={name}
              onChange={e => setName(e.target.value)}
              required
            />
          </div>
          <div>
            <label className="block font-medium mb-1">Description</label>
            <input
              type="text"
              className="w-full border rounded px-3 py-2"
              value={description}
              onChange={e => setDescription(e.target.value)}
            />
          </div>
          {error && <div className="text-red-500">{error}</div>}
          <div className="flex justify-end gap-2">
            <button
              type="button"
              className="px-4 py-2 bg-gray-300 rounded"
              onClick={onClose}
              disabled={loading}
            >
              Annuler
            </button>
            <button
              type="submit"
              className="px-4 py-2 bg-blue-600 text-white rounded"
              disabled={loading}
            >
              {loading ? "Enregistrement..." : editClass ? "Enregistrer" : "Créer"}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
} 