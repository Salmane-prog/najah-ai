'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { 
  Brain, 
  Plus, 
  Save, 
  ArrowLeft, 
  Loader2, 
  CheckCircle, 
  AlertCircle,
  BookOpen,
  Target,
  Clock,
  Users,
  Eye,
  Edit
} from 'lucide-react';
import { formativeEvaluationService, FormativeEvaluationRequest, AIGeneratedEvaluation } from '@/services/formativeEvaluationService';

export default function CreateFormativeAssessmentPage() {
  const router = useRouter();
  const [isLoading, setIsLoading] = useState(false);
  const [isGenerating, setIsGenerating] = useState(false);
  const [availableTypes, setAvailableTypes] = useState<any[]>([]);
  const [generatedEvaluation, setGeneratedEvaluation] = useState<AIGeneratedEvaluation | null>(null);
  const [showGenerated, setShowGenerated] = useState(false);

  // Formulaire de base
  const [formData, setFormData] = useState<FormativeEvaluationRequest>({
    title: '',
    subject: '',
    assessment_type: '',
    description: '',
    target_level: 'intermediate',
    duration_minutes: 60,
    max_students: 30,
    learning_objectives: [''],
    custom_requirements: ''
  });

  // Charger les types d'évaluations disponibles
  useEffect(() => {
    loadAvailableTypes();
  }, []);

  const loadAvailableTypes = async () => {
    try {
      const types = await formativeEvaluationService.getAvailableTypes();
      setAvailableTypes(types);
    } catch (error) {
      console.error('Erreur lors du chargement des types:', error);
      // Types par défaut si l'API échoue
      setAvailableTypes([
        { type: 'project', name: 'Projet de Recherche', description: 'Travail de recherche individuel ou en groupe' },
        { type: 'presentation', name: 'Présentation Orale', description: 'Exposé oral devant la classe' },
        { type: 'discussion', name: 'Discussion Critique', description: 'Débat et analyse critique en groupe' },
        { type: 'portfolio', name: 'Portfolio', description: 'Collection de travaux et réflexions' },
        { type: 'observation', name: 'Observation Participante', description: 'Observation et analyse de situations' },
        { type: 'self_evaluation', name: 'Auto-évaluation', description: 'Évaluation de ses propres compétences' }
      ]);
    }
  };

  // Gérer les changements du formulaire
  const handleInputChange = (field: keyof FormativeEvaluationRequest, value: any) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  // Gérer les objectifs d'apprentissage
  const handleLearningObjectiveChange = (index: number, value: string) => {
    const newObjectives = [...formData.learning_objectives];
    newObjectives[index] = value;
    setFormData(prev => ({ ...prev, learning_objectives: newObjectives }));
  };

  const addLearningObjective = () => {
    setFormData(prev => ({
      ...prev,
      learning_objectives: [...prev.learning_objectives, '']
    }));
  };

  const removeLearningObjective = (index: number) => {
    if (formData.learning_objectives.length > 1) {
      const newObjectives = formData.learning_objectives.filter((_, i) => i !== index);
      setFormData(prev => ({ ...prev, learning_objectives: newObjectives }));
    }
  };

  // Générer l'évaluation avec l'IA
  const handleGenerateWithAI = async () => {
    if (!formData.assessment_type || !formData.subject || !formData.description) {
      alert('Veuillez remplir tous les champs obligatoires');
      return;
    }

    setIsGenerating(true);
    try {
      const evaluation = await formativeEvaluationService.generateWithAI(formData);
      setGeneratedEvaluation(evaluation);
      setShowGenerated(true);
    } catch (error) {
      console.error('Erreur lors de la génération IA:', error);
      alert('Erreur lors de la génération avec l\'IA');
    } finally {
      setIsGenerating(false);
    }
  };

  // Sauvegarder l'évaluation générée
  const handleSaveEvaluation = async () => {
    if (!generatedEvaluation) return;

    setIsLoading(true);
    try {
      // Passer à la fois l'évaluation générée ET les données du formulaire
      await formativeEvaluationService.createEvaluation(generatedEvaluation, formData);
      alert('Évaluation créée avec succès !');
      router.push('/dashboard/teacher/adaptive-evaluation');
    } catch (error) {
      console.error('Erreur lors de la sauvegarde:', error);
      alert('Erreur lors de la sauvegarde');
    } finally {
      setIsLoading(false);
    }
  };

  // Modifier l'évaluation générée
  const handleEditGenerated = () => {
    setShowGenerated(false);
  };

  return (
    <div className="container mx-auto p-6 max-w-4xl">
      {/* Header */}
      <div className="flex items-center justify-between mb-8">
        <div className="flex items-center space-x-4">
          <Button
            variant="ghost"
            onClick={() => router.back()}
            className="flex items-center space-x-2"
          >
            <ArrowLeft className="w-4 h-4" />
            <span>Retour</span>
          </Button>
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Créer une Évaluation Formative</h1>
            <p className="text-gray-600">Utilisez l&apos;IA pour générer des évaluations personnalisées</p>
          </div>
        </div>
      </div>

      {!showGenerated ? (
        /* Formulaire de base */
        <Card className="mb-8">
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <BookOpen className="w-5 h-5" />
              <span>Informations de base</span>
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-6">
            {/* Type d'évaluation */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="space-y-2">
                <label htmlFor="assessment_type" className="block text-sm font-medium text-gray-700">
                  Type d&apos;évaluation *
                </label>
                <select
                  id="assessment_type"
                  value={formData.assessment_type}
                  onChange={(e) => handleInputChange('assessment_type', e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                >
                  <option value="">Sélectionnez un type</option>
                  {availableTypes.map((type) => (
                    <option key={type.type} value={type.type}>
                      {type.name}
                    </option>
                  ))}
                </select>
                {formData.assessment_type && (
                  <p className="text-sm text-gray-600">
                    {availableTypes.find(t => t.type === formData.assessment_type)?.description}
                  </p>
                )}
              </div>

              <div className="space-y-2">
                <label htmlFor="subject" className="block text-sm font-medium text-gray-700">
                  Matière *
                </label>
                <input
                  id="subject"
                  type="text"
                  value={formData.subject}
                  onChange={(e) => handleInputChange('subject', e.target.value)}
                  placeholder="Ex: Mathématiques, Français, Histoire..."
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>
            </div>

            {/* Titre et description */}
            <div className="space-y-2">
              <label htmlFor="title" className="block text-sm font-medium text-gray-700">
                Titre de l&apos;évaluation *
              </label>
              <input
                id="title"
                type="text"
                value={formData.title}
                onChange={(e) => handleInputChange('title', e.target.value)}
                placeholder="Ex: Évaluation des compétences de recherche"
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>

            <div className="space-y-2">
              <label htmlFor="description" className="block text-sm font-medium text-gray-700">
                Description détaillée *
              </label>
              <textarea
                id="description"
                value={formData.description}
                onChange={(e) => handleInputChange('description', e.target.value)}
                placeholder="Décrivez les objectifs et le contexte de cette évaluation..."
                rows={4}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>

            {/* Paramètres avancés */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div className="space-y-2">
                <label htmlFor="target_level" className="block text-sm font-medium text-gray-700">
                  Niveau cible
                </label>
                <select
                  id="target_level"
                  value={formData.target_level}
                  onChange={(e) => handleInputChange('target_level', e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                >
                  <option value="beginner">Débutant</option>
                  <option value="intermediate">Intermédiaire</option>
                  <option value="advanced">Avancé</option>
                </select>
              </div>

              <div className="space-y-2">
                <label htmlFor="duration_minutes" className="block text-sm font-medium text-gray-700">
                  Durée (minutes)
                </label>
                <input
                  id="duration_minutes"
                  type="number"
                  value={formData.duration_minutes}
                  onChange={(e) => handleInputChange('duration_minutes', parseInt(e.target.value))}
                  min="15"
                  max="480"
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>

              <div className="space-y-2">
                <label htmlFor="max_students" className="block text-sm font-medium text-gray-700">
                  Étudiants max
                </label>
                <input
                  id="max_students"
                  type="number"
                  value={formData.max_students}
                  onChange={(e) => handleInputChange('max_students', parseInt(e.target.value))}
                  min="1"
                  max="100"
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>
            </div>

            {/* Objectifs d'apprentissage */}
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <label className="block text-sm font-medium text-gray-700">Objectifs d&apos;apprentissage</label>
                <Button
                  type="button"
                  variant="outline"
                  size="sm"
                  onClick={addLearningObjective}
                  className="flex items-center space-x-2"
                >
                  <Plus className="w-4 h-4" />
                  <span>Ajouter</span>
                </Button>
              </div>
              
              <div className="space-y-3">
                {formData.learning_objectives.map((objective, index) => (
                  <div key={index} className="flex items-center space-x-2">
                    <input
                      type="text"
                      value={objective}
                      onChange={(e) => handleLearningObjectiveChange(index, e.target.value)}
                      placeholder={`Objectif ${index + 1}`}
                      className="flex-1 px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    />
                    {formData.learning_objectives.length > 1 && (
                      <Button
                        type="button"
                        variant="ghost"
                        size="sm"
                        onClick={() => removeLearningObjective(index)}
                        className="text-red-500 hover:text-red-700"
                      >
                        <AlertCircle className="w-4 h-4" />
                      </Button>
                    )}
                  </div>
                ))}
              </div>
            </div>

            {/* Exigences personnalisées */}
            <div className="space-y-2">
              <label htmlFor="custom_requirements" className="block text-sm font-medium text-gray-700">
                Exigences personnalisées (optionnel)
              </label>
              <textarea
                id="custom_requirements"
                value={formData.custom_requirements}
                onChange={(e) => handleInputChange('custom_requirements', e.target.value)}
                placeholder="Ajoutez des exigences spécifiques ou des contraintes particulières..."
                rows={3}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>

            {/* Bouton de génération IA */}
            <div className="pt-4">
              <Button
                onClick={handleGenerateWithAI}
                disabled={isGenerating || !formData.assessment_type || !formData.subject || !formData.description}
                className="w-full bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 text-white py-3 text-lg"
              >
                {isGenerating ? (
                  <>
                    <Loader2 className="w-5 h-5 mr-2 animate-spin" />
                    Génération en cours...
                  </>
                ) : (
                  <>
                    <Brain className="w-5 h-5 mr-2" />
                    Générer avec l&apos;IA
                  </>
                )}
              </Button>
            </div>
          </CardContent>
        </Card>
      ) : (
        /* Affichage de l'évaluation générée */
        <div className="space-y-6">
          {/* Actions */}
          <div className="flex items-center justify-between">
            <h2 className="text-2xl font-bold text-gray-900">Évaluation générée par l&apos;IA</h2>
            <div className="flex space-x-3">
              <Button
                variant="outline"
                onClick={handleEditGenerated}
                className="flex items-center space-x-2"
              >
                <AlertCircle className="w-4 h-4" />
                <span>Modifier</span>
              </Button>
              <Button
                onClick={handleSaveEvaluation}
                disabled={isLoading}
                className="bg-green-600 hover:bg-green-700 text-white"
              >
                {isLoading ? (
                  <>
                    <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                    Sauvegarde...
                  </>
                ) : (
                  <>
                    <Save className="w-4 h-4 mr-2" />
                    Sauvegarder
                  </>
                )}
              </Button>
            </div>
          </div>

          {/* Évaluation générée */}
          <Card>
            <CardHeader>
              <div className="flex items-center justify-between">
                <div>
                  <CardTitle className="text-xl">{generatedEvaluation?.title}</CardTitle>
                  <p className="text-gray-600 mt-1">{generatedEvaluation?.description}</p>
                </div>
                <span className="px-3 py-1 bg-orange-100 text-orange-800 rounded-full text-sm font-medium capitalize">
                  {generatedEvaluation?.assessment_type}
                </span>
              </div>
            </CardHeader>
            <CardContent className="space-y-6">
              {/* Informations générales */}
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                <div className="flex items-center space-x-2 text-sm text-gray-600">
                  <Target className="w-4 h-4" />
                  <span>Niveau {generatedEvaluation?.difficulty_level || 'Non défini'}</span>
                </div>
                <div className="flex items-center space-x-2 text-sm text-gray-600">
                  <Clock className="w-4 h-4" />
                  <span>{generatedEvaluation?.estimated_duration || 0} min</span>
                </div>
                <div className="flex items-center space-x-2 text-sm text-gray-600">
                  <Users className="w-4 h-4" />
                  <span>Max {formData.max_students}</span>
                </div>
                <div className="flex items-center space-x-2 text-sm text-gray-600">
                  <BookOpen className="w-4 h-4" />
                  <span>{generatedEvaluation?.questions?.length || 0} questions</span>
                </div>
              </div>

              {/* Critères d'évaluation */}
              <div className="space-y-4">
                <h3 className="text-lg font-semibold text-gray-900">Critères d&apos;évaluation</h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {generatedEvaluation?.criteria?.map((criterion, index) => (
                    <Card key={index} className="p-4">
                      <div className="flex items-center justify-between mb-2">
                        <h4 className="font-medium text-gray-900">{criterion.name}</h4>
                        <span className="px-2 py-1 bg-gray-100 text-gray-800 rounded text-xs font-medium">
                          {criterion.weight}%
                        </span>
                      </div>
                      <p className="text-sm text-gray-600">{criterion.description}</p>
                      <div className="mt-2 text-xs text-gray-500">
                        Points max: {criterion.max_points}
                      </div>
                    </Card>
                  ))}
                </div>
              </div>

              {/* Grille de notation */}
              <div className="space-y-4">
                <h3 className="text-lg font-semibold text-gray-900">Grille de notation</h3>
                <div className="grid grid-cols-1 md:grid-cols-4 gap-3">
                  {generatedEvaluation?.rubric && Object.entries(generatedEvaluation.rubric).map(([level, data]: [string, any]) => (
                    <Card key={level} className="p-3 text-center">
                      <div className="text-lg font-bold text-gray-900 capitalize mb-1">
                        {level === 'excellent' ? '⭐ Excellent' : 
                         level === 'good' ? '👍 Bon' : 
                         level === 'satisfactory' ? '✅ Satisfaisant' : '⚠️ À améliorer'}
                      </div>
                      <div className="text-2xl font-bold text-purple-600 mb-1">
                        {data.points} pts
                      </div>
                      <p className="text-xs text-gray-600">{data.description}</p>
                    </Card>
                  ))}
                </div>
              </div>

              {/* Questions */}
              <div className="space-y-4">
                <h3 className="text-lg font-semibold text-gray-900">Questions d&apos;évaluation</h3>
                <div className="space-y-3">
                  {generatedEvaluation?.questions?.map((question, index) => (
                    <Card key={index} className="p-4">
                      <div className="flex items-start justify-between">
                        <div className="flex-1">
                          <p className="font-medium text-gray-900 mb-2">
                            {index + 1}. {question.question}
                          </p>
                          <div className="flex items-center space-x-4 text-sm text-gray-600">
                            <span>Type: {question.type}</span>
                            <span>Points: {question.max_points}</span>
                          </div>
                        </div>
                      </div>
                    </Card>
                  ))}
                </div>
              </div>

              {/* Instructions */}
              <div className="space-y-4">
                <h3 className="text-lg font-semibold text-gray-900">Instructions pour les étudiants</h3>
                <Card className="p-4 bg-blue-50">
                  <p className="text-gray-800 whitespace-pre-line">{generatedEvaluation?.instructions}</p>
                </Card>
              </div>

              {/* Indicateurs de réussite */}
              <div className="space-y-4">
                <h3 className="text-lg font-semibold text-gray-900">Indicateurs de réussite</h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                  {generatedEvaluation?.success_indicators?.map((indicator, index) => (
                    <div key={index} className="flex items-center space-x-2">
                      <CheckCircle className="w-4 h-4 text-green-500" />
                      <span className="text-sm text-gray-700">{indicator}</span>
                    </div>
                  ))}
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      )}
    </div>
  );
}
