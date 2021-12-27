import csv
import os

from features import Feature
from spritesheet import Spritesheet


class Prop(Feature):
    def __init__(self, x, y, gc_input, gd_input):
        super().__init__(x, y, gc_input, gd_input)
        self.imagey = y
        self.imagex = x
        self.drawing_priority = 1
        self.size_x = None
        self.size_y = None
        self.feature_type = "Prop"
        self.width = None
        self.height = None
        self.spritesheet = Spritesheet("assets/prop_sprites/image_error.png", 32, 32)
        self.img = self.spritesheet.get_image(0, 0)
        self.name = None
        self.offset_y = 16
        self.room = None

        try:
            self.gd_input.room_list[self.room].add_room_prop(self.name)
        except:
            pass

    def draw(self, screen):
        screen.blit(self.img, [((self.imagex + self.gc_input.camera[0]) * self.gd_input.square_size[0])
                               + self.gd_input.base_locator_x, ((self.imagey + self.gc_input.camera[1])
                                                                * self.gd_input.square_size[1] - self.offset_y) + self.gd_input.base_locator_y])
    #TODO: Fix this!
    def get_interacted_with(self):
        print("I'm a " + self.name + "!")

class GenericProp(Prop):
    def __init__(self, x, y, gc_input, gd_input, width, height, spritesheet, name, size_x, size_y, room):
        super().__init__(x, y, gc_input, gd_input)
        self.imagey = y
        self.imagex = x
        self.drawing_priority = 1
        self.size_x = size_x
        self.size_y = size_y
        self.feature_type = "Prop"
        self.width = width
        self.height = height
        self.spritesheet = spritesheet
        self.img = self.spritesheet.get_image(0, 0)
        self.name = name
        self.offset_y = 20
        self.room = room

        try:
            self.gd_input.room_list[self.room].add_room_prop(self.name)
        except:
            pass

    def draw(self, screen):
        screen.blit(self.img, [((self.imagex + self.gc_input.camera[0]) * self.gd_input.square_size[0])
                               + self.gd_input.base_locator_x, ((self.imagey + self.gc_input.camera[1])
                                                                * self.gd_input.square_size[1] - self.offset_y) + self.gd_input.base_locator_y])

    #TODO: Fix this!
    def get_interacted_with(self):
        print("I'm a " + self.name + "!")

class Decoration(Feature):
    def __init__(self, x, y, gc_input, gd_input, width, height, spritesheet, name, size_x, size_y, location_list, room):
        super().__init__(x, y, gc_input, gd_input)
        self.location_list = location_list
        self.offset_y = 3
        self.width = width
        self.height = height
        self.spritesheet = spritesheet
        self.img = self.spritesheet.get_image(0, 0)
        self.name = name
        self.size_x = size_x
        self.size_y = size_y
        self.room = room
        self.drawing_priority = 1

        self.gd_input.room_list[self.room].add_room_decoration(self.name)

    def draw(self, screen):
        for location in self.location_list:
            screen.blit(self.img, [((location[0] + self.gc_input.camera[0]) * self.gd_input.square_size[
                            0]) + self.gd_input.base_locator_x, (((location[1] + self.gc_input.camera[1]) *
                                                                  self.gd_input.square_size[1]) - self.offset_y) + self.gd_input.base_locator_y])

class Tree(Prop):
    def __init__(self, x, y, name, gc_input, gd_input, room_name):
        super().__init__(x, y, gc_input, gd_input)
        self.drawing_priority = 1
        self.imagex = x
        self.imagey = y
        self.width = 64
        self.height = 96
        self.spritesheet = Spritesheet("assets/prop_sprites/tree.png", 64, 96)
        self.name = name
        self.size_x = 2
        self.size_y = 1
        self.offset_y = 64
        self.feature_type = "Prop"
        self.cur_img = 0
        self.img = self.spritesheet.get_image(0, 0)
        self.gc_input = gc_input
        self.gd_input = gd_input
        self.room = room_name

        self.gd_input.room_list[self.room].add_room_prop(self.name)

    def draw(self, screen):
        screen.blit(self.img, [((self.imagex + self.gc_input.camera[0]) * self.gd_input.square_size[0])
                               + self.gd_input.base_locator_x, ((self.imagey + self.gc_input.camera[1])
                                * self.gd_input.square_size[1] - self.offset_y) + self.gd_input.base_locator_y])


    #TODO: Fix this!
    def get_interacted_with(self):
        print("I'm a " + self.name + "!")

class PlumTree(Prop):
    def __init__(self, x, y, name, gc_input, gd_input, room_name):
        super().__init__(x, y, gc_input, gd_input)
        self.drawing_priority = 1
        self.imagex = x
        self.imagey = y
        self.width = 96
        self.height = 128
        self.spritesheet = Spritesheet("assets/prop_sprites/ringside_tree.png", 96, 128)
        self.name = name
        self.size_x = 1
        self.size_y = 1
        self.offset_y = 64
        self.feature_type = "Prop"
        self.cur_img = 0
        self.img = self.spritesheet.get_image(0, 0)
        self.gc_input = gc_input
        self.gd_input = gd_input
        self.room = room_name

        self.gd_input.room_list[self.room].add_room_prop(self.name)

    def draw(self, screen):
        screen.blit(self.img, [((self.imagex + self.gc_input.camera[0]) * self.gd_input.square_size[0])
                               + self.gd_input.base_locator_x, ((self.imagey + self.gc_input.camera[1])
                                * self.gd_input.square_size[1] - self.offset_y) + self.gd_input.base_locator_y])


    #TODO: Fix this!
    def get_interacted_with(self):
        print("I'm a " + self.name + "!")

class PicnicTable(Prop):
    def __init__(self, x, y, name, gc_input, gd_input, room_name):
        super().__init__(x, y, gc_input, gd_input)
        self.drawing_priority = 1
        self.imagex = x
        self.imagey = y
        self.width = 64
        self.height = 64
        self.spritesheet = Spritesheet("assets/prop_sprites/picnic_table.png", 64, 64)
        self.name = name
        self.size_x = 2
        self.size_y = 2
        self.offset_y = 0
        self.feature_type = "Prop"
        self.cur_img = 0
        self.img = self.spritesheet.get_image(0, 0)
        self.gc_input = gc_input
        self.gd_input = gd_input
        self.room = room_name

        self.gd_input.room_list[self.room].add_room_prop(self.name)

    def draw(self, screen):
        screen.blit(self.img, [((self.imagex + self.gc_input.camera[0]) * self.gd_input.square_size[0])
                               + self.gd_input.base_locator_x, ((self.imagey + self.gc_input.camera[1])
                                * self.gd_input.square_size[1] - self.offset_y) + self.gd_input.base_locator_y])


    #TODO: Fix this!
    def get_interacted_with(self):
        print("I'm a " + self.name + "!")

class Building(Prop):
    def __init__(self, x, y, gc_input, gd_input, width, height, spritesheet, name, size_x, size_y, room, fill_csv):
        super().__init__(x, y, gc_input, gd_input)
        self.imagey = y
        self.imagex = x
        self.drawing_priority = 1
        self.size_x = size_x
        self.size_y = size_y
        self.width = width
        self.height = height
        self.spritesheet = Spritesheet(spritesheet, self.width, self.height)
        self.img = self.spritesheet.get_image(0, 0)
        self.name = name
        self.offset_y = -10
        self.room = room
        # TODO: use this to make people walk behind buildings
        self.building_height = 1

        self.fill_csv = fill_csv
        self.feature_type = "Building"
        self.fill_map = self.read_csv(self.fill_csv)

        self.image_list = []
        for item in range(self.size_y):
            self.image_list.append(self.spritesheet.get_strip(item))
            if self.name == "Coop_Building":
                print(self.spritesheet.get_strip(item))

        try:
            self.gd_input.room_list[self.room].add_room_prop(self.name)
        except:
            pass

    def draw(self, screen):
        screen.blit(self.img, [((self.imagex + self.gc_input.camera[0]) * self.gd_input.square_size[0])
                               + self.gd_input.base_locator_x, ((self.imagey + self.gc_input.camera[1])
                                                                * self.gd_input.square_size[1] - self.offset_y) + self.gd_input.base_locator_y])

    def draw_strip(self, screen, strip):
        screen.blit(self.image_list[strip-1], [((self.imagex + self.gc_input.camera[0]) * self.gd_input.square_size[0])
                               + self.gd_input.base_locator_x, ((self.imagey + self.gc_input.camera[1])
                                                                * self.gd_input.square_size[1] - self.offset_y) + self.gd_input.base_locator_y+((int(strip-1))*32)])

    def read_csv(self, filename):
        map = []
        with open(os.path.join(filename)) as data:
            data = csv.reader(data, delimiter=',')
            for row in data:
                map.append(list(row))
        return map

class BenchHorizontal(Prop):
    def __init__(self, x, y, name, gc_input, gd_input, room_name):
        super().__init__(x, y, gc_input, gd_input)
        self.drawing_priority = 1
        self.imagex = x
        self.imagey = y
        self.width = (3*32)
        self.height = (1*32)
        self.spritesheet = Spritesheet("assets/prop_sprites/bench_horizontal.png", 96, 32)
        self.name = name
        self.size_x = 3
        self.size_y = 1
        self.offset_y = 0
        self.feature_type = "Prop"
        self.cur_img = 0
        self.img = self.spritesheet.get_image(0, 0)
        self.gc_input = gc_input
        self.gd_input = gd_input
        self.room = room_name

        self.gd_input.room_list[self.room].add_room_prop(self.name)

    def draw(self, screen):
        screen.blit(self.img, [((self.imagex + self.gc_input.camera[0]) * self.gd_input.square_size[0])
                               + self.gd_input.base_locator_x, ((self.imagey + self.gc_input.camera[1])
                                * self.gd_input.square_size[1] - self.offset_y) + self.gd_input.base_locator_y])

class BenchVertical(Prop):
    def __init__(self, x, y, name, gc_input, gd_input, room_name):
        super().__init__(x, y, gc_input, gd_input)
        self.drawing_priority = 1
        self.imagex = x
        self.imagey = y
        self.width = (3*32)
        self.height = (1*32)
        self.spritesheet = Spritesheet("assets/prop_sprites/bench_vertical.png", 32, 96)
        self.name = name
        self.size_x = 1
        self.size_y = 3
        self.offset_y = 0
        self.feature_type = "Prop"
        self.cur_img = 0
        self.img = self.spritesheet.get_image(0, 0)
        self.gc_input = gc_input
        self.gd_input = gd_input
        self.room = room_name

        self.gd_input.room_list[self.room].add_room_prop(self.name)

    def draw(self, screen):
        screen.blit(self.img, [((self.imagex + self.gc_input.camera[0]) * self.gd_input.square_size[0])
                               + self.gd_input.base_locator_x, ((self.imagey + self.gc_input.camera[1])
                                * self.gd_input.square_size[1] - self.offset_y) + self.gd_input.base_locator_y])

class Computer(Prop):
    def __init__(self, x, y, name, gc_input, gd_input, room_name):
        super().__init__(x, y, gc_input, gd_input)
        self.drawing_priority = 1
        self.imagex = x
        self.imagey = y
        self.width = (1*32)
        self.height = (2*32)
        self.spritesheet = Spritesheet("assets/prop_sprites/computer.png", 32, 64)
        self.name = name
        self.size_x = 1
        self.size_y = 1
        self.offset_y = 36
        self.feature_type = "Prop"
        self.cur_img = 0
        self.img = self.spritesheet.get_image(0, 0)
        self.gc_input = gc_input
        self.gd_input = gd_input
        self.room = room_name

        self.gd_input.room_list[self.room].add_room_prop(self.name)

    def draw(self, screen):
        screen.blit(self.img, [((self.imagex + self.gc_input.camera[0]) * self.gd_input.square_size[0])
                               + self.gd_input.base_locator_x, ((self.imagey + self.gc_input.camera[1])
                                * self.gd_input.square_size[1] - self.offset_y) + self.gd_input.base_locator_y])

class Counter(Prop):
    def __init__(self, x, y, name, gc_input, gd_input, room_name):
        super().__init__(x, y, gc_input, gd_input)
        self.drawing_priority = 1
        self.imagex = x
        self.imagey = y
        self.width = (1*32)
        self.height = (1*32)
        self.spritesheet = Spritesheet("assets/prop_sprites/counter.png", 32, 32)
        self.name = name
        self.size_x = 1
        self.size_y = 1
        self.offset_y = 2
        self.feature_type = "Prop"
        self.cur_img = 0
        self.img = self.spritesheet.get_image(0, 0)
        self.gc_input = gc_input
        self.gd_input = gd_input
        self.room = room_name

        self.gd_input.room_list[self.room].add_room_prop(self.name)

    def draw(self, screen):
        screen.blit(self.img, [((self.imagex + self.gc_input.camera[0]) * self.gd_input.square_size[0])
                               + self.gd_input.base_locator_x, ((self.imagey + self.gc_input.camera[1])
                                * self.gd_input.square_size[1] - self.offset_y) + self.gd_input.base_locator_y])