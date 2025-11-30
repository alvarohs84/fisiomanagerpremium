from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import Base, engine, get_db
from models import User
from auth import hash_password
from routers import users, patients, evolutions, appointments

Base.metadata.create_all(bind=engine)

app = FastAPI(title="FisioManager Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ou coloque somente seu frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "FisioManager Backend OK (CORS liberado)"}

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

app.include_router(users.router)
app.include_router(patients.router)
app.include_router(evolutions.router)
app.include_router(appointments.router)

