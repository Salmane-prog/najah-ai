"use client";
import React, { createContext, useContext, useState, useEffect, ReactNode } from "react";
import { useRouter } from "next/navigation";

export type UserRole = "student" | "teacher" | "parent" | "admin";
export type User = {
  id: number;
  email: string;
  name: string;
  role: UserRole;
};

interface AuthContextType {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;
  login: (email: string, password: string) => Promise<void>;
  register: (data: { email: string; password: string; name: string; role: UserRole }) => Promise<void>;
  logout: () => void;
  clearError: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export { AuthContext };

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Persistance (localStorage)
  useEffect(() => {
    try {
      const stored = localStorage.getItem("najah_user");
      const storedToken = localStorage.getItem("najah_token");
      
      if (stored && storedToken && stored !== "null" && stored !== "undefined") {
        const parsed = JSON.parse(stored);
        setUser(parsed);
        setToken(storedToken);
        setIsAuthenticated(true);
        console.log('[AUTH] Restauration user:', parsed);
        
        // Vérifier si le token est toujours valide
        verifyToken(storedToken);
      }
    } catch (error) {
      console.error('[AUTH] Erreur lors de la restauration des données:', error);
      // Nettoyer les données corrompues
      localStorage.removeItem('najah_user');
      localStorage.removeItem('najah_token');
    }
  }, []);

  const verifyToken = async (token: string) => {
    try {
      const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
      const response = await fetch(`${API_BASE_URL}/api/v1/auth/me`, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });
      
      if (!response.ok) {
        // Token invalide, déconnecter l'utilisateur
        console.log('[AUTH] Token invalide, déconnexion');
        logout();
      }
    } catch (error) {
      console.log('[AUTH] Erreur de vérification du token:', error);
      logout();
    }
  };

  const login = async (email: string, password: string) => {
    setIsLoading(true);
    setError(null);
    try {
      const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
      console.log('[AUTH] Attempting login to:', `${API_BASE_URL}/api/v1/auth/login`);
      console.log('[AUTH] Login payload:', { email, password });
      
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 10000); // 10 second timeout
      
      try {
        const res = await fetch(`${API_BASE_URL}/api/v1/auth/login`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ email, password }),
          signal: controller.signal
        });
        
        clearTimeout(timeoutId);
        console.log('[AUTH] Response status:', res.status);
        console.log('[AUTH] Response headers:', Object.fromEntries(res.headers.entries()));
        
        if (!res.ok) {
          const err = await res.json();
          console.log('[AUTH] Error response:', err);
          setError(err.detail || 'Email ou mot de passe incorrect');
          setIsLoading(false);
          setIsAuthenticated(false);
          setUser(null);
          setToken(null);
          localStorage.removeItem('najah_user');
          localStorage.removeItem('najah_token');
          throw new Error(err.detail || 'Email ou mot de passe incorrect');
        }
        const data = await res.json();
        console.log('[AUTH] Success response:', data);
        // data: { access_token, token_type, role, id, name }
        const userObj = { id: data.id, email, name: data.name || '', role: data.role };
        setUser(userObj);
        setToken(data.access_token);
        setIsAuthenticated(true);
        localStorage.setItem('najah_user', JSON.stringify(userObj));
        localStorage.setItem('najah_token', data.access_token);
        setIsLoading(false);
        console.log('[AUTH] Login user:', userObj);
      } catch (fetchError: any) {
        clearTimeout(timeoutId);
        if (fetchError.name === 'AbortError') {
          throw new Error('La requête a pris trop de temps. Vérifiez votre connexion internet.');
        }
        throw fetchError;
      }
    } catch (e: any) {
      console.log('[AUTH] Login error:', e);
      console.log('[AUTH] Error type:', typeof e);
      console.log('[AUTH] Error message:', e.message);
      
      let errorMessage = 'Erreur lors de la connexion';
      if (e.name === 'AbortError') {
        errorMessage = 'La requête a pris trop de temps. Vérifiez votre connexion internet.';
      } else if (e.name === 'TypeError' && e.message.includes('Failed to fetch')) {
        errorMessage = 'Erreur de connexion au serveur. Vérifiez que le backend est en cours d\'exécution.';
      } else if (e.message) {
        errorMessage = e.message;
      }
      
      setError(errorMessage);
      setIsLoading(false);
      setIsAuthenticated(false);
      setUser(null);
      setToken(null);
      localStorage.removeItem('najah_user');
      localStorage.removeItem('najah_token');
      throw e;
    }
  };

  const register = async (data: { email: string; password: string; name: string; role: UserRole }) => {
    setIsLoading(true);
    setError(null);
    try {
      const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
      const res = await fetch(`${API_BASE_URL}/api/v1/auth/register`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          email: data.email,
          password: data.password,
          username: data.name, // le backend attend username
          role: data.role
        })
      });
      if (!res.ok) {
        const err = await res.json();
        setError(err.detail || 'Erreur lors de l\'inscription');
        setIsLoading(false);
        throw new Error(err.detail || 'Erreur lors de l\'inscription');
      }
      setIsLoading(false);
    } catch (e: any) {
      setError(e.message || 'Erreur lors de l\'inscription');
      setIsLoading(false);
      throw e;
    }
  };

  const logout = () => {
    setUser(null);
    setToken(null);
    setIsAuthenticated(false);
    localStorage.removeItem('najah_user');
    localStorage.removeItem('najah_token');
    
    // Redirection vers la page de connexion
    if (typeof window !== 'undefined') {
      window.location.href = 'http://localhost:3001/login';
    }
  };

  const clearError = () => setError(null);

  return (
    <AuthContext.Provider
      value={{ user, token, isAuthenticated, isLoading, error, login, register, logout, clearError }}
    >
      {children}
    </AuthContext.Provider>
  );
}

 