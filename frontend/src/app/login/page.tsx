"use client";
import React, { useState, useEffect, Suspense } from "react";
import { useAuth } from '../../hooks/useAuth';
import { useRouter, useSearchParams } from 'next/navigation';
import { Card } from '../../components/Card';
import Button from '../../components/Button';
import Logo from '../../components/Logo';
import Link from 'next/link';
import { BookOpen, Eye, EyeOff, Mail, Lock, Home, AlertCircle } from 'lucide-react';

function LoginPageContent() {
  const { login, isLoading, isAuthenticated, user, error, clearError } = useAuth();
  const router = useRouter();
  const searchParams = useSearchParams();
  const message = searchParams.get('message');

  const [showPassword, setShowPassword] = useState(false);
  const [credentials, setCredentials] = useState({ email: '', password: '' });
  const [localError, setLocalError] = useState<string | null>(null);

  useEffect(() => {
    if (isAuthenticated && user) {
      if (user.role === 'student') router.push('/dashboard/student');
      else if (user.role === 'teacher') router.push('/dashboard/teacher');
      else if (user.role === 'parent') router.push('/dashboard/parent');
      else if (user.role === 'admin') router.push('/dashboard/admin');
    }
  }, [isAuthenticated, user, router]);

  useEffect(() => { setLocalError(error || null); }, [error]);
  useEffect(() => { clearError(); }, []);

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setLocalError(null);
    if (!credentials.email || !credentials.password) {
      setLocalError("Veuillez remplir tous les champs.");
      return;
    }
    try {
      await login(credentials.email, credentials.password);
    } catch (e) {
      // handled by context
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50 flex items-center justify-center p-4">
      <div className="w-full max-w-md">
        {/* Logo et titre */}
        <div className="text-center mb-8">
          <Logo size={64} />
          <h1 className="text-3xl font-bold text-gray-800 mb-2 mt-4">Najah AI</h1>
          <p className="text-gray-600">Plateforme d&apos;Apprentissage Adaptatif</p>
        </div>
        <Card variant="elevated" className="p-8 animate-fade-in-up">
          <h2 className="text-2xl font-bold text-gray-800 mb-6 text-center">Connexion</h2>
          {/* Message de succès */}
          {message && (
            <div className="mb-6 p-4 bg-green-50 border border-green-200 rounded-lg">
              <div className="flex items-center gap-2">
                <AlertCircle className="text-green-600" size={20} />
                <p className="text-sm text-green-700">{message}</p>
              </div>
            </div>
          )}
          {/* Formulaire de connexion */}
          <form onSubmit={handleLogin} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Email</label>
              <div className="relative">
                <Mail className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" size={20} />
                <input
                  type="email"
                  value={credentials.email}
                  onChange={(e) => setCredentials({ ...credentials, email: e.target.value })}
                  className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200"
                  placeholder="votre@email.com"
                  required
                />
              </div>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Mot de passe</label>
              <div className="relative">
                <Lock className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" size={20} />
                <input
                  type={showPassword ? 'text' : 'password'}
                  value={credentials.password}
                  onChange={(e) => setCredentials({ ...credentials, password: e.target.value })}
                  className="w-full pl-10 pr-12 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200"
                  placeholder="••••••••"
                  required
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-600"
                  tabIndex={-1}
                >
                  {showPassword ? <EyeOff size={20} /> : <Eye size={20} />}
                </button>
              </div>
            </div>
            {localError && (
              <div className="p-3 bg-red-50 border border-red-200 rounded-lg">
                <p className="text-sm text-red-600">{localError}</p>
              </div>
            )}
            <Button
              type="submit"
              variant="primary"
              loading={isLoading}
              fullWidth
              className="mt-6"
            >
              {isLoading ? 'Connexion...' : 'Se connecter'}
            </Button>
          </form>
          {/* Informations de test */}
          <div className="mt-6 p-4 bg-blue-50 rounded-lg">
            <h4 className="font-medium text-blue-800 mb-2">Comptes de test disponibles</h4>
            <div className="text-sm text-blue-700 space-y-1">
              <p>• student@test.com (password123) - Élève</p>
              <p>• teacher@test.com (password123) - Enseignant</p>
              <p>• parent@test.com (password123) - Parent</p>
              <p>• admin@test.com (password123) - Administrateur</p>
            </div>
          </div>
          {/* Liens */}
          <div className="mt-6 space-y-3">
            <div className="text-center">
              <Link 
                href="/register" 
                className="text-sm text-blue-600 hover:text-blue-500 font-medium transition-colors"
              >
                Pas encore de compte ? S&apos;inscrire
              </Link>
            </div>
            <div className="text-center">
              <Link
                href="/"
                className="inline-flex items-center gap-2 text-sm text-gray-600 hover:text-gray-800 transition-colors"
              >
                <Home size={16} />
                Retour à l&apos;accueil
              </Link>
            </div>
          </div>
        </Card>
      </div>
    </div>
  );
}

export default function LoginPage() {
  return (
    <Suspense fallback={<div>Loading...</div>}>
      <LoginPageContent />
    </Suspense>
  );
} 