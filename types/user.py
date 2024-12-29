import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import Document, init_beanie
from pydantic import Field
import utils

config=utils.config

# 定义文档模型
class User(Document):
    name: str
    age: int
    email: str = Field(unique=True)

    class Settings:
        name = "users"
        


def _get_db_uri(mongo_config)->str:
    username = mongo_config["username"]
    password = mongo_config["password"]
    host = mongo_config["host"]
    port = mongo_config["port"]
    if username=="":
        return f"mongodb://{host}:{port}/"
    else:
        return f"mongodb://{username}:{password}@{host}:{port}/"
    

# 初始化数据库
async def init_db():
    mongo_config = config('mongodb')
    uri = _get_db_uri(mongo_config)
    client = AsyncIOMotorClient(uri)
    database = client[mongo_config["database"]]
    await init_beanie(database=database, document_models=[User])

# 插入文档
async def create_user():
    user = User(name="Alice", age=25, email="alice@example.com")
    await user.insert()
    print("User created:", user)

# 查询文档
async def find_user():
    user = await User.find_one(User.name == "Alice")
    print("Found user:", user)

# 更新文档
async def update_user():
    user = await User.find_one(User.name == "Alice")
    if user:
        user.age = 26
        await user.save()
        print("Updated user:", user)

# 删除文档
async def delete_user():
    user = await User.find_one(User.name == "Alice")
    if user:
        await user.delete()
        print("User deleted:", user)

# 主函数
async def main():
    await init_db()
    await create_user()
    await find_user()
    await update_user()
    await delete_user()

# 运行程序
asyncio.run(main())
