from packages.shared.config import get_settings
from redis import Redis


def get_redis_client() -> Redis:
    settings = get_settings()
    
    client = Redis(
        host=settings.redis_host,
        port=settings.redis_port,
        db=settings.redis_db,
        decode_responses=True)
    
    return client