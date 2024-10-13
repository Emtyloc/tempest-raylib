from src.shared import EventManager, SCREEN_CENTER, TempestColors
from pyray import *

class ScoreManager:
    def __init__(self, event_manager: EventManager):
        self.total_score = 0
        self.event_manager = event_manager
        self.event_manager.subscribe(EventManager.Topics.SCORE_UPDATE, self.score_update)

    def score_update(self, data: dict):
        self.total_score += data["score"]
    
    def update_frame(self):
        pass

    def draw_frame(self):
        text = str(self.total_score)
        text_size = 40
        draw_text(text, int(SCREEN_CENTER.x - measure_text(text, text_size) / 2), int(0 + text_size), text_size, TempestColors.GREEN_NEON.rgba())

