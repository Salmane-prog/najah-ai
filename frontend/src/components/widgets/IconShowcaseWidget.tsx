'use client';

import React from 'react';
import UnifiedIcon, { IconWithBackground, StatusIcon, CardIcon } from '../ui/UnifiedIcon';

export default function IconShowcaseWidget({ className = '' }: { className?: string }) {
  return (
    <div className={`card-unified ${className}`}>
      <div className="card-unified-header">
        <h2 className="text-xl font-bold text-primary mb-0">Système d'icônes unifié</h2>
      </div>
      <div className="card-unified-body">
        <div className="space-y-6">
          {/* Icônes de base */}
          <div>
            <h3 className="text-lg font-semibold text-secondary mb-3">Icônes de base (style outline)</h3>
            <div className="grid grid-cols-4 gap-4">
              <div className="text-center">
                <UnifiedIcon name="checkCircle" size="lg" color="success" />
                <p className="text-sm text-muted mt-2">checkCircle</p>
              </div>
              <div className="text-center">
                <UnifiedIcon name="trendingUp" size="lg" color="primary" />
                <p className="text-sm text-muted mt-2">trendingUp</p>
              </div>
              <div className="text-center">
                <UnifiedIcon name="star" size="lg" color="warning" />
                <p className="text-sm text-muted mt-2">star</p>
              </div>
              <div className="text-center">
                <UnifiedIcon name="award" size="lg" color="secondary" />
                <p className="text-sm text-muted mt-2">award</p>
              </div>
            </div>
          </div>

          {/* Icônes avec fond gradient */}
          <div>
            <h3 className="text-lg font-semibold text-secondary mb-3">Icônes avec fond gradient</h3>
            <div className="grid grid-cols-4 gap-4">
              <div className="text-center">
                <IconWithBackground name="bookOpen" backgroundType="primary" size="lg" />
                <p className="text-sm text-muted mt-2">bookOpen</p>
              </div>
              <div className="text-center">
                <IconWithBackground name="calendar" backgroundType="secondary" size="lg" />
                <p className="text-sm text-muted mt-2">calendar</p>
              </div>
              <div className="text-center">
                <IconWithBackground name="fileText" backgroundType="info" size="lg" />
                <p className="text-sm text-muted mt-2">fileText</p>
              </div>
              <div className="text-center">
                <IconWithBackground name="checkSquare" backgroundType="success" size="lg" />
                <p className="text-sm text-muted mt-2">checkSquare</p>
              </div>
            </div>
          </div>

          {/* Icônes de statut */}
          <div>
            <h3 className="text-lg font-semibold text-secondary mb-3">Icônes de statut</h3>
            <div className="grid grid-cols-4 gap-4">
              <div className="text-center">
                <StatusIcon status="online" />
                <p className="text-sm text-muted mt-2">Online</p>
              </div>
              <div className="text-center">
                <StatusIcon status="offline" />
                <p className="text-sm text-muted mt-2">Offline</p>
              </div>
              <div className="text-center">
                <StatusIcon status="busy" />
                <p className="text-sm text-muted mt-2">Busy</p>
              </div>
              <div className="text-center">
                <StatusIcon status="away" />
                <p className="text-sm text-muted mt-2">Away</p>
              </div>
            </div>
          </div>

          {/* Icônes de carte */}
          <div>
            <h3 className="text-lg font-semibold text-secondary mb-3">Icônes de carte</h3>
            <div className="grid grid-cols-3 gap-4">
              <div className="text-center">
                <CardIcon name="trophy" cardType="warning" size="lg" />
                <p className="text-sm text-muted mt-2">Trophy</p>
              </div>
              <div className="text-center">
                <CardIcon name="target" cardType="info" size="lg" />
                <p className="text-sm text-muted mt-2">Target</p>
              </div>
              <div className="text-center">
                <CardIcon name="activity" cardType="success" size="lg" />
                <p className="text-sm text-muted mt-2">Activity</p>
              </div>
            </div>
          </div>

          {/* Tailles d'icônes */}
          <div>
            <h3 className="text-lg font-semibold text-secondary mb-3">Tailles d'icônes</h3>
            <div className="flex items-center justify-center space-x-4">
              <div className="text-center">
                <UnifiedIcon name="star" size="xs" color="warning" />
                <p className="text-xs text-muted mt-1">xs</p>
              </div>
              <div className="text-center">
                <UnifiedIcon name="star" size="sm" color="warning" />
                <p className="text-xs text-muted mt-1">sm</p>
              </div>
              <div className="text-center">
                <UnifiedIcon name="star" size="md" color="warning" />
                <p className="text-xs text-muted mt-1">md</p>
              </div>
              <div className="text-center">
                <UnifiedIcon name="star" size="lg" color="warning" />
                <p className="text-xs text-muted mt-1">lg</p>
              </div>
              <div className="text-center">
                <UnifiedIcon name="star" size="xl" color="warning" />
                <p className="text-xs text-muted mt-1">xl</p>
              </div>
            </div>
          </div>

          {/* Couleurs d'icônes */}
          <div>
            <h3 className="text-lg font-semibold text-secondary mb-3">Couleurs d'icônes</h3>
            <div className="grid grid-cols-4 gap-4">
              <div className="text-center">
                <UnifiedIcon name="checkCircle" size="lg" color="primary" />
                <p className="text-sm text-muted mt-2">Primary</p>
              </div>
              <div className="text-center">
                <UnifiedIcon name="checkCircle" size="lg" color="secondary" />
                <p className="text-sm text-muted mt-2">Secondary</p>
              </div>
              <div className="text-center">
                <UnifiedIcon name="checkCircle" size="lg" color="success" />
                <p className="text-sm text-muted mt-2">Success</p>
              </div>
              <div className="text-center">
                <UnifiedIcon name="checkCircle" size="lg" color="warning" />
                <p className="text-sm text-muted mt-2">Warning</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

