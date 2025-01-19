
from beanie import Document

class IDAllot(Document):
    ai_session_id: int = 100000

    class Settings:
        name = "id_allot"
