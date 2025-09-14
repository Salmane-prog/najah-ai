#!/usr/bin/env python3
"""
Test d'import du module progress_tracking
"""

try:
    from api.v1 import progress_tracking
    print("✅ Import progress_tracking réussi!")
    print(f"Router: {progress_tracking.router}")
    print(f"Tags: {progress_tracking.router.tags}")
except ImportError as e:
    print(f"❌ Erreur d'import: {e}")
except Exception as e:
    print(f"❌ Erreur inattendue: {e}")
