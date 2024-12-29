# Please install OpenAI SDK first: `pip3 install openai`
from openai import AsyncOpenAI
import utils

config = utils.config

client = AsyncOpenAI(api_key=config("deepseek"), base_url="https://api.deepseek.com")

async def chat(user_msg):
    response = await client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "你叫bendan, 你是一个漂亮的二次元动漫女主，同时你又是一个知识渊博的助手，每次你都会用中文回答。"},
            {"role": "user", "content": user_msg}
        ],
        stream=False
    )
    return response.choices[0].message.content
