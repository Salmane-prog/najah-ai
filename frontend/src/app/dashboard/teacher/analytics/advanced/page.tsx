'use client';

import React from 'react';
import { useRouter } from 'next/navigation';
import AnalyticsWrapper from '@/components/analytics/AnalyticsWrapper';

export default function AdvancedAnalyticsPage() {
  const router = useRouter();

  const handleNavigate = (route: string) => {
    router.push(route);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header de la page */}
      <div className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold text-gray-900">
                📊 Analytics Avancés
              </h1>
              <p className="text-gray-600 mt-1">
                Analyse cognitive, IRT et insights intelligents
              </p>
            </div>
            <div className="flex space-x-3">
              <button
                onClick={() => router.push('/dashboard/teacher/analytics')}
                className="bg-gray-100 text-gray-700 px-4 py-2 rounded-lg hover:bg-gray-200 transition-colors"
              >
                ← Retour aux Analytics
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Contenu principal avec le composant AnalyticsWrapper */}
      <AnalyticsWrapper
        viewMode="overview"
        onNavigate={handleNavigate}
        teacherId={1} // Remplacez par l'ID réel de l'enseignant connecté
      />
    </div>
  );
}















