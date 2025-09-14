from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from fastapi.responses import HTMLResponse
from typing import Dict
from jose import jwt, JWTError
from core.config import settings
import json as JSON

router = APIRouter()

active_connections: Dict[int, WebSocket] = {}

async def get_current_user_id_from_token(token: str) -> int:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email = payload.get("sub")
        # Retourner l'email au lieu de user_id pour l'instant
        return email
    except (JWTError, Exception) as e:
        print(f"[WEBSOCKET] Erreur décodage token: {e}")
        return None

@router.websocket("/ws/notifications/")
async def websocket_notifications(websocket: WebSocket):
    await websocket.accept()
    user_email = None
    try:
        token = websocket.query_params.get("token")
        if not token:
            print("[WEBSOCKET] Token manquant")
            await websocket.close(code=1008)
            return
            
        user_email = await get_current_user_id_from_token(token)
        if not user_email:
            print("[WEBSOCKET] Token invalide")
            await websocket.close(code=1008)
            return
            
        print(f"[WEBSOCKET] Connexion acceptée pour: {user_email}")
        active_connections[user_email] = websocket
        
        # Envoyer un message de confirmation
        await websocket.send_text(JSON.dumps({
            "type": "connection_established",
            "message": "WebSocket connecté avec succès"
        }))
        
        while True:
            data = await websocket.receive_text()
            print(f"[WEBSOCKET] Message reçu: {data}")
            # Ici, on pourrait traiter des commandes du client si besoin
            
    except WebSocketDisconnect:
        print(f"[WEBSOCKET] Déconnexion: {user_email}")
        if user_email and user_email in active_connections:
            del active_connections[user_email]
    except Exception as e:
        print(f"[WEBSOCKET] Erreur: {e}")
        if user_email and user_email in active_connections:
            del active_connections[user_email]
        await websocket.close()

# Fonction utilitaire pour envoyer une notification à un utilisateur
async def send_notification(user_id: int, message: str):
    ws = active_connections.get(user_id)
    if ws:
        await ws.send_text(message) 