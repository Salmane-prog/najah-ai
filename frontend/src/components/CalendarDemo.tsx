'use client';

import React, { useState } from 'react';
import Calendar from './Calendar';
import { CalendarEvent } from '../api/student/organization';

export default function CalendarDemo() {
  const [selectedEvent, setSelectedEvent] = useState<CalendarEvent | null>(null);

  const handleEventClick = (event: CalendarEvent) => {
    setSelectedEvent(event);
    console.log('Événement sélectionné:', event);
  };

  const handleEventCreated = () => {
    console.log('Nouvel événement créé !');
    setSelectedEvent(null);
  };

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-7xl mx-auto">
        {/* En-tête */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            Calendrier d'Organisation
          </h1>
          <p className="text-lg text-gray-600">
            Gérez votre calendrier, devoirs, objectifs, sessions d'étude et rappels
          </p>
        </div>

        {/* Grille principale */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Calendrier principal */}
          <div className="lg:col-span-2">
            <Calendar
              onEventClick={handleEventClick}
              onEventCreated={handleEventCreated}
            />
          </div>

          {/* Panneau latéral */}
          <div className="space-y-6">
            {/* Informations sur l'événement sélectionné */}
            {selectedEvent && (
              <div className="bg-white rounded-lg shadow-md p-6">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">
                  Détails de l'événement
                </h3>
                <div className="space-y-3">
                  <div>
                    <span className="text-sm font-medium text-gray-500">Titre:</span>
                    <p className="text-gray-900">{selectedEvent.title}</p>
                  </div>
                  {selectedEvent.description && (
                    <div>
                      <span className="text-sm font-medium text-gray-500">Description:</span>
                      <p className="text-gray-900">{selectedEvent.description}</p>
                    </div>
                  )}
                  <div>
                    <span className="text-sm font-medium text-gray-500">Type:</span>
                    <p className="text-gray-900 capitalize">{selectedEvent.event_type}</p>
                  </div>
                  <div>
                    <span className="text-sm font-medium text-gray-500">Date de début:</span>
                    <p className="text-gray-900">
                      {new Date(selectedEvent.start_date).toLocaleString('fr-FR')}
                    </p>
                  </div>
                  {selectedEvent.end_date && (
                    <div>
                      <span className="text-sm font-medium text-gray-500">Date de fin:</span>
                      <p className="text-gray-900">
                        {new Date(selectedEvent.end_date).toLocaleString('fr-FR')}
                      </p>
                    </div>
                  )}
                  {selectedEvent.location && (
                    <div>
                      <span className="text-sm font-medium text-gray-500">Localisation:</span>
                      <p className="text-gray-900">{selectedEvent.location}</p>
                    </div>
                  )}
                </div>
              </div>
            )}

            {/* Guide d'utilisation */}
            <div className="bg-white rounded-lg shadow-md p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">
                Guide d'utilisation
              </h3>
              <div className="space-y-3 text-sm text-gray-600">
                <div className="flex items-start space-x-2">
                  <div className="w-2 h-2 bg-red-500 rounded-full mt-2 flex-shrink-0"></div>
                  <p><strong>Devoirs</strong> - Assignés par le professeur</p>
                </div>
                <div className="flex items-start space-x-2">
                  <div className="w-2 h-2 bg-blue-500 rounded-full mt-2 flex-shrink-0"></div>
                  <p><strong>Sessions d'étude</strong> - Créées par l'étudiant</p>
                </div>
                <div className="flex items-start space-x-2">
                  <div className="w-2 h-2 bg-green-500 rounded-full mt-2 flex-shrink-0"></div>
                  <p><strong>Objectifs</strong> - Créés par l'étudiant</p>
                </div>
                <div className="flex items-start space-x-2">
                  <div className="w-2 h-2 bg-yellow-500 rounded-full mt-2 flex-shrink-0"></div>
                  <p><strong>Rappels</strong> - Créés par l'étudiant</p>
                </div>
              </div>
            </div>

            {/* Actions rapides */}
            <div className="bg-white rounded-lg shadow-md p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">
                Actions rapides
              </h3>
              <div className="space-y-3">
                <button className="w-full px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors">
                  + Ajouter un devoir
                </button>
                <button className="w-full px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors">
                  + Nouvelle session
                </button>
                <button className="w-full px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors">
                  + Nouvel objectif
                </button>
                <button className="w-full px-4 py-2 bg-yellow-600 text-white rounded-lg hover:bg-yellow-700 transition-colors">
                  + Nouveau rappel
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
