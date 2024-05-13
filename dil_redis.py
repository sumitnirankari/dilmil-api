
import redis
from settings import REDIS_HOST, REDIS_PORT

class DilRedis:
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(DilRedis, cls).__new__(cls)
        return cls.instance

    _redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)
    _redis_available = None
    _enable_redis = True

    def redis_client(self):
        return self._redis_client

    def available(self):
        if self._enable_redis and self._redis_available is None:
            try:
                self._redis_available = self._redis_client.ping()
            except:
                self._redis_available = False
        return self._enable_redis and self._redis_available
    