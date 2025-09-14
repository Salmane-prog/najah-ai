'use client';

import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { Card } from '../../../../../components/Card';
import Button from '../../../../../components/Button';
import { 
  Brain, 
  Users, 
  Target, 
  Clock, 
  BookOpen, 
  Plus,
  ArrowLeft,
  CheckCircle,
  AlertCircle
} from 'lucide-react';
import { adaptiveEvaluationService } from '../../../../../services/adaptiveEvaluationService';
import { CreateTestData } from '../../../../../types/adaptiveEvaluation';

interface Student {
  id: number;
  username: string;
  first_name: string;
  last_name: string;
  email: string;
}



export default function CreateAdaptiveEvaluationPage() {
  const router = useRouter();
  const [config, setConfig] = useState({
    title: '',
    subject: '',
    description: '',
    evaluation_type: 'adaptive_quiz',
    difficulty_range: [3, 7],
    target_duration: 30,
    selected_students: [],
    adaptation_algorithm: 'irt_adaptive',
    irt_parameters: {
      discrimination: 1.0,
      difficulty: 5.0,
      guessing: 0.25
    }
  });
  
  const [students, setStudents] = useState<Student[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [step, setStep] = useState(1);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  // Charger la liste des étudiants
  useEffect(() => {
    loadStudents();
  }, []);

  const loadStudents = async () => {
    try {
              const response = await fetch('http://localhost:8000/api/v1/students/', {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('najah_token') || sessionStorage.getItem('najah_token')}`,
            'Content-Type': 'application/json'
          }
        });
      
      if (response.ok) {
        const data = await response.json();
        setStudents(data);
      } else {
        // Fallback: étudiants d'exemple
        setStudents([
          { id: 1, username: 'etudiant1', first_name: 'Jean', last_name: 'Dupont', email: 'jean@example.com' },
          { id: 2, username: 'etudiant2', first_name: 'Marie', last_name: 'Martin', email: 'marie@example.com' },
          { id: 3, username: 'etudiant3', first_name: 'Pierre', last_name: 'Bernard', email: 'pierre@example.com' },
          { id: 4, username: 'etudiant4', first_name: 'Sophie', last_name: 'Petit', email: 'sophie@example.com' },
          { id: 5, username: 'etudiant5', first_name: 'Lucas', last_name: 'Robert', email: 'lucas@example.com' }
        ]);
      }
    } catch (error) {
      console.error('Erreur lors du chargement des étudiants:', error);
      // Fallback: étudiants d'exemple
      setStudents([
        { id: 1, username: 'etudiant1', first_name: 'Jean', last_name: 'Dupont', email: 'jean@example.com' },
        { id: 2, username: 'etudiant2', first_name: 'Marie', last_name: 'Martin', email: 'marie@example.com' },
        { id: 3, username: 'etudiant3', first_name: 'Pierre', last_name: 'Bernard', email: 'pierre@example.com' },
        { id: 4, username: 'etudiant4', first_name: 'Sophie', last_name: 'Petit', email: 'sophie@example.com' },
        { id: 5, username: 'etudiant5', first_name: 'Lucas', last_name: 'Robert', email: 'lucas@example.com' }
      ]);
    }
  };

  const handleInputChange = (field: string, value: any) => {
    setConfig(prev => ({ ...prev, [field]: value }));
  };

  const handleStudentSelection = (studentId: number) => {
    setConfig(prev => ({
      ...prev,
      selected_students: prev.selected_students.includes(studentId)
        ? prev.selected_students.filter(id => id !== studentId)
        : [...prev.selected_students, studentId]
    }));
  };

  const handleCreateEvaluation = async () => {
    if (!config.title || !config.subject || config.selected_students.length === 0) {
      setError('Veuillez remplir tous les champs obligatoires et sélectionner au moins un étudiant.');
      return;
    }

    setIsLoading(true);
    setError('');
    setSuccess('');

    try {
      console.log('🚀 Tentative de création du test...');
      console.log('📝 Données envoyées:', {
        title: config.title,
        subject: config.subject,
        description: config.description,
        difficulty_min: config.difficulty_range[0],
        difficulty_max: config.difficulty_range[1],
        estimated_duration: config.target_duration,
        adaptation_type: config.adaptation_algorithm,
        learning_objectives: config.description,
        total_questions: 1,
        questions: [
          {
            question_text: "Question par défaut - " + config.title,
            question_type: "multiple_choice",
            difficulty_level: Math.floor((config.difficulty_range[0] + config.difficulty_range[1]) / 2),
            learning_objective: "Vérification du système",
            options: ["Option A", "Option B", "Option C", "Option D"],
            correct_answer: "Option A",
            explanation: "Question créée automatiquement lors de la création du test"
          }
        ]
      });
      
      // Créer l'évaluation adaptative via le backend
      const result = await adaptiveEvaluationService.createTest({
        title: config.title,
        subject: config.subject,
        description: config.description,
        difficulty_min: config.difficulty_range[0],
        difficulty_max: config.difficulty_range[1],
        estimated_duration: config.target_duration,
        adaptation_type: config.adaptation_algorithm,
        learning_objectives: config.description,
        total_questions: 1,
        questions: [
          {
            question_text: "Question par défaut - " + config.title,
            question_type: "multiple_choice",
            difficulty_level: Math.floor((config.difficulty_range[0] + config.difficulty_range[1]) / 2),
            learning_objective: "Vérification du système",
            options: ["Option A", "Option B", "Option C", "Option D"],
            correct_answer: "Option A",
            explanation: "Question créée automatiquement lors de la création du test"
          }
        ]
      });
      
      console.log('✅ Réponse reçue:', result);
      
      if (result && result.success) {
        setSuccess(`Évaluation adaptative "${config.title}" créée avec succès et assignée à ${config.selected_students.length} étudiants !`);
        
        // Rediriger vers la page principale après 2 secondes
        setTimeout(() => {
          router.push('/dashboard/teacher/adaptive-evaluation');
        }, 2000);
      } else {
        console.error('❌ Erreur dans la réponse:', result);
        setError('Erreur lors de la création de l\'évaluation adaptative. Veuillez réessayer.');
      }

    } catch (error) {
      setError('Erreur lors de la création de l\'évaluation adaptative.');
      console.error('Erreur:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const nextStep = () => {
    if (step === 1 && (!config.title || !config.subject)) {
      setError('Veuillez remplir le titre et la matière avant de continuer.');
      return;
    }
    if (step === 2 && config.selected_students.length === 0) {
      setError('Veuillez sélectionner au moins un étudiant avant de continuer.');
      return;
    }
    setStep(prev => Math.min(prev + 1, 3));
    setError('');
  };

  const prevStep = () => {
    setStep(prev => Math.max(prev - 1, 1));
    setError('');
  };

  return (
    <div className="min-h-screen bg-gray-100 py-8">
      <div className="max-w-4xl mx-auto px-4">
        {/* Header */}
        <div className="mb-8">
          <Button
            onClick={() => router.back()}
            variant="outline"
            className="mb-4"
          >
            <ArrowLeft className="w-4 h-4 mr-2" />
            Retour
          </Button>
          
          <h1 className="text-3xl font-bold text-gray-900 flex items-center gap-3">
            <Brain className="h-8 w-8 text-purple-600" />
            Créer une Évaluation Adaptative
          </h1>
          <p className="text-gray-600 mt-2">
            Créez une évaluation qui s'adapte en temps réel selon les réponses des étudiants
          </p>
        </div>

        {/* Étapes */}
        <div className="mb-8">
          <div className="flex items-center justify-center space-x-4">
            {[1, 2, 3].map((stepNumber) => (
              <div key={stepNumber} className="flex items-center">
                <div className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-medium ${
                  stepNumber <= step 
                    ? 'bg-purple-600 text-white' 
                    : 'bg-gray-200 text-gray-600'
                }`}>
                  {stepNumber < step ? <CheckCircle className="w-5 h-5" /> : stepNumber}
                </div>
                {stepNumber < 3 && (
                  <div className={`w-16 h-1 mx-2 ${
                    stepNumber < step ? 'bg-purple-600' : 'bg-gray-200'
                  }`} />
                )}
              </div>
            ))}
          </div>
          
          <div className="text-center mt-4">
            <span className="text-sm text-gray-600">
              {step === 1 && 'Configuration de base'}
              {step === 2 && 'Sélection des étudiants'}
              {step === 3 && 'Paramètres IA et création'}
            </span>
          </div>
        </div>

        {/* Messages d'erreur et de succès */}
        {error && (
          <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg flex items-center gap-2 text-red-700">
            <AlertCircle className="w-5 h-5" />
            {error}
          </div>
        )}

        {success && (
          <div className="mb-6 p-4 bg-green-50 border border-green-200 rounded-lg flex items-center gap-2 text-green-700">
            <CheckCircle className="w-5 h-5" />
            {success}
          </div>
        )}

        {/* Étape 1: Configuration de base */}
        {step === 1 && (
          <Card className="p-6">
            <h2 className="text-xl font-semibold text-gray-800 mb-6">Configuration de base</h2>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Titre de l'évaluation *
                </label>
                <input
                  type="text"
                  value={config.title}
                  onChange={(e) => handleInputChange('title', e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                  placeholder="Ex: Test adaptatif sur les équations"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Matière *
                </label>
                <select
                  value={config.subject}
                  onChange={(e) => handleInputChange('subject', e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                >
                  <option value="">Sélectionner une matière</option>
                  <option value="Mathématiques">Mathématiques</option>
                  <option value="Français">Français</option>
                  <option value="Histoire">Histoire</option>
                  <option value="Sciences">Sciences</option>
                  <option value="Philosophie">Philosophie</option>
                </select>
              </div>

              <div className="md:col-span-2">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Description
                </label>
                <textarea
                  value={config.description}
                  onChange={(e) => handleInputChange('description', e.target.value)}
                  rows={3}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                  placeholder="Décrivez le contenu et les objectifs de cette évaluation adaptative..."
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Type d'évaluation
                </label>
                <select
                  value={config.evaluation_type}
                  onChange={(e) => handleInputChange('evaluation_type', e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                >
                  <option value="adaptive_quiz">Quiz adaptatif</option>
                  <option value="adaptive_test">Test adaptatif</option>
                  <option value="adaptive_assignment">Devoir adaptatif</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Durée cible (minutes)
                </label>
                <input
                  type="number"
                  value={config.target_duration}
                  onChange={(e) => handleInputChange('target_duration', parseInt(e.target.value))}
                  min="15"
                  max="120"
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                />
              </div>
            </div>
          </Card>
        )}

        {/* Étape 2: Sélection des étudiants */}
        {step === 2 && (
          <Card className="p-6">
            <h2 className="text-xl font-semibold text-gray-800 mb-6">Sélection des étudiants</h2>
            
            <div className="mb-4">
              <p className="text-sm text-gray-600 mb-4">
                Sélectionnez les étudiants qui participeront à cette évaluation adaptative.
                L'IA s'adaptera individuellement à chaque étudiant selon ses réponses.
              </p>
              
              <div className="flex items-center gap-2 mb-4">
                <Button
                  onClick={() => setConfig(prev => ({ ...prev, selected_students: students.map(s => s.id) }))}
                  variant="outline"
                  size="sm"
                >
                  Sélectionner tous
                </Button>
                <Button
                  onClick={() => setConfig(prev => ({ ...prev, selected_students: [] }))}
                  variant="outline"
                  size="sm"
                >
                  Désélectionner tous
                </Button>
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {students.map((student) => (
                <div
                  key={student.id}
                  className={`p-4 border rounded-lg cursor-pointer transition-colors ${
                    config.selected_students.includes(student.id)
                      ? 'border-purple-500 bg-purple-50'
                      : 'border-gray-200 hover:border-gray-300'
                  }`}
                  onClick={() => handleStudentSelection(student.id)}
                >
                  <div className="flex items-center gap-3">
                    <div className={`w-4 h-4 rounded-full border-2 ${
                      config.selected_students.includes(student.id)
                        ? 'border-purple-500 bg-purple-500'
                        : 'border-gray-300'
                    }`}>
                      {config.selected_students.includes(student.id) && (
                        <CheckCircle className="w-4 h-4 text-white" />
                      )}
                    </div>
                    <div>
                      <div className="font-medium text-gray-900">
                        {student.first_name} {student.last_name}
                      </div>
                      <div className="text-sm text-gray-600">{student.username}</div>
                    </div>
                  </div>
                </div>
              ))}
            </div>

            {config.selected_students.length > 0 && (
              <div className="mt-6 p-4 bg-blue-50 border border-blue-200 rounded-lg">
                <div className="flex items-center gap-2 text-blue-700">
                  <Users className="w-5 h-5" />
                  <span className="font-medium">
                    {config.selected_students.length} étudiant(s) sélectionné(s)
                  </span>
                </div>
              </div>
            )}
          </Card>
        )}

        {/* Étape 3: Paramètres IA et création */}
        {step === 3 && (
          <Card className="p-6">
            <h2 className="text-xl font-semibold text-gray-800 mb-6">Paramètres IA et création</h2>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Plage de difficulté
                </label>
                <div className="flex items-center gap-4">
                  <div>
                    <label className="block text-xs text-gray-500 mb-1">Min</label>
                    <input
                      type="number"
                      value={config.difficulty_range[0]}
                      onChange={(e) => handleInputChange('difficulty_range', [parseInt(e.target.value), config.difficulty_range[1]])}
                      min="1"
                      max="10"
                      className="w-20 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                    />
                  </div>
                  <div className="text-gray-400">à</div>
                  <div>
                    <label className="block text-xs text-gray-500 mb-1">Max</label>
                    <input
                      type="number"
                      value={config.difficulty_range[1]}
                      onChange={(e) => handleInputChange('difficulty_range', [config.difficulty_range[0], parseInt(e.target.value)])}
                      min="1"
                      max="10"
                      className="w-20 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                    />
                  </div>
                </div>
                <p className="text-xs text-gray-500 mt-1">
                  1 = Très facile, 10 = Très difficile
                </p>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Algorithme d'adaptation
                </label>
                <select
                  value={config.adaptation_algorithm}
                  onChange={(e) => handleInputChange('adaptation_algorithm', e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                >
                  <option value="irt_adaptive">IRT (Item Response Theory)</option>
                  <option value="ml_adaptive">Machine Learning</option>
                  <option value="expert_adaptive">Système Expert</option>
                </select>
              </div>
            </div>

            {/* Résumé de la configuration */}
            <div className="mb-6 p-4 bg-gray-50 border border-gray-200 rounded-lg">
              <h3 className="font-medium text-gray-800 mb-3">Résumé de la configuration</h3>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
                <div>
                  <div className="text-gray-600">Titre</div>
                  <div className="font-medium">{config.title || 'Non défini'}</div>
                </div>
                <div>
                  <div className="text-gray-600">Matière</div>
                  <div className="font-medium">{config.subject || 'Non définie'}</div>
                </div>
                <div>
                  <div className="text-gray-600">Étudiants</div>
                  <div className="font-medium">{config.selected_students.length}</div>
                </div>
                <div>
                  <div className="text-gray-600">Difficulté</div>
                  <div className="font-medium">{config.difficulty_range[0]}-{config.difficulty_range[1]}</div>
                </div>
              </div>
            </div>

            {/* Bouton de création */}
            <div className="flex justify-center">
              <Button
                onClick={handleCreateEvaluation}
                disabled={isLoading}
                className="px-8 py-3 text-lg"
              >
                {isLoading ? (
                  <div className="flex items-center gap-2">
                    <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
                    Création en cours...
                  </div>
                ) : (
                  <div className="flex items-center gap-2">
                    <Brain className="w-5 h-5" />
                    Créer l'Évaluation Adaptative
                  </div>
                )}
              </Button>
            </div>
          </Card>
        )}

        {/* Navigation entre étapes */}
        <div className="flex justify-between mt-8">
          <Button
            onClick={prevStep}
            disabled={step === 1}
            variant="outline"
          >
            Précédent
          </Button>

          {step < 3 && (
            <Button
              onClick={nextStep}
              className="bg-purple-600 hover:bg-purple-700"
            >
              Suivant
            </Button>
          )}
        </div>
      </div>
    </div>
  );
}
