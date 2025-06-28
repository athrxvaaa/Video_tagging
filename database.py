from pymongo import MongoClient
from gridfs import GridFS
from bson import ObjectId
import logging
from config import settings

logger = logging.getLogger(__name__)

class Database:
    def __init__(self):
        self.client = None
        self.db = None
        self.fs = None
        
    def connect(self):
        """Connect to MongoDB"""
        try:
            self.client = MongoClient(settings.MONGODB_URI)
            self.db = self.client[settings.DATABASE_NAME]
            self.fs = GridFS(self.db)
            
            # Test connection
            self.client.admin.command('ping')
            logger.info("Connected to MongoDB")
            
        except Exception as e:
            logger.error(f"Failed to connect to MongoDB: {e}")
            raise
    
    def close(self):
        """Close MongoDB connection"""
        if self.client:
            self.client.close()
            logger.info("MongoDB connection closed")
    
    def get_db(self):
        """Get database instance"""
        return self.db
    
    def get_fs(self):
        """Get GridFS instance"""
        return self.fs

# Global database instance
db = Database() 