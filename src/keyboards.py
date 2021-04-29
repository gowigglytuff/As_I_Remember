from abc import ABC, abstractmethod

import pygame

#TODO add other keyboards
class KeyboardManager(ABC):

    @property
    @abstractmethod
    def ID(self):
        pass

    def parse_key(self, key_pressed):
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

class InGameKeyboardManager(KeyboardManager):
    ID = "IG_Keyer"

    def __init__(self, GameController, GameData):
        self.GameController = GameController
        self.GameData = GameData

    def key_right(self):
        # changes players direction
        self.GameData.player["Player"].turn_right()

        # checks mapClasses - position_manager to see if the player is acing a wall or another object
        can_move = self.GameData.positioner[self.GameController.current_room].can_move(self.GameData.player["Player"])

        # checks mapClasses - positioner to see if player is facing a door
        is_door = self.GameData.positioner[self.GameController.current_room].check_door(self.GameData.player["Player"])

        # moves the player a single step if they are able to
        if can_move:
            self.GameData.player["Player"].walk_right()
            self.GameData.player["Player"].walk_cycle()
            self.GameController.LockInput()

        # moves the player through door to it's exit location in its exit room
        elif is_door:
            the_tile = self.GameData.player["Player"].get_facing_tile().object_filling
            self.GameData.positioner[self.GameController.current_room].through_door(self.GameData.room_list[self.GameController.current_room].door_list[the_tile])
        else:
            pass

    def key_left(self):
        # changes players direction
        self.GameData.player["Player"].turn_left()
        # checks mapClasses - position_manager to see if the player is acing a wall or another object
        can_move = self.GameData.positioner[self.GameController.current_room].can_move(self.GameData.player["Player"])
        # checks mapClasses - positioner to see if player is facing a door
        is_door = self.GameData.positioner[self.GameController.current_room].check_door(self.GameData.player["Player"])
        # moves the player a single step if they are able to
        if can_move:
            self.GameData.player["Player"].walk_left()
            self.GameData.player["Player"].walk_cycle()
            self.GameController.LockInput()
        # moves the player through door to it's exit location in its exit room
        elif is_door:
            print("hi")
            print("went through door!")
            the_tile = self.GameData.player["Player"].get_facing_tile().object_filling
            self.GameData.positioner[self.GameController.current_room].through_door(self.GameData.room_list[self.GameController.current_room].door_list[the_tile])
        else:
            pass

    def key_up(self):
        self.GameData.player["Player"].turn_back()
        can_move = self.GameData.positioner[self.GameController.current_room].can_move(self.GameData.player["Player"])
        is_door = self.GameData.positioner[self.GameController.current_room].check_door(self.GameData.player["Player"])
        if can_move:
            self.GameData.player["Player"].walk_back()
            self.GameData.player["Player"].walk_cycle()
            self.GameController.LockInput()
        elif is_door:
            print("went through door!")
            the_tile = self.GameData.player["Player"].get_facing_tile().object_filling
            self.GameData.positioner[self.GameController.current_room].through_door(self.GameData.room_list[self.GameController.current_room].door_list[the_tile])
        else:
            pass

    def key_down(self):
        self.GameData.player["Player"].turn_front()
        can_move = self.GameData.positioner[self.GameController.current_room].can_move(self.GameData.player["Player"])
        is_door = self.GameData.positioner[self.GameController.current_room].check_door(self.GameData.player["Player"])
        if can_move:
            self.GameData.player["Player"].walk_front()
            self.GameData.player["Player"].walk_cycle()
            self.GameController.LockInput()
        elif is_door:
            print("went through door!")
            the_tile = self.GameData.player["Player"].get_facing_tile().object_filling
            self.GameData.positioner[self.GameController.current_room].through_door(self.GameData.room_list[self.GameController.current_room].door_list[the_tile])
        else:
            pass

    def key_return(self):
        # interacts with the feature that is in the tile that the player is facing
        self.GameData.player["Player"].interact()



    def key_space(self):
        pass

    def key_control(self):
        self.GameController.set_keyboard_manager(InMenuKeyboardManager.ID)
        self.GameController.set_menu("testing_menu")

    def key_shift(self):
        self.GameController.set_keyboard_manager(InStartMenuKeyboardManager.ID)
        self.GameController.set_menu("start_menu")

    def key_caps(self):
        self.GameController.set_keyboard_manager(InTextKeyboardManager.ID)
        self.GameController.set_text_box("text_box")

class InMenuKeyboardManager(KeyboardManager):
    ID = "IM_Keyer"

    def __init__(self, GameController, GameData):
        self.GameController = GameController
        self.GameData = GameData

    def key_right(self):
        print("right")

    def key_left(self):
        print("left")

    def key_up(self):
        print("up")
        menu = self.GameData.menu_list["testing_menu"].menu_item_list
        menu.append(menu.pop(menu.index(menu[0])))

    def key_down(self):
        menu = self.GameData.menu_list["testing_menu"].menu_item_list
        menu.insert(0, menu.pop(-1))

    def key_return(self):
        self.GameController.set_keyboard_manager(InGameKeyboardManager.ID)
        self.GameController.set_menu(None)

    def key_space(self):
        pass

    def key_control(self):
        pass

    def key_shift(self):
        pass

class InStartMenuKeyboardManager(KeyboardManager):
    ID = "ISM_Keyer"

    def __init__(self, GameController, GameData):
        self.GameController = GameController
        self.GameData = GameData

    def key_right(self):
        print("right")

    def key_left(self):
        print("left")

    def key_up(self):
        print("close")
        self.GameData.menu_list["start_menu"].cursor_up()

    def key_down(self):
        self.GameData.menu_list["start_menu"].cursor_down()

    def key_return(self):
        menu_selection = self.GameData.menu_list["start_menu"].get_current_menu_item()
        if menu_selection == self.GameData.menu_list["start_menu"].menu_item_list[0]:
            print("You got out your pokedex!")
        elif menu_selection == self.GameData.menu_list["start_menu"].menu_item_list[1]:
            print("You checked on your pokemon!")
        elif menu_selection == self.GameData.menu_list["start_menu"].menu_item_list[2]:
            print("You looked in your bag!")
        elif menu_selection == self.GameData.menu_list["start_menu"].menu_item_list[7]:
            print("You exited the menu")
        self.GameController.set_keyboard_manager(InGameKeyboardManager.ID)
        self.GameController.set_menu(None)


    def key_space(self):
        pass

    def key_control(self):
        self.GameController.set_keyboard_manager(InGameKeyboardManager.ID)
        self.GameController.set_menu(None)

    def key_shift(self):
        pass

class InTextKeyboardManager(KeyboardManager):
    ID = "IT_Keyer"

    def __init__(self, GameController, GameData):
        self.GameController = GameController
        self.GameData = GameData

    def key_right(self):
        print("right")

    def key_left(self):
        print("left")

    def key_up(self):
        print("up")

    def key_down(self):
        print("down")

    def key_return(self):
        self.GameController.set_keyboard_manager(InGameKeyboardManager.ID)
        self.GameData.character_list[self.GameController.current_speaker].set_state("idle")
        self.GameController.set_text_box(None)
        self.GameController.set_speaker(None)


    def key_space(self):
        pass

    def key_control(self):
        pass

    def key_shift(self):
        pass

class InTalkingMenuKeyboardManager(KeyboardManager):
    ID = "ITKM_Keyer"

    def __init__(self, GameController, GameData):
        self.GameController = GameController
        self.GameData = GameData

    def key_right(self):
        print("right")

    def key_left(self):
        print("left")

    def key_up(self):
        print("close")
        self.GameData.menu_list["character_interact_menu"].cursor_up()

    def key_down(self):
        self.GameData.menu_list["character_interact_menu"].cursor_down()

    def key_return(self):
        menu_selection = self.GameData.menu_list["character_interact_menu"].get_current_menu_item()
        print(menu_selection)
        if menu_selection == self.GameData.menu_list["character_interact_menu"].menu_item_list[0]:
            self.GameController.set_speaker(self.GameData.player["Player"].get_facing_tile().object_filling)
            self.GameData.character_list[self.GameData.player["Player"].get_facing_tile().object_filling].set_state("talking")
            self.GameController.set_keyboard_manager(InTextKeyboardManager.ID)
            self.GameController.set_menu(None)


    def key_space(self):
        pass

    def key_control(self):
        self.GameController.set_keyboard_manager(InGameKeyboardManager.ID)
        self.GameController.set_menu(None)

    def key_shift(self):
        pass

# all possible keys to be used
# def key_right(self):
# def key_left(self):
#
# def key_up(self):
#
# def key_down(self):
#
# def key_return(self):
#
# def key_space(self):

# def key_control(self):