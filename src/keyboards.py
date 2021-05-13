from abc import ABC, abstractmethod

import pygame

#TODO add other keyboards
class KeyboardManager(ABC):

    @property
    @abstractmethod
    def ID(self):
        pass

    def parse_key(self, key_pressed):
        self.key_pushed()

        if key_pressed == pygame.K_RIGHT:
            self.key_right()

        if key_pressed == pygame.K_LEFT:
            self.key_left()

        if key_pressed == pygame.K_DOWN:
            self.key_down()

        if key_pressed == pygame.K_UP:
            self.key_up()

        if key_pressed == pygame.K_RETURN:
            self.key_return()

        if key_pressed == pygame.K_SPACE:
            self.key_space()

        if key_pressed == pygame.K_LCTRL:
            self.key_control()

        if key_pressed == pygame.K_LSHIFT:
            self.key_shift()

        if key_pressed == pygame.K_CAPSLOCK:
            self.key_caps()

    def key_pushed(self):
        pass

    @abstractmethod
    def key_right(self):
        pass

    @abstractmethod
    def key_left(self):
        pass

    @abstractmethod
    def key_down(self):
        pass

    @abstractmethod
    def key_up(self):
        pass

    @abstractmethod
    def key_return(self):
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

    def key_pushed(self):
        self.GameController.key_held = True

    def key_right(self):
        self.GameData.player["Player"].try_walk_right()

    def key_left(self):
        self.GameData.player["Player"].try_walk_left()

    def key_up(self):
        self.GameData.player["Player"].try_walk_back()

    def key_down(self):
        self.GameData.player["Player"].try_walk_front()

    def key_return(self):
        # interacts with the feature that is in the tile that the player is facing
        self.GameData.player["Player"].interact_with()

    def key_space(self):
        for x in self.GameData.room_list["room2"].tiles_array:
            for y in x:

                print(y.x, y.y, y.terrain)

    def key_control(self):
        self.GameController.set_keyboard_manager(InStartMenu.ID)
        #         # self.GameController.set_menu("start_menu")
        self.GameController.MenuManager.start_menu = True


    def key_shift(self):
        pass

    def key_caps(self):
        pass


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

    def key_up(self):
        self.GameData.menu_list["start_menu"].cursor_up()

    def key_down(self):
        self.GameData.menu_list["start_menu"].cursor_down()

    def key_return(self):
        menu_selection = self.GameData.menu_list["start_menu"].get_current_menu_item()
        if menu_selection == "Bag":
            print("You looked in your bag!")

            # self.GameController.set_menu(None)
            self.GameController.MenuManager.start_menu = False
            self.GameController.MenuManager.inventory_menu = True
            self.GameController.set_keyboard_manager(InInventory.ID)
            self.GameData.menu_list["start_menu"].reset_cursor()

        elif menu_selection == "Key Items":
            print("You looked in your bag!")

            # self.GameController.set_menu(None)
            self.GameController.MenuManager.start_menu = False
            self.GameController.MenuManager.key_inventory_menu = True
            self.GameController.set_keyboard_manager(InKeyInventory.ID)
            self.GameData.menu_list["start_menu"].reset_cursor()

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
        self.GameController.MenuManager.inventory_menu = False
        self.GameController.MenuManager.key_inventory_menu = True
        self.GameController.set_keyboard_manager(InKeyInventory.ID)

    def key_left(self):
        self.GameController.MenuManager.inventory_menu = False
        self.GameController.MenuManager.key_inventory_menu = True
        self.GameController.set_keyboard_manager(InKeyInventory.ID)

    def key_up(self):
        self.GameData.menu_list["inventory_menu"].cursor_up()

    def key_down(self):
        self.GameData.menu_list["inventory_menu"].cursor_down()

    def key_return(self):
        menu_selection = self.GameData.menu_list["inventory_menu"].get_current_menu_item()
        self.GameController.inventory.select_item(menu_selection)
        self.GameController.set_keyboard_manager(InUseInventory.ID)
        self.GameController.MenuManager.use_menu = True

    def key_space(self):
        pass

    def key_control(self):
        pass

    def key_shift(self):
        pass

    def key_caps(self):
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

    def key_up(self):
        self.GameData.menu_list["use_menu"].cursor_up()

    def key_down(self):
        self.GameData.menu_list["use_menu"].cursor_down()

    def key_return(self):
        menu_selection = self.GameData.menu_list["use_menu"].get_current_menu_item()

        if menu_selection == "Use":
            self.GameData.item_list[self.GameController.inventory.selected_item].use_item()

            # self.GameController.set_menu(None)
            self.GameController.inventory.select_item(None)
            self.GameController.MenuManager.use_menu = False
            self.GameController.set_keyboard_manager(InGame.ID)
            self.GameController.MenuManager.inventory_menu = False

        elif menu_selection == "Toss":
            print("You looked in your bag!")

            # self.GameController.set_menu(None)
            self.GameController.MenuManager.use_menu = False
            self.GameController.set_keyboard_manager(InGame.ID)
            self.GameController.MenuManager.inventory_menu = False
            self.GameController.MenuManager.key_inventory_menu = False

        elif menu_selection == "Exit":

            print("You looked in your bag!")
            # self.GameController.set_menu(None)
            self.GameController.MenuManager.use_menu = False
            self.GameController.set_keyboard_manager(InGame.ID)
            self.GameController.MenuManager.inventory_menu = False
            self.GameController.MenuManager.key_inventory_menu = False

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

    def key_right(self):
        self.GameController.MenuManager.key_inventory_menu = False
        self.GameController.MenuManager.inventory_menu = True
        self.GameController.set_keyboard_manager(InInventory.ID)

    def key_left(self):
        self.GameController.MenuManager.key_inventory_menu = False
        self.GameController.MenuManager.inventory_menu = True
        self.GameController.set_keyboard_manager(InInventory.ID)

    def key_up(self):
        self.GameData.menu_list["key_inventory_menu"].cursor_up()

    def key_down(self):
        self.GameData.menu_list["key_inventory_menu"].cursor_down()

    def key_return(self):
        menu_selection = self.GameData.menu_list["key_inventory_menu"].get_current_menu_item()
        self.GameController.inventory.select_item(menu_selection)
        self.GameController.set_keyboard_manager(InUseKeyInventory.ID)
        self.GameController.MenuManager.use_menu = True

    def key_space(self):
        pass

    def key_control(self):
        pass

    def key_shift(self):
        pass

    def key_caps(self):
        pass


# Keyboard Manager for when the player has selected an item in key inventory and is deciding what to do with it
class InUseKeyInventory(KeyboardManager):
    ID = "IUKM_Keyer"

    def __init__(self, GameController, GameData):
        self.GameController = GameController
        self.GameData = GameData

    def key_right(self):
        pass

    def key_left(self):
        pass

    def key_up(self):
        self.GameData.menu_list["use_menu"].cursor_up()

    def key_down(self):
        self.GameData.menu_list["use_menu"].cursor_down()

    def key_return(self):
        menu_selection = self.GameData.menu_list["use_menu"].get_current_menu_item()

        if menu_selection == "Use":
            self.GameData.key_item_list[self.GameController.inventory.selected_item].use_item()

            # self.GameController.set_menu(None)
            self.GameController.inventory.select_item(None)
            self.GameController.MenuManager.use_menu = False
            self.GameController.set_keyboard_manager(InGame.ID)
            self.GameController.MenuManager.key_inventory_menu = False

        elif menu_selection == "Toss":
            print("You looked in your bag!")

            # self.GameController.set_menu(None)
            self.GameController.MenuManager.use_menu = False
            self.GameController.set_keyboard_manager(InGame.ID)
            self.GameController.MenuManager.inventory_menu = False
            self.GameController.MenuManager.key_inventory_menu = False

        elif menu_selection == "Exit":

            print("You looked in your bag!")
            # self.GameController.set_menu(None)
            self.GameController.MenuManager.use_menu = False
            self.GameController.set_keyboard_manager(InGame.ID)
            self.GameController.MenuManager.inventory_menu = False
            self.GameController.MenuManager.key_inventory_menu = False

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

    def key_up(self):
        self.GameData.menu_list["character_interact_menu"].cursor_up()

    def key_down(self):
        self.GameData.menu_list["character_interact_menu"].cursor_down()

    def key_return(self):
        #TODO: Fix this to use characters name instead of facing tile
        menu_selection = self.GameData.menu_list["character_interact_menu"].get_current_menu_item()
        if menu_selection == self.GameData.menu_list["character_interact_menu"].menu_item_list[0]:
            self.GameController.set_speaker(self.GameData.player["Player"].get_facing_tile().object_filling)
            self.GameData.character_list[self.GameData.player["Player"].get_facing_tile().object_filling].set_state("talking")
            self.GameData.character_list[self.GameData.player["Player"].get_facing_tile().object_filling].set_current_phrase()
            self.GameData.character_list[self.GameData.player["Player"].get_facing_tile().object_filling].set_speaking_queue()
            self.GameController.set_keyboard_manager(InConversation.ID)
            self.GameData.menu_list["character_interact_menu"].set_talking_to(None)
            self.GameController.MenuManager.character_interact_menu = False
        elif menu_selection == "Exit":
            self.GameController.set_keyboard_manager(InGame.ID)
            self.GameController.MenuManager.character_interact_menu = False
            self.GameData.character_list[self.GameData.player["Player"].get_facing_tile().object_filling].set_state(
                "idle")

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

    def key_up(self):
        pass

    def key_down(self):
        pass

    def key_return(self):
        if self.GameData.character_list[self.GameData.player["Player"].get_facing_tile().object_filling].current_phrase != None:
            self.GameData.character_list[self.GameData.player["Player"].get_facing_tile().object_filling].set_speaking_queue()
        else:
            self.GameData.character_list[
                self.GameData.player["Player"].get_facing_tile().object_filling].clear_speaking_queue()
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