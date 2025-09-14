from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pathlib import Path
import os

router = APIRouter()

@router.get("/uploads/assignments/{filename}")
async def get_assignment_file(filename: str):
    """Récupère un fichier de devoir"""
    try:
        # Chemin du fichier - utiliser un chemin absolu
        base_path = Path(__file__).parent.parent.parent.parent / "data" / "uploads" / "assignments"
        file_path = base_path / filename
        
        print(f"🔍 Recherche du fichier: {file_path}")
        print(f"📁 Dossier de base: {base_path}")
        print(f"📄 Fichier demandé: {filename}")
        
        # Vérifier que le fichier existe
        if not file_path.exists():
            print(f"❌ Fichier non trouvé: {file_path}")
            raise HTTPException(status_code=404, detail=f"Fichier non trouvé: {filename}")
        
        print(f"✅ Fichier trouvé: {file_path}")
        
        # Vérifier que le fichier est dans le bon dossier
        if not str(file_path).startswith(str(base_path)):
            print(f"❌ Accès non autorisé: {file_path}")
            raise HTTPException(status_code=403, detail="Accès non autorisé")
        
        # Déterminer le type MIME basé sur l'extension
        if filename.lower().endswith('.pdf'):
            media_type = 'application/pdf'
        elif filename.lower().endswith('.doc'):
            media_type = 'application/msword'
        elif filename.lower().endswith('.docx'):
            media_type = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        elif filename.lower().endswith('.txt'):
            media_type = 'text/plain'
        else:
            media_type = 'application/octet-stream'
        
        print(f"📋 Type MIME: {media_type}")
        
        # Retourner le fichier
        return FileResponse(
            path=str(file_path),
            filename=filename,
            media_type=media_type
        )
        
    except Exception as e:
        print(f"💥 Erreur: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Erreur lors de la récupération du fichier: {str(e)}")

