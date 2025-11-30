from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import User
from schemas import UserLogin, Token
from auth import verify_password, create_access_token

router = APIRouter(prefix="", tags=["Users"])

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

