from os import close
from pydantic import BaseModel
from beanie import Document, Indexed

from utils import config_loader
config = config_loader.config

class ChatMessageList(BaseModel):
    role: str
    content: str

class AISession(Document):
    session_id: Indexed(int, unique=True)
    message_list: list[ChatMessageList]
    prompt: str = config('ai_prompt')

    ref_session_id: int = 0 # 引用其他ai会话的message_list
    ref_session_len: int = 0 # 引用的长度

    use_count: int = 0 # session_id当前被其他使用对象使用或者引用的计数。
    
    last_use_ts: int # 最后的使用时间。

