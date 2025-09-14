#!/usr/bin/env python3

"""
Script alternatif pour démarrer le serveur FastAPI sur le port 8001
"""

import uvicorn
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    print("🚀 Démarrage du serveur FastAPI sur le port 8001...")
    print("📡 URL: http://localhost:8001")
    print("📚 Documentation: http://localhost:8001/docs")
    print("🔧 Port alternatif pour éviter les conflits")
    
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8001,  # Port alternatif
        reload=True,
        log_level="info"
    )
