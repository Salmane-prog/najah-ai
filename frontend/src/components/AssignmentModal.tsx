'use client';

import React, { useState } from 'react';
import { X, Users, BookOpen, Calendar, CheckCircle, AlertCircle } from 'lucide-react';
import { Class, User, AssignmentData } from '../types/adaptiveEvaluation';

interface AssignmentModalProps {
  isOpen: boolean;
  onClose: () => void;
  testTitle: string;
  onSubmit: (data: AssignmentData) => Promise<void>;
  classes: Class[];
  students: User[];
  isLoadingClasses: boolean;
  isLoadingStudents: boolean;
}

export default function AssignmentModal({
  isOpen,
  onClose,
  testTitle,
  onSubmit,
  classes,
  students,
  isLoadingClasses,
  isLoadingStudents
}: AssignmentModalProps) {
  const [assignmentData, setAssignmentData] = useState<AssignmentData>({
    class_ids: [],
    student_ids: [],
    due_date: ''
  });
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [activeTab, setActiveTab] = useState<'classes' | 'students'>('classes');

  const handleClassToggle = (classId: number) => {
    setAssignmentData(prev => ({
      ...prev,
      class_ids: prev.class_ids.includes(classId)
        ? prev.class_ids.filter(id => id !== classId)
        : [...prev.class_ids, classId]
    }));
  };

  const handleStudentToggle = (studentId: number) => {
    setAssignmentData(prev => ({
      ...prev,
      student_ids: prev.student_ids.includes(studentId)
        ? prev.student_ids.filter(id => id !== studentId)
        : [...prev.student_ids, studentId]
    }));
  };

  const handleSubmit = async () => {
    if (assignmentData.class_ids.length === 0 && assignmentData.student_ids.length === 0) {
      alert('Veuillez sélectionner au moins une classe ou un étudiant');
      return;
    }

    setIsSubmitting(true);
    try {
      await onSubmit(assignmentData);
      onClose();
      setAssignmentData({ class_ids: [], student_ids: [], due_date: '' });
    } catch (error) {
      console.error('Erreur lors de l\'assignation:', error);
      alert('Erreur lors de l\'assignation du test');
    } finally {
      setIsSubmitting(false);
    }
  };

  const totalTargets = assignmentData.class_ids.length + assignmentData.student_ids.length;

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg shadow-xl w-full max-w-4xl max-h-[90vh] overflow-hidden">
        {/* Header */}
        <div className="bg-gradient-to-r from-purple-600 to-blue-600 text-white p-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <BookOpen className="w-6 h-6" />
              <div>
                <h2 className="text-xl font-semibold">Assigner le Test</h2>
                <p className="text-purple-100 text-sm">{testTitle}</p>
              </div>
            </div>
            <button
              onClick={onClose}
              className="text-white hover:text-purple-200 transition-colors"
            >
              <X className="w-6 h-6" />
            </button>
          </div>
        </div>

        {/* Content */}
        <div className="p-6 space-y-6">
          {/* Date d'échéance */}
          <div className="space-y-2">
            <label className="flex items-center space-x-2 text-sm font-medium text-gray-700">
              <Calendar className="w-4 h-4" />
              <span>Date d'échéance (optionnel)</span>
            </label>
            <input
              type="datetime-local"
              value={assignmentData.due_date}
              onChange={(e) => setAssignmentData(prev => ({ ...prev, due_date: e.target.value }))}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent"
            />
          </div>

          {/* Tabs */}
          <div className="border-b border-gray-200">
            <nav className="-mb-px flex space-x-8">
              <button
                onClick={() => setActiveTab('classes')}
                className={`py-2 px-1 border-b-2 font-medium text-sm ${
                  activeTab === 'classes'
                    ? 'border-purple-500 text-purple-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                <div className="flex items-center space-x-2">
                  <Users className="w-4 h-4" />
                  <span>Classes ({assignmentData.class_ids.length})</span>
                </div>
              </button>
              <button
                onClick={() => setActiveTab('students')}
                className={`py-2 px-1 border-b-2 font-medium text-sm ${
                  activeTab === 'students'
                    ? 'border-purple-500 text-purple-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                <div className="flex items-center space-x-2">
                  <Users className="w-4 h-4" />
                  <span>Étudiants Individuels ({assignmentData.student_ids.length})</span>
                </div>
              </button>
            </nav>
          </div>

          {/* Tab Content */}
          <div className="min-h-[400px]">
            {activeTab === 'classes' ? (
              <div className="space-y-4">
                <h3 className="text-lg font-medium text-gray-900">Sélectionner les Classes</h3>
                
                {isLoadingClasses ? (
                  <div className="flex items-center justify-center py-8">
                    <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-purple-600"></div>
                  </div>
                ) : classes.length === 0 ? (
                  <div className="text-center py-8 text-gray-500">
                    <Users className="w-12 h-12 mx-auto mb-3 text-gray-300" />
                    <p>Aucune classe disponible</p>
                  </div>
                ) : (
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    {classes.map((cls) => (
                      <div
                        key={cls.id}
                        className={`p-4 border-2 rounded-lg cursor-pointer transition-all ${
                          assignmentData.class_ids.includes(cls.id)
                            ? 'border-purple-500 bg-purple-50'
                            : 'border-gray-200 hover:border-gray-300'
                        }`}
                        onClick={() => handleClassToggle(cls.id)}
                      >
                        <div className="flex items-start justify-between">
                          <div className="flex-1">
                            <h4 className="font-medium text-gray-900">{cls.name}</h4>
                            <p className="text-sm text-gray-600 mt-1">{cls.description}</p>
                          </div>
                          <div className={`w-5 h-5 rounded-full border-2 flex items-center justify-center ${
                            assignmentData.class_ids.includes(cls.id)
                              ? 'border-purple-500 bg-purple-500'
                              : 'border-gray-300'
                          }`}>
                            {assignmentData.class_ids.includes(cls.id) && (
                              <CheckCircle className="w-4 h-4 text-white" />
                            )}
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            ) : (
              <div className="space-y-4">
                <h3 className="text-lg font-medium text-gray-900">Sélectionner les Étudiants</h3>
                
                {isLoadingStudents ? (
                  <div className="flex items-center justify-center py-8">
                    <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-purple-600"></div>
                  </div>
                ) : students.length === 0 ? (
                  <div className="text-center py-8 text-gray-500">
                    <Users className="w-12 h-12 mx-auto mb-3 text-gray-300" />
                    <p>Aucun étudiant disponible</p>
                  </div>
                ) : (
                  <div className="space-y-3">
                    {students.map((student) => (
                      <div
                        key={student.id}
                        className={`p-3 border-2 rounded-lg cursor-pointer transition-all ${
                          assignmentData.student_ids.includes(student.id)
                            ? 'border-purple-500 bg-purple-50'
                            : 'border-gray-200 hover:border-gray-300'
                        }`}
                        onClick={() => handleStudentToggle(student.id)}
                      >
                        <div className="flex items-center justify-between">
                          <div className="flex items-center space-x-3">
                            <div className="w-8 h-8 bg-purple-100 rounded-full flex items-center justify-center">
                              <span className="text-purple-600 font-medium text-sm">
                                {student.first_name[0]}{student.last_name[0]}
                              </span>
                            </div>
                            <div>
                              <p className="font-medium text-gray-900">
                                {student.first_name} {student.last_name}
                              </p>
                              <p className="text-sm text-gray-600">{student.email}</p>
                            </div>
                          </div>
                          <div className={`w-5 h-5 rounded-full border-2 flex items-center justify-center ${
                            assignmentData.student_ids.includes(student.id)
                              ? 'border-purple-500 bg-purple-500'
                              : 'border-gray-300'
                          }`}>
                            {assignmentData.student_ids.includes(student.id) && (
                              <CheckCircle className="w-4 h-4 text-white" />
                            )}
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            )}
          </div>

          {/* Summary */}
          {totalTargets > 0 && (
            <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
              <div className="flex items-center space-x-2 text-blue-800">
                <AlertCircle className="w-5 h-5" />
                <span className="font-medium">Résumé de l'assignation</span>
              </div>
              <div className="mt-2 text-sm text-blue-700">
                <p>• {assignmentData.class_ids.length} classe(s) sélectionnée(s)</p>
                <p>• {assignmentData.student_ids.length} étudiant(s) sélectionné(s)</p>
                <p>• Total : {totalTargets} cible(s)</p>
                {assignmentData.due_date && (
                  <p>• Date d'échéance : {new Date(assignmentData.due_date).toLocaleDateString('fr-FR')}</p>
                )}
              </div>
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="bg-gray-50 px-6 py-4 flex items-center justify-between">
          <button
            onClick={onClose}
            className="px-4 py-2 text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 transition-colors"
          >
            Annuler
          </button>
          
          <button
            onClick={handleSubmit}
            disabled={totalTargets === 0 || isSubmitting}
            className={`px-6 py-2 rounded-md font-medium transition-colors ${
              totalTargets === 0 || isSubmitting
                ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
                : 'bg-purple-600 text-white hover:bg-purple-700'
            }`}
          >
            {isSubmitting ? (
              <div className="flex items-center space-x-2">
                <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                <span>Assignation...</span>
              </div>
            ) : (
              `Assigner à ${totalTargets} cible${totalTargets > 1 ? 's' : ''}`
            )}
          </button>
        </div>
      </div>
    </div>
  );
}
