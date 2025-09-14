'use client';

import React, { useState, useEffect } from 'react';
import { ArrowLeft, Save, Eye, Target, Calendar, Plus, Trash2 } from 'lucide-react';
import Link from 'next/link';

interface AssessmentConfig {
  title: string;
  subject: string;
  assessmentType: 'project' | 'presentation' | 'discussion' | 'portfolio' | 'observation' | 'self_evaluation';
  description: string;
  dueDate: string;
  duration: number;
  maxStudents: number;
  criteria: string[];
  instructions: string;
  rubric: {
    excellent: string;
    good: string;
    satisfactory: string;
    needsImprovement: string;
  };
}

interface Assessment {
  id: number;
  title: string;
  subject: string;
  assessment_type: string;
  due_date: string;
  status: string;
  student_count: number;
  average_score: number;
  config?: AssessmentConfig;
}

export default function EditAssessmentPage({ params }: { params: { id: string } }) {
  const [assessment, setAssessment] = useState<Assessment | null>(null);
  const [assessmentConfig, setAssessmentConfig] = useState<AssessmentConfig>({
    title: '',
    subject: '',
    assessmentType: 'project',
    description: '',
    dueDate: '',
    duration: 60,
    maxStudents: 30,
    criteria: [],
    instructions: '',
    rubric: {
      excellent: '',
      good: '',
      satisfactory: '',
      needsImprovement: ''
    }
  });
  const [isLoading, setIsLoading] = useState(true);
  const [isSaving, setIsSaving] = useState(false);
  const [showPreview, setShowPreview] = useState(false);

  const subjects = [
    'Français', 'Mathématiques', 'Histoire', 'Géographie', 'Sciences', 
    'Anglais', 'Espagnol', 'Physique', 'Chimie', 'Biologie', 'Philosophie',
    'Arts Plastiques', 'Musique', 'EPS', 'Technologie'
  ];

  const assessmentTypes = [
    { 
      value: 'project', 
      label: 'Projet de Recherche', 
      icon: Target,
      description: 'Travail de recherche individuel ou en groupe',
      color: 'text-blue-600'
    },
    { 
      value: 'presentation', 
      label: 'Présentation Orale', 
      icon: Target,
      description: 'Exposé oral devant la classe',
      color: 'text-green-600'
    },
    { 
      value: 'discussion', 
      label: 'Discussion Critique', 
      icon: Target,
      description: 'Débat et analyse critique en groupe',
      color: 'text-purple-600'
    },
    { 
      value: 'portfolio', 
      label: 'Portfolio', 
      icon: Target,
      description: 'Collection de travaux et réflexions',
      color: 'text-orange-600'
    },
    { 
      value: 'observation', 
      label: 'Observation Participante', 
      icon: Target,
      description: 'Observation et analyse de situations',
      color: 'text-red-600'
    },
    { 
      value: 'self_evaluation', 
      label: 'Auto-évaluation', 
      icon: Target,
      description: 'Évaluation de ses propres compétences',
      color: 'text-indigo-600'
    }
  ];

  const defaultCriteria = [
    'Compréhension du sujet',
    'Qualité de la recherche',
    'Organisation des idées',
    'Clarté de l\'expression',
    'Originalité de la réflexion',
    'Respect des consignes',
    'Ponctualité',
    'Participation active'
  ];

  useEffect(() => {
    // Récupérer toutes les évaluations depuis localStorage
    const allAssessments = JSON.parse(localStorage.getItem('formativeAssessments') || '[]');
    const defaultAssessments = [
      {
        id: 1,
        title: "Projet de Recherche - Écologie",
        subject: "Sciences",
        assessment_type: "project",
        due_date: "2024-02-15",
        status: "active",
        student_count: 22,
        average_score: 78.5
      },
      {
        id: 2,
        title: "Présentation Orale - Littérature",
        subject: "Français",
        assessment_type: "presentation",
        due_date: "2024-02-10",
        status: "completed",
        student_count: 25,
        average_score: 82.3
      },
      {
        id: 3,
        title: "Discussion Critique - Philosophie",
        subject: "Philosophie",
        assessment_type: "discussion",
        due_date: "2024-02-20",
        status: "active",
        student_count: 20,
        average_score: 0
      }
    ];

    const allAssessmentsCombined = [...defaultAssessments, ...allAssessments];
    const foundAssessment = allAssessmentsCombined.find(a => a.id === parseInt(params.id));
    
    if (foundAssessment) {
      setAssessment(foundAssessment);
      
      // Remplir la configuration avec les données existantes
      if (foundAssessment.config) {
        setAssessmentConfig({
          title: foundAssessment.title,
          subject: foundAssessment.subject,
          assessmentType: foundAssessment.assessment_type as any,
          description: foundAssessment.config.description || '',
          dueDate: foundAssessment.due_date,
          duration: foundAssessment.config.duration || 60,
          maxStudents: foundAssessment.config.maxStudents || foundAssessment.student_count,
          criteria: foundAssessment.config.criteria || [],
          instructions: foundAssessment.config.instructions || '',
          rubric: foundAssessment.config.rubric || {
            excellent: '',
            good: '',
            satisfactory: '',
            needsImprovement: ''
          }
        });
      } else {
        // Configuration par défaut si pas de config existante
        setAssessmentConfig({
          title: foundAssessment.title,
          subject: foundAssessment.subject,
          assessmentType: foundAssessment.assessment_type as any,
          description: '',
          dueDate: foundAssessment.due_date,
          duration: 60,
          maxStudents: foundAssessment.student_count,
          criteria: [],
          instructions: '',
          rubric: {
            excellent: '',
            good: '',
            satisfactory: '',
            needsImprovement: ''
          }
        });
      }
    }
    
    setIsLoading(false);
  }, [params.id]);

  const handleSave = async () => {
    if (!assessment) return;
    
    setIsSaving(true);
    
    // Simulation de sauvegarde
    await new Promise(resolve => setTimeout(resolve, 1500));
    
    // Mettre à jour l'évaluation
    const updatedAssessment = {
      ...assessment,
      title: assessmentConfig.title,
      subject: assessmentConfig.subject,
      assessment_type: assessmentConfig.assessmentType,
      due_date: assessmentConfig.dueDate,
      student_count: assessmentConfig.maxStudents,
      config: assessmentConfig
    };

    // Mettre à jour dans localStorage
    const allAssessments = JSON.parse(localStorage.getItem('formativeAssessments') || '[]');
    const defaultAssessments = [
      {
        id: 1,
        title: "Projet de Recherche - Écologie",
        subject: "Sciences",
        assessment_type: "project",
        due_date: "2024-02-15",
        status: "active",
        student_count: 22,
        average_score: 78.5
      },
      {
        id: 2,
        title: "Présentation Orale - Littérature",
        subject: "Français",
        assessment_type: "presentation",
        due_date: "2024-02-10",
        status: "completed",
        student_count: 25,
        average_score: 82.3
      },
      {
        id: 3,
        title: "Discussion Critique - Philosophie",
        subject: "Philosophie",
        assessment_type: "discussion",
        due_date: "2024-02-20",
        status: "active",
        student_count: 20,
        average_score: 0
      }
    ];

    // Remplacer l'évaluation par défaut si c'est le cas
    let updated = false;
    const updatedDefaultAssessments = defaultAssessments.map(a => {
      if (a.id === assessment.id) {
        updated = true;
        return updatedAssessment;
      }
      return a;
    });

    // Si c'était une évaluation par défaut, la mettre à jour
    if (updated) {
      // Mettre à jour les évaluations par défaut dans le localStorage
      localStorage.setItem('defaultFormativeAssessments', JSON.stringify(updatedDefaultAssessments));
    } else {
      // Mettre à jour dans les évaluations créées par l'utilisateur
      const updatedUserAssessments = allAssessments.map(a => 
        a.id === assessment.id ? updatedAssessment : a
      );
      localStorage.setItem('formativeAssessments', JSON.stringify(updatedUserAssessments));
    }

    setIsSaving(false);
    
    // Rediriger vers la page de visualisation
    window.location.href = `/dashboard/teacher/adaptive-evaluation/view-assessment/${assessment.id}`;
  };

  const handleAddCriterion = (criterion: string) => {
    if (criterion.trim() && !assessmentConfig.criteria.includes(criterion.trim())) {
      setAssessmentConfig({
        ...assessmentConfig,
        criteria: [...assessmentConfig.criteria, criterion.trim()]
      });
    }
  };

  const handleRemoveCriterion = (criterionToRemove: string) => {
    setAssessmentConfig({
      ...assessmentConfig,
      criteria: assessmentConfig.criteria.filter(c => c !== criterionToRemove)
    });
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Chargement de l'évaluation...</p>
        </div>
      </div>
    );
  }

  if (!assessment) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="text-red-500 text-6xl mb-4">⚠️</div>
          <h2 className="text-2xl font-bold text-gray-900 mb-2">Évaluation non trouvée</h2>
          <p className="text-gray-600 mb-4">L'évaluation que vous voulez modifier n'existe pas.</p>
          <Link
            href="/dashboard/teacher/adaptive-evaluation"
            className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
          >
            Retour aux évaluations
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-4xl mx-auto py-8 px-4">
        {/* Header */}
        <div className="mb-8">
          <Link
            href={`/dashboard/teacher/adaptive-evaluation/view-assessment/${assessment.id}`}
            className="inline-flex items-center text-blue-600 hover:text-blue-700 mb-4"
          >
            <ArrowLeft className="w-4 h-4 mr-2" />
            Retour à l'évaluation
          </Link>
          <h1 className="text-3xl font-bold text-gray-900">Modifier l'Évaluation</h1>
          <p className="text-gray-600 mt-2">
            Modifiez les paramètres de "{assessment.title}"
          </p>
        </div>

        {/* Formulaire de modification */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-8">
          <div className="space-y-6">
            {/* Titre et Matière */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Titre de l'évaluation <span className="text-red-500">*</span>
                </label>
                <input
                  type="text"
                  value={assessmentConfig.title}
                  onChange={(e) => setAssessmentConfig({...assessmentConfig, title: e.target.value})}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Matière <span className="text-red-500">*</span>
                </label>
                <select
                  value={assessmentConfig.subject}
                  onChange={(e) => setAssessmentConfig({...assessmentConfig, subject: e.target.value})}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                >
                  <option value="">Sélectionnez une matière</option>
                  {subjects.map(subject => (
                    <option key={subject} value={subject}>{subject}</option>
                  ))}
                </select>
              </div>
            </div>

            {/* Type d'évaluation */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Type d'évaluation <span className="text-red-500">*</span>
              </label>
              <div className="grid grid-cols-1 gap-3">
                {assessmentTypes.map(type => (
                  <label key={type.value} className="flex items-start space-x-3 p-3 border border-gray-200 rounded-lg cursor-pointer hover:border-blue-300">
                    <input
                      type="radio"
                      name="assessmentType"
                      value={type.value}
                      checked={assessmentConfig.assessmentType === type.value}
                      onChange={(e) => setAssessmentConfig({...assessmentConfig, assessmentType: e.target.value as any})}
                      className="mt-1 rounded-full border-gray-300 text-blue-600 focus:ring-blue-500"
                    />
                    <div className="flex items-center space-x-3">
                      <type.icon className={`w-5 h-5 ${type.color}`} />
                      <div>
                        <div className="font-medium text-gray-900">{type.label}</div>
                        <div className="text-sm text-gray-600">{type.description}</div>
                      </div>
                    </div>
                  </label>
                ))}
              </div>
            </div>

            {/* Description */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Description
              </label>
              <textarea
                value={assessmentConfig.description}
                onChange={(e) => setAssessmentConfig({...assessmentConfig, description: e.target.value})}
                placeholder="Décrivez brièvement l'évaluation..."
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                rows={3}
              />
            </div>

            {/* Planning */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Date d'échéance <span className="text-red-500">*</span>
                </label>
                <input
                  type="date"
                  value={assessmentConfig.dueDate}
                  onChange={(e) => setAssessmentConfig({...assessmentConfig, dueDate: e.target.value})}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Durée estimée (minutes)
                </label>
                <input
                  type="number"
                  value={assessmentConfig.duration}
                  onChange={(e) => setAssessmentConfig({...assessmentConfig, duration: parseInt(e.target.value)})}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  min="15"
                  max="480"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Nombre maximum d'étudiants
                </label>
                <input
                  type="number"
                  value={assessmentConfig.maxStudents}
                  onChange={(e) => setAssessmentConfig({...assessmentConfig, maxStudents: parseInt(e.target.value)})}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  min="1"
                  max="100"
                />
              </div>
            </div>

            {/* Instructions */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Instructions détaillées
              </label>
              <textarea
                value={assessmentConfig.instructions}
                onChange={(e) => setAssessmentConfig({...assessmentConfig, instructions: e.target.value})}
                placeholder="Donnez des instructions claires aux étudiants..."
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                rows={4}
              />
            </div>

            {/* Critères d'évaluation */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Critères d'évaluation
              </label>
              <div className="grid grid-cols-2 gap-2 mb-4">
                {defaultCriteria.map(criterion => (
                  <label key={criterion} className="flex items-center space-x-2">
                    <input
                      type="checkbox"
                      checked={assessmentConfig.criteria.includes(criterion)}
                      onChange={(e) => {
                        if (e.target.checked) {
                          setAssessmentConfig({...assessmentConfig, criteria: [...assessmentConfig.criteria, criterion]});
                        } else {
                          setAssessmentConfig({...assessmentConfig, criteria: assessmentConfig.criteria.filter(c => c !== criterion)});
                        }
                      }}
                      className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                    />
                    <span className="text-sm text-gray-700">{criterion}</span>
                  </label>
                ))}
              </div>
              
              <div className="flex space-x-2">
                <input
                  type="text"
                  placeholder="Ajouter un critère personnalisé..."
                  className="flex-1 px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  onKeyPress={(e) => {
                    if (e.key === 'Enter' && e.currentTarget.value.trim()) {
                      handleAddCriterion(e.currentTarget.value);
                      e.currentTarget.value = '';
                    }
                  }}
                />
                <button
                  onClick={(e) => {
                    const input = e.currentTarget.previousElementSibling as HTMLInputElement;
                    if (input.value.trim()) {
                      handleAddCriterion(input.value);
                      input.value = '';
                    }
                  }}
                  className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
                >
                  <Plus className="w-4 h-4" />
                </button>
              </div>

              {/* Critères personnalisés ajoutés */}
              {assessmentConfig.criteria.filter(c => !defaultCriteria.includes(c)).length > 0 && (
                <div className="mt-4">
                  <h4 className="text-sm font-medium text-gray-700 mb-2">Critères personnalisés :</h4>
                  <div className="flex flex-wrap gap-2">
                    {assessmentConfig.criteria.filter(c => !defaultCriteria.includes(c)).map((criterion, index) => (
                      <span key={index} className="px-2 py-1 bg-blue-100 text-blue-800 rounded-full text-xs flex items-center space-x-1">
                        <span>{criterion}</span>
                        <button
                          onClick={() => handleRemoveCriterion(criterion)}
                          className="ml-1 text-blue-600 hover:text-blue-800"
                        >
                          <Trash2 className="w-3 h-3" />
                        </button>
                      </span>
                    ))}
                  </div>
                </div>
              )}
            </div>

            {/* Grille d'évaluation */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Grille d'évaluation (Rubric)
              </label>
              <div className="space-y-3">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Excellent (4 points)</label>
                  <textarea
                    value={assessmentConfig.rubric.excellent}
                    onChange={(e) => setAssessmentConfig({
                      ...assessmentConfig, 
                      rubric: {...assessmentConfig.rubric, excellent: e.target.value}
                    })}
                    placeholder="Description du niveau excellent..."
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    rows={2}
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Bon (3 points)</label>
                  <textarea
                    value={assessmentConfig.rubric.good}
                    onChange={(e) => setAssessmentConfig({
                      ...assessmentConfig, 
                      rubric: {...assessmentConfig.rubric, good: e.target.value}
                    })}
                    placeholder="Description du niveau bon..."
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    rows={2}
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Satisfaisant (2 points)</label>
                  <textarea
                    value={assessmentConfig.rubric.satisfactory}
                    onChange={(e) => setAssessmentConfig({
                      ...assessmentConfig, 
                      rubric: {...assessmentConfig.rubric, satisfactory: e.target.value}
                    })}
                    placeholder="Description du niveau satisfaisant..."
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    rows={2}
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">À améliorer (1 point)</label>
                  <textarea
                    value={assessmentConfig.rubric.needsImprovement}
                    onChange={(e) => setAssessmentConfig({
                      ...assessmentConfig, 
                      rubric: {...assessmentConfig.rubric, needsImprovement: e.target.value}
                    })}
                    placeholder="Description du niveau à améliorer..."
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    rows={2}
                  />
                </div>
              </div>
            </div>
          </div>

          {/* Actions */}
          <div className="flex justify-between items-center mt-8 pt-6 border-t border-gray-200">
            <div className="flex space-x-3">
              <button
                onClick={() => setShowPreview(!showPreview)}
                className="px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors flex items-center"
              >
                <Eye className="w-4 h-4 mr-2" />
                {showPreview ? 'Masquer' : 'Aperçu'}
              </button>
              <Link
                href={`/dashboard/teacher/adaptive-evaluation/view-assessment/${assessment.id}`}
                className="px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors"
              >
                Annuler
              </Link>
            </div>

            <button
              onClick={handleSave}
              disabled={isSaving || !assessmentConfig.title || !assessmentConfig.subject || !assessmentConfig.dueDate}
              className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors flex items-center"
            >
              {isSaving ? (
                <>
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                  Sauvegarde...
                </>
              ) : (
                <>
                  <Save className="w-4 h-4 mr-2" />
                  Sauvegarder les modifications
                </>
              )}
            </button>
          </div>

          {/* Aperçu */}
          {showPreview && (
            <div className="mt-6 p-6 bg-gray-50 rounded-lg border border-gray-200">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Aperçu de l'évaluation</h3>
              <div className="space-y-4">
                <div>
                  <h4 className="font-medium text-gray-900">{assessmentConfig.title}</h4>
                  <p className="text-gray-600">{assessmentConfig.description}</p>
                </div>
                <div className="grid grid-cols-2 gap-4 text-sm">
                  <div>
                    <span className="font-medium text-gray-700">Matière:</span>
                    <span className="ml-2 text-gray-900">{assessmentConfig.subject}</span>
                  </div>
                  <div>
                    <span className="font-medium text-gray-700">Type:</span>
                    <span className="ml-2 text-gray-900 capitalize">{assessmentConfig.assessmentType}</span>
                  </div>
                  <div>
                    <span className="font-medium text-gray-700">Échéance:</span>
                    <span className="ml-2 text-gray-900">{assessmentConfig.dueDate}</span>
                  </div>
                  <div>
                    <span className="font-medium text-gray-700">Critères:</span>
                    <span className="ml-2 text-gray-900">{assessmentConfig.criteria.length}</span>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
























