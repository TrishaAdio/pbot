import aiohttp
import asyncio
import json
from config import Config
import logging

logger = logging.getLogger(__name__)

class PaymentAPI:
    def __init__(self):
        self.base_url = Config.PAYMENT_API_URL
    
    async def create_invoice(self, amount: int, merchant_name: str, merchant_desc: str):
        """Create invoice and get payment details"""
        try:
            async with aiohttp.ClientSession() as session:
                payload = {
                    "amount": amount,
                    "merchant_name": merchant_name,
                    "merchant_desc": merchant_desc
                }
                
                print(f"[PAYMENT API] Creating invoice: {payload}")
                
                async with session.post(f"{self.base_url}/create", json=payload) as resp:
                    response_text = await resp.text()
                    print(f"[PAYMENT API] Response: {response_text}")
                    
                    if resp.status == 200:
                        result = await resp.json()
                        # The API returns unique_amount that user needs to pay
                        unique_amount = result.get('unique_amount', amount)
                        return {
                            'success': True,
                            'unique_amount': unique_amount,
                            'original_amount': amount,
                            'full_response': result
                        }
                    else:
                        return {'success': False, 'error': f"HTTP {resp.status}: {response_text}"}
        except Exception as e:
            logger.error(f"Payment API error: {e}")
            return {'success': False, 'error': str(e)}
    
    async def check_payment(self, amount: float):
        """Check if payment is completed"""
        try:
            async with aiohttp.ClientSession() as session:
                print(f"[PAYMENT API] Checking payment for amount: {amount}")
                
                async with session.get(f"{self.base_url}/verify?amount={amount}") as resp:
                    response_text = await resp.text()
                    print(f"[PAYMENT API] Verify response: {response_text}")
                    
                    if resp.status == 200:
                        result = await resp.json()
                        # Check if payment is verified/successful
                        if result.get('status') == 'success' or result.get('verified') or result.get('paid'):
                            return {'success': True, 'paid': True, 'data': result}
                        else:
                            return {'success': True, 'paid': False, 'data': result}
                    else:
                        return {'success': False, 'paid': False, 'error': f"HTTP {resp.status}"}
        except Exception as e:
            logger.error(f"Payment check error: {e}")
            return {'success': False, 'paid': False, 'error': str(e)}

payment_api = PaymentAPI()
