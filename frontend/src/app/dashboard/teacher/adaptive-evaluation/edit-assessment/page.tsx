'use client';

import React, { useState, useEffect, Suspense } from 'react';
import { useSearchParams } from 'next/navigation';
import Sidebar from '@/components/Sidebar';
import { useAuth  } from '@/hooks/useAuth';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { 
  ArrowLeft, 
  Save, 
  Eye,
  Target, 
  Clock, 
  Users, 
  BookOpen,
  Plus,
  Trash2,
  CheckCircle
} from 'lucide-react';
import { FormativeEvaluation, formativeEvaluationService } from '@/services/formativeEvaluationService';

function EditAssessmentContent() {
  const searchParams = useSearchParams();
  const { user, token } = useAuth();
  const [evaluation, setEvaluation] = useState<FormativeEvaluation | null>(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);

  // Formulaire d'édition
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    subject: '',
    target_level: 'intermediate',
    duration_minutes: 60,
    max_students: 30,
    learning_objectives: [''],
    is_active: true
  });

  // Données modifiables
  const [criteria, setCriteria] = useState<Array<{
    name: string;
    description: string;
    weight: number;
    max_points: number;
  }>>([]);

  const [questions, setQuestions] = useState<Array<{
    question: string;
    type: string;
    max_points: number;
  }>>([]);

  const [instructions, setInstructions] = useState('');
  const [successIndicators, setSuccessIndicators] = useState(['']);

  useEffect(() => {
    const id = searchParams.get('id');
    if (id) {
      loadEvaluation(id);
    }
  }, [searchParams]);

  const loadEvaluation = async (evaluationId: string) => {
    try {
      setLoading(true);
      setError(null);
      
      // Essayer de récupérer depuis l'API
      try {
        const evaluations = await formativeEvaluationService.getAllEvaluations();
        const foundEvaluation = evaluations.find(e => e.id.toString() === evaluationId);
        
        if (foundEvaluation) {
          setEvaluation(foundEvaluation);
          populateFormData(foundEvaluation);
          console.log('✅ Évaluation chargée depuis l\'API:', foundEvaluation);
        } else {
          throw new Error('Évaluation non trouvée');
        }
      } catch (apiError) {
        console.log('⚠️ Erreur API, tentative localStorage...');
        // Fallback: chercher dans localStorage
        const allKeys = Object.keys(localStorage);
        const formativeKeys = allKeys.filter(key => key.startsWith('formativePreview_'));
        
        for (const key of formativeKeys) {
          try {
            const storedData = localStorage.getItem(key);
            if (storedData) {
              const parsed = JSON.parse(storedData);
              if (parsed.id && parsed.id.toString() === evaluationId) {
                setEvaluation(parsed);
                populateFormData(parsed);
                console.log('✅ Évaluation chargée depuis localStorage:', parsed);
                break;
              }
            }
          } catch (e) {
            console.error('Erreur parsing localStorage:', e);
          }
        }
        
        if (!evaluation) {
          setError('Évaluation non trouvée. Veuillez revenir à la liste.');
        }
      }
    } catch (err) {
      console.error('❌ Erreur lors du chargement:', err);
      setError('Erreur lors du chargement de l\'évaluation');
    } finally {
      setLoading(false);
    }
  };

  const populateFormData = (evaluation: FormativeEvaluation) => {
    setFormData({
      title: evaluation.title || '',
      description: evaluation.description || '',
      subject: evaluation.subject || '',
      target_level: evaluation.target_level || 'intermediate',
      duration_minutes: evaluation.duration_minutes || 60,
      max_students: evaluation.max_students || 30,
      learning_objectives: evaluation.learning_objectives && evaluation.learning_objectives.length > 0 
        ? evaluation.learning_objectives 
        : [''],
      is_active: evaluation.is_active !== undefined ? evaluation.is_active : true
    });

    if (evaluation.criteria && evaluation.criteria.length > 0) {
      setCriteria(evaluation.criteria);
    }

    if (evaluation.questions && evaluation.questions.length > 0) {
      setQuestions(evaluation.questions);
    }

    if (evaluation.instructions) {
      setInstructions(evaluation.instructions);
    }

    if (evaluation.success_indicators && evaluation.success_indicators.length > 0) {
      setSuccessIndicators(evaluation.success_indicators);
    }
  };

  const handleInputChange = (field: string, value: any) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  const handleArrayChange = (field: string, index: number, value: string) => {
    if (field === 'learning_objectives') {
      const newArray = [...formData.learning_objectives];
      newArray[index] = value;
      setFormData(prev => ({ ...prev, learning_objectives: newArray }));
    }
  };

  const addArrayItem = (field: string) => {
    if (field === 'learning_objectives') {
      setFormData(prev => ({ 
        ...prev, 
        learning_objectives: [...prev.learning_objectives, ''] 
      }));
    }
  };

  const removeArrayItem = (field: string, index: number) => {
    if (field === 'learning_objectives') {
      const newArray = formData.learning_objectives.filter((_, i) => i !== index);
      setFormData(prev => ({ ...prev, learning_objectives: newArray }));
    }
  };

  const handleCriteriaChange = (index: number, field: string, value: any) => {
    const newCriteria = [...criteria];
    newCriteria[index] = { ...newCriteria[index], [field]: value };
    setCriteria(newCriteria);
  };

  const addCriterion = () => {
    setCriteria([...criteria, {
      name: '',
      description: '',
      weight: 25,
      max_points: 4
    }]);
  };

  const removeCriterion = (index: number) => {
    setCriteria(criteria.filter((_, i) => i !== index));
  };

  const handleQuestionChange = (index: number, field: string, value: any) => {
    const newQuestions = [...questions];
    newQuestions[index] = { ...newQuestions[index], [field]: value };
    setQuestions(newQuestions);
  };

  const addQuestion = () => {
    setQuestions([...questions, {
      question: '',
      type: 'reflection',
      max_points: 5
    }]);
  };

  const removeQuestion = (index: number) => {
    setQuestions(questions.filter((_, i) => i !== index));
  };

  const handleSuccessIndicatorChange = (index: number, value: string) => {
    const newIndicators = [...successIndicators];
    newIndicators[index] = value;
    setSuccessIndicators(newIndicators);
  };

  const addSuccessIndicator = () => {
    setSuccessIndicators([...successIndicators, '']);
  };

  const removeSuccessIndicator = (index: number) => {
    setSuccessIndicators(successIndicators.filter((_, i) => i !== index));
  };

  const handleSave = async () => {
    try {
      setSaving(true);
      setError(null);
      setSuccess(null);

      if (!evaluation) {
        throw new Error('Aucune évaluation à sauvegarder');
      }

      // Préparer les données mises à jour
      const updatedEvaluation = {
        ...evaluation,
        title: formData.title,
        description: formData.description,
        subject: formData.subject,
        target_level: formData.target_level,
        duration_minutes: formData.duration_minutes,
        max_students: formData.max_students,
        learning_objectives: formData.learning_objectives.filter(obj => obj.trim() !== ''),
        is_active: formData.is_active,
        criteria: criteria.filter(c => c.name.trim() !== ''),
        questions: questions.filter(q => q.question.trim() !== ''),
        instructions: instructions,
        success_indicators: successIndicators.filter(ind => ind.trim() !== '')
      };

      // Sauvegarder via l'API
      await formativeEvaluationService.updateEvaluation(evaluation.id, updatedEvaluation);
      
      setSuccess('Évaluation mise à jour avec succès !');
      setEvaluation(updatedEvaluation);
      
      // Mettre à jour localStorage
      const previewId = `edit_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
      localStorage.setItem(`formativePreview_${previewId}`, JSON.stringify(updatedEvaluation));
      
      console.log('✅ Évaluation mise à jour:', updatedEvaluation);
      
    } catch (err) {
      console.error('❌ Erreur lors de la sauvegarde:', err);
      setError(err instanceof Error ? err.message : 'Erreur lors de la sauvegarde');
    } finally {
      setSaving(false);
    }
  };

  const handlePreview = () => {
    if (evaluation) {
      const previewId = `preview_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
      const previewData = {
        ...evaluation,
        title: formData.title,
        description: formData.description,
        subject: formData.subject,
        target_level: formData.target_level,
        duration_minutes: formData.duration_minutes,
        max_students: formData.max_students,
        learning_objectives: formData.learning_objectives.filter(obj => obj.trim() !== ''),
        criteria: criteria.filter(c => c.name.trim() !== ''),
        questions: questions.filter(q => q.question.trim() !== ''),
        instructions: instructions,
        success_indicators: successIndicators.filter(ind => ind.trim() !== '')
      };
      
      localStorage.setItem(`formativePreview_${previewId}`, JSON.stringify(previewData));
      window.open(`/dashboard/teacher/adaptive-evaluation/preview-formative?previewId=${previewId}`, '_blank');
    }
  };

  if (loading) {
    return (
      <div className="flex h-screen">
        <Sidebar />
        <div className="flex-1 flex items-center justify-center">
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-orange-600 mx-auto mb-4"></div>
            <p className="text-gray-600">Chargement de l'évaluation...</p>
          </div>
        </div>
      </div>
    );
  }

  if (error || !evaluation) {
    return (
      <div className="flex h-screen">
        <Sidebar />
        <div className="flex-1 flex items-center justify-center">
          <div className="text-center max-w-md">
            <div className="text-red-500 text-6xl mb-4">⚠️</div>
            <h2 className="text-xl font-semibold text-gray-800 mb-2">Erreur de chargement</h2>
            <p className="text-gray-600 mb-6">{error || 'Évaluation non trouvée'}</p>
            <Button onClick={() => window.history.back()} className="bg-orange-600 hover:bg-orange-700">
              <ArrowLeft className="w-4 h-4 mr-2" />
              Retour
            </Button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="flex h-screen">
      <Sidebar />
      <div className="flex-1 overflow-y-auto bg-gray-50">
        {/* Header */}
        <div className="bg-white border-b border-gray-200 px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <Button
                onClick={() => window.history.back()}
                variant="ghost"
                className="text-gray-600 hover:text-gray-800"
              >
                <ArrowLeft className="w-4 h-4 mr-2" />
                Retour
              </Button>
              <div>
                <h1 className="text-2xl font-bold text-gray-900">Modifier l'Évaluation</h1>
                <p className="text-gray-600">Modifiez les détails de votre évaluation formative</p>
              </div>
            </div>
            <div className="flex space-x-3">
              <Button
                onClick={handlePreview}
                variant="outline"
                className="border-orange-200 text-orange-600 hover:bg-orange-50"
              >
                <Eye className="w-4 h-4 mr-2" />
                Prévisualiser
              </Button>
              <Button
                onClick={handleSave}
                disabled={saving}
                className="bg-orange-600 hover:bg-orange-700 text-white"
              >
                <Save className="w-4 h-4 mr-2" />
                {saving ? 'Sauvegarde...' : 'Sauvegarder'}
              </Button>
            </div>
          </div>
        </div>

        {/* Messages */}
        {error && (
          <div className="mx-6 mt-4 p-4 bg-red-50 border border-red-200 rounded-lg">
            <p className="text-red-700">{error}</p>
          </div>
        )}

        {success && (
          <div className="mx-6 mt-4 p-4 bg-green-50 border border-green-200 rounded-lg">
            <p className="text-green-700">{success}</p>
          </div>
        )}

        {/* Formulaire principal */}
        <div className="p-6 max-w-4xl mx-auto space-y-6">
          {/* Informations de base */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center">
                <BookOpen className="w-5 h-5 mr-2 text-blue-600" />
                Informations de base
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <Label htmlFor="title">Titre *</Label>
                  <Input
                    id="title"
                    value={formData.title}
                    onChange={(e) => handleInputChange('title', e.target.value)}
                    placeholder="Titre de l'évaluation"
                  />
                </div>
                <div>
                  <Label htmlFor="subject">Matière *</Label>
                  <Input
                    id="subject"
                    value={formData.subject}
                    onChange={(e) => handleInputChange('subject', e.target.value)}
                    placeholder="Ex: Mathématiques"
                  />
                </div>
              </div>

              <div>
                <Label htmlFor="description">Description</Label>
                <Textarea
                  id="description"
                  value={formData.description}
                  onChange={(e) => handleInputChange('description', e.target.value)}
                  placeholder="Description détaillée de l'évaluation"
                  rows={3}
                />
              </div>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div>
                  <Label htmlFor="target_level">Niveau cible</Label>
                  <Select
                    value={formData.target_level}
                    onValueChange={(value) => handleInputChange('target_level', value)}
                  >
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="beginner">Débutant</SelectItem>
                      <SelectItem value="intermediate">Intermédiaire</SelectItem>
                      <SelectItem value="advanced">Avancé</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
                <div>
                  <Label htmlFor="duration_minutes">Durée (minutes)</Label>
                  <Input
                    id="duration_minutes"
                    type="number"
                    value={formData.duration_minutes}
                    onChange={(e) => handleInputChange('duration_minutes', parseInt(e.target.value) || 60)}
                    min="15"
                    max="300"
                  />
                </div>
                <div>
                  <Label htmlFor="max_students">Étudiants max</Label>
                  <Input
                    id="max_students"
                    type="number"
                    value={formData.max_students}
                    onChange={(e) => handleInputChange('max_students', parseInt(e.target.value) || 30)}
                    min="1"
                    max="100"
                  />
                </div>
              </div>

              <div>
                <Label>Objectifs d'apprentissage</Label>
                <div className="space-y-2">
                  {formData.learning_objectives.map((objective, index) => (
                    <div key={index} className="flex space-x-2">
                      <Input
                        value={objective}
                        onChange={(e) => handleArrayChange('learning_objectives', index, e.target.value)}
                        placeholder={`Objectif ${index + 1}`}
                      />
                      <Button
                        type="button"
                        variant="outline"
                        size="sm"
                        onClick={() => removeArrayItem('learning_objectives', index)}
                        className="text-red-600 border-red-200 hover:bg-red-50"
                      >
                        <Trash2 className="w-4 h-4" />
                      </Button>
                    </div>
                  ))}
                  <Button
                    type="button"
                    variant="outline"
                    onClick={() => addArrayItem('learning_objectives')}
                    className="w-full border-dashed border-gray-300 text-gray-600 hover:border-gray-400"
                  >
                    <Plus className="w-4 h-4 mr-2" />
                    Ajouter un objectif
                  </Button>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Critères d'évaluation */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center">
                <Target className="w-5 h-5 mr-2 text-purple-600" />
                Critères d'évaluation
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {criteria.map((criterion, index) => (
                  <div key={index} className="border rounded-lg p-4 bg-gray-50">
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <div>
                        <Label>Nom du critère</Label>
                        <Input
                          value={criterion.name}
                          onChange={(e) => handleCriteriaChange(index, 'name', e.target.value)}
                          placeholder="Ex: Qualité de la recherche"
                        />
                      </div>
                      <div>
                        <Label>Description</Label>
                        <Input
                          value={criterion.description}
                          onChange={(e) => handleCriteriaChange(index, 'description', e.target.value)}
                          placeholder="Description du critère"
                        />
                      </div>
                      <div>
                        <Label>Poids (%)</Label>
                        <Input
                          type="number"
                          value={criterion.weight}
                          onChange={(e) => handleCriteriaChange(index, 'weight', parseInt(e.target.value) || 25)}
                          min="1"
                          max="100"
                        />
                      </div>
                      <div>
                        <Label>Points max</Label>
                        <Input
                          type="number"
                          value={criterion.max_points}
                          onChange={(e) => handleCriteriaChange(index, 'max_points', parseInt(e.target.value) || 4)}
                          min="1"
                          max="10"
                        />
                      </div>
                    </div>
                    <div className="mt-3 flex justify-end">
                      <Button
                        type="button"
                        variant="outline"
                        size="sm"
                        onClick={() => removeCriterion(index)}
                        className="text-red-600 border-red-200 hover:bg-red-50"
                      >
                        <Trash2 className="w-4 h-4 mr-2" />
                        Supprimer
                      </Button>
                    </div>
                  </div>
                ))}
                <Button
                  type="button"
                  variant="outline"
                  onClick={addCriterion}
                  className="w-full border-dashed border-gray-300 text-gray-600 hover:border-gray-400"
                >
                  <Plus className="w-4 h-4 mr-2" />
                  Ajouter un critère
                </Button>
              </div>
            </CardContent>
          </Card>

          {/* Questions */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center">
                <BookOpen className="w-5 h-5 mr-2 text-orange-600" />
                Questions
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {questions.map((question, index) => (
                  <div key={index} className="border rounded-lg p-4 bg-gray-50">
                    <div className="space-y-4">
                      <div>
                        <Label>Question {index + 1}</Label>
                        <Textarea
                          value={question.question}
                          onChange={(e) => handleQuestionChange(index, 'question', e.target.value)}
                          placeholder="Tapez votre question ici..."
                          rows={2}
                        />
                      </div>
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div>
                          <Label>Type de question</Label>
                          <Select
                            value={question.type}
                            onValueChange={(value) => handleQuestionChange(index, 'type', value)}
                          >
                            <SelectTrigger>
                              <SelectValue />
                            </SelectTrigger>
                            <SelectContent>
                              <SelectItem value="reflection">Réflexion</SelectItem>
                              <SelectItem value="methodology">Méthodologie</SelectItem>
                              <SelectItem value="analysis">Analyse</SelectItem>
                              <SelectItem value="evaluation">Évaluation</SelectItem>
                            </SelectContent>
                          </Select>
                        </div>
                        <div>
                          <Label>Points max</Label>
                          <Input
                            type="number"
                            value={question.max_points}
                            onChange={(e) => handleQuestionChange(index, 'max_points', parseInt(e.target.value) || 5)}
                            min="1"
                            max="20"
                          />
                        </div>
                      </div>
                    </div>
                    <div className="mt-3 flex justify-end">
                      <Button
                        type="button"
                        variant="outline"
                        size="sm"
                        onClick={() => removeQuestion(index)}
                        className="text-red-600 border-red-200 hover:bg-red-50"
                      >
                        <Trash2 className="w-4 h-4 mr-2" />
                        Supprimer
                      </Button>
                    </div>
                  </div>
                ))}
                <Button
                  type="button"
                  variant="outline"
                  onClick={addQuestion}
                  className="w-full border-dashed border-gray-300 text-gray-600 hover:border-gray-400"
                >
                  <Plus className="w-4 h-4 mr-2" />
                  Ajouter une question
                </Button>
              </div>
            </CardContent>
          </Card>

                     {/* Instructions */}
           <Card>
             <CardHeader>
               <CardTitle className="flex items-center">
                 <CheckCircle className="w-5 h-5 mr-2 text-green-600" />
                 Instructions
               </CardTitle>
             </CardHeader>
             <CardContent>
               <Textarea
                 value={instructions}
                 onChange={(e) => setInstructions(e.target.value)}
                 placeholder="Instructions détaillées pour les étudiants..."
                 rows={4}
               />
             </CardContent>
           </Card>

                     {/* Indicateurs de succès */}
           <Card>
             <CardHeader>
               <CardTitle className="flex items-center">
                 <CheckCircle className="w-5 h-5 mr-2 text-green-600" />
                 Indicateurs de succès
               </CardTitle>
             </CardHeader>
             <CardContent>
               <div className="space-y-2">
                 {successIndicators.map((indicator, index) => (
                   <div key={index} className="flex space-x-2">
                     <Input
                       value={indicator}
                       onChange={(e) => handleSuccessIndicatorChange(index, e.target.value)}
                       placeholder={`Indicateur ${index + 1}`}
                     />
                     <Button
                       type="button"
                       variant="outline"
                       size="sm"
                       onClick={() => removeSuccessIndicator(index)}
                       className="text-red-600 border-red-200 hover:bg-red-50"
                     >
                       <Trash2 className="w-4 h-4" />
                     </Button>
                   </div>
                 ))}
                 <Button
                   type="button"
                   variant="outline"
                   onClick={addSuccessIndicator}
                   className="w-full border-dashed border-gray-300 text-gray-600 hover:border-gray-400"
                 >
                   <Plus className="w-4 h-4 mr-2" />
                   Ajouter un indicateur
                 </Button>
               </div>
             </CardContent>
           </Card>

          {/* Boutons d'action */}
          <div className="flex justify-end space-x-4 pt-6 border-t">
            <Button
              onClick={handlePreview}
              variant="outline"
              className="border-orange-200 text-orange-600 hover:bg-orange-50"
            >
              <Eye className="w-4 h-4 mr-2" />
              Prévisualiser
            </Button>
            <Button
              onClick={handleSave}
              disabled={saving}
              className="bg-orange-600 hover:bg-orange-700 text-white"
            >
              <Save className="w-4 h-4 mr-2" />
              {saving ? 'Sauvegarde...' : 'Sauvegarder'}
            </Button>
          </div>
        </div>
      </div>
    </div>
  );
}

export default function EditAssessment() {
  return (
    <Suspense fallback={<div>Loading...</div>}>
      <EditAssessmentContent />
    </Suspense>
  );
}
