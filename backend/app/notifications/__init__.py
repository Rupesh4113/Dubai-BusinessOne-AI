"""Notification package."""

from .base import BaseNotificationAdapter, NotificationDispatchResult
from .email_adapter import EmailNotificationAdapter
from .whatsapp_adapter import WhatsAppNotificationAdapter
from .teams_adapter import TeamsNotificationAdapter
from .webhook_adapter import WebhookNotificationAdapter

email_adapter = EmailNotificationAdapter()
whatsapp_adapter = WhatsAppNotificationAdapter()
teams_adapter = TeamsNotificationAdapter()
webhook_adapter = WebhookNotificationAdapter()

__all__ = [
    "BaseNotificationAdapter",
    "NotificationDispatchResult",
    "EmailNotificationAdapter",
    "WhatsAppNotificationAdapter",
    "TeamsNotificationAdapter",
    "WebhookNotificationAdapter",
    "email_adapter",
    "whatsapp_adapter",
    "teams_adapter",
    "webhook_adapter"
]
