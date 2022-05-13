from abc import abstractmethod
from enum import Enum

import pygame

# from menus import *


class Direction(Enum):
    LEFT = 1
    RIGHT = 2
    UP = 3
    DOWN = 4


class Facing(Enum):
    LEFT = 1
    RIGHT = 2
    FRONT = 4
    BACK = 3

class KeyboardManager():
    @property
    @abstractmethod
    def ID(self):
        pass

    def parse_events(self, events):
        """Parse events from the main game loop.

        Args:
            events (pygame.event.Event): List of events to parse, must be type
                pygame.KEYDOWN or pygame.KEYUP.

        Raises:
            TypeError: Event of non-keyboard type sent to KeyboardManger.
        """        
        for e in events:
            if e.type == pygame.KEYDOWN:
                self.parse_key_pressed(e.key)
            elif e.type == pygame.KEYUP:
                self.parse_key_released(e.key)
            else:
                raise TypeError("Non-keyboard event sent to KeyboardManager")
    
    def parse_key_pressed(self, key):
        if key == pygame.K_RIGHT:
            self.direction_key_pressed(Direction.RIGHT)

        if key == pygame.K_LEFT:
            self.direction_key_pressed(Direction.LEFT)

        if key == pygame.K_DOWN:
            self.direction_key_pressed(Direction.DOWN)

        if key == pygame.K_UP:
            self.direction_key_pressed(Direction.UP)

        if key == pygame.K_RETURN:
            self.key_return()

        if key == pygame.K_SPACE:
            self.key_space()

        if key == pygame.K_LCTRL:
            self.key_control()

        if key == pygame.K_LSHIFT:
            self.key_shift()

        if key == pygame.K_CAPSLOCK:
            self.key_caps()

    def parse_key_released(self, key):
        if key == pygame.K_RIGHT:
            self.direction_key_released(Direction.RIGHT)

        if key == pygame.K_LEFT:
            self.direction_key_released(Direction.LEFT)

        if key == pygame.K_DOWN:
            self.direction_key_released(Direction.DOWN)

        if key == pygame.K_UP:
            self.direction_key_released(Direction.UP)

        if key == pygame.K_RETURN:
            #self.key_return()
            pass

        if key == pygame.K_SPACE:
            #self.key_space()
            pass

        if key == pygame.K_LCTRL:
            #self.key_control()
            pass

        if key == pygame.K_LSHIFT:
            #self.key_shift()
            pass

        if key == pygame.K_CAPSLOCK:
            #self.key_caps()
            pass

    def key_pushed(self):
        pass

    def direction_key_released(self, key):
        pass

    def direction_key_pressed(self, direction):
        pass

    @abstractmethod
    def key_return(self):
        pass


    def key_caps(self):
        pass

    @abstractmethod
    def key_space(self):
        pass

    @abstractmethod
    def key_control(self):
        pass

    @abstractmethod
    def key_shift(self):
        pass


# Keyboard Manager for when the player is walking around in the game
class InGame(KeyboardManager):
    ID = "IG_Keyer"

    def __init__(self, GameController, GameData):
        self.GameController = GameController
        self.GameData = GameData
        self.current_direction_key = None
        self.associated_menu = None

    def direction_key_released(self, direction):
        if self.current_direction_key == direction:
            self.current_direction_key = None


    def direction_key_pressed(self, direction):
        self.current_direction_key = direction


    def key_return(self):
        # interacts with the feature that is in the tile that the player is facing

        self.GameData.player["Player"].interact_with()

    def key_space(self):
        self.GameData.player["Player"].perform_diagnostic()
        self.GameData.character_list["Maggie"].write_to_gamestate()

    def key_control(self):

        if self.GameData.player["Player"].state == "idle":
            self.current_direction_key = None
            self.GameData.menu_list["start_menu"].set_menu()

    def key_shift(self):
        # self.GameData.player["Player"].teleport_to_sandpiper()
        self.GameData.key_item_list[self.GameController.inventory.selected_tool].use_item()


    def key_caps(self):
        self.GameData.menu_list["hitchiking_menu"].set_menu()

class InMenu(KeyboardManager):
    ID = "IM_Keyer"

    def __init__(self, GameController, GameData):
        self.GameController = GameController
        self.GameData = GameData


    def direction_key_released(self, direction):
        self.direction = direction
        if self.direction == Direction.DOWN:
            self.GameData.menu_list[self.GameController.menu_manager.menu_stack[0]].cursor_down()
        if self.direction == Direction.UP:
            self.GameData.menu_list[self.GameController.menu_manager.menu_stack[0]].cursor_up()
        if self.direction == Direction.LEFT:
            self.GameData.menu_list[self.GameController.menu_manager.menu_stack[0]].cursor_left()
        if self.direction == Direction.RIGHT:
            self.GameData.menu_list[self.GameController.menu_manager.menu_stack[0]].cursor_right()

    def direction_key_pressed(self, direction):
        pass

    def key_return(self):
        self.GameData.menu_list[self.GameController.menu_manager.menu_stack[0]].choose_option()

    def key_space(self):
        pass

    def key_control(self):
        self.GameData.menu_list[self.GameController.menu_manager.menu_stack[0]].exit_all_menus()

    def key_shift(self):
        self.GameData.menu_list[self.GameController.menu_manager.menu_stack[0]].shift_pressed()