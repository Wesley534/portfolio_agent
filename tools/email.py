from __future__ import annotations

import logging
import os

import resend

logger = logging.getLogger(__name__)


class EmailTool:
    """Send an email to Wesley via the Resend API."""

    name = "send_email"
    description = "Send an email message to Wesley"

    async def execute(
        self,
        query: str = "",
        to_email: str = "peterwesley484@gmail.com",
        from_name: str = "",
        from_email: str = "",
        message: str = "",
    ) -> dict:
        """Send an email to Wesley.

        Args:
            query: If called directly from the agent, this is the user's message.
            to_email: Recipient email (defaults to Wesley).
            from_name: Sender's name.
            from_email: Sender's email.
            message: The message body.

        Returns:
            Dict with success status and message.
        """
        api_key = os.getenv("RESEND_API_KEY")
        if not api_key:
            return {"success": False, "message": "Email service not configured"}

        resend.api_key = api_key

        # If called from agent without structured fields, parse from query
        if not from_name and query:
            # Agent will have already collected this info — just send
            pass

        try:
            params = {
                "from": "Portfolio Chat <portfolio@yourdomain.com>",
                "to": [to_email],
                "subject": f"Portfolio Chat — Message from {from_name or 'a visitor'}",
                "html": f"""
                    <h2>New Message from Portfolio Chatbot</h2>
                    <p><strong>From:</strong> {from_name} ({from_email})</p>
                    <hr>
                    <p>{message}</p>
                    <hr>
                    <p style="color: #888; font-size: 12px;">
                        Sent via Wesley's Portfolio AI Assistant
                    </p>
                """,
            }
            response = resend.Emails.send(params)
            logger.info("Email sent: %s", response.get("id"))
            return {"success": True, "message": "Email sent successfully"}
        except Exception as e:
            logger.exception("Failed to send email")
            return {"success": False, "message": str(e)}
