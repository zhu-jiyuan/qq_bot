from beanie import Document, Indexed
from pydantic import BaseModel
# from typing import Optional
# from pprint import pprint
from .ai import AIRecord
from .profile import Profile


class User(Document):
    user_id: Indexed(str, unique=True)
    ai: AIRecord = AIRecord()
    level: int = 0
    profile: Profile = Profile()

    class Settings:
        name = "users"
        indexes = ["user_id"]
        use_state_management = True
