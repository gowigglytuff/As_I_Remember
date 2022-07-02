import pygame

from inventory import *
from menus import *
import pickle


class Game(object):
    def __init__(self, state, tick):
        self.state = state
        self.tick = tick


class GameData(object):
    def __init__(self):
        self.settings = {}
        self.settings["resolution"] = (1000, 1000)
        self.settings["FPS"] = 30
        self.square_size = [32, 32]
        self.base_locator_x = self.settings["resolution"][0]/2 - self.square_size[0]/2
        self.base_locator_y = self.settings["resolution"][1]/2 - self.square_size[1]/2

        self.player = {}
        self.character_list = {}
        self.prop_list = {}
        self.decoration_list = {}

        self.room_list = {}
        self.positioner_list = {}
        self.door_list = {}
        self.tiles_img_dict = {}
        self.keyboard_manager_list = {}

        self.menu_list = {}
        self.overlay_list = {}
        self.item_list = {}
        self.key_item_list = {}
        self.goal_list = {}
        self.outfit_list = {}
        self.spreadsheet_list = {}

    def add_character(self, character_name, character_object):
        self.character_list[character_name] = character_object

    def add_player(self, player_name, player_object):
        self.player[player_name] = player_object

    def add_keyboard_manager(self, keyboard_manager_name, keyboard_manager_object):
        self.keyboard_manager_list[keyboard_manager_name] = keyboard_manager_object

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
    def __init__(self, gd_input):
        self.gd_input = gd_input



class GameController(object):
    def __init__(self, gd_input, gst_input):
        self.gst_input = gst_input  # type: GameState
        self.gd_input = gd_input  # type: GameData
        self.inventory = None # type: Inventory
        self.menu_manager = None # type: MenuManager
        self.screen = pygame.display.set_mode(gd_input.settings["resolution"])
        self._FPS = gd_input.settings["FPS"]
        self.font = "assets/fonts/PressStart.ttf"
        self.current_keyboard_manager = None # type: KeyboardManager
        self.current_menu = None # type: Menu
        self.clock = pygame.time.Clock()
        self.night_filter = pygame.Surface(pygame.Rect((0, 0, self.gd_input.settings["resolution"][0], self.gd_input.settings["resolution"][1])).size)

        self.number_of_sky_change_hours = 6
        self.fully_dark_hours = 4
        self.sky_darkening_degree = 15
        self.new_game = True # type: bool
        # self.read_all_controls()


        self.current_room = "Ringside" # type: str
        self.camera = [-79, -79]
        self.your_coins = 127  # type: int
        self.your_seeds = 24  # type: int
        self.total_seeds_found = 26 # type: int
        self.total_seeds_findable = 100  # type: int
        self.day_of_summer = 12  # type: int
        self.time_of_day = 14  # type: int
        self.night_filter_current_alpha = 0 # type: int

        self.night_filter.set_alpha(self.night_filter_current_alpha)

    def write_all_to_gamestate(self):
        self.write_all_controls()
        self.write_all_characters()
        self.write_all_player()

    def write_all_player(self):
        player_state_dict = {}
        player_state_dict["player_x"] = self.gd_input.player["Player"].x
        player_state_dict["player_y"] = self.gd_input.player["Player"].y
        player_state_dict["player_image_x"] = self.gd_input.player["Player"].imagex
        player_state_dict["player_image_y"] = self.gd_input.player["Player"].imagey
        self.gst_input.player_state = player_state_dict
        print(self.gst_input.player_state)

    def write_all_controls(self):
        states_dict = {}
        states_dict["game_data"] = {}
        states_dict["game_data"]["your_coins"] = self.your_coins
        states_dict["game_data"]["camera"] = self.camera
        states_dict["game_data"]["current_room"] = self.current_room
        states_dict["game_data"]["your_seeds"] = self.your_seeds
        states_dict["game_data"]["day_of_summer"] = self.day_of_summer
        states_dict["game_data"]["time_of_day"] = self.time_of_day
        states_dict["game_data"]["night_filter_current_alpha"] = self.night_filter_current_alpha
        self.gst_input.game_controls = states_dict
        print(self.gst_input.game_controls)

    def write_all_characters(self):
        characters_dict = {}
        for character in self.gd_input.character_list:
            try:
                characters_dict[self.gd_input.character_list[character].name] = {}
                characters_dict[self.gd_input.character_list[character].name]["x"] = self.gd_input.character_list[character].x
                characters_dict[self.gd_input.character_list[character].name]["y"] = self.gd_input.character_list[character].y
                characters_dict[self.gd_input.character_list[character].name]["imagex"] = self.gd_input.character_list[character].imagex
                characters_dict[self.gd_input.character_list[character].name]["imagey"] = self.gd_input.character_list[character].imagey
                characters_dict[self.gd_input.character_list[character].name]["friendship"] = self.gd_input.character_list[character].friendship
                characters_dict[self.gd_input.character_list[character].name]["state"] = self.gd_input.character_list[character].state
                characters_dict[self.gd_input.character_list[character].name]["facing"] = self.gd_input.character_list[character].facing
                characters_dict[self.gd_input.character_list[character].name]["current step number"] = self.gd_input.character_list[character].current_step_number
                characters_dict[self.gd_input.character_list[character].name]["cur_img"] = self.gd_input.character_list[character].cur_img
                print("Wrote " + character)
            except:
                print("An error occured for " + character)

        self.gst_input.character_states = characters_dict

    def pickle_gamestate(self):
        self.write_all_controls()
        self.write_all_player()
        self.write_all_characters()
        pickle_out = open("gamestate.pickle", "wb")
        pickle.dump(self.gst_input, pickle_out)
        pickle_out.close()

        # save stuff
    def read_all_states(self):
        self.read_all_controls()
        self.read_all_player()
        # self.read_all_characters()

    def read_all_controls(self):
        states_dict = self.gst_input.game_controls
        self.your_coins = states_dict["game_data"]["your_coins"]
        self.camera = states_dict["game_data"]["camera"]
        self.current_room = states_dict["game_data"]["current_room"]
        self.your_seeds = states_dict["game_data"]["your_seeds"]
        self.day_of_summer = states_dict["game_data"]["day_of_summer"]
        self.time_of_day = states_dict["game_data"]["time_of_day"]
        self.night_filter_current_alpha = states_dict["game_data"]["night_filter_current_alpha"]

        self.night_filter.set_alpha(self.night_filter_current_alpha)

    def read_all_characters(self):
        characters_dict = self.gst_input.character_states
        for character in self.gd_input.character_list:
            try:
                self.gd_input.character_list[self.gd_input.character_list[character].name].x = characters_dict[self.gd_input.character_list[character].name]["x"]
                self.gd_input.character_list[self.gd_input.character_list[character].name].y = characters_dict[self.gd_input.character_list[character].name]["y"]
                self.gd_input.character_list[self.gd_input.character_list[character].name].imagex = characters_dict[self.gd_input.character_list[character].name]["imagex"]
                self.gd_input.character_list[self.gd_input.character_list[character].name].imagey = characters_dict[self.gd_input.character_list[character].name]["imagey"]
                self.gd_input.character_list[self.gd_input.character_list[character].name].friendship = characters_dict[self.gd_input.character_list[character].name]["friendship"]
                self.gd_input.character_list[self.gd_input.character_list[character].name].state = characters_dict[self.gd_input.character_list[character].name]["state"]
                self.gd_input.character_list[self.gd_input.character_list[character].name].facing = characters_dict[self.gd_input.character_list[character].name]["facing"]
                self.gd_input.character_list[self.gd_input.character_list[character].name].current_step_number = characters_dict[self.gd_input.character_list[character].name]["current step number"]
                self.gd_input.character_list[character].cur_img = characters_dict[self.gd_input.character_list[character].name]["cur_img"]
                print("Read " + self.gd_input.character_list[character].name)
            except:
                print("An error occured while reading " + self.gd_input.character_list[character].name)

    def read_all_player(self):
        self.gd_input.player["Player"].x = self.gst_input.player_state["player_x"]
        self.gd_input.player["Player"].y = self.gst_input.player_state["player_y"]
        self.gd_input.player["Player"].imagex = self.gst_input.player_state["player_image_x"]
        self.gd_input.player["Player"].imagey = self.gst_input.player_state["player_image_y"]

    # setters
    def set_current_keyboard_manager(self, active_manager):
        self.current_keyboard_manager = self.gd_input.keyboard_manager_list[active_manager]

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

        for character in self.gd_input.room_list[fillable].character_list:
            if character != None:
                drawables_list.append(self.gd_input.character_list[character])

        for prop in self.gd_input.room_list[fillable].prop_list:
            drawables_list.append(self.gd_input.prop_list[prop])

        drawables_list.append(self.gd_input.player["Player"])

        return drawables_list

    # wallet stuff
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

    # other
    def update_game_dialogue(self, phrase):
        self.gd_input.menu_list[GameActionDialogue.NAME].show_dialogue(phrase)

    # time stuff
    def display_night_sky_layer(self, surface):
        pygame.draw.rect(self.night_filter, (0, 0, 25), self.night_filter.get_rect())
        surface.blit(self.night_filter, (0, 0, self.gd_input.settings["resolution"][0], self.gd_input.settings["resolution"][1]))

    def darken_sky(self):
        self.night_filter_current_alpha += self.sky_darkening_degree
        self.night_filter.set_alpha(self.night_filter_current_alpha)

    def lighten_sky(self):
        self.night_filter_current_alpha -= self.sky_darkening_degree
        self.night_filter.set_alpha(self.night_filter_current_alpha)

    def tick_hour(self):
        if self.time_of_day < 24:
            self.time_of_day += 1
        elif self.time_of_day == 24:
            self.time_of_day = 1

        # darken/lighten sky
        if (24-(self.fully_dark_hours/2)-self.number_of_sky_change_hours) <= self.time_of_day <= (24-(self.fully_dark_hours/2)):
            self.darken_sky()
        elif (1 + (self.fully_dark_hours / 2)) <= self.time_of_day <= (1 + (self.fully_dark_hours / 2) + self.number_of_sky_change_hours):
            self.lighten_sky()


class GameState(object):
    def __init__(self):
        self.player_state = {}
        self.game_controls = {}
        self.character_states = {}
        self.prop_states = {}

    def pickle_characters(self):
        pickle_out = open("character_states.pickle", "wb")
        pickle.dump(self.character_states, pickle_out)
        pickle_out.close()

    def unpickle_characters(self):
        pickle_in = open("character_states.pickle", "rb")
        self.character_states = pickle.load(pickle_in)
        print(self.character_states)
        pickle_in.close()

    def pickle_self(self):
        pickle_out = open("GAMESTATE.pickle", "wb")
        pickle.dump(GameState, pickle_out)
        pickle_out.close()

    def unpickle_self(self):
        pickle_in = open("GAMESTATE.pickle", "rb")
        g = pickle.load(pickle_in)
        print(g.game_controls)
        pickle_in.close()

class Updater(object):
    def __init__(self, gd_input, gc_input):
        self.gd_input = gd_input
        self.gc_input = gc_input

    def run_updates(self):
        self.gd_input.menu_list[StatsMenu.NAME].update_menu_items_list()


class EventsManager(object):
    def __init__(self, gd_input, gc_input):
        self.gd_input = gd_input
        self.gc_input = gc_input
        self.step_timer = pygame.USEREVENT + 6

    def start_events(self):
        pygame.time.set_timer(self.step_timer, 60)


class Picaso(object):
    def __init__(self, gd_input, gc_input):
        self.gd_input = gd_input
        self.gc_input = gc_input

    def get_all_drawable(self):
        drawables_list = []
        for character in self.gd_input.room_list[self.gc_input.current_room].character_list:
            drawables_list.append(self.gd_input.character_list[character])

        for prop in self.gd_input.room_list[self.gc_input.current_room].prop_list:
            drawables_list.append(self.gd_input.prop_list[prop])

        for decoration in self.gd_input.room_list[self.gc_input.current_room].decoration_list:
            drawables_list.append(self.gd_input.decoration_list[decoration])

        drawables_list.append(self.gd_input.player["Player"])

        drawing_order = []

        # for drawable in drawables_list:
        #     for height in range(drawable.size_y):
        #         height += 1
        #         drawing_order.append((drawable.name, drawable.y + height, drawable.drawing_priority, height))

        for drawable in drawables_list:
            rect_base = [drawable.x, drawable.y, drawable.size_x, drawable.size_y]
            drawing_order.append((drawable.name, drawable.y, drawable.drawing_priority))
            print(rect_base)

        drawing_order = sorted(drawing_order, key=lambda x: (x[1], x[2]))


        final_drawing_list =[]
        for drawable in drawing_order:
            for drawabl2 in drawables_list:
                if drawabl2.name == drawable[0]:
                    final_drawing_list.append([drawabl2])


        # drawables_list = sorted(drawables_list, key=lambda x: (x.y, x.drawing_priority))
        return final_drawing_list

    def big_draw(self):
        # Blits the background for the current room
        self.gd_input.room_list[self.gc_input.current_room].draw_bg(self.gc_input.screen)

        # Gets all the drawables and prints them in order of y and printing priority
        drawable_list = self.get_all_drawable()
        for drawable in drawable_list:
            drawable[0].draw(self.gc_input.screen)

        # Draws the square that makes it lighter or darker depending on time of day
        self.gc_input.display_night_sky_layer(self.gc_input.screen)

        # Draws the menus that are always on screen
        for item in self.gc_input.menu_manager.static_menus:
            self.gd_input.menu_list[item].display_menu()

        # Draws the temporary menus that are currently visible
        for item in self.gc_input.menu_manager.visible_menus:
            self.gd_input.menu_list[item].display_menu()
