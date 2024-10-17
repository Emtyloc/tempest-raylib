from src.utils import SingletonMeta

class EventManager(metaclass=SingletonMeta):
    def __init__(self):
        self.listeners: dict[str, list] = {}

    def subscribe(self, event_type: str, listener):
        if event_type not in self.listeners:
            self.listeners[event_type] = []
        self.listeners[event_type].append(listener)
    
    def unsubscribe(self, event_type: str, listener):
        if event_type in self.listeners:
            self.listeners[event_type].remove(listener)
        if not self.listeners[event_type]:
            del self.listeners[event_type]

    def notify(self, event_type: str, data: dict):
        if event_type in self.listeners:
            for listener in self.listeners[event_type]:
                listener(data)
    
    def reset(self):
        self.listeners = {}
    
    def reset_topic(self, event_type: str):
        if event_type in self.listeners:
            del self.listeners[event_type]

    def level_reset(self):
        self.reset_topic(self.Topics.BLASTER_BORDER_UPDATE)
        self.reset_topic(self.Topics.BLASTER_BULLET_UPDATE)
        self.reset_topic(self.Topics.BLASTER_BULLET_COLLIDE)
        self.reset_topic(self.Topics.BLASTER_DEAD)
        self.reset_topic(self.Topics.SUPER_ZAPPER)
        self.reset_topic(self.Topics.SPAWN_ENEMY)
    
    class Topics:
        BLASTER_BORDER_UPDATE = "blaster/border/update"
        BLASTER_BULLET_UPDATE = "blaster/bullet/update"
        BLASTER_BULLET_COLLIDE = "blaster/bullet/collide"
        BLASTER_DEAD = "blaster/dead"
        SCORE_UPDATE = "score/update"
        SUPER_ZAPPER = "blaster/super_zapper"
        SPAWN_ENEMY = "enemy/spawn"
