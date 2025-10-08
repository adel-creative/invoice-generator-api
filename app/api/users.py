"""
User Management API Endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from typing import Optional
from ..database import get_db
from ..models.user import User
from ..schemas.auth import UserResponse
from ..utils.dependencies import get_current_user
from ..services.auth_service import hash_password

router = APIRouter(prefix="/users", tags=["Users"])


class UserUpdate(BaseModel):
    """Schema for updating user profile"""
    full_name: Optional[str] = None
    company_name: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    email: Optional[EmailStr] = None


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """
    Get current user profile
    
    Returns complete user information including payment link
    """
    return current_user


@router.put("/me", response_model=UserResponse)
async def update_user_profile(
    update_data: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update user profile
    
    **Updatable Fields:**
    - full_name: Full name
    - company_name: Company or business name
    - phone: Phone number
    - address: Business address
    - email: Email address (must be unique)
    """
    # Check if email is being changed and if it's already taken
    if update_data.email and update_data.email != current_user.email:
        existing_user = db.query(User).filter(User.email == update_data.email).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        current_user.email = update_data.email
    
    # Update other fields
    if update_data.full_name is not None:
        current_user.full_name = update_data.full_name
    if update_data.company_name is not None:
        current_user.company_name = update_data.company_name
    if update_data.phone is not None:
        current_user.phone = update_data.phone
    if update_data.address is not None:
        current_user.address = update_data.address
    
    db.commit()
    db.refresh(current_user)
    
    return current_user


@router.get("/me/stats")
async def get_user_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get user statistics
    
    Returns summary of invoices and totals
    """
    from ..models.invoice import Invoice
    from sqlalchemy import func
    
    # Total invoices
    total_invoices = db.query(Invoice).filter(
        Invoice.user_id == current_user.id
    ).count()
    
    # Invoices by status
    status_counts = db.query(
        Invoice.status,
        func.count(Invoice.id)
    ).filter(
        Invoice.user_id == current_user.id
    ).group_by(Invoice.status).all()
    
    status_dict = {status: count for status, count in status_counts}
    
    # Total revenue (sum of all paid invoices)
    total_revenue = db.query(func.sum(Invoice.total)).filter(
        Invoice.user_id == current_user.id,
        Invoice.status == "paid"
    ).scalar() or 0
    
    # Pending amount (sum of sent but not paid invoices)
    pending_amount = db.query(func.sum(Invoice.total)).filter(
        Invoice.user_id == current_user.id,
        Invoice.status == "sent"
    ).scalar() or 0
    
    return {
        "total_invoices": total_invoices,
        "status_breakdown": {
            "draft": status_dict.get("draft", 0),
            "sent": status_dict.get("sent", 0),
            "paid": status_dict.get("paid", 0),
            "cancelled": status_dict.get("cancelled", 0)
        },
        "total_revenue": round(total_revenue, 2),
        "pending_amount": round(pending_amount, 2),
        "payment_link": current_user.payment_link
    }