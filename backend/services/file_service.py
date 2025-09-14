import os
import shutil
from pathlib import Path
from fastapi import UploadFile, HTTPException
from datetime import datetime
import uuid

class FileService:
    def __init__(self):
        # Créer le dossier uploads s'il n'existe pas - utiliser un chemin absolu
        base_path = Path(__file__).parent.parent.parent / "data" / "uploads"
        self.uploads_dir = base_path
        self.uploads_dir.mkdir(parents=True, exist_ok=True)
        
        # Créer le dossier assignments s'il n'existe pas
        self.assignments_dir = self.uploads_dir / "assignments"
        self.assignments_dir.mkdir(exist_ok=True)
        
        print(f"📁 Dossier uploads créé: {self.uploads_dir}")
        print(f"📁 Dossier assignments créé: {self.assignments_dir}")
    
    async def save_assignment_file(self, file: UploadFile, assignment_id: int) -> dict:
        """Sauvegarde un fichier de devoir et retourne ses métadonnées"""
        try:
            # Vérifier le type de fichier
            allowed_extensions = {'.pdf', '.doc', '.docx', '.txt'}
            file_extension = Path(file.filename).suffix.lower()
            
            if file_extension not in allowed_extensions:
                raise HTTPException(
                    status_code=400, 
                    detail=f"Type de fichier non autorisé. Extensions autorisées: {', '.join(allowed_extensions)}"
                )
            
            # Vérifier la taille (10 MB max)
            if file.size > 10 * 1024 * 1024:
                raise HTTPException(
                    status_code=400, 
                    detail="Fichier trop volumineux. Taille maximum: 10 MB"
                )
            
            # Générer un nom de fichier unique
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            unique_id = str(uuid.uuid4())[:8]
            safe_filename = f"assignment_{assignment_id}_{timestamp}_{unique_id}{file_extension}"
            
            # Chemin complet du fichier
            file_path = self.assignments_dir / safe_filename
            
            print(f"💾 Sauvegarde du fichier: {file_path}")
            print(f"📁 Dossier de destination: {self.assignments_dir}")
            print(f"📄 Nom du fichier: {safe_filename}")
            
            # Sauvegarder le fichier
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            
            print(f"✅ Fichier sauvegardé avec succès: {file_path}")
            print(f"🔍 Vérification de l'existence: {file_path.exists()}")
            
            # Retourner les métadonnées
            return {
                "name": file.filename,
                "size": file.size,
                "type": file.content_type,
                "path": str(file_path),
                "url": f"/uploads/assignments/{safe_filename}"
            }
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erreur lors de la sauvegarde du fichier: {str(e)}")
    
    def get_file_path(self, filename: str) -> Path:
        """Retourne le chemin complet d'un fichier"""
        return self.assignments_dir / filename
    
    def delete_file(self, filename: str) -> bool:
        """Supprime un fichier"""
        try:
            file_path = self.get_file_path(filename)
            if file_path.exists():
                file_path.unlink()
                return True
            return False
        except Exception:
            return False

# Instance globale du service
file_service = FileService()

