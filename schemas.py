from pydantic import BaseModel, EmailStr
from typing import List

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class UserUpdate(BaseModel):
    balance: float = None
    is_admin: bool = None

class User(UserBase):
    id: int
    balance: float
    is_admin: bool

    class Config:
        from_attributes = True

class GameBase(BaseModel):
    name: str
    description: str

class GameCreate(GameBase):
    pass

class Game(GameBase):
    id: int

    class Config:
        from_attributes = True

class BlackjackGameBase(BaseModel):
    bet_amount: float
    user_cards: List[str] = []
    dealer_cards: List[str] = []
    status: str = "in_progress"

class BlackjackGameCreate(BlackjackGameBase):
    pass

class BlackjackGame(BlackjackGameBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str = None