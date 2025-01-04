from beanie import Document, Indexed
from .ai import AIRecord
from .profile import Profile


class Group(Document):
    group_id: Indexed(str, unique=True)
    ai: AIRecord = AIRecord()
    level: int = 0
    profile: Profile = Profile()

    class Settings:
        name = "groups"
        indexes = ["group_id"]
        use_state_management = True

