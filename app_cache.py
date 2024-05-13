
from flask_caching import Cache
from settings import FLASK_CACHE_CONFIG, REDIS_HOST, REDIS_PORT

class AppCache:
    def __new__(cls, app = None):
        if not hasattr(cls, 'instance'):
            cls.instance = super(AppCache, cls).__new__(cls)
            cls.instance._cache = Cache(app, config=FLASK_CACHE_CONFIG)
        return cls.instance

    _cache = None

    def Cache(self):
        return self._cache
    