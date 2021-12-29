from abc import ABC, abstractmethod
from enum import Enum

import pygame

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


#TODO add other keyboards
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


    def key_right(self):
        pass


    def key_left(self):
        pass


    def key_down(self):
        pass


    def key_up(self):
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
        print("Player Location: " + str(self.GameData.player["Player"].x), str(self.GameData.player["Player"].y))

        self.GameData.player["Player"].interact_with()

    def key_space(self):
        pass

    def key_control(self):
        self.GameData.menu_list["start_menu"].set_menu()


    def key_shift(self):
        self.GameData.menu_list["yes_no_menu"].set_menu()


    def key_caps(self):
        print(self.GameData.player["Player"].x, self.GameData.player["Player"].y)


# Keyboard Manager for when the player is in the start menu
class InStartMenu(KeyboardManager):
    ID = "ISM_Keyer"

    def __init__(self, GameController, GameData):
        self.GameController = GameController
        self.GameData = GameData

    def key_right(self):
        pass

    def key_left(self):
        pass

    def direction_key_released(self, direction):
        self.direction = direction
        if self.direction == Direction.DOWN:
            self.GameData.menu_list["start_menu"].cursor_down()
        if self.direction == Direction.UP:
            self.GameData.menu_list["start_menu"].cursor_up()

    def direction_key_pressed(self, direction):
        pass


    def key_return(self):
        menu_selection = self.GameData.menu_list["start_menu"].get_current_menu_item()
        if menu_selection == "Bag":
            print("You looked in your bag!")
            self.GameData.menu_list["inventory_menu"].set_menu()

        elif menu_selection == "Key Items":
            print("You looked in your bag!")
            self.GameData.menu_list["key_inventory_menu"].set_menu()

        elif menu_selection == "Profile":
            self.GameController.add_current_overlay("ID_card")
            self.GameController.MenuManager.start_menu = False
            self.GameController.set_keyboard_manager(InProfile.ID)
            self.GameData.menu_list["start_menu"].reset_cursor()

        elif menu_selection == "Chore List":
            self.GameController.add_current_overlay("To_do_list")
            self.GameController.MenuManager.start_menu = False
            self.GameController.set_keyboard_manager(InToDoList.ID)
            self.GameData.menu_list["start_menu"].reset_cursor()


        else:
            print("You exited the menu")
            self.GameController.set_keyboard_manager(InGame.ID)
            # self.GameController.set_menu(None)
            self.GameController.MenuManager.start_menu = False
            self.GameData.menu_list["start_menu"].reset_cursor()


    def key_space(self):
        pass

    def key_control(self):
        self.GameController.set_keyboard_manager(InGame.ID)
        # self.GameController.set_menu(None)
        self.GameController.MenuManager.start_menu = False

    def key_shift(self):
        pass

    def key_caps(self):
        pass


# Inventory Keyboard Managers
# Keyboard Manager for when the player is looking through their inventory
class InInventory(KeyboardManager):
    ID = "IIM_Keyer"

    def __init__(self, GameController, GameData):
        self.GameController = GameController
        self.GameData = GameData

    def key_right(self):
        pass

    def key_left(self):
        pass

    def direction_key_released(self, direction):
        self.direction = direction
        if self.direction == Direction.DOWN:
            self.GameData.menu_list["inventory_menu"].cursor_down()
        if self.direction == Direction.UP:
            self.GameData.menu_list["inventory_menu"].cursor_up()
        if self.direction == Direction.LEFT:
            self.GameController.inventory.bag_slot_left()

        if self.direction == Direction.RIGHT:
            self.GameController.inventory.bag_slot_right()

    def direction_key_pressed(self, direction):
        pass

    def key_up(self):
        pass

    def key_down(self):
        pass

    def key_return(self):
        self.GameData.menu_list[self.GameController.current_menu].choose_option()

    def key_space(self):
        pass

    def key_control(self):
        pass

    def key_shift(self):
        pass


# Keyboard Manager for when the player has selected an item in inventory and is deciding what to do with it
class InUseInventory(KeyboardManager):
    ID = "IUM_Keyer"

    def __init__(self, GameController, GameData):
        self.GameController = GameController
        self.GameData = GameData

    def key_right(self):
        pass

    def key_left(self):
        pass

    def direction_key_released(self, direction):
        self.direction = direction
        if self.direction == Direction.DOWN:
            self.GameData.menu_list["use_menu"].cursor_down()
        if self.direction == Direction.UP:
            self.GameData.menu_list["use_menu"].cursor_up()

    def direction_key_pressed(self, direction):
        pass

    def key_up(self):
        pass

    def key_down(self):
        pass

    def key_return(self):
        self.GameData.menu_list[self.GameController.current_menu].choose_option()

    def key_space(self):
        pass

    def key_control(self):
        self.GameController.set_keyboard_manager(InGame.ID)
        # self.GameController.set_menu(None)
        self.GameController.MenuManager.start_menu = False

    def key_shift(self):
        pass

    def key_caps(self):
        pass


# Keyboard Manager for when the player is looking through their key inventory
class InKeyInventory(KeyboardManager):
    ID = "IKM_Keyer"

    def __init__(self, GameController, GameData):
        self.GameController = GameController
        self.GameData = GameData

    def direction_key_released(self, direction):
        self.direction = direction
        if self.direction == Direction.DOWN:
            self.GameData.menu_list["key_inventory_menu"].cursor_down()

        if self.direction == Direction.UP:
            self.GameData.menu_list["key_inventory_menu"].cursor_up()

        if self.direction == Direction.LEFT:
            self.GameController.inventory.bag_slot_left()

        if self.direction == Direction.RIGHT:
            self.GameController.inventory.bag_slot_right()

    def key_right(self):
        pass

    def key_left(self):
        pass

    def key_up(self):
        pass

    def key_down(self):
        pass

    def key_return(self):
        self.GameData.menu_list[self.GameController.current_menu].choose_option()


    def key_space(self):
        pass

    def key_control(self):
        pass

    def key_shift(self):
        pass

    def key_caps(self):
        pass

# Conversation Keyboard Managers
# Keyboard Manager for when the player is talking to a NPC and choosing how to interact with them
class InConversationOptions(KeyboardManager):
    ID = "ITKM_Keyer"

    def __init__(self, GameController, GameData):
        self.GameController = GameController
        self.GameData = GameData

    def key_right(self):
        pass

    def key_left(self):
        pass

    def direction_key_released(self, direction):
        self.direction = direction
        if self.direction == Direction.DOWN:
            self.GameData.menu_list["character_interact_menu"].cursor_down()
        if self.direction == Direction.UP:
            self.GameData.menu_list["character_interact_menu"].cursor_up()

    def direction_key_pressed(self, direction):
        pass

    def key_up(self):
        print("hi")
        self.GameData.menu_list["character_interact_menu"].cursor_up()

    def key_down(self):
        self.GameData.menu_list["character_interact_menu"].cursor_down()

    def key_return(self):
        #TODO: Fix this to use characters name instead of facing tile
        menu_selection = self.GameData.menu_list["character_interact_menu"].get_current_menu_item()
        if menu_selection == self.GameData.menu_list["character_interact_menu"].menu_item_list[0]:


            self.GameController.set_speaker(self.GameData.player["Player"].check_adj_tile(self.GameData.player["Player"].get_direct(self.GameData.player["Player"].facing)).object_filling)
            self.GameData.character_list[self.GameData.player["Player"].check_adj_tile(self.GameData.player["Player"].get_direct(self.GameData.player["Player"].facing)).object_filling].set_state("talking")
            self.GameData.character_list[self.GameData.player["Player"].check_adj_tile(self.GameData.player["Player"].get_direct(self.GameData.player["Player"].facing)).object_filling].set_current_phrase()
            self.GameData.character_list[self.GameData.player["Player"].check_adj_tile(self.GameData.player["Player"].get_direct(self.GameData.player["Player"].facing)).object_filling].set_speaking_queue()
            self.GameController.set_keyboard_manager(InConversation.ID)


            self.GameData.menu_list["character_interact_menu"].set_talking_to(None)
            self.GameController.MenuManager.character_interact_menu = False
        elif menu_selection == "Give Gift":
            print("here, take this poop")
            self.GameController.set_keyboard_manager(InGame.ID)
            self.GameController.MenuManager.character_interact_menu = False
            self.GameData.character_list[self.GameData.player["Player"].check_adj_tile(self.GameData.player["Player"].direction).object_filling].set_state("idle")
        elif menu_selection == "Exit":
            self.GameController.set_keyboard_manager(InGame.ID)
            self.GameController.MenuManager.character_interact_menu = False
            self.GameData.character_list[self.GameData.player["Player"].check_adj_tile(self.GameData.player["Player"].direction).object_filling].set_state(
                "idle")
        self.GameData.menu_list["character_interact_menu"].reset_cursor()

    def key_space(self):
        pass

    def key_control(self):
        pass

    def key_shift(self):
        pass


# Keyboard Manager for when the player has chosen to talk to an NPC and is flipping through the conversation
class InConversation(KeyboardManager):
    ID = "IT_Keyer"

    def __init__(self, GameController, GameData):
        self.GameController = GameController
        self.GameData = GameData

    def key_right(self):
        pass

    def key_left(self):
        pass

    def direction_key_released(self, direction):
        self.direction = direction
        if self.direction == Direction.DOWN:
            pass
        if self.direction == Direction.UP:
            pass
        if self.direction == Direction.LEFT:
            pass
        if self.direction == Direction.RIGHT:
            pass

    def key_up(self):
        pass

    def key_down(self):
        pass

    def key_return(self):
        if self.GameData.character_list[self.GameData.player["Player"].check_adj_tile(self.GameData.player["Player"].get_direct(self.GameData.player["Player"].facing)).object_filling].current_phrase != None:
            self.GameData.character_list[self.GameData.player["Player"].check_adj_tile(self.GameData.player["Player"].get_direct(self.GameData.player["Player"].facing)).object_filling].set_speaking_queue()
        else:
            self.GameData.character_list[
                self.GameData.player["Player"].check_adj_tile(self.GameData.player["Player"].get_direct(self.GameData.player["Player"].facing)).object_filling].clear_speaking_queue()
            self.GameController.set_keyboard_manager(InGame.ID)
            self.GameData.character_list[self.GameController.current_speaker].set_state("idle")
            self.GameController.set_text_box(None)
            self.GameController.set_speaker(None)


    def key_space(self):
        pass

    def key_control(self):
        pass

    def key_shift(self):
        pass

    def key_caps(self):
        pass


# Keyboard Manager for when you are looking at your profile card
class InProfile(KeyboardManager):
    ID = "IPM_Keyer"

    def __init__(self, GameController, GameData):
        self.GameController = GameController
        self.GameData = GameData

    def key_right(self):
        pass

    def key_left(self):
        pass

    def key_up(self):
        pass

    def key_down(self):
        pass

    def key_return(self):
        self.GameController.set_keyboard_manager(InGame.ID)
        self.GameController.remove_current_overlay("ID_card")

    def key_space(self):
        pass

    def key_control(self):
        self.GameController.set_keyboard_manager(InGame.ID)
        self.GameController.remove_current_overlay("ID_card")

    def key_shift(self):
        pass

    def key_caps(self):
        pass


# Keyboard Manager for when you are looking at your profile card
class InToDoList(KeyboardManager):
    ID = "ITDLM_Keyer"

    def __init__(self, GameController, GameData):
        self.GameController = GameController
        self.GameData = GameData

    def key_right(self):
        pass

    def key_left(self):
        pass

    def key_up(self):
        pass

    def key_down(self):
        pass

    def key_return(self):
        self.GameController.set_keyboard_manager(InGame.ID)
        self.GameController.remove_current_overlay("To_do_list")

    def key_space(self):
        pass

    def key_control(self):
        self.GameController.set_keyboard_manager(InGame.ID)
        self.GameController.remove_current_overlay("To_do_list")

    def key_shift(self):
        pass

    def key_caps(self):
        pass


class InYesNo(KeyboardManager):
    ID = "YN_Keyer"

    def __init__(self, GameController, GameData):
        self.GameController = GameController
        self.GameData = GameData

    def key_right(self):
        pass

    def key_left(self):
        pass

    def direction_key_released(self, direction):
        self.direction = direction
        if self.direction == Direction.DOWN:
            self.GameData.menu_list["yes_no_menu"].cursor_down()
        if self.direction == Direction.UP:
            self.GameData.menu_list["yes_no_menu"].cursor_up()

    def direction_key_pressed(self, direction):
        pass
    def key_up(self):
        pass

    def key_down(self):
        pass

    def key_return(self):
        self.GameData.menu_list[self.GameController.current_menu].choose_option()


    def key_space(self):
        pass

    def key_control(self):
        pass

    def key_shift(self):
        pass

    def key_caps(self):
        pass