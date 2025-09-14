from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional
import requests
import json
import os
from datetime import datetime, timedelta

from core.database import get_db
from api.v1.users import get_current_user
from api.v1.auth import require_role
from models.user import User

router = APIRouter()

class ExternalIntegrations:
    """Classe pour gérer les intégrations externes"""
    
    def __init__(self):
        # Configuration des APIs externes (dans un vrai système, ces clés seraient dans des variables d'environnement)
        self.youtube_api_key = os.getenv("YOUTUBE_API_KEY", "demo_key")
        self.openweather_api_key = os.getenv("OPENWEATHER_API_KEY", "demo_key")
        self.news_api_key = os.getenv("NEWS_API_KEY", "demo_key")
        self.translate_api_key = os.getenv("TRANSLATE_API_KEY", "demo_key")
    
    def search_educational_videos(self, query: str, subject: str = None, max_results: int = 10) -> List[Dict]:
        """Rechercher des vidéos éducatives sur YouTube"""
        try:
            # Simulation de recherche YouTube (dans un vrai système, utiliser l'API YouTube)
            search_query = f"{query} {subject or ''} éducation cours"
            
            # Données simulées
            videos = [
                {
                    "id": f"video_{i}",
                    "title": f"Tutoriel {query} - {subject or 'Général'}",
                    "description": f"Vidéo éducative sur {query} pour les étudiants",
                    "thumbnail": f"https://img.youtube.com/vi/demo{i}/maxresdefault.jpg",
                    "duration": f"{15 + i * 5} minutes",
                    "views": 1000 + i * 500,
                    "rating": 4.5 - i * 0.1,
                    "url": f"https://www.youtube.com/watch?v=demo{i}",
                    "channel": f"Canal Éducatif {i}",
                    "published_date": (datetime.now() - timedelta(days=i*30)).isoformat()
                }
                for i in range(1, max_results + 1)
            ]
            
            return videos
            
        except Exception as e:
            return [{"error": f"Erreur lors de la recherche: {str(e)}"}]
    
    def get_weather_forecast(self, city: str = "Paris") -> Dict[str, Any]:
        """Obtenir les prévisions météo (pour planifier les activités extérieures)"""
        try:
            # Simulation de données météo
            weather_data = {
                "city": city,
                "current": {
                    "temperature": 22,
                    "description": "Ensoleillé",
                    "humidity": 65,
                    "wind_speed": 12
                },
                "forecast": [
                    {
                        "date": (datetime.now() + timedelta(days=i)).strftime("%Y-%m-%d"),
                        "temperature": 20 + i,
                        "description": "Ensoleillé" if i % 2 == 0 else "Nuageux",
                        "precipitation": 0 if i % 2 == 0 else 30
                    }
                    for i in range(1, 6)
                ]
            }
            
            return weather_data
            
        except Exception as e:
            return {"error": f"Erreur lors de la récupération météo: {str(e)}"}
    
    def get_educational_news(self, subject: str = None, max_results: int = 5) -> List[Dict]:
        """Obtenir les actualités éducatives"""
        try:
            # Simulation de nouvelles éducatives
            news = []
            for i in range(1, max_results + 1):
                subject_value = subject if subject else "l'éducation"
                news.append({
                    "id": f"news_{i}",
                    "title": f"Nouvelle approche pedagogique pour {subject_value}",
                    "description": f"Article sur les innovations en {subject_value}",
                    "url": f"https://example.com/news/{i}",
                    "published_date": (datetime.now() - timedelta(days=i*2)).isoformat(),
                    "source": f"Source Educative {i}",
                    "category": subject or "General"
                })
            return news
            
        except Exception as e:
            return [{"error": f"Erreur lors de la récupération des nouvelles: {str(e)}"}]
    
    def translate_educational_content(self, text: str, target_language: str = "en") -> Dict[str, Any]:
        """Traduire du contenu éducatif"""
        try:
            # Simulation de traduction
            translations = {
                "en": {
                    "Bonjour": "Hello",
                    "Mathématiques": "Mathematics",
                    "Sciences": "Sciences",
                    "Histoire": "History",
                    "Géographie": "Geography"
                },
                "es": {
                    "Bonjour": "Hola",
                    "Mathématiques": "Matemáticas",
                    "Sciences": "Ciencias",
                    "Histoire": "Historia",
                    "Géographie": "Geografía"
                }
            }
            
            # Traduction simple basée sur des mots-clés
            translated_text = text
            if target_language in translations:
                for french, translation in translations[target_language].items():
                    translated_text = translated_text.replace(french, translation)
            
            return {
                "original_text": text,
                "translated_text": translated_text,
                "target_language": target_language,
                "confidence": 0.85
            }
            
        except Exception as e:
            return {"error": f"Erreur lors de la traduction: {str(e)}"}
    
    def get_calendar_holidays(self, country: str = "FR", year: int = None) -> List[Dict]:
        """Obtenir les jours fériés pour la planification"""
        try:
            if year is None:
                year = datetime.now().year
            
            # Jours fériés français (simulés)
            holidays = [
                {"date": f"{year}-01-01", "name": "Jour de l'an", "type": "Férié"},
                {"date": f"{year}-05-01", "name": "Fête du travail", "type": "Férié"},
                {"date": f"{year}-05-08", "name": "Victoire 1945", "type": "Férié"},
                {"date": f"{year}-07-14", "name": "Fête nationale", "type": "Férié"},
                {"date": f"{year}-08-15", "name": "Assomption", "type": "Férié"},
                {"date": f"{year}-11-01", "name": "Toussaint", "type": "Férié"},
                {"date": f"{year}-11-11", "name": "Armistice", "type": "Férié"},
                {"date": f"{year}-12-25", "name": "Noël", "type": "Férié"}
            ]
            
            return holidays
            
        except Exception as e:
            return [{"error": f"Erreur lors de la récupération des jours fériés: {str(e)}"}]
    
    def get_currency_exchange_rates(self, base_currency: str = "EUR") -> Dict[str, float]:
        """Obtenir les taux de change (pour les projets internationaux)"""
        try:
            # Taux de change simulés
            rates = {
                "USD": 1.08,
                "GBP": 0.86,
                "JPY": 160.5,
                "CAD": 1.47,
                "AUD": 1.65,
                "CHF": 0.95
            }
            
            return {
                "base_currency": base_currency,
                "rates": rates,
                "last_updated": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {"error": f"Erreur lors de la récupération des taux: {str(e)}"}

# Instance globale des intégrations
integrations = ExternalIntegrations()

@router.get("/videos/search")
def search_educational_videos(
    query: str = Query(..., description="Terme de recherche"),
    subject: str = Query(None, description="Matière spécifique"),
    max_results: int = Query(10, description="Nombre maximum de résultats"),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['teacher', 'admin']))
):
    """Rechercher des vidéos éducatives"""
    try:
        videos = integrations.search_educational_videos(query, subject, max_results)
        
        return {
            "query": query,
            "subject": subject,
            "results_count": len(videos),
            "videos": videos
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la recherche: {str(e)}")

@router.get("/weather/forecast")
def get_weather_forecast(
    city: str = Query("Paris", description="Ville pour les prévisions"),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['teacher', 'admin']))
):
    """Obtenir les prévisions météo"""
    try:
        weather = integrations.get_weather_forecast(city)
        
        return {
            "city": city,
            "weather": weather
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la récupération météo: {str(e)}")

@router.get("/news/educational")
def get_educational_news(
    subject: str = Query(None, description="Matière spécifique"),
    max_results: int = Query(5, description="Nombre maximum d'articles"),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['teacher', 'admin']))
):
    """Obtenir les actualités éducatives"""
    try:
        news = integrations.get_educational_news(subject, max_results)
        
        return {
            "subject": subject,
            "results_count": len(news),
            "news": news
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la récupération des nouvelles: {str(e)}")

@router.post("/translate/content")
def translate_educational_content(
    text: str = Query(..., description="Texte à traduire"),
    target_language: str = Query("en", description="Langue cible"),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['teacher', 'admin']))
):
    """Traduire du contenu éducatif"""
    try:
        translation = integrations.translate_educational_content(text, target_language)
        
        return translation
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la traduction: {str(e)}")

@router.get("/calendar/holidays")
def get_calendar_holidays(
    country: str = Query("FR", description="Code pays"),
    year: int = Query(None, description="Année (optionnel)"),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['teacher', 'admin']))
):
    """Obtenir les jours fériés"""
    try:
        holidays = integrations.get_calendar_holidays(country, year)
        
        return {
            "country": country,
            "year": year or datetime.now().year,
            "holidays": holidays
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la récupération des jours fériés: {str(e)}")

@router.get("/currency/rates")
def get_currency_exchange_rates(
    base_currency: str = Query("EUR", description="Devise de base"),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['teacher', 'admin']))
):
    """Obtenir les taux de change"""
    try:
        rates = integrations.get_currency_exchange_rates(base_currency)
        
        return rates
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la récupération des taux: {str(e)}")

@router.get("/integrations/status")
def get_integrations_status(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(['teacher', 'admin']))
):
    """Obtenir le statut de toutes les intégrations"""
    try:
        status = {
            "youtube_api": {
                "status": "active" if integrations.youtube_api_key != "demo_key" else "demo",
                "description": "Recherche de vidéos éducatives"
            },
            "weather_api": {
                "status": "active" if integrations.openweather_api_key != "demo_key" else "demo",
                "description": "Prévisions météo"
            },
            "news_api": {
                "status": "active" if integrations.news_api_key != "demo_key" else "demo",
                "description": "Actualités éducatives"
            },
            "translate_api": {
                "status": "active" if integrations.translate_api_key != "demo_key" else "demo",
                "description": "Traduction de contenu"
            }
        }
        
        return {
            "integrations": status,
            "last_checked": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la vérification du statut: {str(e)}") 