from enum import Enum
from ..worlds import LevelData

class Level:
    
    class States(Enum):
        LEVEL_BEGIN = 0
        LEVEL_COMPLETE = 1
        LEVEL_READY = 2

    def __init__(self) -> None:
        self._init_defaults()
    
    def _init_defaults(self):
        self._world = None
        self.state = self.States.LEVEL_BEGIN
        self.has_flippers = False
        self.has_tankers = False
        self.has_fuseballs = False
        self.has_spikers = False
        self.has_pulsars = False
    
    @property
    def world(self) -> LevelData:
        return self._world

    @world.setter
    def world(self, value: LevelData):
        self._world = value
    
