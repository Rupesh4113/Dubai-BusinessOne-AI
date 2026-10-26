"""Base Notification Adapter Interface."""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from pydantic import BaseModel


class NotificationDispatchResult(BaseModel):
    channel: str
    recipient: str
    success: bool
    message_id: str
    details: Optional[str] = None


class BaseNotificationAdapter(ABC):
    channel_name: str

    @abstractmethod
    def send(self, recipient: str, subject: str, message: str, metadata: Optional[Dict[str, Any]] = None) -> NotificationDispatchResult:
        pass
