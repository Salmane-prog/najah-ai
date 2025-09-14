'use client';

import React, { useState, useEffect } from 'react';
import Sidebar from '../../../../components/Sidebar';
import { useAuth  } from '../../../../hooks/useAuth';
import NotificationBell from '../../../../components/NotificationBell';
import { 
  fetchUserSettings, 
  updateUserSettings,
  fetchPrivacySettings,
  updatePrivacySettings,
  fetchNotificationSettings,
  updateNotificationSettings,
  fetchUserGoals,
  updateUserGoals
} from '../../../../api/student/settings';
import { Settings, Bell, Shield, Target, Palette, Globe, Save, Check } from 'lucide-react';

export default function SettingsPage() {
  const { user, token } = useAuth();
  const userId = user?.id;
  
  const [settings, setSettings] = useState<any>(null);
  const [privacy, setPrivacy] = useState<any>(null);
  const [notifications, setNotifications] = useState<any>(null);
  const [goals, setGoals] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [saved, setSaved] = useState(false);

  useEffect(() => {
    if (!userId) return;
    
    const loadSettings = async () => {
      try {
        const [settingsRes, privacyRes, notificationsRes, goalsRes] = await Promise.all([
          fetchUserSettings(userId),
          fetchPrivacySettings(userId),
          fetchNotificationSettings(userId),
          fetchUserGoals(userId)
        ]);

        setSettings(settingsRes);
        setPrivacy(privacyRes);
        setNotifications(notificationsRes);
        setGoals(goalsRes);
        setLoading(false);
      } catch (error) {
        console.error('Erreur lors du chargement des réglages:', error);
        setLoading(false);
      }
    };

    loadSettings();
  }, [userId]);

  const handleSave = async () => {
    if (!userId) return;
    
    setSaving(true);
    try {
      await Promise.all([
        updateUserSettings(userId, settings),
        updatePrivacySettings(userId, privacy),
        updateNotificationSettings(userId, notifications),
        updateUserGoals(userId, goals)
      ]);
      
      setSaved(true);
      setTimeout(() => setSaved(false), 2000);
    } catch (error) {
      console.error('Erreur lors de la sauvegarde:', error);
    } finally {
      setSaving(false);
    }
  };

  if (!userId) {
    return (
      <div className="flex min-h-screen bg-gray-50">
        <Sidebar />
        <div className="flex-1 flex items-center justify-center">
          <div className="text-red-600 text-lg font-bold">Erreur : utilisateur non connecté.</div>
        </div>
      </div>
    );
  }

  if (loading) {
    return (
      <div className="flex min-h-screen bg-gray-50">
        <Sidebar />
        <div className="flex-1 flex items-center justify-center">
          <div className="text-blue-600 animate-pulse text-xl font-bold">Chargement des réglages...</div>
        </div>
      </div>
    );
  }

  return (
    <div className="flex min-h-screen bg-gray-50">
      <Sidebar />
      <div className="flex-1 overflow-auto pl-0 md:pl-56">
        <div className="p-6">
          {/* Header */}
          <div className="mb-8 flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-gray-800 mb-2 flex items-center gap-3">
                <Settings className="text-blue-600" />
                Réglages
              </h1>
              <p className="text-gray-600">Personnalisez votre expérience d'apprentissage</p>
            </div>
            <div className="flex items-center gap-4">
              <NotificationBell />
              <button
                onClick={handleSave}
                disabled={saving}
                className={`flex items-center gap-2 px-4 py-2 rounded-lg font-medium transition-colors ${
                  saving 
                    ? 'bg-gray-300 text-gray-500 cursor-not-allowed' 
                    : saved
                    ? 'bg-green-500 text-white hover:bg-green-600'
                    : 'bg-blue-600 text-white hover:bg-blue-700'
                }`}
              >
                {saving ? (
                  <>
                    <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                    Sauvegarde...
                  </>
                ) : saved ? (
                  <>
                    <Check className="w-4 h-4" />
                    Sauvegardé !
                  </>
                ) : (
                  <>
                    <Save className="w-4 h-4" />
                    Sauvegarder
                  </>
                )}
              </button>
            </div>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            {/* Apparence */}
            <div className="bg-white rounded-lg shadow-sm p-6">
              <div className="flex items-center gap-2 mb-6">
                <Palette className="text-purple-500" size={24} />
                <h2 className="text-xl font-bold text-gray-800">Apparence</h2>
              </div>
              
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Thème
                  </label>
                  <select
                    value={settings?.theme || 'light'}
                    onChange={(e) => setSettings({...settings, theme: e.target.value})}
                    className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  >
                    <option value="light">Clair</option>
                    <option value="dark">Sombre</option>
                    <option value="auto">Automatique</option>
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Langue
                  </label>
                  <select
                    value={settings?.language || 'fr'}
                    onChange={(e) => setSettings({...settings, language: e.target.value})}
                    className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  >
                    <option value="fr">Français</option>
                    <option value="en">English</option>
                    <option value="es">Español</option>
                  </select>
                </div>
              </div>
            </div>

            {/* Notifications */}
            <div className="bg-white rounded-lg shadow-sm p-6">
              <div className="flex items-center gap-2 mb-6">
                <Bell className="text-yellow-500" size={24} />
                <h2 className="text-xl font-bold text-gray-800">Notifications</h2>
              </div>
              
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <div>
                    <label className="text-sm font-medium text-gray-700">Notifications générales</label>
                    <p className="text-xs text-gray-500">Recevoir des notifications importantes</p>
                  </div>
                  <label className="relative inline-flex items-center cursor-pointer">
                    <input
                      type="checkbox"
                      checked={notifications?.notifications_enabled || false}
                      onChange={(e) => setNotifications({...notifications, notifications_enabled: e.target.checked})}
                      className="sr-only peer"
                    />
                    <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
                  </label>
                </div>

                <div className="flex items-center justify-between">
                  <div>
                    <label className="text-sm font-medium text-gray-700">Notifications par email</label>
                    <p className="text-xs text-gray-500">Recevoir des emails de rappel</p>
                  </div>
                  <label className="relative inline-flex items-center cursor-pointer">
                    <input
                      type="checkbox"
                      checked={notifications?.email_notifications || false}
                      onChange={(e) => setNotifications({...notifications, email_notifications: e.target.checked})}
                      className="sr-only peer"
                    />
                    <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
                  </label>
                </div>

                <div className="flex items-center justify-between">
                  <div>
                    <label className="text-sm font-medium text-gray-700">Rappels d'étude</label>
                    <p className="text-xs text-gray-500">Rappels pour étudier régulièrement</p>
                  </div>
                  <label className="relative inline-flex items-center cursor-pointer">
                    <input
                      type="checkbox"
                      checked={notifications?.study_reminders || false}
                      onChange={(e) => setNotifications({...notifications, study_reminders: e.target.checked})}
                      className="sr-only peer"
                    />
                    <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
                  </label>
                </div>
              </div>
            </div>

            {/* Confidentialité */}
            <div className="bg-white rounded-lg shadow-sm p-6">
              <div className="flex items-center gap-2 mb-6">
                <Shield className="text-green-500" size={24} />
                <h2 className="text-xl font-bold text-gray-800">Confidentialité</h2>
              </div>
              
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Niveau de confidentialité
                  </label>
                  <select
                    value={privacy?.privacy_level || 'public'}
                    onChange={(e) => setPrivacy({...privacy, privacy_level: e.target.value})}
                    className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  >
                    <option value="public">Public</option>
                    <option value="friends">Amis uniquement</option>
                    <option value="private">Privé</option>
                  </select>
                </div>

                <div className="flex items-center justify-between">
                  <div>
                    <label className="text-sm font-medium text-gray-700">Afficher ma progression</label>
                    <p className="text-xs text-gray-500">Permettre aux autres de voir vos progrès</p>
                  </div>
                  <label className="relative inline-flex items-center cursor-pointer">
                    <input
                      type="checkbox"
                      checked={privacy?.show_progress || false}
                      onChange={(e) => setPrivacy({...privacy, show_progress: e.target.checked})}
                      className="sr-only peer"
                    />
                    <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
                  </label>
                </div>

                <div className="flex items-center justify-between">
                  <div>
                    <label className="text-sm font-medium text-gray-700">Afficher dans le classement</label>
                    <p className="text-xs text-gray-500">Apparaître dans les classements</p>
                  </div>
                  <label className="relative inline-flex items-center cursor-pointer">
                    <input
                      type="checkbox"
                      checked={privacy?.show_leaderboard || false}
                      onChange={(e) => setPrivacy({...privacy, show_leaderboard: e.target.checked})}
                      className="sr-only peer"
                    />
                    <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
                  </label>
                </div>
              </div>
            </div>

            {/* Objectifs */}
            <div className="bg-white rounded-lg shadow-sm p-6">
              <div className="flex items-center gap-2 mb-6">
                <Target className="text-red-500" size={24} />
                <h2 className="text-xl font-bold text-gray-800">Objectifs</h2>
              </div>
              
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Objectif quotidien (quiz)
                  </label>
                  <input
                    type="number"
                    value={goals?.daily_goal || 3}
                    onChange={(e) => setGoals({...goals, daily_goal: parseInt(e.target.value)})}
                    className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    min="1"
                    max="20"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Objectif hebdomadaire (quiz)
                  </label>
                  <input
                    type="number"
                    value={goals?.weekly_goal || 15}
                    onChange={(e) => setGoals({...goals, weekly_goal: parseInt(e.target.value)})}
                    className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    min="5"
                    max="100"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Préférence de difficulté
                  </label>
                  <select
                    value={goals?.difficulty_preference || 'medium'}
                    onChange={(e) => setGoals({...goals, difficulty_preference: e.target.value})}
                    className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  >
                    <option value="easy">Facile</option>
                    <option value="medium">Moyen</option>
                    <option value="hard">Difficile</option>
                    <option value="mixed">Mixte</option>
                  </select>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
} 