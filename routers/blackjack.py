from typing import List  # Добавляем импорт
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import crud
import schemas
from database import get_db
from auth import get_current_user
from blackjack import deal_card, calculate_hand_value, determine_winner
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/blackjack/start/", response_model=schemas.BlackjackGame)
def start_blackjack_game(
    bet_amount: float,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    logger.info(f"User {current_user.username} starting a new Blackjack game with bet: {bet_amount}")

    if current_user.balance < bet_amount:
        logger.warning(f"User {current_user.username} has insufficient balance")
        raise HTTPException(status_code=400, detail="Not enough balance")

    user_hand = [deal_card(), deal_card()]
    dealer_hand = [deal_card(), deal_card()]

    blackjack_game = schemas.BlackjackGameCreate(
        bet_amount=bet_amount,
        user_cards=user_hand,
        dealer_cards=dealer_hand,
        status="in_progress"
    )
    db_game = crud.create_blackjack_game(db=db, blackjack_game=blackjack_game, user_id=current_user.id)

    current_user.balance -= bet_amount
    db.commit()

    return db_game

@router.post("/blackjack/hit/{game_id}/", response_model=schemas.BlackjackGame)
def hit_blackjack_game(
    game_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    logger.info(f"User {current_user.username} hitting in Blackjack game {game_id}")

    db_game = crud.get_blackjack_game(db, game_id=game_id)
    if not db_game or db_game.user_id != current_user.id:
        logger.warning(f"Game {game_id} not found or unauthorized")
        raise HTTPException(status_code=404, detail="Game not found")

    if db_game.status != "in_progress":
        logger.warning(f"Game {game_id} is already finished")
        raise HTTPException(status_code=400, detail="Game is already finished")

    user_hand = db_game.user_cards.split(",")
    user_hand.append(deal_card())
    db_game.user_cards = ",".join(user_hand)

    if calculate_hand_value(user_hand) > 21:
        db_game.status = "lose"
        db.commit()
        return db_game

    db.commit()
    return db_game

@router.post("/blackjack/stand/{game_id}/", response_model=schemas.BlackjackGame)
def stand_blackjack_game(
    game_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user)
):
    logger.info(f"User {current_user.username} standing in Blackjack game {game_id}")

    db_game = crud.get_blackjack_game(db, game_id=game_id)
    if not db_game or db_game.user_id != current_user.id:
        logger.warning(f"Game {game_id} not found or unauthorized")
        raise HTTPException(status_code=404, detail="Game not found")

    if db_game.status != "in_progress":
        logger.warning(f"Game {game_id} is already finished")
        raise HTTPException(status_code=400, detail="Game is already finished")

    dealer_hand = db_game.dealer_cards.split(",")
    while calculate_hand_value(dealer_hand) < 17:
        dealer_hand.append(deal_card())

    user_hand = db_game.user_cards.split(",")
    status = determine_winner(user_hand, dealer_hand)
    db_game.status = status
    db_game.dealer_cards = ",".join(dealer_hand)

    if status == "win":
        current_user.balance += db_game.bet_amount * 2
    elif status == "draw":
        current_user.balance += db_game.bet_amount

    db.commit()
    return db_game