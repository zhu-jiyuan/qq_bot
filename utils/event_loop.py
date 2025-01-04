from typing import Callable, final
from logging import error
from models.event import Event

class Suber:
    handle:int
    func:Callable
    cancel:bool = False
    
    def __init__(self, handle:int, func:Callable) -> None:
        self.handle = handle
        self.func = func


class Topic:
    queue:list[Suber] = []
    allot_id: int = 0



class EventLoop:
    '''
    事件循环
    注册异步回调函数，发布事件时，调用所有注册的回调函数
    
    TODO: 延迟发布事件
    '''

    def __init__(self) -> None:
        self.topic_dict:dict[Event, Topic] = {}

    async def pub(self, event_id:Event, **kwargs):
        if event_id not in self.topic_dict:
            return
        topic = self.topic_dict[event_id]
        if len(topic.queue)==0:
            return

        for suber in topic.queue:
            if not suber.cancel:
                try:
                    await suber.func(**kwargs)
                except Exception as e:
                    error(f"Unexpected error for event {event_id}: {e}")

        for i in range(len(topic.queue), 1, -1):
            if topic.queue[i].cancel:
                topic.queue.pop(i)

    def sub(self, event_id:Event, func:Callable)->int:
        if event_id not in self.topic_dict:
            self.topic_dict[event_id] = Topic()

        topic = self.topic_dict[event_id]
        allot_id = topic.allot_id
        topic.queue.append(Suber(allot_id, func))
        topic.allot_id += 1
        return allot_id

    def unsub(self, event_id:Event, handle:int):
        if event_id not in self.topic_dict:
            return
        topic = self.topic_dict[event_id]
        queue = topic.queue
        for i in range(len(queue)):
            if queue[i].handle == handle:
                queue[i].cancel = True
                break
