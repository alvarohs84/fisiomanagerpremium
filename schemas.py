from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional

# AUTH
class Token(BaseModel):
    access_token: str
    token_type: str

class UserLogin(BaseModel):
    username: str
    password: str
    
class AdminCreate(BaseModel):
    username: str
    password: str

# PACIENTES
class PatientBase(BaseModel):
    name: str
    # Agora tudo é opcional exceto o nome
    birth_date: Optional[date] = None            
    sex: Optional[str] = None
    phone: Optional[str] = None
    insurance: Optional[str] = None

class PatientCreate(PatientBase):
    pass

class PatientUpdate(BaseModel): # Novo Schema para Edição
    name: Optional[str] = None
    birth_date: Optional[date] = None
    sex: Optional[str] = None
    phone: Optional[str] = None
    insurance: Optional[str] = None

class PatientOut(PatientBase):
    id: int
    idade: int
    class Config:
        from_attributes = True

# EVOLUÇÕES
class EvolutionCreate(BaseModel):
    patient_id: int
    description: str

class EvolutionOut(BaseModel):
    id: int
    patient_id: int
    description: str
    date: datetime
    class Config:
        from_attributes = True

# AGENDA
class AppointmentBase(BaseModel):
    patient_id: int
    start_time: datetime
    end_time: datetime
    status: Optional[str] = "Agendado"
    notes: Optional[str] = None

class AppointmentCreate(AppointmentBase):
    pass

class AppointmentUpdate(BaseModel):
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    status: Optional[str] = None
    notes: Optional[str] = None

class AppointmentOut(AppointmentBase):
    id: int
    patient_name: str = "Desconhecido"
    class Config:
        from_attributes = True
        

        
        
