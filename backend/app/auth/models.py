"""Authentication and User Data Models with RBAC."""

from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, Field


class UserRole(str, Enum):
    ADMIN = "ADMIN"
    SUPERVISOR = "SUPERVISOR"
    OPERATOR = "OPERATOR"
    VIEWER = "VIEWER"


class UserBase(BaseModel):
    email: str = Field(..., description="User email address")
    full_name: str
    tenant_id: str = "demo_tenant_dubai"
    role: UserRole = UserRole.OPERATOR
    is_active: bool = True


class UserCreate(UserBase):
    password: str = Field(..., min_length=8)


class UserLogin(BaseModel):
    email: str = Field(..., description="User email address")
    password: str


class UserResponse(UserBase):
    user_id: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in_seconds: int
    user: UserResponse


class ApprovalDecision(BaseModel):
    """Payload for human supervisor approving or rejecting a high-risk task."""
    task_id: str
    approval_token: str
    decision: str  # "APPROVE" or "REJECT"
    comments: Optional[str] = None
