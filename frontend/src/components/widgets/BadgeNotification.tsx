import React, { useState, useEffect } from 'react';
import { Award, X, CheckCircle } from 'lucide-react';

interface BadgeNotificationProps {
  badges: string[];
  isVisible: boolean;
  onClose: () => void;
  onDismiss: () => void;
}

export default function BadgeNotification({ 
  badges, 
  isVisible, 
  onClose, 
  onDismiss 
}: BadgeNotificationProps) {
  const [isAnimating, setIsAnimating] = useState(false);

  useEffect(() => {
    if (isVisible && badges.length > 0) {
      setIsAnimating(true);
      
      // Auto-hide après 8 secondes
      const timer = setTimeout(() => {
        onClose();
      }, 8000);

      return () => clearTimeout(timer);
    }
  }, [isVisible, badges, onClose]);

  if (!isVisible || badges.length === 0) return null;

  return (
    <div className="fixed top-4 right-4 z-50 animate-in slide-in-from-right-2 duration-300">
      <div className="bg-gradient-to-r from-yellow-400 to-orange-500 rounded-lg shadow-2xl border-2 border-yellow-300 p-4 max-w-sm">
        {/* Header avec bouton fermer */}
        <div className="flex items-center justify-between mb-3">
          <div className="flex items-center gap-2">
            <Award className="text-white" size={20} />
            <span className="text-white font-bold text-lg">
              Nouveaux badges !
            </span>
          </div>
          <button
            onClick={onClose}
            className="text-white hover:text-yellow-200 transition-colors"
          >
            <X size={18} />
          </button>
        </div>

        {/* Liste des badges */}
        <div className="space-y-2 mb-3">
          {badges.map((badge, index) => (
            <div key={index} className="flex items-center gap-2 bg-white/20 rounded-lg p-2">
              <CheckCircle className="text-green-400" size={16} />
              <span className="text-white font-medium text-sm">{badge}</span>
            </div>
          ))}
        </div>

        {/* Footer avec bouton de fermeture */}
        <div className="flex justify-between items-center">
          <span className="text-white/80 text-xs">
            {badges.length} badge(s) attribué(s) automatiquement
          </span>
          <button
            onClick={onDismiss}
            className="text-white/80 hover:text-white text-xs underline"
          >
            Ne plus afficher
          </button>
        </div>

        {/* Barre de progression */}
        <div className="w-full bg-white/20 rounded-full h-1 mt-3">
          <div 
            className="bg-white h-1 rounded-full transition-all duration-300 ease-linear"
            style={{ width: '100%' }}
          />
        </div>
      </div>
    </div>
  );
}
