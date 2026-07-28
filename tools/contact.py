class ContactTool:
    """Provide Wesley's contact information."""

    name = "contact_info"
    description = "Get Wesley's contact information — email, LinkedIn, WhatsApp, GitHub, Twitter"

    CONTACT_INFO = {
        "email": "peterwesley484@gmail.com",
        "whatsapp": "+254114578444",
        "whatsapp_link": "https://wa.me/254114578444",
        "linkedin": "https://www.linkedin.com/in/peter-wesley-22b744268",
        "github": "https://github.com/Wesley534",
        "twitter": "https://x.com/@Wesley467954392",
        "location": "Nairobi, Kenya",
    }

    async def execute(self, query: str = "") -> dict:
        """Return Wesley's contact information."""
        return self.CONTACT_INFO
