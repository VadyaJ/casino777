from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import crud
import schemas
from database import get_db
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/games/", response_model=list[schemas.Game])
def read_games(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    logger.info("Fetching all games")
    return crud.get_games(db, skip=skip, limit=limit)

@router.post("/games/", response_model=schemas.Game)
def create_game(game: schemas.GameCreate, db: Session = Depends(get_db)):
    logger.info(f"Creating new game: {game.name}")
    return crud.create_game(db=db, game=game)