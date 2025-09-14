'use client';

import React from 'react';

interface SimpleIconProps {
  name: string;
  size?: 'xs' | 'sm' | 'md' | 'lg' | 'xl' | '2xl' | '3xl';
  color?: 'primary' | 'secondary' | 'success' | 'warning' | 'danger' | 'info' | 'neutral' | 'muted';
  className?: string;
}

const sizeMap = {
  xs: 'icon-xs',
  sm: 'icon-sm',
  md: 'icon-md',
  lg: 'icon-lg',
  xl: 'icon-xl',
  '2xl': 'icon-2xl',
  '3xl': 'icon-3xl'
};

const colorMap = {
  primary: 'icon-primary',
  secondary: 'icon-secondary',
  success: 'icon-success',
  warning: 'icon-warning',
  danger: 'icon-danger',
  info: 'icon-info',
  neutral: 'icon-neutral',
  muted: 'icon-muted'
};

// Icônes simples avec des formes géométriques basiques
const SimpleIconComponent = ({ name, size = 'md', color = 'neutral', className = '' }: SimpleIconProps) => {
  const sizeClass = sizeMap[size];
  const colorClass = colorMap[color];
  
  const renderIcon = () => {
    switch (name) {
      // Formes géométriques basiques
      case 'circle':
        return (
          <svg className={`icon ${sizeClass} ${colorClass} ${className}`} viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <circle cx="12" cy="12" r="10" strokeWidth="2"/>
          </svg>
        );
      
      case 'square':
        return (
          <svg className={`icon ${sizeClass} ${colorClass} ${className}`} viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <rect x="3" y="3" width="18" height="18" rx="2" strokeWidth="2"/>
          </svg>
        );
      
      case 'triangle':
        return (
          <svg className={`icon ${sizeClass} ${colorClass} ${className}`} viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <path d="M12 2L2 22h20L12 2z" strokeWidth="2"/>
          </svg>
        );
      
      case 'diamond':
        return (
          <svg className={`icon ${sizeClass} ${colorClass} ${className}`} viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <path d="M12 2L22 12L12 22L2 12L12 2z" strokeWidth="2"/>
          </svg>
        );
      
      case 'hexagon':
        return (
          <svg className={`icon ${sizeClass} ${colorClass} ${className}`} viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <path d="M12 2L22 8.5V15.5L12 22L2 15.5V8.5L12 2z" strokeWidth="2"/>
          </svg>
        );
      
      case 'star':
        return (
          <svg className={`icon ${sizeClass} ${colorClass} ${className}`} viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <path d="M12 2L15.09 8.26L22 9L17 14.14L18.18 21L12 17.77L5.82 21L7 14.14L2 9L8.91 8.26L12 2z" strokeWidth="2"/>
          </svg>
        );
      
      case 'heart':
        return (
          <svg className={`icon ${sizeClass} ${colorClass} ${className}`} viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z" strokeWidth="2"/>
          </svg>
        );
      
      case 'plus':
        return (
          <svg className={`icon ${sizeClass} ${colorClass} ${className}`} viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <line x1="12" y1="5" x2="12" y2="19" strokeWidth="2"/>
            <line x1="5" y1="12" x2="19" y2="12" strokeWidth="2"/>
          </svg>
        );
      
      case 'minus':
        return (
          <svg className={`icon ${sizeClass} ${colorClass} ${className}`} viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <line x1="5" y1="12" x2="19" y2="12" strokeWidth="2"/>
          </svg>
        );
      
      case 'check':
        return (
          <svg className={`icon ${sizeClass} ${colorClass} ${className}`} viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <polyline points="20,6 9,17 4,12" strokeWidth="2"/>
          </svg>
        );
      
      case 'x':
        return (
          <svg className={`icon ${sizeClass} ${colorClass} ${className}`} viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <line x1="18" y1="6" x2="6" y2="18" strokeWidth="2"/>
            <line x1="6" y1="6" x2="18" y2="18" strokeWidth="2"/>
          </svg>
        );
      
      case 'arrow-up':
        return (
          <svg className={`icon ${sizeClass} ${colorClass} ${className}`} viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <line x1="12" y1="19" x2="12" y2="5" strokeWidth="2"/>
            <polyline points="5,12 12,5 19,12" strokeWidth="2"/>
          </svg>
        );
      
      case 'arrow-down':
        return (
          <svg className={`icon ${sizeClass} ${colorClass} ${className}`} viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <line x1="12" y1="5" x2="12" y2="19" strokeWidth="2"/>
            <polyline points="19,12 12,19 5,12" strokeWidth="2"/>
          </svg>
        );
      
      case 'arrow-left':
        return (
          <svg className={`icon ${sizeClass} ${colorClass} ${className}`} viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <line x1="19" y1="12" x2="5" y2="12" strokeWidth="2"/>
            <polyline points="12,19 5,12 12,5" strokeWidth="2"/>
          </svg>
        );
      
      case 'arrow-right':
        return (
          <svg className={`icon ${sizeClass} ${colorClass} ${className}`} viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <line x1="5" y1="12" x2="19" y2="12" strokeWidth="2"/>
            <polyline points="12,5 19,12 12,19" strokeWidth="2"/>
          </svg>
        );
      
      case 'dot':
        return (
          <svg className={`icon ${sizeClass} ${colorClass} ${className}`} viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <circle cx="12" cy="12" r="4" fill="currentColor"/>
          </svg>
        );
      
      case 'line':
        return (
          <svg className={`icon ${sizeClass} ${colorClass} ${className}`} viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <line x1="3" y1="12" x2="21" y2="12" strokeWidth="2"/>
          </svg>
        );
      
      case 'grid':
        return (
          <svg className={`icon ${sizeClass} ${colorClass} ${className}`} viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <rect x="3" y="3" width="7" height="7" strokeWidth="2"/>
            <rect x="14" y="3" width="7" height="7" strokeWidth="2"/>
            <rect x="3" y="14" width="7" height="7" strokeWidth="2"/>
            <rect x="14" y="14" width="7" height="7" strokeWidth="2"/>
          </svg>
        );
      
      case 'list':
        return (
          <svg className={`icon ${sizeClass} ${colorClass} ${className}`} viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <line x1="8" y1="6" x2="21" y2="6" strokeWidth="2"/>
            <line x1="8" y1="12" x2="21" y2="12" strokeWidth="2"/>
            <line x1="8" y1="18" x2="21" y2="18" strokeWidth="2"/>
            <line x1="3" y1="6" x2="3.01" y2="6" strokeWidth="2"/>
            <line x1="3" y1="12" x2="3.01" y2="12" strokeWidth="2"/>
            <line x1="3" y1="18" x2="3.01" y2="18" strokeWidth="2"/>
          </svg>
        );
      
      case 'menu':
        return (
          <svg className={`icon ${sizeClass} ${colorClass} ${className}`} viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <line x1="3" y1="6" x2="21" y2="6" strokeWidth="2"/>
            <line x1="3" y1="12" x2="21" y2="12" strokeWidth="2"/>
            <line x1="3" y1="18" x2="21" y2="18" strokeWidth="2"/>
          </svg>
        );
      
      case 'search':
        return (
          <svg className={`icon ${sizeClass} ${colorClass} ${className}`} viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <circle cx="11" cy="11" r="8" strokeWidth="2"/>
            <path d="M21 21L16.65 16.65" strokeWidth="2"/>
          </svg>
        );
      
      case 'settings':
        return (
          <svg className={`icon ${sizeClass} ${colorClass} ${className}`} viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <circle cx="12" cy="12" r="3" strokeWidth="2"/>
            <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1 1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z" strokeWidth="2"/>
          </svg>
        );
      
      case 'user':
        return (
          <svg className={`icon ${sizeClass} ${colorClass} ${className}`} viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2" strokeWidth="2"/>
            <circle cx="12" cy="7" r="4" strokeWidth="2"/>
          </svg>
        );
      
      case 'home':
        return (
          <svg className={`icon ${sizeClass} ${colorClass} ${className}`} viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z" strokeWidth="2"/>
            <polyline points="9,22 9,12 15,12 15,22" strokeWidth="2"/>
          </svg>
        );
      
      case 'mail':
        return (
          <svg className={`icon ${sizeClass} ${colorClass} ${className}`} viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z" strokeWidth="2"/>
            <polyline points="22,6 12,13 2,6" strokeWidth="2"/>
          </svg>
        );
      
      case 'phone':
        return (
          <svg className={`icon ${sizeClass} ${colorClass} ${className}`} viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z" strokeWidth="2"/>
          </svg>
        );
      
      case 'calendar':
        return (
          <svg className={`icon ${sizeClass} ${colorClass} ${className}`} viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <rect x="3" y="4" width="18" height="18" rx="2" strokeWidth="2"/>
            <line x1="16" y1="2" x2="16" y2="6" strokeWidth="2"/>
            <line x1="8" y1="2" x2="8" y2="6" strokeWidth="2"/>
            <line x1="3" y1="10" x2="21" y2="10" strokeWidth="2"/>
          </svg>
        );
      
      case 'clock':
        return (
          <svg className={`icon ${sizeClass} ${colorClass} ${className}`} viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <circle cx="12" cy="12" r="10" strokeWidth="2"/>
            <polyline points="12,6 12,12 16,14" strokeWidth="2"/>
          </svg>
        );
      
      case 'book':
        return (
          <svg className={`icon ${sizeClass} ${colorClass} ${className}`} viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20" strokeWidth="2"/>
            <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z" strokeWidth="2"/>
          </svg>
        );
      
      case 'file':
        return (
          <svg className={`icon ${sizeClass} ${colorClass} ${className}`} viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" strokeWidth="2"/>
            <polyline points="14,2 14,8 20,8" strokeWidth="2"/>
            <line x1="16" y1="13" x2="8" y2="13" strokeWidth="2"/>
            <line x1="16" y1="17" x2="8" y2="17" strokeWidth="2"/>
            <polyline points="10,9 9,9 8,9" strokeWidth="2"/>
          </svg>
        );
      
      case 'folder':
        return (
          <svg className={`icon ${sizeClass} ${colorClass} ${className}`} viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z" strokeWidth="2"/>
          </svg>
        );
      
      case 'download':
        return (
          <svg className={`icon ${sizeClass} ${colorClass} ${className}`} viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" strokeWidth="2"/>
            <polyline points="7,10 12,15 17,10" strokeWidth="2"/>
            <line x1="12" y1="15" x2="12" y2="3" strokeWidth="2"/>
          </svg>
        );
      
      case 'upload':
        return (
          <svg className={`icon ${sizeClass} ${colorClass} ${className}`} viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" strokeWidth="2"/>
            <polyline points="17,8 12,3 7,8" strokeWidth="2"/>
            <line x1="12" y1="3" x2="12" y2="15" strokeWidth="2"/>
          </svg>
        );
      
      case 'lock':
        return (
          <svg className={`icon ${sizeClass} ${colorClass} ${className}`} viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <rect x="3" y="11" width="18" height="11" rx="2" strokeWidth="2"/>
            <circle cx="12" cy="16" r="1" strokeWidth="2"/>
            <path d="M7 11V7a5 5 0 0 1 10 0v4" strokeWidth="2"/>
          </svg>
        );
      
      case 'unlock':
        return (
          <svg className={`icon ${sizeClass} ${colorClass} ${className}`} viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <rect x="3" y="11" width="18" height="11" rx="2" strokeWidth="2"/>
            <circle cx="12" cy="16" r="1" strokeWidth="2"/>
            <path d="M7 11V7a5 5 0 0 1 9.9-.8" strokeWidth="2"/>
          </svg>
        );
      
      case 'eye':
        return (
          <svg className={`icon ${sizeClass} ${colorClass} ${className}`} viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z" strokeWidth="2"/>
            <circle cx="12" cy="12" r="3" strokeWidth="2"/>
          </svg>
        );
      
      case 'eye-off':
        return (
          <svg className={`icon ${sizeClass} ${colorClass} ${className}`} viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24" strokeWidth="2"/>
            <line x1="1" y1="1" x2="23" y2="23" strokeWidth="2"/>
          </svg>
        );
      
      case 'bell':
        return (
          <svg className={`icon ${sizeClass} ${colorClass} ${className}`} viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9" strokeWidth="2"/>
            <path d="M13.73 21a2 2 0 0 1-3.46 0" strokeWidth="2"/>
          </svg>
        );
      
      case 'trash':
        return (
          <svg className={`icon ${sizeClass} ${colorClass} ${className}`} viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <polyline points="3,6 5,6 21,6" strokeWidth="2"/>
            <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2" strokeWidth="2"/>
          </svg>
        );
      
      case 'edit':
        return (
          <svg className={`icon ${sizeClass} ${colorClass} ${className}`} viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7" strokeWidth="2"/>
            <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z" strokeWidth="2"/>
          </svg>
        );
      
      case 'share':
        return (
          <svg className={`icon ${sizeClass} ${colorClass} ${className}`} viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <circle cx="18" cy="5" r="3" strokeWidth="2"/>
            <circle cx="6" cy="12" r="3" strokeWidth="2"/>
            <circle cx="18" cy="19" r="3" strokeWidth="2"/>
            <line x1="8.59" y1="13.51" x2="15.42" y2="17.49" strokeWidth="2"/>
            <line x1="15.41" y1="6.51" x2="8.59" y2="10.49" strokeWidth="2"/>
          </svg>
        );
      
      case 'more':
        return (
          <svg className={`icon ${sizeClass} ${colorClass} ${className}`} viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <circle cx="12" cy="12" r="1" fill="currentColor"/>
            <circle cx="19" cy="12" r="1" fill="currentColor"/>
            <circle cx="5" y="12" r="1" fill="currentColor"/>
          </svg>
        );
      
      default:
        return (
          <svg className={`icon ${sizeClass} ${colorClass} ${className}`} viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <circle cx="12" cy="12" r="10" strokeWidth="2"/>
            <line x1="12" y1="8" x2="12" y2="12" strokeWidth="2"/>
            <line x1="12" y1="16" x2="12.01" y2="16" strokeWidth="2"/>
          </svg>
        );
    }
  };
  
  return renderIcon();
};

export default SimpleIconComponent;

// Composants d'icônes spécialisés avec fond gradient
export function SimpleIconWithBackground({ 
  name, 
  backgroundType = 'primary',
  size = 'md',
  className = '' 
}: {
  name: string;
  backgroundType?: 'primary' | 'secondary' | 'success' | 'warning' | 'danger' | 'info';
  size?: 'xs' | 'sm' | 'md' | 'lg' | 'xl' | '2xl' | '3xl';
  className?: string;
}) {
  const backgroundClass = `icon-${backgroundType}`;
  
  return (
    <div className={`${backgroundClass} ${className}`}>
      <SimpleIconComponent name={name} size={size} color="white" />
    </div>
  );
}

// Composant d'icône de statut
export function SimpleStatusIcon({ 
  status,
  className = '' 
}: {
  status: 'online' | 'offline' | 'busy' | 'away';
  className?: string;
}) {
  return (
    <div className={`icon-status icon-status-${status} ${className}`}></div>
  );
}

// Composant d'icône de carte
export function SimpleCardIcon({ 
  name, 
  cardType = 'primary',
  size = 'lg',
  className = '' 
}: {
  name: string;
  cardType?: 'primary' | 'secondary' | 'success' | 'warning' | 'danger' | 'info';
  size?: 'xs' | 'sm' | 'md' | 'lg' | 'xl' | '2xl' | '3xl';
  className?: string;
}) {
  const cardClass = `icon-card icon-card-${cardType}`;
  
  return (
    <div className={`${cardClass} ${className}`}>
      <SimpleIconComponent name={name} size={size} color="white" />
    </div>
  );
}

