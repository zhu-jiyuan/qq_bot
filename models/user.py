from beanie import Document, Indexed
from pydantic import BaseModel
# from typing import Optional
# from pprint import pprint
from .profile import Profile
from .ai_agent import AIAgent


class User(Document):
    user_id: Indexed(str, unique=True)
    level: int = 0
    profile: Profile = Profile()


    class Settings:
        name = "users"
        indexes = ["user_id"]
        use_state_management = True
