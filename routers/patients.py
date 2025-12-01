from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database import get_db
import models
import schemas
from auth import get_current_user 

router = APIRouter(prefix="/patients", tags=["Patients"])

# CRIAR (Cadastro Rápido aceita null agora)
@router.post("/", response_model=schemas.PatientOut)
def create_patient(patient: schemas.PatientCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    db_patient = models.Patient(
        name=patient.name,
        birth_date=patient.birth_date, # Pode ser None
        sex=patient.sex,
        phone=patient.phone,
        insurance=patient.insurance
    )
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient

# LISTAR
@router.get("/", response_model=List[schemas.PatientOut])
def list_patients(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return db.query(models.Patient).all()

# BUSCAR UM
@router.get("/{patient_id}", response_model=schemas.PatientOut)
def get_patient(patient_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    patient = db.query(models.Patient).filter(models.Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")
    return patient

# EDITAR (NOVA ROTA)
@router.patch("/{patient_id}", response_model=schemas.PatientOut)
def update_patient(
    patient_id: int, 
    data: schemas.PatientUpdate, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    db_patient = db.query(models.Patient).filter(models.Patient.id == patient_id).first()
    if not db_patient:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")
    
    # Atualiza apenas os campos enviados
    if data.name: db_patient.name = data.name
    if data.birth_date: db_patient.birth_date = data.birth_date
    if data.sex: db_patient.sex = data.sex
    if data.phone: db_patient.phone = data.phone
    if data.insurance: db_patient.insurance = data.insurance
    
    db.commit()
    db.refresh(db_patient)
    return db_patient

# DELETAR
@router.delete("/{patient_id}")
def delete_patient(patient_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    patient = db.query(models.Patient).filter(models.Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")
    db.delete(patient)
    db.commit()
    return {"message": "Paciente deletado"}
