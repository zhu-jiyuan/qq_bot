from models import group

def test_is_command():
    from utils import command
    is_command = command.is_command

    def assert_command(msg, expected):
        ok, cmd, args = is_command(msg)
        assert ok == expected
        if ok:
            print(msg, ok, cmd, args)
            # print("cmd==>", cmd())

    assert_command('', False)
    assert_command(' ', False)
    assert_command('/ls', True)
    assert_command(' /ls', False)
    assert_command('/ls ', True)
    assert_command('   /ls  ', False)
    assert_command('/lss', False)
    assert_command('/ls sss', True)

# test_is_command()

import time
def test_lru_cache():
    from utils import lru_cache
    cache = lru_cache.LruCache(3)
    cache.set('a', 1)
    assert cache.get('a') == 1
    time.sleep(2)
    cache.set('b', 2)
    time.sleep(2)

    ret = cache.clean()
    assert ret == [1]

    assert cache.get('a') == None
    assert cache.get('b') == 2

    cache.delete('b')
    assert cache.get('b') == None
# test_lru_cache()

def test_db_helper():
    from db_helper import DBHelper
    import asyncio

    db = DBHelper(5)

    async def test():
        await db.init_db()

        asyncio.create_task(db.start_timer_save(5))
        
        user = await db.get_user('test')
        print("user==>", user)
        group = await db.get_group('test_group')
        print("group==>", group)

        await asyncio.sleep(3)
        user.profile.total_talk_times = 100
        user.ai.cur_message_list.append({'role': 'user', 'content': 'test'})


        await asyncio.sleep(10)

        await db.close()

    asyncio.run(test())


        
# test_db_helper()


def test_event_loop():
    from utils.event_loop import EventLoop
    import asyncio
    from models.event import Event

    loop = EventLoop()

    async def ppp(**kwargs):
        print('ppp', kwargs["name"])

    async def test():
        handle = loop.sub(Event.AIPROFILE_UPDATE, ppp)
        loop.sub(Event.AIPROFILE_UPDATE, ppp)
        await loop.pub(Event.AIPROFILE_UPDATE, 
                       name = "test"
                       )
        loop.unsub(Event.AIPROFILE_UPDATE, handle)
        await loop.pub(Event.AIPROFILE_UPDATE, 
                       name = "test2"
                       )
        await asyncio.sleep(3)

    asyncio.run(test())

test_event_loop()


