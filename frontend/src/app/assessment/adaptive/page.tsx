'use client';

import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import AssessmentWrapper from '@/components/assessment/AssessmentWrapper';

export default function AdaptiveAssessmentPage() {
  const router = useRouter();
  const [showAssessment, setShowAssessment] = useState(false);
  const [assessmentConfig, setAssessmentConfig] = useState({
    studentId: 1, // Remplacez par l'ID réel de l'étudiant connecté
    studentName: "Alice Martin", // Remplacez par le nom réel
    subject: 'math',
    difficulty: 5,
    questionCount: 10
  });

  const handleStartAssessment = () => {
    setShowAssessment(true);
  };

  const handleAssessmentComplete = (results: any) => {
    console.log('Évaluation terminée:', results);
    
    // Rediriger vers les résultats ou le dashboard
    if (results.cognitiveProfile) {
      router.push(`/dashboard/student/cognitive-profile?profile=${JSON.stringify(results.cognitiveProfile)}`);
    } else {
      router.push('/dashboard/student');
    }
  };

  const handleCloseAssessment = () => {
    setShowAssessment(false);
    router.push('/dashboard/student');
  };

  if (showAssessment) {
    return (
      <AssessmentWrapper
        studentId={assessmentConfig.studentId}
        studentName={assessmentConfig.studentName}
        mode="evaluation"
        onComplete={handleAssessmentComplete}
        onClose={handleCloseAssessment}
      />
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      {/* Header */}
      <div className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold text-gray-900">
                🔄 Évaluation Adaptative
              </h1>
              <p className="text-gray-600 mt-1">
                Test intelligent qui s'adapte à votre niveau
              </p>
            </div>
            <button
              onClick={() => router.push('/dashboard/student')}
              className="bg-gray-100 text-gray-700 px-4 py-2 rounded-lg hover:bg-gray-200 transition-colors"
            >
              ← Retour au Dashboard
            </button>
          </div>
        </div>
      </div>

      {/* Configuration de l'évaluation */}
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="bg-white rounded-xl shadow-lg p-8">
          <div className="text-center mb-8">
            <div className="text-6xl mb-4">🧠</div>
            <h2 className="text-3xl font-bold text-gray-900 mb-4">
              Prêt pour votre évaluation intelligente ?
            </h2>
            <p className="text-lg text-gray-600 max-w-2xl mx-auto">
              Notre système d'IA analyse vos réponses en temps réel et adapte 
              automatiquement la difficulté pour optimiser votre apprentissage.
            </p>
          </div>

          {/* Options de configuration */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
            <div className="bg-blue-50 rounded-lg p-6 text-center">
              <div className="text-2xl mb-2">📚</div>
              <h3 className="font-semibold text-gray-900 mb-2">Matière</h3>
              <select
                value={assessmentConfig.subject}
                onChange={(e) => setAssessmentConfig(prev => ({ ...prev, subject: e.target.value }))}
                className="w-full p-2 border rounded-md bg-white"
              >
                <option value="math">Mathématiques</option>
                <option value="french">Français</option>
                <option value="science">Sciences</option>
                <option value="history">Histoire</option>
              </select>
            </div>

            <div className="bg-green-50 rounded-lg p-6 text-center">
              <div className="text-2xl mb-2">🎯</div>
              <h3 className="font-semibold text-gray-900 mb-2">Difficulté initiale</h3>
              <select
                value={assessmentConfig.difficulty}
                onChange={(e) => setAssessmentConfig(prev => ({ ...prev, difficulty: parseInt(e.target.value) }))}
                className="w-full p-2 border rounded-md bg-white"
              >
                <option value={3}>Facile (3)</option>
                <option value={5}>Moyen (5)</option>
                <option value={7}>Difficile (7)</option>
              </select>
            </div>

            <div className="bg-purple-50 rounded-lg p-6 text-center">
              <div className="text-2xl mb-2">❓</div>
              <h3 className="font-semibold text-gray-900 mb-2">Nombre de questions</h3>
              <select
                value={assessmentConfig.questionCount}
                onChange={(e) => setAssessmentConfig(prev => ({ ...prev, questionCount: parseInt(e.target.value) }))}
                className="w-full p-2 border rounded-md bg-white"
              >
                <option value={5}>5 questions</option>
                <option value={10}>10 questions</option>
                <option value={15}>15 questions</option>
                <option value={20}>20 questions</option>
              </select>
            </div>
          </div>

          {/* Fonctionnalités avancées */}
          <div className="bg-gradient-to-r from-indigo-50 to-purple-50 rounded-lg p-6 mb-8">
            <h3 className="text-lg font-semibold text-gray-900 mb-4 text-center">
              🚀 Fonctionnalités Avancées
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="flex items-center space-x-3">
                <div className="text-green-500">✅</div>
                <span className="text-gray-700">Analyse cognitive en temps réel</span>
              </div>
              <div className="flex items-center space-x-3">
                <div className="text-green-500">✅</div>
                <span className="text-gray-700">Adaptation automatique de la difficulté</span>
              </div>
              <div className="flex items-center space-x-3">
                <div className="text-green-500">✅</div>
                <span className="text-gray-700">Détection des patterns d'apprentissage</span>
              </div>
              <div className="flex items-center space-x-3">
                <div className="text-green-500">✅</div>
                <span className="text-gray-700">Profil cognitif personnalisé</span>
              </div>
            </div>
          </div>

          {/* Bouton de démarrage */}
          <div className="text-center">
            <button
              onClick={handleStartAssessment}
              className="bg-gradient-to-r from-blue-600 to-indigo-600 text-white px-8 py-4 rounded-lg text-lg font-semibold hover:from-blue-700 hover:to-indigo-700 transition-all duration-200 transform hover:scale-105 shadow-lg"
            >
              🚀 Commencer l'Évaluation
            </button>
            <p className="text-gray-500 mt-3">
              Temps estimé : {Math.ceil(assessmentConfig.questionCount * 2)} minutes
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}















