from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
import models
import schemas
from auth import get_current_user

router = APIRouter(prefix="/appointments", tags=["Appointments"])

# LISTAR TUDO (Para o calendário)
@router.get("/", response_model=List[schemas.AppointmentOut])
def get_appointments(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    appts = db.query(models.Appointment).all()
    
    # Preenche o nome do paciente para mostrar no calendário
    results = []
    for a in appts:
        appt_out = schemas.AppointmentOut.model_validate(a)
        if a.patient:
            appt_out.patient_name = a.patient.name
        results.append(appt_out)
    return results

# CRIAR
@router.post("/", response_model=schemas.AppointmentOut)
def create_appointment(
    appt: schemas.AppointmentCreate, 
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(get_current_user)
):
    db_appt = models.Appointment(
        patient_id=appt.patient_id,
        start_time=appt.start_time,
        end_time=appt.end_time,
        status=appt.status,
        notes=appt.notes
    )
    db.add(db_appt)
    db.commit()
    db.refresh(db_appt)
    
    # Retorno com nome
    resp = schemas.AppointmentOut.model_validate(db_appt)
    resp.patient_name = db_appt.patient.name
    return resp

# ATUALIZAR (Arrastar e Soltar ou Editar)
@router.patch("/{appt_id}")
def update_appointment(
    appt_id: int, 
    data: schemas.AppointmentUpdate, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    appt = db.query(models.Appointment).filter(models.Appointment.id == appt_id).first()
    if not appt:
        raise HTTPException(status_code=404, detail="Agendamento não encontrado")
    
    if data.start_time: appt.start_time = data.start_time
    if data.end_time: appt.end_time = data.end_time
    if data.status: appt.status = data.status
    if data.notes: appt.notes = data.notes
    
    db.commit()
    return {"message": "Atualizado com sucesso"}

# DELETAR
@router.delete("/{appt_id}")
def delete_appointment(
    appt_id: int, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    appt = db.query(models.Appointment).filter(models.Appointment.id == appt_id).first()
    if not appt:
        raise HTTPException(status_code=404, detail="Não encontrado")
    
    db.delete(appt)
    db.commit()
    return {"message": "Deletado"}
