from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from database import Base, engine, get_db
import models
import auth
from routers import users, patients, evolutions, appointments, finance, assessments

Base.metadata.create_all(bind=engine)

app = FastAPI(title="FisioManager API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/token")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Dados incorretos")
    
    # Retornamos também o role e o nome para o frontend saber quem é
    access_token = auth.create_access_token(data={"sub": user.username})
    return {
        "access_token": access_token, 
        "token_type": "bearer",
        "role": user.role,         # <--- Extra
        "full_name": user.full_name # <--- Extra
    }

@app.post("/create-admin")
def create_admin(db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == "admin").first()
    if user: return {"message": "Admin já existe"}
    
    hashed_pwd = auth.hash_password("123456")
    new_user = models.User(
        username="admin", 
        hashed_password=hashed_pwd,
        full_name="Administrador Principal",
        role="admin" # <--- IMPORTANTE: Define como Admin
    )
    db.add(new_user)
    db.commit()
    return {"message": "Admin criado com sucesso!", "username": "admin"}

@app.get("/reset-database-force")
def reset_database():
    models.Base.metadata.drop_all(bind=engine)
    models.Base.metadata.create_all(bind=engine)
    return {"message": "Banco de dados RESETADO!"}

@app.get("/")
def root():
    return {"message": "API FisioManager Online"}

app.include_router(users.router)
app.include_router(patients.router)
app.include_router(evolutions.router)
app.include_router(appointments.router)
app.include_router(finance.router)
app.include_router(assessments.router)
