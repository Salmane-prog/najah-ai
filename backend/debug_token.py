#!/usr/bin/env python3
"""
Script pour décoder et vérifier le token JWT
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.security import decode_access_token
from core.config import settings
from jose import jwt, JWTError

# Token de l'utilisateur (copié depuis les logs)
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJoYWpvdWppczQ3QGdtYWlsLmNvbSIsInJvbGUiOiJzdHVkZW50IiwiZXhwIjoxNzUzMjkwODkwfQ.GRJUO_bCrQOY86Fljp6qxT8VF9e3_Yn2SJcZ_i6xL_s"

print("=== DEBUG TOKEN JWT ===")

print(f"Token: {token}")
print(f"Secret Key: {settings.SECRET_KEY}")
print(f"Algorithm: {settings.ALGORITHM}")

# Test direct avec jose
try:
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    print(f"\n✅ Token décodé avec succès!")
    print(f"Payload: {payload}")
    print(f"Subject (email): {payload.get('sub')}")
    print(f"Role: {payload.get('role')}")
    print(f"Exp: {payload.get('exp')}")
except JWTError as e:
    print(f"\n❌ Erreur JWT: {e}")
except Exception as e:
    print(f"\n❌ Erreur générale: {e}")

# Test avec notre fonction
payload = decode_access_token(token)
if payload:
    print(f"\n✅ Token valide avec notre fonction!")
    print(f"Payload: {payload}")
else:
    print(f"\n❌ Token invalide avec notre fonction!")

print("\n✅ Debug terminé") 