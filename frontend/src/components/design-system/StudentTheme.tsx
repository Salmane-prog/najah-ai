// Design System pour la partie étudiant
export const StudentTheme = {
  colors: {
    primary: {
      50: '#eff6ff',
      100: '#dbeafe',
      500: '#3b82f6',
      600: '#2563eb',
      700: '#1d4ed8',
    },
    secondary: {
      50: '#f0f9ff',
      100: '#e0f2fe',
      500: '#0ea5e9',
      600: '#0284c7',
    },
    success: {
      50: '#f0fdf4',
      100: '#dcfce7',
      500: '#22c55e',
      600: '#16a34a',
    },
    warning: {
      50: '#fffbeb',
      100: '#fef3c7',
      500: '#f59e0b',
      600: '#d97706',
    },
    danger: {
      50: '#fef2f2',
      100: '#fee2e2',
      500: '#ef4444',
      600: '#dc2626',
    },
    neutral: {
      50: '#f9fafb',
      100: '#f3f4f6',
      200: '#e5e7eb',
      300: '#d1d5db',
      400: '#9ca3af',
      500: '#6b7280',
      600: '#4b5563',
      700: '#374151',
      800: '#1f2937',
      900: '#111827',
    }
  },
  
  spacing: {
    xs: '0.25rem',
    sm: '0.5rem',
    md: '1rem',
    lg: '1.5rem',
    xl: '2rem',
    '2xl': '3rem',
    '3xl': '4rem',
  },
  
  borderRadius: {
    sm: '0.25rem',
    md: '0.375rem',
    lg: '0.5rem',
    xl: '0.75rem',
    '2xl': '1rem',
    full: '9999px',
  },
  
  shadows: {
    sm: '0 1px 2px 0 rgb(0 0 0 / 0.05)',
    md: '0 4px 6px -1px rgb(0 0 0 / 0.1)',
    lg: '0 10px 15px -3px rgb(0 0 0 / 0.1)',
    xl: '0 20px 25px -5px rgb(0 0 0 / 0.1)',
  },
  
  typography: {
    h1: 'text-3xl font-bold text-gray-900',
    h2: 'text-2xl font-semibold text-gray-800',
    h3: 'text-xl font-semibold text-gray-800',
    h4: 'text-lg font-medium text-gray-700',
    body: 'text-base text-gray-600',
    caption: 'text-sm text-gray-500',
    button: 'text-sm font-medium',
  },
  
  animations: {
    fadeIn: 'animate-fade-in',
    slideUp: 'animate-slide-up',
    pulse: 'animate-pulse',
    bounce: 'animate-bounce',
  }
};

// Composants de base pour étudiants
export const StudentComponents = {
  Card: {
    base: 'bg-white rounded-lg shadow-sm border border-gray-200',
    interactive: 'bg-white rounded-lg shadow-sm border border-gray-200 hover:shadow-md transition-shadow cursor-pointer',
    elevated: 'bg-white rounded-lg shadow-lg border border-gray-200',
  },
  
  Button: {
    primary: 'bg-blue-600 hover:bg-blue-700 text-white font-medium px-4 py-2 rounded-lg transition-colors',
    secondary: 'bg-gray-100 hover:bg-gray-200 text-gray-700 font-medium px-4 py-2 rounded-lg transition-colors',
    success: 'bg-green-600 hover:bg-green-700 text-white font-medium px-4 py-2 rounded-lg transition-colors',
    danger: 'bg-red-600 hover:bg-red-700 text-white font-medium px-4 py-2 rounded-lg transition-colors',
    outline: 'border border-gray-300 hover:bg-gray-50 text-gray-700 font-medium px-4 py-2 rounded-lg transition-colors',
  },
  
  Badge: {
    success: 'bg-green-100 text-green-800 text-xs font-medium px-2.5 py-0.5 rounded-full',
    warning: 'bg-yellow-100 text-yellow-800 text-xs font-medium px-2.5 py-0.5 rounded-full',
    danger: 'bg-red-100 text-red-800 text-xs font-medium px-2.5 py-0.5 rounded-full',
    info: 'bg-blue-100 text-blue-800 text-xs font-medium px-2.5 py-0.5 rounded-full',
  },
  
  Progress: {
    container: 'w-full bg-gray-200 rounded-full h-2',
    bar: 'bg-gradient-to-r from-blue-500 to-purple-600 h-2 rounded-full transition-all duration-300',
  }
}; 