"use client";

import React, { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Brain } from 'lucide-react';
import GapAnalysis from './GapAnalysis';
import AdaptiveQuizzes from './AdaptiveQuizzes';
import CognitiveDiagnostic from './CognitiveDiagnostic';

type TabType = 'gaps' | 'adaptive' | 'cognitive';

const AdvancedAI: React.FC = () => {
  const [activeTab, setActiveTab] = useState<TabType>('gaps');

  const tabs = [
    { id: 'gaps', label: 'Analyse des Lacunes', component: <GapAnalysis /> },
    { id: 'adaptive', label: 'Tests Adaptatifs', component: <AdaptiveQuizzes /> },
    { id: 'cognitive', label: 'Diagnostic Cognitif', component: <CognitiveDiagnostic /> },
  ];

  return (
    <div className="relative h-screen flex flex-col">
      {/* Header fixe */}
      <div className="flex-shrink-0 p-6 bg-white border-b border-gray-200">
        <div className="flex items-center justify-between">
          <h1 className="text-3xl font-bold">Fonctionnalités IA Avancées</h1>
          <Badge variant="outline" className="text-sm">
            <Brain className="h-4 w-4 mr-1" />
            IA Intelligente
          </Badge>
        </div>

        {/* Navigation par onglets */}
        <div className="border-b border-gray-200 mt-6">
          <nav className="flex space-x-8">
            {tabs.map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id as TabType)}
                className={`flex items-center gap-2 py-4 px-1 border-b-2 font-medium text-sm transition-colors ${
                  activeTab === tab.id
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                {tab.label}
              </button>
            ))}
          </nav>
        </div>
      </div>

      {/* Contenu avec scroll */}
      <div className="flex-1 overflow-y-auto p-6">
        {tabs.find(tab => tab.id === activeTab)?.component}
      </div>
    </div>
  );
};

export default AdvancedAI; 