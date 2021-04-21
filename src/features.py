import pygame
from spritesheet import *
from random import choice

class Feature(object):
    def __init__(self, x, y, imagex, imagey, width, height, img_file_name_list, name):
        self.x = x
        self.y = y
        self.imagex = imagex
        self.imagey = imagey
        self.name = name
        self.width = width
        self.height = height
        self.img_list = [file_name for file_name in
                         img_file_name_list]
        self.cur_img = 0
        self.img = self.img_list[self.cur_img]

    def set_image(self, img_number):
        self.cur_img = img_number
        self.img = self.img_list[self.cur_img]

    def draw(self, screen):
        screen.blit(Spritesheet(self.img).image_at((0, 0, self.width, self.height)), [self.imagex*32, self.imagey*40])

class Person(Feature):

    UPDATE_COLOUR_EVENT = pygame.USEREVENT + 5

    def __init__(self, x, y, imagex, imagey, width, height, img_file_name_list, name, facing):
        super().__init__(x, y, imagex, imagey, width, height, img_file_name_list, name)

        self.activity = None
        self.facing = facing
        self.printing_priority = 2

    def draw(self, screen):
        screen.blit(Spritesheet(self.img).image_at((0, 0, self.width, self.height)), [self.imagex*32, self.imagey*40])

    def update_behaviour(self, some_parameter=None):
        '''
        Updates character behavior based onn timer
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

    def change_green(self):
        self.set_image(0)

    def change_red(self):
        self.set_image(1)

    def change_blue(self):
        self.set_image(2)

class Player(Person):
    def __init__(self, x, y, imagex, imagey, width, height, img_file_name_list, name, facing, GameController, GameData, type = "player"):
        super().__init__(x, y, imagex, imagey, width, height, img_file_name_list, name, facing)
        self.front = ["assets/player/P_front.png", "assets/player/P_front.png", "assets/player/P_front.png", "assets/player/P_front.png", "assets/player/P_front.png", "assets/player/P_front.png", "assets/player/P_front.png", "assets/player/P_front.png"]
        self.back = ["assets/player/P_back.png", "assets/player/P_back.png", "assets/player/P_back.png", "assets/player/P_back.png", "assets/player/P_back.png", "assets/player/P_back.png", "assets/player/P_back.png", "assets/player/P_back.png"]
        self.left = ["assets/player/P_left.png", "assets/player/P_left.png", "assets/player/P_left.png", "assets/player/P_left.png", "assets/player/P_left.png", "assets/player/P_left.png", "assets/player/P_left.png", "assets/player/P_left.png"]
        self.right = ["assets/player/P_right.png", "assets/player/P_right.png", "assets/player/P_right.png", "assets/player/P_right.png", "assets/player/P_right.png", "assets/player/P_right.png", "assets/player/P_right.png", "assets/player/P_right.png"]
        self.state = "idle"
        self.GameController = GameController
        self.GameData = GameData
        self.type = type
        self.printing_priority = 2

    def draw(self, screen):
        screen.blit(Spritesheet(self.img).image_at((0, 0, self.width, self.height)),
                    [self.imagex * 32, (self.imagey * 40)-4])

    def turn_left(self):
        self.img_list = [file_name for file_name in self.left]
        self.img = self.img_list[self.cur_img]
        self.facing = "left"

    def turn_right(self):
        self.img_list = [file_name for file_name in self.right]
        self.img = self.img_list[self.cur_img]
        self.facing = "right"

    def turn_front(self):
        self.img_list = [file_name for file_name in self.front]
        self.img = self.img_list[self.cur_img]
        self.facing = "front"

    def turn_back(self):
        self.img_list = [file_name for file_name in self.back]
        self.img = self.img_list[self.cur_img]
        self.facing = "back"

    def walk_left(self):
        self.state = "walk_left"
        self.GameData.positioner[self.GameController.room].empty_tile(self)
        self.x -= 1
        self.GameData.positioner[self.GameController.room].fill_tile(self)

    def walk_right(self):
        self.state = "walk_right"
        self.GameData.positioner[self.GameController.room].empty_tile(self)
        self.x += 1
        self.GameData.positioner[self.GameController.room].fill_tile(self)

    def walk_front(self):
        self.state = "walk_front"
        self.GameData.positioner[self.GameController.room].empty_tile(self)
        self.y += 1
        self.GameData.positioner[self.GameController.room].fill_tile(self)

    def walk_back(self):
        self.state = "walk_back"
        self.GameData.positioner[self.GameController.room].empty_tile(self)
        self.y -= 1
        self.GameData.positioner[self.GameController.room].fill_tile(self)

    def walk_cycle(self):
        if self.state == "walk_left":
            if 0 <= self.cur_img < 7:
                self.set_image(self.cur_img + 1)
                self.imagex -= 1/8

            elif self.cur_img == (7):
                self.set_image(0)
                self.imagex -= 1/8
                self.state = "idle"
                self.GameController.UnlockInput()

            else:
                self.cur_img = 0
                self.set_image(0)

        elif self.state == "walk_right":
            if 0 <= self.cur_img < 7:
                self.set_image(self.cur_img + 1)
                self.imagex += 1 / 8

            elif self.cur_img == (7):
                self.set_image(0)
                self.imagex += 1 / 8
                self.state = "idle"
                self.GameController.UnlockInput()

            else:
                self.cur_img = 0
                self.set_image(0)
        elif self.state == "walk_front":
            if 0 <= self.cur_img < 7:
                self.set_image(self.cur_img + 1)
                self.imagey += 1 / 8

            elif self.cur_img == (7):
                self.set_image(0)
                self.imagey += 1 / 8
                self.state = "idle"
                self.GameController.UnlockInput()

            else:
                self.cur_img = 0
                self.set_image(0)
        elif self.state == "walk_back":
            if 0 <= self.cur_img < 7:
                self.set_image(self.cur_img + 1)
                self.imagey -= 1 / 8

            elif self.cur_img == (7):
                self.set_image(0)
                self.imagey -= 1 / 8
                self.state = "idle"
                self.GameController.UnlockInput()

            else:
                self.cur_img = 0
                self.set_image(0)

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

        facing_tile = self.GameData.room[self.GameController.room].tiles_array[facing_tile_x][facing_tile_y]

        return facing_tile

class NPC(Person):
    def __init__(self, x, y, imagex, imagey, width, height, img_file_name_list, name, state, GameController, GameData, facing, initiate, walk_clock, type = "NPC"):
        super().__init__(x, y, imagex, imagey, width, height, img_file_name_list, name, facing)
        self.state = "idle"
        self.actions = ["walk_left", "walk_right", "walk_front", "walk_back"] #, "idle", "say_hi"]
        self.GameController = GameController
        self.GameData = GameData
        self.type = type
        self.initiate = initiate
        self.walk_clock = walk_clock
        self.printing_priority = 2

    def activate_timers(self):
        pygame.time.set_timer(self.initiate, 500)
        pygame.time.set_timer(self.walk_clock, 60)

    def do_activity(self):

        if self.state == "idle":
            result = choice(self.actions)

            if result == "walk_left":
                self.facing = "left"
                can_walk = self.GameData.positioner[self.GameController.room].can_move(self)
                if can_walk:
                    self.walk_left()

            if result == "walk_right":
                self.facing = "right"
                can_walk = self.GameData.positioner[self.GameController.room].can_move(self)
                if can_walk:
                    self.walk_right()

            if result == "walk_front":
                self.facing = "front"
                can_walk = self.GameData.positioner[self.GameController.room].can_move(self)
                if can_walk:
                    self.walk_front()

            if result == "walk_back":
                self.facing = "back"
                can_walk = self.GameData.positioner[self.GameController.room].can_move(self)
                if can_walk:
                    self.walk_back()

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
            self.state = "idle"

    def walk_left(self):
        self.state = "walk_left"
        self.GameData.positioner[self.GameController.room].empty_tile(self)
        self.x -= 1
        self.GameData.positioner[self.GameController.room].fill_tile(self)


    def walk_right(self):
        self.state = "walk_right"
        self.GameData.positioner[self.GameController.room].empty_tile(self)
        self.x += 1
        self.GameData.positioner[self.GameController.room].fill_tile(self)

    def walk_front(self):
        self.state = "walk_front"
        self.GameData.positioner[self.GameController.room].empty_tile(self)
        self.y += 1
        self.GameData.positioner[self.GameController.room].fill_tile(self)

    def walk_back(self):
        self.state = "walk_back"
        self.GameData.positioner[self.GameController.room].empty_tile(self)
        self.y -= 1
        self.GameData.positioner[self.GameController.room].fill_tile(self)

    def walk_cycle(self):
        if self.state == "walk_left":
            if 0 <= self.cur_img < 7:
                self.set_image(self.cur_img + 1)
                self.imagex -= 1 / 8

            elif self.cur_img == (7):
                self.set_image(0)
                self.imagex -= 1 / 8
                self.state = "idle"

            else:
                self.cur_img = 0
                self.set_image(0)

        elif self.state == "walk_right":
            if 8 <= self.cur_img < 15:
                self.set_image(self.cur_img + 1)
                self.imagex += 1 / 8

            elif self.cur_img == (15):
                self.set_image(8)
                self.imagex += 1 / 8
                self.state = "idle"

            else:
                self.cur_img = 8
                self.set_image(8)

        elif self.state == "walk_front":
            if 0 <= self.cur_img < 7:
                self.set_image(self.cur_img + 1)
                self.imagey += 1 / 8

            elif self.cur_img == (7):
                self.set_image(0)
                self.imagey += 1 / 8
                self.state = "idle"

            else:
                self.cur_img = 0
                self.set_image(0)
        elif self.state == "walk_back":
            if 0 <= self.cur_img < 7:
                self.set_image(self.cur_img + 1)
                self.imagey -= 1 / 8

            elif self.cur_img == (7):
                self.set_image(0)
                self.imagey -= 1 / 8
                self.state = "idle"

            else:
                self.cur_img = 0
                self.set_image(0)

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

        facing_tile = self.GameData.room[self.GameController.room].tiles_array[facing_tile_x][facing_tile_y]

        return facing_tile

class Prop(Feature):
    def __init__(self, x, y, imagex, imagey, width, height, img_file_name_list, name):
        super().__init__(x, y, imagex, imagey, width, height, img_file_name_list, name)

        self.printing_priority = 1