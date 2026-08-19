from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    role: str
    user_id: str
    customer_id: Optional[str] = None
    email: str
    name: str


class TokenPayload(BaseModel):
    sub: Optional[str] = None
    role: Optional[str] = None
    type: Optional[str] = None


class UserBase(BaseModel):
    email: str
    full_name: str
    role: str = "CUSTOMER"  # ADMIN, ANALYST, CUSTOMER


class UserCreate(UserBase):
    password: str = Field(..., min_length=6)


class UserLogin(BaseModel):
    email: str
    password: str


class UserOut(UserBase):
    id: str
    is_active: bool
    created_at: datetime
    customer_id: Optional[str] = None

    class Config:
        from_attributes = True


class RefreshTokenRequest(BaseModel):
    refresh_token: str
