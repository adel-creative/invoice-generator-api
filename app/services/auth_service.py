"""
Authentication Service
Handles password hashing, verification, and JWT token creation
"""

from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt, JWTError
from typing import Optional
import hashlib
from ..config import settings

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """
    Hash a password using bcrypt.

    IMPORTANT: bcrypt has a 72-byte limit. We handle this by:
    1. First hashing with SHA256 (produces fixed 32-byte output)
    2. Then applying bcrypt to the hash

    This way:
    - Passwords of any length are accepted
    - Security is maintained (SHA256 + bcrypt)
    - bcrypt limit is never exceeded

    Args:
        password: Plain text password (any length)

    Returns:
        Hashed password string
    """
    # Pre-hash long passwords with SHA256 to fit bcrypt's 72-byte limit
    if len(password.encode('utf-8')) > 72:
        # Hash password with SHA256 first (produces hex string of 64 chars)
        password = hashlib.sha256(password.encode('utf-8')).hexdigest()

    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against its hash.

    Args:
        plain_password: Plain text password to verify
        hashed_password: Hashed password from database

    Returns:
        True if password matches, False otherwise
    """
    # Apply same pre-hashing logic as hash_password
    if len(plain_password.encode('utf-8')) > 72:
        plain_password = hashlib.sha256(
            plain_password.encode('utf-8')).hexdigest()

    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT access token.

    Args:
        data: Dictionary containing user data to encode
        expires_delta: Optional token expiration time

    Returns:
        Encoded JWT token string
    """
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    return encoded_jwt


def decode_access_token(token: str) -> Optional[dict]:
    """
    Decode and validate a JWT token.

    Args:
        token: JWT token string

    Returns:
        Decoded token data if valid, None otherwise
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY,
                             algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        return None
