from .type import MessageContent

from datetime import datetime
from pytz import timezone

import locale
import httpx
import os
import logging

logger = logging.getLogger(__name__)

class WebhookConfig:
    def __init__(self):
        self.error_url = os.getenv("ERROR_WEBHOOK_URL")
        self.warn_url = os.getenv("WARN_WEBHOOK_URL")
        self.info_url = os.getenv("INFO_WEBHOOK_URL")
        
        try:
            locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
        except locale.Error:
            print("Locale pt_BR.UTF-8 não disponível. Usando padrão.")
            locale.setlocale(locale.LC_ALL, 'Portuguese_Brazil')
            
    async def send_message(self, content: dict, level: str):
        """
        Send the message to a Discord webhook.

        Args:
            content (dict): The content of the message.
            level (str): The webhook level (error_url, warn_url, or info_url)

        Raises:
            Exception: If there is an error sending the message.
        """
        webhook_urls = {
            "error_url": self.error_url,
            "warn_url": self.warn_url,
            "info_url": self.info_url
        }
        
        webhook_url = webhook_urls.get(level)
        if not webhook_url:
            raise ValueError(f"Invalid webhook level: {level}")

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(webhook_url, json=content)
                response.raise_for_status()
                
        except httpx.HTTPStatusError as e:
            raise Exception(f"Error sending message to Discord: {str(e)}")

    async def error_message(self, payload: MessageContent):
        """
        Sends an error message to a Discord webhook with details about the error.

        Args:
            id_error (str): Unique identifier for the error.
            path (str): The URL path where the error occurred.
            method (str): The HTTP method used (e.g., GET, POST).
            ip_adress (str): The IP address of the client.
            user_agent (str): The user agent string of the client.
            error (str): Description of the error encountered.

        Raises:
            Exception: If there is an error sending the message to Discord.
        """

        content = {
            "embeds": [{ 
                "author": {
                    "name": f"{payload.method} {payload.path}",
                    "icon_url": "https://encrypted-tbn3.gstatic.com/images?q=tbn:ANd9GcRUREvlCvHREdbT-Xsf2L2dmgO7AulT-6hqeDRUThJvVKKQwYuPwNatanNGyJiXSwubdlC8iTQHCPxOrsM-uuUCfg"
                },
                "title": ":rotating_light:  Application Error",
                "description": "A problem occurred. See the details below:",
                "color": 13762819,
                "footer": {
                    "text": f"Logged at: {datetime.now(timezone('America/Sao_Paulo')).strftime('%A, %B %d, %Y at %H:%M')} | ID: {payload.id_error}",
                },
                "fields": [
                    {
                        "name": "**User Agent & IP Address**",
                        "value": f"```{payload.user_agent} | {payload.ip_address}```",
                        "inline": True
                    },
                    {
                        "name": "**Error**",
                        "value": f"```{payload.error}```",
                        "inline": False
                    }
                ]
            }]
        }
        
        await self.send_message(content, "error_url")
        
    async def info_message(self, payload: MessageContent):
        """
        Sends an informational message to a Discord webhook with the provided details.

        Args:
            path (str): The URL path related to the information.
            method (str): The HTTP method used (e.g., GET, POST).
            ip_adress (str): The IP address of the client making the request.
            user_agent (str): The user agent string of the client.
            description (str): A brief description of the information.
            message_content (str): Additional content details to be included.

        Raises:
            Exception: If there is an error sending the message to Discord.
        """

        content = {
            "embeds": [{ 
                "author": {
                    "name": f"{payload.method} {payload.path}",
                    "icon_url": "https://encrypted-tbn3.gstatic.com/images?q=tbn:ANd9GcRUREvlCvHREdbT-Xsf2L2dmgO7AulT-6hqeDRUThJvVKKQwYuPwNatanNGyJiXSwubdlC8iTQHCPxOrsM-uuUCfg"
                },
                "title": "Information",
                "description": payload.description,
                "color": 3447003,
                "footer": {
                    "text": f"Logged at: {datetime.now(timezone('America/Sao_Paulo')).strftime('%A, %B %d, %Y at %H:%M')}",
                },
                "fields": [
                    {
                        "name": "**Details**",
                        "value": f"```{payload.content}```",
                        "inline": False
                    },
                    {
                        "name": "**User Agent & IP Address**",
                        "value": f"```{payload.user_agent} | {payload.ip_address}```",
                        "inline": True
                    }
                ]
            }]
        }
        
        await self.send_message(content, "info_url")

    async def warning_message(self, payload: MessageContent):
        """
        Sends a warning message to Discord webhook with timeout and error handling.
        """
        content = {
            "embeds": [{ 
                "author": {
                    "name": f"{payload.method} {payload.path}",
                    "icon_url": "https://encrypted-tbn3.gstatic.com/images?q=tbn:ANd9GcRUREvlCvHREdbT-Xsf2L2dmgO7AulT-6hqeDRUThJvVKKQwYuPwNatanNGyJiXSwubdlC8iTQHCPxOrsM-uuUCfg"
                },
                "title": "Warning",
                "description": payload.description,
                "color": 16766720,
                "footer": {
                    "text": f"Logged at: {datetime.now(timezone('America/Sao_Paulo')).strftime('%A, %B %d, %Y at %H:%M')}",
                },
                "fields": [
                    {
                        "name": "**Details**",
                        "value": f"```{payload.content}```",
                        "inline": False
                    },
                    {
                        "name": "**User Agent & IP Address**",
                        "value": f"```{payload.user_agent} | {payload.ip_address}```",
                        "inline": True
                    }
                ]
            }]
        }
        
        await self.send_message(content, "warn_url")
                
webhook = WebhookConfig()