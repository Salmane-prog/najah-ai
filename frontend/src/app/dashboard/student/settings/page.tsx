'use client';

import React, { useState, useEffect } from 'react';
import { Card } from '@/components/Card';
import Button from '@/components/Button';
import Sidebar from '@/components/Sidebar';

interface UserProfile {
  id: number;
  first_name: string;
  last_name: string;
  email: string;
  avatar: string;
  phone?: string;
  date_of_birth?: string;
  bio?: string;
}

interface NotificationSettings {
  email_notifications: boolean;
  push_notifications: boolean;
  quiz_reminders: boolean;
  course_updates: boolean;
  achievement_alerts: boolean;
  weekly_reports: boolean;
}

interface PrivacySettings {
  profile_visibility: 'public' | 'private' | 'friends';
  show_progress: boolean;
  show_achievements: boolean;
  allow_messages: boolean;
}

const SettingsPage: React.FC = () => {
  const [activeTab, setActiveTab] = useState('profile');
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  
  const [profile, setProfile] = useState<UserProfile>({
    id: 1,
    first_name: 'Salmane',
    last_name: 'EL Hajouji',
    email: 'hajoujis47@gmail.com',
    avatar: 'S',
    phone: '+33 6 12 34 56 78',
    date_of_birth: '1995-03-15',
    bio: 'Étudiant passionné par l\'apprentissage en ligne'
  });

  const [notifications, setNotifications] = useState<NotificationSettings>({
    email_notifications: true,
    push_notifications: true,
    quiz_reminders: true,
    course_updates: true,
    achievement_alerts: true,
    weekly_reports: false
  });

  const [privacy, setPrivacy] = useState<PrivacySettings>({
    profile_visibility: 'friends',
    show_progress: true,
    show_achievements: true,
    allow_messages: true
  });

  const [currentPassword, setCurrentPassword] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');

  useEffect(() => {
    // Simuler le chargement des données
    setTimeout(() => {
      setLoading(false);
    }, 1000);
  }, []);

  const handleProfileUpdate = async () => {
    setSaving(true);
    // Simuler la sauvegarde
    await new Promise(resolve => setTimeout(resolve, 1000));
    setSaving(false);
    console.log('Profile updated:', profile);
  };

  const handleNotificationUpdate = async () => {
    setSaving(true);
    await new Promise(resolve => setTimeout(resolve, 1000));
    setSaving(false);
    console.log('Notifications updated:', notifications);
  };

  const handlePrivacyUpdate = async () => {
    setSaving(true);
    await new Promise(resolve => setTimeout(resolve, 1000));
    setSaving(false);
    console.log('Privacy updated:', privacy);
  };

  const handlePasswordChange = async () => {
    if (newPassword !== confirmPassword) {
      alert('Les mots de passe ne correspondent pas');
      return;
    }
    
    setSaving(true);
    await new Promise(resolve => setTimeout(resolve, 1000));
    setSaving(false);
    setCurrentPassword('');
    setNewPassword('');
    setConfirmPassword('');
    console.log('Password changed');
  };

  const tabs = [
    { id: 'profile', label: 'Profil', icon: '👤' },
    { id: 'notifications', label: 'Notifications', icon: '🔔' },
    { id: 'privacy', label: 'Confidentialité', icon: '🔒' },
    { id: 'security', label: 'Sécurité', icon: '🛡️' }
  ];

  if (loading) {
    return (
      <div className="flex min-h-screen bg-gray-50">
        <Sidebar />
        <div className="flex-1 flex items-center justify-center">
          <div className="text-blue-600 animate-pulse text-xl font-bold">
            Chargement des paramètres...
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="flex min-h-screen bg-gray-50">
      <Sidebar />
      <div className="flex-1 overflow-auto pl-0 md:pl-56">
        <div className="p-6">
          <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            Réglages
          </h1>
          <p className="text-gray-600">
            Gérez votre profil, vos préférences et vos paramètres de confidentialité.
          </p>
        </div>

        {/* Tabs */}
        <div className="bg-white rounded-lg shadow-sm mb-6">
          <div className="border-b border-gray-200">
            <nav className="flex space-x-8 px-6">
              {tabs.map((tab) => (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`py-4 px-1 border-b-2 font-medium text-sm ${
                    activeTab === tab.id
                      ? 'border-blue-500 text-blue-600'
                      : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                  }`}
                >
                  <span className="mr-2">{tab.icon}</span>
                  {tab.label}
                </button>
              ))}
            </nav>
          </div>
        </div>

        {/* Tab Content */}
        <div className="bg-white rounded-lg shadow-sm">
          {activeTab === 'profile' && (
            <div className="p-6">
              <h2 className="text-xl font-semibold text-gray-900 mb-6">Informations du Profil</h2>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Prénom
                  </label>
                  <input
                    type="text"
                    value={profile.first_name}
                    onChange={(e) => setProfile({ ...profile, first_name: e.target.value })}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Nom
                  </label>
                  <input
                    type="text"
                    value={profile.last_name}
                    onChange={(e) => setProfile({ ...profile, last_name: e.target.value })}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Email
                  </label>
                  <input
                    type="email"
                    value={profile.email}
                    onChange={(e) => setProfile({ ...profile, email: e.target.value })}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Téléphone
                  </label>
                  <input
                    type="tel"
                    value={profile.phone || ''}
                    onChange={(e) => setProfile({ ...profile, phone: e.target.value })}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Date de naissance
                  </label>
                  <input
                    type="date"
                    value={profile.date_of_birth || ''}
                    onChange={(e) => setProfile({ ...profile, date_of_birth: e.target.value })}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                </div>
              </div>
              
              <div className="mt-6">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Bio
                </label>
                <textarea
                  value={profile.bio || ''}
                  onChange={(e) => setProfile({ ...profile, bio: e.target.value })}
                  rows={4}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="Parlez-nous de vous..."
                />
              </div>
              
              <div className="mt-6">
                <Button
                  onClick={handleProfileUpdate}
                  disabled={saving}
                >
                  {saving ? 'Sauvegarde...' : 'Sauvegarder les modifications'}
                </Button>
              </div>
            </div>
          )}

          {activeTab === 'notifications' && (
            <div className="p-6">
              <h2 className="text-xl font-semibold text-gray-900 mb-6">Paramètres de Notifications</h2>
              
              <div className="space-y-4">
                <div className="flex items-center justify-between p-4 border rounded-lg">
                  <div>
                    <h3 className="font-medium text-gray-900">Notifications par email</h3>
                    <p className="text-sm text-gray-600">Recevoir les notifications importantes par email</p>
                  </div>
                  <label className="relative inline-flex items-center cursor-pointer">
                    <input
                      type="checkbox"
                      checked={notifications.email_notifications}
                      onChange={(e) => setNotifications({ ...notifications, email_notifications: e.target.checked })}
                      className="sr-only peer"
                    />
                    <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
                  </label>
                </div>

                <div className="flex items-center justify-between p-4 border rounded-lg">
                  <div>
                    <h3 className="font-medium text-gray-900">Notifications push</h3>
                    <p className="text-sm text-gray-600">Recevoir des notifications sur votre appareil</p>
                  </div>
                  <label className="relative inline-flex items-center cursor-pointer">
                    <input
                      type="checkbox"
                      checked={notifications.push_notifications}
                      onChange={(e) => setNotifications({ ...notifications, push_notifications: e.target.checked })}
                      className="sr-only peer"
                    />
                    <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
                  </label>
                </div>

                <div className="flex items-center justify-between p-4 border rounded-lg">
                  <div>
                    <h3 className="font-medium text-gray-900">Rappels de quiz</h3>
                    <p className="text-sm text-gray-600">Être notifié des quiz à venir</p>
                  </div>
                  <label className="relative inline-flex items-center cursor-pointer">
                    <input
                      type="checkbox"
                      checked={notifications.quiz_reminders}
                      onChange={(e) => setNotifications({ ...notifications, quiz_reminders: e.target.checked })}
                      className="sr-only peer"
                    />
                    <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
                  </label>
                </div>

                <div className="flex items-center justify-between p-4 border rounded-lg">
                  <div>
                    <h3 className="font-medium text-gray-900">Mises à jour de cours</h3>
                    <p className="text-sm text-gray-600">Être notifié des nouvelles leçons et contenus</p>
                  </div>
                  <label className="relative inline-flex items-center cursor-pointer">
                    <input
                      type="checkbox"
                      checked={notifications.course_updates}
                      onChange={(e) => setNotifications({ ...notifications, course_updates: e.target.checked })}
                      className="sr-only peer"
                    />
                    <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
                  </label>
                </div>

                <div className="flex items-center justify-between p-4 border rounded-lg">
                  <div>
                    <h3 className="font-medium text-gray-900">Alertes de réussite</h3>
                    <p className="text-sm text-gray-600">Être notifié de vos nouvelles réussites</p>
                  </div>
                  <label className="relative inline-flex items-center cursor-pointer">
                    <input
                      type="checkbox"
                      checked={notifications.achievement_alerts}
                      onChange={(e) => setNotifications({ ...notifications, achievement_alerts: e.target.checked })}
                      className="sr-only peer"
                    />
                    <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
                  </label>
                </div>

                <div className="flex items-center justify-between p-4 border rounded-lg">
                  <div>
                    <h3 className="font-medium text-gray-900">Rapports hebdomadaires</h3>
                    <p className="text-sm text-gray-600">Recevoir un résumé de votre progression</p>
                  </div>
                  <label className="relative inline-flex items-center cursor-pointer">
                    <input
                      type="checkbox"
                      checked={notifications.weekly_reports}
                      onChange={(e) => setNotifications({ ...notifications, weekly_reports: e.target.checked })}
                      className="sr-only peer"
                    />
                    <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
                  </label>
                </div>
              </div>
              
              <div className="mt-6">
                <Button
                  onClick={handleNotificationUpdate}
                  disabled={saving}
                >
                  {saving ? 'Sauvegarde...' : 'Sauvegarder les préférences'}
                </Button>
              </div>
            </div>
          )}

          {activeTab === 'privacy' && (
            <div className="p-6">
              <h2 className="text-xl font-semibold text-gray-900 mb-6">Paramètres de Confidentialité</h2>
              
              <div className="space-y-6">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Visibilité du profil
                  </label>
                  <select
                    value={privacy.profile_visibility}
                    onChange={(e) => setPrivacy({ ...privacy, profile_visibility: e.target.value as any })}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  >
                    <option value="public">Public</option>
                    <option value="friends">Amis uniquement</option>
                    <option value="private">Privé</option>
                  </select>
                </div>

                <div className="space-y-4">
                  <div className="flex items-center justify-between p-4 border rounded-lg">
                    <div>
                      <h3 className="font-medium text-gray-900">Afficher ma progression</h3>
                      <p className="text-sm text-gray-600">Permettre aux autres de voir vos statistiques</p>
                    </div>
                    <label className="relative inline-flex items-center cursor-pointer">
                      <input
                        type="checkbox"
                        checked={privacy.show_progress}
                        onChange={(e) => setPrivacy({ ...privacy, show_progress: e.target.checked })}
                        className="sr-only peer"
                      />
                      <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
                    </label>
                  </div>

                  <div className="flex items-center justify-between p-4 border rounded-lg">
                    <div>
                      <h3 className="font-medium text-gray-900">Afficher mes réussites</h3>
                      <p className="text-sm text-gray-600">Partager vos badges et accomplissements</p>
                    </div>
                    <label className="relative inline-flex items-center cursor-pointer">
                      <input
                        type="checkbox"
                        checked={privacy.show_achievements}
                        onChange={(e) => setPrivacy({ ...privacy, show_achievements: e.target.checked })}
                        className="sr-only peer"
                      />
                      <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
                    </label>
                  </div>

                  <div className="flex items-center justify-between p-4 border rounded-lg">
                    <div>
                      <h3 className="font-medium text-gray-900">Autoriser les messages</h3>
                      <p className="text-sm text-gray-600">Permettre aux autres de vous contacter</p>
                    </div>
                    <label className="relative inline-flex items-center cursor-pointer">
                      <input
                        type="checkbox"
                        checked={privacy.allow_messages}
                        onChange={(e) => setPrivacy({ ...privacy, allow_messages: e.target.checked })}
                        className="sr-only peer"
                      />
                      <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
                    </label>
                  </div>
                </div>
              </div>
              
              <div className="mt-6">
                <Button
                  onClick={handlePrivacyUpdate}
                  disabled={saving}
                >
                  {saving ? 'Sauvegarde...' : 'Sauvegarder les paramètres'}
                </Button>
              </div>
            </div>
          )}

          {activeTab === 'security' && (
            <div className="p-6">
              <h2 className="text-xl font-semibold text-gray-900 mb-6">Sécurité du Compte</h2>
              
              <div className="space-y-6">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Mot de passe actuel
                  </label>
                  <input
                    type="password"
                    value={currentPassword}
                    onChange={(e) => setCurrentPassword(e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    placeholder="Entrez votre mot de passe actuel"
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Nouveau mot de passe
                  </label>
                  <input
                    type="password"
                    value={newPassword}
                    onChange={(e) => setNewPassword(e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    placeholder="Entrez votre nouveau mot de passe"
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Confirmer le nouveau mot de passe
                  </label>
                  <input
                    type="password"
                    value={confirmPassword}
                    onChange={(e) => setConfirmPassword(e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    placeholder="Confirmez votre nouveau mot de passe"
                  />
                </div>
              </div>
              
              <div className="mt-6">
                <Button
                  onClick={handlePasswordChange}
                  disabled={saving || !currentPassword || !newPassword || !confirmPassword}
                >
                  {saving ? 'Modification...' : 'Changer le mot de passe'}
                </Button>
              </div>

              <div className="mt-8 pt-6 border-t border-gray-200">
                <h3 className="text-lg font-medium text-gray-900 mb-4">Actions Dangereuses</h3>
                <div className="space-y-4">
                  <div className="p-4 border border-red-200 rounded-lg bg-red-50">
                    <h4 className="font-medium text-red-900 mb-2">Supprimer le compte</h4>
                    <p className="text-sm text-red-700 mb-3">
                      Cette action est irréversible. Toutes vos données seront définitivement supprimées.
                    </p>
                    <Button
                      variant="outline"
                      className="border-red-300 text-red-700 hover:bg-red-100"
                    >
                      Supprimer mon compte
                    </Button>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
                </div>
        </div>
      </div>
    </div>
  );
};

export default SettingsPage; 