import asyncio
from models.user import User
from models.group import Group
from db_helper import DBHelper, update_base_profile, update_ai_profile

from utils import config_loader
config = config_loader.config

from utils import command, date
from utils.event_loop import EventLoop
from models.event import Event

import ben_dan_bot
import botpy
logging = botpy.get_logger()
import ai
import traceback

def try_update_today_info(obj: User|Group):
    last_talk_ts = date.second()
    profile = obj.profile
    if date.is_same_day(profile.last_talk_ts, last_talk_ts)!=True:
        profile.today_talk_times = 0
        profile.ai.today_talk_times = 0


async def handler(user_id, message: str, reply, group_id: None|str, loop:EventLoop, user_obj: User, group_obj: Group|None):
    if message == '':
        return
    message = message.strip()
    try_update_today_info(user_obj)
    if group_obj:
        try_update_today_info(group_obj)

    try:
        reply_msg = None
        ok, cmd, args = command.is_command(message)
        if ok:
            reply_msg = await cmd(
                user_id = user_id,
                msg = message,
                cmd_arg = args,
                group_id = group_id,
                user_obj = user_obj,
                group_obj = group_obj,
                loop = loop,
            )
        else:
            if group_obj:
                reply_msg = await ai.chat_with_group(message, group_obj)
                await loop.pub(Event.AIPROFILE_UPDATE, obj = group_obj)
            else:
                reply_msg = await ai.chat_with_user(message, user_obj)
        
            await loop.pub(Event.AIPROFILE_UPDATE, obj = user_obj)

        if reply_msg:
            await reply(reply_msg)
        
    except Exception as e:
        logging.error(f"user:{user_id}, message:'{message}',error:{e}")
        logging.error(traceback.format_exc())
    finally:
        update_base_profile(obj = user_obj)
        if group_obj:
            update_base_profile(obj = group_obj)

async def start():
    db_helper = DBHelper(None)
    await db_helper.init_db()
    cache = config("cache")
    t = int(cache["lifetime"]/2)
    asyncio.create_task(db_helper.start_timer_save(t))

    loop = EventLoop()
    loop.sub(Event.AIPROFILE_UPDATE, update_ai_profile)

    async def msg_handler(user_id, message: str, reply, group_id: None|str):
        user = await db_helper.get_user(user_id)
        group = None
        if group_id:
            group = await db_helper.get_group(group_id)

        await handler(user_id, message, reply, group_id, loop, user, group)
    
    client = ben_dan_bot.generate_bot(msg_handler)
    await client.start(appid=config("appid"), secret=config("secret"))

if __name__ == "__main__":
    asyncio.run(start())
