from typing import List
from sqlalchemy.orm import Session
import models
import schemas
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Функции для работы с пользователями
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = pwd_context.hash(user.password)
    db_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: int, user: schemas.UserUpdate):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        if user.balance is not None:
            db_user.balance = user.balance
        if user.is_admin is not None:
            db_user.is_admin = user.is_admin
        db.commit()
        db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user

# Функции для работы с играми
def get_games(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Game).offset(skip).limit(limit).all()

def create_game(db: Session, game: schemas.GameCreate):
    db_game = models.Game(name=game.name, description=game.description)
    db.add(db_game)
    db.commit()
    db.refresh(db_game)
    return db_game

# Функции для работы с блэкджеком
def create_blackjack_game(db: Session, blackjack_game: schemas.BlackjackGameCreate, user_id: int):
    db_blackjack_game = models.BlackjackGame(
        user_id=user_id,
        bet_amount=blackjack_game.bet_amount,
        user_cards=",".join(blackjack_game.user_cards),
        dealer_cards=",".join(blackjack_game.dealer_cards),
        status=blackjack_game.status
    )
    db.add(db_blackjack_game)
    db.commit()
    db.refresh(db_blackjack_game)
    return db_blackjack_game

def get_blackjack_game(db: Session, game_id: int):
    return db.query(models.BlackjackGame).filter(models.BlackjackGame.id == game_id).first()

def update_blackjack_game(db: Session, game_id: int, status: str, user_cards: List[str], dealer_cards: List[str]):
    db_game = db.query(models.BlackjackGame).filter(models.BlackjackGame.id == game_id).first()
    if db_game:
        db_game.status = status
        db_game.user_cards = ",".join(user_cards)
        db_game.dealer_cards = ",".join(dealer_cards)
        db.commit()
        db.refresh(db_game)
    return db_game