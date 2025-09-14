'use client';

import React from 'react';
import { IntelligentStudentDashboard } from '../../components/widgets';

export default function DemoIntelligentPage() {
  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-7xl mx-auto">
        <div className="mb-6">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            Démonstration - Dashboard Intelligent
          </h1>
          <p className="text-gray-600">
            Testez les nouveaux widgets intelligents intégrés avec les endpoints backend
          </p>
        </div>
        
        <IntelligentStudentDashboard />
      </div>
    </div>
  );
}







