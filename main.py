import asyncio
import os.path
from sys import exception

import utils
import ben_dan_bot
import botpy
logging = botpy.get_logger()
config = utils.config
import ai



async def handler(user_id, message: str, reply):
    if message == '':
        return
    message = message.strip()

    try:
        reply_msg = None
        ok, cmd, args = utils.is_command(message)
        if ok:
            reply_msg = cmd(
                user_id = user_id,
                msg = message,
                cmd_arg = args
            )
        else:
            reply_msg = await ai.chat(message)
        
        if reply_msg:
            await reply(reply_msg)
        
    except Exception as e:
        logging.error(f"Unexpected error for user {user_id} with message '{message}': {e}")
    finally:
        pass

def start():
    client = ben_dan_bot.generate_bot(handler)
    client.run(appid=config("appid"), secret=config("secret"))

if __name__ == "__main__":
    start()
