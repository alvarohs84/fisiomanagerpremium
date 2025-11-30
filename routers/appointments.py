from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Appointment, Patient
from schemas import AppointmentCreate, AppointmentOut

router = APIRouter(prefix="/appointments", tags=["Appointments"])

@router.post("/", response_model=AppointmentOut)
def create_appointment(data: AppointmentCreate, db: Session = Depends(get_db)):

    patient = db.query(Patient).filter(Patient.id == data.patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")

    appt = Appointment(**data.dict())
    db.add(appt)
    db.commit()
    db.refresh(appt)
    return appt

@router.get("/patient/{patient_id}", response_model=list[AppointmentOut])
def list_appointments(patient_id: int, db: Session = Depends(get_db)):
    return db.query(Appointment).filter(Appointment.patient_id == patient_id).all()
