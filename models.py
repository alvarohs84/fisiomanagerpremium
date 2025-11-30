from sqlalchemy import Column, Integer, String, ForeignKey
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
# PACIENTES
# ======================================================

class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    age = Column(Integer)
    plan = Column(String)

    evolutions = relationship("Evolution", back_populates="patient")


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
# AGENDAMENTOS (se existir)
# ======================================================

class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    date = Column(String)
    time = Column(String)
    notes = Column(String, nullable=True)


