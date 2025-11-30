from pydantic import BaseModel

# =============================
# AUTH
# =============================
class Token(BaseModel):
    access_token: str
    token_type: str

class UserLogin(BaseModel):
    username: str
    password: str


# =============================
# PACIENTES
# =============================
class PatientCreate(BaseModel):
    name: str
    age: int
    plan: str

class PatientOut(BaseModel):
    id: int
    name: str
    age: int
    plan: str

    class Config:
        from_attributes = True


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
    notes: str | None = None

class AppointmentOut(BaseModel):
    id: int
    patient_id: int
    date: str
    time: str
    notes: str | None

    class Config:
        from_attributes = True
