from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import Base, engine, get_db
from models import User
from auth import hash_password

# Importando seus roteadores
from routers import users, patients, evolutions, appointments

# Cria as tabelas
Base.metadata.create_all(bind=engine)

app = FastAPI(title="FisioManager Backend")

# --- CONFIGURAÇÃO DE CORS ATUALIZADA ---
origins = [
    "http://localhost:3000",
    "https://fisiomanager-frontend1.onrender.com", # Seu Front
    "https://fisiomanager-frontend1.onrender.com/"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, # Use a lista específica
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "FisioManager Backend OK (CORS Configurado)"}

@app.post("/create-admin")
def create_admin(db: Session = Depends(get_db)):
    try:
        existing = db.query(User).filter(User.username == "admin").first()
        if existing:
            return {"message": "Admin já existe"}

        admin = User(
            username="admin",
            hashed_password=hash_password("123456")
        )
        db.add(admin)
        db.commit()
        db.refresh(admin)

        return {
            "message": "Admin criado com sucesso!",
            "username": "admin",
            "password": "123456"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Incluindo as rotas
app.include_router(users.router)
app.include_router(patients.router)
app.include_router(evolutions.router)
app.include_router(appointments.router)

# ==========================================
# ROTA DE EMERGÊNCIA (COLE ISSO NO MAIN.PY)
# ==========================================
from database import engine
import models

@app.get("/reset-database-force")
def reset_database():
    # Isso apaga a tabela velha e cria a nova
    models.Base.metadata.drop_all(bind=engine)
    models.Base.metadata.create_all(bind=engine)
    return {"message": "Banco de dados RESETADO com sucesso! Tabela pacientes atualizada."}

