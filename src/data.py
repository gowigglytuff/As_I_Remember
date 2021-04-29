from random import choice

import pygame

from keyboards import KeyboardManager
from spritesheet import *
from Phrases import*
from TileMap import *
from menus import *

class Game(object):
    def __init__(self, state, tick):
        self.state = state
        self.tick = tick

class GameData(object):
    def __init__(self):
        self.settings = {}
        self.settings["resolution"] = (1000, 800)
        self.settings["FPS"] = 30
        self.base_locator_x = 400
        self.base_locator_y = 300
        self.square_size = [32, 32]
        self.BG = {}
        self.room_list = {}
        self.prop_list = {}
        self.decoration_list = {}
        self.door = {}
        self.menu_list = {}
        self.overlay_list = {}
        self.character_list = {}
        self.player = {}
        self.positioner = {}

    def get_all_drawables(self):
        return list(self.character_list.values()) + list(self.player.values()) + list(self.prop_list.values())

    def add_character(self, character_name, character_object):
        self.character_list[character_name] = character_object

    def add_player(self, player_name, player_object):
        self.player[player_name] = player_object

    def add_bg(self, bg_name, bg_object):
        self.BG[bg_name] = bg_object

    def add_room(self, room_name, room_object):
        self.room_list[room_name] = room_object

    def add_door(self, door_name, door_object):
        self.door[door_name] = door_object

    def add_decoration(self, decoration_name, decoration_object):
        self.decoration_list[decoration_name] = decoration_object

    def add_positioner(self, positioner_name, positioner_object):
        self.positioner[positioner_name] = positioner_object

    def add_prop(self, prop_name, prop_object):
        self.prop_list[prop_name] = prop_object

    def add_menu(self, menu_name, menu_object):
        self.menu_list[menu_name] = menu_object

    def add_overlay(self, overlay_name, overlay_object):
        self.overlay_list[overlay_name] = overlay_object

class GameController(object):
    def __init__(self, GameData):
        self.GameData = GameData
        self.screen = pygame.display.set_mode(GameData.settings["resolution"])
        self.clock = pygame.time.Clock()
        self._FPS = GameData.settings["FPS"]
        self.font = "assets/fonts/PressStart2P-Regular.ttf"
        self.input = True
        self.current_room = "room1"
        self.camera = [0, 0]
        self.current_overlay_list = ["top_bar"]
        self.current_menu = None # type: Menu
        self.current_text_box = None # type: Overlay
        self.current_speaker = None
        self.keyboard_manager_list = {}
        self.current_keyboard_manager = None # type: KeyboardManager


    def add_keyboard_manager(self, keyboard_manager_name, keyboard_manager_object):
        self.keyboard_manager_list[keyboard_manager_name] = keyboard_manager_object

    def set_keyboard_manager(self, active_manager):
        self.current_keyboard_manager = self.keyboard_manager_list[active_manager]

    def set_menu(self, active_menu):
        self.current_menu = active_menu

    def set_room(self, active_room):
        self.current_room = active_room

    def set_text_box(self, active_text_box):
        self.current_text_box = active_text_box

    def set_speaker(self, active_speaker):
        self.current_speaker = active_speaker

    def tick(self):
        self.clock.tick(self._FPS)

    def LockInput(self):
        self.input = False

    def UnlockInput(self):
        self.input = True

    def get_current_drawables(self, fillable):
        drawables_list = []
        for character in self.GameData.room_list[fillable].character_list:
            drawables_list.append(self.GameData.character_list[character])
        for prop in self.GameData.room_list[fillable].prop_list:
            drawables_list.append(self.GameData.prop_list[prop])
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

        drawables_list = []
        for character in self.GameData.room_list[self.GameController.current_room].character_list:
            drawables_list.append(self.GameData.character_list[character])

        for prop in self.GameData.room_list[self.GameController.current_room].prop_list:
            drawables_list.append(self.GameData.prop_list[prop])

        for decoration in self.GameData.room_list[self.GameController.current_room].decoration_list:
            drawables_list.append(self.GameData.decoration_list[decoration])

        drawables_list.append(self.GameData.player["Player"])
        drawables_list = sorted(drawables_list, key=lambda x: (x.y, x.printing_priority))
        return drawables_list

    def big_draw(self):
        # Blits the background for the current room
        self.GameData.room_list[self.GameController.current_room].draw_bg(self.GameController.screen)

        # get's all the drawables and prints them in order of y and printing priority
        drawable_list = self.get_all_drawable()
        for drawable in drawable_list:
            drawable.draw(self.GameController.screen)

        # blits the menu that is active
        if self.GameController.current_menu != None:
            self.GameData.menu_list[self.GameController.current_menu].print_menu()

        # blits any overlays that are always active and ons tghat are associated with currently active menus
        for overlay in self.GameController.current_overlay_list:
            self.GameData.overlay_list[overlay].print_overlay()

        # TODO: Find some other better way to do this
        if self.GameController.current_speaker != None:
            self.GameData.overlay_list["text_box"].print_overlay()
            self.GameData.character_list[self.GameController.current_speaker].speak(self.GameData.character_list[self.GameController.current_speaker].current_phrase)



class Camera(object):
    def __init__(self, GameController, GameData, coordinates, anchor):
        self.GameData = GameData
        self.GameController = GameController
        self.anchor = anchor
        self.coordinates = [5 - self.anchor.x, 5 - self.anchor.y]

