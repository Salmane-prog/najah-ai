// Configuration des routes de l'application
// Intègre les nouvelles fonctionnalités avancées

export const APP_ROUTES = {
  // Routes principales
  HOME: '/',
  LOGIN: '/login',
  REGISTER: '/register',
  
  // Dashboard étudiant
  STUDENT_DASHBOARD: '/dashboard/student',
  STUDENT_PROFILE: '/dashboard/student/profile',
  STUDENT_PROGRESS: '/dashboard/student/progress',
  
  // Dashboard enseignant
  TEACHER_DASHBOARD: '/dashboard/teacher',
  TEACHER_CLASSES: '/dashboard/teacher/classes',
  TEACHER_STUDENTS: '/dashboard/teacher/students',
  
  // Analytics et rapports
  ANALYTICS_OVERVIEW: '/dashboard/teacher/analytics',
  ANALYTICS_CLASS: '/dashboard/teacher/analytics/class',
  ANALYTICS_STUDENT: '/dashboard/teacher/analytics/student',
  ANALYTICS_ADVANCED: '/dashboard/teacher/analytics/advanced',
  
  // Évaluations
  ASSESSMENT_CREATE: '/dashboard/teacher/assessment/create',
  ASSESSMENT_EDIT: '/dashboard/teacher/assessment/edit',
  ASSESSMENT_VIEW: '/dashboard/teacher/assessment/view',
  ASSESSMENT_RESULTS: '/dashboard/teacher/assessment/results',
  
  // Évaluation adaptative
  ADAPTIVE_ASSESSMENT: '/assessment/adaptive',
  ASSESSMENT_SESSION: '/assessment/session',
  ASSESSMENT_RESULTS_DETAILED: '/assessment/results',
  
  // Banque de questions
  QUESTION_BANK: '/dashboard/teacher/questions',
  QUESTION_CREATE: '/dashboard/teacher/questions/create',
  QUESTION_EDIT: '/dashboard/teacher/questions/edit',
  QUESTION_CATEGORIES: '/dashboard/teacher/questions/categories',
  
  // Profils cognitifs
  COGNITIVE_PROFILES: '/dashboard/teacher/cognitive-profiles',
  COGNITIVE_ANALYSIS: '/dashboard/teacher/cognitive-analysis',
  STUDENT_COGNITIVE_PROFILE: '/dashboard/student/cognitive-profile',
  
  // IRT et adaptation
  IRT_DASHBOARD: '/dashboard/teacher/irt',
  ADAPTATION_SETTINGS: '/dashboard/teacher/adaptation',
  DIFFICULTY_ANALYSIS: '/dashboard/teacher/difficulty-analysis',
  
  // Rapports et exports
  REPORTS_WEEKLY: '/dashboard/teacher/reports/weekly',
  REPORTS_MONTHLY: '/dashboard/teacher/reports/monthly',
  REPORTS_CUSTOM: '/dashboard/teacher/reports/custom',
  EXPORT_DATA: '/dashboard/teacher/export',
  
  // Configuration
  SETTINGS: '/dashboard/settings',
  USER_PROFILE: '/dashboard/profile',
  SYSTEM_CONFIG: '/dashboard/admin/config'
};

// Configuration des sous-routes pour les analytics
export const ANALYTICS_ROUTES = {
  OVERVIEW: {
    path: '/dashboard/teacher/analytics',
    label: 'Vue d\'ensemble',
    icon: '📊',
    description: 'Vue générale des performances'
  },
  CLASS_ANALYSIS: {
    path: '/dashboard/teacher/analytics/class',
    label: 'Analyse de classe',
    icon: '👥',
    description: 'Analytics détaillés par classe'
  },
  STUDENT_ANALYSIS: {
    path: '/dashboard/teacher/analytics/student',
    label: 'Analyse d\'étudiant',
    icon: '👤',
    description: 'Profil détaillé d\'un étudiant'
  },
  ADVANCED_ANALYTICS: {
    path: '/dashboard/teacher/analytics/advanced',
    label: 'Analytics avancés',
    icon: '🧠',
    description: 'Analyse cognitive et IRT'
  },
  COGNITIVE_INSIGHTS: {
    path: '/dashboard/teacher/analytics/cognitive',
    label: 'Insights cognitifs',
    icon: '🧠',
    description: 'Analyse des patterns d\'apprentissage'
  },
  IRT_ANALYSIS: {
    path: '/dashboard/teacher/analytics/irt',
    label: 'Analyse IRT',
    icon: '📈',
    description: 'Théorie de réponse aux items'
  },
  TEMPORAL_TRENDS: {
    path: '/dashboard/teacher/analytics/trends',
    label: 'Tendances temporelles',
    icon: '📅',
    description: 'Évolution dans le temps'
  }
};

// Configuration des routes d'évaluation
export const ASSESSMENT_ROUTES = {
  CREATE: {
    path: '/dashboard/teacher/assessment/create',
    label: 'Créer une évaluation',
    icon: '➕',
    description: 'Créer une nouvelle évaluation'
  },
  ADAPTIVE: {
    path: '/assessment/adaptive',
    label: 'Évaluation adaptative',
    icon: '🔄',
    description: 'Évaluation qui s\'adapte au niveau'
  },
  SESSION: {
    path: '/assessment/session',
    label: 'Session d\'évaluation',
    icon: '📝',
    description: 'Passer une évaluation'
  },
  RESULTS: {
    path: '/assessment/results',
    label: 'Résultats',
    icon: '📊',
    description: 'Voir les résultats'
  }
};

// Configuration des composants pour chaque route
export const ROUTE_COMPONENTS = {
  [APP_ROUTES.ANALYTICS_ADVANCED]: 'AdvancedAnalyticsDashboard',
  [APP_ROUTES.ADAPTIVE_ASSESSMENT]: 'AdvancedAssessmentInterface',
  [APP_ROUTES.COGNITIVE_ANALYSIS]: 'CognitiveAnalysisDashboard',
  [APP_ROUTES.IRT_DASHBOARD]: 'IRTDashboard'
};

// Configuration des permissions par route
export const ROUTE_PERMISSIONS = {
  [APP_ROUTES.ANALYTICS_ADVANCED]: ['teacher', 'admin'],
  [APP_ROUTES.ADAPTIVE_ASSESSMENT]: ['student', 'teacher', 'admin'],
  [APP_ROUTES.COGNITIVE_ANALYSIS]: ['teacher', 'admin'],
  [APP_ROUTES.IRT_DASHBOARD]: ['teacher', 'admin'],
  [APP_ROUTES.QUESTION_BANK]: ['teacher', 'admin'],
  [APP_ROUTES.ASSESSMENT_CREATE]: ['teacher', 'admin'],
  [APP_ROUTES.ASSESSMENT_EDIT]: ['teacher', 'admin']
};

// Configuration des breadcrumbs
export const BREADCRUMB_CONFIG = {
  [APP_ROUTES.ANALYTICS_ADVANCED]: [
    { label: 'Dashboard', path: APP_ROUTES.TEACHER_DASHBOARD },
    { label: 'Analytics', path: APP_ROUTES.ANALYTICS_OVERVIEW },
    { label: 'Avancés', path: APP_ROUTES.ANALYTICS_ADVANCED }
  ],
  [APP_ROUTES.ADAPTIVE_ASSESSMENT]: [
    { label: 'Dashboard', path: APP_ROUTES.STUDENT_DASHBOARD },
    { label: 'Évaluation', path: APP_ROUTES.ASSESSMENT_SESSION },
    { label: 'Adaptative', path: APP_ROUTES.ADAPTIVE_ASSESSMENT }
  ],
  [APP_ROUTES.COGNITIVE_ANALYSIS]: [
    { label: 'Dashboard', path: APP_ROUTES.TEACHER_DASHBOARD },
    { label: 'Analytics', path: APP_ROUTES.ANALYTICS_OVERVIEW },
    { label: 'Cognitif', path: APP_ROUTES.COGNITIVE_ANALYSIS }
  ]
};

// Configuration des métadonnées des pages
export const PAGE_METADATA = {
  [APP_ROUTES.ANALYTICS_ADVANCED]: {
    title: 'Analytics Avancés - Najah AI',
    description: 'Dashboard analytics avancé avec analyse cognitive et IRT',
    keywords: ['analytics', 'cognitive', 'IRT', 'éducation', 'IA']
  },
  [APP_ROUTES.ADAPTIVE_ASSESSMENT]: {
    title: 'Évaluation Adaptative - Najah AI',
    description: 'Interface d\'évaluation adaptative intelligente',
    keywords: ['évaluation', 'adaptative', 'IA', 'éducation', 'apprentissage']
  },
  [APP_ROUTES.COGNITIVE_ANALYSIS]: {
    title: 'Analyse Cognitive - Najah AI',
    description: 'Analyse des patterns d\'apprentissage et profils cognitifs',
    keywords: ['cognitive', 'apprentissage', 'patterns', 'éducation', 'IA']
  }
};

// Configuration des menus de navigation
export const NAVIGATION_MENUS = {
  TEACHER: {
    analytics: {
      label: 'Analytics',
      icon: '📊',
      items: [
        { label: 'Vue d\'ensemble', path: APP_ROUTES.ANALYTICS_OVERVIEW },
        { label: 'Par classe', path: APP_ROUTES.ANALYTICS_CLASS },
        { label: 'Par étudiant', path: APP_ROUTES.ANALYTICS_STUDENT },
        { label: 'Avancés', path: APP_ROUTES.ANALYTICS_ADVANCED },
        { label: 'Cognitif', path: APP_ROUTES.COGNITIVE_ANALYSIS },
        { label: 'IRT', path: APP_ROUTES.IRT_DASHBOARD }
      ]
    },
    assessment: {
      label: 'Évaluations',
      icon: '📝',
      items: [
        { label: 'Créer', path: APP_ROUTES.ASSESSMENT_CREATE },
        { label: 'Gérer', path: APP_ROUTES.ASSESSMENT_VIEW },
        { label: 'Résultats', path: APP_ROUTES.ASSESSMENT_RESULTS }
      ]
    },
    questions: {
      label: 'Banque de questions',
      icon: '❓',
      items: [
        { label: 'Voir toutes', path: APP_ROUTES.QUESTION_BANK },
        { label: 'Créer', path: APP_ROUTES.QUESTION_CREATE },
        { label: 'Catégories', path: APP_ROUTES.QUESTION_CATEGORIES }
      ]
    }
  },
  STUDENT: {
    assessment: {
      label: 'Évaluations',
      icon: '📝',
      items: [
        { label: 'Passer un test', path: APP_ROUTES.ASSESSMENT_SESSION },
        { label: 'Adaptative', path: APP_ROUTES.ADAPTIVE_ASSESSMENT },
        { label: 'Mes résultats', path: APP_ROUTES.ASSESSMENT_RESULTS }
      ]
    },
    profile: {
      label: 'Mon profil',
      icon: '👤',
      items: [
        { label: 'Informations', path: APP_ROUTES.STUDENT_PROFILE },
        { label: 'Progression', path: APP_ROUTES.STUDENT_PROGRESS },
        { label: 'Profil cognitif', path: APP_ROUTES.STUDENT_COGNITIVE_PROFILE }
      ]
    }
  }
};

export default {
  APP_ROUTES,
  ANALYTICS_ROUTES,
  ASSESSMENT_ROUTES,
  ROUTE_COMPONENTS,
  ROUTE_PERMISSIONS,
  BREADCRUMB_CONFIG,
  PAGE_METADATA,
  NAVIGATION_MENUS
};















