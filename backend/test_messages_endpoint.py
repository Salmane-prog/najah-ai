#!/usr/bin/env python3
"""
Script pour tester l'endpoint messages
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_messages_endpoint():
    print("=== TEST DE L'ENDPOINT MESSAGES ===")
    
    try:
        from fastapi import FastAPI
        from fastapi.middleware.cors import CORSMiddleware
        from api.v1 import messages
        from core.database import SessionLocal
        from models.message import Message
        from models.user import User
        
        # Créer l'app FastAPI
        app = FastAPI()
        
        # Ajouter les routes messages
        app.include_router(messages.router, prefix="/api/v1/messages", tags=["messages"])
        
        print("✅ Application créée")
        print("✅ Routes messages incluses")
        
        # Tester la base de données
        db = SessionLocal()
        try:
            print("\n🔍 Test de la base de données...")
            
            # Test User
            users = db.query(User).all()
            print(f"✅ Users trouvés: {len(users)}")
            
            # Test Message
            messages_db = db.query(Message).all()
            print(f"✅ Messages trouvés: {len(messages_db)}")
            
            # Test spécifique pour user_id = 5
            user_messages = db.query(Message).filter(Message.user_id == 5).all()
            print(f"✅ Messages pour user_id=5: {len(user_messages)}")
            
        except Exception as e:
            print(f"❌ Erreur base de données: {e}")
            import traceback
            traceback.print_exc()
        finally:
            db.close()
        
        print("\n✅ Test terminé")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_messages_endpoint() 