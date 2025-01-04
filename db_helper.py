import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from utils import config_loader
from models.user import User
from models.group import Group

from utils import lru_cache, date
config = config_loader.config
import botpy
logging = botpy.get_logger()


def _get_db_uri(mongo_config)->str:
    username = mongo_config["username"]
    password = mongo_config["password"]
    host = mongo_config["host"]
    port = mongo_config["port"]
    if username=="":
        return f"mongodb://{host}:{port}/"
    else:
        return f"mongodb://{username}:{password}@{host}:{port}/"

class DBHelper:
    
    def __init__(self, cache_second:int|None) -> None:
        mongo_config = config('mongodb')
        if cache_second is None:
            cache_config = config('cache')
            cache_second = cache_config["lifetime"]

        uri = _get_db_uri(mongo_config)

        self.db_client = AsyncIOMotorClient(uri)
        self.cache = lru_cache.LruCache(cache_second)
        self._running = False

    async def init_db(self):
        mongo_config = config('mongodb')
        await init_beanie(database=self.db_client[mongo_config["database"]], document_models=[User, Group])
        
    async def start_timer_save(self, second: int):
        self._running = True
        while self._running:
            await asyncio.sleep(second)
            doc_list = self.cache.clean()
            for doc in doc_list:
                await doc.save_changes()
                logging.info(f"save {doc.id} success")
        
    async def close(self):
        self._running = False
        self.db_client.close()

    async def get_user(self, user_id: str) -> User:
        user = self.cache.get(user_id)
        if user:
            return user

        user = await User.find_one({"user_id": user_id})
        if user==None:
            user = User(user_id=user_id)
            await user.save()
        
        self.cache.set(user_id, user)
        return user
        

    async def get_group(self, group_id: str) -> Group:
        group = self.cache.get(group_id)
        if group:
            return group

        group = await Group.find_one({"group_id": group_id})
        if group==None:
            group = Group(group_id=group_id)
            await group.save()
        
        self.cache.set(group_id, group)
        return group


def update_base_profile(**kwargs):
    obj:User|Group = kwargs['obj']

    last_talk_ts = date.second()
    profile = obj.profile
    profile.last_talk_ts = last_talk_ts
    profile.total_talk_times += 1
    profile.today_talk_times += 1

async def update_ai_profile(**kwargs):
    obj:User|Group = kwargs['obj']
    profile = obj.profile
    profile.ai.total_talk_times += 1
    profile.ai.today_talk_times += 1
