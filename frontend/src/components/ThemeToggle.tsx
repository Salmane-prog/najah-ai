"use client";
import React, { useState } from 'react';
import { useTheme } from '../contexts/ThemeContext';
import { Sun, Moon, Monitor, ChevronDown } from 'lucide-react';

const ThemeToggle: React.FC = () => {
  const { theme, setTheme, isDark, toggleTheme } = useTheme();
  const [showDropdown, setShowDropdown] = useState(false);

  const themes = [
    { value: 'light', label: 'Clair', icon: Sun },
    { value: 'dark', label: 'Sombre', icon: Moon },
    { value: 'system', label: 'Système', icon: Monitor },
  ];

  const currentTheme = themes.find(t => t.value === theme);
  const CurrentIcon = currentTheme?.icon || Sun;

  return (
    <div className="relative">
      {/* Bouton principal */}
      <button
        onClick={() => setShowDropdown(!showDropdown)}
        className="flex items-center space-x-2 px-3 py-2 text-gray-600 hover:text-gray-900 hover:bg-gray-100 dark:text-gray-300 dark:hover:text-gray-100 dark:hover:bg-gray-800 rounded-lg transition-colors"
        aria-label="Changer le thème"
      >
        <CurrentIcon className="w-5 h-5" />
        <span className="hidden sm:block text-sm">{currentTheme?.label}</span>
        <ChevronDown className={`w-4 h-4 transition-transform ${showDropdown ? 'rotate-180' : ''}`} />
      </button>

      {/* Dropdown */}
      {showDropdown && (
        <div className="absolute right-0 mt-2 w-48 bg-white dark:bg-gray-800 rounded-lg shadow-lg border border-gray-200 dark:border-gray-700 z-50">
          <div className="py-1">
            {themes.map((themeOption) => {
              const Icon = themeOption.icon;
              return (
                <button
                  key={themeOption.value}
                  onClick={() => {
                    setTheme(themeOption.value as 'light' | 'dark' | 'system');
                    setShowDropdown(false);
                  }}
                  className={`w-full flex items-center space-x-3 px-4 py-2 text-sm transition-colors ${
                    theme === themeOption.value
                      ? 'bg-blue-50 dark:bg-blue-900 text-blue-600 dark:text-blue-400'
                      : 'text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700'
                  }`}
                >
                  <Icon className="w-4 h-4" />
                  <span>{themeOption.label}</span>
                  {theme === themeOption.value && (
                    <div className="ml-auto w-2 h-2 bg-blue-500 rounded-full"></div>
                  )}
                </button>
              );
            })}
          </div>
        </div>
      )}

      {/* Overlay pour fermer le dropdown */}
      {showDropdown && (
        <div
          className="fixed inset-0 z-40"
          onClick={() => setShowDropdown(false)}
        />
      )}
    </div>
  );
};

export default ThemeToggle; 