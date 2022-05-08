import pygame

from inventory import *
from menus import *


class Game(object):
    def __init__(self, state, tick):
        self.state = state
        self.tick = tick


class GameData(object):
    def __init__(self):
        self.settings = {}
        self.settings["resolution"] = (1800, 1000)
        self.settings["FPS"] = 30
        self.square_size = [32, 32]
        self.base_locator_x = self.settings["resolution"][0]/2 - self.square_size[0]/2
        self.base_locator_y = self.settings["resolution"][1]/2 - self.square_size[1]/2
        self.room_list = {}
        self.prop_list = {}
        self.decoration_list = {}
        self.door_list = {}
        self.menu_list = {}
        self.overlay_list = {}
        self.character_list = {}
        self.player = {}
        self.positioner_list = {}
        self.item_list = {}
        self.key_item_list = {}
        self.tiles_img_dict = {}
        self.goal_list = {}
        self.outfit_list = {}
        self.spreadsheet_list = {}

    def get_all_drawables(self):
        return list(self.character_list.values()) + list(self.player.values()) + list(self.prop_list.values())

    def add_character(self, character_name, character_object):
        self.character_list[character_name] = character_object

    def add_player(self, player_name, player_object):
        self.player[player_name] = player_object

    def add_room(self, room_name, room_object):
        self.room_list[room_name] = room_object

    def add_door(self, door_name, door_object):
        self.door_list[door_name] = door_object

    # Decorations are images that have no substance in the game and thus cannot be interacted with in any way
    def add_decoration(self, decoration_name, decoration_object):
        self.decoration_list[decoration_name] = decoration_object

    # Each room has a positioner which manages how objects are positioned in the room
    def add_positioner(self, positioner_name, positioner_object):
        self.positioner_list[positioner_name] = positioner_object

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

    def add_goal(self, goal_name, goal_object):
        self.goal_list[goal_name] = goal_object

    def add_outfit(self, outfit_name, outfit_object):
        self.outfit_list[outfit_name] = outfit_object

    def add_spreadsheet(self, spreadsheet_name, spreadsheet_object):
        self.spreadsheet_list[spreadsheet_name] = spreadsheet_object


# TODO: Make this in charge of some things
class GameSettings(object):
    def __init__(self, GameData):
        self.GameData = GameData


class GameController(object):
    def __init__(self, GameData):
        self.GameData = GameData
        self.inventory = None
        self.menu_manager = None # type: MenuManager
        self.screen = pygame.display.set_mode(GameData.settings["resolution"])
        self.clock = pygame.time.Clock()
        self._FPS = GameData.settings["FPS"]
        self.font = "assets/fonts/PressStart.ttf"
        self.current_room = "Ringside"
        self.camera = [-24-55, -79]
        self.current_menu = None # type: Menu
        self.keyboard_manager_list = {}
        self.current_keyboard_manager = None # type: KeyboardManager
        self.current_key_pressed = None
        self.your_coins = 127
        self.your_seeds = 24
        self.day_of_summer = 12
        self.time_of_day = 17
        self.night_filter = pygame.Surface(pygame.Rect((0, 0, self.GameData.settings["resolution"][0], self.GameData.settings["resolution"][1])).size)
        self.night_filter.set_alpha(0)

    def load_saved_data(self):
        ss_data = self.GameData.spreadsheet_list["player_location"].spreadsheet_load_location()
        self.camera[0] = ss_data["camera_x"]
        self.camera[1] = ss_data["camera_y"]
        self.current_room = ss_data["current_room"]

    def save_game(self):
        self.GameData.spreadsheet_list["player_location"].write_to_workbook(self.GameData.player["Player"].x, self.GameData.player["Player"].y, self.camera[0], self.camera[1], self.current_room)

    def add_keyboard_manager(self, keyboard_manager_name, keyboard_manager_object):
        self.keyboard_manager_list[keyboard_manager_name] = keyboard_manager_object

    def set_keyboard_manager(self, active_manager):
        self.current_keyboard_manager = self.keyboard_manager_list[active_manager]

    def set_current_menu(self, active_menu):
        self.current_menu = active_menu

    def set_room(self, active_room):
        self.current_room = active_room

    def set_inventory(self, inv):
        self.inventory = inv

    def set_menu_manager(self, mm):
        self.menu_manager = mm

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
        self.GameData.menu_list[GameActionDialogue.NAME].show_dialogue(phrase)

    # TODO: Edit for efficiency
    def display_night_sky_layer(self, surface):
        pygame.draw.rect(self.night_filter, (0, 0, 25), self.night_filter.get_rect())
        surface.blit(self.night_filter, (0, 0, self.GameData.settings["resolution"][0], self.GameData.settings["resolution"][1]))

    def darken_sky(self):
        self.night_filter.set_alpha(self.night_filter.get_alpha()+20)

    def lighten_sky(self):
        self.night_filter.set_alpha(self.night_filter.get_alpha()-20)

    def tick_hour(self):
        print("Did it?")
        if self.time_of_day < 23:
            self.time_of_day += 1

        elif self.time_of_day == 23:
            self.time_of_day = 0

        if 16 <= self.time_of_day <= 23:
            self.darken_sky()

        elif 1 <= self.time_of_day <= 8:
            self.lighten_sky()

        print("tod:" + str(self.time_of_day))

class Updater(object):
    def __init__(self, GameData, GameController):
        self.GameData = GameData
        self.GameController = GameController


    def run_updates(self):
        self.GameData.menu_list[StatsMenu.NAME].update_menu_items_list()


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

        # TODO: Make this work for night time
        self.GameController.display_night_sky_layer(self.GameController.screen)

        for item in self.GameController.menu_manager.static_menus:
            self.GameData.menu_list[item].display_menu()

        for item in self.GameController.menu_manager.visible_menus:
            self.GameData.menu_list[item].display_menu()


class Camera(object):
    def __init__(self, GameController, GameData, coordinates, anchor):
        self.GameData = GameData
        self.GameController = GameController
        self.anchor = anchor
        self.coordinates = [5 - self.anchor.x, 5 - self.anchor.y]

