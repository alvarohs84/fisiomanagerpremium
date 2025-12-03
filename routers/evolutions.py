from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models
import schemas
from auth import get_current_user

router = APIRouter(prefix="/evolutions", tags=["Evolutions"])

@router.get("/", response_model=list[schemas.EvolutionOut])
def list_evolutions(patient_id: int = None, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    query = db.query(models.Evolution)
    if patient_id:
        query = query.filter(models.Evolution.patient_id == patient_id)
    return query.order_by(models.Evolution.date.desc()).all()

@router.post("/", response_model=schemas.EvolutionOut)
def create_evolution(evo: schemas.EvolutionCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    db_evo = models.Evolution(
        patient_id=evo.patient_id,
        description=evo.description,
        content=evo.content # <--- Salvando os dados extras
    )
    db.add(db_evo)
    db.commit()
    db.refresh(db_evo)
    return db_evo

@router.delete("/{evo_id}")
def delete_evolution(evo_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    evo = db.query(models.Evolution).filter(models.Evolution.id == evo_id).first()
    if not evo:
        raise HTTPException(status_code=404, detail="Evolução não encontrada")
    db.delete(evo)
    db.commit()
    return {"message": "Deletado"}
