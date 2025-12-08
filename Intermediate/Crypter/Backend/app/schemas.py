# app/schemas.py
from pydantic import BaseModel, EmailStr
import uuid

# Schema for creating a user (request)
class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str

# Schema for user response (omitting password)
class UserOut(BaseModel):
    id: uuid.UUID
    email: EmailStr
    username: str

    class Config:
        orm_mode = True

# Schema for login request
class UserLogin(BaseModel):
    username: str
    password: str

# Schema for token response
class Token(BaseModel):
    access_token: str
    token_type: str