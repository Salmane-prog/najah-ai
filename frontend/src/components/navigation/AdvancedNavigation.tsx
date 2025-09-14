'use client';

import React, { useState } from 'react';
import { useRouter, usePathname } from 'next/navigation';
import Link from 'next/link';

interface NavigationItem {
  label: string;
  path: string;
  icon: string;
  description: string;
  children?: NavigationItem[];
}

const teacherNavigation: NavigationItem[] = [
  {
    label: 'Dashboard',
    path: '/dashboard/teacher',
    icon: '🏠',
    description: 'Vue d\'ensemble'
  },
  {
    label: 'Analytics',
    path: '/dashboard/teacher/analytics',
    icon: '📊',
    description: 'Analytics et rapports',
    children: [
      {
        label: 'Vue d\'ensemble',
        path: '/dashboard/teacher/analytics',
        icon: '📈',
        description: 'Métriques générales'
      },
      {
        label: 'Analytics Avancés',
        path: '/dashboard/teacher/analytics/advanced',
        icon: '🧠',
        description: 'Analyse cognitive et IRT'
      },
      {
        label: 'Par classe',
        path: '/dashboard/teacher/analytics/class',
        icon: '👥',
        description: 'Analytics par classe'
      },
      {
        label: 'Par étudiant',
        path: '/dashboard/teacher/analytics/student',
        icon: '👤',
        description: 'Profil étudiant détaillé'
      }
    ]
  },
  {
    label: 'Évaluations',
    path: '/dashboard/teacher/assessment',
    icon: '📝',
    description: 'Gérer les évaluations',
    children: [
      {
        label: 'Créer',
        path: '/dashboard/teacher/assessment/create',
        icon: '➕',
        description: 'Créer une évaluation'
      },
      {
        label: 'Gérer',
        path: '/dashboard/teacher/assessment/view',
        icon: '📋',
        description: 'Voir toutes les évaluations'
      },
      {
        label: 'Résultats',
        path: '/dashboard/teacher/assessment/results',
        icon: '📊',
        description: 'Analyser les résultats'
      }
    ]
  },
  {
    label: 'Banque de Questions',
    path: '/dashboard/teacher/questions',
    icon: '🗃️',
    description: 'Gérer les questions',
    children: [
      {
        label: 'Voir toutes',
        path: '/dashboard/teacher/questions',
        icon: '👁️',
        description: 'Parcourir la banque'
      },
      {
        label: 'Créer',
        path: '/dashboard/teacher/questions/create',
        icon: '➕',
        description: 'Ajouter une question'
      },
      {
        label: 'Catégories',
        path: '/dashboard/teacher/questions/categories',
        icon: '🏷️',
        description: 'Organiser par tags'
      }
    ]
  },
  {
    label: 'Profils Cognitifs',
    path: '/dashboard/teacher/cognitive-profiles',
    icon: '🧠',
    description: 'Analyser les profils',
    children: [
      {
        label: 'Vue d\'ensemble',
        path: '/dashboard/teacher/cognitive-profiles',
        icon: '📊',
        description: 'Tous les profils'
      },
      {
        label: 'Analyse Cognitive',
        path: '/dashboard/teacher/cognitive-analysis',
        icon: '🔍',
        description: 'Insights détaillés'
      }
    ]
  },
  {
    label: 'IRT & Adaptation',
    path: '/dashboard/teacher/irt',
    icon: '📈',
    description: 'Moteur IRT et adaptation',
    children: [
      {
        label: 'Dashboard IRT',
        path: '/dashboard/teacher/irt',
        icon: '📊',
        description: 'Vue d\'ensemble IRT'
      },
      {
        label: 'Paramètres d\'adaptation',
        path: '/dashboard/teacher/adaptation',
        icon: '⚙️',
        description: 'Configurer l\'adaptation'
      },
      {
        label: 'Analyse de difficulté',
        path: '/dashboard/teacher/difficulty-analysis',
        icon: '🎯',
        description: 'Analyser les niveaux'
      }
    ]
  }
];

const studentNavigation: NavigationItem[] = [
  {
    label: 'Dashboard',
    path: '/dashboard/student',
    icon: '🏠',
    description: 'Vue d\'ensemble'
  },
  {
    label: 'Évaluations',
    path: '/assessment',
    icon: '📝',
    description: 'Passer des tests',
    children: [
      {
        label: 'Passer un test',
        path: '/assessment/session',
        icon: '📋',
        description: 'Test standard'
      },
      {
        label: 'Évaluation adaptative',
        path: '/assessment/adaptive',
        icon: '🔄',
        description: 'Test intelligent'
      },
      {
        label: 'Mes résultats',
        path: '/assessment/results',
        icon: '📊',
        description: 'Voir mes scores'
      }
    ]
  },
  {
    label: 'Mon Profil',
    path: '/dashboard/student/profile',
    icon: '👤',
    description: 'Informations personnelles',
    children: [
      {
        label: 'Informations',
        path: '/dashboard/student/profile',
        icon: 'ℹ️',
        description: 'Détails du compte'
      },
      {
        label: 'Progression',
        path: '/dashboard/student/progress',
        icon: '📈',
        description: 'Suivi des progrès'
      },
      {
        label: 'Profil cognitif',
        path: '/dashboard/student/cognitive-profile',
        icon: '🧠',
        description: 'Style d\'apprentissage'
      }
    ]
  }
];

interface AdvancedNavigationProps {
  userType: 'teacher' | 'student';
  className?: string;
}

export default function AdvancedNavigation({ userType, className = '' }: AdvancedNavigationProps) {
  const router = useRouter();
  const pathname = usePathname();
  const [expandedItems, setExpandedItems] = useState<Set<string>>(new Set());

  const navigation = userType === 'teacher' ? teacherNavigation : studentNavigation;

  const toggleExpanded = (path: string) => {
    const newExpanded = new Set(expandedItems);
    if (newExpanded.has(path)) {
      newExpanded.delete(path);
    } else {
      newExpanded.add(path);
    }
    setExpandedItems(newExpanded);
  };

  const isActive = (path: string) => {
    return pathname === path || pathname.startsWith(path + '/');
  };

  const isExpanded = (path: string) => {
    return expandedItems.has(path);
  };

  return (
    <nav className={`bg-white shadow-lg rounded-lg overflow-hidden ${className}`}>
      <div className="px-4 py-6">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">
          {userType === 'teacher' ? '👨‍🏫 Navigation Enseignant' : '👨‍🎓 Navigation Étudiant'}
        </h2>
        
        <div className="space-y-2">
          {navigation.map((item) => (
            <div key={item.path}>
              {/* Item principal */}
              <div
                className={`flex items-center justify-between p-3 rounded-lg cursor-pointer transition-colors ${
                  isActive(item.path)
                    ? 'bg-blue-100 text-blue-700 border-l-4 border-blue-500'
                    : 'hover:bg-gray-100 text-gray-700'
                }`}
                onClick={() => {
                  if (item.children) {
                    toggleExpanded(item.path);
                  } else {
                    router.push(item.path);
                  }
                }}
              >
                <div className="flex items-center space-x-3">
                  <span className="text-xl">{item.icon}</span>
                  <div>
                    <div className="font-medium">{item.label}</div>
                    <div className="text-sm text-gray-500">{item.description}</div>
                  </div>
                </div>
                
                {item.children && (
                  <span className={`transform transition-transform ${isExpanded(item.path) ? 'rotate-180' : ''}`}>
                    ▼
                  </span>
                )}
              </div>

              {/* Sous-items */}
              {item.children && isExpanded(item.path) && (
                <div className="ml-8 mt-2 space-y-1">
                  {item.children.map((child) => (
                    <Link
                      key={child.path}
                      href={child.path}
                      className={`flex items-center space-x-3 p-2 rounded-lg transition-colors ${
                        isActive(child.path)
                          ? 'bg-blue-50 text-blue-600'
                          : 'hover:bg-gray-50 text-gray-600'
                      }`}
                    >
                      <span className="text-lg">{child.icon}</span>
                      <div>
                        <div className="font-medium">{child.label}</div>
                        <div className="text-sm text-gray-500">{child.description}</div>
                      </div>
                    </Link>
                  ))}
                </div>
              )}
            </div>
          ))}
        </div>

        {/* Actions rapides */}
        <div className="mt-6 pt-6 border-t border-gray-200">
          <h3 className="text-sm font-medium text-gray-900 mb-3">Actions Rapides</h3>
          
          {userType === 'teacher' ? (
            <div className="space-y-2">
              <button
                onClick={() => router.push('/dashboard/teacher/analytics/advanced')}
                className="w-full flex items-center space-x-3 p-3 bg-gradient-to-r from-blue-500 to-indigo-500 text-white rounded-lg hover:from-blue-600 hover:to-indigo-600 transition-all duration-200"
              >
                <span className="text-xl">🧠</span>
                <span>Analytics Avancés</span>
              </button>
              
              <button
                onClick={() => router.push('/dashboard/teacher/questions')}
                className="w-full flex items-center space-x-3 p-3 bg-gradient-to-r from-green-500 to-emerald-500 text-white rounded-lg hover:from-green-600 hover:to-emerald-600 transition-all duration-200"
              >
                <span className="text-xl">🗃️</span>
                <span>Banque de Questions</span>
              </button>
            </div>
          ) : (
            <div className="space-y-2">
              <button
                onClick={() => router.push('/assessment/adaptive')}
                className="w-full flex items-center space-x-3 p-3 bg-gradient-to-r from-purple-500 to-pink-500 text-white rounded-lg hover:from-purple-600 hover:to-pink-600 transition-all duration-200"
              >
                <span className="text-xl">🔄</span>
                <span>Évaluation Adaptative</span>
              </button>
              
              <button
                onClick={() => router.push('/dashboard/student/cognitive-profile')}
                className="w-full flex items-center space-x-3 p-3 bg-gradient-to-r from-indigo-500 to-blue-500 text-white rounded-lg hover:from-indigo-600 hover:to-blue-600 transition-all duration-200"
              >
                <span className="text-xl">🧠</span>
                <span>Mon Profil Cognitif</span>
              </button>
            </div>
          )}
        </div>
      </div>
    </nav>
  );
}












