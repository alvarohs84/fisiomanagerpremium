from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database import get_db
import models
import schemas
import auth

router = APIRouter(prefix="/users", tags=["Users"])

# TROCAR SENHA (Qualquer um pode)
@router.patch("/me/password")
def change_password(
    data: schemas.UserPasswordUpdate, 
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(auth.get_current_user)
):
    if not auth.verify_password(data.old_password, current_user.hashed_password):
        raise HTTPException(status_code=400, detail="Senha antiga incorreta")
    
    current_user.hashed_password = auth.hash_password(data.new_password)
    db.commit()
    return {"message": "Senha atualizada com sucesso"}

# LISTAR USUÁRIOS (Só Admin)
@router.get("/", response_model=List[schemas.UserOut])
def list_users(db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Acesso negado")
    return db.query(models.User).all()

# CRIAR NOVO USUÁRIO (Só Admin)
@router.post("/", response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Apenas Admin pode criar usuários")
    
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Usuário já existe")

    new_user = models.User(
        username=user.username,
        hashed_password=auth.hash_password(user.password),
        full_name=user.full_name,
        role=user.role
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# DELETAR USUÁRIO (Só Admin)
@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Acesso negado")
    
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    if user.username == "admin":
        raise HTTPException(status_code=400, detail="Não é possível deletar o Admin principal")

    db.delete(user)
    db.commit()
    return {"message": "Usuário deletado"}
