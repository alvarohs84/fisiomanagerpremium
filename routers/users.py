from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import User
from schemas import UserLogin, Token, AdminCreate
from auth import verify_password, create_access_token, hash_password

router = APIRouter(prefix="", tags=["Users"])


@router.post("/create-admin")
def create_admin(data: AdminCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == data.username).first()

    if user:
        raise HTTPException(status_code=400, detail="Usuário já existe")

    new_user = User(
        username=data.username,
        hashed_password=hash_password(data.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "Admin criado com sucesso"}


@router.post("/token", response_model=Token)
def login(form: UserLogin, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.username == form.username).first()

    if not user or not verify_password(form.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Usuário ou senha incorretos")

    token = create_access_token({"sub": user.username})

    return {
        "access_token": token,
        "token_type": "bearer"
    }
