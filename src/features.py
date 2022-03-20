import random

import pygame
from spritesheet import *
from random import choice
from keyboards import *
import textwrap


class Feature(object):
    def __init__(self, x, y, gc_input, gd_input):
        self.x = x
        self.y = y
        self.imagex = None
        self.imagey = None
        self.name = None
        self.width = None
        self.height = None
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
    def __init__(self, x, y, gc_input, gd_input):
        super().__init__(x, y, gc_input, gd_input)
        self.x = 24
        self.y = 79
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
        self.spritesheet = Spritesheet("assets/NPC_sprites/Shuma_CS.png", 32, 40)
        self.img = self.spritesheet.get_image(0, 0)
        self.name = "Bug"
        self.offset_y = 16

    def teleport_to_ringside(self):
        self.gc_input.current_room = "Ringside"
        self.x = 22
        self.y = 60
        self.gc_input.camera[0] = 0 - self.x
        self.gc_input.camera[1] = 0 - self.y

    def activate_timer(self):
        pygame.time.set_timer(self.step_timer, 30)

    def draw(self, screen):
        self_x = (self.imagex * self.gd_input.square_size[0]) + self.gd_input.base_locator_x
        self_y = ((self.imagey * self.gd_input.square_size[1]) - self.offset_y) + self.gd_input.base_locator_y
        screen.blit(self.img, [(self.imagex * self.gd_input.square_size[0]) + self.gd_input.base_locator_x,
                               ((self.imagey * self.gd_input.square_size[1]) - self.offset_y) + self.gd_input.base_locator_y])

    def try_door(self, direction):
        self.direction = direction
        the_tile = self.check_adj_tile(self.direction).object_filling
        self.gd_input.positioner[self.gc_input.current_room].through_door(
            self.gd_input.room_list[self.gc_input.current_room].door_list[the_tile])
        self.set_state("idle")

    #TODO: Fix this so that it doesn't screw up when you go through a door
    def try_walk(self, direction):
        self.turn_player(direction)

        # checks mapClasses - position_manager to see if the player is acing a wall or another object
        can_move_player = self.gd_input.positioner[self.gc_input.current_room].check_adj_square_full(self.gd_input.player["Player"], direction)

        # Check if player is going to enter a door
        is_door = self.gd_input.positioner[self.gc_input.current_room].check_door(self.gd_input.player["Player"], direction)
        if is_door:
            self.gd_input.player["Player"].try_door(direction)

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

        self.gd_input.positioner[self.gc_input.current_room].empty_tile(self)
        if direction is Direction.LEFT:
            self.x -= 1
        elif direction is Direction.RIGHT:
            self.x += 1
        elif direction is Direction.UP:
            self.y -= 1
        elif direction is Direction.DOWN:
            self.y += 1
        self.gd_input.positioner[self.gc_input.current_room].fill_tile(self)

    def walk_cycle(self):
        if self.state == Direction.LEFT:
            if 0 <= self.cur_img < 3:
                self.cur_img += 1
                self.set_image(self.cur_img, 3)
                self.gc_input.camera[0] += 1 / 4

            elif self.cur_img == (3):
                self.cur_img = 0
                self.set_image(self.cur_img, 3)
                self.gc_input.camera[0] += 1 / 4
                self.set_state("idle")

            else:
                self.cur_img = 0
                self.set_image(0, 3)

        elif self.state == Direction.RIGHT:
            if 0 <= self.cur_img < 3:
                self.cur_img += 1
                self.set_image(self.cur_img, 2)
                self.gc_input.camera[0] -= 1 / 4

            elif self.cur_img == (3):
                self.cur_img = 0
                self.set_image(self.cur_img, 2)
                self.gc_input.camera[0] -= 1 / 4
                self.set_state("idle")

            else:
                self.cur_img = 0
                self.set_image(0, 2)

        elif self.state == Direction.DOWN:
            if 0 <= self.cur_img < 3:
                self.cur_img += 1
                self.set_image(self.cur_img, 0)
                self.gc_input.camera[1] -= 1 / 4

            elif self.cur_img == (3):
                self.cur_img = 0
                self.set_image(self.cur_img, 0)
                self.gc_input.camera[1] -= 1 / 4
                self.set_state("idle")

            else:
                self.cur_img = 0
                self.set_image(0, 0)


        elif self.state == Direction.UP:
            if 0 <= self.cur_img < 3:
                self.cur_img += 1
                self.set_image(self.cur_img, 1)

                self.gc_input.camera[1] += 1 / 4

            elif self.cur_img == (3):
                self.cur_img = 0
                self.set_image(self.cur_img, 1)
                self.gc_input.camera[1] += 1 / 4
                self.set_state("idle")

            else:
                self.cur_img = 0
                self.set_image(0, 1)

    def continue_walking(self):
        if self.state == Direction.LEFT:
            self.walk_cycle()

        elif self.state == Direction.RIGHT:
            self.walk_cycle()

        elif self.state == Direction.UP:
            self.walk_cycle()

        elif self.state == Direction.DOWN:
            self.walk_cycle()

    def check_if_walking(self):
        if self.state in [Direction.LEFT, Direction.RIGHT, Direction.UP, Direction.DOWN]:
            return True
        else:
            return False

    def check_adj_tile(self, direction_to_check):
        self.direction_to_check = direction_to_check

        adj_tile_y = 0
        adj_tile_x = 0
        if direction_to_check == Direction.UP:
            adj_tile_y = int(self.y - 1)
            adj_tile_x = int(self.x)

        elif direction_to_check == Direction.DOWN:
            adj_tile_y = int(self.y + 1)
            adj_tile_x = int(self.x)

        elif direction_to_check == Direction.LEFT:
            adj_tile_y = int(self.y)
            adj_tile_x = int(self.x - 1)

        elif direction_to_check == Direction.RIGHT:
            adj_tile_y = int(self.y)
            adj_tile_x = int(self.x + 1)

        adj_tile = self.gd_input.room_list[self.gc_input.current_room].tiles_array[adj_tile_x][adj_tile_y]

        return adj_tile

    def interact_with(self):
        print("I'm interacting")
        facing_tile = self.check_adj_tile(self.get_direct(self.facing))
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

    def get_direct(self, direct):
        choice = direct
        returning_direction = None
        if choice == Direction.LEFT:
            returning_direction = Direction.LEFT
        elif choice == Direction.RIGHT:
            returning_direction = Direction.RIGHT
        elif choice == Direction.DOWN:
            returning_direction = Direction.DOWN
        elif choice == Direction.UP:
            returning_direction = Direction.UP

        return returning_direction

    def perform_diagnostic(self):
        #Player Location:
        print("(" + str(self.x) + ", " + str(self.y) + ")")

        #Player Image Location:
        print("(" + str(self.imagex) + ", " + str(self.imagey) + ")")

        #Camera Location
        print("(" + str(self.gc_input.camera[0]) + ", " + str(self.gc_input.camera[1]) + ")")

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

    NPC_TIMER_ID = 10

    def __init__(self, x, y, gc_input, gd_input, spritesheet, name, room, phrase, walk_pattern, start_facing, face_image):
        super().__init__(x, y, gc_input, gd_input)
        self.width = 32
        self.height = 40
        self.set_state("idle")
        self.initiate = pygame.USEREVENT + NPC.NPC_TIMER_ID
        self.action_clock = pygame.USEREVENT + NPC.NPC_TIMER_ID + 1
        self.drawing_priority = 2
        self.friendship = 0
        self.feature_type = "NPC"
        self.offset_y = 16

        self.imagex = x
        self.imagey = y

        self.spritesheet = spritesheet
        self.name = name
        self.phrase = phrase
        self.walk_pattern = walk_pattern
        self.facing = start_facing
        self.turn_npc(self.facing)
        self.face_image = face_image.get_image(0, 0)

        self.room = room
        self.gd_input.room_list[self.room].add_room_character(self.name)
        self.current_step_number = 0
        self.get_step()
        self.phrase_thanks = "Hey, thanks!"
        NPC.NPC_TIMER_ID += 2

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
        self.facing = direction
        can_walk = self.gd_input.positioner[self.room].can_move_NPC(self)
        if can_walk:
            self.npc_walk_direction(self.facing)

    def npc_walk_direction(self, direction):
        if direction == Direction.LEFT:
            self.set_state("walk_left")
            self.gd_input.positioner[self.gc_input.current_room].empty_tile(self)
            self.x -= 1
            self.gd_input.positioner[self.gc_input.current_room].fill_tile(self)

        if direction == Direction.RIGHT:
            self.set_state("walk_right")
            self.gd_input.positioner[self.gc_input.current_room].empty_tile(self)
            self.x += 1
            self.gd_input.positioner[self.gc_input.current_room].fill_tile(self)

        if direction == Direction.UP:
            self.set_state("walk_back")
            self.gd_input.positioner[self.gc_input.current_room].empty_tile(self)
            self.y -= 1
            self.gd_input.positioner[self.gc_input.current_room].fill_tile(self)

        if direction == Direction.DOWN:
            self.set_state("walk_front")
            self.gd_input.positioner[self.gc_input.current_room].empty_tile(self)
            self.y += 1
            self.gd_input.positioner[self.gc_input.current_room].fill_tile(self)

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
            if self.current_step_number == len(self.step) -1:
                self.current_step_number = 0
            elif self.current_step_number < len(self.step) -1:
                self.current_step_number += 1
            result = self.step[self.current_step_number]

            if result == "rest":
                pass

            elif result in ["walk_left", "walk_right", "walk_front", "walk_back"]:
                if result == "walk_left":
                    self.try_npc_walk_direction(Direction.LEFT)
                elif result == "walk_right":
                    self.try_npc_walk_direction(Direction.RIGHT)
                elif result == "walk_front":
                    self.try_npc_walk_direction(Direction.DOWN)
                elif result == "walk_back":
                    self.try_npc_walk_direction(Direction.UP)

            elif result in ["turning_front", "turning_back", "turning_left", "turning_right"]:
                if result == "turning_front":
                    self.turn_npc(Direction.DOWN)
                elif result == "turning_back":
                    self.turn_npc(Direction.UP)
                elif result == "turning_left":
                    self.turn_npc(Direction.LEFT)
                elif result == "turning_right":
                    self.turn_npc(Direction.RIGHT)


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

    def __init__(self, x, y, gc_input, gd_input, spritesheet, name, room, phrase, walk_pattern, start_facing, face_image):
        super().__init__(x, y, gc_input, gd_input, spritesheet, name, room, phrase, walk_pattern, start_facing, face_image)
        assert self.state in self.AVAILABLE_STATES


    def activate_timers(self):
        pygame.time.set_timer(self.initiate, 1000)
        pygame.time.set_timer(self.action_clock, 80)

    def get_interacted_with(self):
        if self.state == "idle":
            self.npc_face_player()
            self.gd_input.menu_list["conversation_options_menu_2"].set_menu(self.name)
            self.set_state("talking")
            self.gc_input.update_game_dialogue("You talked to " + self.name)
        else:
            pass

    def receive_gift(self):
        pass


class ShopKeeper(NPC):
    IDLE = "idle"
    AVAILABLE_STATES = [IDLE]

    def __init__(self, x, y, gc_input, gd_input, spritesheet, name, room, phrase, walk_pattern, start_facing, face_image):
        super().__init__(x, y, gc_input, gd_input, spritesheet, name, room, phrase, walk_pattern, start_facing, face_image)

    def activate_timers(self):
        pygame.time.set_timer(self.initiate, 1000)
        pygame.time.set_timer(self.action_clock, 80)

    def get_interacted_with(self):
        if self.state == "idle":
            self.npc_face_player()
            self.gd_input.menu_list["shopkeeper_interact_menu_2"].set_menu(self.name)
            self.set_state("selling")
        else:
            pass


class ShopKeeperTamma(ShopKeeper):
    IDLE = "idle"
    AVAILABLE_STATES = [IDLE]

    def __init__(self, x, y, gc_input, gd_input, spritesheet, name, room, phrase, walk_pattern, start_facing, face_image):
        super().__init__(x, y, gc_input, gd_input, spritesheet, name, room, phrase, walk_pattern, start_facing, face_image)
        self.items_list = [("Cheese", 2), ("Item1", 2), ("Stick", 1)]


class ShopKeeperCheryl(ShopKeeper):
    IDLE = "idle"
    AVAILABLE_STATES = [IDLE]

    def __init__(self, x, y, gc_input, gd_input, spritesheet, name, room, phrase, walk_pattern, start_facing, face_image):
        super().__init__(x, y, gc_input, gd_input, spritesheet, name, room, phrase, walk_pattern, start_facing, face_image)
        self.items_list = [("Book 1", 5), ("Book 2", 7), ("Book 3", 10)]





