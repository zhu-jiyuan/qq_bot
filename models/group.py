from beanie import Document, Indexed
from .profile import Profile
from pydantic import BaseModel
from .ai_agent import AIAgent

class GroupAI(BaseModel):
    agent: AIAgent


class Group(Document):
    group_id: Indexed(str, unique=True)
    level: int = 0
    profile: Profile = Profile()
    AI: GroupAI

    class Settings:
        name = "groups"
        indexes = ["group_id"]
        use_state_management = True

