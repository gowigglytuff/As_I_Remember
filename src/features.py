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
        self.imagex = x
        self.imagey = y
        self.state = "idle"
        self.drawing_priority = 2
        self.step_timer = pygame.USEREVENT + 7
        self.facing = Direction.DOWN
        self.direction = Direction.DOWN
        self.feature_type = "Player"
        self.width = 32
        self.height = 40
        self.spritesheet = Spritesheet("assets/NPC_sprites/Shuma.png", 32, 40)
        self.img = self.spritesheet.get_image(0, 0)
        self.name = "Bug"
        self.offset_y = 16

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

class NPC(Feature):

    NPC_TIMER_ID = 10

    def __init__(self, x, y, gc_input, gd_input):
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



        NPC.NPC_TIMER_ID += 2

    # TODO: make sets of walking behaviour types that different NPC can have (back and forth/look around/square/etc.)

    def turn_left(self):
        self.set_image(0, 3)
        self.facing = Direction.LEFT
        self.set_state("idle")
        self.set_state("idle")

    def turn_right(self):
        self.set_image(1, 2)
        self.facing = Direction.RIGHT
        self.set_state("idle")

    def turn_front(self):
        self.set_image(0, 0)
        self.facing = Direction.DOWN
        self.set_state("idle")

    def turn_back(self):
        self.set_image(0, 1)
        self.facing = Direction.UP
        self.set_state("idle")

    def check_if_walking(self):
        if self.state == "walk_left":
            self.walk_cycle()

        if self.state == "walk_right":
            self.walk_cycle()

        if self.state == "walk_front":
            self.walk_cycle()

        if self.state == "walk_back":
            self.walk_cycle()

        elif self.state == "say_hi":
            print("Hello everyone!")
            self.set_state("idle")

    def walk_left(self):
        self.set_state("walk_left")
        self.gd_input.positioner[self.gc_input.current_room].empty_tile(self)
        self.x -= 1
        self.gd_input.positioner[self.gc_input.current_room].fill_tile(self)

    def walk_right(self):
        self.set_state("walk_right")
        self.gd_input.positioner[self.gc_input.current_room].empty_tile(self)
        self.x += 1
        self.gd_input.positioner[self.gc_input.current_room].fill_tile(self)

    def walk_front(self):
        self.set_state("walk_front")
        self.gd_input.positioner[self.gc_input.current_room].empty_tile(self)
        self.y += 1
        self.gd_input.positioner[self.gc_input.current_room].fill_tile(self)

    def walk_back(self):
        self.set_state("walk_back")
        self.gd_input.positioner[self.gc_input.current_room].empty_tile(self)
        self.y -= 1
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

    def set_phrase(self, phrase_to_set):
        self.current_phrase = phrase_to_set

    def set_state(self, state_to_set):
        self.state = state_to_set



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
        super().__init__(x, y, gc_input, gd_input)
        assert self.state in self.AVAILABLE_STATES
        #TODO: make it so you assign each NPC a movement type and then they move based on that
        self.actions = ["walk_left", "walk_right", "walk_front", "walk_back", "turning_left", "turning_front", "turning_right", "turning_back", "rest", "rest"]
        self.available_actions = ["turn"]
        self.spritesheet = spritesheet
        self.state = "idle"
        self.phrase = phrase
        self.current_phrase = None
        self.speaking_queue = None #textwrap.wrap("Hi everyone, it's so nice to see you here today! I hope you have all been doing well", width=30)
        self.facing = start_facing
        self.face_image = face_image.get_image(0, 0)

        if self.facing == Direction.DOWN:
            self.img = self.spritesheet.get_image(0, 0)
        elif self.facing == Direction.UP:
            self.img = self.spritesheet.get_image(0, 1)
        elif self.facing == Direction.RIGHT:
            self.img = self.spritesheet.get_image(0, 2)
        elif self.facing == Direction.LEFT:
            self.img = self.spritesheet.get_image(0, 3)
        self.imagex = x
        self.imagey = y

        self.name = name
        self.phrase = phrase

        self.current_step_number = 0
        self.walk_pattern = walk_pattern
        #TODO: Make it so you can't interupt the pattern, make them start at a random spot in the pattern
        if self.walk_pattern == "square":
            self.step = ["walk_left", "rest", "walk_front", "rest", "walk_right", "rest", "walk_back", "rest"]
        elif self.walk_pattern == "left_right":
            self.step = ["turning_left", "rest", "walk_left", "rest", "turning_right", "rest", "walk_right", "rest"]
        elif self.walk_pattern == "pace":
            self.step = ["walk_left", "walk_left", "walk_left", "turning_right", "walk_right", "walk_right", "walk_right", "turning_left"]
        elif self.walk_pattern == "stand_still":
            self.step = ["rest"]
        elif self.walk_pattern == "stay_left":
            self.step = ["turning_left"]
        elif self.walk_pattern == "stay_right":
            self.step = ["turning_right"]
        elif self.walk_pattern == "stay_front":
            self.step = ["turning_front"]
        elif self.walk_pattern == "stay_back":
            self.step = ["turning_back"]
        else:
            self.step = ["turning_right", "rest", "turning_front", "rest", "turning_left", "rest", "turning_front"]

        self.room = room
        self.gd_input.room_list[self.room].add_room_character(self.name)

    def activate_timers(self):
        pygame.time.set_timer(self.initiate, 1000)
        pygame.time.set_timer(self.action_clock, 80)

    def do_activity(self):
        if self.state == "idle":
            if self.current_step_number == len(self.step) -1:
                self.current_step_number = 0
            elif self.current_step_number < len(self.step) -1:
                self.current_step_number += 1
            result = self.step[self.current_step_number]


            if result == "rest":
                pass

            if result == "walk_left":
                self.facing = Direction.LEFT
                can_walk = self.gd_input.positioner[self.room].can_move_NPC(self)
                if can_walk:
                    self.walk_left()

            elif result == "walk_right":
                self.facing = Direction.RIGHT
                can_walk = self.gd_input.positioner[self.room].can_move_NPC(self)
                if can_walk:
                    self.walk_right()

            elif result == "walk_front":
                self.facing = Direction.DOWN
                can_walk = self.gd_input.positioner[self.room].can_move_NPC(self)
                if can_walk:
                    self.walk_front()

            elif result == "walk_back":
                self.facing = Direction.UP
                can_walk = self.gd_input.positioner[self.room].can_move_NPC(self)
                if can_walk:
                    self.walk_back()

            elif result == "turning_front":
                self.turn_front()

            elif result == "turning_back":
                self.turn_back()

            elif result == "turning_left":
                self.turn_left()

            elif result == "turning_right":
                self.turn_right()

    def get_interacted_with(self):
        # TODO: Fix all of this mess - make their picture pop up in their speech bubble thing
        if self.state == "idle":
            if self.gd_input.player["Player"].facing == Direction.UP:
                self.turn_front()
            elif self.gd_input.player["Player"].facing == Direction.DOWN:
                self.turn_back()
            elif self.gd_input.player["Player"].facing == Direction.LEFT:
                self.turn_right()
            elif self.gd_input.player["Player"].facing == Direction.RIGHT:
                self.turn_left()
            self.gd_input.menu_list["conversation_options_menu"].set_menu(self.name)
            # self.gd_input.menu_list["conversation_options_menu"].set_talking_to(self.name)
            self.set_state("talking")
            self.gc_input.update_game_dialogue("You talked to " + self.name)

    def speak(self, chosen_phrase):
        my_font = pygame.font.Font(self.gc_input.font, 10)
        item = my_font.render(self.name + ":", 1, (0, 0, 0))
        self.gc_input.screen.blit(item, (
            self.gd_input.overlay_list["text_box"].x + 150, self.gd_input.overlay_list["text_box"].y + 20))

        my_font = pygame.font.Font(self.gc_input.font, 10)
        item = my_font.render(chosen_phrase, 1, (0, 0, 0))
        self.gc_input.screen.blit(item, (self.gd_input.overlay_list["text_box"].x + 150, self.gd_input.overlay_list["text_box"].y + 60))

    def display_name(self):
        my_font = pygame.font.Font(self.gc_input.font, 10)
        item = my_font.render(self.name + ":", 1, (0, 0, 0))
        self.gc_input.screen.blit(item, (self.gd_input.overlay_list["text_box"].x + 150, self.gd_input.overlay_list["text_box"].y + 20))

    def test_speak(self):
        text_line = 0
        for line in self.current_phrase:
            my_font = pygame.font.Font(self.gc_input.font, 10)
            item = my_font.render(line, 1, (0, 0, 0))
            self.gc_input.screen.blit(item, (self.gd_input.overlay_list["text_box"].x + 150, self.gd_input.overlay_list["text_box"].y + 60 + 25 * text_line))
            text_line += 1

    def set_current_phrase(self):
        self.current_phrase = textwrap.wrap(self.phrase, width=30)

    def set_speaking_queue(self):

        phrase_counter = 0
        self.speaking_queue = []
        for line in range(3):
            if len(self.current_phrase) > 0:
                self.speaking_queue.append(self.current_phrase[0])
                self.current_phrase.pop(0)

        if len(self.current_phrase) == 0:
            self.current_phrase = None

    def clear_speaking_queue(self):
        self.speaking_queue = None

    def receive_gift(self):
        pass


class ShopKeeper(NPC):
    IDLE = "idle"
    AVAILABLE_STATES = [IDLE]

    def __init__(self, x, y, gc_input, gd_input, room):
        super().__init__(x, y, gc_input, gd_input)

        self.actions = ["turning_left", "turning_front", "turning_right", "rest", "rest", "rest", "rest"]
        self.available_actions = ["turning_front"]
        self.spritesheet = Spritesheet("assets/NPC_sprites/Tamma_CS.png", 32, 40)
        self.state = "idle"
        self.phrase = "Hi, welcome to my store, what would you like to do?"
        self.current_phrase = None
        self.speaking_queue = None #textwrap.wrap("Hi everyone, it's so nice to see you here today! I hope you have all been doing well", width=30)
        self.img = self.spritesheet.get_image(0, 0)
        self.imagex = x
        self.imagey = y
        self.name = "Tamma"
        self.items_list = [("Cheese", 2), ("Item1", 2), ("Stick", 1)]

        self.current_step_number = 0
        self.step1 = ["turning_left", "rest", "walk_left", "rest", "turning_right", "rest", "walk_right", "rest"]
        self.walk_pattern = "random"

        self.room = room
        self.gd_input.room_list[self.room].add_room_character(self.name)

    def activate_timers(self):
        pygame.time.set_timer(self.initiate, 1000)
        pygame.time.set_timer(self.action_clock, 80)

    def do_activity(self):
        if self.state == "idle":
            result = None
            if self.walk_pattern == "step1":
                if self.current_step_number == len(self.step1) - 1:
                    self.current_step_number = 0
                elif self.current_step_number < len(self.step1) - 1:
                    self.current_step_number += 1
                result = self.step1[self.current_step_number]
            elif self.walk_pattern == "random":
                result = choice(self.actions)

            if self.walk_pattern == "rest":
                pass

            elif self.walk_pattern == "turning_front":
                self.turn_front()

    def get_interacted_with(self):
        print("I, a shopkeeper, got interacted with")
        # TODO: Fix all of this mess - make their picture pop up in their speech bubble thing
        if self.state == "idle":
            if self.gd_input.player["Player"].facing == Direction.UP:
                self.turn_front()
            elif self.gd_input.player["Player"].facing == Direction.DOWN:
                self.turn_back()
            elif self.gd_input.player["Player"].facing == Direction.LEFT:
                self.turn_right()
            elif self.gd_input.player["Player"].facing == Direction.RIGHT:
                self.turn_left()
            self.gc_input.set_keyboard_manager(InRegularMenu.ID)
            # self.GameController.set_current_menu("conversation_options_menu")
            self.gd_input.menu_list["shopkeeper_interact_menu"].set_menu(self.name)
            self.set_state("selling")

    def speak(self, chosen_phrase):
        my_font = pygame.font.Font(self.gc_input.font, 10)
        item = my_font.render(self.name + ":", 1, (0, 0, 0))
        self.gc_input.screen.blit(item, (
            self.gd_input.overlay_list["text_box"].x + 150, self.gd_input.overlay_list["text_box"].y + 20))

        my_font = pygame.font.Font(self.gc_input.font, 10)
        item = my_font.render(chosen_phrase, 1, (0, 0, 0))
        self.gc_input.screen.blit(item, (self.gd_input.overlay_list["text_box"].x + 150, self.gd_input.overlay_list["text_box"].y + 60))

    def speak_items(self):
        for item in self.items_list:
            print(item)

    def display_name(self):
        my_font = pygame.font.Font(self.gc_input.font, 10)
        item = my_font.render(self.name + ":", 1, (0, 0, 0))
        self.gc_input.screen.blit(item, (self.gd_input.overlay_list["text_box"].x + 150, self.gd_input.overlay_list["text_box"].y + 20))

    def test_speak(self):
        text_line = 0
        for line in self.current_phrase:
            my_font = pygame.font.Font(self.gc_input.font, 10)
            item = my_font.render(line, 1, (0, 0, 0))
            self.gc_input.screen.blit(item, (self.gd_input.overlay_list["text_box"].x + 150, self.gd_input.overlay_list["text_box"].y + 60 + 25 * text_line))
            text_line += 1

    def set_current_phrase(self):
        self.current_phrase = textwrap.wrap(self.phrase, width=30)

    def set_speaking_queue(self):

        phrase_counter = 0
        self.speaking_queue = []
        for line in range(3):
            if len(self.current_phrase) > 0:
                self.speaking_queue.append(self.current_phrase[0])
                self.current_phrase.pop(0)

        if len(self.current_phrase) == 0:
            self.current_phrase = None

    def clear_speaking_queue(self):
        self.speaking_queue = None


class ShopKeeperTamma(ShopKeeper):
    IDLE = "idle"
    AVAILABLE_STATES = [IDLE]

    def __init__(self, x, y, gc_input, gd_input, room):
        super().__init__(x, y, gc_input, gd_input, room)

        self.actions = ["turning_left", "turning_front", "turning_right", "rest", "rest", "rest", "rest"]
        self.available_actions = ["turning_front"]
        self.spritesheet = Spritesheet("assets/NPC_sprites/Tamma_CS.png", 32, 40)
        self.state = "idle"
        self.phrase = "Hi, welcome to my store, what would you like to do?"
        self.current_phrase = None
        self.speaking_queue = None #textwrap.wrap("Hi everyone, it's so nice to see you here today! I hope you have all been doing well", width=30)
        self.img = self.spritesheet.get_image(0, 0)
        self.imagex = x
        self.imagey = y
        self.name = "Tamma"
        self.items_list = [("Cheese", 2), ("Item1", 2), ("Stick", 1)]

        self.current_step_number = 0
        self.step1 = ["turning_left", "rest", "walk_left", "rest", "turning_right", "rest", "walk_right", "rest"]
        self.walk_pattern = "turning_front"

        self.room = room
        self.gd_input.room_list[self.room].add_room_character(self.name)
        self.face_image = Spritesheet("assets/NPC_sprites/faces/TammaFace.png", 150, 150).get_image(0, 0)

class ShopKeeperCheryl(ShopKeeper):
    IDLE = "idle"
    AVAILABLE_STATES = [IDLE]

    def __init__(self, x, y, gc_input, gd_input, room):
        super().__init__(x, y, gc_input, gd_input, room)

        self.actions = ["turning_left", "turning_front", "turning_right", "rest", "rest", "rest", "rest"]
        self.available_actions = ["turning_front"]
        self.spritesheet = Spritesheet("assets/NPC_sprites/Sub_CS.png", 32, 40)
        self.state = "idle"
        self.phrase = "Hi, welcome to the bookstore, what would you like to do?"
        self.current_phrase = None
        self.speaking_queue = None  # textwrap.wrap("Hi everyone, it's so nice to see you here today! I hope you have all been doing well", width=30)
        self.img = self.spritesheet.get_image(0, 0)
        self.imagex = x
        self.imagey = y
        self.name = "Cheryl"
        self.items_list = [("Book 1", 5), ("Book 2", 7), ("Book 3", 10)]

        self.current_step_number = 0
        self.step1 = ["turning_left", "rest", "walk_left", "rest", "turning_right", "rest", "walk_right", "rest"]
        self.walk_pattern = "turning_front"

        self.room = room
        self.gd_input.room_list[self.room].add_room_character(self.name)
        self.face_image = Spritesheet("assets/NPC_sprites/faces/NeutralFace.png", 150, 150).get_image(0, 0)
