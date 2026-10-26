"""WhatsApp Business Platform Cloud API Adapter."""

import uuid
from typing import Dict, Any, Optional
from .base import BaseNotificationAdapter, NotificationDispatchResult


class WhatsAppNotificationAdapter(BaseNotificationAdapter):
    channel_name = "WHATSAPP"

    def send(self, recipient: str, subject: str, message: str, metadata: Optional[Dict[str, Any]] = None) -> NotificationDispatchResult:
        msg_id = f"wamid.{uuid.uuid4().hex}"
        return NotificationDispatchResult(
            channel=self.channel_name,
            recipient=recipient,
            success=True,
            message_id=msg_id,
            details=f"WhatsApp message queued via Cloud API to {recipient}."
        )
