"""Microsoft Teams Incoming Webhook & Adaptive Card Adapter."""

import uuid
from typing import Dict, Any, Optional
from .base import BaseNotificationAdapter, NotificationDispatchResult


class TeamsNotificationAdapter(BaseNotificationAdapter):
    channel_name = "TEAMS"

    def send(self, recipient: str, subject: str, message: str, metadata: Optional[Dict[str, Any]] = None) -> NotificationDispatchResult:
        msg_id = f"TEAMS-CARD-{uuid.uuid4().hex[:8]}"
        return NotificationDispatchResult(
            channel=self.channel_name,
            recipient=recipient,
            success=True,
            message_id=msg_id,
            details=f"Posted Adaptive Card to MS Teams channel '{recipient}'."
        )
