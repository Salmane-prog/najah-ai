"use client";
import React, { useRef, useEffect, useState } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { LogOut, BookOpen, Home, MessageCircle, Settings, GraduationCap, User, Target, Map, Plus, PieChart, Users, BarChart3, Calendar, Zap, TrendingUp, Lightbulb, ChevronUp, ChevronDown, FileText, Database, Play } from 'lucide-react';
import Logo from './Logo';
import { useAuth  } from '../hooks/useAuth';

interface SidebarProps {
  userType?: 'student' | 'teacher' | 'admin';
}

const navItems = [
  // Navigation pour les étudiants
  { label: 'Dashboard', href: '/dashboard/student', icon: <Home size={20} />, studentOnly: true },
  { label: 'Évaluation Initiale', href: '/dashboard/student/assessment', icon: <Target size={20} />, studentOnly: true },
  { label: 'Parcours d\'Apprentissage', href: '/dashboard/student/learning-path', icon: <Map size={20} />, studentOnly: true },
  { label: 'Mes Quiz Assignés', href: '/dashboard/student/quiz-assignments', icon: <BookOpen size={20} />, studentOnly: true },
  { label: 'Analytics Avancées', href: '/dashboard/student/advanced-analytics', icon: <BarChart3 size={20} />, studentOnly: true },

  { label: 'Cours', href: '/dashboard/student/courses', icon: <BookOpen size={20} />, studentOnly: true },
  { label: 'Messages', href: '/dashboard/student/messages', icon: <MessageCircle size={20} />, studentOnly: true },
  { label: 'Forum d\'entraide', href: '/dashboard/student/forum', icon: <MessageCircle size={20} />, studentOnly: true },
  { label: 'Mes Notes', href: '/dashboard/student/notes', icon: <BookOpen size={20} />, studentOnly: true },
  { label: 'Notes Avancées', href: '/dashboard/student/notes-advanced', icon: <FileText size={20} />, studentOnly: true },
  { label: 'Organisation', href: '/dashboard/student/organization', icon: <Calendar size={20} />, studentOnly: true },
  { label: 'Bibliothèque', href: '/dashboard/student/library', icon: <BookOpen size={20} />, studentOnly: true },
  { label: 'Réglages', href: '/dashboard/student/settings', icon: <Settings size={20} />, studentOnly: true },
  
  // Navigation pour les professeurs
  { label: 'Dashboard', href: '/dashboard/teacher', icon: <Home size={20} />, teacherOnly: true },
  { label: 'Classes', href: '/dashboard/teacher/classes', icon: <Users size={20} />, teacherOnly: true },
  { label: 'Élèves', href: '/dashboard/teacher/students', icon: <User size={20} />, teacherOnly: true },
  { label: 'Contenu', href: '/dashboard/teacher/content', icon: <BookOpen size={20} />, teacherOnly: true },
              { label: 'Assignations', href: '/dashboard/teacher/assignments', icon: <Target size={20} />, teacherOnly: true },
            { label: 'Calendrier', href: '/dashboard/teacher/calendar', icon: <Calendar size={20} />, teacherOnly: true },
  { label: 'Messages', href: '/dashboard/teacher/messages', icon: <MessageCircle size={20} />, teacherOnly: true },
  { label: 'Réglages', href: '/dashboard/teacher/settings', icon: <Settings size={20} />, teacherOnly: true },
  { label: 'Générer un Quiz', href: '/dashboard/teacher/quiz', icon: <GraduationCap size={20} />, teacherOnly: true },
];

// Section IA & Analytics pour les professeurs
const aiNavItems = [
  { label: 'Évaluation Adaptative', href: '/dashboard/teacher/adaptive-evaluation', icon: <Target size={20} />, teacherOnly: true, studentOnly: false },
  { label: 'Résultats des Tests', href: '/dashboard/teacher/test-results', icon: <TrendingUp size={20} />, teacherOnly: true, studentOnly: false },
  
  { label: 'Analytics', href: '/dashboard/teacher/analytics', icon: <BarChart3 size={20} />, teacherOnly: true, studentOnly: false },
];

export default function Sidebar({ userType }: SidebarProps) {
  const pathname = usePathname();
  const { user, logout } = useAuth();
  const [showScrollUp, setShowScrollUp] = useState(false);
  const [showScrollDown, setShowScrollDown] = useState(false);
  const navRef = useRef<HTMLDivElement>(null);

  // Filtrer les éléments de navigation selon le rôle
  const filteredNavItems = navItems.filter(item => {
    if (item.studentOnly && user?.role !== 'student') return false;
    if (item.teacherOnly && user?.role !== 'teacher') return false;
    return true;
  });

  // Filtrer les éléments IA selon le rôle
  const filteredAiNavItems = aiNavItems.filter(item => {
    if (item.studentOnly && user?.role !== 'student') return false;
    if (item.teacherOnly && user?.role !== 'teacher') return false;
    return true;
  });

  // Vérifier si le scroll est nécessaire
  useEffect(() => {
    const checkScroll = () => {
      if (navRef.current) {
        const { scrollTop, scrollHeight, clientHeight } = navRef.current;
        setShowScrollUp(scrollTop > 0);
        setShowScrollDown(scrollTop < scrollHeight - clientHeight - 1);
      }
    };

    checkScroll();
    const navElement = navRef.current;
    if (navElement) {
      navElement.addEventListener('scroll', checkScroll);
      return () => navElement.removeEventListener('scroll', checkScroll);
    }
  }, [user?.role]);

  const scrollUp = () => {
    if (navRef.current) {
      navRef.current.scrollBy({ top: -100, behavior: 'smooth' });
    }
  };

  const scrollDown = () => {
    if (navRef.current) {
      navRef.current.scrollBy({ top: 100, behavior: 'smooth' });
    }
  };

  return (
    <div className="fixed left-0 top-0 h-full w-56 bg-white shadow-lg z-50">
      <div className="flex flex-col h-full">
        {/* Logo */}
        <div className="flex-shrink-0 p-6 border-b border-gray-200">
          <Logo />
        </div>

        {/* Navigation avec scroll */}
        <div className="flex-1 relative">
          {/* Bouton scroll up */}
          {showScrollUp && (
            <button
              onClick={scrollUp}
              className="absolute top-2 left-1/2 transform -translate-x-1/2 z-10 bg-white border border-gray-200 rounded-full p-1 shadow-md hover:shadow-lg transition-all duration-200"
            >
              <ChevronUp size={16} className="text-gray-600" />
            </button>
          )}

          {/* Zone de navigation scrollable */}
          <nav 
            ref={navRef}
            className="h-full overflow-y-auto p-4 space-y-6"
            style={{ 
              scrollbarWidth: 'thin', 
              scrollbarColor: '#CBD5E0 #F7FAFC',
              paddingTop: showScrollUp ? '3rem' : '1rem',
              paddingBottom: showScrollDown ? '3rem' : '1rem'
            }}
          >
            {/* Navigation principale */}
            <div>
              <ul className="space-y-2">
                {filteredNavItems.map((item) => {
                  const isActive = pathname === item.href;
                  return (
                    <li key={item.href}>
                      <Link
                        href={item.href}
                        className={`flex items-center gap-3 px-4 py-3 rounded-lg transition-colors ${
                          isActive
                            ? 'bg-blue-50 text-blue-700 border border-blue-200'
                            : 'text-gray-700 hover:bg-gray-50'
                        }`}
                      >
                        {item.icon}
                        <span className="font-medium">{item.label}</span>
                      </Link>
                    </li>
                  );
                })}
              </ul>
            </div>

            {/* Section IA Avancées - seulement pour les professeurs */}
            {user?.role === 'teacher' && filteredAiNavItems.length > 0 && (
              <div>
                <div className="px-4 py-2">
                  <h3 className="text-xs font-semibold text-gray-500 uppercase tracking-wider">
                    IA & Analytics
                  </h3>
                </div>
                <ul className="space-y-2">
                  {filteredAiNavItems.map((item) => {
                    const isActive = pathname === item.href;
                    return (
                      <li key={item.href}>
                        <Link
                          href={item.href}
                          className={`flex items-center gap-3 px-4 py-3 rounded-lg transition-colors ${
                            isActive
                              ? 'bg-purple-50 text-purple-700 border border-purple-200'
                              : 'text-gray-700 hover:bg-purple-50'
                          }`}
                        >
                          {item.icon}
                          <span className="font-medium">{item.label}</span>
                        </Link>
                      </li>
                    );
                  })}
                </ul>
              </div>
            )}
          </nav>

          {/* Bouton scroll down */}
          {showScrollDown && (
            <button
              onClick={scrollDown}
              className="absolute bottom-2 left-1/2 transform -translate-x-1/2 z-10 bg-white border border-gray-200 rounded-full p-1 shadow-md hover:shadow-lg transition-all duration-200"
            >
              <ChevronDown size={16} className="text-gray-600" />
            </button>
          )}
        </div>

        {/* User Profile */}
        <div className="flex-shrink-0 p-4 border-t border-gray-200">
          <div className="flex items-center gap-3 p-3 rounded-lg bg-gray-50">
            <div className="w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center">
              <span className="text-white text-sm font-medium">
                {user?.name?.charAt(0) || user?.email?.charAt(0) || 'U'}
              </span>
            </div>
            <div className="flex-1 min-w-0">
              <p className="text-sm font-medium text-gray-900 truncate">
                {user?.name || user?.email || 'Utilisateur'}
              </p>
              <p className="text-xs text-gray-500 truncate">
                {user?.email || 'email@example.com'}
              </p>
            </div>
            <button
              onClick={logout}
              className="text-gray-400 hover:text-gray-600 transition-colors"
            >
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
              </svg>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
} 