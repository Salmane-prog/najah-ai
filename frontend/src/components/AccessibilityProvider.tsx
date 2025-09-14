"use client";
import React, { createContext, useContext, useEffect, useState } from 'react';

interface AccessibilitySettings {
  highContrast: boolean;
  largeText: boolean;
  reducedMotion: boolean;
  screenReader: boolean;
  keyboardNavigation: boolean;
  focusIndicator: boolean;
}

interface AccessibilityContextType {
  settings: AccessibilitySettings;
  updateSettings: (newSettings: Partial<AccessibilitySettings>) => void;
  toggleSetting: (setting: keyof AccessibilitySettings) => void;
}

const AccessibilityContext = createContext<AccessibilityContextType | undefined>(undefined);

export const useAccessibility = () => {
  const context = useContext(AccessibilityContext);
  if (context === undefined) {
    throw new Error('useAccessibility must be used within an AccessibilityProvider');
  }
  return context;
};

interface AccessibilityProviderProps {
  children: React.ReactNode;
}

export const AccessibilityProvider: React.FC<AccessibilityProviderProps> = ({ children }) => {
  const [settings, setSettings] = useState<AccessibilitySettings>({
    highContrast: false,
    largeText: false,
    reducedMotion: false,
    screenReader: false,
    keyboardNavigation: false,
    focusIndicator: true,
  });

  // Charger les paramètres depuis localStorage
  useEffect(() => {
    const savedSettings = localStorage.getItem('accessibility-settings');
    if (savedSettings) {
      setSettings(JSON.parse(savedSettings));
    }
  }, []);

  // Sauvegarder les paramètres
  useEffect(() => {
    localStorage.setItem('accessibility-settings', JSON.stringify(settings));
  }, [settings]);

  // Appliquer les paramètres au document
  useEffect(() => {
    const root = document.documentElement;
    
    // Contraste élevé
    root.classList.toggle('high-contrast', settings.highContrast);
    
    // Texte large
    root.classList.toggle('large-text', settings.largeText);
    
    // Mouvement réduit
    root.classList.toggle('reduced-motion', settings.reducedMotion);
    
    // Navigation clavier
    root.classList.toggle('keyboard-navigation', settings.keyboardNavigation);
    
    // Indicateur de focus
    root.classList.toggle('focus-indicator', settings.focusIndicator);
  }, [settings]);

  const updateSettings = (newSettings: Partial<AccessibilitySettings>) => {
    setSettings(prev => ({ ...prev, ...newSettings }));
  };

  const toggleSetting = (setting: keyof AccessibilitySettings) => {
    setSettings(prev => ({ ...prev, [setting]: !prev[setting] }));
  };

  return (
    <AccessibilityContext.Provider value={{ settings, updateSettings, toggleSetting }}>
      {children}
    </AccessibilityContext.Provider>
  );
}; 