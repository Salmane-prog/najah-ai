"use client";
import React, { useState } from "react";
import ClassList from "@/components/classes/ClassList";
import ClassForm from "@/components/classes/ClassForm";
import ClassStudents from "@/components/classes/ClassStudents";
import { useClassGroups, ClassGroup } from "@/hooks/useClassGroups";

export default function ClassesPage() {
  const [showForm, setShowForm] = useState(false);
  const [editClass, setEditClass] = useState<ClassGroup | null>(null);
  const [selectedClass, setSelectedClass] = useState<ClassGroup | null>(null);
  const [showStudents, setShowStudents] = useState(false);
  const { refetch } = useClassGroups();

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">Gestion des classes</h1>
      <button
        className="bg-blue-600 text-white px-4 py-2 rounded mb-4"
        onClick={() => {
          setEditClass(null);
          setShowForm(true);
        }}
      >
        + Nouvelle classe
      </button>
      <ClassList
        onEdit={cls => {
          setEditClass(cls);
          setShowForm(true);
        }}
        onManageStudents={cls => {
          setSelectedClass(cls);
          setShowStudents(true);
        }}
        refetch={refetch}
      />
      {showForm && (
        <ClassForm
          editClass={editClass}
          onClose={() => setShowForm(false)}
          onSuccess={refetch}
        />
      )}
      {showStudents && selectedClass && (
        <ClassStudents
          classGroup={selectedClass}
          onClose={() => setShowStudents(false)}
        />
      )}
    </div>
  );
} 