import pygame

from inventory import *
from items import *
from keyboards import *
from spritesheet import *
from menus import *


class Feature(object):
    def __init__(self, x, y, gc_input, gd_input):
        self.x = x
        self.y = y
        self.imagex = None
        self.imagey = None
        self.name = None
        self.img_width = None
        self.img_height = None
        self.cur_img = 0
        self.spritesheet = None
        try:
            self.img = self.spritesheet.get_image(0, 0)
        except AttributeError:
            self.img = None
        self.gc_input = gc_input
        self.gd_input = gd_input
        self.offset_y = None
        self.size_y = 1
        self.size_x = 1

    def set_image(self, img_x, img_y):
        self.img = self.spritesheet.get_image(img_x, img_y)


class Player(Feature):
    NAME = "Player"

    def __init__(self, x, y, gc_input, gd_input):
        super().__init__(x, y, gc_input, gd_input)
        self.x = None
        self.y = None
        self.imagex = 0
        self.imagey = 0

        self.state = "idle"
        self.drawing_priority = 2
        self.step_timer = pygame.USEREVENT + 7
        self.facing = Direction.DOWN
        self.direction = Direction.DOWN
        self.feature_type = "Player"
        self.width = 32
        self.height = 40
        self.spritesheet = Spritesheet("assets/player/Player_CS.png", 32, 40)
        self.img = self.spritesheet.get_image(0, 0)
        self.name = self.NAME
        self.current_outfit = "Normal Outfit"
        self.offset_y = 16

    def load_location(self):
        ss_data = self.gd_input.spreadsheet_list["player_location"].spreadsheet_load_location()
        self.x = ss_data["player_x"]
        self.y = ss_data["player_y"]
        self.imagex = ss_data["player_image_x"]
        self.imagey = ss_data["player_image_y"]

    def put_on_outfit(self, new_outfit_spritesheet, name):
        self.spritesheet = new_outfit_spritesheet
        if self.facing == Direction.DOWN:
            self.img = self.spritesheet.get_image(0, 0)
        if self.facing == Direction.UP:
            self.img = self.spritesheet.get_image(0, 1)
        if self.facing == Direction.RIGHT:
            self.img = self.spritesheet.get_image(0, 2)
        if self.facing == Direction.LEFT:
            self.img = self.spritesheet.get_image(0, 3)
        self.current_outfit = name

    def teleport_to_ringside(self):
        self.empty_tile_standing()
        self.gc_input.current_room = "Ringside"
        self.x = 80
        self.y = 80
        self.gc_input.camera[0] = 0 - self.x
        self.gc_input.camera[1] = 0 - self.y

    def teleport_to_sandpiper(self):
        self.empty_tile_standing()
        self.gc_input.current_room = "Sandpiper"
        self.x = 22
        self.y = 60
        self.gc_input.camera[0] = 0 - self.x
        self.gc_input.camera[1] = 0 - self.y

    def empty_tile_standing(self):
        self.gd_input.positioner_list[self.gc_input.current_room].empty_tile(self)

    def activate_timer(self):
        pygame.time.set_timer(self.step_timer, 20)

    def draw(self, screen):
        self_x = (self.imagex * self.gd_input.square_size[0]) + self.gd_input.base_locator_x
        self_y = ((self.imagey * self.gd_input.square_size[1]) - self.offset_y) + self.gd_input.base_locator_y
        screen.blit(self.img, [(self.imagex * self.gd_input.square_size[0]) + self.gd_input.base_locator_x,
                               ((self.imagey * self.gd_input.square_size[1]) - self.offset_y) + self.gd_input.base_locator_y])

    def try_door(self, direction):
        self.direction = direction
        the_tile = self.check_adj_tile(self.direction).object_filling
        self.gd_input.positioner_list[self.gc_input.current_room].through_door(self.gd_input.room_list[self.gc_input.current_room].door_list[the_tile])
        self.set_state("idle")

    def try_walk(self, direction):
        self.turn_player(direction)

        # checks mapClasses - position_manager to see if the player is facing a wall or another object
        can_move_player = self.gd_input.positioner_list[self.gc_input.current_room].check_adj_square_full(self, direction)

        # Check if player is going to enter a door
        is_door = self.gd_input.positioner_list[self.gc_input.current_room].check_door(self, direction)
        if is_door:
            self.try_door(direction)

        #  checks to make sure the character doesn't have any obstacles in the direction they want to move
        elif can_move_player:
            self.walk_player(direction)

    def turn_player(self, direction):
        if direction is Direction.LEFT:
            self.set_image(0, 3)
            self.facing = Direction.LEFT
        elif direction is Direction.RIGHT:
            self.set_image(0, 2)
            self.facing = Direction.RIGHT
        elif direction is Direction.UP:
            self.set_image(0, 1)
            self.facing = Direction.UP
        elif direction is Direction.DOWN:
            self.set_image(0, 0)
            self.facing = Direction.DOWN

    def walk_player(self, direction):
        self.state = direction

        self.gd_input.positioner_list[self.gc_input.current_room].empty_tile(self)
        if direction is Direction.LEFT:
            self.x -= 1
        elif direction is Direction.RIGHT:
            self.x += 1
        elif direction is Direction.UP:
            self.y -= 1
        elif direction is Direction.DOWN:
            self.y += 1
        self.gd_input.positioner_list[self.gc_input.current_room].fill_tile(self)

    def walk_cycle(self):
        row = 0
        relevant_camera = None
        movement = 0
        if self.state == Direction.LEFT:
            row = 3
            relevant_camera = 0
            movement = 1 / 4
        elif self.state == Direction.RIGHT:
            row = 2
            relevant_camera = 0
            movement = -1 / 4
        elif self.state == Direction.DOWN:
            row = 0
            relevant_camera = 1
            movement = -1 / 4
        elif self.state == Direction.UP:
            row = 1
            relevant_camera = 1
            movement = 1 / 4

        if 0 <= self.cur_img < 3:
            self.cur_img += 1
            self.set_image(self.cur_img, row)
            self.gc_input.camera[relevant_camera] += movement

        elif self.cur_img == 3:
            self.cur_img = 0
            self.set_image(self.cur_img, row)
            self.gc_input.camera[relevant_camera] += movement
            self.set_state("idle")

        else:
            self.cur_img = 0
            self.set_image(0, row)

    def continue_walking(self):
        if self.state in [Direction.LEFT, Direction.RIGHT, Direction.UP, Direction.DOWN]:
            self.walk_cycle()

    def check_if_walking(self):
        if self.state in [Direction.LEFT, Direction.RIGHT, Direction.UP, Direction.DOWN]:
            return True
        else:
            return False

    def check_adj_tile(self, direction_to_check):
        self.direction_to_check = direction_to_check

        adj_tile_y = int(self.y)
        adj_tile_x = int(self.x)

        if direction_to_check == Direction.UP:
            adj_tile_y = int(self.y - 1)

        elif direction_to_check == Direction.DOWN:
            adj_tile_y = int(self.y + 1)

        elif direction_to_check == Direction.LEFT:
            adj_tile_x = int(self.x - 1)

        elif direction_to_check == Direction.RIGHT:
            adj_tile_x = int(self.x + 1)

        adj_tile = self.gd_input.room_list[self.gc_input.current_room].tiles_array[adj_tile_x][adj_tile_y]

        return adj_tile

    def interact_with(self):
        print("I'm interacting")
        facing_tile = self.check_adj_tile(self.facing)
        object_filling = facing_tile.object_filling
        filling_type = facing_tile.filling_type
        full = facing_tile.full

        if full:
            if filling_type in ["Generic_NPC", "NPC"]:
                self.gd_input.character_list[object_filling].get_interacted_with()

            elif filling_type == "Prop":
                self.gd_input.prop_list[object_filling].get_interacted_with()

            elif filling_type == "Door":
                pass

            else:
                pass

    def set_state(self, state_to_set):
        self.state = state_to_set

    def perform_diagnostic(self):
        # Player Image Location:
        print("PlayerImg: " + "(" + str(self.imagex) + ", " + str(self.imagey) + ")", "Camera: " +"(" + str(self.gc_input.camera[0]) + ", " + str(self.gc_input.camera[1]) + ")", "Player: " + "(" + str(self.x) + ", " + str(self.y) + ")")


class NPC(Feature):
    WALK_LEFT = "walk_left"
    WALK_RIGHT = "walk_right"
    WALK_FRONT = "walk_front"
    WALK_BACK = "walk_back"
    TURNING_LEFT = "turning_left"
    TURNING_FRONT = "turning_front"
    TURNING_RIGHT = "turning_right"
    TURNING_BACK = "turning_back"
    IDLE = "idle"
    AVAILABLE_STATES = [WALK_BACK, WALK_RIGHT, WALK_BACK, WALK_FRONT, TURNING_BACK, TURNING_RIGHT, TURNING_FRONT, TURNING_LEFT, IDLE]
    NPC_TIMER_ID = 10

    def __init__(self, x, y, gc_input, gd_input, spritesheet, name, room, phrase, walk_pattern, start_facing, face_image):
        super().__init__(x, y, gc_input, gd_input)
        self.width = 32
        self.height = 40
        self.initiate = pygame.USEREVENT + NPC.NPC_TIMER_ID
        self.action_clock = pygame.USEREVENT + NPC.NPC_TIMER_ID + 1
        self.drawing_priority = 2
        self.feature_type = "NPC"
        self.offset_y = 16
        self.spritesheet = spritesheet
        self.name = name
        self.phrase = phrase
        self.walk_pattern = walk_pattern
        self.face_image = face_image.get_image(0, 0)
        self.room = room
        self.gd_input.room_list[self.room].add_room_character(self.name)
        self.get_step()
        self.phrase_thanks = "Hey, thanks!"

        self.friendship = 0
        self.state = "idle"
        self.imagex = x
        self.imagey = y
        self.facing = start_facing
        self.turn_npc(self.facing)
        self.current_step_number = 0

        assert self.state in self.AVAILABLE_STATES


    def turn_npc(self, direction):
        self.facing = direction
        if direction is Direction.LEFT:
            self.set_image(0, 3)
        elif direction is Direction.RIGHT:
            self.set_image(0, 2)
        elif direction is Direction.UP:
            self.set_image(0, 1)
        elif direction is Direction.DOWN:
            self.set_image(0, 0)
        self.set_state("idle")
        return True

    def npc_face_player(self):
        if self.gd_input.player["Player"].facing == Direction.UP:
            self.turn_npc(Direction.DOWN)
        elif self.gd_input.player["Player"].facing == Direction.DOWN:
            self.turn_npc(Direction.UP)
        elif self.gd_input.player["Player"].facing == Direction.LEFT:
            self.turn_npc(Direction.RIGHT)
        elif self.gd_input.player["Player"].facing == Direction.RIGHT:
            self.turn_npc(Direction.LEFT)

    def check_if_walking(self):
        if self.state in ["walk_left", "walk_right", "walk_front", "walk_back"]:
            self.walk_cycle()
        else:
            pass

    def try_npc_walk_direction(self, direction):
        success = False
        self.facing = direction
        can_walk = self.gd_input.positioner_list[self.room].can_move_NPC(self)
        if can_walk:
            self.npc_walk_direction(self.facing)
            success = True
        return success

    def npc_walk_direction(self, direction):
        if direction == Direction.LEFT:
            self.set_state("walk_left")
            self.gd_input.positioner_list[self.gc_input.current_room].empty_tile(self)
            self.x -= 1
            self.gd_input.positioner_list[self.gc_input.current_room].fill_tile(self)

        if direction == Direction.RIGHT:
            self.set_state("walk_right")
            self.gd_input.positioner_list[self.gc_input.current_room].empty_tile(self)
            self.x += 1
            self.gd_input.positioner_list[self.gc_input.current_room].fill_tile(self)

        if direction == Direction.UP:
            self.set_state("walk_back")
            self.gd_input.positioner_list[self.gc_input.current_room].empty_tile(self)
            self.y -= 1
            self.gd_input.positioner_list[self.gc_input.current_room].fill_tile(self)

        if direction == Direction.DOWN:
            self.set_state("walk_front")
            self.gd_input.positioner_list[self.gc_input.current_room].empty_tile(self)
            self.y += 1
            self.gd_input.positioner_list[self.gc_input.current_room].fill_tile(self)

    def walk_cycle(self):
        if self.state == "walk_left":
            if 0 <= self.cur_img < 3:
                self.cur_img += 1
                self.set_image(self.cur_img, 3)
                self.imagex -= 1 / 4

            elif self.cur_img == (3):
                self.cur_img = 0
                self.set_image(self.cur_img, 3)
                self.imagex -= 1 / 4
                self.set_state("idle")

            else:
                self.cur_img = 0
                self.set_image(self.cur_img, 3)

        elif self.state == "walk_right":
            if 0 <= self.cur_img < 3:
                self.cur_img += 1
                self.set_image(self.cur_img, 2)
                self.imagex += 1 / 4

            elif self.cur_img == (3):
                self.cur_img = 0
                self.set_image(self.cur_img, 2)
                self.imagex += 1 / 4
                self.set_state("idle")

            else:
                self.cur_img = 3
                self.set_image(self.cur_img, 2)

        elif self.state == "walk_front":
            if 0 <= self.cur_img < 3:
                self.cur_img += 1
                self.set_image(self.cur_img, 0)
                self.imagey += 1 / 4

            elif self.cur_img == (3):
                self.cur_img = 0
                self.set_image(self.cur_img, 0)

                self.imagey += 1 / 4
                self.set_state("idle")

            else:
                self.cur_img = 0
                self.set_image(self.cur_img, 0)
        elif self.state == "walk_back":
            if 0 <= self.cur_img < 3:
                self.cur_img += 1
                self.set_image(self.cur_img, 1)
                self.imagey -= 1 / 4

            elif self.cur_img == (3):
                self.cur_img = 0
                self.set_image(self.cur_img, 1)
                self.imagey -= 1 / 4
                self.set_state("idle")

            else:
                self.cur_img = 0
                self.set_image(self.cur_img, 1)

    def get_facing_tile(self):

        facing_tile_y = 0
        facing_tile_x = 0
        if self.facing == Direction.UP:
            facing_tile_y = int(self.y - 1)
            facing_tile_x = int(self.x)

        elif self.facing == Direction.DOWN:
            facing_tile_y = int(self.y + 1)
            facing_tile_x = int(self.x)

        elif self.facing == Direction.LEFT:
            facing_tile_y = int(self.y)
            facing_tile_x = int(self.x - 1)

        elif self.facing == Direction.RIGHT:
            facing_tile_y = int(self.y)
            facing_tile_x = int(self.x + 1)

        facing_tile = self.gd_input.room_list[self.gc_input.current_room].tiles_array[facing_tile_x][
            facing_tile_y]

        return facing_tile

    def draw(self, screen):
        screen.blit(self.img, [((self.imagex + self.gc_input.camera[0]) * self.gd_input.square_size[0])
                               + self.gd_input.base_locator_x, ((self.imagey + self.gc_input.camera[1])
                                                                * self.gd_input.square_size[
                                                                    1] - self.offset_y) + self.gd_input.base_locator_y])

    def set_state(self, state_to_set):
        self.state = state_to_set

    def get_step(self):
        if self.walk_pattern == "square":
            self.step = ["walk_left", "rest", "walk_front", "rest", "walk_right", "rest", "walk_back", "rest"]
        elif self.walk_pattern == "left_right":
            self.step = ["turning_left", "rest", "walk_left", "rest", "turning_right", "rest", "walk_right", "rest"]
        elif self.walk_pattern == "pace":
            self.step = ["walk_left", "walk_left", "walk_left", "turning_right", "walk_right", "walk_right", "walk_right", "turning_left"]
        elif self.walk_pattern == "stand_still":
            self.step = ["rest"]
        elif self.walk_pattern == "spin":
            self.step = ["turning_left", "turning_back", "turning_right", "turning_front"]
        elif self.walk_pattern == "stay_left":
            self.step = ["turning_left"]
        elif self.walk_pattern == "stay_right":
            self.step = ["turning_right"]
        elif self.walk_pattern == "stay_front":
            self.step = ["turning_front"]
        elif self.walk_pattern == "stay_back":
            self.step = ["turning_back"]
        elif self.walk_pattern == "random":
            self.step = ["random"]
        else:
            self.step = ["turning_right", "rest", "turning_front", "rest", "turning_left", "rest", "turning_front"]

    def do_activity(self):
        if self.state == "idle":
            result = self.step[self.current_step_number]
            success = False
            if result == "rest":
                pass
                success = True

            elif result in ["walk_left", "walk_right", "walk_front", "walk_back"]:
                if result == "walk_left":
                    success = self.try_npc_walk_direction(Direction.LEFT)
                elif result == "walk_right":
                    success = self.try_npc_walk_direction(Direction.RIGHT)
                elif result == "walk_front":
                    success = self.try_npc_walk_direction(Direction.DOWN)
                elif result == "walk_back":
                    success = self.try_npc_walk_direction(Direction.UP)

            elif result in ["turning_front", "turning_back", "turning_left", "turning_right"]:
                if result == "turning_front":
                    success = self.turn_npc(Direction.DOWN)
                elif result == "turning_back":
                    success = self.turn_npc(Direction.UP)
                elif result == "turning_left":
                    success = self.turn_npc(Direction.LEFT)
                elif result == "turning_right":
                    success = self.turn_npc(Direction.RIGHT)

            if success:
                if self.current_step_number == len(self.step) -1:
                    self.current_step_number = 0
                elif self.current_step_number < len(self.step) -1:
                    self.current_step_number += 1


# class GenericNPC(NPC):
#     WALK_LEFT = "walk_left"
#     WALK_RIGHT = "walk_right"
#     WALK_FRONT = "walk_front"
#     WALK_BACK = "walk_back"
#     TURNING_LEFT = "turning_left"
#     TURNING_FRONT = "turning_front"
#     TURNING_RIGHT = "turning_right"
#     TURNING_BACK = "turning_back"
#     IDLE = "idle"
#     AVAILABLE_STATES = [WALK_BACK, WALK_RIGHT, WALK_BACK, WALK_FRONT, TURNING_BACK, TURNING_RIGHT, TURNING_FRONT, TURNING_LEFT, IDLE]
#
#     def __init__(self, x, y, gc_input, gd_input, spritesheet, name, room, phrase, walk_pattern, start_facing, face_image):
#         super().__init__(x, y, gc_input, gd_input, spritesheet, name, room, phrase, walk_pattern, start_facing, face_image)
#         assert self.state in self.AVAILABLE_STATES
#         self.gift_reactions = {'bad': ["Cheese", "Bread"],
#                                'good': ["Book 1", "Book 2", "Book 3"]}
#
#     def activate_timers(self):
#         pygame.time.set_timer(self.initiate, 1000)
#         pygame.time.set_timer(self.action_clock, 80)
#
#     def get_interacted_with(self):
#         if self.state == "idle":
#             self.npc_face_player()
#             # TODO: Fix this to not be a string
#             self.gd_input.menu_list[ConversationOptionsMenu.NAME].set_menu(self.name)
#             self.set_state("talking")
#             self.gc_input.update_game_dialogue("You talked to " + self.name)
#         else:
#             pass
#
#     def receive_gift(self, gift_name):
#         reaction = self.parse_gift(gift_name)
#         if reaction == "good":
#             self.friendship += 5
#         elif reaction == "bad":
#             self.friendship -= 1
#         else:
#             self.friendship += 1
#         get_phrase = self.gd_input.spreadsheet_list["Thanks"].spreadsheet_get_phrase(self.name, reaction)
#         return get_phrase
#
#     def parse_gift(self, gift_name):
#         reaction = "neutral"
#         if gift_name in self.gift_reactions["good"]:
#             reaction = "good"
#         if gift_name in self.gift_reactions["bad"]:
#             reaction = "bad"
#         return reaction


class GenericNPC(NPC):
    WALK_LEFT = "walk_left"
    WALK_RIGHT = "walk_right"
    WALK_FRONT = "walk_front"
    WALK_BACK = "walk_back"
    TURNING_LEFT = "turning_left"
    TURNING_FRONT = "turning_front"
    TURNING_RIGHT = "turning_right"
    TURNING_BACK = "turning_back"
    IDLE = "idle"
    AVAILABLE_STATES = [WALK_BACK, WALK_RIGHT, WALK_BACK, WALK_FRONT, TURNING_BACK, TURNING_RIGHT, TURNING_FRONT, TURNING_LEFT, IDLE]

    def __init__(self, x, y, gc_input, gd_input, spritesheet, name, room, phrase, walk_pattern, start_facing, face_image, gst_input):
        super().__init__(x, y, gc_input, gd_input, spritesheet, name, room, phrase, walk_pattern, start_facing, face_image)
        assert self.state in self.AVAILABLE_STATES
        self.gst_input = gst_input
        self.gift_reactions = {'bad': ["Cheese", "Bread"],
                               'good': ["Book 1", "Book 2", "Book 3"]}

    def activate_timers(self):
        pygame.time.set_timer(self.initiate, 1000)
        pygame.time.set_timer(self.action_clock, 80)

    def get_interacted_with(self):
        if self.state == "idle":
            self.npc_face_player()
            # TODO: Fix this to not be a string
            self.gd_input.menu_list[ConversationOptionsMenu.NAME].set_menu(self.name)
            self.set_state("talking")
            self.gc_input.update_game_dialogue("You talked to " + self.name)
        else:
            pass

    def receive_gift(self, gift_name):
        reaction = self.parse_gift(gift_name)
        if reaction == "good":
            self.friendship += 5
        elif reaction == "bad":
            self.friendship -= 1
        else:
            self.friendship += 1
        get_phrase = self.gd_input.spreadsheet_list["Thanks"].spreadsheet_get_phrase(self.name, reaction)
        return get_phrase

    def parse_gift(self, gift_name):
        reaction = "neutral"
        if gift_name in self.gift_reactions["good"]:
            reaction = "good"
        if gift_name in self.gift_reactions["bad"]:
            reaction = "bad"
        return reaction

    def write_to_gamestate(self):
        self.gst_input.character_states[self.name] = {}
        self.gst_input.character_states[self.name]["x"] = self.x
        self.gst_input.character_states[self.name]["y"] = self.y
        self.gst_input.character_states[self.name]["imagex"] = self.imagex
        self.gst_input.character_states[self.name]["imagey"] = self.imagey
        self.gst_input.character_states[self.name]["friendship"] = self.friendship
        self.gst_input.character_states[self.name]["state"] = self.state
        self.gst_input.character_states[self.name]["facing"] = self.facing
        self.gst_input.character_states[self.name]["current step number"] = self.current_step_number


class GameMaster(NPC):
    WALK_LEFT = "walk_left"
    WALK_RIGHT = "walk_right"
    WALK_FRONT = "walk_front"
    WALK_BACK = "walk_back"
    TURNING_LEFT = "turning_left"
    TURNING_FRONT = "turning_front"
    TURNING_RIGHT = "turning_right"
    TURNING_BACK = "turning_back"
    IDLE = "idle"
    AVAILABLE_STATES = [WALK_BACK, WALK_RIGHT, WALK_BACK, WALK_FRONT, TURNING_BACK, TURNING_RIGHT, TURNING_FRONT, TURNING_LEFT, IDLE]

    def __init__(self, x, y, gc_input, gd_input, spritesheet, name, room, phrase, walk_pattern, start_facing, face_image):
        super().__init__(x, y, gc_input, gd_input, spritesheet, name, room, phrase, walk_pattern, start_facing, face_image)
        assert self.state in self.AVAILABLE_STATES
        self.gift_reactions = {'bad': ["Cheese", "Bread"],
                               'good': ["Book 1", "Book 2", "Book 3"]}

    def activate_timers(self):
        pygame.time.set_timer(self.initiate, 1000)
        pygame.time.set_timer(self.action_clock, 80)

    def get_interacted_with(self):
        if self.state == "idle":
            self.npc_face_player()
            # TODO: Fix this to not be a string
            self.gd_input.menu_list[GameMasterInteractMenu.NAME].set_menu(self.name)
            self.set_state("talking")
            self.gc_input.update_game_dialogue("You talked to " + self.name)
        else:
            pass

    def receive_gift(self, gift_name):
        get_phrase = self.gd_input.spreadsheet_list["Thanks"].spreadsheet_get_phrase(self.name, self.parse_gift(gift_name))
        return get_phrase

    def parse_gift(self, gift_name):
        reaction = "neutral"
        if gift_name in self.gift_reactions["good"]:
            reaction = "good"
        if gift_name in self.gift_reactions["bad"]:
            reaction = "bad"
        return reaction


class ShopKeeper(NPC):
    IDLE = "idle"
    AVAILABLE_STATES = [IDLE]

    def __init__(self, x, y, gc_input, gd_input, spritesheet, name, room, phrase, walk_pattern, start_facing, face_image):
        super().__init__(x, y, gc_input, gd_input, spritesheet, name, room, phrase, walk_pattern, start_facing, face_image)
        self.intro = "Hi, welcome to the shop! What can I help you with?"


    def activate_timers(self):
        pygame.time.set_timer(self.initiate, 1000)
        pygame.time.set_timer(self.action_clock, 80)

    def get_interacted_with(self):
        if self.state == "idle":
            self.npc_face_player()
            # TODO: Fix this to not be a string
            self.gd_input.menu_list[ShopkeeperDialogue.NAME].set_menu(self.name, self.intro)
            self.set_state("selling")
            self.gc_input.update_game_dialogue("You talked to " + self.name)
        else:
            pass


class ShopKeeperTamma(ShopKeeper):
    IDLE = "idle"
    AVAILABLE_STATES = [IDLE]

    def __init__(self, x, y, gc_input, gd_input, spritesheet, name, room, phrase, walk_pattern, start_facing, face_image):
        super().__init__(x, y, gc_input, gd_input, spritesheet, name, room, phrase, walk_pattern, start_facing, face_image)
        self.items_list = [(Cheese.NAME, 2), (Toy.NAME, 2), (Stick.NAME, 1)]
        self.intro = "Hi, welcome to the Hornby Creative! What can I help you with?"


class ShopKeeperCheryl(ShopKeeper):
    IDLE = "idle"
    AVAILABLE_STATES = [IDLE]

    def __init__(self, x, y, gc_input, gd_input, spritesheet, name, room, phrase, walk_pattern, start_facing, face_image):
        super().__init__(x, y, gc_input, gd_input, spritesheet, name, room, phrase, walk_pattern, start_facing, face_image)
        self.items_list = [(Book1.NAME, 5), (Book2.NAME, 7), (Book3.NAME, 10)]
        self.intro = "Hi, welcome to the the Book store! What can I help you with?"




