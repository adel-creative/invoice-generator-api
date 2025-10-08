"""
User Schemas
Additional user-related Pydantic models
"""

from pydantic import BaseModel, EmailStr
from typing import Optional


class UserBase(BaseModel):
    """Base user schema"""
    email: EmailStr
    username: str
    full_name: Optional[str] = None
    company_name: Optional[str] = None


class UserCreate(BaseModel):
    """Schema for creating user"""
    email: EmailStr
    username: str
    password: str
    full_name: Optional[str] = None
    company_name: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None


class UserInDB(UserBase):
    """User in database schema"""
    id: int
    is_active: bool
    is_verified: bool
    payment_link: Optional[str] = None
    
    class Config:
        from_attributes = True