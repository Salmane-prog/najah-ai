import os
import json
from fastapi import APIRouter, HTTPException, Body, status, Depends
from typing import List, Optional
from api.v1.users import get_current_user
from api.v1.auth import require_role

QCM_ROOT = "data/qcm"

router = APIRouter()

def get_quiz_files():
    quizzes = []
    for matiere in os.listdir(QCM_ROOT):
        matiere_path = os.path.join(QCM_ROOT, matiere)
        if os.path.isdir(matiere_path):
            for file in os.listdir(matiere_path):
                if file.endswith('.json'):
                    quizzes.append({
                        "matiere": matiere,
                        "filename": file,
                        "path": os.path.join(matiere_path, file)
                    })
    return quizzes

@router.get("/json/list", tags=["quiz-json"])
def list_quiz_files(current_user=Depends(get_current_user)):
    """Lister tous les quiz JSON disponibles (par matière)."""
    return get_quiz_files()

@router.get("/json/{matiere}/{filename}", tags=["quiz-json"])
def get_quiz_questions(matiere: str, filename: str, current_user=Depends(get_current_user)):
    """Récupérer toutes les questions d'un quiz JSON."""
    path = os.path.join(QCM_ROOT, matiere, filename)
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="Quiz JSON non trouvé")
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    return data

@router.post("/json/{matiere}/{filename}/add", tags=["quiz-json"])
def add_quiz_question(matiere: str, filename: str, question: dict = Body(...), current_user=Depends(require_role(['teacher', 'admin']))):
    path = os.path.join(QCM_ROOT, matiere, filename)
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="Quiz JSON non trouvé")
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    data["dataset_entrainement_enrichi"].append(question)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return {"message": "Question ajoutée"}

@router.put("/json/{matiere}/{filename}/edit/{question_id}", tags=["quiz-json"])
def edit_quiz_question(matiere: str, filename: str, question_id: str, question: dict = Body(...), current_user=Depends(require_role(['teacher', 'admin']))):
    path = os.path.join(QCM_ROOT, matiere, filename)
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="Quiz JSON non trouvé")
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    questions = data["dataset_entrainement_enrichi"]
    for i, q in enumerate(questions):
        if q["id"] == question_id:
            questions[i] = question
            break
    else:
        raise HTTPException(status_code=404, detail="Question non trouvée")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return {"message": "Question modifiée"}

@router.delete("/json/{matiere}/{filename}/delete/{question_id}", tags=["quiz-json"])
def delete_quiz_question(matiere: str, filename: str, question_id: str, current_user=Depends(require_role(['teacher', 'admin']))):
    path = os.path.join(QCM_ROOT, matiere, filename)
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="Quiz JSON non trouvé")
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    questions = data["dataset_entrainement_enrichi"]
    new_questions = [q for q in questions if q["id"] != question_id]
    if len(new_questions) == len(questions):
        raise HTTPException(status_code=404, detail="Question non trouvée")
    data["dataset_entrainement_enrichi"] = new_questions
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return {"message": "Question supprimée"}

@router.post("/json/{matiere}/create", tags=["quiz-json"])
def create_quiz_json(matiere: str, meta: dict = Body(...), current_user=Depends(require_role(['teacher', 'admin']))):
    """Créer un nouveau quiz JSON pour une matière donnée."""
    matiere_path = os.path.join(QCM_ROOT, matiere)
    os.makedirs(matiere_path, exist_ok=True)
    filename = meta.get("filename") or "quiz_new.json"
    path = os.path.join(matiere_path, filename)
    if os.path.exists(path):
        raise HTTPException(status_code=400, detail="Un quiz avec ce nom existe déjà")
    data = {
        "metadata": meta.get("metadata", {}),
        "dataset_entrainement_enrichi": []
    }
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return {"message": "Quiz créé", "filename": filename}

@router.post("/assign", tags=["quiz-json"])
def assign_quiz(payload: dict = Body(...), current_user=Depends(require_role(['teacher', 'admin']))):
    """Affecter un quiz JSON à plusieurs classes/élèves."""
    # payload: { matiere, filename, class_ids: [], student_ids: [] }
    assign_path = os.path.join(QCM_ROOT, "assignations.json")
    if os.path.exists(assign_path):
        with open(assign_path, encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = []
    data.append({
        "matiere": payload.get("matiere"),
        "filename": payload.get("filename"),
        "class_ids": payload.get("class_ids", []),
        "student_ids": payload.get("student_ids", []),
        "by": getattr(current_user, "id", None)
    })
    with open(assign_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return {"message": "Quiz affecté"} 