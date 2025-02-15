from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import crud
import schemas
from database import get_db
from auth import create_access_token, get_current_user
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/register/", response_model=schemas.User)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    logger.info(f"Attempting to register user: {user.username}")
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        logger.warning(f"Username {user.username} already registered")
        raise HTTPException(status_code=400, detail="Username already registered")
    return crud.create_user(db=db, user=user)

@router.post("/login/", response_model=schemas.Token)
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    logger.info(f"Attempting to login user: {user.username}")
    db_user = crud.get_user_by_username(db, username=user.username)
    if not db_user or not pwd_context.verify(user.password, db_user.hashed_password):
        logger.warning(f"Invalid username or password for user: {user.username}")
        raise HTTPException(status_code=400, detail="Invalid username or password")
    access_token = create_access_token(data={"sub": db_user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me/", response_model=schemas.User)
def read_current_user(current_user: schemas.User = Depends(get_current_user)):
    logger.info(f"Fetching current user: {current_user.username}")
    return current_user

@router.put("/users/{user_id}/", response_model=schemas.User)
def update_user(
    user_id: int,
    user: schemas.UserUpdate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    logger.info(f"Updating user with ID: {user_id}")
    if current_user.id != user_id and not current_user.is_admin:
        logger.warning(f"User {current_user.username} is not authorized to update user {user_id}")
        raise HTTPException(status_code=403, detail="Not authorized")
    return crud.update_user(db=db, user_id=user_id, user=user)

@router.delete("/users/{user_id}/")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    logger.info(f"Deleting user with ID: {user_id}")
    if current_user.id != user_id and not current_user.is_admin:
        logger.warning(f"User {current_user.username} is not authorized to delete user {user_id}")
        raise HTTPException(status_code=403, detail="Not authorized")
    return crud.delete_user(db=db, user_id=user_id)

@router.get("/users/", response_model=list[schemas.User])
def read_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    logger.info("Fetching all users")
    if not current_user.is_admin:
        logger.warning(f"User {current_user.username} is not authorized to fetch all users")
        raise HTTPException(status_code=403, detail="Not authorized")
    return crud.get_users(db, skip=skip, limit=limit)