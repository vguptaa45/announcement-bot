import os
import json
import requests
from typing import List, Dict, Optional
from dotenv import load_dotenv
from supabase import create_client, Client
import logging

logger = logging.getLogger(__name__)
load_dotenv()

class AnnouncementMessageSender:
    def __init__(self):
        self.supabase: Client = create_client(
            os.getenv("SUPABASE_URL"),
            os.getenv("SUPABASE_KEY")
        )
        self.api_key = os.getenv("GUPSHUP_API_KEY")
        self.app_name = os.getenv("GUPSHUP_APP_NAME")
        self.source = "919920660174"
        self.base_url = "https://api.gupshup.io/wa/api/v1"
        self.template_id = "2f891418-a124-44ee-b645-69e13bf11e9d"

    def _format_phone_number(self, phone: str) -> str:
        """Format phone number to match Gupshup requirements"""
        # Remove any whatsapp: prefix
        phone = phone.replace("whatsapp:", "")
        
        # Remove any spaces, dashes, or parentheses
        phone = ''.join(filter(str.isdigit, phone))
        
        # Add country code (91 for India) if not present
        if not phone.startswith('91'):
            phone = '91' + phone
        
        return phone

    def send_template_message(self, to: str, params: List[str]) -> dict:
        """Send template message using Gupshup API"""
        try:
            destination = self._format_phone_number(to)
            url = f"{self.base_url}/template/msg"
            
            # Format template data
            template_data = {
                "id": self.template_id,
                "params": params
            }
            
            payload = {
                "channel": "whatsapp",
                "source": self.source,
                "destination": destination,
                "template": json.dumps(template_data),
                "src.name": self.app_name
            }
            
            headers = {
                "Cache-Control": "no-cache",
                "Content-Type": "application/x-www-form-urlencoded",
                "apikey": self.api_key
            }
            
            logger.info(f"Sending template message to {destination}")
            logger.debug(f"Template payload: {json.dumps(payload, indent=2)}")
            
            response = requests.post(url, data=payload, headers=headers)
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error sending template message: {str(e)}")
            if 'response' in locals():
                logger.error(f"Response: {response.text}")
            raise
        except Exception as e:
            logger.error(f"Failed to send template message to {to}: {str(e)}")
            raise

    def get_subscribers(self, stock_name: str) -> List[str]:
        """Get all phone numbers subscribed to a particular stock"""
        try:
            response = self.supabase.table('stocks_wishlist') \
                .select('user_list') \
                .eq('company_id', stock_name) \
                .execute()
            
            if response.data and response.data[0]['user_list']:
                return response.data[0]['user_list']
            return []
        except Exception as e:
            logger.error(f"Error fetching subscribers: {e}")
            return []

    def send_announcement(self, announcement: Dict) -> None:
        """Send announcement to all subscribers of the stock"""
        try:
            stock_name = f"📊 {announcement['stock_name']}"
            subscribers = self.get_subscribers(announcement['stock_name'])
            
            if not subscribers:
                logger.info(f"No subscribers found for {stock_name}")
                return

            # Prepare template parameters with emoji in stock name
            template_params = [
                stock_name,  # Header {{1}}
                announcement['title'],  # Body {{1}}
                announcement['summary']  # Body {{2}}
            ]

            logger.info(f"Sending announcement to {len(subscribers)} subscribers for {stock_name}")
            
            for phone_number in subscribers:
                try:
                    response = self.send_template_message(
                        to=phone_number,
                        params=template_params
                    )
                    logger.info(f"Successfully sent to {phone_number}")
                    logger.debug(f"Response: {response}")
                except Exception as e:
                    logger.error(f"Failed to send to {phone_number}: {e}")

        except Exception as e:
            logger.error(f"Error in send_announcement: {e}") 