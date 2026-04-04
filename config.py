import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    API_ID = int(os.getenv('API_ID', '123456'))
    API_HASH = os.getenv('API_HASH', 'your_api_hash')
    BOT_TOKEN = os.getenv('BOT_TOKEN', 'your_bot_token')
    
    # MongoDB Configuration
    MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017')
    MONGODB_DB_NAME = os.getenv('MONGODB_DB_NAME', 'telethon_bot')
    
    # Log Channel
    LOG_CHANNEL_ID = int(os.getenv('LOG_CHANNEL_ID', '-1001234567890'))  # Your log channel ID
    
    # Payment API
    PAYMENT_API_URL = os.getenv('PAYMENT_API_URL', 'http://localhost:8000')
