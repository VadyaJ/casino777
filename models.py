from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    balance = Column(Float, default=100.0)
    is_admin = Column(Boolean, default=False)

class Game(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String)

class BlackjackGame(Base):
    __tablename__ = "blackjack_games"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    bet_amount = Column(Float)
    user_cards = Column(String)
    dealer_cards = Column(String)
    status = Column(String)

    user = relationship("User", back_populates="blackjack_games")

User.blackjack_games = relationship("BlackjackGame", back_populates="user")