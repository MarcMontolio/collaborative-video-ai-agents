from packages.shared.redis.client import get_redis_client


def test_redis_client() -> None:
    client = get_redis_client()
    
    data = client.connection_pool.connection_kwargs
    
    assert data["host"] == "localhost"
    assert data["port"] == 6379
    assert data["db"] == 0
    assert data["decode_responses"] is True