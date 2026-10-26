"""Security, cryptographic hashing, and JWT token management."""

import hashlib
import hmac
import os
import time
from typing import Optional, Dict, Any
import jwt
from ..config import settings

# Salt length and iterations for PBKDF2-HMAC-SHA256
SALT_LENGTH = 16
ITERATIONS = 100_000


def hash_password(password: str) -> str:
    """Securely hash a password with random salt using PBKDF2-HMAC-SHA256."""
    salt = os.urandom(SALT_LENGTH)
    key = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, ITERATIONS)
    return f"{salt.hex()}:{key.hex()}"


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies a plain password against the stored salt:hash string."""
    try:
        salt_hex, key_hex = hashed_password.split(":")
        salt = bytes.fromhex(salt_hex)
        expected_key = bytes.fromhex(key_hex)
        actual_key = hashlib.pbkdf2_hmac("sha256", plain_password.encode("utf-8"), salt, ITERATIONS)
        return hmac.compare_digest(actual_key, expected_key)
    except Exception:
        return False


def create_access_token(data: Dict[str, Any], expires_delta_seconds: Optional[int] = None) -> str:
    """Creates a signed JWT access token with role, tenant_id, and expiration."""
    to_encode = data.copy()
    expire_epoch = time.time() + (expires_delta_seconds or (settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60))
    to_encode.update({"exp": expire_epoch, "iat": time.time()})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def decode_access_token(token: str) -> Optional[Dict[str, Any]]:
    """Decodes and validates JWT token signature and expiry."""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        return payload
    except jwt.PyJWTError:
        return None
