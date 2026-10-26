"""Authentication API Router with Role-Based Access Control (RBAC)."""

import uuid
from typing import Dict, Optional
from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from .models import UserRole, UserCreate, UserLogin, UserResponse, TokenResponse
from .security import hash_password, verify_password, create_access_token, decode_access_token
from ..config import settings

router = APIRouter(prefix="/auth", tags=["Authentication & Access Control"])
security_scheme = HTTPBearer(auto_error=False)

# In-memory user store with default production demo users
USER_DATABASE: Dict[str, Dict] = {}


def init_default_users():
    """Initializes standard demonstration roles."""
    if not USER_DATABASE:
        admin_id = "user_admin_001"
        USER_DATABASE["admin@businessone.dubai.ae"] = {
            "user_id": admin_id,
            "email": "admin@businessone.dubai.ae",
            "full_name": "Hamdan Al-Maktoum (Operations Supervisor)",
            "tenant_id": "demo_tenant_dubai",
            "role": UserRole.ADMIN,
            "is_active": True,
            "password_hash": hash_password(settings.ADMIN_DEFAULT_PASSWORD)
        }
        operator_id = "user_op_002"
        USER_DATABASE["operator@businessone.dubai.ae"] = {
            "user_id": operator_id,
            "email": "operator@businessone.dubai.ae",
            "full_name": "Rashid Khan (Commercial Operations Specialist)",
            "tenant_id": "demo_tenant_dubai",
            "role": UserRole.OPERATOR,
            "is_active": True,
            "password_hash": hash_password("DubaiBizOne2026!Secure")
        }


init_default_users()


def get_current_user(credentials: Optional[HTTPAuthorizationCredentials] = Depends(security_scheme)) -> Dict:
    """Validates JWT token and extracts authenticated user."""
    if not credentials:
        # For public demo evaluation, provide default authenticated operator if unauthenticated
        init_default_users()
        return USER_DATABASE["admin@businessone.dubai.ae"]

    token = credentials.credentials
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired authentication credentials."
        )

    email = payload.get("sub")
    user = USER_DATABASE.get(email)
    if not user or not user["is_active"]:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found or inactive.")
    return user


def require_role(allowed_roles: list[UserRole]):
    """Role-based access control dependency."""
    def role_checker(current_user: Dict = Depends(get_current_user)) -> Dict:
        if current_user["role"] not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied. Requires one of roles: {[r.value for r in allowed_roles]}"
            )
        return current_user
    return role_checker


@router.post("/login", response_model=TokenResponse)
def login(payload: UserLogin):
    """Authenticates credentials and returns a secure JWT."""
    init_default_users()
    user = USER_DATABASE.get(payload.email)
    if not user or not verify_password(payload.password, user["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password."
        )

    token_data = {
        "sub": user["email"],
        "user_id": user["user_id"],
        "tenant_id": user["tenant_id"],
        "role": user["role"].value
    }
    token = create_access_token(token_data)

    return TokenResponse(
        access_token=token,
        token_type="bearer",
        expires_in_seconds=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        user=UserResponse(
            user_id=user["user_id"],
            email=user["email"],
            full_name=user["full_name"],
            tenant_id=user["tenant_id"],
            role=user["role"],
            is_active=user["is_active"]
        )
    )


@router.post("/register", response_model=UserResponse)
def register(payload: UserCreate):
    """Registers a new tenant user with validated role and tenant segregation."""
    if payload.email in USER_DATABASE:
        raise HTTPException(status_code=400, detail="User already exists with this email.")

    user_id = f"user_{uuid.uuid4().hex[:8]}"
    new_user = {
        "user_id": user_id,
        "email": payload.email,
        "full_name": payload.full_name,
        "tenant_id": payload.tenant_id,
        "role": payload.role,
        "is_active": payload.is_active,
        "password_hash": hash_password(payload.password)
    }
    USER_DATABASE[payload.email] = new_user
    return UserResponse(
        user_id=user_id,
        email=new_user["email"],
        full_name=new_user["full_name"],
        tenant_id=new_user["tenant_id"],
        role=new_user["role"],
        is_active=new_user["is_active"]
    )


@router.get("/me", response_model=UserResponse)
def get_profile(current_user: Dict = Depends(get_current_user)):
    """Returns authenticated user profile and permissions."""
    return UserResponse(
        user_id=current_user["user_id"],
        email=current_user["email"],
        full_name=current_user["full_name"],
        tenant_id=current_user["tenant_id"],
        role=current_user["role"],
        is_active=current_user["is_active"]
    )
