
from models.user import User
from models.group import Group
from models.event import Event
import ai

async def ls(**kwargs):
    return '''
# base
/ls - 列出基本命令
/about - 机器人关于
/help - 帮助

# profile
/profile - 查看个人资料
/profile_group - 查看群组资料

# AI
/ai_new_chat - 开始新的对话
/ai_new_group_chat - 开始新的群组对话
/ai_set_prompt - 设置个人的默认对话提示词
/ai_set_group_prompt - 设置群组默认对话提示词
/ai_with_user - 私聊对话
/ai_quick_chat - 使用默认提示词快速对话, 不保存对话记录

# epic
/epic_get_free_game 获取epic免费游戏信息。
'''

async def help(**kwargs):
    return '''qq群默认群聊模式，可以使用/ai_with_user命令私聊对话，这会使用私聊对话的默认提示词。
'''

async def about(**kwargs):
    return '''
        bendan bot.
    '''

async def profile(**kwargs):
    user_obj:User = kwargs['user_obj']
    return f'''
user_id: {user_obj.user_id}
当前的ai对话提示词: {user_obj.ai.prompt}
今日使用ai次数: {user_obj.profile.ai.today_talk_times}
总ai使用次数: {user_obj.profile.ai.total_talk_times}
今日总使用次数: {user_obj.profile.today_talk_times}
总使用次数: {user_obj.profile.total_talk_times}
level: {user_obj.level}
'''

async def profile_group(**kwargs):
    group_obj:Group = kwargs['group_obj']
    if not group_obj:
        return '不在群组'
    return f'''
group_id: {group_obj.group_id}
当前的ai对话提示词: {group_obj.ai.prompt}
今日使用ai次数: {group_obj.profile.ai.today_talk_times}
总ai使用次数: {group_obj.profile.ai.total_talk_times}
今日总使用次数: {group_obj.profile.today_talk_times}
总使用次数: {group_obj.profile.total_talk_times}
level: {group_obj.level}
'''

async def ai_new_chat(**kwargs):
    user_obj:User = kwargs['user_obj']
    user_obj.ai.cur_message_list = []
    default_prompt = user_obj.ai.prompt
    user_obj.ai.cur_message_list.append({"role": "system", "content": default_prompt})
    
    cmd_arg = kwargs['cmd_arg']
    if cmd_arg and len(cmd_arg)>0:
        reply_msg = await ai.chat_with_user(cmd_arg, user_obj)
        loop = kwargs['loop']
        await loop.pub(Event.AIPROFILE_UPDATE, obj=user_obj)
        return reply_msg

    return f"已经开始新的对话，当前的对话提示词是: {default_prompt}"

async def ai_new_group_chat(**kwargs):
    group_obj:Group = kwargs['group_obj']
    if not group_obj:
        return '不在群组'
    group_obj.ai.cur_message_list = []
    default_prompt = group_obj.ai.prompt
    group_obj.ai.cur_message_list.append({"role": "system", "content": default_prompt})

    cmd_arg = kwargs['cmd_arg']
    if cmd_arg and len(cmd_arg)>0:
        reply_msg = await ai.chat_with_group(cmd_arg, group_obj)
        loop = kwargs['loop']
        await loop.pub(Event.AIPROFILE_UPDATE, obj=group_obj)
        await loop.pub(Event.AIPROFILE_UPDATE, obj=kwargs['user_obj'])
        return reply_msg

    return f"已经开始新的对话，当前的对话提示词是: {default_prompt}"

async def ai_set_prompt(**kwargs):
    user_obj:User = kwargs['user_obj']
    prompt:str = kwargs['cmd_arg']
    user_obj.ai.prompt = prompt
    return f"已经设置新的对话提示词: {prompt}.\n将在新对话生效."

async def ai_set_group_prompt(**kwargs):
    group_obj:Group = kwargs['group_obj']
    if not group_obj:
        return '不在群组'
    prompt:str = kwargs['cmd_arg']
    group_obj.ai.prompt = prompt
    return f"已经设置新的对话提示词: {prompt}.\n将在新对话生效."

async def ai_with_user(**kwargs):
    user_obj:User = kwargs['user_obj']

    message:str = kwargs['cmd_arg']
    loop = kwargs['loop']
    reply_msg = await ai.chat_with_user(message, user_obj)
    loop.pub(Event.AIPROFILE_UPDATE, obj=user_obj)
    return reply_msg

async def ai_quick_chat(**kwargs):
    message:str = kwargs['cmd_arg']
    reply_msg = await ai.chat_with_quick(message)
    loop = kwargs['loop']
    group_obj:Group = kwargs['group_obj']
    if group_obj:
        await loop.pub(Event.AIPROFILE_UPDATE, obj=group_obj)
    user_obj:User = kwargs['user_obj']
    await loop.pub(Event.AIPROFILE_UPDATE, obj=user_obj)

    return reply_msg

async def epic_get_free_game(**kwargs):
    return '''
        epic_get_free_game is None.
    '''
