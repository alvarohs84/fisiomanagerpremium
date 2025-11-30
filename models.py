from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from database import Base

# ======================================================
# USUÁRIOS
# ======================================================
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)

# ======================================================
# PACIENTES (COM OS NOVOS CAMPOS)
# ======================================================
class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    
    # NOVOS CAMPOS AQUI
    name = Column(String, index=True)
    birth_date = Column(Date, nullable=False)   # Data Nascimento
    sex = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    insurance = Column(String, nullable=True)   # Convênio

    # Relacionamentos
    evolutions = relationship("Evolution", back_populates="patient")
    appointments = relationship("Appointment", back_populates="patient")

# ======================================================
# EVOLUÇÕES
# ======================================================
class Evolution(Base):
    __tablename__ = "evolutions"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    description = Column(String, nullable=False)

    patient = relationship("Patient", back_populates="evolutions")

# ======================================================
# AGENDAMENTOS
# ======================================================
class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    date = Column(String)
    time = Column(String)
    notes = Column(String, nullable=True)
    
    patient = relationship("Patient", back_populates="appointments")