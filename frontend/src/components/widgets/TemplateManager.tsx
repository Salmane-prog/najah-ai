'use client';

import React, { useState, useEffect } from 'react';
import { useAuth  } from '../../hooks/useAuth';
import { 
  FileText, 
  Plus, 
  Edit, 
  Trash2, 
  Copy, 
  Download, 
  Upload,
  Palette,
  Type,
  Layout,
  Save,
  Eye
} from 'lucide-react';

interface Template {
  id: number;
  name: string;
  description: string;
  category: 'quiz' | 'content' | 'assessment' | 'report' | 'presentation';
  content: any;
  variables: string[];
  is_public: boolean;
  created_by: number;
  created_at: string;
  updated_at: string;
}

interface TemplateVariable {
  name: string;
  type: 'text' | 'number' | 'date' | 'select' | 'boolean';
  label: string;
  required: boolean;
  default_value?: any;
  options?: string[];
}

export default function TemplateManager() {
  const { user, token } = useAuth();
  const [templates, setTemplates] = useState<Template[]>([]);
  const [selectedTemplate, setSelectedTemplate] = useState<Template | null>(null);
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [showEditModal, setShowEditModal] = useState(false);
  const [showPreviewModal, setShowPreviewModal] = useState(false);
  const [loading, setLoading] = useState(true);
  const [activeCategory, setActiveCategory] = useState<string>('all');

  // Formulaires
  const [templateForm, setTemplateForm] = useState({
    name: '',
    description: '',
    category: 'quiz' as const,
    content: '',
    variables: [] as TemplateVariable[],
    is_public: false
  });

  const [previewData, setPreviewData] = useState<Record<string, any>>({});

  useEffect(() => {
    if (token) {
      fetchTemplates();
    }
  }, [token]);

  const fetchTemplates = async () => {
    try {
      setLoading(true);
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/v1/templates/`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      
      if (response.ok) {
        const data = await response.json();
        setTemplates(data.templates || []);
      }
    } catch (err) {
      console.error('Erreur lors du chargement des templates:', err);
    } finally {
      setLoading(false);
    }
  };

  const createTemplate = async () => {
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/v1/templates/`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(templateForm)
      });

      if (response.ok) {
        setShowCreateModal(false);
        setTemplateForm({
          name: '',
          description: '',
          category: 'quiz',
          content: '',
          variables: [],
          is_public: false
        });
        fetchTemplates();
      }
    } catch (err) {
      console.error('Erreur lors de la création du template:', err);
    }
  };

  const updateTemplate = async () => {
    if (!selectedTemplate) return;

    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/v1/templates/${selectedTemplate.id}`, {
        method: 'PUT',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(templateForm)
      });

      if (response.ok) {
        setShowEditModal(false);
        setSelectedTemplate(null);
        fetchTemplates();
      }
    } catch (err) {
      console.error('Erreur lors de la mise à jour du template:', err);
    }
  };

  const deleteTemplate = async (templateId: number) => {
    if (!confirm('Êtes-vous sûr de vouloir supprimer ce template ?')) return;

    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/v1/templates/${templateId}`, {
        method: 'DELETE',
        headers: { 'Authorization': `Bearer ${token}` }
      });

      if (response.ok) {
        fetchTemplates();
      }
    } catch (err) {
      console.error('Erreur lors de la suppression du template:', err);
    }
  };

  const duplicateTemplate = async (template: Template) => {
    try {
      const duplicateData = {
        ...template,
        name: `${template.name} (Copie)`,
        is_public: false
      };
      delete duplicateData.id;
      delete duplicateData.created_at;
      delete duplicateData.updated_at;

      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/api/v1/templates/`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(duplicateData)
      });

      if (response.ok) {
        fetchTemplates();
      }
    } catch (err) {
      console.error('Erreur lors de la duplication du template:', err);
    }
  };

  const exportTemplate = async (template: Template) => {
    try {
      const dataStr = JSON.stringify(template, null, 2);
      const dataBlob = new Blob([dataStr], { type: 'application/json' });
      const url = URL.createObjectURL(dataBlob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `${template.name.replace(/\s+/g, '_')}.json`;
      link.click();
      URL.revokeObjectURL(url);
    } catch (err) {
      console.error('Erreur lors de l\'export du template:', err);
    }
  };

  const addVariable = () => {
    setTemplateForm(prev => ({
      ...prev,
      variables: [...prev.variables, {
        name: '',
        type: 'text',
        label: '',
        required: false
      }]
    }));
  };

  const updateVariable = (index: number, field: keyof TemplateVariable, value: any) => {
    setTemplateForm(prev => ({
      ...prev,
      variables: prev.variables.map((v, i) => 
        i === index ? { ...v, [field]: value } : v
      )
    }));
  };

  const removeVariable = (index: number) => {
    setTemplateForm(prev => ({
      ...prev,
      variables: prev.variables.filter((_, i) => i !== index)
    }));
  };

  const getCategoryIcon = (category: string) => {
    switch (category) {
      case 'quiz': return <FileText size={16} />;
      case 'content': return <Type size={16} />;
      case 'assessment': return <Layout size={16} />;
      case 'report': return <FileText size={16} />;
      case 'presentation': return <Layout size={16} />;
      default: return <FileText size={16} />;
    }
  };

  const getCategoryColor = (category: string) => {
    switch (category) {
      case 'quiz': return 'bg-blue-100 text-blue-800';
      case 'content': return 'bg-green-100 text-green-800';
      case 'assessment': return 'bg-purple-100 text-purple-800';
      case 'report': return 'bg-orange-100 text-orange-800';
      case 'presentation': return 'bg-pink-100 text-pink-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const filteredTemplates = templates.filter(template => 
    activeCategory === 'all' || template.category === activeCategory
  );

  if (loading) {
    return (
      <div className="bg-white rounded-xl shadow-lg p-6">
        <div className="flex items-center justify-center h-64">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-xl shadow-lg p-6">
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center gap-2">
          <FileText className="text-blue-600" size={24} />
          <h2 className="text-xl font-bold text-gray-800">Gestionnaire de Templates</h2>
        </div>
        <button
          onClick={() => setShowCreateModal(true)}
          className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition"
        >
          <Plus size={16} />
          Nouveau Template
        </button>
      </div>

      {/* Filtres par catégorie */}
      <div className="flex space-x-2 mb-6 overflow-x-auto">
        {[
          { id: 'all', label: 'Tous', icon: <FileText size={16} /> },
          { id: 'quiz', label: 'Quiz', icon: <FileText size={16} /> },
          { id: 'content', label: 'Contenu', icon: <Type size={16} /> },
          { id: 'assessment', label: 'Évaluation', icon: <Layout size={16} /> },
          { id: 'report', label: 'Rapport', icon: <FileText size={16} /> },
          { id: 'presentation', label: 'Présentation', icon: <Layout size={16} /> }
        ].map((category) => (
          <button
            key={category.id}
            onClick={() => setActiveCategory(category.id)}
            className={`flex items-center gap-2 px-3 py-2 rounded-lg font-medium transition whitespace-nowrap ${
              activeCategory === category.id
                ? 'bg-blue-100 text-blue-700'
                : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
            }`}
          >
            {category.icon}
            {category.label}
          </button>
        ))}
      </div>

      {/* Liste des templates */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {filteredTemplates.map((template) => (
          <div key={template.id} className="border rounded-lg p-4 hover:shadow-md transition">
            <div className="flex items-start justify-between mb-3">
              <div className="flex items-center gap-2">
                {getCategoryIcon(template.category)}
                <span className={`px-2 py-1 rounded-full text-xs font-medium ${getCategoryColor(template.category)}`}>
                  {template.category}
                </span>
              </div>
              <div className="flex gap-1">
                <button
                  onClick={() => {
                    setSelectedTemplate(template);
                    setTemplateForm({
                      name: template.name,
                      description: template.description,
                      category: template.category,
                      content: template.content,
                      variables: template.variables,
                      is_public: template.is_public
                    });
                    setShowPreviewModal(true);
                  }}
                  className="p-1 text-gray-400 hover:text-blue-600"
                  title="Aperçu"
                >
                  <Eye size={14} />
                </button>
                <button
                  onClick={() => duplicateTemplate(template)}
                  className="p-1 text-gray-400 hover:text-green-600"
                  title="Dupliquer"
                >
                  <Copy size={14} />
                </button>
                <button
                  onClick={() => exportTemplate(template)}
                  className="p-1 text-gray-400 hover:text-purple-600"
                  title="Exporter"
                >
                  <Download size={14} />
                </button>
                <button
                  onClick={() => {
                    setSelectedTemplate(template);
                    setTemplateForm({
                      name: template.name,
                      description: template.description,
                      category: template.category,
                      content: template.content,
                      variables: template.variables,
                      is_public: template.is_public
                    });
                    setShowEditModal(true);
                  }}
                  className="p-1 text-gray-400 hover:text-yellow-600"
                  title="Modifier"
                >
                  <Edit size={14} />
                </button>
                <button
                  onClick={() => deleteTemplate(template.id)}
                  className="p-1 text-gray-400 hover:text-red-600"
                  title="Supprimer"
                >
                  <Trash2 size={14} />
                </button>
              </div>
            </div>
            
            <h3 className="font-semibold text-gray-800 mb-2">{template.name}</h3>
            <p className="text-sm text-gray-600 mb-3">{template.description}</p>
            
            <div className="flex items-center justify-between text-xs text-gray-500">
              <span>{template.variables.length} variables</span>
              <span>{template.is_public ? 'Public' : 'Privé'}</span>
            </div>
          </div>
        ))}
      </div>

      {filteredTemplates.length === 0 && (
        <div className="text-center py-12">
          <FileText className="mx-auto text-gray-400 mb-4" size={48} />
          <p className="text-gray-600">Aucun template trouvé</p>
          <p className="text-sm text-gray-500">Créez votre premier template pour commencer</p>
        </div>
      )}

      {/* Modal de création/édition */}
      {(showCreateModal || showEditModal) && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 w-full max-w-2xl max-h-[90vh] overflow-y-auto">
            <h2 className="text-xl font-bold mb-4">
              {showCreateModal ? 'Nouveau Template' : 'Modifier Template'}
            </h2>
            
            <form onSubmit={(e) => { e.preventDefault(); showCreateModal ? createTemplate() : updateTemplate(); }}>
              <div className="space-y-4">
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Nom</label>
                    <input
                      type="text"
                      value={templateForm.name}
                      onChange={(e) => setTemplateForm({...templateForm, name: e.target.value})}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                      required
                    />
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Catégorie</label>
                    <select
                      value={templateForm.category}
                      onChange={(e) => setTemplateForm({...templateForm, category: e.target.value as any})}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    >
                      <option value="quiz">Quiz</option>
                      <option value="content">Contenu</option>
                      <option value="assessment">Évaluation</option>
                      <option value="report">Rapport</option>
                      <option value="presentation">Présentation</option>
                    </select>
                  </div>
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Description</label>
                  <textarea
                    value={templateForm.description}
                    onChange={(e) => setTemplateForm({...templateForm, description: e.target.value})}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    rows={3}
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Contenu du template</label>
                  <textarea
                    value={templateForm.content}
                    onChange={(e) => setTemplateForm({...templateForm, content: e.target.value})}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    rows={6}
                    placeholder="Contenu du template avec variables {{variable_name}}"
                  />
                </div>
                
                <div>
                  <div className="flex items-center justify-between mb-2">
                    <label className="block text-sm font-medium text-gray-700">Variables</label>
                    <button
                      type="button"
                      onClick={addVariable}
                      className="text-sm text-blue-600 hover:text-blue-800"
                    >
                      + Ajouter variable
                    </button>
                  </div>
                  
                  <div className="space-y-2">
                    {templateForm.variables.map((variable, index) => (
                      <div key={index} className="flex items-center gap-2 p-2 border rounded">
                        <input
                          type="text"
                          placeholder="Nom"
                          value={variable.name}
                          onChange={(e) => updateVariable(index, 'name', e.target.value)}
                          className="flex-1 px-2 py-1 border border-gray-300 rounded text-sm"
                        />
                        <input
                          type="text"
                          placeholder="Label"
                          value={variable.label}
                          onChange={(e) => updateVariable(index, 'label', e.target.value)}
                          className="flex-1 px-2 py-1 border border-gray-300 rounded text-sm"
                        />
                        <select
                          value={variable.type}
                          onChange={(e) => updateVariable(index, 'type', e.target.value)}
                          className="px-2 py-1 border border-gray-300 rounded text-sm"
                        >
                          <option value="text">Texte</option>
                          <option value="number">Nombre</option>
                          <option value="date">Date</option>
                          <option value="select">Sélection</option>
                          <option value="boolean">Booléen</option>
                        </select>
                        <input
                          type="checkbox"
                          checked={variable.required}
                          onChange={(e) => updateVariable(index, 'required', e.target.checked)}
                          className="rounded"
                        />
                        <button
                          type="button"
                          onClick={() => removeVariable(index)}
                          className="p-1 text-red-600 hover:text-red-800"
                        >
                          <Trash2 size={14} />
                        </button>
                      </div>
                    ))}
                  </div>
                </div>
                
                <div className="flex items-center gap-2">
                  <input
                    type="checkbox"
                    id="is_public"
                    checked={templateForm.is_public}
                    onChange={(e) => setTemplateForm({...templateForm, is_public: e.target.checked})}
                    className="rounded"
                  />
                  <label htmlFor="is_public" className="text-sm text-gray-700">
                    Template public (visible par tous les utilisateurs)
                  </label>
                </div>
              </div>
              
              <div className="flex gap-3 mt-6">
                <button
                  type="button"
                  onClick={() => {
                    setShowCreateModal(false);
                    setShowEditModal(false);
                    setSelectedTemplate(null);
                  }}
                  className="flex-1 px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50"
                >
                  Annuler
                </button>
                <button
                  type="submit"
                  className="flex-1 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
                >
                  {showCreateModal ? 'Créer' : 'Mettre à jour'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Modal d'aperçu */}
      {showPreviewModal && selectedTemplate && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 w-full max-w-2xl max-h-[90vh] overflow-y-auto">
            <h2 className="text-xl font-bold mb-4">Aperçu du Template</h2>
            
            <div className="space-y-4">
              <div>
                <h3 className="font-semibold text-gray-800 mb-2">{selectedTemplate.name}</h3>
                <p className="text-sm text-gray-600">{selectedTemplate.description}</p>
              </div>
              
              <div>
                <h4 className="font-medium text-gray-800 mb-2">Variables requises:</h4>
                <div className="grid grid-cols-2 gap-2">
                  {selectedTemplate.variables.map((variable, index) => (
                    <div key={index} className="p-2 border rounded">
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        {variable.label}
                      </label>
                      <input
                        type={variable.type === 'number' ? 'number' : 'text'}
                        placeholder={`Entrez ${variable.label.toLowerCase()}`}
                        value={previewData[variable.name] || ''}
                        onChange={(e) => setPreviewData({
                          ...previewData,
                          [variable.name]: e.target.value
                        })}
                        className="w-full px-2 py-1 border border-gray-300 rounded text-sm"
                        required={variable.required}
                      />
                    </div>
                  ))}
                </div>
              </div>
              
              <div>
                <h4 className="font-medium text-gray-800 mb-2">Aperçu:</h4>
                <div className="p-4 border rounded bg-gray-50">
                  <pre className="text-sm text-gray-800 whitespace-pre-wrap">
                    {selectedTemplate.content}
                  </pre>
                </div>
              </div>
            </div>
            
            <div className="flex gap-3 mt-6">
              <button
                onClick={() => setShowPreviewModal(false)}
                className="flex-1 px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50"
              >
                Fermer
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
} 