from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Evolution, Patient
from schemas import EvolutionCreate, EvolutionOut

router = APIRouter(prefix="/evolutions", tags=["Evolutions"])

@router.post("/", response_model=EvolutionOut)
def create_evolution(data: EvolutionCreate, db: Session = Depends(get_db)):
    
    patient = db.query(Patient).filter(Patient.id == data.patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")

    evo = Evolution(**data.dict())
    db.add(evo)
    db.commit()
    db.refresh(evo)
    return evo

@router.get("/patient/{patient_id}", response_model=list[EvolutionOut])
def list_by_patient(patient_id: int, db: Session = Depends(get_db)):
    return db.query(Evolution).filter(Evolution.patient_id == patient_id).all()
