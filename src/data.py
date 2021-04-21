from random import choice

import pygame
from spritesheet import *
from Phrases import*

class Game(object):
    def __init__(self, state, tick):
        self.state = state
        self.tick = tick

class GameData(object):
    def __init__(self):
        self.settings = {}
        self.settings["resolution"] = (416, 416)
        self.settings["FPS"] = 30
        self.BG = {}
        self.room = {}
        self.prop = {}
        self.door = {}
        self.character = {}
        self.player = {}
        self.positioner = {}

    # Is it possible to combine all the adds into one add that takes the type as a parameter??
    # def add_detail(self, classification, this_name, this_object):
    #     classification[this_name] = this_object

    def get_all_drawables(self):
        return list(self.character.values()) + list(self.player.values()) + list(self.prop.values())

    def add_character(self, character_name, character_object):
        self.character[character_name] = character_object

    def add_player(self, player_name, player_object):
        self.player[player_name] = player_object

    def add_bg(self, bg_name, bg_object):
        self.BG[bg_name] = bg_object

    def add_room(self, room_name, room_object):
        self.room[room_name] = room_object

    def add_door(self, door_name, door_object):
        self.door[door_name] = door_object

    def add_positioner(self, positioner_name, positioner_object):
        self.positioner[positioner_name] = positioner_object

    def add_prop(self, prop_name, prop_object):
        self.prop[prop_name] = prop_object

class GameController(object):
    def __init__(self, GameData):
        self.GameData = GameData
        self.screen = pygame.display.set_mode(GameData.settings["resolution"])
        self.clock = pygame.time.Clock()
        self._FPS = GameData.settings["FPS"]
        self.input = True
        self.room = "room1"

    def tick(self):
        self.clock.tick(self._FPS)

    def LockInput(self):
        self.input = False

    def UnlockInput(self):
        self.input = True

    def get_current_drawables(self):
        drawables_list = []
        for character in self.GameData.room[self.room].character_list:
            drawables_list.append(self.GameData.character[character])
        for prop in self.GameData.room[self.room].prop_list:
            drawables_list.append(self.GameData.prop[prop])
        drawables_list.append(self.GameData.player["Player"])
        return drawables_list

class EventsManager(object):
    def __init__(self, GameData, GameController):
        self.GameData = GameData
        self.GameController = GameController
        self.step_timer = pygame.USEREVENT + 6

    def start_events(self):

        pygame.time.set_timer(self.step_timer, 60)

class Picaso(object):
    def __init__(self, GameData, GameController):
        self.GameData = GameData
        self.GameController = GameController

    def get_all_drawable(self):
        # drawables_list = {}
        # for character in self.GameData.room[self.GameController.room].character_list:
        #     drawables_list[character] = self.GameData.character[character]
        # drawables_list["Player"] = self.GameData.player["Player"]
        # drawables_list = sorted(drawables_list, key=lambda x: (x.y, x.printing_priority))
        # # print(drawables_list["Walker"].y)
        # # print(drawables_list["Pink_Walker"].y)
        # # print(drawables_list["Player"].y)
        # print(drawables_list)
        # return drawables_list

        drawables_list = []
        for character in self.GameData.room[self.GameController.room].character_list:
            drawables_list.append(self.GameData.character[character])
        for prop in self.GameData.room[self.GameController.room].prop_list:
            drawables_list.append(self.GameData.prop[prop])
        drawables_list.append(self.GameData.player["Player"])
        drawables_list = sorted(drawables_list, key=lambda x: (x.y, x.printing_priority))
        return drawables_list

    def big_draw(self):
        for bg in self.GameData.room[self.GameController.room].BG_list:
            self.GameData.room[self.GameController.room].BG_list[bg].draw(self.GameController.screen)

        drawable_list = self.get_all_drawable()

        for drawable in drawable_list:
            drawable.draw(self.GameController.screen)
