from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.database import get_db
from app import models, schemas
from app.auth import get_current_user

router = APIRouter(prefix="/transactions", tags=["Transactions"])


# ---------- CREATE ----------
@router.post("/", response_model=schemas.TransactionResponse, status_code=201)
def create_transaction(
    tx: schemas.TransactionCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    new_tx = models.Transaction(
        title=tx.title,
        amount=tx.amount,
        type=tx.type,
        category=tx.category,
        date=tx.date,
        owner_id=current_user.id,   # auto assign owner
    )
    db.add(new_tx)
    db.commit()
    db.refresh(new_tx)
    return new_tx


# ---------- READ ALL ----------
@router.get("/", response_model=list[schemas.TransactionResponse])
def get_all_transactions(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    return db.query(models.Transaction).filter(
        models.Transaction.owner_id == current_user.id
    ).all()


# ---------- FILTER (must be BEFORE /{transaction_id}!) ----------
@router.get("/filter", response_model=list[schemas.TransactionResponse])
def filter_transactions(
    type: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    minimum_amount: Optional[float] = Query(None),
    maximum_amount: Optional[float] = Query(None),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    query = db.query(models.Transaction).filter(
        models.Transaction.owner_id == current_user.id
    )
    if type:
        query = query.filter(models.Transaction.type == type)
    if category:
        query = query.filter(models.Transaction.category == category)
    if minimum_amount is not None:
        query = query.filter(models.Transaction.amount >= minimum_amount)
    if maximum_amount is not None:
        query = query.filter(models.Transaction.amount <= maximum_amount)
    return query.all()


# ---------- READ ONE ----------
@router.get("/{transaction_id}", response_model=schemas.TransactionResponse)
def get_transaction(
    transaction_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    tx = db.query(models.Transaction).filter(
        models.Transaction.id == transaction_id,
        models.Transaction.owner_id == current_user.id,
    ).first()
    if not tx:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return tx


# ---------- UPDATE ----------
@router.put("/{transaction_id}", response_model=schemas.TransactionResponse)
def update_transaction(
    transaction_id: int,
    update: schemas.TransactionUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    tx = db.query(models.Transaction).filter(
        models.Transaction.id == transaction_id,
        models.Transaction.owner_id == current_user.id,
    ).first()
    if not tx:
        raise HTTPException(status_code=404, detail="Transaction not found")

    # Only update fields that were provided
    data = update.model_dump(exclude_unset=True)
    for key, value in data.items():
        setattr(tx, key, value)

    db.commit()
    db.refresh(tx)
    return tx


# ---------- DELETE ----------
@router.delete("/{transaction_id}")
def delete_transaction(
    transaction_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    tx = db.query(models.Transaction).filter(
        models.Transaction.id == transaction_id,
        models.Transaction.owner_id == current_user.id,
    ).first()
    if not tx:
        raise HTTPException(status_code=404, detail="Transaction not found")

    db.delete(tx)
    db.commit()
    return {"message": "Transaction deleted successfully"}