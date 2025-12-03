from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional, Dict, Any

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
    birth_date: Optional[date] = None            
    sex: Optional[str] = None
    phone: Optional[str] = None
    insurance: Optional[str] = None

class PatientCreate(PatientBase):
    pass

class PatientUpdate(BaseModel):
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

# FINANCEIRO
class TransactionBase(BaseModel):
    description: str
    amount: float
    type: str

class TransactionCreate(TransactionBase):
    pass

class TransactionOut(TransactionBase):
    id: int
    date: datetime
    class Config:
        from_attributes = True

# AVALIAÇÕES (NOVO)
class AssessmentCreate(BaseModel):
    patient_id: int
    specialty: str
    content: Dict[str, Any] # Aceita qualquer JSON

class AssessmentOut(BaseModel):
    id: int
    patient_id: int
    specialty: str
    content: Dict[str, Any]
    date: datetime
    class Config:
        from_attributes = True
        
        # =============================
# USUÁRIOS (UPDATE)
# =============================
class UserPasswordUpdate(BaseModel):
    old_password: str
    new_password: str
    
    # EVOLUÇÕES
# =============================
class EvolutionCreate(BaseModel):
    patient_id: int
    description: str
    content: Optional[Dict[str, Any]] = None # Agora aceita JSON opcional

class EvolutionOut(BaseModel):
    id: int
    patient_id: int
    description: str
    content: Optional[Dict[str, Any]] = None # Devolve o JSON
    date: datetime
    class Config:
        from_attributes = True
        
        
