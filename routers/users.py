from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import crud
import schemas
import auth
from database import get_db  # Импортируем get_db
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    logger.info(f"Attempting to create user: {user.username}")
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        logger.warning(f"Username {user.username} already registered")
        raise HTTPException(status_code=400, detail="Username already registered")
    logger.info(f"User {user.username} created successfully")
    return crud.create_user(db=db, user=user)

@router.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    logger.info(f"Fetching user with ID: {user_id}")
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        logger.warning(f"User with ID {user_id} not found")
        raise HTTPException(status_code=404, detail="User not found")
    logger.info(f"User {db_user.username} fetched successfully")
    return db_user