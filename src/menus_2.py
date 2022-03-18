import textwrap

import pygame

from keyboards import InGame
from spritesheet import Spritesheet


class SubMenuManager(object):
    def __init__(self, gd_input, gc_input):
        self.gd_input = gd_input
        self.gc_input = gc_input
        self.static_menus = ["stats_menu", "game_action_dialogue_menu"]
        self.active = []
        self.menu_stack = []
        self.visable_menus = []

    def add_menu_to_stack(self, menu_to_add):
        self.menu_stack.insert(0, menu_to_add)

    def activate_menu(self, menu_to_activate):
        self.active.append(menu_to_activate)

    def deactivate_menu(self, menu_to_deactivate):
        self.active.remove(menu_to_deactivate)

class Overlay2(object):
    def __init__(self, GameController, GameData, name, x, y, image):
        self.GameController = GameController
        self.GameData = GameData
        self.screen = self.GameController.screen
        self.x = x
        self.y = y
        self.name = name
        self.image = image.get_image(0, 0)

    def display_overlay(self):
        self.screen.blit(self.image, (self.x, self.y))