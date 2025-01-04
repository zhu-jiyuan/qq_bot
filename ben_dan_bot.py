
import botpy
from botpy.message import GroupMessage, C2CMessage
# from pprint import pprint

logging = botpy.get_logger()


def make_reply(message: GroupMessage|C2CMessage):
    async def reply(content: str):
        await message.reply(
            msg_type=0, 
            content= content
        )
    return reply

class BenDanClient(botpy.Client):
    # qq group message
    async def on_group_at_message_create(self, message: GroupMessage):
        reply = make_reply(message)
        await self.handler(message.author.member_openid, message.content, reply, message.group_openid)

    # qq private message
    async def on_c2c_message_create(self, message: C2CMessage):
        reply = make_reply(message)
        await self.handler(message.author.user_openid, message.content, reply, None)

    def register_handler(self, handler):
        self.handler = handler
        logging.info("register handler success")

def generate_bot(handler):
    intents = botpy.Intents(public_messages=True, direct_message=True, guilds=True) 
    client = BenDanClient(intents=intents) 
    client.register_handler(handler)
    return client
