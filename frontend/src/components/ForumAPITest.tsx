'use client';

import React, { useState, useEffect } from 'react';
import { forumAPI } from '../api/student/forum';

export default function ForumAPITest() {
  const [testResult, setTestResult] = useState<string>('');
  const [loading, setLoading] = useState(false);

  const testAPI = async () => {
    setLoading(true);
    setTestResult('');

    try {
      // Test 0: Vérifier l'authentification
      console.log('🔍 Test 0: Vérification de l\'authentification');
      const token = localStorage.getItem('najah_token');
      console.log('Token présent:', !!token);
      if (token) {
        console.log('Token (premiers caractères):', token.substring(0, 20) + '...');
      } else {
        throw new Error('Aucun token d\'authentification trouvé. Veuillez vous connecter.');
      }
      
      // Test 1: Vérifier l'objet API
      console.log('🔍 Test 1: Vérification de l\'objet API');
      console.log('forumAPI object:', forumAPI);
      console.log('forumAPI.getCategories:', forumAPI.getCategories);
      
      // Test 2: Vérifier la configuration
      console.log('🔍 Test 2: Vérification de la configuration');
      const config = await import('../api/config');
      console.log('API_BASE_URL:', config.API_BASE_URL);
      
      // Test 3: Tester l'appel API
      console.log('🔍 Test 3: Test de l\'appel API');
      const categories = await forumAPI.getCategories();
      console.log('✅ Categories récupérées:', categories);
      
      setTestResult(`✅ Test réussi! ${categories.length} catégories récupérées`);
      
    } catch (error) {
      console.error('❌ Erreur lors du test:', error);
      setTestResult(`❌ Erreur: ${error instanceof Error ? error.message : String(error)}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-4 border rounded-lg bg-gray-50">
      <h3 className="text-lg font-semibold mb-4">🧪 Test de l'API Forum</h3>
      
      <button
        onClick={testAPI}
        disabled={loading}
        className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 disabled:opacity-50"
      >
        {loading ? 'Test en cours...' : 'Tester l\'API'}
      </button>
      
      {testResult && (
        <div className="mt-4 p-3 rounded bg-gray-100">
          <pre className="text-sm">{testResult}</pre>
        </div>
      )}
      
      <div className="mt-4 text-sm text-gray-600">
        <p>Ouvrez la console du navigateur pour voir les logs détaillés.</p>
      </div>
    </div>
  );
}
