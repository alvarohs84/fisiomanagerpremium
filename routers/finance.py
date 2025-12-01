from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
import models
import schemas
from auth import get_current_user

router = APIRouter(prefix="/finance", tags=["Finance"])

@router.post("/", response_model=schemas.TransactionOut)
def create_transaction(
    tx: schemas.TransactionCreate, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    db_tx = models.Transaction(
        description=tx.description,
        amount=tx.amount,
        type=tx.type
    )
    db.add(db_tx)
    db.commit()
    db.refresh(db_tx)
    return db_tx

@router.get("/", response_model=List[schemas.TransactionOut])
def list_transactions(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    # Retorna do mais recente para o mais antigo
    return db.query(models.Transaction).order_by(models.Transaction.date.desc()).all()

@router.delete("/{tx_id}")
def delete_transaction(
    tx_id: int, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    tx = db.query(models.Transaction).filter(models.Transaction.id == tx_id).first()
    if not tx:
        raise HTTPException(status_code=404, detail="Transação não encontrada")
    db.delete(tx)
    db.commit()
    return {"message": "Deletado"}