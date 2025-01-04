from pydantic import BaseModel

class AIProfile(BaseModel):
    total_talk_times: int = 0
    today_talk_times: int = 0

class Profile(BaseModel):
    total_talk_times: int = 0
    today_talk_times: int = 0
    last_talk_ts: int = 0

    ai: AIProfile = AIProfile()

