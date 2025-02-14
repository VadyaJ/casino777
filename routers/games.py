from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import crud
import schemas
import auth
from database import get_db  # Импортируем get_db
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/games/bet/", response_model=schemas.User)
def place_bet(amount: float, db: Session = Depends(get_db), current_user: schemas.User = Depends(auth.get_current_user)):
    logger.info(f"User {current_user.username} placing a bet of {amount}")

    if amount <= 0:
        logger.warning(f"Invalid bet amount: {amount}")
        raise HTTPException(status_code=400, detail="Bet amount must be positive")

    if current_user.balance < amount:
        logger.warning(f"User {current_user.username} has insufficient balance")
        raise HTTPException(status_code=400, detail="Not enough balance")

    # Простая логика игры: 50% шанс выигрыша
    import random
    if random.random() < 0.5:
        current_user.balance += amount
        logger.info(f"User {current_user.username} won {amount}")
    else:
        current_user.balance -= amount
        logger.info(f"User {current_user.username} lost {amount}")

    db.commit()
    db.refresh(current_user)
    return current_user