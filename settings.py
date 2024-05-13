import os
from dotenv import load_dotenv

load_dotenv()
REDIS_ENABLED = bool(os.getenv("REDIS_ENABLED", 'True'))
REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = os.getenv("REDIS_PORT", "6379")
REDIS_URL = os.getenv("REDIS_URL", 'redis://redis:6379')
QUEUES = ["emails", "default"]
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

CACHE_TYPE = 'redis'
CACHE_KEY_PREFIX = 'fcache'

FLASK_CACHE_CONFIG = {
    'CACHE_TYPE':  CACHE_TYPE,
    'CACHE_KEY_PREFIX': CACHE_KEY_PREFIX,
    'CACHE_REDIS_HOST': REDIS_HOST,
    'CACHE_REDIS_PORT': REDIS_PORT,
    'CACHE_REDIS_URL': REDIS_URL
    }