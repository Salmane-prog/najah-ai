'use client';

import React, { useState, useEffect } from 'react';
import Sidebar from '../../../../components/Sidebar';
import { useAuth  } from '../../../../hooks/useAuth';
import { Settings, User, Bell, Shield, Palette, Save, Edit } from 'lucide-react';

interface UserProfile {
  id: number;
  name: string;
  email: string;
  role: string;
  avatar_url?: string;
  bio?: string;
  phone?: string;
}

interface NotificationSettings {
  email_notifications: boolean;
  push_notifications: boolean;
  quiz_results: boolean;
  new_messages: boolean;
  system_updates: boolean;
}

interface SecuritySettings {
  two_factor_auth: boolean;
  session_timeout: number;
  password_changed_at: string;
}

export default function TeacherSettings() {
  const { user, token } = useAuth();
  const [activeTab, setActiveTab] = useState<'profile' | 'notifications' | 'security' | 'preferences'>('profile');
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);

  // États pour les formulaires
  const [profile, setProfile] = useState<UserProfile | null>(null);
  const [notifications, setNotifications] = useState<NotificationSettings>({
    email_notifications: true,
    push_notifications: true,
    quiz_results: true,
    new_messages: true,
    system_updates: false
  });
  const [security, setSecurity] = useState<SecuritySettings>({
    two_factor_auth: false,
    session_timeout: 30,
    password_changed_at: ''
  });

  useEffect(() => {
    if (token) {
      fetchUserProfile();
      fetchNotificationSettings();
      fetchSecuritySettings();
    }
  }, [token]);

  const fetchUserProfile = async () => {
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/v1/users/profile`, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });

      if (response.ok) {
        const data = await response.json();
        setProfile(data);
      }
    } catch (err) {
      console.error('Erreur lors du chargement du profil:', err);
    } finally {
      setLoading(false);
    }
  };

  const fetchNotificationSettings = async () => {
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/v1/settings/notifications`, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });

      if (response.ok) {
        const data = await response.json();
        setNotifications(data);
      }
    } catch (err) {
      console.error('Erreur lors du chargement des paramètres de notification:', err);
    }
  };

  const fetchSecuritySettings = async () => {
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/v1/settings/security`, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });

      if (response.ok) {
        const data = await response.json();
        setSecurity(data);
      }
    } catch (err) {
      console.error('Erreur lors du chargement des paramètres de sécurité:', err);
    }
  };

  const saveProfile = async () => {
    if (!profile) return;

    setSaving(true);
    setError(null);
    setSuccess(null);

    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/v1/users/profile`, {
        method: 'PUT',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(profile)
      });

      if (response.ok) {
        setSuccess('Profil mis à jour avec succès');
      } else {
        setError('Erreur lors de la mise à jour du profil');
      }
    } catch (err) {
      setError('Erreur de connexion');
    } finally {
      setSaving(false);
    }
  };

  const saveNotificationSettings = async () => {
    setSaving(true);
    setError(null);
    setSuccess(null);

    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/v1/settings/notifications`, {
        method: 'PUT',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(notifications)
      });

      if (response.ok) {
        setSuccess('Paramètres de notification mis à jour');
      } else {
        setError('Erreur lors de la mise à jour des notifications');
      }
    } catch (err) {
      setError('Erreur de connexion');
    } finally {
      setSaving(false);
    }
  };

  const saveSecuritySettings = async () => {
    setSaving(true);
    setError(null);
    setSuccess(null);

    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/v1/settings/security`, {
        method: 'PUT',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(security)
      });

      if (response.ok) {
        setSuccess('Paramètres de sécurité mis à jour');
      } else {
        setError('Erreur lors de la mise à jour de la sécurité');
      }
    } catch (err) {
      setError('Erreur de connexion');
    } finally {
      setSaving(false);
    }
  };

  if (loading) {
    return (
      <div className="flex min-h-screen bg-gray-50">
        <Sidebar userType="teacher" />
        <div className="flex-1 flex items-center justify-center">
          <div className="text-blue-600 animate-pulse text-xl font-bold">Chargement des réglages...</div>
        </div>
      </div>
    );
  }

  return (
    <div className="flex min-h-screen bg-gray-50">
      <Sidebar userType="teacher" />
      <div className="flex-1 overflow-auto pl-0 md:pl-56">
        <div className="p-6">
          {/* Header */}
          <div className="mb-6">
            <h1 className="text-3xl font-bold text-gray-800 mb-2">Réglages</h1>
            <p className="text-gray-600">Gérez vos préférences et paramètres</p>
          </div>

          {/* Navigation des onglets */}
          <div className="mb-6">
            <div className="flex space-x-1 bg-white rounded-lg p-1 shadow-sm">
              {[
                { id: 'profile', label: 'Profil', icon: <User size={16} /> },
                { id: 'notifications', label: 'Notifications', icon: <Bell size={16} /> },
                { id: 'security', label: 'Sécurité', icon: <Shield size={16} /> },
                { id: 'preferences', label: 'Préférences', icon: <Palette size={16} /> }
              ].map((tab) => (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id as any)}
                  className={`flex items-center gap-2 px-4 py-2 rounded-md font-medium transition ${
                    activeTab === tab.id
                      ? 'bg-blue-100 text-blue-700'
                      : 'text-gray-600 hover:text-gray-900'
                  }`}
                >
                  {tab.icon}
                  {tab.label}
                </button>
              ))}
            </div>
          </div>

          {/* Messages de succès/erreur */}
          {success && (
            <div className="mb-4 p-4 bg-green-50 border border-green-200 rounded-lg">
              <p className="text-green-800">{success}</p>
            </div>
          )}
          {error && (
            <div className="mb-4 p-4 bg-red-50 border border-red-200 rounded-lg">
              <p className="text-red-800">{error}</p>
            </div>
          )}

          {/* Contenu des onglets */}
          <div className="bg-white rounded-xl shadow-lg p-6">
            {/* Onglet Profil */}
            {activeTab === 'profile' && profile && (
              <div className="space-y-6">
                <div className="flex items-center gap-2 mb-4">
                  <User className="text-blue-600" size={20} />
                  <h2 className="text-lg font-bold text-gray-800">Informations personnelles</h2>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Nom complet</label>
                    <input
                      type="text"
                      value={profile.name || ''}
                      onChange={(e) => setProfile({ ...profile, name: e.target.value })}
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Email</label>
                    <input
                      type="email"
                      value={profile.email || ''}
                      disabled
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg bg-gray-50"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Téléphone</label>
                    <input
                      type="tel"
                      value={profile.phone || ''}
                      onChange={(e) => setProfile({ ...profile, phone: e.target.value })}
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Rôle</label>
                    <input
                      type="text"
                      value={profile.role || ''}
                      disabled
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg bg-gray-50"
                    />
                  </div>

                  <div className="md:col-span-2">
                    <label className="block text-sm font-medium text-gray-700 mb-2">Bio</label>
                    <textarea
                      value={profile.bio || ''}
                      onChange={(e) => setProfile({ ...profile, bio: e.target.value })}
                      rows={3}
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                  </div>
                </div>

                <div className="flex justify-end">
                  <button
                    onClick={saveProfile}
                    disabled={saving}
                    className="flex items-center gap-2 px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50"
                  >
                    <Save size={16} />
                    {saving ? 'Sauvegarde...' : 'Sauvegarder'}
                  </button>
                </div>
              </div>
            )}

            {/* Onglet Notifications */}
            {activeTab === 'notifications' && (
              <div className="space-y-6">
                <div className="flex items-center gap-2 mb-4">
                  <Bell className="text-blue-600" size={20} />
                  <h2 className="text-lg font-bold text-gray-800">Paramètres de notification</h2>
                </div>

                <div className="space-y-4">
                  {Object.entries(notifications).map(([key, value]) => (
                    <div key={key} className="flex items-center justify-between p-4 border border-gray-200 rounded-lg">
                      <div>
                        <h3 className="font-medium text-gray-900">
                          {key === 'email_notifications' && 'Notifications par email'}
                          {key === 'push_notifications' && 'Notifications push'}
                          {key === 'quiz_results' && 'Résultats de quiz'}
                          {key === 'new_messages' && 'Nouveaux messages'}
                          {key === 'system_updates' && 'Mises à jour système'}
                        </h3>
                        <p className="text-sm text-gray-500">
                          {key === 'email_notifications' && 'Recevoir les notifications par email'}
                          {key === 'push_notifications' && 'Recevoir les notifications push'}
                          {key === 'quiz_results' && 'Être notifié des résultats de quiz'}
                          {key === 'new_messages' && 'Être notifié des nouveaux messages'}
                          {key === 'system_updates' && 'Recevoir les mises à jour système'}
                        </p>
                      </div>
                      <label className="relative inline-flex items-center cursor-pointer">
                        <input
                          type="checkbox"
                          checked={value}
                          onChange={(e) => setNotifications({ ...notifications, [key]: e.target.checked })}
                          className="sr-only peer"
                        />
                        <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
                      </label>
                    </div>
                  ))}
                </div>

                <div className="flex justify-end">
                  <button
                    onClick={saveNotificationSettings}
                    disabled={saving}
                    className="flex items-center gap-2 px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50"
                  >
                    <Save size={16} />
                    {saving ? 'Sauvegarde...' : 'Sauvegarder'}
                  </button>
                </div>
              </div>
            )}

            {/* Onglet Sécurité */}
            {activeTab === 'security' && (
              <div className="space-y-6">
                <div className="flex items-center gap-2 mb-4">
                  <Shield className="text-blue-600" size={20} />
                  <h2 className="text-lg font-bold text-gray-800">Paramètres de sécurité</h2>
                </div>

                <div className="space-y-4">
                  <div className="flex items-center justify-between p-4 border border-gray-200 rounded-lg">
                    <div>
                      <h3 className="font-medium text-gray-900">Authentification à deux facteurs</h3>
                      <p className="text-sm text-gray-500">Ajouter une couche de sécurité supplémentaire</p>
                    </div>
                    <label className="relative inline-flex items-center cursor-pointer">
                      <input
                        type="checkbox"
                        checked={security.two_factor_auth}
                        onChange={(e) => setSecurity({ ...security, two_factor_auth: e.target.checked })}
                        className="sr-only peer"
                      />
                      <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
                    </label>
                  </div>

                  <div className="p-4 border border-gray-200 rounded-lg">
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Timeout de session (minutes)
                    </label>
                    <select
                      value={security.session_timeout}
                      onChange={(e) => setSecurity({ ...security, session_timeout: parseInt(e.target.value) })}
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    >
                      <option value={15}>15 minutes</option>
                      <option value={30}>30 minutes</option>
                      <option value={60}>1 heure</option>
                      <option value={120}>2 heures</option>
                    </select>
                  </div>

                  {security.password_changed_at && (
                    <div className="p-4 bg-gray-50 rounded-lg">
                      <p className="text-sm text-gray-600">
                        Mot de passe changé le: {new Date(security.password_changed_at).toLocaleDateString()}
                      </p>
                    </div>
                  )}
                </div>

                <div className="flex justify-end">
                  <button
                    onClick={saveSecuritySettings}
                    disabled={saving}
                    className="flex items-center gap-2 px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50"
                  >
                    <Save size={16} />
                    {saving ? 'Sauvegarde...' : 'Sauvegarder'}
                  </button>
                </div>
              </div>
            )}

            {/* Onglet Préférences */}
            {activeTab === 'preferences' && (
              <div className="space-y-6">
                <div className="flex items-center gap-2 mb-4">
                  <Palette className="text-blue-600" size={20} />
                  <h2 className="text-lg font-bold text-gray-800">Préférences</h2>
                </div>

                <div className="space-y-4">
                  <div className="p-4 border border-gray-200 rounded-lg">
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Thème de l&apos;interface
                    </label>
                    <select className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500">
                      <option value="light">Clair</option>
                      <option value="dark">Sombre</option>
                      <option value="auto">Automatique</option>
                    </select>
                  </div>

                  <div className="p-4 border border-gray-200 rounded-lg">
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Langue
                    </label>
                    <select className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500">
                      <option value="fr">Français</option>
                      <option value="en">English</option>
                      <option value="ar">العربية</option>
                    </select>
                  </div>

                  <div className="p-4 border border-gray-200 rounded-lg">
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Fuseau horaire
                    </label>
                    <select className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500">
                      <option value="Europe/Paris">Europe/Paris</option>
                      <option value="UTC">UTC</option>
                      <option value="America/New_York">America/New_York</option>
                    </select>
                  </div>
                </div>

                <div className="flex justify-end">
                  <button className="flex items-center gap-2 px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700">
                    <Save size={16} />
                    Sauvegarder
                  </button>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
} 