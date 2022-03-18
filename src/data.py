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
        self.item_list = {}
        self.key_item_list = {}
        self.tiles_img_dict = {}

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

    # Decorations are images that have no substance in the game and thus cannot be interacted with in any way
    def add_decoration(self, decoration_name, decoration_object):
        self.decoration_list[decoration_name] = decoration_object

    # Each room has a positioner which manages how objects are positioned in the room
    def add_positioner(self, positioner_name, positioner_object):
        self.positioner[positioner_name] = positioner_object

    # Adds props to the game, props are items that can be moved
    def add_prop(self, prop_name, prop_object):
        self.prop_list[prop_name] = prop_object

    def add_item(self, item_name, item_object):
        self.item_list[item_name] = item_object

    def add_key_item(self, key_item_name, key_item_object):
        self.key_item_list[key_item_name] = key_item_object

    def add_menu(self, menu_name, menu_object):
        self.menu_list[menu_name] = menu_object

    def add_overlay(self, overlay_name, overlay_object):
        self.overlay_list[overlay_name] = overlay_object

    def add_tile_dict(self, tiles_dict):
        self.tiles_img_dict = tiles_dict


class GameController(object):
    def __init__(self, GameData, MenuManager):
        self.GameData = GameData
        self.MenuManager = MenuManager
        self.inventory = None
        self.menu_manager = None
        self.screen = pygame.display.set_mode(GameData.settings["resolution"])
        self.clock = pygame.time.Clock()
        self._FPS = GameData.settings["FPS"]
        self.font = "assets/fonts/PressStart.ttf"
        self.current_room = "Ringside"
        self.camera = [-24, -79]
        self.current_overlay_list = ["top_bar"]
        self.current_menu = None # type: Menu
        self.current_text_box = None # type: Overlay
        self.current_speaker = None
        self.keyboard_manager_list = {}
        self.current_keyboard_manager = None # type: KeyboardManager
        self.current_key_pressed = None
        self.your_coins = 9
        self.your_seeds = 30


    def add_keyboard_manager(self, keyboard_manager_name, keyboard_manager_object):
        self.keyboard_manager_list[keyboard_manager_name] = keyboard_manager_object

    def set_keyboard_manager(self, active_manager, menu=None, origin=None):
        self.current_keyboard_manager = self.keyboard_manager_list[active_manager]
        if menu is not None:
            self.MenuManager.activate_menu(menu)
        if origin is not None:
            self.GameData.menu_list[menu].set_origin(origin)

    def set_current_menu(self, active_menu):
        self.current_menu = active_menu

    def set_room(self, active_room):
        self.current_room = active_room

    def add_current_overlay(self, overlay_name):
        self.current_overlay_list.append(overlay_name)

    def remove_current_overlay(self, overlay_name):
        self.current_overlay_list.remove(overlay_name)

    def set_inventory(self, inv):
        self.inventory = inv

    def set_menu_manager(self, mm):
        self.menu_manager = mm

    def set_text_box(self, active_text_box):
        self.current_text_box = active_text_box

    def set_speaker(self, active_speaker):
        self.current_speaker = active_speaker

    def tick(self):
        self.clock.tick(self._FPS)

    def get_current_drawables(self, fillable):
        drawables_list = []

        for character in self.GameData.room_list[fillable].character_list:
            if character != None:
                drawables_list.append(self.GameData.character_list[character])
        for prop in self.GameData.room_list[fillable].prop_list:
            drawables_list.append(self.GameData.prop_list[prop])
        drawables_list.append(self.GameData.player["Player"])
        return drawables_list

    def get_coins(self, amount):
        self.your_coins = self.your_coins + amount

    def use_coins(self, amount):
        self.your_coins = self.your_coins - amount

    def try_use_coins(self, amount):
        success = False
        if self.your_coins >= amount:
            self.use_coins(amount)
            success = True
        else:
            success = False
        return success

    def update_game_dialogue(self, phrase):
        self.GameData.menu_list["game_action_dialogue_menu"].show_dialogue(phrase)

class Updater(object):
    def __init__(self, GameData, GameController):
        self.GameData = GameData
        self.GameController = GameController


    def run_updates(self):
        self.GameData.menu_list["stats_menu"].update_menu_items_list()

    def check_for_goals(self):
        pass
        #TODO: make this run through a list of goals and see if any are completed

class Goal(object):
    def __init__(self, name, requirement, reward, status):
        self.requirement = requirement
        self.reward = reward
        self.name = name
        self.status = status

# TODO: Fix this whole mess
class Goallist(object):
    def __init__(self, GameData, GameController):
        self.GameData = GameData
        self.GameController = GameController
        self.goal1_complete = False
        self.goal_1 = None
        self.goal_2 = None

    def add_goals(self):
        if self.goal_1 == None:
            self.goal_1 = Goal("goal 1", ("You saved the game!" in self.GameData.menu_list["game_action_dialogue_menu"].menu_item_list), "TimeSeed", "incomplete")
        if self.goal_2 == None:
            self.goal_2 = Goal("goal 2", self.GameController.current_speaker == "Donna", "Item2", "incomplete")

    def update_goals(self):
        if self.goal_1.status != "complete":
            self.goal_1.requirement = ("You saved the game!" in self.GameData.menu_list["game_action_dialogue_menu"].menu_item_list)
        if self.goal_2.status != "complete":
            self.goal_2.requirement = self.GameController.current_speaker == "Donna"


    def check_goal(self, goal_to_check):
        if goal_to_check.status == "incomplete":
            self.update_goals()
            if goal_to_check.requirement:
                self.GameController.update_game_dialogue(str(goal_to_check.name) + " done, have a " + goal_to_check.reward + "!")
                self.GameController.inventory.get_item(goal_to_check.reward, 1)
                goal_to_check.status = "complete"
                print(goal_to_check.status)
                return True
            else:
                return False
        else:
            pass

    def check_goal_1(self):
        self.check_goal(self.goal_1)
        self.check_goal(self.goal_2)

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
        drawing_order = []
        for drawable in drawables_list:
            for height in range(drawable.size_y):
                height += 1
                drawing_order.append((drawable.name, drawable.y+height, drawable.drawing_priority, height))

        drawing_order = sorted(drawing_order, key=lambda x: (x[1], x[2]))


        final_drawing_list =[]
        for drawable in drawing_order:
            for drawabl2 in drawables_list:
                if drawabl2.name == drawable[0]:
                    final_drawing_list.append([drawabl2, drawable[3]])


        # drawables_list = sorted(drawables_list, key=lambda x: (x.y, x.drawing_priority))
        # print(drawables_list)
        return final_drawing_list

    def big_draw(self):
        # Blits the background for the current room
        self.GameData.room_list[self.GameController.current_room].draw_bg(self.GameController.screen)

        # get's all the drawables and prints them in order of y and printing priority
        drawable_list = self.get_all_drawable()
        for drawable in drawable_list:
            drawable[0].draw(self.GameController.screen)

        for item in self.GameController.MenuManager.static_menus:
            self.GameData.menu_list[item].display_menu()

        for item in self.GameController.MenuManager.active:
            self.GameData.menu_list[item].display_menu()




        # blits any overlays that are always active and ons tghat are associated with currently active menus
        for overlay in self.GameController.current_overlay_list:
            self.GameData.overlay_list[overlay].display_overlay()

        if self.GameController.current_speaker != None:
            self.GameData.overlay_list["text_box"].display_overlay()
            self.GameData.overlay_list["text_box"].display_phrase(self.GameController.current_speaker)


class Camera(object):
    def __init__(self, GameController, GameData, coordinates, anchor):
        self.GameData = GameData
        self.GameController = GameController
        self.anchor = anchor
        self.coordinates = [5 - self.anchor.x, 5 - self.anchor.y]

