'use client';

import React from 'react';
import SimpleIcon, { SimpleIconWithBackground, SimpleStatusIcon, SimpleCardIcon } from '../ui/SimpleIcon';

export default function SimpleIconShowcaseWidget({ className = '' }: { className?: string }) {
  return (
    <div className={`card-unified ${className}`}>
      <div className="card-unified-header">
        <h2 className="text-xl font-bold text-primary mb-0">Icônes simples et épurées</h2>
      </div>
      <div className="card-unified-body">
        <div className="space-y-6">
          {/* Formes géométriques basiques */}
          <div>
            <h3 className="text-lg font-semibold text-secondary mb-3">Formes géométriques basiques</h3>
            <div className="grid grid-cols-4 gap-4">
              <div className="text-center">
                <SimpleIcon name="circle" size="lg" color="primary" />
                <p className="text-sm text-muted mt-2">Cercle</p>
              </div>
              <div className="text-center">
                <SimpleIcon name="square" size="lg" color="secondary" />
                <p className="text-sm text-muted mt-2">Carré</p>
              </div>
              <div className="text-center">
                <SimpleIcon name="triangle" size="lg" color="success" />
                <p className="text-sm text-muted mt-2">Triangle</p>
              </div>
              <div className="text-center">
                <SimpleIcon name="diamond" size="lg" color="warning" />
                <p className="text-sm text-muted mt-2">Diamant</p>
              </div>
            </div>
          </div>

          {/* Icônes avec fond gradient */}
          <div>
            <h3 className="text-lg font-semibold text-secondary mb-3">Icônes avec fond gradient</h3>
            <div className="grid grid-cols-4 gap-4">
              <div className="text-center">
                <SimpleIconWithBackground name="check" backgroundType="primary" size="lg" />
                <p className="text-sm text-muted mt-2">Coche</p>
              </div>
              <div className="text-center">
                <SimpleIconWithBackground name="star" backgroundType="warning" size="lg" />
                <p className="text-sm text-muted mt-2">Étoile</p>
              </div>
              <div className="text-center">
                <SimpleIconWithBackground name="heart" backgroundType="danger" size="lg" />
                <p className="text-sm text-muted mt-2">Cœur</p>
              </div>
              <div className="text-center">
                <SimpleIconWithBackground name="plus" backgroundType="success" size="lg" />
                <p className="text-sm text-muted mt-2">Plus</p>
              </div>
            </div>
          </div>

          {/* Icônes de statut */}
          <div>
            <h3 className="text-lg font-semibold text-secondary mb-3">Icônes de statut</h3>
            <div className="grid grid-cols-4 gap-4">
              <div className="text-center">
                <SimpleStatusIcon status="online" />
                <p className="text-sm text-muted mt-2">Online</p>
              </div>
              <div className="text-center">
                <SimpleStatusIcon status="offline" />
                <p className="text-sm text-muted mt-2">Offline</p>
              </div>
              <div className="text-center">
                <SimpleStatusIcon status="busy" />
                <p className="text-sm text-muted mt-2">Occupé</p>
              </div>
              <div className="text-center">
                <SimpleStatusIcon status="away" />
                <p className="text-sm text-muted mt-2">Absent</p>
              </div>
            </div>
          </div>

          {/* Icônes de carte */}
          <div>
            <h3 className="text-lg font-semibold text-secondary mb-3">Icônes de carte</h3>
            <div className="grid grid-cols-3 gap-4">
              <div className="text-center">
                <SimpleCardIcon name="star" cardType="warning" size="lg" />
                <p className="text-sm text-muted mt-2">Étoile</p>
              </div>
              <div className="text-center">
                <SimpleCardIcon name="grid" cardType="info" size="lg" />
                <p className="text-sm text-muted mt-2">Grille</p>
              </div>
              <div className="text-center">
                <SimpleCardIcon name="check" cardType="success" size="lg" />
                <p className="text-sm text-muted mt-2">Coche</p>
              </div>
            </div>
          </div>

          {/* Icônes utilitaires */}
          <div>
            <h3 className="text-lg font-semibold text-secondary mb-3">Icônes utilitaires</h3>
            <div className="grid grid-cols-4 gap-4">
              <div className="text-center">
                <SimpleIcon name="search" size="lg" color="info" />
                <p className="text-sm text-muted mt-2">Recherche</p>
              </div>
              <div className="text-center">
                <SimpleIcon name="settings" size="lg" color="neutral" />
                <p className="text-sm text-muted mt-2">Paramètres</p>
              </div>
              <div className="text-center">
                <SimpleIcon name="user" size="lg" color="primary" />
                <p className="text-sm text-muted mt-2">Utilisateur</p>
              </div>
              <div className="text-center">
                <SimpleIcon name="home" size="lg" color="success" />
                <p className="text-sm text-muted mt-2">Accueil</p>
              </div>
            </div>
          </div>

          {/* Icônes de navigation */}
          <div>
            <h3 className="text-lg font-semibold text-secondary mb-3">Icônes de navigation</h3>
            <div className="grid grid-cols-4 gap-4">
              <div className="text-center">
                <SimpleIcon name="arrow-up" size="lg" color="success" />
                <p className="text-sm text-muted mt-2">Haut</p>
              </div>
              <div className="text-center">
                <SimpleIcon name="arrow-down" size="lg" color="danger" />
                <p className="text-sm text-muted mt-2">Bas</p>
              </div>
              <div className="text-center">
                <SimpleIcon name="arrow-left" size="lg" color="primary" />
                <p className="text-sm text-muted mt-2">Gauche</p>
              </div>
              <div className="text-center">
                <SimpleIcon name="arrow-right" size="lg" color="secondary" />
                <p className="text-sm text-muted mt-2">Droite</p>
              </div>
            </div>
          </div>

          {/* Icônes d'action */}
          <div>
            <h3 className="text-lg font-semibold text-secondary mb-3">Icônes d'action</h3>
            <div className="grid grid-cols-4 gap-4">
              <div className="text-center">
                <SimpleIcon name="plus" size="lg" color="success" />
                <p className="text-sm text-muted mt-2">Ajouter</p>
              </div>
              <div className="text-center">
                <SimpleIcon name="minus" size="lg" color="danger" />
                <p className="text-sm text-muted mt-2">Retirer</p>
              </div>
              <div className="text-center">
                <SimpleIcon name="edit" size="lg" color="info" />
                <p className="text-sm text-muted mt-2">Modifier</p>
              </div>
              <div className="text-center">
                <SimpleIcon name="trash" size="lg" color="danger" />
                <p className="text-sm text-muted mt-2">Supprimer</p>
              </div>
            </div>
          </div>

          {/* Tailles d'icônes */}
          <div>
            <h3 className="text-lg font-semibold text-secondary mb-3">Tailles d'icônes</h3>
            <div className="flex items-center justify-center space-x-4">
              <div className="text-center">
                <SimpleIcon name="star" size="xs" color="warning" />
                <p className="text-xs text-muted mt-1">xs</p>
              </div>
              <div className="text-center">
                <SimpleIcon name="star" size="sm" color="warning" />
                <p className="text-xs text-muted mt-1">sm</p>
              </div>
              <div className="text-center">
                <SimpleIcon name="star" size="md" color="warning" />
                <p className="text-xs text-muted mt-1">md</p>
              </div>
              <div className="text-center">
                <SimpleIcon name="star" size="lg" color="warning" />
                <p className="text-xs text-muted mt-1">lg</p>
              </div>
              <div className="text-center">
                <SimpleIcon name="star" size="xl" color="warning" />
                <p className="text-xs text-muted mt-1">xl</p>
              </div>
            </div>
          </div>

          {/* Couleurs d'icônes */}
          <div>
            <h3 className="text-lg font-semibold text-secondary mb-3">Couleurs d'icônes</h3>
            <div className="grid grid-cols-4 gap-4">
              <div className="text-center">
                <SimpleIcon name="circle" size="lg" color="primary" />
                <p className="text-sm text-muted mt-2">Primary</p>
              </div>
              <div className="text-center">
                <SimpleIcon name="circle" size="lg" color="secondary" />
                <p className="text-sm text-muted mt-2">Secondary</p>
              </div>
              <div className="text-center">
                <SimpleIcon name="circle" size="lg" color="success" />
                <p className="text-sm text-muted mt-2">Success</p>
              </div>
              <div className="text-center">
                <SimpleIcon name="circle" size="lg" color="warning" />
                <p className="text-sm text-muted mt-2">Warning</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

