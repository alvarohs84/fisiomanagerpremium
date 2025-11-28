from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import Patient
from schemas import PatientCreate

router = APIRouter(prefix="/patients")

@router.get("")
def list(db: Session = Depends(get_db)):
    return db.query(Patient).all()

@router.post("")
def create(data: PatientCreate, db: Session = Depends(get_db)):
    p = Patient(**data.dict())
    db.add(p)
    db.commit()
    return p

@router.get("/{id}")
def get(id: int, db: Session = Depends(get_db)):
    return db.query(Patient).filter(Patient.id == id).first()

@router.put("/{id}")
def update(id: int, data: PatientCreate, db: Session = Depends(get_db)):
    p = db.query(Patient).filter(Patient.id == id).first()
    for k, v in data.dict().items():
        setattr(p, k, v)
    db.commit()
    return p

@router.delete("/{id}")
def delete(id: int, db: Session = Depends(get_db)):
    p = db.query(Patient).filter(Patient.id == id).first()
    db.delete(p)
    db.commit()
    return {"detail": "Paciente removido"}


