from pydantic import BaseModel, Field, EmailStr

class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, example="testuser")
    email: EmailStr = Field(..., example="test@example.com")

class UserCreate(UserBase):
    password: str = Field(..., min_length=6, max_length=50, example="strongpassword")

class User(UserBase):
    id: int
    balance: float

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str = None