from os import close
from pydantic import BaseModel
from beanie import Document, Indexed

class AIAgentSessionList(BaseModel):
    session_id: int
    summary: str
    create_ts: int

class AIAgent(BaseModel):
    cur_session_id: int
    session_list: list[AIAgentSessionList] = []

