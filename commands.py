

def ls(**kwargs):
    return '''
        # base
        /ls - 列出基本命令
        /user_info - 查看用户信息
        /about - 机器人关于

        # AI
        /new_chat - 创建新的聊天
        
        # epic
        /epic_get_free_game 获取epic免费游戏信息。
    '''

def user_info(**kwargs):
    user_id = kwargs["user_id"]
    return f"your user_id is {user_id}."


def about(**kwargs):
    return '''
        bendan bot.
    '''

def new_chat(**kwargs):
    return '''
        new_chat is None.
    '''

def epic_get_free_game(**kwargs):
    return '''
        epic_get_free_game is None.
    '''
