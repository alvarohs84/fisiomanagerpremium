from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
import models
import schemas
import auth

router = APIRouter(prefix="/users", tags=["Users"])

@router.patch("/me/password")
def change_password(
    data: schemas.UserPasswordUpdate, 
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(auth.get_current_user)
):
    # 1. Verifica se a senha antiga bate com a do banco
    if not auth.verify_password(data.old_password, current_user.hashed_password):
        raise HTTPException(status_code=400, detail="Senha antiga incorreta")
    
    # 2. Gera o hash da nova senha
    new_hash = auth.hash_password(data.new_password)
    
    # 3. Salva no banco
    current_user.hashed_password = new_hash
    db.commit()
    
    return {"message": "Senha atualizada com sucesso"}
