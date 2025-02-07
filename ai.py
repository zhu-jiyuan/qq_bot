# Please install OpenAI SDK first: `pip3 install openai`
from openai import AsyncOpenAI
from models.user import User
from models.group import Group
from utils import config_loader

config = config_loader.config

client = AsyncOpenAI(api_key=config("deepseek"), base_url="https://api.deepseek.com")

lock_tbl = {}
def check_lock(id: str):
    if id in lock_tbl:
        return True
    return False
def unlock(id: str):
    if id in lock_tbl:
        del lock_tbl[id]
def lock(id: str):
    lock_tbl[id] = True

async def chat(message_list: list):
    ok = False
    try:
        response = await client.chat.completions.create(
            model=config("deepseek_model"),
            messages=message_list,
            stream=False,
            timeout = config("timeout")
        )
        ok = True
    except Exception as e:
        pass
    
    if ok:
        return ok, response.choices[0].message

    return ok, None


async def chat_with_user(message: str, user_obj: User):
    if check_lock(user_obj.user_id):
        return "当前还有会话未处理"
    message_list = user_obj.ai.cur_message_list
    request_msg_list = message_list.copy()
    request_msg_list.append({"role": "user", "content": message})

    lock(user_obj.user_id)
    ok, reply = await chat(request_msg_list)
    ret = "server error"
    if ok:
        message_list.append({"role": "user", "content": message})
        message_list.append({"role": "assistant", "content": reply.content})
        ret = reply.content
    unlock(user_obj.user_id)
    return ret

async def chat_with_group(message: str, group_obj: Group):
    if check_lock(group_obj.group_id):
        return "当前还有会话未处理"

    message_list = group_obj.ai.cur_message_list
    request_msg_list = message_list.copy()
    request_msg_list.append({"role": "user", "content": message})

    lock(group_obj.group_id)
    ok, reply = await chat(request_msg_list)
    ret = "server error"
    if ok:
        message_list.append({"role": "user", "content": message})
        message_list.append({"role": "assistant", "content": reply.content})
        ret = reply.content

    unlock(group_obj.group_id)
    return ret

async def chat_with_quick(message: str):
    message_list = [{"role": "user", "content": message}]
    ok, reply = await chat(message_list)
    ret = "server error"
    if ok:
        ret = reply.content
    return ret
