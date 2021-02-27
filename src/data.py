import pygame

class Game(object):
    def __init__(self, state, tick, tock):
        self.state = state
        self.tick = tick

class GameData(object):
    def __init__(self):
        self.settings = {}
        self.settings["resolution"] = (416, 416)
        self.settings["FPS"] = 30

class GameController(object):
    def __init__(self, game_data):
        self.screen = pygame.display.set_mode(game_data.settings["resolution"])
        self.clock = pygame.time.Clock()
        self._FPS = game_data.settings["FPS"]

    def tick(self):
        self.clock.tick(self._FPS)

