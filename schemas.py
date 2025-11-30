from pydantic import BaseModel
from typing import Optional


# ======================================================
# TOKEN PARA AUTENTICAÇÃO JWT
# ======================================================

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    username: Optional[str] = None


# ======================================================
# LOGIN DO USUÁRIO
# ======================================================

class UserLogin(BaseModel):
    username: str
    password: str


# ======================================================
# USUÁRIO
# ======================================================

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int

    class Config:
        from_attributes = True


# ======================================================
# PACIENTES
# ======================================================

class PatientBase(BaseModel):
    name: str
    age: int
    plan: str

class PatientCreate(PatientBase):
    pass

class Patient(PatientBase):
    id: int

    class Config:
        from_attributes = True


# ======================================================
# EVOLUÇÕES
# ======================================================

class EvolutionBase(BaseModel):
    patient_id: int
    description: str

class EvolutionCreate(EvolutionBase):
    pass

class Evolution(EvolutionBase):
    id: int

    class Config:
        from_attributes = True


