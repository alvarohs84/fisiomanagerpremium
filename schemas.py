from pydantic import BaseModel
from datetime import date
from typing import Optional

# =============================
# AUTH
# =============================
class Token(BaseModel):
    access_token: str
    token_type: str

class UserLogin(BaseModel):
    username: str
    password: str
    
class AdminCreate(BaseModel):
    username: str
    password: str

# =============================
# PACIENTES
# =============================
class PatientBase(BaseModel):
    name: str
    birth_date: date            # Recebe data (AAAA-MM-DD)
    sex: Optional[str] = None
    phone: Optional[str] = None
    insurance: Optional[str] = None # Antigo 'plan', agora 'insurance' (Convênio)

class PatientCreate(PatientBase):
    pass

class PatientOut(PatientBase):
    id: int
    idade: int # Campo extra que calcularemos automaticamente

    # Configuração deve ficar DENTRO da classe
    class Config:
        from_attributes = True

    # Lógica para calcular a idade ao enviar a resposta
    @staticmethod
    def calculate_age(birth_date: date) -> int:
        today = date.today()
        return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

    def model_dump(self, **kwargs):
        data = super().model_dump(**kwargs)
        data['idade'] = self.calculate_age(self.birth_date)
        return data

# =============================
# EVOLUTIONS
# =============================
class EvolutionCreate(BaseModel):
    patient_id: int
    description: str

class EvolutionOut(BaseModel):
    id: int
    patient_id: int
    description: str

    class Config:
        from_attributes = True

# =============================
# APPOINTMENTS
# =============================
class AppointmentCreate(BaseModel):
    patient_id: int
    date: str
    time: str
    notes: Optional[str] = None

class AppointmentOut(BaseModel):
    id: int
    patient_id: int
    date: str
    time: str
    notes: Optional[str] = None

    class Config:
        from_attributes = True
        

        
        
