import React, { useState } from 'react';
import { ChevronDown, ChevronUp } from 'lucide-react';

interface ProgressiveCardProps {
  title: string;
  primaryContent: React.ReactNode;
  secondaryContent?: React.ReactNode;
  showToggle?: boolean;
  defaultExpanded?: boolean;
  className?: string;
  priority?: 1 | 2 | 3 | 4;
}

export const ProgressiveCard: React.FC<ProgressiveCardProps> = ({
  title,
  primaryContent,
  secondaryContent,
  showToggle = false,
  defaultExpanded = false,
  className = '',
  priority = 2
}) => {
  const [isExpanded, setIsExpanded] = useState(defaultExpanded);

  const priorityClasses = {
    1: 'priority-1',
    2: 'priority-2',
    3: 'priority-3',
    4: 'priority-4'
  };

  return (
    <div className={`dashboard-card ${className}`}>
      <div className="flex items-center justify-between mb-4">
        <h3 className={`${priorityClasses[priority]} font-medium`}>
          {title}
        </h3>
        
        {showToggle && secondaryContent && (
          <button
            onClick={() => setIsExpanded(!isExpanded)}
            className="toggle-button"
            aria-expanded={isExpanded}
            aria-label={isExpanded ? 'Réduire les détails' : 'Afficher plus de détails'}
          >
            {isExpanded ? (
              <>
                <span>Voir moins</span>
                <ChevronUp size={16} />
              </>
            ) : (
              <>
                <span>Voir plus</span>
                <ChevronDown size={16} />
              </>
            )}
          </button>
        )}
      </div>

      {/* Contenu principal - toujours visible */}
      <div className="primary-content">
        {primaryContent}
      </div>

      {/* Contenu secondaire - conditionnel */}
      {secondaryContent && (
        <div className={`secondary-content ${isExpanded ? 'expanded' : ''}`}>
          {secondaryContent}
        </div>
      )}
    </div>
  );
};

export default ProgressiveCard; 