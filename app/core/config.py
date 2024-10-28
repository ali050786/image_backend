import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Unsplash credentials
    UNSPLASH_ACCESS_KEY = os.getenv('UNSPLASH_ACCESS_KEY')
    UNSPLASH_SECRET_KEY = os.getenv('UNSPLASH_SECRET_KEY')
    
    # Cache settings
    CACHE_TYPE = "SimpleCache"  # Can be "SimpleCache", "RedisCache", etc.
    CACHE_DEFAULT_TIMEOUT = 300  # 5 minutes
    CACHE_THRESHOLD = 1000  # Maximum number of items the cache will store
    
    # Optional: Redis cache settings (if using RedisCache)
    # CACHE_REDIS_HOST = "localhost"
    # CACHE_REDIS_PORT = 6379