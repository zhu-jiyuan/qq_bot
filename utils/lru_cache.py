from utils import date

class LruCache:
    __slots__ = ['lifetime', 'cache_dict']

    class _CacheNode:
        __slots__ = ['value', 'expire_ts']

        # lifetime: seconds
        def __init__(self, value, lifetime: int):
            self.value = value
            self.expire_ts = date.second() + lifetime

        def get(self):
            return self.value

        def is_expired(self):
            return date.second() >= self.expire_ts
        
        def update_expire_ts(self, lifetime):
            self.expire_ts = date.second() + lifetime


    def __init__(self, lifetime):
        self.lifetime = lifetime
        self.cache_dict = {}

    def set(self, key, value):
        self.cache_dict[key] = self._CacheNode(value, self.lifetime)

    def get(self, key):
        if key not in self.cache_dict:
            return None

        ret = self.cache_dict[key]
        ret.update_expire_ts(self.lifetime)
        return ret.get()
        
    def delete(self, key):
        if key in self.cache_dict:
            del self.cache_dict[key]

    def clean(self)->list:
        keys_to_delete = []
        del_values = []

        for key, value in self.cache_dict.items():
            if value.is_expired():
                keys_to_delete.append(key)
                del_values.append(value.get())

        for key in keys_to_delete:
            self.delete(key)

        return del_values


