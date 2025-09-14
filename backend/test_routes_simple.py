#!/usr/bin/env python3
"""
Script de test simple pour vérifier les routes assessment
"""

from fastapi import FastAPI
from fastapi.testclient import TestClient
from fastapi.middleware.cors import CORSMiddleware
import sys
import os

# Ajouter le répertoire parent au path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Créer l'app FastAPI
app = FastAPI(title="Najah AI API", version="1.0.0")

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Importer les routes assessment
from api.v1 import assessment
app.include_router(assessment.router, prefix="/api/v1", tags=["assessment"])

print("=== TEST ROUTES SIMPLE ===")

# Créer un client de test
client = TestClient(app)

# Lister toutes les routes
print("\n📋 Routes disponibles:")
for route in app.routes:
    if hasattr(route, 'methods') and hasattr(route, 'path'):
        print(f"  - {route.methods} {route.path}")

# Tester l'endpoint de test
print("\n🧪 Test endpoint simple:")
try:
    response = client.get("/api/v1/assessment/test")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
except Exception as e:
    print(f"Erreur: {e}")

# Tester l'endpoint principal
print("\n🧪 Test endpoint principal:")
try:
    response = client.get("/api/v1/assessment/student/5/start")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Erreur: {e}")

print("\n✅ Test terminé") 