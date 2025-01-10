# Please install OpenAI SDK first: `pip3 install openai`
from openai import AsyncOpenAI
from models.user import User
from models.group import Group
from utils import config_loader

config = config_loader.config

client = AsyncOpenAI(api_key=config("deepseek"), base_url="https://api.deepseek.com")

async def chat(message_list: list):
    response = await client.chat.completions.create(
        model="deepseek-chat",
        messages=message_list,
        stream=False
    )
    return response.choices[0].message


async def chat_with_user(message: str, user_obj: User):
    message_list = user_obj.ai.cur_message_list
    message_list.append({"role": "user", "content": message})

    reply = await chat(message_list)
    message_list.append({"role": reply.role, "content": reply.content})

    return reply.content

async def chat_with_group(message: str, group_obj: Group):
    message_list = group_obj.ai.cur_message_list
    message_list.append({"role": "user", "content": message})

    reply = await chat(message_list)
    message_list.append({"role": reply.role, "content": reply.content})
    return reply.content

async def chat_with_quick(message: str):
    message_list = [{"role": "user", "content": message}]
    reply = await chat(message_list)
    return reply.content
