import pygame
from spritesheet import *
from random import choice
from keyboards import *

class Feature(object):
    def __init__(self, x, y, imagex, imagey, width, height, spritesheet, name, GameController, GameData, offset_y):
        self.x = x
        self.y = y
        self.imagex = imagex
        self.imagey = imagey
        self.name = name
        self.width = width
        self.height = height
        self.cur_img = 0
        self.spritesheet = spritesheet
        self.img = self.spritesheet.get_image(0, 0)
        self.GameController = GameController
        self.GameData = GameData
        self.offset_y = offset_y


    def set_image(self, img_x, img_y):
        self.img = self.spritesheet.get_image(img_x, img_y)

class Interactable(object):
    def __init__(self):
        pass

    def get_interacted_with(self):
        pass


class Person(Feature):

    UPDATE_COLOUR_EVENT = pygame.USEREVENT + 5

    def __init__(self, x, y, imagex, imagey, width, height, spritesheet, name, GameController, GameData, facing, feature_type, offset_y = 24):

        super().__init__(x, y, imagex, imagey, width, height, spritesheet, name, GameController, GameData, offset_y)

        self.activity = None
        self.facing = facing
        self.printing_priority = 2
        self.feature_type = feature_type

    def update_behaviour(self, some_parameter=None):
        '''
        Updates character behavior based on timer
        :param some_parameter: some useless parameter
        :return: time until next update in milliseconds
        '''
        time_to_next_update = 500
        if self.activity == None:
            self.activity = "be_red"
            self.change_red()
        elif self.activity == "be_red":
            self.activity = "be_green"
            self.change_green()
        elif self.activity == "be_green":
            self.activity = "be_blue"
            self.change_blue()
        elif self.activity == "be_blue":
            self.activity = "be_red"
            self.change_red()

        return time_to_next_update

class Player(Person):
    def __init__(self, x, y, imagex, imagey, width, height, spritesheet, name, GameController, GameData):
        super().__init__(x, y, imagex, imagey, width, height, spritesheet, name, GameController, GameData, facing="front", feature_type="Player", offset_y=10)
        self.front = ["assets/player/P_front_1.png", "assets/player/P_front_2.png", "assets/player/P_front_3.png", "assets/player/P_front_4.png", "assets/player/P_front_1.png", "assets/player/P_front_2.png", "assets/player/P_front_3.png", "assets/player/P_front_4.png"]
        self.back = ["assets/player/P_back_1.png", "assets/player/P_back_2.png", "assets/player/P_back_3.png", "assets/player/P_back_4.png", "assets/player/P_back_1.png", "assets/player/P_back_2.png", "assets/player/P_back_3.png", "assets/player/P_back_4.png"]
        self.left = ["assets/player/P_left_1.png", "assets/player/P_left_2.png", "assets/player/P_left_3.png", "assets/player/P_left_4.png", "assets/player/P_left_1.png", "assets/player/P_left_2.png", "assets/player/P_left_3.png", "assets/player/P_left_4.png"]
        self.right = ["assets/player/P_right_1.png", "assets/player/P_right_2.png", "assets/player/P_right_3.png", "assets/player/P_right_4.png", "assets/player/P_right_1.png", "assets/player/P_right_2.png", "assets/player/P_right_3.png", "assets/player/P_right_4.png"]
        self.state = "idle"
        self.printing_priority = 2
        self.step_timer = pygame.USEREVENT + 7

    def activate_timer(self):
        pygame.time.set_timer(self.step_timer, 20)


    def draw(self, screen):
        screen.blit(self.img, [(self.imagex * self.GameData.square_size[0])+self.GameData.base_locator_x,
                               ((self.imagey * self.GameData.square_size[1])-self.offset_y)+self.GameData.base_locator_y])

    def turn_left(self):
        self.set_image(0, 3)
        self.facing = "left"


    def turn_right(self):
        self.set_image(0, 2)
        self.facing = "right"

    def turn_front(self):
        self.set_image(0, 0)
        self.facing = "front"

    def turn_back(self):
        self.set_image(0, 1)
        self.facing = "back"

    def walk_left(self):
        self.state = "walk_left"
        self.GameData.positioner[self.GameController.current_room].empty_tile(self)
        self.x -= 1
        self.GameData.positioner[self.GameController.current_room].fill_tile(self)

    def walk_right(self):
        self.state = "walk_right"
        self.GameData.positioner[self.GameController.current_room].empty_tile(self)
        self.x += 1
        self.GameData.positioner[self.GameController.current_room].fill_tile(self)

    def walk_front(self):
        self.state = "walk_front"
        self.GameData.positioner[self.GameController.current_room].empty_tile(self)
        self.y += 1
        self.GameData.positioner[self.GameController.current_room].fill_tile(self)

    def walk_back(self):
        self.state = "walk_back"
        self.GameData.positioner[self.GameController.current_room].empty_tile(self)
        self.y -= 1
        self.GameData.positioner[self.GameController.current_room].fill_tile(self)

    def walk_cycle(self):
        if self.state == "walk_left":
            if 0 <= self.cur_img < 3:
                self.cur_img += 1
                self.set_image(self.cur_img, 3)
                self.GameController.camera[0] += 1/4

            elif self.cur_img == (3):
                self.cur_img = 0
                self.set_image(self.cur_img, 3)
                self.GameController.camera[0] += 1 / 4
                self.set_state("idle")
                self.GameController.UnlockInput()

            else:
                self.cur_img = 0
                self.set_image(0, 3)

        elif self.state == "walk_right":
            if 0 <= self.cur_img < 3:
                self.cur_img += 1
                self.set_image(self.cur_img, 2)
                self.GameController.camera[0] -= 1 / 4

            elif self.cur_img == (3):
                self.cur_img = 0
                self.set_image(self.cur_img, 2)
                self.GameController.camera[0] -= 1 / 4
                self.set_state("idle")
                self.GameController.UnlockInput()

            else:
                self.cur_img = 0
                self.set_image(0, 2)

        elif self.state == "walk_front":
            if 0 <= self.cur_img < 3:
                self.cur_img += 1
                self.set_image(self.cur_img, 0)
                self.GameController.camera[1] -= 1 / 4

            elif self.cur_img == (3):
                self.cur_img = 0
                self.set_image(self.cur_img, 0)
                self.GameController.camera[1] -= 1 / 4
                self.set_state("idle")
                self.GameController.UnlockInput()

            else:
                self.cur_img = 0
                self.set_image(0, 0)


        elif self.state == "walk_back":
            if 0 <= self.cur_img < 3:
                self.cur_img += 1
                self.set_image(self.cur_img, 1)

                self.GameController.camera[1] += 1 / 4

            elif self.cur_img == (3):
                self.cur_img = 0
                self.set_image(self.cur_img, 1)
                self.GameController.camera[1] += 1 / 4
                self.set_state("idle")
                self.GameController.UnlockInput()

            else:
                self.cur_img = 0
                self.set_image(0, 1)

    def check_if_walking(self):
        if self.state == "walk_left":
            self.walk_cycle()

        elif self.state == "walk_right":
            self.walk_cycle()

        elif self.state == "walk_back":
            self.walk_cycle()

        elif self.state == "walk_front":
            self.walk_cycle()

    def get_facing_tile(self):

        facing_tile_y = 0
        facing_tile_x = 0
        if self.facing == "back":
            facing_tile_y = int(self.y - 1)
            facing_tile_x = int(self.x)

        elif self.facing == "front":
            facing_tile_y = int(self.y + 1)
            facing_tile_x = int(self.x)

        elif self.facing == "left":
            facing_tile_y = int(self.y)
            facing_tile_x = int(self.x - 1)

        elif self.facing == "right":
            facing_tile_y = int(self.y)
            facing_tile_x = int(self.x + 1)

        facing_tile = self.GameData.room_list[self.GameController.current_room].tiles_array[facing_tile_x][facing_tile_y]

        return facing_tile

    def interact(self):
        facing_tile = self.get_facing_tile()
        object_filling = facing_tile.object_filling
        filling_type = facing_tile.filling_type
        full = facing_tile.full

        if full:

            if filling_type in ["Pixie","Walker"]:
                self.GameData.character_list[object_filling].get_interacted_with()

            elif filling_type == "Prop":
                self.GameData.prop_list[object_filling].get_interacted_with()

            elif filling_type == "Door":
                pass
            else:
                pass

    def set_state(self, state_to_set):
        self.state = state_to_set

class NPC(Person):

    NPC_TIMER_ID = 10
    

    def __init__(self, x, y, imagex, imagey, width, height, spritesheet, name, GameController, GameData, facing, feature_type, offset_y):

        super().__init__(x, y, imagex, imagey, width, height, spritesheet, name, GameController, GameData, facing, feature_type, offset_y)

        self.set_state("idle")
        self.facing = "front"
        self.initiate = pygame.USEREVENT + NPC.NPC_TIMER_ID
        self.action_clock = pygame.USEREVENT + NPC.NPC_TIMER_ID + 1
        self.printing_priority = 2

        NPC.NPC_TIMER_ID += 2

    # TODO: make sets of walking behaviour types that different NPC can have (back and forth/look around/square/etc.)

    def turn_left(self):
        self.set_image(0, 3)
        self.facing = "left"
        self.set_state("idle")
        self.set_state("idle")

    def turn_right(self):
        self.set_image(1, 2)
        self.facing = "right"
        self.set_state("idle")

    def turn_front(self):
        self.set_image(0, 0)
        self.facing = "front"
        self.set_state("idle")

    def turn_back(self):
        self.set_image(0, 1)
        self.facing = "back"
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
        self.GameData.positioner[self.GameController.current_room].empty_tile(self)
        self.x -= 1
        self.GameData.positioner[self.GameController.current_room].fill_tile(self)

    def walk_right(self):
        self.set_state("walk_right")
        self.GameData.positioner[self.GameController.current_room].empty_tile(self)
        self.x += 1
        self.GameData.positioner[self.GameController.current_room].fill_tile(self)

    def walk_front(self):
        self.set_state("walk_front")
        self.GameData.positioner[self.GameController.current_room].empty_tile(self)
        self.y += 1
        self.GameData.positioner[self.GameController.current_room].fill_tile(self)

    def walk_back(self):
        self.set_state("walk_back")
        self.GameData.positioner[self.GameController.current_room].empty_tile(self)
        self.y -= 1
        self.GameData.positioner[self.GameController.current_room].fill_tile(self)

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
                self.set_image(self.cur_img, 0)
                self.cur_img = 0
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
        if self.facing == "back":
            facing_tile_y = int(self.y - 1)
            facing_tile_x = int(self.x)

        elif self.facing == "front":
            facing_tile_y = int(self.y + 1)
            facing_tile_x = int(self.x)

        elif self.facing == "left":
            facing_tile_y = int(self.y)
            facing_tile_x = int(self.x - 1)

        elif self.facing == "right":
            facing_tile_y = int(self.y)
            facing_tile_x = int(self.x + 1)

        facing_tile = self.GameData.room_list[self.GameController.current_room].tiles_array[facing_tile_x][
            facing_tile_y]

        return facing_tile

    def draw(self, screen):
        screen.blit(self.img, [((self.imagex + self.GameController.camera[0]) * self.GameData.square_size[0])
                               + self.GameData.base_locator_x, ((self.imagey + self.GameController.camera[1])
                                                                * self.GameData.square_size[
                                                                    1] - self.offset_y) + self.GameData.base_locator_y])

    def set_phrase(self, phrase_to_set):
        self.current_phrase = phrase_to_set

    def set_state(self, state_to_set):
        self.state = state_to_set


class Pixie(NPC):
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

    def __init__(self, x, y, imagex, imagey, width, height, spritesheet, name, GameController, GameData, current_phrase):
        super().__init__(x, y, imagex, imagey, width, height, spritesheet, name, GameController, GameData, facing = "front", feature_type="Pixie", offset_y=10)
        assert self.state in self.AVAILABLE_STATES
        self.actions = ["walk_left", "walk_right", "walk_front", "walk_back", "turning_left", "turning_front", "turning_right", "turning_back"]
        self.available_actions = ["turn"]
        self.spritesheet = spritesheet
        self.current_phrase = "Hi, how are you today??"
        self.state = "idle"
        self.current_phrase = current_phrase

    def activate_timers(self):
        pygame.time.set_timer(self.initiate, 1000)
        pygame.time.set_timer(self.action_clock, 60)

    def do_activity(self):
        if self.state == "idle":
            result = choice(self.actions)
            #self.state = result

            if result == "walk_left":
                self.facing = "left"
                can_walk = self.GameData.positioner[self.GameController.current_room].can_move(self)
                if can_walk:
                    self.walk_left()

            elif result == "walk_right":
                self.facing = "right"
                can_walk = self.GameData.positioner[self.GameController.current_room].can_move(self)
                if can_walk:
                    self.walk_right()

            elif result == "walk_front":
                self.facing = "front"
                can_walk = self.GameData.positioner[self.GameController.current_room].can_move(self)
                if can_walk:
                    self.walk_front()

            elif result == "walk_back":
                self.facing = "back"
                can_walk = self.GameData.positioner[self.GameController.current_room].can_move(self)
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
            if self.GameData.player["Player"].facing == "back":
                self.turn_front()
            elif self.GameData.player["Player"].facing == "front":
                self.turn_back()
            elif self.GameData.player["Player"].facing == "left":
                self.turn_right()
            elif self.GameData.player["Player"].facing == "right":
                self.turn_left()
            self.GameController.set_keyboard_manager(InTalkingMenuKeyboardManager.ID)
            self.GameController.set_menu("character_interact_menu")
            self.set_state("talking")


    def speak(self, chosen_phrase):
        print("speaking")
        my_font = pygame.font.Font(self.GameController.font, 10)
        item = my_font.render(self.name + ":", 1, (0, 0, 0))
        self.GameController.screen.blit(item, (
        self.GameData.overlay_list["text_box"].x + 80, self.GameData.overlay_list["text_box"].y + 20))

        my_font = pygame.font.Font(self.GameController.font, 10)
        item = my_font.render(chosen_phrase, 1, (0, 0, 0))
        self.GameController.screen.blit(item, (self.GameData.overlay_list["text_box"].x + 80, self.GameData.overlay_list["text_box"].y + 40))


class Prop(Feature):
    def __init__(self, x, y, imagex, imagey, width, height, spritesheet, name, GameController, GameData, size_x, size_y, offset_y=10):
        super().__init__(x, y, imagex, imagey, width, height, spritesheet, name, GameController, GameData, offset_y)
        self.printing_priority = 1
        self.size_x = size_x
        self.size_y = size_y
        self.feature_type = "Prop"

    def draw(self, screen):
        screen.blit(self.img, [((self.imagex + self.GameController.camera[0]) * self.GameData.square_size[0])
                                + self.GameData.base_locator_x,  ((self.imagey + self.GameController.camera[1])
                                * self.GameData.square_size[1] - self.offset_y) + self.GameData.base_locator_y])


    def get_interacted_with(self):
        print("I'm a " + self.name + "!")

class Decoration(Prop):
    def __init__(self, x, y, imagex, imagey, width, height, spritesheet, name, GameController, GameData, size_x, size_y, location_list):
        super().__init__(x, y, imagex, imagey, width, height, spritesheet, name, GameController, GameData, size_x, size_y)
        self.location_list = location_list
        self.offset_y = 10

    def draw(self, screen):
        for location in self.location_list:
            screen.blit(self.img,[((location[0] + self.GameController.camera[0]) * self.GameData.square_size[
                            0]) + self.GameData.base_locator_x, (((location[1] + self.GameController.camera[1]) *
                            self.GameData.square_size[1]) - self.offset_y) + self.GameData.base_locator_y])
