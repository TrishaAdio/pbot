from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime
from config import Config
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Database:
    def __init__(self):
        self.client = None
        self.db = None
        self.users = None
        self.purchases = None
        
    async def init_db(self):
        """Initialize MongoDB connection"""
        self.client = AsyncIOMotorClient(Config.MONGODB_URI)
        self.db = self.client[Config.MONGODB_DB_NAME]
        self.users = self.db.users
        self.purchases = self.db.purchases
        
        # Create indexes for better performance
        await self.users.create_index("user_id", unique=True)
        await self.users.create_index("username")
        await self.purchases.create_index("user_id")
        await self.purchases.create_index("purchase_date")
        
        logger.info(f"MongoDB connected to database: {Config.MONGODB_DB_NAME}")
        
    async def close(self):
        """Close MongoDB connection"""
        if self.client:
            self.client.close()
            logger.info("MongoDB connection closed")
        
    async def add_user(self, user_id: int, username: str, first_name: str, last_name: str = None):
        """Add or update user in database"""
        try:
            user_data = {
                "user_id": user_id,
                "username": username,
                "first_name": first_name,
                "last_name": last_name,
                "created_at": datetime.now(),
                "updated_at": datetime.now()
            }
            
            # Update if exists, insert if not
            result = await self.users.update_one(
                {"user_id": user_id},
                {"$set": user_data},
                upsert=True
            )
            
            if result.upserted_id:
                logger.info(f"Added new user: {user_id}")
            else:
                logger.info(f"Updated user: {user_id}")
                
        except Exception as e:
            logger.error(f"Error adding user {user_id}: {e}")
            
    async def add_purchase(self, user_id: int, plan: str, price: float, package_type: str = None):
        """Add purchase record"""
        try:
            purchase_data = {
                "user_id": user_id,
                "plan": plan,
                "price": price,
                "package_type": package_type,
                "purchase_date": datetime.now()
            }
            
            result = await self.purchases.insert_one(purchase_data)
            logger.info(f"Added purchase for user {user_id}: {plan} - ${price}")
            return result.inserted_id
            
        except Exception as e:
            logger.error(f"Error adding purchase for user {user_id}: {e}")
            
    async def get_user_purchases(self, user_id: int, limit: int = 50):
        """Get user's purchase history"""
        try:
            cursor = self.purchases.find(
                {"user_id": user_id}
            ).sort("purchase_date", -1).limit(limit)
            
            purchases = []
            async for purchase in cursor:
                purchases.append({
                    'plan': purchase.get('plan'),
                    'price': purchase.get('price'),
                    'package_type': purchase.get('package_type'),
                    'date': purchase.get('purchase_date').strftime("%Y-%m-%d %H:%M"),
                    'purchase_id': str(purchase.get('_id'))
                })
            
            return purchases
            
        except Exception as e:
            logger.error(f"Error getting purchases for user {user_id}: {e}")
            return []
            
    async def get_total_spent(self, user_id: int):
        """Get total amount spent by user"""
        try:
            pipeline = [
                {"$match": {"user_id": user_id}},
                {"$group": {"_id": None, "total": {"$sum": "$price"}}}
            ]
            
            cursor = self.purchases.aggregate(pipeline)
            result = await cursor.to_list(length=1)
            
            if result:
                return result[0]['total']
            return 0
            
        except Exception as e:
            logger.error(f"Error getting total spent for user {user_id}: {e}")
            return 0
            
    async def get_user(self, user_id: int):
        """Get user details"""
        try:
            user = await self.users.find_one({"user_id": user_id})
            return user
        except Exception as e:
            logger.error(f"Error getting user {user_id}: {e}")
            return None
            
    async def get_all_users(self, skip: int = 0, limit: int = 100):
        """Get all users with pagination"""
        try:
            cursor = self.users.find({}).skip(skip).limit(limit)
            users = []
            async for user in cursor:
                users.append(user)
            return users
        except Exception as e:
            logger.error(f"Error getting all users: {e}")
            return []
            
    async def get_user_count(self):
        """Get total number of users"""
        try:
            count = await self.users.count_documents({})
            return count
        except Exception as e:
            logger.error(f"Error getting user count: {e}")
            return 0
            
    async def get_purchase_count(self, user_id: int = None):
        """Get purchase count for a user or all purchases"""
        try:
            if user_id:
                count = await self.purchases.count_documents({"user_id": user_id})
            else:
                count = await self.purchases.count_documents({})
            return count
        except Exception as e:
            logger.error(f"Error getting purchase count: {e}")
            return 0
            
    async def get_recent_purchases(self, limit: int = 10):
        """Get recent purchases across all users"""
        try:
            cursor = self.purchases.find().sort("purchase_date", -1).limit(limit)
            purchases = []
            async for purchase in cursor:
                # Get user info
                user = await self.get_user(purchase.get('user_id'))
                purchases.append({
                    'user': user,
                    'purchase': purchase
                })
            return purchases
        except Exception as e:
            logger.error(f"Error getting recent purchases: {e}")
            return []
            
    async def delete_user(self, user_id: int):
        """Delete user and their purchases"""
        try:
            # Delete user
            user_result = await self.users.delete_one({"user_id": user_id})
            # Delete user's purchases
            purchase_result = await self.purchases.delete_many({"user_id": user_id})
            
            logger.info(f"Deleted user {user_id} and {purchase_result.deleted_count} purchases")
            return user_result.deleted_count > 0
            
        except Exception as e:
            logger.error(f"Error deleting user {user_id}: {e}")
            return False

# Initialize database instance
db = Database()
