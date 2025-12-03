from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Date, Float, JSON
from sqlalchemy.orm import relationship
from database import Base
from datetime import date, datetime

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
    
    birth_date = Column(Date, nullable=True)   
    sex = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    insurance = Column(String, nullable=True)

    evolutions = relationship("Evolution", back_populates="patient", cascade="all, delete-orphan")
    appointments = relationship("Appointment", back_populates="patient", cascade="all, delete-orphan")
    assessments = relationship("Assessment", back_populates="patient", cascade="all, delete-orphan")

    @property
    def idade(self):
        if not self.birth_date: return 0
        today = date.today()
        return today.year - self.birth_date.year - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))

# ======================================================
# EVOLUÇÕES
# ======================================================
class Evolution(Base):
    __tablename__ = "evolutions"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    description = Column(String, nullable=False)
    date = Column(DateTime, default=datetime.utcnow)

    patient = relationship("Patient", back_populates="evolutions")

# ======================================================
# AGENDAMENTOS
# ======================================================
class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    status = Column(String, default="Agendado")
    notes = Column(String, nullable=True)
    
    patient = relationship("Patient", back_populates="appointments")

# ======================================================
# FINANCEIRO
# ======================================================
class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    type = Column(String, nullable=False)
    date = Column(DateTime, default=datetime.utcnow)

# ======================================================
# AVALIAÇÕES (NOVO)
# ======================================================
class Assessment(Base):
    __tablename__ = "assessments"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    
    specialty = Column(String, nullable=False) # Ex: "Ortopedica"
    content = Column(JSON, nullable=False)     # Salva as perguntas/respostas
    date = Column(DateTime, default=datetime.utcnow)

    patient = relationship("Patient", back_populates="assessments")
    
class Evolution(Base):
    __tablename__ = "evolutions"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    description = Column(String, nullable=False) # Texto livre
    
    # NOVO: Campo para guardar EVA, MRC e Goniometria estruturados
    content = Column(JSON, nullable=True) 
    
    date = Column(DateTime, default=datetime.utcnow)

    patient = relationship("Patient", back_populates="evolutions")