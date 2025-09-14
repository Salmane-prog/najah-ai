from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from core.database import SessionLocal
from models.category import Category
from schemas.category import CategoryCreate, CategoryRead
from api.v1.users import get_current_user
from api.v1.auth import require_role

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=List[CategoryRead])
def list_categories(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return db.query(Category).all()

@router.post("/", response_model=CategoryRead, status_code=201)
def create_category(category: CategoryCreate, db: Session = Depends(get_db), current_user=Depends(require_role(['admin', 'teacher']))):
    db_cat = Category(**category.dict())
    db.add(db_cat)
    db.commit()
    db.refresh(db_cat)
    return db_cat

@router.get("/{category_id}", response_model=CategoryRead)
def get_category(category_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    cat = db.query(Category).filter(Category.id == category_id).first()
    if not cat:
        raise HTTPException(status_code=404, detail="Category not found")
    return cat

@router.delete("/{category_id}", status_code=204)
def delete_category(category_id: int, db: Session = Depends(get_db), current_user=Depends(require_role(['admin']))):
    cat = db.query(Category).filter(Category.id == category_id).first()
    if not cat:
        raise HTTPException(status_code=404, detail="Category not found")
    db.delete(cat)
    db.commit()
    return None 