import json

from redis import Redis, exceptions

# redis = Redis.from_url(url=f'redis://redis:6379/0')

# def search(key: str):
#     return redis.scan_iter(match=key)


class DB:
    def __init__(self):
        self._redis = Redis.from_url(url=f'redis://redis:6379/0')

    @property
    def redis(self) -> 'Redis':
        try:
            self._redis.ping()
        except (exceptions.ConnectionError, exceptions.BusyLoadingError, ):
            self._redis = Redis.from_url(url=f'redis://redis:6379/0')

        return self._redis

    def load(self, key: str) -> str or None:
        """
        loads the value stored under given key
        :param db_id:
        :return: the corresponding value or, if key is not found, None
        """
        return self.redis.get(key)

    def search(self, pattern: str) -> 'iter':
        """
        Find all keys that match given regex pattern
        :param pattern: the regex pattern for db keys
        :return: iterator over values that match the given pattern
        """
        keys = self.redis.scan_iter(match=pattern)
        for key in keys:
            yield self.redis.get(key)

    def exists(self, key: int or str) -> bool:
        """
        Verifies if the exists given key in the db
        :param key: the potential key of the db
        :return: true if the key is in db, false otherwise
        """
        return bool(self.redis.exists(key))

    def save(self, key: str, value: str) -> None:
        """
        Add/update db record for given (key, value) pair
        :param key: the key in the db
        :param value: the value to be stored under the given key in db
        """
        self.redis.set(key, value)

    def delete(self, key: str) -> None:
        """
        Remove the (key, value) pair from the db
        :param key: the key in the db
        """
        self.redis.delete(key)


db = DB()
