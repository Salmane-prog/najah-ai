"use client";
import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { useAuth, UserRole  } from '../../hooks/useAuth';
import { Card } from '../../components/Card';
import Button from '../../components/Button';
import Logo from '../../components/Logo';
import { User, Mail, Lock, Home } from 'lucide-react';

export default function RegisterPage() {
  const router = useRouter();
  const { register, error, clearError, isLoading } = useAuth();
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    confirmPassword: '',
    name: '',
    role: 'student' as UserRole,
  });
  const [validationErrors, setValidationErrors] = useState<Record<string, string>>({});

  const validateForm = () => {
    const errors: Record<string, string> = {};
    if (!formData.email) {
      errors.email = 'L\'email est requis';
    } else if (!/\S+@\S+\.\S+/.test(formData.email)) {
      errors.email = 'Format d\'email invalide';
    }
    if (!formData.password) {
      errors.password = 'Le mot de passe est requis';
    } else if (formData.password.length < 6) {
      errors.password = 'Le mot de passe doit contenir au moins 6 caractères';
    }
    if (formData.password !== formData.confirmPassword) {
      errors.confirmPassword = 'Les mots de passe ne correspondent pas';
    }
    if (!formData.name.trim()) {
      errors.name = 'Le nom est requis';
    }
    setValidationErrors(errors);
    return Object.keys(errors).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    clearError();
    if (!validateForm()) return;
    try {
      await register({
        email: formData.email,
        password: formData.password,
        name: formData.name,
        role: formData.role,
      });
      router.push('/login?message=Inscription réussie ! Vous pouvez maintenant vous connecter.');
    } catch (error) {
      // handled by context
    }
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
    if (validationErrors[name]) {
      setValidationErrors(prev => ({ ...prev, [name]: '' }));
    }
  };

  const roles = [
    { value: 'student', label: 'Élève', description: 'Accès aux QCM et suivi de progression' },
    { value: 'teacher', label: 'Enseignant', description: 'Création et gestion de QCM' },
    { value: 'parent', label: 'Parent', description: 'Suivi des progrès de vos enfants' },
    { value: 'admin', label: 'Administrateur', description: 'Gestion complète de la plateforme' },
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center p-4">
      <div className="max-w-md w-full space-y-8">
        <div className="bg-white rounded-2xl shadow-xl p-8 animate-fade-in-up">
          {/* Header */}
          <div className="text-center mb-8">
            <Logo size={56} />
            <h1 className="text-3xl font-bold text-gray-900 mb-2 mt-4">Créer un compte</h1>
            <p className="text-gray-600">Rejoignez notre plateforme d&apos;apprentissage adaptatif</p>
          </div>
          {/* Formulaire */}
          <form onSubmit={handleSubmit} className="space-y-6">
            {/* Nom */}
            <div>
              <label htmlFor="name" className="block text-sm font-medium text-gray-700 mb-2">Nom complet</label>
              <div className="relative">
                <User className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" size={20} />
                <input
                  id="name"
                  name="name"
                  type="text"
                  required
                  value={formData.name}
                  onChange={handleInputChange}
                  className={`w-full pl-10 pr-4 py-3 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-colors ${validationErrors.name ? 'border-red-500' : 'border-gray-300'}`}
                  placeholder="Votre nom complet"
                />
              </div>
              {validationErrors.name && (
                <p className="mt-1 text-sm text-red-600">{validationErrors.name}</p>
              )}
            </div>
            {/* Email */}
            <div>
              <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-2">Adresse email</label>
              <div className="relative">
                <Mail className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" size={20} />
                <input
                  id="email"
                  name="email"
                  type="email"
                  required
                  value={formData.email}
                  onChange={handleInputChange}
                  className={`w-full pl-10 pr-4 py-3 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-colors ${validationErrors.email ? 'border-red-500' : 'border-gray-300'}`}
                  placeholder="votre@email.com"
                />
              </div>
              {validationErrors.email && (
                <p className="mt-1 text-sm text-red-600">{validationErrors.email}</p>
              )}
            </div>
            {/* Rôle */}
            <div>
              <label htmlFor="role" className="block text-sm font-medium text-gray-700 mb-2">Type de compte</label>
              <select
                id="role"
                name="role"
                value={formData.role}
                onChange={handleInputChange}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-colors"
              >
                {roles.map((role) => (
                  <option key={role.value} value={role.value}>{role.label}</option>
                ))}
              </select>
              <p className="mt-1 text-xs text-gray-500">{roles.find(r => r.value === formData.role)?.description}</p>
            </div>
            {/* Mot de passe */}
            <div>
              <label htmlFor="password" className="block text-sm font-medium text-gray-700 mb-2">Mot de passe</label>
              <div className="relative">
                <Lock className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" size={20} />
                <input
                  id="password"
                  name="password"
                  type="password"
                  required
                  value={formData.password}
                  onChange={handleInputChange}
                  className={`w-full pl-10 pr-4 py-3 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-colors ${validationErrors.password ? 'border-red-500' : 'border-gray-300'}`}
                  placeholder="Au moins 6 caractères"
                />
              </div>
              {validationErrors.password && (
                <p className="mt-1 text-sm text-red-600">{validationErrors.password}</p>
              )}
            </div>
            {/* Confirmation du mot de passe */}
            <div>
              <label htmlFor="confirmPassword" className="block text-sm font-medium text-gray-700 mb-2">Confirmer le mot de passe</label>
              <input
                id="confirmPassword"
                name="confirmPassword"
                type="password"
                required
                value={formData.confirmPassword}
                onChange={handleInputChange}
                className={`w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-colors ${validationErrors.confirmPassword ? 'border-red-500' : 'border-gray-300'}`}
                placeholder="Répétez votre mot de passe"
              />
              {validationErrors.confirmPassword && (
                <p className="mt-1 text-sm text-red-600">{validationErrors.confirmPassword}</p>
              )}
            </div>
            {/* Erreur globale */}
            {error && (
              <div className="bg-red-50 border border-red-200 rounded-lg p-4">
                <p className="text-sm text-red-600">{error}</p>
              </div>
            )}
            {/* Bouton d'inscription */}
            <Button
              type="submit"
              variant="primary"
              loading={isLoading}
              fullWidth
              className="mt-2"
            >
              {isLoading ? (
                <div className="flex items-center justify-center">
                  <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
                  Création du compte...
                </div>
              ) : (
                'Créer mon compte'
              )}
            </Button>
          </form>
          {/* Lien vers la connexion */}
          <div className="mt-6 text-center">
            <p className="text-sm text-gray-600">
              Déjà un compte ?{' '}
              <Link 
                href="/login" 
                className="font-medium text-blue-600 hover:text-blue-500 transition-colors"
              >
                Se connecter
              </Link>
            </p>
          </div>
        </div>
        {/* Footer */}
        <div className="text-center text-sm text-gray-500">
          <p>En créant un compte, vous acceptez nos conditions d&apos;utilisation</p>
        </div>
      </div>
    </div>
  );
} 