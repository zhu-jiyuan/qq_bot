from pydantic import BaseModel

from utils import config_loader
config = config_loader.config

class ChatMessageList(BaseModel):
    role: str
    content: str

class AIRecord(BaseModel):
    prompt: str = config('ai_prompt')
    cur_message_list: list[ChatMessageList] = []

