import aiohttp
import asyncio
from config import Config
import logging

logger = logging.getLogger(__name__)

class PaymentAPI:
    def __init__(self):
        self.base_url = Config.PAYMENT_API_URL
    
    async def create_invoice(self, amount: int, merchant_name: str, merchant_desc: str):
        """Create invoice and get payment amount"""
        try:
            async with aiohttp.ClientSession() as session:
                payload = {
                    "amount": amount,
                    "merchant_name": merchant_name,
                    "merchant_desc": merchant_desc
                }
                
                async with session.post(f"{self.base_url}/create", json=payload) as resp:
                    if resp.status == 200:
                        result = await resp.json()
                        unique_amount = result.get('unique_amount', amount)
                        return {
                            'success': True,
                            'unique_amount': unique_amount,
                            'original_amount': amount
                        }
                    else:
                        return {'success': False, 'error': f"HTTP {resp.status}"}
        except Exception as e:
            logger.error(f"Payment API error: {e}")
            return {'success': False, 'error': str(e)}
    
    async def check_payment(self, amount: float):
        """Check if payment is completed"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.base_url}/verify?amount={amount}") as resp:
                    if resp.status == 200:
                        result = await resp.json()
                        if result.get('status') == 'success' or result.get('verified'):
                            return {'success': True, 'paid': True}
                        else:
                            return {'success': True, 'paid': False}
                    else:
                        return {'success': False, 'paid': False}
        except Exception as e:
            logger.error(f"Payment check error: {e}")
            return {'success': False, 'paid': False, 'error': str(e)}

payment_api = PaymentAPI()
