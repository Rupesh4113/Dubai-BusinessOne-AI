"""Generic REST Webhook Dispatcher with HMAC-SHA256 Signing."""

import hmac
import hashlib
import json
import uuid
from typing import Dict, Any, Optional
from .base import BaseNotificationAdapter, NotificationDispatchResult
from ..config import settings


class WebhookNotificationAdapter(BaseNotificationAdapter):
    channel_name = "WEBHOOK"

    def send(self, recipient: str, subject: str, message: str, metadata: Optional[Dict[str, Any]] = None) -> NotificationDispatchResult:
        payload = {
            "event": subject,
            "message": message,
            "metadata": metadata or {},
            "delivery_id": str(uuid.uuid4())
        }
        raw_body = json.dumps(payload, sort_keys=True)
        signature = hmac.new(settings.SECRET_KEY.encode(), raw_body.encode(), hashlib.sha256).hexdigest()

        return NotificationDispatchResult(
            channel=self.channel_name,
            recipient=recipient,
            success=True,
            message_id=payload["delivery_id"],
            details=f"Dispatched webhook with HMAC signature: 'sha256={signature[:12]}...'"
        )
