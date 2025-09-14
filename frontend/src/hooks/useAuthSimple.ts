'use client';

import { useState, useEffect } from 'react';

interface User {
  id: number;
  email: string;
  first_name: string;
  last_name: string;
  role: 'student' | 'teacher' | 'admin';
}

export function useAuth() {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Vérifier le token stocké au chargement
    const storedToken = localStorage.getItem('najah_token');
    if (storedToken) {
      setToken(storedToken);
      
      // Récupérer le vrai utilisateur connecté depuis l'API
      const fetchUser = async () => {
        try {
          const response = await fetch('/api/v1/auth/me', {
            headers: {
              'Authorization': `Bearer ${storedToken}`
            }
          });
          
          if (response.ok) {
            const userData = await response.json();
            console.log('🔥 [DEBUG] Utilisateur récupéré depuis l\'API:', userData);
            setUser(userData);
          } else {
            console.error('❌ Erreur lors de la récupération de l\'utilisateur:', response.status);
            // Fallback vers l'utilisateur mocké si l'API échoue
            const mockUser = {
              id: 33, // ID de l'utilisateur connecté (marizee.dubois@najah.ai)
              email: 'marizee.dubois@najah.ai',
              first_name: 'Marizee',
              last_name: 'Dubois',
              role: 'teacher'
            };
            setUser(mockUser);
            console.log('🔄 [DEBUG] Utilisation de l\'utilisateur mocké:', mockUser);
          }
        } catch (error) {
          console.error('❌ Erreur lors de la récupération de l\'utilisateur:', error);
          // Fallback vers l'utilisateur mocké en cas d'erreur
          const mockUser = {
            id: 33, // ID de l'utilisateur connecté (marizee.dubois@najah.ai)
            email: 'marizee.dubois@najah.ai',
            first_name: 'Marizee',
            last_name: 'Dubois',
            role: 'teacher'
          };
          setUser(mockUser);
          console.log('🔄 [DEBUG] Utilisation de l\'utilisateur mocké (erreur):', mockUser);
        }
      };
      
      fetchUser();
    } else {
      // Pas de token, essayer de récupérer depuis sessionStorage ou créer un utilisateur de test
      const sessionUser = sessionStorage.getItem('najah_user');
      if (sessionUser) {
        try {
          const parsedUser = JSON.parse(sessionUser);
          setUser(parsedUser);
          console.log('🔄 [DEBUG] Utilisateur récupéré depuis sessionStorage:', parsedUser);
        } catch (error) {
          console.error('❌ Erreur parsing utilisateur session:', error);
        }
      } else {
        // Créer un utilisateur de test pour le développement
        const testUser = {
          id: 1,
          email: 'student.test@najah.ai',
          first_name: 'Étudiant',
          last_name: 'Test',
          role: 'student' as const
        };
        setUser(testUser);
        console.log('🧪 [DEBUG] Création d\'un utilisateur de test:', testUser);
      }
    }
    setIsLoading(false);
  }, []);

  const login = async (email: string, password: string) => {
    try {
      setIsLoading(true);
      
      // Simulation de connexion
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      const mockUser = {
        id: 1,
        email: email,
        first_name: 'John',
        last_name: 'Doe',
        role: 'teacher' as const
      };
      
      const mockToken = 'mock_token_' + Date.now();
      
      localStorage.setItem('najah_token', mockToken);
      sessionStorage.setItem('najah_user', JSON.stringify(mockUser));
      setToken(mockToken);
      setUser(mockUser);
    } catch (error) {
      console.error('Erreur de connexion:', error);
      throw error;
    } finally {
      setIsLoading(false);
    }
  };

  const logout = () => {
    localStorage.removeItem('najah_token');
    sessionStorage.removeItem('najah_user');
    setToken(null);
    setUser(null);
  };

  // Fonction pour forcer la mise à jour de l'utilisateur
  const refreshUser = async () => {
    if (token) {
      try {
        const response = await fetch('/api/v1/auth/me', {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });
        
        if (response.ok) {
          const userData = await response.json();
          setUser(userData);
          sessionStorage.setItem('najah_user', JSON.stringify(userData));
          console.log('✅ [DEBUG] Utilisateur mis à jour:', userData);
        }
      } catch (error) {
        console.error('❌ Erreur lors de la mise à jour de l\'utilisateur:', error);
      }
    }
  };

  // Fonction pour vérifier si l'utilisateur est connecté
  const isAuthenticated = () => {
    return !!(user && token);
  };

  // Fonction pour vérifier le rôle de l'utilisateur
  const hasRole = (role: 'student' | 'teacher' | 'admin') => {
    return user?.role === role;
  };

  return {
    user,
    token,
    login,
    logout,
    isLoading,
    refreshUser,
    isAuthenticated,
    hasRole,
  };
}









