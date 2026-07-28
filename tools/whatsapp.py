from urllib.parse import quote


class WhatsAppTool:
    """Generate a pre-filled WhatsApp link for contacting Wesley."""

    name = "whatsapp_link"
    description = "Generate a WhatsApp link to message Wesley directly"

    PHONE_NUMBER = "254114578444"

    async def execute(self, query: str = "", message: str = "") -> dict:
        """Generate a WhatsApp link with optional pre-filled message.

        Args:
            query: If called from the agent, this is the user's message.
            message: The message to pre-fill.

        Returns:
            Dict with the WhatsApp link.
        """
        text = message or query or "Hi Wesley, I just chatted with your portfolio bot..."
        encoded = quote(text)
        link = f"https://wa.me/{self.PHONE_NUMBER}?text={encoded}"

        return {
            "link": link,
            "phone": self.PHONE_NUMBER,
            "prefilled_message": text,
        }
